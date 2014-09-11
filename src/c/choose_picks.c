/**
 * Makes picks based on game predictions
 */
#include <stdlib.h>
#include <stdio.h>

#include "picks.h"

int main(int argc, char *argv[]) {
  if (argc < 2) {
    fprintf(stderr, "Usage: %s predictions.txt [teams,to,not,pick]\n", argv[0]);
    exit(1);
  }
  else if (argc == 2) {
    picks_run(argv[1], "");
  } else {
    picks_run(argv[1], argv[2]);
  }
}
