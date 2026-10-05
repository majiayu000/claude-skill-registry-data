---
name: uplift
description: Diagnose and fix emule regressions caused by bumping the tt-metal pin (and its bundled tt-umd submodule). Use when a pin bump turns the C++ or TTNN regression red — device-open crashes, JIT-compile errors, hangs, or new data mismatches — and you need to prove the cause and land a faithful emule-side fix.
---

# Uplift: surviving a tt-metal / tt-umd pin bump

When the tt-metal pin moves forward (e.g. a companion change merges to main, or
you re-pin to a newer commit), you import **two** moving parts at once: the
tt-metal source *and* the tt-umd submodule it points at. Either can regress the
emule build because emule substitutes its own runtime (`SWEmuleChip`,
`emulated_program_runner.cpp`) and JIT kernel shims (`include/jit_hw/`) for the
real hardware path. This skill is the methodology for turning a red post-bump
regression into a proven root cause and a minimal, faithful fix.

The governing principle, learned the hard way: **prove it by building and
running, not by reading `git log`.** Pickaxe/`git show`/blame routinely mislead
(moved code, squash merges, shallow submodule object DBs that render a commit as
a whole-tree add). A bisection that compiles and runs an oracle is the only
authority.

## When to invoke

- A pin bump (or `tt-metal-pin.txt` change) makes a previously-green regression
  fail.
- Symptoms after a bump: device-open aborts (`SIGABRT`/`SIGSEGV` during
  `start_device`), `jit_compile_kernel: compiler failed` (`use of undeclared
  identifier ...`), a deterministic hang, or new ATOL/PCC mismatches across many
  unrelated ops.
- You suspect the bundled umd bump rather than tt-metal source, and need to
  isolate which.

For a *single* missing compute shim (one `<op>_tile`), use `/compute-llk-bringup`.
For data-corruption on a kernel that runs without crashing, use `/memory-debug`.
This skill is for **broad** regressions that a pin bump introduced.

## Step 0 — Read the failure correctly, don't trust the label

- **Inspect artifacts, not the check's green/red.** A C++ regression job can show
  "pass" while its result artifact shows aborts — known-failure allowlists and
  classify steps can absorb failures, and exit codes don't always propagate. Open
  the actual run log/artifact and read the per-test verdicts.
- **Classify the failure mode** before chasing — they have different root-cause
  paths:
  - *device-open crash* (fails in the `device` fixture / `start_device`, before
    any op) → a shared runtime/reset/topology path, almost always umd or the
    emule chip.
  - *JIT-compile error* (`undeclared identifier`, header not found) → a jit_hw
    shim drift; the kernel can't compile against emule's headers.
  - *hang* → often a JIT-infra issue (e.g. forking a compiler from a
    many-threaded process), not the op.
  - *data mismatch* → op-correctness; usually `/memory-debug` territory.
- **Per-arch scope.** Supported arches gate the decision; an out-of-scope arch is
  typically allowlist-gated and expected-broken — don't let its churn block a
  bump, but don't silently regenerate its allowlist over a *real* new regression
  either.

## Step 1 — Build a fast, deterministic oracle

Pick the **smallest, fastest** test that reproduces the failure with an
unambiguous signal, and wrap it so it emits exactly `GOOD` / `BAD` / `SKIP`:

- `GOOD` = clean pass.
- `BAD` = the *specific* signature (e.g. a particular abort message + address, or
  the exact compiler error). Match the signature, not just "non-zero exit", so an
  unrelated failure can't masquerade as the bug.
- `SKIP` = build break or any other outcome → maps to `git bisect` 125.

## Step 2 — Bisect: isolate metal-source vs the umd bump

The pin range moves both metal and the umd gitlink, so bisect in two stages.

