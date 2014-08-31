/**
 * A set backed by a 32-bit bitmap.
 */

#include<stdint.h>

typedef uint32_t BitSet;

inline void bitset_init(BitSet *);
inline void bitset_insert(BitSet *, int);
inline void bitset_remove(BitSet *, int);
inline void bitset_difference(BitSet *, BitSet *, BitSet *);
inline int bitset_smallest(BitSet *);
