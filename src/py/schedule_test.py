"""Does some basic sanity checks on game outcome predictions."""
import unittest

import schedule
import test_utils

class TestScheduleFunctions(test_utils.BaseTest):

  def setUp(self):
    self._MockFetchPastGames()
    self._MockFetchFutureGames()
  
  def testSchedulePredictions(self):
    predictions = schedule.GetSchedulePredictions(2014, 1)
    # Denver had best margin of victory over 2013 regular season.
    # Make sure their win probabilities are all > .5, except for bye week .
    num_zero = 0  # Bye week
    for week in range(1, 17):
      winning_prob = predictions['DEN'][str(week)]
      if winning_prob == 0:
        num_zero += 1
      else:
        self.assertGreater(winning_prob, 0.5)
    self.assertEqual(1, num_zero)

    # Jacksonville had worst margin of victory over 2013 regular season.
    # Perform similar checks
    num_zero = 0  # Bye week
    for week in range(1, 17):
      winning_prob = predictions['JAX'][str(week)]
      if winning_prob == 0:
        num_zero += 1
      else:
        self.assertLess(winning_prob, 0.5)
    self.assertEqual(1, num_zero)

    
if __name__ == '__main__':
  unittest.main()
