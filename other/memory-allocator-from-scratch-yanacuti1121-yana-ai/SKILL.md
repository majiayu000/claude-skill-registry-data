---
name: memory-allocator-from-scratch
description: "Use when implementing a custom malloc/free-style memory allocator from first principles — not when just using a language's built-in allocator. Triggers on: 'write a malloc implementation', 'build a memory allocator', 'free list allocator', 'buddy allocator', 'slab allocator', 'implement my own malloc/free'. Covers free-list design, block metadata, coalescing, alignment, and allocator strategy tradeoffs."
origin: yana-ai — synthesized from classic allocator literature (K&R malloc, dlmalloc design notes, jemalloc/tcmalloc public design docs) and community from-scratch tutorials indexed in codecrafters-io/build-your-own-x
license: Apache-2.0
version: 1.0.0
compatibility: yana-ai >= 0.43.2
---

# /memory-allocator-from-scratch

## When to Use

- Implementing `malloc`/`free`/`realloc` semantics from raw memory (e.g. over `mmap`/`sbrk`, or a fixed byte array) for teaching, an embedded target, or a custom-runtime project.
- Choosing between allocator strategies (bump, free-list, buddy, slab) for a specific workload and needing the actual tradeoffs, not just the names.
- Debugging fragmentation, use-after-free, or double-free in a hand-rolled allocator.

## Do NOT use for

- Application-level memory management in a language with a GC or a mature allocator (JS, Python, Go, Java) — there is nothing to build here, use the runtime's allocator.
- General performance profiling of memory usage — see `memory-leak-detection` and `profiling-benchmarking` instead.
- Production allocator replacement — use jemalloc/mimalloc/tcmalloc; this skill is for understanding the mechanism, not shipping a faster malloc than decades of tuned production allocators.

---

## Strategy Decision

```
Need the simplest possible allocator, never freeing individual objects?
  → Bump allocator (Step 1) — O(1) alloc, no free, reset all at once

Need general alloc/free of variable sizes, simplicity over raw speed?
  → Free-list allocator (Step 2) — the "classic malloc" approach

Need to minimize external fragmentation with fast coalescing?
  → Buddy allocator (Step 3) — power-of-2 sizes, easy merge, some internal waste

Need fast alloc/free of many same-sized objects (e.g. a fixed struct)?
  → Slab allocator (Step 4) — pre-carved fixed-size slots, near-zero overhead per alloc
```

## Step 1: Bump Allocator (baseline)

Simplest possible allocator: keep one pointer to the next free byte, hand out `size` bytes and advance the pointer. No `free()` — the whole arena resets or is discarded at once (common in arena/region allocators for a single request's lifetime, e.g. a per-frame game allocator or a per-HTTP-request arena).

```
alloc(size):
  aligned = align_up(next_free, ALIGNMENT)
  if aligned + size > arena_end: return OUT_OF_MEMORY
  next_free = aligned + size
  return aligned
```

## Step 2: Free-List Allocator

The mechanism behind classic `malloc`. Every allocated AND free block gets a small header before the returned pointer:

```
struct BlockHeader {
  size_t size;       // payload size, not including header
  bool   is_free;
  BlockHeader* next; // intrusive linked list of free blocks
}
```

`alloc(size)`: walk the free list looking for a block big enough.
- **First-fit**: take the first block that fits — fast, can fragment.
- **Best-fit**: scan for the smallest block that fits — less waste per allocation, slower, can leave many tiny unusable fragments over time.
- If the found block is much bigger than needed, **split** it: carve off the requested size, leave the remainder as a new (smaller) free block.

`free(ptr)`: walk back from `ptr` to its header, mark `is_free = true`, then **coalesce** with adjacent free blocks (check the block immediately before and after in memory address order, merge if both are free) — without coalescing, freed memory fragments into unusable slivers over time even though total free bytes is fine.

**Alignment**: most platforms require allocations aligned to 8 or 16 bytes (SIMD types need more). Round the requested size up to the alignment boundary before computing block size — an unaligned pointer returned to the caller can crash on some architectures (e.g. ARM strict alignment) or silently corrupt SIMD loads.

## Step 3: Buddy Allocator

Only allocates in power-of-2 sizes. The whole arena starts as one free block of size `2^max`. To satisfy a request, repeatedly split the smallest available block in half ("buddies") until you reach the smallest power-of-2 that fits the request. To free, check if your buddy (computable directly from your address via XOR with the block size) is also free — if so, merge back into the parent block, and recurse the check upward.

Tradeoff vs free-list: coalescing is O(log n) and address-computable (no list walk needed to find the buddy), but every allocation rounds up to the next power of 2 — a 65-byte request costs 128 bytes (internal fragmentation).

## Step 4: Slab Allocator

For a workload that allocates/frees many objects of the SAME fixed size (e.g. kernel `task_struct`, a game's particle objects): pre-allocate a "slab" (a page or arena) already carved into fixed-size slots, and track free slots with a simple bitmap or intrusive free list of slot indices. Alloc and free are both O(1) with no header-walking or fragmentation concerns, since every slot is identical size.

## What NOT to Do

- Don't skip the header — without per-block metadata, `free()` has no way to know a block's size or its free-list neighbors.
- Don't forget alignment — misaligned pointers are a portability bug that won't show up on every platform/compiler, making it easy to ship broken and not notice.
- Don't free() without coalescing adjacent blocks — a free-list allocator that never merges will eventually report "out of memory" while holding plenty of free (but fragmented) bytes.
- Don't reach for buddy or slab allocators before a free-list works correctly — they solve fragmentation/speed problems a working free-list doesn't have yet.
