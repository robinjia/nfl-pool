"""Module for computing strengths of teams."""
import argparse
import collections
import cvxpy
import itertools
import json
import math
import sys

import table
import util

# How much to weight games from last season compared to this season.
LAST_SEASON_WEIGHT = .25

# Variance of margin of victory for a game.
# Instead of estimating variance from the data,
# we use a historical average, which should be more robust.
# See http://www.pro-football-reference.com/about/win_prob.htm
GAME_VARIANCE = 13.45 ** 2  

# Variance of the prior distribution of team strengths
PRIOR_VARIANCE = 7.0 ** 2

def _ReadArgs():
  parser = argparse.ArgumentParser(description='Compute strengths of teams.  '
                                   'Prints results to stdout.')
  parser.add_argument('year', type=int, help='The current year')
  parser.add_argument('week', type=int,
                      help='The current week.  Represents the week about to be '
                      'played, e.g. week 1 means the season hasn\'t started.')
  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
  return vars(parser.parse_args())


def GetTeamStrengthsSimple(year, week):
  """Computes estimates of team strengths, based on past performance.

  Uses games from both the current season and the last season.  Last season's
  games are weighted less (see LAST_SEASON_WEIGHT)

  Here, we use a simple metric: point differential over the regular season.
  For each team, we find its average margin of victory/defeat, and report that
  as its score s_i.  We model that the margin of victory of team i over team j
  is distributed normally with fixed variance and mean s_i - s_j.  Therefore,
  assuming that the teams in team i's schedule had average score of 0 (i.e.
  the schedule was balanced), the sample mean of margin of victory is the MLE
  for s_i.

  Args:
    year: The current year.
    week: Only use games before this week of the current year.
  Returns:
    JSON-like dictionary structured like: {
        'variance': var,
        'scores': {
            'ARI': s_1,
            'ATL': s_2,
            ...
            'WAS': s_32
        }
    }
  """
  last_season_games = table.FetchPastGames(
      year - 1)[:util.NUM_REGULAR_SEASON_GAMES]  # Only use regular season 
  cur_season_games = [g for g in table.FetchPastGames(year) if
                      g.week.isdigit() and int(g.week) < week]
  total_point_diff = collections.defaultdict(int)
  total_weighted_games = collections.defaultdict(int)

  for game in last_season_games:
    differential = game.GetPointDifferential()
    total_point_diff[game.winning_team] += LAST_SEASON_WEIGHT * differential
    total_weighted_games[game.winning_team] += LAST_SEASON_WEIGHT
    total_point_diff[game.losing_team] -= LAST_SEASON_WEIGHT * differential
    total_weighted_games[game.losing_team] += LAST_SEASON_WEIGHT
  for game in cur_season_games:
    if not game.week.isdigit() or int(game.week) >= week:
      # Game is from post-season or is from current week or after
      continue
    differential = game.GetPointDifferential()
    total_point_diff[game.winning_team] += differential
    total_weighted_games[game.winning_team] += 1
    total_point_diff[game.losing_team] -= differential
    total_weighted_games[game.losing_team] += 1
  scores = {}
  for team in total_point_diff:
    scores[team] = float(total_point_diff[team]) / total_weighted_games[team]

  # Compute sample variance
  # This is not weighted, as we don't expect this to change season to season.
  # Still use only regular season, to avoid any postseason bias.
  total_sq_error = 0
  for game in last_season_games + cur_season_games:
    differential = game.GetPointDifferential()
    estimated_score = scores[game.winning_team] - scores[game.losing_team]
    total_sq_error += (differential - estimated_score)**2
  num_games = len(last_season_games) + len(cur_season_games)
  variance = float(total_sq_error) / (num_games - 1)
  return {'variance': variance, 'scores': scores}


