/**
 * Functions and structs to compute optimal picks, via dynamic programming.
 *
 * The natural DP goes week-by-week, but that requires the DP state to store 
 * subsets of teams, of which there are 2^32 ~ 4 billion.  The trick is to do
 * the DP goes team-by-team, so that the DP state is pairs
 *    (number of teams, subsets of weeks)
 * of which there are 32 * 2^17 ~ 2 million.  dp_table[i][week_subset] gives
 * the optimal expected wins if you only choose games in week_subset and only
 * pick one of the first i teams.
 * 
 * As in sequence alignement, we store pointers between nodes so that we can recover
 * the entire sequence of optimal picks.
 * 
 * TODO(robinjia): Figure out if there's a better way to get the expectimax
 * outcome given that you pick team i in the current week.  Dumb way is just to
 * run this 32 times.
 */
#ifndef NFLPOOL_PICKS_H_
#define NFLPOOL_PICKS_H_

#include <stdint.h>

/**
 * One cell in our dynamic programming table.
 */
typedef struct DpCell {

  /* Maximum expected wins using the current teams and weeks. */
  float expected_wins;

  /* "Pointer" to the DP state with one fewer team. */
  uint32_t prev_weeks;
} DpCell;

DpCell **picks_run_dp(int, float **);
float picks_get_opt(DpCell **, int, int *);
void picks_print(int, float, int *, char *);
void picks_run(char *);

#endif  // NFLPOOL_PICKS_H_
