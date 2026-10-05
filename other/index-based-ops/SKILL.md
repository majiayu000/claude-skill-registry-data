---
name: index-based-ops
description: Bring up or debug index-based compute ops (TopK, Sort, Argmax) in tt-emule — ops that return values + indices, where ties make the index choice non-unique. Use when implementing one of these ops or triaging its value/index test failures.
---

# Index-based ops (TopK, Sort, Argmax)

These ops return **values + indices**. emule does the math in f32, silicon in
the SFPU; on value ties the index assignment can differ yet still be correct.
Match the **test's contract**, not silicon's exact index choice.

## What the test asserts (TopK; Sort/Argmax are analogous)
`test_topk.py` checks:
1. `assert_numeric_metrics` on **values** (PCC 0.9999, atol/rtol 1e-6).
2. `assert_equal` on **values** vs `torch.topk(sorted=True)` — exact. bf16
   round-trips losslessly (CB bf16 → f32 DST → bf16), so the correct top-K
   *values* match torch exactly regardless of which tied index won. The only
   requirement: select the correct top-K **set**, sorted.
3. **Gather cosine** on indices: `cosine(torch_vals, gather(input, ttnn_idx)) > 0.99`.
   Indices are never compared to torch directly — only via gather, which is
   robust to ties ⇒ indices need only be *valid* (point at the right values).

So "correct but non-identical to silicon" is a non-issue: return the correct
top-K values (sorted) + valid indices and it passes. A throwaway probe (call
the op, then `torch.equal` on values + `CosineSimilarity` on
`gather(input, indices)`) localizes failures fast.

## Sort axis — the #1 gotcha
The ttnn topk kernels run `transpose_wh_tile` on every value/index tile *before*
the LLK calls, moving the sort dim W onto the **row** index of the 32×32 DST
tile (`DST[r*32+c] = input[H=c][W=r]`). Top-K along W at fixed H=c compares
datums across **rows** at a fixed **column** → each column is an independent
sort sequence. A per-row implementation returns garbage.

## TopK kernel paths and the three LLK shims
| Path | Kernel(s) | When | Uses |
|---|---|---|---|
| Single-core insertion sort | `topk.cpp` | dim-size < `multi_core_min_width` (8192) | `topk_local_sort` (`i_end_phase=5`) |
| Multi-core bitonic + cross-core agg | `topk_local.cpp` + `topk_final.cpp` | dim-size ≥ 8192 | `topk_local_sort`, `topk_merge`, `topk_rebuild` |

Shims in `compute_kernel_api.h` (`namespace __emule_topk`): `merge_split_col` =
full-sort 64 (V0∪V1), top-32→V0 / bottom-32→V1; `sort_col` = sort one tile's 32
per column.
- `topk_local_sort(idir, i_end_phase)`: `i_end_phase>=5` → `merge_split_col`;
  `<5` → independent per-tile `sort_col`.
- `topk_merge<top_min>` **and** `topk_rebuild`: both "move the larger 32 into V0,
  lower 32 into V1" (`topk_common_funcs.hpp:100,160`) → both = `merge_split_col`.
  The full 64-sort is order-independent, so the kernel's reduction tree converges
  to the global top-K for all K (32/64/3000) without reproducing the SFPU's exact
  bitonic intermediate state.

## Sort (`ttnn.sort`)
Reuses the TopK shims verbatim (`topk_local_sort`/`topk_merge`, not
`topk_rebuild`) — `merge_split_col` is also correct for a full sort, so no new
math is needed. It selects one of three program factories by width-in-tiles
`Wt` against a grid-dependent threshold: single-core (`Wt<=64`) and cross-core
exchange are supported; the single-row multi-core DRAM path (`Wt` above the
threshold) is not (see below). The threshold scales with the core grid, so the
same case can differ by arch — e.g. `262144` is cross-core on WH (64 cores) but
single-row-multi-core on BH (110 cores, where it rounds just over the threshold).

The cross-core reader collapses an L1 pointer to a 32-bit address inside an
`#include`d header, which the JIT x86 patcher now reaches (companion tt-metal
change). For the semaphore handshake itself see *Cross-core handshakes* below.

