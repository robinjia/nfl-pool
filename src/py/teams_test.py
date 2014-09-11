import math
import mock
import unittest

import table
import teams
import test_utils
import util

class TestTeamsFunctions(test_utils.BaseTest):
  # TODO(robinjia): Add test for when there are games played in current season.

  def setUp(self):
    self._MockFetchPastGames()

  def testTeamStrengthsSimple(self):
    strengths = teams.GetTeamStrengthsSimple(2014, 1)
    # Comparing to http://www.pro-football-reference.com/years/2013/
    self.assertAlmostEqual(-2.1, strengths['scores']['CHI'], delta=0.05)
    self.assertAlmostEqual(-9.0, strengths['scores']['WAS'], delta=0.05)
    self.assertAlmostEqual(12.9, strengths['scores']['DEN'], delta=0.05)
    self.assertAlmostEqual(11.6, strengths['scores']['SEA'], delta=0.05)

  def testTeamStrengthsMLE(self):
    """Some very approximate tests of GetTeamStrengthsMLE()."""
    strengths_simple = teams.GetTeamStrengthsSimple(2014, 1)
    strengths_mle = teams.GetTeamStrengthsMLE(2014, 1)
    # Expect that overall, "MLE" and "simple" don't differ by that much.
    # RMSE between the two should be < 3.
    rmse = math.sqrt(
        sum((strengths_simple['scores'][k] - strengths_mle['scores'][k])**2
            for k in util.TEAM_ABBREVIATIONS) / util.NUM_TEAMS)
    self.assertLess(rmse, 3)

    # Expect home field advantage to be significantly positive
    self.assertGreater(strengths_mle['home_field'], 2)

    # Seattle crushed Denver in the super bowl
    # Since "MLE" includes post-season whereas "simple" doesn't, expect SEA to
    # go up and DEN to go down by > 1 point.
    self.assertGreater(strengths_mle['scores']['SEA'], 11.6 + 1)
    self.assertLess(strengths_mle['scores']['DEN'], 12.9 + 1)

    # Expect MLE variance to be lower than simple
    self.assertLess(strengths_mle['variance'], strengths_simple['variance'])

if __name__ == '__main__':
  unittest.main()
