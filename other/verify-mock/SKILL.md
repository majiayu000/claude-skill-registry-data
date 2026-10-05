---
name: verify-mock
description: Verification checklist to walk before declaring a tt-emule mock complete. Use after implementing a stub (typically at the end of /implement-mock or /compute-llk-bringup) to catch the recurring failure modes — signature drift, no-op math, missing format dispatch, JIT-cache staleness, regression baseline drift.
user_invocable: true
---

# /verify-mock — Verify your mock before declaring done

You've implemented a mock for a silicon API in tt-emule. Before
declaring it complete, walk this checklist. Skipping any step is how
regressions creep in.

Invoke from `/implement-mock` Step 4 or `/compute-llk-bringup` PCC
triage, or directly when finishing up a mock.

## Pre-implementation

- Confirm you ran `/arch-lookup "<silicon_function>"` and have the
  authoritative HW spec.
- Confirm you picked a Strategy (A/B/C — see `/implement-mock` Step 2)
  and which kernel-API layer (layer-1 / 1.5 / 2 / 3, per
  `docs/kernel-api-layers.md`) the mock targets.
- If the spec is arch-specific (WH vs BH vs QSR), confirm which arch
  the target test uses (`TT_EMULE_ARCH=blackhole|wormhole|quasar`).
- Check no existing mock already covers the same surface (avoid
  duplicates / conflicting overloads).

## Implementation

- The mock signature **exactly** matches silicon's signature (template
  params, defaults, return type). Mismatches cause silent ADL
  surprises.
- Real math (not a no-op) if the test will check PCC against torch.
  No-op stubs are only OK for HW pipeline state (UNPACK/MATH/PACK
  config calls).
- Format-aware path for bf16 vs fp32 vs uint16 vs Bfp8_b vs Bfp4_b if
  the API reads/writes a CB. Use the enum-driven predicates
  (`__emule_compute::cb_is_32bit_format(cb_id)` and siblings) — never
  page-size heuristics (see `docs/cb-dataformat.md`).
- Use `__emule_nfaces::rowmajor_to_nfaces[]` on CB reads/writes —
  emule DST is row-major, CB tiles are face-packed.
- If touching DST: call `__emule_dst_check(idst, "name")` early and
  `__emule_dst_mark_dirty(idst)` on writes.
- If the silicon impl has multiple template variants (e.g.
  `<BroadcastType bcast_type>`), all variants are supported (use
  `if constexpr` to dispatch).
- Comment cites silicon source (DeepWiki page, Confluence page, or
  `tt_llk_*/...:line`) for non-obvious choices.

## Build + sanity

- Build passes (only when you touched `emulated_program_runner.cpp`
  or other runner sources):
  ```bash
  cmake --build ${TT_METAL_DIR}/build_emule -j$(nproc)
  ```
- Wipe per-test JIT temp dirs before testing:
  ```bash
  rm -rf /tmp/tt_emule_jit_* /tmp/tt_emule_src_*
  ```
  The persistent disk cache at `/tmp/tt_emule_jit_cache_*` is
  hashed and self-invalidates on header content change; per-test
  temp dirs at `/tmp/tt_emule_jit_*/` need an explicit wipe.

## Verification

- **Sentinel test passes** — your project's smallest end-to-end
  emule test that exercises the JIT compile + dispatch path.
- Target test reaches the new mock (verify with
  `TT_EMULE_KEEP_JIT_TEMP=1` + grep the patched `kernel.cpp` /
  `wrapper.cpp` under `/tmp/tt_emule_jit_*/`).
- Target test passes (or PCC improves above its threshold).
- **tt-metal regression matches the recorded baseline**:
  ```bash
  TT_METAL_DIR=<tt-metal-checkout> bash scripts/run_regression_wormhole.sh   2>&1 | tee /tmp/rg-wh.log
  TT_METAL_DIR=<tt-metal-checkout> bash scripts/run_regression_blackhole.sh  2>&1 | tee /tmp/rg-bh.log
  TT_METAL_DIR=<tt-metal-checkout> bash scripts/run_regression_quasar.sh     2>&1 | tee /tmp/rg-qs.log
  ```
  Run the three sequentially (shared JIT cache). Any test that
  previously passed and now fails blocks ship; consult
  `.github/known-failures-quasar.txt` for the QS allowlist.
- **Coverage came from an existing tt-metal test, not a new one.**
  Prefer fixing the mock so a canonical tt-metal test passes over
  authoring a test. A new tt-metal test is a last resort; when
  genuinely unavoidable it must live under **`tests/emule/`** (e.g.
  `tests/emule/ccl/`), formatted to tt-metal's pre-commit config
  (**black line-length 120**, isort, autoflake), wired into the emule
  pytest runner (`scripts/run_ttnn_pytests_*.sh`), with the pin bumped
  to the companion commit. See the CLAUDE.md project rule.

## Documentation

- If you added a new strategy / pattern, append to
  `.claude/references/emule-mapping.md` (the catalog) and link from
  `/implement-mock` Step 2 (the strategy taxonomy).
- If you discovered a HW-spec-vs-emule-mock divergence the test
  doesn't catch, note it in the commit message and in any relevant
  `docs/<subsystem>-emulation.md`.

## Common gotchas

- **No-op stub compiles but produces zero/garbage at runtime.** Add
  real math even if "obvious" — `recip_tile` returning 0 is harder
  to debug than `recip_tile` undefined.
- **Template parameter mismatch with silicon signature.** Causes
  "no matching function" errors that look like the mock isn't found.
  Always copy the silicon signature exactly, then maybe add defaults.
- **`#ifdef __EMULE_JIT_MODE` placed inside a `#if defined(COMPILE_FOR_*)`
  block.** Both run; the inner one wins. Make sure the gate is at the
  right level — usually OUTSIDE the per-RISC guard.
- **Allowlist-add poisons sentinel.** If the op's op.hpp doesn't
  compile under TRISC (even if your test only uses BRISC), the whole
  allowlist breaks. The sentinel run catches this.
- **`tt_l1_ptr`, `VALID`/`INVALID` undefined.** These come from
  `dataflow_api.h` (`tt_l1_ptr`) and `hostdevcommon/common_values.hpp`
  (`VALID`/`INVALID`). Both must be `#include`d for any code path
  that uses them — silicon path may pull them transitively, emule may
  not.
- **`compute_kernel_hw_startup` redefinition.** Both
  `jit_kernel_stubs.hpp` and `api/compute/compute_kernel_hw_startup.h`
  define overloads. Use the `__EMULE_COMPUTE_KERNEL_HW_STARTUP_DEFINED`
  guard pattern (first-included-wins).

## Anti-checklist

These are NOT done criteria — don't get hung up:

- Bit-exact match with silicon output. PCC > test's threshold
  (~0.998) is the bar.
- Real `sfpi::` SIMD math (the shim provides types only).
- Fabric / multichip semantics (out of scope).

## Related skills

- `/implement-mock` — end-to-end workflow (this checklist is its
  Step 4 in expanded form).
- `/compute-llk-bringup` — specialization for LLK compute shims.
- `/memory-debug` — when verification fails with PCC < threshold or
  ATOL mismatch (partial zeros, off-by-N writes).
