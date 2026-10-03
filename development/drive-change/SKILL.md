---
name: drive-change
description: Use when the user says "/drive-change", "drive the change", "make this change happen", "implement and review", "ship this fix", or wants Claude to drive a change end-to-end (implement if needed + audit + fix) without going through formal planning. For quick or clear changes where the implementation can be derived from conversation intent. For substantial changes warranting an ADR + Gherkin spec, use /drive-plan instead. drive-change runs the audit pipeline (slice → fan-out to /review-* specialists in parallel → merge with apply-validation → cross-slice verify → dispatch fix-applier agents under sensitivity gating). Sensitive paths (auth, crypto, IPC) route to Opus fix-appliers; everything else goes to Sonnet. Adds /review-ux automatically if UI files are touched (.tsx/.jsx/.vue/.svelte/.astro/.html/.css/.scss/.less). Produces a single unified report grouped by severity.
allowed-tools: Bash(gh:*), Bash(git:*), Read, Edit, Write, Grep, Glob, Skill, Task
---

# drive-change — implement + audit + fix the current change

`/drive-change` is the workhorse for changes that don't need formal planning. It:

1. Writes the implementation if conversation intent describes work to do.
2. Runs the full audit pipeline (slice → fan-out to `/review-*` specialists → merge → verify) via the agent layer.
3. Dispatches fix-applier agents in parallel to act on the findings (sensitivity-gated to Opus when the file path matches auth/crypto/IPC patterns).
4. Produces a unified report grouped by severity.

For substantial changes warranting an ADR + Gherkin spec, use `/drive-plan` instead. For audit-only (no fixes), use `/review-change`.

## Phase 0 — Scope

Find what changed:

```bash
# PR context first
gh pr diff --name-only 2>/dev/null

# Working tree fallback
git diff --name-only HEAD
git diff --name-only --cached
git ls-files --others --exclude-standard
```

Build the list of touched files. Exclude lockfiles, generated files (`linguist-generated=true`, `dist/`, `build/`, `generated/`, `__generated__/`, `*.pb.*`), binary blobs, fixtures, vendored code — same exclusions as `/review-code` Phase 0.

Then branch:

- **List empty AND user described work to do**: proceed to Phase 1 (Implementation).
- **List empty AND no implementation intent expressed**: stop with `"No changes to drive, and no implementation intent given. Tell me what you want to implement, or use /review-change to audit the working tree if you meant audit-only."`
- **List non-empty**: skip Phase 1 — the work is already done. Proceed to Phase 2.

## Phase 1 — Implement from conversation intent (when needed)

This phase runs only when the working tree is clean and the user has described work to be done. It writes the implementation directly without invoking `/implement-change` — that skill requires a formal ADR + spec, which we don't have here.

The pattern:

1. Restate the change in one sentence. Confirm with the user before writing.
2. Map the touched surface (LSP-preferred — see [`references/language-tooling.md`](../../references/language-tooling.md)).
3. Apply edits via `Edit` and `Write`.
4. Commit logically (one commit per coherent step; match `git log -5` for message style).

After Phase 1, the working tree is no longer clean — the diff carries the new code. Proceed to Phase 2 with that diff as scope.

**If the change is substantial** (touches more than the small-mode threshold of 30 files or 3 top-level dirs), stop and recommend `/drive-plan` instead — at that size, formal planning before implementation pays for itself.

## Phase 2 — Decide whether to include UX

Glob the touched files for UI extensions:

```bash
<touched-files> | grep -E '\.(tsx|jsx|vue|svelte|astro|html|css|scss|less)$' | head -1
```

If at least one match, include `/review-ux`. Otherwise skip it.

Also include UX if a framework route file changed:

```bash
<touched-files> | grep -E '(app|pages|src/routes)/.*\.(tsx?|jsx?)$' | head -1
```

The URL surface is in scope when route files change.

## Phase 3 — Build the change envelope

Build a [`references/change-envelope.md`](../../references/change-envelope.md)-shaped block — same shape the read-only orchestrators (`/review-change`, `/review-pr`) use:

