---
name: perf-regression-test
description: Check a change for performance regression against this machine's recorded baseline - decide whether the diff needs checking, run the deck benchmark under the hygiene wrapper, and attribute any regression to an element. Use before opening a PR that touches the simulation hot path.
---

# Perf regression test

The deciding step is *whether to run this at all*. Running a two-minute benchmark on a
docs PR trains people to skip it entirely; running it on an unquiesced, contended machine
produces a "regression" that is really just noise, and one false alarm burns more trust
than ten skipped checks would have saved. Read this whole page before running anything.

**Never run any of this in CI.** GitHub-hosted runners are shared VMs whose run-to-run
spread (2-3x) exceeds any regression worth catching — a threshold loose enough not to
false-positive there catches nothing. See `.claude/notes/perf-tools-not-in-ci.md`.

## 1. Decide whether to run it

Run only when the diff touches:

```
src/elements/          include/elements/
src/simulation/        include/simulation/
src/tools/             include/tools/math.h
include/tools/fft_convolution.h
include/tools/simd_dispatch.h
```

Skip for `wiki/`, `examples/`, `src/user_interface/`, `src/visualization/`, `tests/`-only
and docs-only diffs. **Say that it was skipped and why** — a silent skip reads as a pass to
anyone reading the PR later.

Also skip (for now, re-run later) when:

- **Other builds or agents are active on this machine.** Wall-clock measurement under
  concurrent load is worthless — it will not just be noisy, it will be systematically
  biased toward "everything got slower." Wait for the machine to go quiet, or say clearly
  that the check could not be run cleanly.
- **No baseline exists yet for this environment.** `--check` will tell you this itself
  (exit code 2) — see step 3.

## 2. Build

```bash
cmake --build --preset release --target dnf_composer_deckbench --parallel 4
```

Use the `build-and-test` skill for the general build workflow. **Let the build finish
before timing anything** — a build running in the background will contend for CPU exactly
like a second agent would.

## 3. Run under the hygiene wrapper

```powershell
scripts\bench.ps1 build\release\tests\dnf_composer_deckbench.exe --check
```
```bash
scripts/bench.sh build/release/tests/dnf_composer_deckbench.exe --check
```

The wrapper pins CPU affinity, raises priority, and fixes clocks where the platform
allows it, then records what it actually managed to do into the tool's own JSON output —
see `.claude/performance-workplan/WP-07-machine-hygiene-scripts.md` for why. Running the
tool directly (unwrapped) works, but expect a wider noise floor and more `[NOISY]` /
exit-3 results.

## 4. Read the exit code

| Code | Meaning | What to do |
|---|---|---|
| 0 | Every deck within threshold | Report the deltas anyway — they're useful even when nothing regressed |
| 1 | At least one deck regressed | Go to step 5 to attribute it, then decide: real regression, or does the change justify it? |
| 2 | No baseline for this fingerprint, or a deck's file hash no longer matches the baseline's | Do **not** compare. Report the check as unverified. `--record` only ever happens on a known-good tree — see step 6 |
| 3 | Too noisy to conclude | Inconclusive, not a pass and not a failure. Re-run under the wrapper, or on a quieter machine, or report it as unverified |

`--check`'s own table (deck / baseline / current / delta / verdict) prints on every exit
code — read it, don't just act on the number.

## 5. Attribute a regression to an element

```bash
build\release\tests\dnf_composer_profiler.exe --deck <the deck that regressed>
```

Find the deck's path in `tests/benchmark/decks.json` from the tier name `--check` printed
(`small` / `medium` / `large-a` / `large-b`). The profiler drives each element's own
`step()` directly — no library instrumentation involved — and prints (and can write as
JSON via `--json`) each element's mean µs and share of the step. Compare against the
matching session in `tests/profiler/profile.md` to see which element's share grew.

**Then check the numerics didn't move too.** Every deck in `decks.json` is also a
validation fixture with a committed reference CSV (see `tests/benchmark/DECKS.md`) — run
the matching case in `dnf_composer_tests` (`GoldenFieldDynamics*` / `SpectralGolden2D*`
depending on which deck). A change that is faster and numerically different is not an
optimization; it's a different, unverified algorithm.

## 6. Updating a baseline

```powershell
scripts\bench.ps1 build\release\tests\dnf_composer_deckbench.exe --record --force
```

Only on a tree you already know is correct, and only deliberately — the same rule
`tests/golden/README.md` sets for golden data. State why the number moved in the PR. A
baseline quietly re-recorded to turn a red check green is worse than no baseline at all:
it launders a real regression into the new normal.

`--record` refuses on its own if the run is noisy, and refuses to overwrite an existing
baseline without `--force` — both are the tool protecting itself from exactly this
failure mode, not obstacles to route around.

## What this cannot tell you

This gate catches regressions in the four architectures `decks.json` covers (1D direct, a
2-term 2D kernel, and the direct/spectral pair straddling `kFFTTapThreshold`) at the sizes
those decks use. It says nothing about an architecture or grid size outside that set. If
the change is architecturally novel, note that in the PR rather than treating a clean
`--check` as full coverage.
