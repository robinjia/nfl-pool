"""Module for computing strengths of teams."""
import argparse
import collections
import json
import sys

import table
import util

# How much to weight games from last season compared to this season.
LAST_SEASON_WEIGHT = .25

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


def GetTeamStrengths(year, week):
  """Computes estimates of team strengths, based on past performance.

  Uses games from both the current season and the last season.  Last season's
  games are weighted less (see LAST_SEASON_WEIGHT)

  Currently, we use a simple metric: point differential over the regular season.
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
        'team_scores': {
            'ARI': s_1,
            'ATL': s_2,
            ...
            'WAS': s_32
        }
    }
  """
  last_season_games = table.FetchPastGames(year - 1)
  cur_season_games = table.FetchPastGames(year)
  # Only use regular season 
  last_regular_season_games = last_season_games[:util.NUM_REGULAR_SEASON_GAMES]

  total_point_diff = collections.defaultdict(int)
  total_weighted_games = collections.defaultdict(int)


  for game in last_regular_season_games:
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
  for game in last_regular_season_games + cur_season_games:
    differential = game.GetPointDifferential()
    estimated_score = scores[game.winning_team] - scores[game.losing_team]
    total_sq_error += (differential - estimated_score)**2
  num_games = len(last_regular_season_games) + len(cur_season_games)
  variance = float(total_sq_error) / (num_games - 1)
  return {'variance': variance, 'scores': scores}


def _TeamStrengthsToString(team_strengths, output='json'):
  """Creates a string representation of team strengths.
  
  Args:
    team_strengths: Output of GetTeamStrengths()
    output: 'text' or 'json'
  Returns:
    String of appropriate format.  'json' works as expected.
    'text' creates a space-delimited file with the format:
        [variance]
        ARI [s_1]
        ATL [s_2]
        ...
        WAS [s_32]
  """
  if output == 'json':
    return json.dumps(team_strengths, indent=2)
  elif output == 'text':
    lines = []
    lines.append(str(team_strengths['variance']))
    for team, score in sorted(team_strengths['scores'].items()):
      lines.append('%s %g' % (team, score))
    return '\n'.join(lines)
  else:
    raise ValueError('Unrecognized output format "%s".' % output)


def _PrintTeamStrengths(year, week):
  """Prints out team strengths to stdout"""
  team_strengths = GetTeamStrengths(year, week)
  print _TeamStrengthsToString(team_strengths, output='text')


if __name__ == '__main__':
  args = _ReadArgs()
  _PrintTeamStrengths(**args)