1. **Metal bisect.** `git bisect start <new-pin> <old-pin>` in tt-metal, then
   `git bisect run` a script that, per commit: updates the umd submodule to *that
   commit's* recorded gitlink, builds **only the oracle's target** (not the whole
   tree), runs the oracle, and returns 0/1/125.
   - If the first-bad commit changes **only the umd gitlink**, the regression
     rides with the umd bump — proceed to the umd bisect.
   - If it's a metal-source commit, the cause is in tt-metal; triage that commit.
2. **UMD bisect.** Pin metal at the first-bad (umd-bump) commit, then
   `git bisect start <bad-umd> <good-umd>` *inside the submodule* and bisect with
   the same oracle, varying only umd. Build breaks on old-umd-vs-newer-metal
   become `SKIP`.

Bisection rules that keep it honest:
- **Hold the emule layer fixed** (the jit_hw headers and any local emule source)
  for the whole bisect — the variable under test is metal+umd, exactly what the
  bump changed.
- **Build the minimal target** so each step is a fast incremental relink.
- **Automate with `git bisect run`** so you don't hand-judge steps.
- Restore all repos (`git bisect reset`, re-checkout the intended pin, resync the
  submodule) when done.

## Step 3 — Prove the boundary and the mechanism

- **Controlled before/after:** build+run the oracle at `culprit^` (GOOD) and
  `culprit` (BAD) with everything else fixed. That's the proof.
- **Read the mechanism from a two-tree diff, not `git show`.** `git show
  <culprit>` can render a whole-tree add in a shallow/grafted submodule; use
  `git diff <culprit^> <culprit> -- <file>` between two checked-out trees.
- **Read the upstream PR the culprit came from.** It is the authoritative spec for
  any emule-side mirror — its diff tells you the exact old→new API or behavior
  mapping to replicate.

## Step 4 — Design the fix (two recurring classes)

Most uplift regressions are one of these.

### A. Behavioral regression in a shared runtime path
Upstream changed a path that emule used to neutralize. *Example shape:* a device
bring-up step that used to dispatch through a per-chip virtual the SW chip
overrode as a no-op now issues an unconditional register write that the emule
memory model can't satisfy.

Fix principles:
- **Preempt at the right layer**, using an existing mode/chip-type signal the code
  already branches on. Gate **strictly** on the emulated case so silicon /
  simulation / other modes are untouched.
- **No magic constants** when a canonical accessor exists; prefer "skip the
  operation for this mode" over "match a hardcoded address".

### B. API-surface drift in the JIT kernel shims (`jit_hw`)
Upstream renamed/refactored a kernel-facing API (an enum collapse, a template
signature change, a moved header) and the emule shim still exposes the old
surface, so kernels fail to JIT-compile with `undeclared identifier`.

Fix principles:
- **Mirror the upstream change exactly** in the shim — same enum/struct/signature
  surface — using the upstream PR diff as the spec.
- **Preserve emule's bodies** (host `memcpy` / no-op / emulated sync). Only the
  *option/signature surface* changes; the emulated semantics stay.
- Migrate **all dependents in the same surface** (the header's call sites, sibling
  headers that reference the renamed symbols) so nothing dangles. Leave genuinely
  independent/older surfaces (e.g. a separate `experimental/` API with its own
  self-contained definitions) alone.
- Keep `.claude/references/structure.yaml` in sync when symbols are added/removed.

## Step 5 — Wire the fix through the repo chain

A fix can span tt-umd → tt-metal → tt-emule. Order and push mechanics matter:

- **Push dependencies before dependents.** If the metal commit bumps the umd
  gitlink to a fix commit, that umd commit must be on its remote *first*, or the
  submodule pointer dangles for CI.
- **Never push without explicit go-ahead**; for tt-emule's own PR, bump
  `tt-metal-pin.txt` to the (pushed) metal fix commit, using the **full** SHA.
