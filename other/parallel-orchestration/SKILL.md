---
name: parallel-orchestration
description: Concurrent phase runner for the build pipelines. Dispatches Phases 4.5-9 in parallel after the component-lanes workflow, or all of Phases 4-9 when workflows are unavailable, respecting the dependency graph and resource constraints in pipeline.config.json
user-invocable: false
---

# Parallel Orchestration

## Overview

A concurrent phase scheduler that dispatches independent pipeline phases in parallel using background agents. It reads the phase dependency graph and resource constraints from `pipeline.config.json`, determines which phases can safely run concurrently, and schedules them up to the configured `maxConcurrent` limit. Phases with unmet dependencies or conflicting exclusive resources are held until their prerequisites complete and resources free up.

The scheduler produces real-time streaming output as phases start and finish, and a final batch summary with wall-clock timing, estimated sequential time, and speedup factor.

## When to Use

- **Pipeline invocation:** Called by `/build-from-figma`, `/build-from-canva`, and `/build-from-screenshot` after the sequential phases (0-3: token-sync, intake, token-lock, tdd-scaffold) complete. When the Workflow tool is available, the pipelines run the per-item work of Phases 4-5 (component builds, visual-diff rounds) through the `component-lanes` workflow (`.claude/workflows/component-lanes.js`) first, then hand this skill the phase-level remainder: `storybook`, `dark-mode`, `e2e-tests`, `cross-browser`, `quality-gate`, `responsive`, `report`. Without workflows, this skill runs all of Phases 4-9.
- **Standalone:** Claude can apply it to ad-hoc parallel work given a list of independent tasks. It is not offered as a slash command (`user-invocable: false`).

This skill schedules phases in prose. The workflow is the deterministic part: loop bounds, the per-component lanes and the test-file checks are enforced in its code, so prefer it for Phases 4-5 whenever it is available.

## Input

1. **Phase IDs** -- ordered list of phase IDs to execute (e.g., `["component-build", "storybook", "visual-diff", "dark-mode", "e2e-tests", "cross-browser", "quality-gate", "responsive", "report"]`).
2. **Prior context** -- artifacts from earlier sequential phases:
   - `build-spec.json` (component list, appType, `renderer`, E2E flows)
   - `design-tokens.lock.json` (locked token values)
   - Test files from tdd-scaffold phase
3. **Pipeline config** -- `.claude/pipeline.config.json`, specifically the `orchestration` section.
4. **Renderer manifest** -- the resolved manifest for the build-spec's `renderer`, used to drop excluded phases and select the converter (see Step 0 and Step 5).

## Algorithm

### Step 0: Resolve Renderer and Exclude Phases

Before scheduling, read `renderer` from `build-spec.json` and resolve its manifest:

```bash
node scripts/renderer-registry.js resolve <renderer> --json
```

Read `manifest.phases.exclude` (an array, absent/empty for most renderers) and **drop every listed phase from the requested phase set before building the dependency graph.** Excluded phases never enter the scheduler — they are not dispatched, not tracked, and not awaited.

Example: the `expo` renderer excludes `visual-diff`, `cross-browser`, `responsive`, and `dark-mode` (no browser rendering), so those phases are removed up front and only `component-build`, `storybook`, `e2e-tests`, `quality-gate`, and `report` schedule. When a dependent phase's dependency was excluded, treat that dependency as pre-satisfied (same as a phase completed externally).

This replaces any per-framework phase-skipping logic — the manifest is the single source of truth for which phases a renderer supports.

### Step 1: Load Configuration

Read `.claude/pipeline.config.json` and extract the `orchestration` section:

- `maxConcurrent` -- maximum number of phases running at once (default: 3)
- `phases` -- dependency graph, resource declarations, blocking flags
- `qualityGateSubtasks` -- sub-tasks for the quality-gate phase
- `reporting` -- output preferences (streaming, summary, timeline)

Validate that every requested phase ID exists in `phases`. Abort with an error if any phase is unknown.

### Step 2: Build Execution State

Initialize a state tracker for all requested phases:

```
state = {
  [phaseId]: {
    status: "pending",    // pending | running | completed | failed | skipped
    startTime: null,
    endTime: null,
    duration: null,
    result: null,         // output or error message
    agentId: null,        // background agent identifier
    blocking: <from config>,
    depends: <from config>,
    resources: <from config>
  }
}
```

Mark any phase whose dependencies include a phase NOT in the requested set as having those dependencies pre-satisfied (assumed completed externally, e.g., phases 0-3).

### Step 3: Scheduling Loop

