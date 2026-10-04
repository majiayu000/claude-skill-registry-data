---
name: parallel-code-review
description: Weekly chunked code-review gate. /workweek-complete only.
argument-hint: "[--force] [--gate-mode strict|advisory]"
version: 2.0.0
allowed-tools: ["Read","Write","Edit","Bash","Grep","Glob","Agent","Skill","AskUserQuestion","TaskCreate","TaskUpdate","TaskGet","TaskList"]
---

# Parallel Code Review

## Overview

The /workweek-complete pre-merge code-review gate. Snapshots the week's diff against
`origin/main`, dispatches N `code-reviewer-weekly` chunk reviewers over the narrowed
code-semantics scope plus 3 mechanical specialists (security, deps, tests) over the full diff —
all in parallel — synthesizes into BLOCKED/WARN/OK, halts or proceeds before release notes.
Enforcement surface for `${CLAUDE_PLUGIN_ROOT}/snippets/em-operating-doctrine.md` § How to Review What Came
Back. The Staff Engineer's Layer-2 pass runs separately at `/workweek-complete` Step 7.5 (wiki).

## Wrong-Context Refusal

Invoked exclusively from coordinator:/workweek-complete, by the top-level EM
(`A-SKILL-PHASE-NAMES-ITS-ACTOR`). Reached any other way — STOP, surface the misroute to the PM.
`coordinator/skills/review/SKILL.md` § A.3 governs every other surface.

---

## Gate, Chunk, and Resolver Decisions

Three CLI calls drive dispatch shape; each prints a decision envelope whose `next_move` field is
the literal next step to take. **On a PowerShell host, invoke the `.exe` launcher by absolute path
through the call operator** (Shape W) for every invocation on this page, never the `${...}`
POSIX-shell form shown below. Ladder and shapes: `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`.

- **Gate:** invoke `parallel-review-gate-decision gate --range "origin/main...HEAD" [--force]`,
  resolved per `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md` (Shape A/B on POSIX hosts, Shape W on
  PowerShell). `judgment_points` is always `[]` here.
- **Chunking:** same binary, `chunk --scope-files-file <scope-files> --seam-manifest-file
  <seam-manifest> [--target-size 25] --out "$FINDINGS_DIR/chunk-manifest.tsv"` — `<scope-files>`
  is `staff_eng_scope`'s narrowed code-semantics scope (the 3 specialists still see the full
  diff), `<seam-manifest>` a `<file>\t<session_id>` TSV. Skip entirely on a doc-only week; write
  `printf 'skipped: doc-only\n' > "$FINDINGS_DIR/code_semantics_skip.sentinel"` instead.
- **Test resolver:** `parallel-review-gate-decision resolver-branch --resolver-exit
  "$RESOLVER_EXIT" --test-cmd "$TEST_CMD"` (after resolving `$TEST_CMD`/`$RESOLVER_EXIT` per Test-
  Output Capture below).

**Rule 5 is the one EM judgment here, never auto-fired.** On a large catch-up span where every
workstream carries a review-trail verdict, run `rule5-inputs --scope-shas-file <scope-shas>
--seam-files-file <seam-files> --review-trail-dir state/review-trail`; decide **(a) skip**
(record `incrementally-reviewed`, name the records) or **(b) narrow** to `unreviewed_set`. Wiki.

---

## Pre-Flight Orthogonality Assertion

Before dispatch: invoke `parallel-review-orthogonality-guard guard`, resolved per
`${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md` (Shape A/B on POSIX hosts, Shape W on PowerShell). Non-zero
— do not dispatch, surface to the PM.

After chunking, before dispatching chunk reviewers: same command with `--chunk-manifest
"$FINDINGS_DIR/chunk-manifest.tsv"`. Non-zero — re-chunk.

---

## Snapshot

Invoke `parallel-review-orthogonality-guard snapshot --range "origin/main...HEAD"`, resolved per
`${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`. Capture its four printed fields as
`$FINDINGS_DIR`, `$WEEKLY_SLICE_ID`, `$DIFF_PATH`, `$HEAD_SHA_PATH` — the only copies; reviewers
and the synthesizer read them directly, never from `$FINDINGS_DIR`.

### Test-Output Capture — Tier-U, EM-only

`/workweek-complete` holds this ceremony's implicit Tier-U grant. Consult it anyway, resolved per
`${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md` (Shape A/B on POSIX hosts, Shape W on PowerShell):
`tier-u-grant-cli check`.
Ungranted (exit 1, or malformed/absent) — halt, surface to the PM, skip this step.

Resolve: `coordinator-resolve-validation-cmd --full` (same resolution) → `$TEST_CMD` / `$RESOLVER_EXIT`. Set
`TEST_OUTPUT_PATH="state/review-trail/diffs/${WEEKLY_SLICE_ID}.test.log"`, then run the
resolver-branch decision above and act on its `next_move`.

Pre-scaffold (`Edit` cannot create a file): `printf '<!-- FINDINGS -->\n' >
"$FINDINGS_DIR/tests.md"`. On `RESOLVER_EXIT=2`, still write it but don't dispatch
test-evidence-parser (it surfaces as `failed_disk_read`).

---

## Parallel Dispatch

> **Do not ask whether to dispatch** — invoking this skill IS the request for the dispatch this
> step names; it dissolves no gate this skill's own body names.

