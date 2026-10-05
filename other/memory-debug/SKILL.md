---
name: memory-debug
description: Diagnose data-corruption failures in tt-emule operations (wrong values, partial zeros, off-by-N row/col writes). Use when a regression test reports ATOL > 1e-3 on otherwise-functional kernel paths.
---

# Memory & data-corruption debug for tt-emule

Distills the diagnostic playbook used across rounds 7-12. Targets the
failure mode "kernel runs, no crash, but output bytes don't match
input". Most fixes land in `include/jit_hw/api/dataflow/`,
`include/jit_hw/llk_pack.h`, `include/jit_hw/api/compute/common.h`,
or `tt_metal/impl/emulation/emulated_program_runner.cpp`.

For pure JIT-compile failures (missing shim), use `/compute-llk-bringup`.
For missing API surface, use `/implement-mock`.

## When to invoke

- "ATOL > 1e-3" / "PCC failure" / "max diff X" on a kernel that
  previously worked or that runs to completion.
- "Output is mostly correct but has wrong regions" / "some rows are
  wrong" / "some tiles are zero".
- "Sharded → interleaved" (or vice versa) data movement is wrong.
- "Output bytes are zero" where they shouldn't be.

Also applies when:
- Test crashes / segfault / abort during kernel execution (not at
  compile/dispatch) — segfaults are usually one specific
  bad-pointer-dereference reachable through the same trace pass plus
  a gdb post-mortem (see "Crashes" section below).

Don't invoke for:
- "Test fails to compile" — that's `/compute-llk-bringup`.

## The discriminator: zeros vs random-wrong

The very first question to answer:

| Output at the wrong cells | What it means |
|---|---|
| **Exact `0.0`** (bf16: `0x0000`, fp32: `0x00000000`) | L1 was never written there. Bug is "writer skipped" or "writer's dest_addr is wrong". |
| Non-zero but mismatched | Writer wrote *something* — either wrong src bytes or wrong dst location with another shard's data. |
| All zeros across the entire region | Entire NOC write missed. Bank topology, dst_addr crashed silently, or bank_offset_idx out of range. |
| Off-by-N pattern (e.g., row N→row N+1) | Address arithmetic off by a stride; trace `output_page_id`. |

This single bit of evidence narrows from "anywhere in pipeline" to
"compute" vs "writer" vs "address resolution".

L1 zero-init is in `Core::l1_ptr` allocation in
`tt_metal/impl/emulation/`. If output bytes are exact zero, no
NOC write landed there — assume "writer skipped" until proven otherwise.

## Layer chain (where to look)

```
torch input
    ↓
ttnn.from_torch / to_device          ← host I/O
    ↓
SWEmuleChip::write_to_device         ← emule host→L1 memcpy (W2D layer)
    ↓
input L1 buffer                       ← emule: Core::l1_ptr
    ↓                                  ← anything between W2D and the kernel
                                         that touches L1: reset_l1_bump,
                                         init_cb_sync, scratch memsets, etc.
    ↓
reader kernel: cb_reserve_back / noc_async_read
    ↓
input CB (per-core)                   ← __emule_compute::cb_read/write_ptr
    ↓
compute kernel: copy_tile / __llk_pack_untilize / sfpu ops
    ↓
DST array (__emule_dst[16][1024])     ← per-thread, float32
    ↓
output CB (per-core)
    ↓
writer kernel: cb_wait_front / noc_async_write
    ↓
output L1 buffer (interleaved or sharded)
    ↓
ttnn.to_torch
```

Trace at each ↓. The first transition where bytes diverge from
expected is the fault site. Pay particular attention to the gap
between W2D and the kernel — that's where host-side scratch /
reset hooks can silently mutate L1 between when the host wrote
real data and when the kernel reads it.

## Diagnostic recipe — the 5-step trace pass

### Step 1: capture the corruption pattern in python

Stand up a canonical repro `.py` outside the pytest harness — pytest
runs in parallel and burns the shared JIT cache (`/tmp/tt_emule_jit_cache_$UID`).
A 30-line script that calls `ttnn.from_torch → to_device → op → to_torch`
and prints `diff` arrays is faster to iterate than pytest.

Then characterize:

