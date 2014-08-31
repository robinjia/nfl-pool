#include<strings.h>

#include "bitset.h"

/* Initializes an empty set. */
inline void bitset_init(BitSet *set) {
  *set = 0;
}

/* Inserts a value into the set */
inline void bitset_insert(BitSet *set, int val) {
  *set |= (1 << val);
}

/* Removes a value from the set */
inline void bitset_remove(BitSet *set, int val) {
  *set &= ~(1 << val);
}

/* Computes symmetric difference */
inline void bitset_difference(BitSet *a, BitSet *b, BitSet *out) {
  *out = *a ^ *b;
}

/* Finds smallest element in set, or -1 if empty.*/
inline int bitset_smallest(BitSet *set) {
  return ffs(*set) - 1;
}
