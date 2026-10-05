---
name: implement-mock
description: Workflow for adding a faithful mock of a silicon API to tt-emule. Composes `/arch-lookup` (find HW spec) → emule-mapping strategy selection → stub implementation → verification against sentinel + tt-metal regression.
user_invocable: true
---

# /implement-mock — Add a faithful mock to tt-emule

You've identified a silicon API that tt-emule needs to mock (or a
mock that's diverging from silicon). This skill walks the
end-to-end workflow.

## Usage

```
/implement-mock <silicon_function_or_concept>
/implement-mock noc_async_write_tile
/implement-mock llk_unpack_AB_matmul
/implement-mock TensorAccessor::get_noc_addr
```

## Step 1 — Look up the HW spec

Run `/arch-lookup "<silicon_function>"` first. The arch-lookup skill
gives you the authoritative HW behavior across wormhole / blackhole
(and quasar if asked), AND a starting recommendation for the mock.

Read the sage output's **"Emule mapping"** + **"Recommendation"** sections
carefully — they may already point at the right strategy.

## Step 2 — Pick a strategy

A mock sits at one of three rungs of the kernel API stack (see
[`docs/kernel-api-layers.md`](../../../docs/kernel-api-layers.md) for
the layer-1 / 1.5 / 2 / 3 vocabulary). Pick the strategy that matches
the layer the silicon API bottoms out at:

| Strategy | Kernel-API layer | When |
|---|---|---|
| **A — stub in `include/jit_hw/`** | layer-1 (PoR tile-op) | The silicon API is generic enough that one emule-side body works for every kernel that calls it. |
| **B — per-op `#ifdef __EMULE_JIT_MODE` patch in the consumer's op header** | layer-1.5 / layer-2 mix | The API can't be generically stubbed (takes a constexpr L1 firmware address, calls a small set of LLKs) but the consuming op can route through an emule-friendly equivalent. |
| **C — semantic rewrite under `__EMULE_JIT_MODE`** | layer-2 / layer-3 reframing | The op's TRISC body is deeply LLK / sfpi / `TTI_*`-bound (>5 LLK template errors on first compile). Re-express the op at a higher layer rather than stub every header below it. |

### Strategy A — stub in `include/jit_hw/`
Default for layer-1 lifts: new compute primitives, dataflow helpers,
generic API surface. Example: `noc_async_write`, `mul_tiles`,
`recip_tile`, `pack_tile`.

- Add the function to the appropriate header under `jit_hw/`
- If it operates on DST: use `__emule_dst[idst][i]` row-major float32
- If it operates on a CB tile: use `__emule_compute::cb_read_ptr_at` /
  `cb_write_ptr_at` + `__emule_nfaces::rowmajor_to_nfaces[]` permute