```
WHILE any phase has status "pending" or "running":
  ready = phases WHERE status == "pending"
                  AND all deps have status "completed"
                  AND no resource conflict with currently "running" phases

  available_slots = maxConcurrent - count(status == "running")
  to_dispatch = ready[0..available_slots]

  FOR EACH phase IN to_dispatch:
    dispatch phase as background agent (see Phase Dispatch Table)
    set status = "running"
    record startTime and agentId
    REPORT "[START] {phase} dispatched"

  Wait for next completion notification

  On completion of phase P:
    record endTime, compute duration
    If success:
      set status = "completed"
      REPORT "[PASS] {phase} ({duration}s)"
    If failed AND phase.blocking == true:
      set status = "failed"
      mark all transitive dependents as "skipped"
      REPORT "[FAIL] {phase} -- blocking, skipping dependents: {list}"
    If failed AND phase.blocking == false:
      set status = "failed"
      REPORT "[WARN] {phase} failed -- non-blocking, continuing"
```

### Step 4: Resource Conflict Check

Two phases conflict if they share any **exclusive** resource. The conflict rules:

- **String resource** (e.g., `"filesystem:src"`): exclusive by default. Two running phases with the same string resource conflict.
- **Object resource** with `"mode": "shared"` (e.g., `{ "name": "port:dev-server", "mode": "shared" }`): never conflicts with any other phase holding the same resource.
- **Empty resources** `[]`: no conflicts with anything.

Implementation:

```
function hasResourceConflict(candidatePhase, runningPhases):
  candidateExclusive = candidatePhase.resources
    .filter(r => typeof r === "string")  // strings are exclusive

  FOR EACH running IN runningPhases:
    runningExclusive = running.resources
      .filter(r => typeof r === "string")

    IF intersection(candidateExclusive, runningExclusive) is non-empty:
      RETURN true

  RETURN false
```

### Step 5: Phase Dispatch Table

When the app is scaffolded beside the framework (`./scripts/setup-project.sh my-app`), run each **Bash** dispatch from the app directory, `cd my-app && ../scripts/<name>.sh …`: `generate-stories.sh` reads that directory's `src/components` and `package.json`, and `check-responsive.sh` installs Playwright there. The artifacts still land under the Aurelius checkout's `.claude/`.

