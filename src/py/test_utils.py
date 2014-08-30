"""Utilities for testing."""
import os

FILE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

def ReadTestdataFile(filename):
  """Reads a file from the testdata directory.""" 
  with open(os.path.join(FILE_DIRECTORY, 'testdata', filename)) as f:
    return ''.join(f)
