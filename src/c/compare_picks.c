/**
 * Compares different possible picks for the current week
 */
#include <stdlib.h>
#include <stdio.h>

#include "picks.h"

int main(int argc, char *argv[]) {
  if (argc < 2) {
    fprintf(stderr, "Usage: %s predictions.txt\n", argv[0]);
    exit(1);
  }
  picks_compare(argv[1], argv[2]);
}
