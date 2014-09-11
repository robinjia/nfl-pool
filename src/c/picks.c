#include <stdlib.h>
#include <stdio.h>

#include "bitset.h"
#include "predictions.h"
#include "picks.h"

/* Fills in the DP table, given the individual game outcome predictions. */
DpCell **picks_run_dp(int num_games, float **predictions) {
  // Initialize memory.
  DpCell **dp_table = calloc(NUM_TEAMS, sizeof(DpCell*));
  for (int i = 0; i < NUM_TEAMS; ++i) {
    dp_table[i] = calloc(1 << num_games, sizeof(DpCell));
    for (int j = 0; j < (1 << num_games); ++j) {
      // Use -1 as sentinel for "impossible"
      // e.g. if only 1 team, can't use of 2 weeks.
      dp_table[i][j].expected_wins = -1;
    }
  }
  
  // Base case: First team is obvious.
  dp_table[0][0].expected_wins = 0;
  for (int i = 0; i < num_games; ++i) {
    uint32_t set = 1 << i;
    dp_table[0][set].expected_wins = predictions[0][i];
    // dp_table[0][set] will correctly == 0, thanks to calloc.
  }

  // Recurse.
  for (int i = 1; i < NUM_TEAMS; ++i) {
    for (int prev_set = 0; prev_set < (1 << num_games); ++prev_set) {
      DpCell *prev_cell = &dp_table[i-1][prev_set];
      if (prev_cell->expected_wins == -1) continue;

      // Try not picking the current team in any week.
      DpCell *new_cell = &dp_table[i][prev_set];
      if (new_cell->expected_wins < prev_cell->expected_wins) {
        new_cell->expected_wins = prev_cell->expected_wins;
        new_cell->prev_weeks = prev_set;
      }
      
      // Try picking the current team in some week.
      for (int new_game = 0; new_game < num_games; ++new_game) {
        if (bitset_contains(prev_set, new_game)) continue;
        uint32_t new_set = bitset_insert(prev_set, new_game);
        float new_expected_wins = (prev_cell->expected_wins +
                                   predictions[i][new_game]);
        DpCell *new_cell = &dp_table[i][new_set];
        if (new_cell->expected_wins < new_expected_wins) {
          new_cell->expected_wins = new_expected_wins;
          new_cell->prev_weeks = prev_set;
        }
      }
    }
  }
  return dp_table;
}

/* Frees the memeory of a dp table */
void picks_free_table(DpCell **dp_table) {
  for (int i = 0; i < NUM_TEAMS; ++i) {
    free(dp_table[i]);
  }  
  free(dp_table);
}

/* Get the optimal sequence of picks, returns opt value. */
float picks_get_opt(DpCell **dp_table, int num_games, int *pick_sequence) {
  // Start from the last cell.
  int cur_team = NUM_TEAMS - 1;
  uint32_t cur_weeks = (1 << num_games) - 1;  // All weeks
  float opt_val = -1;  // Sentinel: if we get -1, something went wrong.
  for (; cur_team >= 0; --cur_team) {
    DpCell *cur_cell = &dp_table[cur_team][cur_weeks];
    if (cur_team == NUM_TEAMS - 1) opt_val = cur_cell->expected_wins;
    uint32_t prev_weeks = cur_cell->prev_weeks;  // Also works if cur_team == 0.
    if (prev_weeks != cur_weeks) {
      uint32_t diff = bitset_difference(prev_weeks, cur_weeks);
      int week = bitset_smallest(diff);
      pick_sequence[week] = cur_team;
    }
    cur_weeks = prev_weeks;
  }
  return opt_val;
}

void picks_print(int num_weeks, float opt_val, int *pick_sequence, char *names) {
  printf("Optimal expected wins: %g.\n", opt_val);
  printf("Optimal pick sequence:\n");
  for (int i = 0; i < num_weeks; ++i) {
    int week = 17 - num_weeks + i + 1;
    char *team_name = names + 4 * pick_sequence[i];
    printf("  Week %d: %s\n", week, team_name);
  }
}

/* Runs the pipeline to make picks based on game predictions. */
void picks_run(char *filename, char *teams_to_avoid){ 
  float **predictions = predictions_allocate();
  char team_names[NUM_TEAMS * 4];
  int num_games = predictions_read(filename, teams_to_avoid, predictions,
                                   team_names);
  DpCell **dp_table = picks_run_dp(num_games, predictions);
  int *pick_sequence = calloc(num_games, sizeof(int));
  float opt_val = picks_get_opt(dp_table, num_games, pick_sequence);
  picks_print(num_games, opt_val, pick_sequence, team_names);

  // Cleanup
  predictions_free(predictions);
  free(pick_sequence);
  picks_free_table(dp_table);
}