```python
diff = (np.abs(inp_flat - out_flat) > 1e-3)
print(f"wrong elements: {diff.sum()} / {diff.size}")
print(f"rows with any wrong cell: {np.flatnonzero(diff.any(axis=1)).tolist()}")
# Strides between wrong rows tell you tile/face boundaries
print(f"strides: {np.diff(np.flatnonzero(diff.any(axis=1))).tolist()}")
# Are the wrong columns identical across all wrong rows?
unique_col_sets = {tuple(np.flatnonzero(diff[r]).tolist()) for r in np.flatnonzero(diff.any(axis=1))}
print(f"unique col-sets: {len(unique_col_sets)}")
# What's at the wrong cells — exact zero or random wrong?
nz_at_wrong = (out_flat[diff] != 0.0).sum()
print(f"of {diff.sum()} wrong cells, {nz_at_wrong} are non-zero")
```

Strides of 16 or 32 → tile/face boundary. Strides of 32×tile_height
→ tile-row boundary. Repeating-mod stride at shard-height intervals
(1024, 256, …) → bug is per-shard at the same offset.

### Step 2: locate the cell in tile-coords

Map the corrupted (row, col) back to:
- Tile-row index: `row / 32`
- Sub-row within tile: `row % 32`
- Tile-col index: `col / 32`
- Sub-col within tile: `col % 32`
- Face index: `(sub_row >= 16) * 2 + (sub_col >= 16)` → 0/1/2/3
- DST index: `r * 32 + c` for `r = sub_row, c = sub_col`
- `rowmajor_to_nfaces[r*32+c] = face*256 + (r%16)*16 + (c%16)`

### Step 3: instrument the suspected hop with gated fprintf

Pattern (gate by env var **and** the specific tile/offset of interest
to avoid 4096-line dumps):

```cpp
// in noc_async_write — writer side, addr resolution
if (getenv("TT_EMULE_TRACE_WRITE")) {
    const uint16_t* sp = reinterpret_cast<const uint16_t*>(src);
    fprintf(stderr, "[WRITE] src_l1=0x%x → dst_noc=0x%llx size=%u "
            "first8=%04x %04x %04x %04x %04x %04x %04x %04x\n",
            (unsigned)src_local_l1_addr, (unsigned long long)dst_noc_addr,
            (unsigned)size, sp[0], sp[1], sp[2], sp[3],
            sp[4], sp[5], sp[6], sp[7]);
}
```

```cpp
// in __llk_pack_untilize — compute output → CB
bool trace_this = getenv("TT_EMULE_TRACE_PACK") && tile_idx == K && __llk_pack_offset == O;
if (trace_this) {
    fprintf(stderr, "[PACK_PRE]  DST[%u] face%u first8: %.4f %.4f %.4f %.4f ...\n",
            tile_idx, face, __emule_dst[tile_idx][r*32+c0], ...);
}
// ... do the pack ...
if (trace_this) {
    const uint16_t* rb = reinterpret_cast<const uint16_t*>(base + cb_byte_offset);
    fprintf(stderr, "[PACK_POST] CB bytes %u..%u: %04x %04x ... \n",
            cb_byte_offset, cb_byte_offset+31, rb[0], rb[1], ...);
}
```

```cpp
// in __emule_unpack_cb_tile_to (common.h) — CB → DST
if (getenv("TT_EMULE_TRACE_UNPACK") && tile_idx == K) {
    fprintf(stderr, "[UNPACK] src_bf16[528]=%04x out[528]=%.4f ...\n",
            bf[__emule_nfaces::rowmajor_to_nfaces[528]], out[528]);
}
```

Always gate by **at least** one specific position (tile_idx, offset,
`output_page_id == X`) — emule generates O(num_tiles × num_pages)
log lines without a filter.

**When the failure only occurs at iteration N (not iteration 0)** —
your `tile_idx == K` gate fires once per block × num_cores, so the
first samples you print are block 0, block 1, etc. — not the
failing block. You'll see "looks correct" and miss the bug. Fix:
add a thread-local block counter that increments when the kernel
starts a new block (e.g. `if (tile_idx == 0 && __llk_pack_offset == 0)
__block_counter++;`) and gate trace on `__block_counter == N`.
Counter is `thread_local` so each core has its own — block 18 on
core 0 and block 18 on core 1 both print, confirming
per-shard-reproducibility (or surfacing a single-shard outlier).

