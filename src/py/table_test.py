import unittest

import table
import test_utils

class TestTableFunctions(unittest.TestCase):

  def setUp(self):
    self.past_html = test_utils.ReadTestdataFile('2013_past_season.html')
    self.future_html = test_utils.ReadTestdataFile('2014_future_season.html')

  def testParsePast_PastSeason(self):
    """Parse past games from a page for a season that has completed."""
    games = table.ParsePastGamesTable(self.past_html)
    self.assertEqual('DEN', games[0].winning_team)
    self.assertEqual('BAL', games[0].losing_team)
    self.assertEqual(table.HOME_TEAM_WON, games[0].home_or_away)
    self.assertEqual(49, games[0].winning_points)
    self.assertEqual(27, games[0].losing_points)
    self.assertEqual(22, games[0].GetPointDifferential())
    self.assertEqual(table.HOME_TEAM_LOST, games[2].home_or_away)
    self.assertEqual(table.NO_HOME_TEAM, games[-1].home_or_away)
    self.assertEqual(table.NUM_TOTAL_GAMES, len(games))

  def testParseFuture_FutureSeason(self):
    """Parse future games from a page for a season that hasn't started."""
    games = table.ParseFutureGamesTable(self.future_html)
    self.assertEqual('1', games[0].week)
    self.assertEqual('SEA', games[0].home_team)
    self.assertEqual('GB', games[0].visiting_team)
    self.assertEqual(table.NUM_REGULAR_SEASON_GAMES, len(games))

    
if __name__ == '__main__':
  unittest.main()