- `### Diff` — concatenation of `git diff HEAD` + `git diff --cached` + untracked-file "all-additions" diffs
- `### Files` — flat list of touched paths
- `### Language hints` — derive from extensions per top-level directory
- `### Pre-fetched outlines` — when LSP available, `outline` per file (see [`references/language-tooling.md`](../../references/language-tooling.md))
- `### LSP edges` — when LSP available, `references` + `call_hierarchy` on changed symbols

If no LSPs are available for the languages in scope, omit `Pre-fetched outlines` and `LSP edges` — the slicer's structural fallback will handle it.

## Phase 4 — Triage and run the agent pipeline

Apply the adaptive routing logic:

```
files_changed  = files in scope minus exclusions
loc_changed    = sum of additions + deletions
top_dirs       = unique first path segments

if len(files_changed) <= 5 and loc_changed <= 200:
    mode = "tiny"
elif len(files_changed) <= 30 and loc_changed <= 1500 and len(top_dirs) <= 3:
    mode = "small"
else:
    mode = "large"
```

Branch by mode:

### Tiny mode

Skip slice/fan-out/merge/verify. Single Opus pass with reviewer prompts inlined. Apply mechanical fixes directly (Edit + git commit per logical change). Skip to Phase 7 (report).

### Small mode

Fan-out to `/review-*` specialists in parallel via `Skill`, then merge via `agents/orchestrate-merge.md`. Skip slice and verify.

### Large mode

Full pipeline: `orchestrate-slice` → per-slice fan-out → `orchestrate-merge` per slice → `orchestrate-verify` cross-slice.

### Agent invocations

**Slice (large mode only):**

1. `Read` `agents/orchestrate-slice.md`.
2. Concatenate with the envelope from Phase 3.
3. `Task(subagent_type: "general-purpose", model: "opus", prompt: <agent + envelope>, timeout_ms: 240000, description: "Slice diff into domain units")`.
4. Parse the JSON fence. On timeout or parse failure, emit a P0 meta-finding and fall back to single-slice (treat the whole diff as one slice).

**Fan-out (small or large mode):**

For each slice (or the whole diff in small mode), invoke read-only review specialists in parallel via `Skill`:

- Always: `/review-hygiene`, `/review-code`, `/review-test`, `/review-feature`, `/review-security`
- Conditional: `/review-ux` (Phase 2 decision), `/review-spec` (`.feature` or ADR files touched)

Each specialist receives a change envelope scoped to its slice.

**Merge (small or large mode, per slice):**

1. `Read` `agents/orchestrate-merge.md`.
2. Concatenate with:
   - `### Reviewer outputs` — concatenated reviewer transcripts with `--- reviewer: <name> ---` markers
   - `### Slice metadata` — `{ slice_name, files }`
   - `### Sensitivity patterns` — `Read('references/sensitivity-paths.md')`
   - `### Finding schema` — `Read('references/finding-format.schema.json')`
3. `Task(subagent_type: "general-purpose", model: "opus", prompt: ..., timeout_ms: 120000)`.
4. Parse: `work_packets`, `judgment_findings`, `discarded`, `drifted_reviewers`.

**Verify (large mode only):**

1. `Read` `agents/orchestrate-verify.md`.
2. Concatenate with `### Slices`, `### Per-slice findings`, `### Diff`, `### LSP availability`.
3. `Task(subagent_type: "general-purpose", model: "opus", prompt: ..., timeout_ms: 120000)`.
4. Parse: `findings`, `contracts_verified`.

## Phase 5 — Dispatch fix-applier agents

For each `work_packet` from the merger output:

1. `Read` `agents/fix-applier.md`.
2. Concatenate with `## Input\n### Packet\n<work_packet as JSON>`.
3. `Task(subagent_type: "general-purpose", model: packet.suggested_model, prompt: ..., timeout_ms: 180000, description: "Apply N findings on packet.file")`.
4. Dispatch all packets **in parallel** — the merger guaranteed file-partition, so no write collisions.
5. Parse each return: `applied`, `unappliable`, `skipped_judgment`, `post_apply_validation`.