**When you've gated on a specific tile and the bytes look wrong** —
the next question is "is this tile actually special, or is everything
in this block wrong?" Add a scan that walks ALL tiles in the failing
iteration (loop `t = 0..num_tiles_per_block` over
`cb_read_ptr_at(icb, t)`) and prints non-zero counts per tile. If
only one tile shows the anomaly, the bug is tile-position-specific.
If all tiles show it, the bug is block-level.

**Host-side trace (W2D layer)** — when the kernel reads zeros at
bytes you believe the host wrote, instrument
`SWEmuleChip::write_to_device` in
`tt_metal/third_party/umd/device/chip/sw_emule_chip.cpp` to log
`(core, l1_dest, size, first/last bytes)`. Run with the trace and
compute the absolute L1 offset of the corrupted bytes (CB virtual
ptr − core mmap base + intra-tile offset). Cross-reference: did the
host actually write non-zero bytes at that offset? If yes, something
between W2D completion and kernel read mutated L1 — audit anything
in `tt_emule/` that touches L1 between programs (reset hooks,
scratch memsets, init routines for mailbox / barrier / debug
regions). The relevant offsets are usually fixed constants whose
value was correct under an older L1 layout but now overlaps
allocator output.

### Step 4: rebuild + rerun the canonical repro

```bash
rm -rf /tmp/tt_emule_jit_cache_$(id -u)  # one-shot per instrumentation edit
cd /localdev/arminale/tt-metal && \
PYTHONPATH=$PWD/ttnn:$PWD/tools:$PWD/build_emule/lib:$PWD \
LD_LIBRARY_PATH=$PWD/build_emule/lib \
TT_METAL_HOME=$PWD TT_METAL_RUNTIME_ROOT=$PWD \
TT_METAL_EMULE_MODE=1 TT_METAL_SLOW_DISPATCH_MODE=1 \
TT_METAL_MOCK_CLUSTER_DESC_PATH=$PWD/tt_metal/third_party/umd/tests/cluster_descriptor_examples/wormhole_N150.yaml \
MESH_DEVICE=N150 \
TT_EMULE_TRACE_PACK=1 \
timeout 90 /opt/ttmlir-toolchain/venv/bin/python /tmp/your_repro.py 2>&1 | tee /tmp/round.log
```

Critical: JIT cache invalidation per instrumentation edit. `clang -E`
caches the preprocessed kernel — a fprintf added without bumping the
cache will be silently elided.

### Step 5: discriminate

| Trace evidence | Diagnosis | Where to fix |
|---|---|---|
| PACK_PRE shows correct DST, PACK_POST shows correct CB bytes, dest L1 has zeros | Writer never wrote those bytes (or wrote elsewhere) | `noc_async_write` resolution, `s.get_noc_addr`, or writer kernel logic |
| PACK_PRE shows correct DST, PACK_POST shows zeros in CB | `__llk_pack_untilize` row/col arithmetic bug | `llk_pack.h::__llk_pack_untilize` row_stride / tile_row_offset / tile_col_offset |
| PACK_PRE shows zeros in DST | `copy_tile` or `__emule_unpack_cb_tile_to` doesn't fill DST face | `common.h::copy_tile`, `__emule_unpack_cb_tile_to` |
| WRITE trace shows `src_ptr` first8 = zeros | Writer reading from wrong CB offset, or compute didn't write CB before writer's `cb_wait_front` returned | CB sync (cb_push_back / cb_wait_front semantics) |
| WRITE trace shows correct src bytes but `dst_noc_addr` resolves to wrong core | Bank topology bug | `emulated_program_runner.cpp::populate_bank_mapping` or `dataflow_api_addrgen.h` extern arrays |
| WRITE trace shows duplicate writes from two shards to the same `dst_noc_addr` | Cross-shard race / host-side address compute wrong | Trace `runtime_args` of writer kernel, check if `width_wise_output_block_start_index` is double-allocated |

## Common root-cause classes (sorted by hit count across rounds 7-12)

### Class 1: bank topology not populated from SoC descriptor

**Symptoms**: `Core::l1_ptr OOB` crashes with very high offsets
(`0x7fc5750`, `0x834b750`); or large blocks of output are exact zero;
or "all writes to bank N fail".

