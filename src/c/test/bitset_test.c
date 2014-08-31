/* Rudimentary tests for the bitset module. */
#include <assert.h>
#include <stdio.h>
#include <stdint.h>

#include "../bitset.h"

/* Redefine number of teams to 4 */
#define NUM_TEAMS 4

/* Colors */
#define KNRM  "\x1B[0m"
#define KGRN  "\x1B[32m"

void run_tests(void) {
  uint64_t a = bitset_insert(bitset_insert(bitset_insert(0, 0), 1), 2);
  uint64_t b = bitset_insert(bitset_insert(bitset_insert(0, 2), 3), 4);
  uint64_t c = bitset_difference(a, b);
  assert(a == 7);
  assert(b == 28);
  assert(c == 27);  // 11011
  assert(bitset_smallest(a) == 0);
  assert(bitset_smallest(b) == 2);
  assert(bitset_smallest(c) == 0);
  assert(bitset_contains(a, 2));
  assert(!bitset_contains(a, 3));
  uint64_t d = bitset_remove(b, 2);
  assert(d == 24);
  assert(bitset_smallest(d) == 3);
}

int main(int argc, char *argv[]) {
  run_tests();
  printf("%sBitset tests passed!%s\n", KGRN, KNRM);
  return 0;
}