def GetTeamStrengthsMLE(year, week):
  """Computes estimates of team strengths, based on past performance.

  Uses games from both the current season and the last season.  Last season's
  games are weighted less (see LAST_SEASON_WEIGHT).

  Compared to GetTeamStrengthsSimple, this method takes into account strength
  of schedule.  This means we can use postseason games from the previous season
  without introducing bias, and we can incorporate games from early in the
  current season, when teams may have had early-season opponents of very
  different strengths.

  We model that each team has a single strength s_i.  When team i plays team j
  at team i, we model the margin of victory of team i over team j as a Gaussian
  with fixed variance and mean s_i - s_j + k, where k is a constant representing
  average home field advantage.  

  Luckily, we can find the MLE solution exactly, via convex optimization.  We 
  use games from both the current year and previous year, though the previous
  year's games are down-weighted by LAST_SEASON_WEIGHT.

  == More details ==
  We introduce the following notation:
    - n: number of games
    - m: number of teams
    - h_i: home team in game i
    - a_i: away team in game i
    - d_i: (points scored by h_i) - (points scored by a_i) in game i
  
  We can write the log likelihood of the i-th game as
    l_i = -log(sigma_sq) - (s_{h_i} - s_{a_i} + k - d_i)^2/(2 * sigma_sq).
  
  Our overall log likelihood is simply
    ll = \sum_{i=1}^n w_i l_i,
  where w_i is the weight assigned to game i (either 1 or LAST_SEASON_WEIGHT).

  We use GAME_VARIANCE as a fixed variance sigma_Sq, instead of estimating it
  from the data, as it should be better approximated by historical data.

  We also add an L2 regularization term, to avoid making teams too good or too
  bad.  This effectively puts a Gaussian prior on the team strengths.  For
  each team j, we add a penalty 
    s_{j}^2 / (2 * PRIOR_VARIANCE),
  which corresponds to a prior distribution of mean 0 and variance 
  PRIOR_VARIANCE.

  We can find the optimal MAP estimators of s and k by
  solving a simple least squares problem:
    s*, k* = \argmin_{s, k} 1/(2 sigma_sq) \sum_{i=1}^n w_i (s_{h_i} - s_{a_i} + k - d_i)^2
                            + 1/(2 PRIOR_VARIANCE) \sum_{j=1}^m. s_{j} s_j^2
  
  
  Args:
    year: The current year.
    week: Only use games before this week of the current year.
  Returns:
    JSON-like dictionary structured like: {
        'variance': var,
        'home_field': k,
        'scores': {
            'ARI': s_1,
            'ATL': s_2,
            ...
            'WAS': s_32
        }
    }
  """
  # Set up the variables for the least squares problem.
  s = cvxpy.Variable(util.NUM_TEAMS)
  k = cvxpy.Variable()

  # Set up the least squares objective
  obj_fn = 0
  last_season_games = table.FetchPastGames(year - 1)
  cur_season_games = [g for g in table.FetchPastGames(year) if
                      g.week.isdigit() and int(g.week) < week]
  all_games = itertools.chain(last_season_games, cur_season_games)
  weights = ([ LAST_SEASON_WEIGHT ] * len(last_season_games) + 
             [ 1 ] * len(cur_season_games))
  for game, weight in itertools.izip(all_games, weights):
    winning_index = util.GetTeamIndex(game.winning_team)
    losing_index = util.GetTeamIndex(game.losing_team)
    point_diff = game.GetPointDifferential()  # Absolute margin of victory
    if game.home_or_away == table.HOME_TEAM_WON:
      error = s[winning_index] - s[losing_index] + k - point_diff
    elif game.home_or_away == table.HOME_TEAM_LOST:
      error = s[losing_index] - s[winning_index] + k + point_diff
    else:  # Super Bowl, no home team
      error = s[winning_index] - s[losing_index] - point_diff
    obj_fn += weight * cvxpy.square(error)

  # Add L2 Regularization
  # Note: cvxpy had issues when we divided by 2 * variance
  # So instead, the previous terms were not scaled by variance,
  # and we scale this by GAME_VARIANCE / PRIOR_VARIANCE > 1.
  for i in range(util.NUM_TEAMS):
    obj_fn += GAME_VARIANCE / PRIOR_VARIANCE * cvxpy.square(s[i])
  objective = cvxpy.Minimize(obj_fn)

  # Solve the least squares problem
  problem = cvxpy.Problem(objective)
  opt_squared_error = problem.solve()

  # Return JSON-like object
  # To really make it JSON-like, convert numpy arrays returned by cvxpy to float
  return {
      'variance': GAME_VARIANCE,
      'home_field': float(k.value), 
      'scores': collections.OrderedDict(
          itertools.izip(util.TEAM_ABBREVIATIONS, (float(x) for x in s.value)))
  }


def _PrintTeamStrengths(year, week):
  """Prints out team strengths to stdout"""
  team_strengths = GetTeamStrengthsMLE(year, week)
  print json.dumps(team_strengths, indent=2)


if __name__ == '__main__':
  args = _ReadArgs()
  _PrintTeamStrengths(**args)