**Root cause**: `emulated_program_runner.cpp` ships a placeholder
`EMULE_NUM_L1_BANKS = 1` or `EMULE_NUM_DRAM_BANKS = N` constant that
doesn't match the real `device->allocator()->get_num_banks(...)`.

**Fix shape**: populate from the allocator in `populate_bank_mapping`:

```cpp
const auto& allocator = device->allocator();
num_banks_out = allocator->get_num_banks(BufferType::L1);  // or DRAM
for (uint32_t b = 0; b < num_banks_out && b < MAX_NUM_BANKS; ++b) {
    auto logical = allocator->get_logical_core_from_bank_id(b);
    auto virt = device->virtual_core_from_logical_core(logical, CoreType::WORKER);
    uint16_t noc_xy = (uint16_t(virt.y) << NOC_NODE_ID_BITS) | uint16_t(virt.x);
    bank_to_noc_xy[0][b] = noc_xy;
    bank_to_noc_xy[1][b] = noc_xy;
}
```

Thread `num_banks` through `populate_bank_mapping` →
`execute_program_emulated` → `collect_kernels` →
`build_kernel_defines` and emit `NUM_L1_BANKS=N` /
`LOG_BASE_2_OF_NUM_L1_BANKS` / `IS_NOT_POW2_NUM_L1_BANKS`. Match the
extern array sizes in `dataflow_api_addrgen.h` /
`jit_kernel_stubs.hpp` (use `[NUM_*_BANKS]`, not literal `[32]`).

Past closures: R7 DRAM (`IS_NOT_POW2_NUM_DRAM_BANKS`), R11 L1 (B8.4
+ B8.1 as side effect).

### Class 2: per-shard same-offset corruption (compute/writer math)

**Symptoms**: All shards corrupt at the *same intra-shard offset*.
With S shards and shard height H, you see corruption at rows
`H·s + k…H·s + k+15` for `s = 0..S-1` and some fixed `k`.

**Diagnosis**: bug is in per-core writer or compute math (the same
math runs on each core, hitting the same threshold).

**Common sub-causes**:
- DST array indexing bug at a specific tile-row threshold
- `__llk_pack_untilize`'s `tile_row` / `tile_col` derived from
  `__llk_pack_offset` is wrong above some block_c
- Reader-side `cb_reserve_back` / `cb_push_back` count mismatch
  causes compute to read stale CB front

### Class 3: face-3 (bottom-right quadrant) data lost

**Symptoms**: Corrupted region is exactly 16 cols × 16 rows = 256
elements. Position aligned to a tile boundary (col % 32 == 16 and
row % 32 == 16 within the tile).

**Diagnosis**: `rowmajor_to_nfaces` LUT or `copy_tile` / SFPU
`<op>_tile` ops only fill the top-left quadrant of DST.

**Check**: `include/jit_hw/api/compute/nfaces.h::rowmajor_to_nfaces`
should be `face*256 + (r%16)*16 + (c%16)`. Many SFPU `_tile` shims
loop `i in [0, 256)` covering only one face — should be `[0, 1024)`
covering all four.

### Class 4: DAZ / FTZ flushing denormals

**Symptoms**: Output is non-zero but very small input values become
exact zero. Only triggers on `bfloat16 → fp32 → bfloat16` round-trips
where the bf16's exponent is below the fp32 normal range.

**Diagnosis**: SSE control word has DAZ / FTZ enabled in the JIT TU.

**Check**: `_MM_GET_DENORMALS_ZERO_MODE()` and `_MM_GET_FLUSH_ZERO_MODE()`
at the start of the kernel. Random Gaussian inputs in `[-3, 3]` won't
trigger this; tests with handcrafted small inputs will.

### Class 5: extern array size mismatch

**Symptoms**: kernel C++ compiles but linker emits "conflicting
declaration" or runtime accesses go to bank N+offset with stale data.

**Diagnosis**: `bank_to_noc_xy[]` in
`include/jit_hw/internal/dataflow/dataflow_api_addrgen.h` vs
`include/jit_hw/jit_kernel_stubs.hpp` declared with different array
sizes (`[32]` vs `[NUM_L1_BANKS]` vs `[256]`).

**Fix**: align all extern declarations to `[NUM_*_BANKS]` (the JIT
define), matching upstream `dataflow_api_common.h`.

## Crashes (segfault / abort during kernel execution)

