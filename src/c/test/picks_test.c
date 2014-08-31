#include <assert.h>
#include <stdlib.h>
#include <stdio.h>

#include "../predictions.h"
#include "../picks.h"

/* Colors */
#define KNRM  "\x1B[0m"
#define KGRN  "\x1B[32m"

static char *test_file = "src/c/testdata/test_predictions.txt";

void run_tests(void) {
  float **predictions = predictions_allocate();
  char team_names[NUM_TEAMS * 4];
  int num_games = predictions_read(test_file, predictions, team_names);
  DpCell **dp_table = picks_run_dp(num_games, predictions);
  int *pick_sequence = calloc(num_games, sizeof(int));
  float opt_val = picks_get_opt(dp_table, num_games, pick_sequence);
  
  assert(opt_val - 2.2 <= 1e-7 && opt_val - 2.2 >= -1e-7);
  assert(pick_sequence[0] == 0);  // CHI
  assert(pick_sequence[1] == 1);  // DET
  assert(pick_sequence[2] == 3);  // MIN
}

int main(int argc, char *argv[]) {
  run_tests();
  printf("%sPicks tests passed!%s\n", KGRN, KNRM);
  return 0;
}
