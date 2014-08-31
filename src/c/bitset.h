/**
 * Functions for treating integers like bitsets.
 */
#ifndef NFLPOOL_BITSET_H_
#define NFLPOOL_BITSET_H_

#include <stdbool.h>
#include <stdint.h>

/* Inserts a value into the set */
static inline uint64_t bitset_insert(uint64_t set, int val) {
  return set | (1 << val);
}

/* Removes a value from the set */
static inline uint64_t bitset_remove(uint64_t set, int val) {
  return set & ~(1 << val);
}

/* Checks if a bitset contains a given value */
static inline bool bitset_contains(uint64_t set, int val) {
  return (set & (1 << val)) != 0;
}

/* Computes symmetric difference */
static inline uint64_t bitset_difference(uint64_t a, uint64_t b) {
  return a ^ b;
}

/* Finds smallest element in set, or -1 if empty.*/
static inline int bitset_smallest(uint64_t set) {
  return __builtin_ffs(set) - 1;
}

#endif  // NFLPOOL_BITSET_H_