When the kernel runs but the process dies mid-execution (SIGSEGV,
abort), the standard 5-step trace doesn't apply directly because
nothing reaches `to_torch`. The data is in registers and the stack
at the moment of the crash. Use gdb post-mortem to pinpoint the
faulting instruction, then re-enter the trace methodology from
the layer just above the fault.

**Localize the fault**:

```bash
# Run the canonical repro under gdb, catching the fatal signal:
gdb -batch \
  -ex 'set pagination off' \
  -ex 'handle SIGSEGV stop print' \
  -ex 'run' \
  -ex 'info registers' \
  -ex 'x/30i $pc-60' \
  --args /opt/.../python /tmp/your_repro.py
```

What you're looking for in the output:
- The PC at the time of the crash. If it lives in a JIT-built `.so`
  under `/tmp/tt_emule_jit_cache_*/`, the fault is in a JIT kernel,
  not the emule runtime.
- The instruction at the PC. A pattern like `mov (%rdx,%rax,4),%eax`
  with a bogus `rdx` value points to an array-of-pointers load
  through a truncated/uninitialized pointer.
- Pointer-value sanity: emule maps L1 below 4 GB (MAP_32BIT) and
  static globals live high (around `0x7fff…`). A register holding
  `0xc0…` or another low 4-byte value is usually a 64-bit pointer
  that got narrowed to 32-bit somewhere upstream.

**Keep the JIT build sources for diff**:

The runner cleans up the per-kernel build directory by default.
Gate that cleanup behind an env var (it's typically a single
`std::filesystem::remove_all(dir)` call in
`emulated_program_runner.cpp`) so you can read the generated
`wrapper.cpp` + `patched_kernel.cpp` of the crashing kernel.
Identify the kernel by matching the `.so.tmp.*` path from the gdb
output to its sibling build dir.

**Cross-reference the upstream call**:

Once you know the JIT kernel and the failing instruction, look at
the original kernel `.cpp` and follow the call chain backwards.
Pay particular attention to **silicon-side functions that take or
produce `uint32_t` for an L1 address**. Under emule's L1 offset model
those `uint32_t` values are **0-based firmware offsets**; the deref
site must rebase onto this fiber's `bridge_l1` via
`__emule_local_l1_to_ptr`, which the JIT patch pass inserts (see
`docs/jit-l1-patch-pass.md`).

The failure mode is a **missed deref site**: a 0-based offset (e.g.
~`0x1240`) dereferenced directly as a pointer hits an unmapped low page
→ immediate SIGSEGV at the real `kernel.cpp:<line>` (the intentional
SIGSEGV net). An un-migrated absolute/aliased value that reaches the
translate chokepoint instead trips the debug assert
`[EMULE_L1] L1 offset 0x… out of range`.

The fix is emule-side and lives in the **patch pass**, not the mmap:
add a targeted rewrite rule for the missed idiom so the offset is
rebased at deref (`docs/jit-l1-patch-pass.md` enumerates the rules).
Do **not** reach for `MAP_32BIT` — worker L1 is a plain 64-bit mmap
now, and the old truncated-host-pointer model is retired.

## Dataflow-only debug (no compute kernel involved)

Some ops are pure data movement — permute, sharded↔interleaved
without dtype conversion, transpose. They have a reader and a
writer kernel, no compute. The 5-step trace's compute hop
(DST/PACK) doesn't exist; the pipeline is shorter:

```
input L1  →  reader  →  CB  →  writer (noc_async_write)  →  output L1
```

For these, instrument noc_async_write (and noc_async_read for the
reader side). Print `(src_phys_core, src_local_l1_addr,
dst_noc_addr, size)` per write, then in a Python post-pass
decompose `dst_noc_addr`:

```python
# dst_noc_addr layout on WH:  [noc_xy:12 << 36] | [l1_offset:36]
import re, collections
nocs, phys, pairs = collections.Counter(), collections.Counter(), collections.defaultdict(set)
for line in open('writes.log'):
    m = re.match(r'\[W\] phys=\((\d+),(\d+)\) .* dst_noc=0x([0-9a-f]+) size=(\d+)', line)
    if not m: continue
    px, py = int(m.group(1)), int(m.group(2))
    dst = int(m.group(3), 16)
    noc_xy = (dst >> 36) & 0xFFFF
    nx, ny = noc_xy & 0x3F, (noc_xy >> 6) & 0x3F
    nocs[(nx, ny)] += 1; phys[(px, py)] += 1
    pairs[(px, py)].add((nx, ny))
```

