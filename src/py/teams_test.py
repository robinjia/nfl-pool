import mock
import unittest

import table
import teams
import test_utils

class TestTableFunctions(unittest.TestCase):

  def setUp(self):
    self._MockFetchPastGames()

  def _MockFetchPastGames(self):
    past_html = test_utils.ReadTestdataFile('2013_past_season.html')
    past_games = table.ParsePastGamesTable(past_html)
    patcher = mock.patch.object(table, 'FetchPastGames')
    mock_games = patcher.start()
    games_dict = {2013: past_games, 2014: []} 
    mock_games.side_effect = lambda x: games_dict[x]
    self.addCleanup(patcher.stop)

  def testTeamStrengths(self):
    strengths = teams.GetTeamStrengths(2014, 1)
    # Comparing to http://www.pro-football-reference.com/years/2013/
    self.assertAlmostEqual(-2.1, strengths['scores']['CHI'], delta=0.05)
    self.assertAlmostEqual(-9.0, strengths['scores']['WAS'], delta=0.05)
    self.assertAlmostEqual(12.9, strengths['scores']['DEN'], delta=0.05)
    self.assertAlmostEqual(11.6, strengths['scores']['SEA'], delta=0.05)


if __name__ == '__main__':
  unittest.main()
