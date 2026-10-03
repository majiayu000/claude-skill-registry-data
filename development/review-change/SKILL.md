---
name: review-change
description: Use when the user says "review the change", "/review-change", "audit my working tree", "what's wrong with what I've got staged", "review without fixing", or asks Claude to audit the working tree's diff read-only without modifying files, committing, or pushing. Read-only mirror of /drive-change — same slice/fan-out/merge/verify pipeline, same finding-format output, never edits or commits. Always runs /review-code + /review-test + /review-feature + /review-security; adds /review-ux when UI extensions are touched. Produces a single terminal report grouped by severity. Use /drive-change when you want Claude to apply the fixes; use /review-change when you want the verdict and intend to act on it yourself.
allowed-tools: Bash(gh:*), Bash(git:*), Read, Grep, Glob, Skill, Task
---

# review-change

Read-only audit of the working tree's diff. Drives the change through the full agent pipeline (slice → fan-out → merge → verify) and emits findings in the structured format. Never edits, never commits, never pushes.

This is the read-only twin of `/drive-change`. Same audit, no writes.

For PR audit (instead of working tree), use `/review-pr`.

## Phase 0 — Scope

Determine the change scope. Default:
- `git diff HEAD` (committed-but-unpushed + uncommitted-but-tracked changes)
- plus staged-but-not-committed changes (`git diff --cached`)
- plus untracked files (`git status --porcelain | awk '/^\?\?/ {print $2}'`)

Where a sensible base exists, compare against the merge-base with the default branch:

```
base=$(git merge-base HEAD origin/main 2>/dev/null || git merge-base HEAD origin/master 2>/dev/null)
[ -n "$base" ] && git diff "$base"...HEAD
```

Apply exclusions: lockfiles, `dist/`, `build/`, `generated/`, `__generated__/`, `*.pb.*`, binary blobs, fixtures, vendored code.

If the scope is empty (no diff, no staged, no untracked), exit early with `No changes to review.`

## Phase 1 — Pull the change envelope

Build a [`references/change-envelope.md`](../../references/change-envelope.md)-shaped block:

- `### Diff` — concatenation of `git diff` outputs from Phase 0, plus per-untracked-file synthesized "all-additions" diffs (`diff --no-index /dev/null <file>`)
- `### Files` — flat list of paths
- `### Language hints` — derive from extensions, group by top-level directory
- `### Pre-fetched outlines` — when LSP available, `outline` per file (see [`references/language-tooling.md`](../../references/language-tooling.md))
- `### LSP edges` — when LSP available, `references` + `call_hierarchy` on changed symbols

If no LSPs are available, omit `Pre-fetched outlines` and `LSP edges`.

## Phase 2 — Triage

Apply the adaptive routing logic:

```
files_changed  = files from Phase 0 minus exclusions
loc_changed    = sum of additions + deletions
top_dirs       = unique first path segments

if len(files_changed) <= 5 and loc_changed <= 200:
    mode = "tiny"
elif len(files_changed) <= 30 and loc_changed <= 1500 and len(top_dirs) <= 3:
    mode = "small"
else:
    mode = "large"
```

Record `mode` under a `## Triage` heading along with the counts. Branch:

- `tiny` → Phase 4 only (single Opus pass with reviewer prompts inlined).
- `small` → Phases 4 + 5 (no slice, no verifier).
- `large` → full pipeline (Phases 3 + 4 + 5 + 6).

## Phase 3 — Slice (large only)

Invoke `agents/orchestrate-slice.md` via `Task`:

1. `Read` the agent file.
2. Concatenate with the change envelope from Phase 1.
3. `Task(subagent_type: "general-purpose", model: "opus", prompt: ..., timeout_ms: 240000, description: "Slice working-tree diff")`.
4. Parse the JSON fence.

On parse failure or timeout, emit a P0 meta-finding and fall back to single-slice mode. Never treat as zero slices.

## Phase 4 — Fan-out to /review-* specialists

For each slice (or whole diff in small/tiny mode), invoke read-only specialists in parallel via `Skill`:

- Always: `/review-hygiene`, `/review-code`, `/review-test`, `/review-feature`, `/review-security`
- Conditional: `/review-ux` (UI files touched), `/review-spec` (`.feature` or ADR files touched)

Each specialist receives a change envelope scoped to its slice.

## Phase 5 — Merge (per slice)

Invoke `agents/orchestrate-merge.md` via `Task` per slice:

1. `Read` the agent file.
2. Concatenate with:
   - `### Reviewer outputs`
   - `### Slice metadata` — `{ slice_name, files }`
   - `### Sensitivity patterns` — `Read('references/sensitivity-paths.md')`
   - `### Finding schema` — `Read('references/finding-format.schema.json')`
3. `Task(subagent_type: "general-purpose", model: "opus", prompt: ..., timeout_ms: 120000)`.
4. Parse: `work_packets`, `judgment_findings`, `discarded`, `drifted_reviewers`.

In `/review-change`'s read-only mode, `work_packets` are not dispatched — they appear in the report as "could be fixed mechanically."

## Phase 6 — Verify (large only)

Invoke `agents/orchestrate-verify.md` via `Task`:

1. `Read` the agent file.
2. Concatenate with `### Slices`, `### Per-slice findings`, `### Diff`, `### LSP availability`.
3. `Task(subagent_type: "general-purpose", model: "opus", prompt: ..., timeout_ms: 120000)`.
4. Parse: `findings`, `contracts_verified`.

Append verifier findings to the merger output for the final report.

## Phase 7 — Terminal report

Print findings grouped by severity:

```
[P0] [security] auth/session.ts:147 — refresh tokens stored in localStorage
  why: XSS-readable; one DOM injection exfiltrates every active session.
  fix: replace localStorage.setItem(...) with cookieStore.set
  reviewers: review-security, review-code
```

Summary footer:
- Total findings by severity
- Drifted reviewers
- Judgment findings (decisions for the user)
- Cross-slice contract status (large mode only)
- Work packets that could be applied mechanically (with `/drive-change` to act on them)

No `--comment` mode — this skill doesn't have a PR to comment on. Use `/review-pr` for that.

## Operating rules

- **Read-only is non-negotiable.** `Edit`, `Write`, `git commit`, `git push` are not in `allowed-tools`. Structural guard.
- **Untracked files are in scope.** The user often hasn't staged or committed yet. Synthesize an "all-additions" diff for each untracked file.
- **Findings are always structured.** Skip rather than prose.

## Composing with other skills

- Calls: `/review-hygiene`, `/review-code`, `/review-test`, `/review-feature`, `/review-security`, `/review-ux` (conditionally), `/review-spec` (conditionally) — via `Skill`.
- Invokes: `agents/orchestrate-slice.md`, `agents/orchestrate-merge.md`, `agents/orchestrate-verify.md` — via `Task`.
- Sibling: `/review-pr` (PR audit), `/drive-change` (writes), `/drive-plan` (composes /review-change as its Phase 3).
