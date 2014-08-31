#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "predictions.h"

/* Initializes a table to store game outcome predictions. */
float **predictions_allocate() {
  float **games = calloc(NUM_TEAMS, sizeof(float *));
  for (int i = 0; i < NUM_TEAMS; ++i) {
    games[i] = calloc(17, sizeof(float));  // Need at most 17.
  }
  return games;
}

/**
 * Reads games input from stdin
 *
 * Expected input is a bunch of lines like
 * ARI 0.2 0.7 ...
 */
int predictions_read(char *filename, float **predictions, char *names) {
  int cur_team = -1;
  int cur_game = 0;
  int num_games = 0;
  char buf[32];
  float prob;

  FILE *fp = fopen(filename, "r");
  if (fp == NULL) {
    fprintf(stderr, "Could not open file %s.\n", filename);
    exit(1);
  }
  while (fscanf(fp, "%s", buf) == 1) {
    if (sscanf(buf, "%g", &prob) == 1) {
      // Read in a winning probability
      predictions[cur_team][cur_game] = prob;
      cur_game++;
    } else {
      // Read in a new team name
      cur_team++;
      strncpy(names + 4 * cur_team, buf, 4);
      num_games = cur_game;
      cur_game = 0;
    }
  }
  return num_games;
}
