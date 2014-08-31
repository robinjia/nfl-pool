/* Rudimentary tests for the bitset module. */
#include <assert.h>
#include <stdio.h>
#include <stdint.h>

#include "../bitset.h"

void TestBasic(void) {
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
  TestBasic();
  printf("Bitset tests passed!\n");
  return 0;
}
