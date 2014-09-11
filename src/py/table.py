"""Module for parsing tables from pro-football-reference.com"""
from lxml import html as lxml_html
import sys
import urllib2

import util

# Enum for keeping track of home/away teams
HOME_TEAM_WON = 0
HOME_TEAM_LOST = 1
NO_HOME_TEAM = 2  # Basically means this was the Super Bowl

class Game(object):
  """Represents one NFL game."""
  @classmethod
  def ParseFromList(cls, table_row):
    """Parses object from the <td> elements in the <tr>."""
    raise NotImplementedError


class PastGame(Game):
  """Represents a game that has finished."""

  def __init__(self, week, winning_team, losing_team, home_or_away,
               winning_points, losing_points):
    self.week = week
    self.winning_team = winning_team
    self.losing_team = losing_team
    self.home_or_away = home_or_away
    self.winning_points = winning_points
    self.losing_points = losing_points

  @classmethod
  def ParseFromList(cls, table_row):
    """Parses object from the <td> elements in the <tr>."""
    week = table_row[0]
    winning_team = util.TEAM_NAMES_TO_ABBREVIATIONS[table_row[4]]
    home_or_away = _ParseHomeOrAway(table_row[5])
    losing_team = util.TEAM_NAMES_TO_ABBREVIATIONS[table_row[6]]
    try:
      winning_points = int(table_row[7])
      losing_points = int(table_row[8])
    except ValueError:
      winning_points = None
      losing_points = None
    return cls(week, winning_team, losing_team, home_or_away, winning_points,
               losing_points)

  def IsValid(self):
    return self.winning_points is not None and self.losing_points is not None
  
  def GetPointDifferential(self):
    return self.winning_points - self.losing_points

  def ToFutureGame(self):
    """Converts a past game into a FutureGame object."""
    if self.home_or_away == HOME_TEAM_WON:
      home_team = self.winning_team
      away_team = self.losing_team
    else:
      home_team = self.losing_team
      away_team = self.winning_team
    # TODO(robinjia): How should the Super Bowl be represented?
    return FutureGame(self.week, home_team, away_team)


class FutureGame(Game):
  """Represents a game that is scheduled for the future."""

  def __init__(self, week, home_team, away_team):
    self.week = week
    self.home_team = home_team
    self.away_team = away_team

  @classmethod
  def ParseFromList(cls, table_row):
    """Parses object from the <td> elements in the <tr>."""
    week = table_row[0]  # Don't convert to int, due to postseason
    away_team = util.TEAM_NAMES_TO_ABBREVIATIONS[table_row[3]]
    home_team = util.TEAM_NAMES_TO_ABBREVIATIONS[table_row[5]]
    return cls(week, home_team, away_team)


def _ParseHomeOrAway(symbol):
  """Parses the symbol that gives who was home/away."""
  if symbol == '':
    return HOME_TEAM_WON  
  elif symbol == '@':
    return HOME_TEAM_LOST
  elif symbol == 'N':
    return NO_HOME_TEAM
  else:
    raise KeyError('Unrecognized home/away symbol "%s"' % symbol)


def TableRowsIter(html_body, table_id):
  """Iterates over rows in the table with the given ID.
  
  Args:
    html_body: The string contents of an HTML document.
    table_id: The id of the table to look for in the document.
  Yields:
    For each <tr> in the table, a list containing the text of all <td>
    elements in that <tr>.
  """
  root = lxml_html.fromstring(html_body)
  for table in root.iter('table'):
    if table.get('id') == table_id:
      for tr in table.iter('tr'):
        row = []
        for td in tr.iter('td'):
          row.append(td.text_content())
        yield(row)


def ParsePastGamesTable(html_body, future=False):
  """Parses the table of games that have been played.

  Args:
    html_body: HTML string.
    future: If True, will convert games to FutureGame objects
  Returns: list of PastGame objects, or FutureGame objects if future == True
  """
  games = []
  for row in TableRowsIter(html_body, 'games'):
    if not row or not row[0]:
      # Empty row contained only <th> elements, ignore.
      # If row[0] is empty, this row just says "Playoffs"
      continue
    game = PastGame.ParseFromList(row)
    if future:
      games.append(game.ToFutureGame())
    elif game.IsValid():
      # Only append valid games here
      games.append(game)
  return games
    

def ParseFutureGamesTable(html_body):
  """Parses the table of upcoming games."""
  games = []
  for row in TableRowsIter(html_body, 'games_left'):
    if not row or not row[0]:
      # Empty row contained only <th> elements, ignore.
      # If row[0] is empty, this row just says "Playoffs"
      continue
    games.append(FutureGame.ParseFromList(row))
  return games


def MakeUrlForYear(year):
  """Makes a URL for the page that contains games for the given year."""
  return 'http://www.pro-football-reference.com/years/%d/games.htm' % year


def FetchPastGames(year):
  """Fetches past games from the given year."""
  return ParsePastGamesTable(urllib2.urlopen(MakeUrlForYear(year)).read())


def FetchPastGamesAsFuture(year):
  """Fetches FutureGame objects for all past games of the given year."""
  return ParsePastGamesTable(urllib2.urlopen(MakeUrlForYear(year)).read(),
                             future=True)


def FetchFutureGames(year, week):
  """Fetches future games from the given year, starting at the given week."""
  # Get games that are literally in the future
  future_games = ParseFutureGamesTable(
      urllib2.urlopen(MakeUrlForYear(year)).read())
  # We may augment this with games from the past 
  past_games = [game for game in FetchPastGamesAsFuture(year)
                if game.week.isdigit() and int(game.week) >= week]
  return past_games + future_games
