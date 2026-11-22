---
name: verify-this
description: "Verify a claim with fresh local evidence: restate it falsifiably, capture baseline and treatment, compare artifacts, and return VERIFIED, NOT VERIFIED, or INCONCLUSIVE. A UI claim covers a case matrix of entry points, data states, input, interaction, persistence, layout, accessibility, and regressions."
---

# Verify This

Verification is not a recap. It proves or disproves a specific claim with repeatable evidence.

## When To Use

- The user asks "verify this", "prove it works", "did this fix it", or "show me the evidence".
- A bug fix needs a before/after repro.
- A UI, CLI, API, performance, or memory claim needs measurement.
- A test passes but the user-visible behavior still needs confirmation.

If you are about to write that a UI bug is fixed or a UI feature works, run this skill first. A green unit test is a different surface than the user-visible repro. Only when the original bug was user-visible. A one-line copy fix does not need a full baseline/treatment artifact tree.

Do not use this for vague claims like "the code is cleaner". Ask for a measurable claim first.

## Workflow

1. Restate the claim in falsifiable form: condition, metric, and threshold.
2. For a UI behavior claim, split it into a case matrix per [`references/case-matrix-ui.md`](references/case-matrix-ui.md). Each row is its own falsifiable sub-claim. The happy path is one row.
3. Pick the smallest local surface that can disprove it.
4. Capture a baseline from the old state: merge base, parent commit, failing branch, or current broken repro. A matrix row that describes new behavior has no old state and needs treatment evidence only.
5. Capture treatment from the changed state with the same command, data, warmup, and environment. For a matrix, capture every row.
6. Compare raw artifacts: numbers, screenshots, terminal transcripts, HTTP responses, profiles, heap snapshots, or test output.
7. For a matrix, run `node scripts/check-matrix.mjs <matrix.tsv>` from this skill directory and fix what it prints.
8. Return exactly one verdict: `VERIFIED`, `NOT VERIFIED`, or `INCONCLUSIVE`.

## Local Surfaces

- Code behavior: focused unit/integration tests or a minimal repro script.
- CLI/TUI behavior: `control-cli`, terminal transcript, or demo recording.
- UI behavior: a case matrix, each row driven through `control-ui`, with screenshots, accessibility snapshots, or browser traces.
- API behavior: local HTTP/RPC request and response diff.
- Performance: same-machine baseline/treatment timings or CPU profiles.
- Memory: heap snapshots before and after the suspected operation.

## Artifact Layout

When safe to write artifacts:

```text
/tmp/verify-this/<claim-slug>/
├── claim.md
├── matrix.tsv
├── timeline.md
├── baseline/
├── treatment/
├── diff/
└── verdict.md
```

If artifacts may contain sensitive code, prompts, screenshots, HTTP bodies, or heap data, keep only the minimal inline evidence unless the user agrees to disk storage.

## Verdict Rules

- `VERIFIED`: baseline and treatment differ in the predicted direction, by the claimed threshold, with no obvious confound.
- `NOT VERIFIED`: the behavior is unchanged, moves the wrong way, or misses the threshold.
- `INCONCLUSIVE`: no valid baseline, noisy signal, failed measurement, or an environment difference invalidates the comparison.
- A UI claim is `VERIFIED` only when `check-matrix` exits 0. Any `FAIL` row makes it `NOT VERIFIED`. A matrix with only the happy path driven, a `TODO` row, or a missing dimension makes it `INCONCLUSIVE`, never `VERIFIED`.

## Output

Use this shape:

```text
VERIFIED | NOT VERIFIED | INCONCLUSIVE
Claim: <falsifiable claim>
Coverage: <the check-matrix coverage line, for a UI claim>

Evidence:
<metric/artifact>: baseline=<...>, treatment=<...>, delta=<...>, threshold=<...>

Reasoning:
<one tight paragraph naming the evidence and any confounds>
```

Do not soften a negative result. A clear `NOT VERIFIED` is useful.
