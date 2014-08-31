/**
 * Module for reading in game outcome predictions
 */
#ifndef NFLPOOL_PREDICTIONS_H_
#define NFLPOOL_PREDICTIONS_H_

#define NUM_TEAMS 32

float **predictions_allocate(void);
int predictions_read(char *, float **, char *);

#endif  // NFLPOOL_PREDICTIONS_H_