Unsupported — multi-core DRAM path (tracked in #214): its coordinator broadcasts a
toggled VALID/0 release via `noc_semaphore_set_multicast`, which races under
emule's synchronous (zero-latency) multicast — the consumer can lose a release
(`Semaphore::wait(0) stuck at 1`, or a downstream `cb_wait_front` deadlock). This
hits `524288` (both arches) and `262144` (BH only; WH `262144` is cross-core and
passes). Pacing the multicast fixes sort but stalls sticky-signal multicasts (e.g.
matmul DRAM-sharded), and the two are indistinguishable at the multicast layer; the
cases are excluded from the regression entries.

## Argmax (`ttnn.argmax`)
**Dataflow-only** — no compute/SFPU; the max-scan runs in the NCRISC reader.
Indices are compared **exactly** to `torch.argmax` (first/lowest max wins), not
gather-validated, so the kernel's strict-`>` / `idx<max_idx` tie-break must run
faithfully (it does — emule just executes it). Three readers: single-core
ROW_MAJOR, single-core TILE (walks faces, excludes the `-42` implicit padding),
multi-core ROW_MAJOR. No new shim needed — `api/numeric/*` and
`api/debug/waypoint.h` resolve to real tt-metal headers (waypoint is a no-op
without `WATCHER_ENABLED`). The multi-core path depends on the cross-core
start-ordering below.

## MoE (`ttnn.moe`)
TopK + `-inf`-masked softmax, reusing the four `topk_*` shims; value-based (PCC
0.999). Selects the 0th expert via `eqz(index)` then `mul(weights, mask)`,
routing a 0/1 mask through the UInt16 index CB — see *Integer-mask round-trip*.
Symptom when wrong: ttnn output all-zero vs nonzero torch.

## Integer-mask round-trip (an int CB used as a numeric 0/1 mask)
A UInt16 CB carries two kinds of datum: raw integer **index payloads** (must stay
bit-exact, read via `__emule_dst_load_i32`) and **numeric** masks (a 1 must
multiply as `1.0f`). emule's DST is untyped float32, so a per-slot tag
`__emule_dst_holds_int[]` (`common_globals.h`) disambiguates: `copy_tile` sets it
from the source CB (`cb_is_int_format`), `eqz_tile` consults it to emit an integer
1/0 (survives the bit-exact pack) vs a float, and the FPU binary ops convert an
integer operand to its numeric value (`__emule_unpack_cb_tile_numeric`). Pack is
unchanged, so TopK/Sort/Argmax can't regress. Mirrors silicon, where the SFPU's
integer mode leaves an integer (not IEEE-float) result.

## Sampling (`ttnn.sampling`)
top-k/top-p filter + inverse-CDF draw over the SFPU RNG. Index-validity contract
(determinism / randomness / validity / k=1) — match the contract, not the RNG bit
sequence. `rand.h` uses a per-core thread-local `mt19937` seeded from (op seed,
core coords): seeded → reproducible, `seed == 0` → reseeded from entropy each draw
(every emule core is a host thread, so a process-global `std::rand` both races and
can't reproduce per core). The writer pulls the SDPA dataflow chain via a
`cpp/ttnn/...` include, resolved by the `-I <src>/ttnn` JIT flag.

## Cross-core handshakes under emule
A reducer-style op (workers signal a collator core, which waits) leans on two
silicon timings emule collapses. When one hangs, suspect these before declaring a
path unsupportable:

1. **Zero-latency atomics.** `noc_semaphore_inc` lands instantly, so a polling
   waiter can skip past a value the NOC's latency would have let it observe. Use
   `noc_semaphore_wait`'s `>= val` for monotonic counters (exact `==0` only for a
   VALID→0 toggle). The class `Semaphore<>::wait` is exact-match — fine for a
   counter that settles at its terminal value, but not robust to overshoot.
2. **Instant reads + sequential thread spawn.** A worker can run to its increment
   before a peer has executed its prologue. If that peer is an *ungated* reducer
   resetting its counter (no start-sem gate that iteration), the reset clobbers the
   early increment and the exact-match wait hangs — worse with more cores. The
   startup barrier (`docs/noc-emulation.md` §1.1) models simultaneous dispatch but
   does **not** order a reducer's prologue against worker increments — that
   ordering is the kernel's job. The fix is in the kernel, not emule: make the
   reset timing-independent. A reset that only re-asserts the dispatcher's
   zero-init is redundant — drop it (argmax's `k=0` case); a reset that clears a
   prior iteration's count must sit behind the same start-sem handshake that gates
   the increments (argmax's `k>0` case). Do not reintroduce a NOC-latency sleep to
   paper over this — emule surfacing the race is correct.

Symptom to recognize: `Semaphore::wait(N) stuck at M<N`, nondeterministic, scaling
with core count. *Genuinely* unsupportable is different — see the sort multi-core
DRAM multicast race above (a toggled release the synchronous multicast loses).

## Infra gaps these ops surfaced (general, not topk-specific)
1. **`__emule_pack_offset` resets on `cb_push_back`, not `cb_reserve_back`**
   (`cb_api.h`, matching silicon `pack.h`). The multi-core final kernel fills a
   staging CB with `reserve_back(1)` per tile + one trailing `push_back(Wt)`,
   relying on auto-advancing `pack_tile(0,cb)` to hit distinct slots.
2. **uint16 unpack clamp** (`common.h::__emule_unpack_cb_tile_to`): clamp `n` to
   the tile bound (an oversized index page on the dim=1 path indexed
   `rowmajor_to_nfaces[]`/DST out of bounds).
3. **Program-global CB addressing** (`emulated_program_runner.cpp`): cross-core
   `get_write_ptr(cb)` for a remote-core CB — see `references/emule-mapping.md` §4.
4. **`dataflow_api.h` includes `hostdevcommon/common_values.hpp`** (INVALID/VALID).
5. **Self-recycled CB reserve** (`cb_api.h`): non-blocking `cb_reserve_back` for a
   CB the same compute thread also consumes — the in-place bitonic recycle
   deadlocks otherwise (emule runs compute single-threaded).

## Debug method that worked
Instrument the dataflow/compute boundary with `fprintf` in the JIT kernels/shims
(they run as host threads): dump per-tile values at the final-core input copy and
after the merge reduction to separate "data present but not surfaced" (merge/pack
bug) from "data missing" (inter-core transfer bug).
