"""Utilities for testing."""
import mock
import os
import unittest

import table

FILE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

def ReadTestdataFile(filename):
  """Reads a file from the testdata directory.""" 
  with open(os.path.join(FILE_DIRECTORY, 'testdata', filename)) as f:
    return ''.join(f)


class BaseTest(unittest.TestCase):
  """Provides a couple helpful methods that are used commonly."""

  def _MockFetchPastGames(self, filename='2013_past_season.html'):
    past_html = ReadTestdataFile(filename)
    past_games = table.ParsePastGamesTable(past_html)
    patcher = mock.patch.object(table, 'FetchPastGames')
    mock_games = patcher.start()
    games_dict = {2013: past_games, 2014: []} 
    mock_games.side_effect = lambda x: games_dict[x]
    self.addCleanup(patcher.stop)

  def _MockFetchFutureGames(self, filename='2014_future_season.html'):
    future_html = ReadTestdataFile(filename)
    future_games = table.ParseFutureGamesTable(future_html)
    patcher = mock.patch.object(table, 'FetchFutureGames')
    mock_games = patcher.start()
    mock_games.return_value = future_games
    self.addCleanup(patcher.stop)
