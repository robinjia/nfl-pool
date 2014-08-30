"""General utilities and constants."""
# Numeric Constants
NUM_TEAMS = 32
NUM_WEEKS_PER_SEASON = 17
NUM_GAMES_PER_TEAM = 16
NUM_REGULAR_SEASON_GAMES = NUM_TEAMS * NUM_GAMES_PER_TEAM / 2
NUM_PLAYOFF_TEAMS = 12
NUM_PLAYOFF_GAMES = NUM_PLAYOFF_TEAMS - 1
NUM_TOTAL_GAMES = NUM_REGULAR_SEASON_GAMES + NUM_PLAYOFF_GAMES

# Map from team names to abbreviations
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

# List of team abbreviations, sorted alphabetically
TEAM_ABBREVIATIONS = sorted([TEAM_NAMES_TO_ABBREVIATIONS[k]
                             for k in TEAM_NAMES_TO_ABBREVIATIONS])
