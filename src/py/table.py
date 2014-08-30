"""Module for parsing tables from pro-football-reference.com"""
from lxml import html as lxml_html
import sys

# Enum for keeping track of home/away teams
HOME_TEAM_WON = 0
HOME_TEAM_LOST = 1
NO_HOME_TEAM = 2  # Basically means this was the Super Bowl

# Maps team names to abbreviations
TEAM_NAMES_TO_ABBREVIATIONS = {
  'Arizona Cardinals': 'ARI',
  'Atlanta Falcons': 'ATL',
  'Baltimore Ravens': 'BAL',
  'Buffalo Bills': 'BUF',
  'Carolina Panthers': 'CAR',
  'Chicago Bears': 'CHI',
  'Cincinnati Bengals': 'CIN',
  'Cleveland Browns': 'CLE',
  'Dallas Cowboys': 'DAL',
  'Denver Broncos': 'DEN',
  'Detroit Lions': 'DET',
  'Green Bay Packers': 'GB',
  'Houston Texans': 'HOU',
  'Indianapolis Colts': 'IND',
  'Jacksonville Jaguars': 'JAX',
  'Kansas City Chiefs': 'KC',
  'Miami Dolphins': 'MIA',
  'Minnesota Vikings': 'MIN',
  'New England Patriots': 'NE',
  'New Orleans Saints': 'NO',
  'New York Giants': 'NYG',
  'New York Jets': 'NYJ',
  'Oakland Raiders': 'OAK',
  'Philadelphia Eagles': 'PHI',
  'Pittsburgh Steelers': 'PIT',
  'San Diego Chargers': 'SD',
  'Seattle Seahawks': 'SEA',
  'San Francisco 49ers': 'SF',
  'St. Louis Rams': 'STL',
  'Tampa Bay Buccaneers': 'TB',
  'Tennessee Titans': 'TEN',
  'Washington Redskins': 'WAS'
}


class Game(object):
  """Represents one NFL game."""
  @classmethod
  def ParseFromList(cls, table_row):
    """Parses object from the <td> elements in the <tr>."""
    raise NotImplementedError


class PastGame(Game):
  """Represents a game that has finished."""

  def __init__(self, winning_team, losing_team, home_or_away, winning_points,
               losing_points):
    self.winning_team = winning_team
    self.losing_team = losing_team
    self.home_or_away = home_or_away
    self.winning_points = winning_points
    self.losing_points = losing_points

  @classmethod
  def ParseFromList(cls, table_row):
    """Parses object from the <td> elements in the <tr>."""
    winning_team = TEAM_NAMES_TO_ABBREVIATIONS[table_row[4]]
    home_or_away = ParseHomeOrAway(table_row[5])
    losing_team = TEAM_NAMES_TO_ABBREVIATIONS[table_row[6]]
    winning_points = int(table_row[7])
    losing_points = int(table_row[8])
    return cls(winning_team, losing_team, home_or_away, winning_points,
               losing_points)

  def GetPointDifferential(self):
    return self.winning_points - self.losing_points


class FutureGame(Game):
  """Represents a game that is scheduled for the future."""

  @classmethod
  def ParseFromList(cls, table_row):
    """Parses object from the <td> elements in the <tr>."""


def ParseHomeOrAway(symbol):
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


def ParsePastGamesTable(html_body):
  """Parses the table of games that have been played."""
  games = []
  for row in TableRowsIter(html_body, 'games'):
    if not row or not row[0]:
      # Empty row contained only <th> elements, ignore.
      # If row[0] is empty, this row just says "Playoffs"
      continue
    games.append(PastGame.ParseFromList(row))
  return games
    


def ParseFutureGamesTable(html_body):
  """Parses the table of upcoming games."""


def main(argv):
  pass


if __name__ == '__main__':
  main(sys.argv)