- **Re-sync the vendored e2e demo on any pin bump.** The end-to-end model lane
  (`docs/e2e-models.md`) drives an emule-vendored copy of `simple_text_demo.py`
  at `tt-metal/tests/emule/models/test_tt_transformers_text_demo.py`, which
  tracks upstream only as of the pin SHA in its header. When you move
  `tt-metal-pin.txt`, re-run
  `git show <new-pin>:models/tt_transformers/demo/simple_text_demo.py` into the
  vendored file and re-apply its two `# emule:` markers. The demo is not in the
  C++ regression, so this drift is otherwise uncaught until the nightly e2e lane
  runs against the new pin.
- **jit_hw edits need no C++ rebuild.** Shims are compiled at JIT time, so a
  jit_hw change takes effect on the next kernel compile — clear the JIT cache and
  re-run; iteration is fast.

## Step 6 — Verify recovery and prove no regression

- **Oracle before/after** on the built fix: the `BAD` signature is gone.
- **Broad sweep:** run one test per previously-failing file. The headline
  invariant is that the **crash-signature count goes to zero**; PASS count rises
  with no new failures.
- **Triage every residual** into exactly one bucket: (a) caused by the fix — must
  be zero; (b) the original bug — must be zero; (c) a *separate* pre-existing gap
  that was merely unmasked once earlier crashes stopped. A fix that doesn't touch
  op math can't cause a data mismatch — reason from that.
- **Don't conflate a sweep with the curated suite.** A one-test-per-file sweep
  runs the *first collected* test in each file, which is usually **not** what the
  curated regression script selects (it uses `-k`/`::node` subsets). Before
  treating a sweep failure as real, check whether the curated script even
  exercises that node:
  - Map the failing node to the script's exact `run_pytest` args and resolve
    membership with `--collect-only`.
  - **Validate your collection-parsing first.** Verbose pytest config (`-vvs`)
    makes `--collect-only` print a `<Function ...>` tree, *not* `file::node`
    lines — grep for the `<Function ...>` reprs, and confirm your grep matches a
    test you *know* is selected before trusting any zero counts. (Class-based
    tests are `Class::method`; a bare `file::method` nodeid will error.)

## Step 7 — De-scope and track what isn't yours

- A residual that is a **separate pre-existing gap** (e.g. a missing compute-LLK
  shim, a known SIGFPE, an op-correctness mismatch) should be **filed and
  tracked**, not used to block the uplift, and not "fixed" by widening the uplift
  fix's scope.
- If the uplift's root cause is upstream-intended (a legitimate refactor), the
  emule side is what must adapt — the fix belongs in the emule layer
  (umd SW chip / `jit_hw`), not a revert.
- Note any cross-arch implication (a shim/runtime fix for the supported arch often
  also addresses the same root cause flagged for an out-of-scope arch) but don't
  chase the out-of-scope arch in the same change.

## Anti-patterns (consolidated)

1. **Concluding from `git log -S` / `git show` / blame.** They mislead on moved
   code, squashes, and shallow submodules. Bisect (build+run) is authoritative.
2. **Trusting a green CI label.** Read the artifact; allowlists hide aborts.
3. **A range-based guard that swallows real errors.** Gate on the specific
   case/mode, not "anything that would fault".
4. **Intercepting low-level I/O to dodge a high-level behavior change.** Preempt
   the operation at the layer that owns it.
5. **Hardcoding magic values** when a canonical accessor or a mode flag exists.
6. **Pushing a dependent before its dependency** (metal gitlink before the umd
   commit it references).
7. **Reading a one-test-per-file sweep as the curated suite.** Check
   `--collect-only` membership, with a validated parser.

## References

- `/compute-llk-bringup` — for a single missing compute `<op>_tile` shim (the
  common Class-B fix when the drift is one op).
- `/memory-debug` — for data-corruption residuals (Class-C, op math).
- `docs/api-injection-points.md` — where emule intercepts the pipeline
  (helps choose the "right layer" in Step 4A).
- `references/emule-mapping.md` — HW concept → emule strategy vocabulary.
- `BUILD_GUIDE.md` — build/test setup, the targets to build for an oracle, and the
  regression scripts.