- If it's pipeline state (UNPACK/MATH/PACK config): no-op stub
- No `__EMULE_JIT_MODE` guard needed (`jit_hw/` is inside `-I` ahead
  of tt-metal's `hw/inc`)

**For LLK compute shims** (functions like `<op>_tile` /
`<op>_tile_init` under `include/jit_hw/api/compute/`), use
`/compute-llk-bringup` directly — it specializes Strategy A with the
shim-pattern catalog, `sfpu_split_includes.h` wiring, op→test-file
mapping, polynomial-port recipe, and PCC triage flow for that scope.

### Strategy B — per-op `#ifdef __EMULE_JIT_MODE` patch
Edit the consumer's `op.hpp` (or equivalent header) directly under
`__EMULE_JIT_MODE`. Most common shape (constexpr L1 firmware address
cast routed through `__emule_local_l1_to_ptr`):
```cpp
volatile tt_l1_ptr T* p =
#ifdef __EMULE_JIT_MODE
    reinterpret_cast<volatile tt_l1_ptr T*>(__emule_local_l1_to_ptr(L1_ADDR));
#else
    reinterpret_cast<volatile tt_l1_ptr T*>(L1_ADDR);
#endif
```

### Strategy C — semantic rewrite under `__EMULE_JIT_MODE`
- Gate off the entire silicon `#include` block AND the `operator()`
  body under `#ifdef __EMULE_JIT_MODE`
- Reimplement the op directly with CB read/write + `__emule_dst[]` math
- Validated 4× to date: RMSNorm, clamped_silu, Mcast, eltwise_mul

If unsure: default to A (stub in `jit_hw/`) if generic, B (per-op
patch) if a single op uses it, C (semantic rewrite) if the LLK / sfpi
chain is too deep.

## Step 3 — Wire it in

Common scaffolding tasks:

1. **Allowlist the op** (if the consumer uses an `__EMULE_JIT_MODE`
   aggregator header): add the op to the `#else`/emule branch — append,
   don't reorder existing entries.

2. **Wipe the JIT cache** before testing:
   ```bash
   rm -rf /tmp/tt_emule_jit_* /tmp/tt_emule_src_*
   ```
   If the persistent cache at `/tmp/tt_emule_jit_cache_*` doesn't hash
   the aggregator/op headers, wipe it too; otherwise per-test temp dirs
   at `/tmp/tt_emule_jit_*/` are enough.

3. **Run the test that exercises the new mock.**

4. **Verify the sentinel test still passes** (your smallest end-to-end
   emule test, used to catch broad collateral damage).

## Step 4 — Verify

Pass bar:
- Target test: 100% parametrizations passing (or PCC > test's threshold)
- **Sentinel test**: still passes (your mock changes may have
  collateral damage on existing tests)
- **tt-metal regression**: totals must match the last known good
  baseline (no previously-passing test now failing):
  ```bash
  # default arch is wormhole n150; use the per-arch script (also
  # run_regression_blackhole.sh / run_regression_quasar.sh as needed)
  TT_METAL_DIR=<tt-metal-checkout> bash scripts/run_regression_wormhole.sh 2>&1 | tee regression-wormhole.log
  ```

If any of the above slips, see "Recovery" below.

## Step 5 — Document

- If the mock is faithful to silicon: short comment at the impl site
  noting the HW behavior + reference (DeepWiki page, Confluence page,
  or LLK file:line).
- If the mock is intentionally simplified (no UNPACK/MATH/PACK
  pipeline state, no fabric, no real sfpi:: SIMD): note the
  simplification.
- If you discover a new pattern (e.g. a fresh instance of the semantic
  rewrite, or a brand-new strategy), add it to
  `.claude/references/emule-mapping.md`.

## Batch mode

For sweeps (≥4 similar mocks at once), see
`/parallel-mock-implementation` for the Workflow-tool dispatch pattern:
one sub-agent per file, structured DONE/STUCK output, orchestrator
handles centralized wiring afterward.

## Step 6 — Time-box

Set a budget (e.g., 30 min for a non-trivial mock, 15 min for a sweep).
If you're past the time-box and not converging, mark BLOCKED with a
precise triage note + the deepest error message, and move on.

## Recovery / rollback

- If a primitive change breaks the sentinel:
  ```bash
  git checkout <file>
  ```
  and move on with the next primitive.
- If an op's allowlist add poisons all kernels (sentinel breaks),
  remove the allowlist entry and move on.
- If tt-metal regression slips, bisect by reverting hunks; worst case,
  restore from a pre-change snapshot.

## Anti-patterns

These cause more harm than good — avoid:

1. **Stubbing without consulting the HW spec.** A no-op stub may
   compile but produce wrong output, and that's harder to debug
   than a missing-symbol error.
2. **Adding an op to the allowlist before verifying its op.hpp
   parses under TRISC.** Sentinel breaks; everyone else also breaks.
3. **Blanket `rm -rf /tmp/tt_emule_jit_*` while other workers run.**
   Wave-1 swarm hit this. Sequential work is fine.
4. **Implementing real sfpi:: SIMD math just to get one test to
   pass.** The shim provides types only; for an op that needs real
   SIMD, use the semantic rewrite pattern instead.
5. **Editing the silicon path in a consumer's aggregator header's
   `#ifndef __EMULE_JIT_MODE` branch.** That branch isn't ours;
   keep edits under `#else` (or `#ifdef __EMULE_JIT_MODE`).

## Related references

- `docs/kernel-api-layers.md` — layer-1 / 1.5 / 2 / 3 vocabulary the
  Step 2 strategies map onto
- `.claude/references/emule-mapping.md` — HW concept → emule mock
  catalog (§§1–6 + out-of-scope table)
- `docs/api-injection-points.md` — where in the pipeline emule injects
- `CLAUDE.md` — project conventions (clang-20, slow dispatch, always run
  regressions)
- `BUILD_GUIDE.md` — `TT_METAL_DIR`, regression scripts