`judgment_findings` from the merger are **not** dispatched. Surface them to the user as "decisions to make" — they'll respond, and on confirmation you can construct a synthetic work packet with the resolved fix and dispatch then.

## Phase 6 — Re-run loop

After all fix-appliers return, re-run the audit pipeline (Phases 3–5) to see if new findings emerged from the applied changes. Loop until:

- No new findings reach steady state, **or**
- The user calls it done, **or**
- 3 iterations elapsed without convergence — surface to user that we're not converging.

If P0/P1 findings remain that fix-applier marked unappliable, surface to user — they may need manual intervention.

## Phase 7 — Unified report

Produce a single combined report:

```
drive-change ran on <PR #N or working tree>.

  Mode: tiny | small | large
  Slices: <N>            (large only)
  Specialists: review-hygiene, review-code, review-test, review-feature, review-security[, review-ux][, review-spec]

Findings, severity-ordered:

  P0  <one-line finding>     auth/session.ts:147     (review-security)
  P0  <one-line finding>     api/orders.ts:23        (review-feature)
  P1  <one-line finding>     src/orders/cancel.ts:88 (review-feature)
  P2  <one-line finding>     ...

Fix-applier results:
  applied:           <N>
  unappliable:       <N> — see details below
  judgment escalated: <N> — listed below

Cross-slice contracts (large only):
  consistent:    <N>
  broken:        <N> — see findings above
  unverifiable:  <N>

Drifted reviewers (if any):
  review-X: <N> findings discarded by schema validation — possible prompt drift

Next steps:
  - <suggested action>
```

Build from the merger output and fix-applier returns, NOT from re-reading transcripts. The structured output is the source of truth.

Group findings by severity, not by sub-audit. The user wants "what to fix and in what order", not a wall of text per audit.

## Phase 8 — Recommend next step

End the report with one of:

- **No findings, clean apply**: "Ready for `/open-pr`."
- **Only P2 polish**: "Safe to `/open-pr` now; P2 findings can land in a follow-up."
- **Unappliable P0/P1**: "Manual intervention needed on the unappliable findings above before `/open-pr`."
- **Judgment escalated**: "Review the judgment findings above and decide; I can dispatch fixes once you confirm."

The user decides; the skill states the read.

## Operating rules

- **Phase 1 implementation is direct.** `/drive-change` writes code from conversation intent. For formal planning, use `/drive-plan`. For audit-only, use `/review-change`.
- **The pipeline shape is the same across modes.** Tiny/small/large differ only in which agent invocations are skipped — never in the underlying contracts.
- **Findings flow through the schema.** Every reviewer emits structured findings; the merger validates; the fix-applier consumes already-validated input. No prose handoffs.
- **Sensitivity gating is the merger's job.** Don't second-guess `suggested_model` on a work packet — the merger applied the gate; honour it.
- **Dispatch in parallel.** Fix-appliers don't share files. The merger guaranteed this. Don't serialize without reason.
- **Drifted reviewers are a finding, not a silent failure.** If the merger reports a reviewer had schema failures, surface it in the report — the user may need to adjust that reviewer's prompt.
- **Don't open the PR.** That's `/open-pr`. `/drive-change` is pre-PR; `/drive-pr` is post-open iteration.

## Composing with other skills

- **Calls (via Skill):** `/review-hygiene`, `/review-code`, `/review-test`, `/review-feature`, `/review-security`, `/review-ux` (conditional), `/review-spec` (conditional).
- **Invokes (via Task):** `agents/orchestrate-slice.md`, `agents/orchestrate-merge.md`, `agents/orchestrate-verify.md`, `agents/fix-applier.md`.
- **Before:** none directly — this is the entry point for unplanned changes. For planned changes, `/drive-plan` runs `/plan-change` → `/implement-change` → `/review-change` → here.
- **After:** `/open-pr` (turn the change into a PR), then `/drive-pr` (drive the PR to mergeable).
- **Sibling:** `/drive-plan` (with formal planning), `/drive-pr` (post-open).
