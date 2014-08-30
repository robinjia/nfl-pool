import unittest

import table

class TestTableFunctions(unittest.TestCase):

  def setUp(self):
    with open('testdata/2013_past_season.html') as f:
      self.past_html = ''.join(f)

  def testParsePast_PastSeason(self):
    """Tries to parse a page from a season that has completed."""
    games = table.ParsePastGamesTable(self.past_html)
    self.assertEqual('DEN', games[0].winning_team)
    self.assertEqual('BAL', games[0].losing_team)
    self.assertEqual(table.HOME_TEAM_WON, games[0].home_or_away)
    self.assertEqual(49, games[0].winning_points)
    self.assertEqual(27, games[0].losing_points)
    self.assertEqual(22, games[0].GetPointDifferential())
    self.assertEqual(table.HOME_TEAM_LOST, games[2].home_or_away)
    self.assertEqual(table.NO_HOME_TEAM, games[-1].home_or_away)
    
if __name__ == '__main__':
  unittest.main()