Then ask the diagnostic questions:

- **How many distinct destination cores?** If 1, the writer's
  bank-id math collapses to one bank. If `num_cores / 8` or
  similar, it's likely walking only one axis of the shard grid.
  If exactly `num_cores`, the destinations are at least spread
  but might still be permuted.
- **How many distinct source cores write?** If less than expected,
  some cores never enter the kernel body — check `cb_wait_front`
  / runtime arg propagation.
- **Per-source: how many destinations does each source touch?**
  Most sharded paths have each source writing to exactly one
  shard. If the (src → dst) map is the identity (each source
  writes to itself), HEIGHT-sharded layouts are matching
  source-cores-to-destination-shards correctly. If it's a
  transposition (src `(0, K)` → dst `(K, 0)`) you have an x↔y
  orientation mismatch — the host's `packed_xy_coords` ordering
  and the kernel's `bank_id` derivation disagree on row-major
  vs column-major.

The two ends of the kernel-host contract are:
`tt_metal/impl/buffers/tensor_accessor_args.cpp` (host packs
`bank_coords[i] = (coord.x << 8) | coord.y` in the order returned
by `buffer_distribution_spec.cores()`) and
`tt_metal/hw/inc/api/tensor/tensor_accessor.h` (kernel uses
`packed_xy_coords[bank_id]` with `bank_id` derived from
`flattened_shard_id` per `dspec.shard_grid_strides`). When these
disagree on stride ordering, the symptom is the transposition
above. The fix is in whichever side ordered wrong relative to the
silicon contract — typically the upstream specifies row-major and
emule's path needs to match.

## Defer rule

If after ~2 hours of characterization the fix site isn't pinpointed,
write a `roundN-bX-handoff.md` capturing:
- Exact failing tests + tensor shapes
- Corruption pattern (rows, cols, exact-zero vs random-wrong)
- Tile-coord mapping of the corrupted region
- Trace excerpts at each pipeline hop
- Hypotheses ruled in/out
- Suggested next instrumentation

Then pivot to next-priority B-item. Don't guess at fixes — guessed
"fixes" have rolled back successful R-N work in past rounds.

## Critical files

- `include/jit_hw/api/dataflow/dataflow_api.h` — `noc_async_write`,
  `noc_async_read` (write-side / read-side trace site)
- `include/jit_hw/llk_pack.h` — `__llk_pack_untilize` (compute scatter)
- `include/jit_hw/api/compute/common.h` — `copy_tile`,
  `__emule_unpack_cb_tile_to` (DST fill)
- `include/jit_hw/api/compute/nfaces.h` — `rowmajor_to_nfaces` LUT
- `include/jit_hw/internal/dataflow/dataflow_api_addrgen.h` — extern
  bank arrays + `NOC_XY_ADDR` macro
- `include/jit_hw/jit_kernel_stubs.hpp` — extern array declarations
  (must match `dataflow_api_addrgen.h`)
- `tt_metal/impl/emulation/emulated_program_runner.cpp` —
  `populate_bank_mapping`, `build_kernel_defines`, bank topology
- `tt_metal/impl/emulation/...::Core::l1_ptr` — L1 zero-init

## Methodology lessons from past rounds

- **Misdiagnosis happens when you stop at the first plausible hop.**
  A "self-loop NOC" hypothesis was wrong; the real cause was a
  topology constant several layers up the chain. Cheap to verify
  one hop at a time; expensive to commit to one hypothesis and
  build out a fix.
- **The same characterization pattern can have multiple root-cause
  classes.** Exact zeros at tile/face boundaries have been bank
  topology, extern-array mismatch, AND host scratch overlap in
  different rounds. Don't pattern-match to a single class — run
  the trace pass.
- **When standard tooling shows "looks correct"**, the trace gate
  is probably wrong, not the hypothesis. Re-check iteration index,
  per-core fire counts, and whether you're sampling the failing
  case.
- **The cross-layer discriminator is the strongest signal.** "Host
  wrote X, kernel reads Y" tells you the mutation is between those
  two points — independent of how complex the layers in between are.
