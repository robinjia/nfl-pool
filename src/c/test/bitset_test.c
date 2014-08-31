/* Rudimentary tests for the bitset module. */
#include <assert.h>
#include <stdio.h>

#include "../bitset.h"

void TestBasic() {
  BitSet a, b, c;
  bitset_init(&a);
  bitset_init(&b);
  bitset_insert(&a, 0);
  bitset_insert(&a, 1);
  bitset_insert(&a, 2);
  bitset_insert(&b, 2);
  bitset_insert(&b, 3);
  bitset_insert(&b, 4);
  bitset_difference(&a, &b, &c);
  assert(a == 7);
  assert(b == 28);
  assert(c == 27);  // 11011
  assert(bitset_smallest(&a) == 0);
  assert(bitset_smallest(&b) == 2);
  assert(bitset_smallest(&c) == 0);
  bitset_remove(&b, 2);
  assert(b == 24);
  assert(bitset_smallest(&b) == 3);
}

int main(int argc, char *argv[]) {
  TestBasic();
  printf("All tests passed!\n");
  return 0;
}
