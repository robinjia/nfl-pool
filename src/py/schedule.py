"""Assigns probabilities to games in a schedule."""
import argparse
import collections
import math
from scipy import stats
import sys

import table
import teams
import util

def _ReadArgs():
  parser = argparse.ArgumentParser(description='Predict outcomes of games.  '
                                   'Prints results to stdout.')
  parser.add_argument('year', type=int, help='The current year')
  parser.add_argument('week', type=int,
                      help='The current week.  Represents the week about to be '
                      'played, e.g. week 1 means the season hasn\'t started.')
  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
  return vars(parser.parse_args())


def _PredictHomeTeamWinningProbability(home_team, away_team, team_strengths):
  """Predicts probability that home team will win against away team.
  
  Args:
    home_team: The home team
    away_tema: The away team
    team_strengths: Output of teams.GetTeamStrengths()
  Returns:
    Probability that home team will win.
  """
  variance = team_strengths['variance']
  scores = team_strengths['scores']
  return stats.norm.cdf((scores[home_team] - scores[away_team]) /
                        math.sqrt(variance))


def GetSchedulePredictions(year, week):
  """Predicts outcomes of games starting at the given week and year.
  
  Args:
    year: The current year.
    week: Predict games starting in this week.
  Returns:
    A dict predictions where predictions[week][team] gives the win probability
    of that team to win in that week.
  """
  team_strengths = teams.GetTeamStrengths(year, week)

  future_games = table.FetchFutureGames(year)
  predictions = collections.defaultdict(lambda: collections.defaultdict(float))
  for game in future_games:
    if not game.week.isdigit() or int(game.week) < week:
      # Game is from post-season or is from before the current week.
      continue
    home_prob = _PredictHomeTeamWinningProbability(
        game.home_team, game.away_team, team_strengths)
    predictions[game.home_team][game.week] = home_prob
    predictions[game.away_team][game.week] = 1 - home_prob
  return predictions


def _SchedulePredictionsToString(predictions, week):
  """Creates a string representation of predictions.

  Args:
    predictions: Output of GetSchedulePredictions().  This is a nested dict
        mapping (team, week) pairs to the probability the given team will win
        in the given week.
    week: The week in which predictions start.
  Returns:
    String with one line per NFL team.
    Each line will have the team abbreviation and n numbers, where n is the
    number of games left in the season.  The i-th number represents the team's
    winning probability in the i-th upcoming game.  Teams will be in
    alphabetical order.  Fields are delimited by the space character.
  """
  lines = []
  for team in util.TEAM_ABBREVIATIONS:
    tokens = [team]
    for cur_week in range(week, util.NUM_WEEKS_PER_SEASON + 1):
      tokens.append('%g' % predictions[team][str(cur_week)])
    lines.append(' '.join(tokens))
  return '\n'.join(lines)


def _PrintSchedulePredictions(year, week):
  """Prints out predictions of winning probabilities to stdout."""
  predictions = GetSchedulePredictions(year, week)
  print _SchedulePredictionsToString(predictions, week)


if __name__ == '__main__':
  args = _ReadArgs()
  _PrintSchedulePredictions(**args)