| Phase | Dispatch Method |
|-------|----------------|
| `component-build` | **Agent:** dispatch the converter named by the resolved renderer manifest. For React renderers the calling command supplies the source-appropriate converter (figma/screenshot → figma-react-converter via the figma-to-react-workflow skill, canva → canva-react-converter); otherwise dispatch `manifest.converter` (e.g. react-native-converter for expo, future vue-converter / svelte-converter) |
| `storybook` | **Bash:** `./scripts/generate-stories.sh` (exits 0 with `status: skipped` when the app's `package.json` lists no Storybook package; record the phase as skipped) |
| `visual-diff` | **Agent:** invoke visual-qa-verification skill with pixel-diff loop (max iterations from `iterationLoop.maxVisualIterations`) |
| `dark-mode` | **Bash:** `./scripts/check-dark-mode.sh http://localhost:3000` |
| `e2e-tests` | **Agent:** invoke e2e-test-generator skill with flows from build-spec.json |
| `cross-browser` | **Bash:** `./scripts/cross-browser-baseline.sh compare http://localhost:3000 --json` (diffs firefox/webkit against committed baselines with provenance checks — RFC 0002; skips with a capture hint when no baselines exist) |
| `quality-gate` | **Parallel sub-dispatch:** run all `qualityGateSubtasks` concurrently (see below) |
| `responsive` | **Bash:** `./scripts/check-responsive.sh http://localhost:3000` (installs Playwright in the directory it runs from when that holds a `package.json`) |
| `report` | **Agent:** generate `build-report.md` in `.claude/visual-qa/` from all collected phase results, timings, and diff images |

### Step 6: Quality Gate Sub-Parallelization

When `quality-gate` is dispatched, it internally runs its subtasks using the same scheduling algorithm with independent concurrency tracking:

| Subtask | Command |
|---------|---------|
| `coverage` | `pnpm vitest run --coverage` -- check 80% threshold |
| `typecheck` | `pnpm tsc --noEmit` |
| `build` | `pnpm build` |
| `token-verify` | `./scripts/verify-tokens.sh` |
| `lighthouse` | Lighthouse audit via Chrome DevTools MCP or CLI, check thresholds from `qualityGate.lighthouseThresholds` |

All subtasks run in parallel (respecting their resource declarations). The quality-gate phase passes only if **all** subtasks pass. If any subtask fails, quality-gate fails.

Report each subtask result inline:

```
[QUALITY-GATE] coverage: PASS (87%)
[QUALITY-GATE] typecheck: PASS (0 errors)
[QUALITY-GATE] build: PASS (3.2s)
[QUALITY-GATE] token-verify: PASS (no drift)
[QUALITY-GATE] lighthouse: PASS (perf:92 a11y:98 bp:95 seo:100)
```

## Batch Summary

After all phases resolve, output a summary:

```
=== PARALLEL ORCHESTRATION SUMMARY ===

Phases:  9 total | 7 passed | 1 failed | 1 skipped
Wall time:       47s
Sequential est:  138s
Speedup:         2.9x

Timeline:
 0s   [################] component-build      32s  PASS
 32s  [#####]            storybook             8s  PASS
 32s  [###########]      visual-diff          22s  PASS
 32s  [###]              dark-mode             5s  WARN (non-blocking)
 32s  [########]         quality-gate         16s  PASS
 32s  [######]           cross-browser        12s  PASS
 32s  [####]             responsive            7s  PASS
 54s  [#######]          e2e-tests            14s  FAIL
 --   [-------]          report                --  SKIPPED (dep: e2e-tests)

Failures:
  e2e-tests: 2/5 flows failed (popup-interact, content-script-inject)
```

Include:
- **Total / passed / failed / skipped** counts
- **Wall time** (actual elapsed from first dispatch to last completion)
- **Sequential estimate** (sum of all phase durations)
- **Speedup factor** (sequential / wall)
- **ASCII timeline** showing each phase's start offset, duration bar, and result
- **Failures section** with details for any failed phase

## Standalone Usage

The skill can be invoked directly for ad-hoc parallel work outside the pipeline context. Provide a list of independent tasks as phase descriptors:

```
Run these tasks in parallel using parallel-orchestration:
1. Run lint: pnpm eslint .
2. Run type check: pnpm tsc --noEmit
3. Run tests: pnpm vitest run
4. Check bundle size: ./scripts/check-bundle-size.sh
```

The scheduler treats each task as a phase with no dependencies and no resource conflicts, dispatching up to `maxConcurrent` at a time and producing the same batch summary on completion.

## Error Handling

- **Agent crash or unexpected failure:** Mark the phase as `failed`. If the phase is `blocking`, mark all transitive dependents as `skipped` and report the root cause. If non-blocking, log a warning and continue.
- **Timeout:** Log a warning after 5 minutes of a phase running, but do not auto-kill. The phase may be legitimately long-running (e.g., visual-diff iteration loop). Warn again at 10 minutes.
- **Resource deadlock:** Impossible by design. The dependency graph is a DAG (acyclic), and resources are held only during phase execution. A phase releases all resources upon completion, so no circular wait can occur.
- **All phases skipped:** If every requested phase ends up skipped (due to a blocking failure cascade), report the root-cause phase prominently at the top of the summary.
- **Config validation failure:** If `pipeline.config.json` is missing or the `orchestration` section is absent, abort with a clear error message listing what is expected.

## Integration with Pipeline Commands

Pipeline skills (`/build-from-figma`, `/build-from-canva`, `/build-from-screenshot`) invoke this skill after completing the sequential phases 0-3, and after the `component-lanes` workflow when it ran (then `component-build` and `visual-diff` are not in the requested set, so their dependents treat them as pre-satisfied). Each phase result is also written to `.claude/plans/pipeline-state.json`. The handoff without the workflow looks like:

```
# Phases 0-3 run sequentially (mandatory ordering)
Phase 0: token-sync        -> completed
Phase 1: intake             -> completed (build-spec.json written)
Phase 2: token-lock         -> completed (design-tokens.lock.json written)
Phase 3: tdd-scaffold       -> completed (failing tests written)

# Hand off to parallel-orchestration for phases 4+
Invoke parallel-orchestration with phases:
  ["component-build", "storybook", "visual-diff", "dark-mode",
   "e2e-tests", "cross-browser", "quality-gate", "responsive", "report"]

Context provided:
  - build-spec.json (appType, renderer, component list, E2E flows)
  - design-tokens.lock.json
  - Test files from phase 3
  - Pipeline config
  - Resolved renderer manifest (drives phase exclusion + converter selection)
```

Before scheduling, the scheduler resolves the renderer manifest and drops any phase in `manifest.phases.exclude` (Step 0). The parallel scheduler then respects the dependency graph within the remaining handed-off phases. For example, `component-build` has no unmet deps (its dep `tdd-scaffold` was completed in the sequential block), so it starts immediately. Phases like `visual-diff`, `storybook`, `dark-mode`, `quality-gate`, `cross-browser`, and `responsive` all depend on `component-build`, so they fan out once it completes. Finally, `report` waits for `quality-gate` and `e2e-tests` before running.