**Dispatch the whole span as one Workflow — `Workflow({scriptPath: "coordinator/workflows/review-wave.mjs", args: {...}})`.** It encodes this
section and the synthesizer dispatch below; its `args` contract is in the script's own header.
Pre-provision each dispatched agent's sidecar first, resolved per
`${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md` (Shape A/B on POSIX hosts, Shape W on PowerShell) —
`provision-sidecar --agent-type <type> --provision-key <slice-id>` — and inject the printed path
as `sidecar_path:` in its brief: a Workflow spawn never auto-provisions one. Omit
`testOutputPath` on an unconfigured-resolver (`RESOLVER_EXIT=2`) week and the parser is skipped.

The gate is not a checkpoint: reviewers run to completion without pausing for EM authorization;
oversight is on disk and after the fact (findings files, sidecars), reverted like any landed change.

**Hand-dispatch is the fallback for a broken vehicle, not a preference.** If the Workflow refuses,
dispatch all active reviewers in one multi-tool-call batch and say why. Each reviewer reads its own
frozen input and writes only its own findings file. The fallback's named `Agent` dispatch requires
agent teams (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, session-start-only); the `Workflow` path
does not.

- **Chunk reviewers** (`agents/code-reviewer-weekly.md`, skip all if `SKIP_CODE_SEMANTICS=1`): one
  per chunk, its file-scope list plus `$DIFF_PATH`, writing **only** `$FINDINGS_DIR/chunk-<k>.md`
  incrementally. Marks `escalate_to_architecture: true` where relevant. Findings the reviewer
  applies land in the diff itself, verified via `review-findings-ledger verify`, not this file.
- **security-audit-worker**: `$DIFF_PATH` → `$FINDINGS_DIR/security.md`.
- **dep-cve-auditor**: repo manifests at HEAD vs. `$DIFF_PATH` → `$FINDINGS_DIR/deps.md`.
- **test-evidence-parser**: `$TEST_OUTPUT_PATH` → `$FINDINGS_DIR/tests.md` via one `Edit` on the
  pre-scaffolded sentinel. Skip on `RESOLVER_EXIT=2`.

These four are orthogonal lenses; the N chunk reviewers partition one by file-scope. Rationale
and the two orthogonality assertions: wiki.

Reviewers never commit. A chunk reviewer's footprint is exactly its one `chunk-<k>.md` —
anything else is a contract violation to revert.
<!-- engine-gap: field=chunks[k].footprint producer=unknown memo=engine-gap-markers-name-a-memo-that-was-never-filed.md -->

## Lens-Domain Manifest

Machine-readable form of the four lenses. `verify-parallel-review-lens-orthogonality` parses this
table (agent files exist, no shared lens domain, at least four rows) and fails closed.

| Reviewer | Lens domain |
|---|---|
| `agents/code-reviewer-weekly.md` | code semantics |
| `agents/security-audit-worker.md` | source security |
| `agents/dep-cve-auditor.md` | dependency CVEs |
| `agents/test-evidence-parser.md` | test evidence |

---

## Synthesizer Pre-Flight and Dispatch

Each expected findings file (chunk-*.md glob + active specialists, or the skip sentinel on a
doc-only week) must exist and be >1KB before the synthesizer runs. A failing/missing file:
`lens_coverage[<reviewer>]: failed_disk_read`, degrade to WARN, never "no findings = no issues."

**Quota-exhausted dispatch.** Scan each returned slice against
`${CLAUDE_PLUGIN_ROOT}/snippets/quota-self-detect-preamble.md`'s pattern set before synthesizer dispatch — a
match (or the `QUOTA-EXHAUSTED-DISPATCH:` envelope) is failed-needing-re-dispatch, excluded from
synthesis. Wait-and-re-dispatch or escalate partial coverage to the PM; the gate holds until
resolved.

A non-quota failed dispatch: retry once via `SendMessage` (never redispatch from scratch). Second
failure: `failed_disk_read`/WARN degrade — an infra dropout never blocks.

Once all present files pass, dispatch Sonnet `parallel-review-synthesizer`
(`agents/parallel-review-synthesizer.md`) with `$HEAD_SHA_PATH` (not mirrored into
`$FINDINGS_DIR`). It owns verdict computation, convergence detection, and
`arch_tier_candidates` aggregation — this skill does not restate its rules. Writes
`$FINDINGS_DIR/synthesis.json`.

`review-wave.mjs`'s Synthesize phase runs this span; the rules here are the contract either
vehicle satisfies.

---

## Verdict Emission and Gate Behavior

Read `verdict`/counts from `$FINDINGS_DIR/synthesis.json`, format:

```markdown
**Code-review gate:** [BLOCKED|WARN|OK] — convergent: N — code-semantics: <N chunks, P0/P1/P2/nit counts> — arch-tier candidates: <count> — security: <count> — deps: <count> — tests: <pass/fail/flake>
```

BLOCKED halts `/workweek-complete` before Step 9 and Step 11, surfacing the line and
`synthesis.json` path to the PM — fix and re-run, or `--force`, never proceed silently. WARN
carries the line into the release-notes draft (Step 9) and the eventual PR body. OK proceeds
silently. `arch-tier candidates` feeds the Staff Engineer's Layer-2 pass, never this verdict.

---

Cost discipline, worked examples, the chunking algorithm, and the carve-out enforcement mapping:
wiki.
