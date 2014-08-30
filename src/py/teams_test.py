import mock
import unittest

import table
import teams
import test_utils

class TestTeamsFunctions(test_utils.BaseTest):
  # TODO(robinjia): Add test for when there are games played in current season.

  def setUp(self):
    self._MockFetchPastGames()

  def testTeamStrengths(self):
    strengths = teams.GetTeamStrengths(2014, 1)
    # Comparing to http://www.pro-football-reference.com/years/2013/
    self.assertAlmostEqual(-2.1, strengths['scores']['CHI'], delta=0.05)
    self.assertAlmostEqual(-9.0, strengths['scores']['WAS'], delta=0.05)
    self.assertAlmostEqual(12.9, strengths['scores']['DEN'], delta=0.05)
    self.assertAlmostEqual(11.6, strengths['scores']['SEA'], delta=0.05)


if __name__ == '__main__':
  unittest.main()
