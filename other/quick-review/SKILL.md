---
name: quick-review
description: 'Reviews uncommitted changes inline without saving by default. Use when requesting a quick review, checking a small local diff, or reviewing without a saved artifact.'
argument-hint: '[--parallel | --team] [--yes | --save | --write-and-apply] [--severity <level>] [--no-worktree]'
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Skill
  - Agent
  - AskUserQuestion
  - TaskCreate
  - TaskUpdate
  - TaskList
  - TaskGet
  - SendMessage
  - Bash(git:*)
  - Bash(ls:*)
  - Bash(cat:*)
  - Bash(test:*)
  - Bash(mkdir:*)
  - Bash(date:*)
---

# Quick Review

Interactive low-friction review of uncommitted changes. Output is **inline**. The default fix path is artifact-free.

**Operational context:** "Apply fixes" delegates inline findings to /ycc:quick-fix without an artifact; "Save to file" saves under docs/prps/reviews/; "Write file and apply fixes" saves an artifact and delegates to /ycc:review-fix. Writes require confirmation unless a documented scripted action selects them.

**Input**: `$ARGUMENTS`

**Core rule**: "Apply fixes" must not write a review artifact. It hands the
inline findings directly to `/ycc:quick-fix`. Only "Save to file" and
"Write file and apply fixes" write `docs/prps/reviews/quick-*.md`.

---

## Phase 0 — Parse flags

Extract flags from `$ARGUMENTS`:

| Flag                 | Effect                                                                                                                                                                                      |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--parallel`         | Fan out REVIEW across 3 standalone `ycc:code-reviewer` sub-agents (correctness, security, quality) and merge findings. Works in Claude Code, Cursor, and Codex bundles.                     |
| `--team`             | (Claude Code only) Same 3-reviewer fan-out as a coordinated agent team with shared `TaskList`, per-reviewer `TaskCreate`, and coordinated shutdown. Heavier dispatch, richer communication. |
| `--yes`              | Skip the confirmation prompt and behave as "Apply fixes" through `/ycc:quick-fix`. Mutually exclusive with `--save` and `--write-and-apply`.                                                |
| `--save`             | Skip the confirmation prompt and behave as "Save to file" (write artifact, print Next steps, exit). Mutually exclusive with `--yes` and `--write-and-apply`.                                |
| `--write-and-apply`  | Skip the confirmation prompt, write the review artifact, then hand off to `/ycc:review-fix`. Mutually exclusive with `--yes` and `--save`.                                                  |
| `--severity <level>` | Forwarded to `/ycc:quick-fix` or `/ycc:review-fix` during hand-off. Valid: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`. Default: `HIGH`. Ignored on "Save to file" / "Discard".                     |
| `--no-worktree`      | Accepted as a **no-op**. Quick mode never creates a worktree. Emit a note: `--no-worktree has no effect in quick mode.`                                                                     |

Strip these from `$ARGUMENTS` and set `PARALLEL_MODE`, `AGENT_TEAM_MODE`,
`AUTO_YES`, `AUTO_SAVE`, `AUTO_WRITE_AND_APPLY`, and `MIN_SEVERITY` (default
`HIGH`). The remaining text MUST be empty; if not, abort with:

```
Error: /ycc:quick-review takes no positional argument (only flags).
```

**Validation**:

- `--parallel` and `--team` mutually exclusive -> abort with: `--parallel and --team are mutually exclusive. Pick one.`
- More than one of `--yes`, `--save`, `--write-and-apply` present -> abort with: `--yes, --save, and --write-and-apply are mutually exclusive. Pick one.`
- `--team` in a Cursor/Codex bundle (no agent team support) -> abort with: `--team is not supported in bundle invocations; use --parallel instead.`
- `--team` passed while `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is not set to `1` in the environment -> abort with: `--team requires CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1. Use --parallel instead, or set CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 in your Claude Code settings if you intentionally want agent-team dispatch.`
- `--severity` value not one of `CRITICAL|HIGH|MEDIUM|LOW` -> abort with: `Invalid --severity value. Use CRITICAL, HIGH, MEDIUM, or LOW.`

**Questions:** class `choose-path` (Phase 4 review action); headless (no question tool or chat turn): behave as `--save` (Save to file). See `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/question-policy.md`.

---

## Phase 1 — GATHER

```bash
git diff --name-only HEAD
```

If the output is empty, print `Nothing to review.` and exit. Do NOT prompt,
do NOT write anything.

Capture the list of changed files as `CHANGED_FILES` for the REVIEW phase.

---

## Phase 2 — REVIEW

Neither flag: **Path A** single-pass (default). `PARALLEL_MODE`: **Path B**,
3 parallel reviewers. `AGENT_TEAM_MODE`: **Path C**, 3-reviewer agent team.

Findings from all paths stay **in memory**. Do not write to disk here.

### Path A — Single-Pass Review (default)

Read each changed file in full and apply the **Local / Quick Review —
Single-Pass Checklist** and **Severity Rubric**. Flag only gaps that affect
correctness or the stated requirements. From:

```
${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/review-checklist.md
```

### Path B / C — fan-out (`PARALLEL_MODE` or `AGENT_TEAM_MODE`)

Generate `TIMESTAMP=$(date +%Y%m%d-%H%M%S)` once; reuse it for run-id
`quick-<TIMESTAMP>`, the team name, and any later `quick-<TIMESTAMP>-review.md`.
Read only on this path:

- `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/review-dispatch.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/standalone-dispatch.md` (`--parallel`)
- `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/agent-team-dispatch.md` (`--team`)

Use the Local / Quick Mode Roster and Standard Findings Format from
`review-checklist.md`; merge via its Merge Procedure into one list for Phase 3.
The reviewer prompt states: flag only gaps that affect correctness or the
stated requirements. Scratch under
`docs/prps/reviews/.review-scratch/quick-<TIMESTAMP>/` is always removed at the
end of Phase 5, even on "Discard" and "Apply fixes" — the one ephemeral
exception to the artifact-free guarantee.

---

## Phase 3 — REPORT (inline)

Assign IDs and initial Status after merge using the shared artifact schema
loaded below (Finding ID rules: ordered by severity, CRITICAL first, then by
file path); the same contract applies to inline findings.

Compute:

- `critical_count`, `high_count`, `medium_count`, `low_count`
- `total_findings`
- `finding_file_count` (unique files with findings)
- `large_review = total_findings >= 5 || finding_file_count >= 3`

**Print** the review to stdout in the quick-mode variant of the Review Artifact
Format, **without** writing a file. Read the schema:

`${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/review-artifact-format.md`

Header: `# Quick Review — Uncommitted Changes`, `**Mode**: Quick (inline)`,
`**Author**: local`, `**Branch**: <current-branch>`,
`**Decision**: (pending user confirmation)`, then Summary, Findings (all four
fields per finding, `Status: Open`) and Files Reviewed. No Worktree Setup or
Validation Results sections. Categories: Security | Correctness | Code Quality
| Best Practices.

After the artifact block, print:

```
Findings: [C] {critical_count}  [H] {high_count}  [M] {medium_count}  [L] {low_count}
```

If `large_review=true`, also print:

```
Large quick review: {total_findings} findings across {finding_file_count} files.
You can still apply fixes directly, or write an artifact before applying fixes for an audit trail.
```

If the count is zero across all severities, skip Phase 4 entirely. Print
`No findings. Nothing to do.` and exit.

Keep the exact printed review block in memory as `INLINE_REVIEW_PAYLOAD` for
`/ycc:quick-fix` or artifact writing.

---

## Phase 4 — DECIDE (confirmation)

If `AUTO_YES=true` -> skip this phase, proceed directly to Phase 5 as if the
user selected "Apply fixes".

If `AUTO_SAVE=true` -> skip this phase, proceed directly to Phase 5 as if the
user selected "Save to file".

If `AUTO_WRITE_AND_APPLY=true` -> skip this phase, proceed directly to Phase 5
as if the user selected "Write file and apply fixes".

Otherwise, ask the user with `AskUserQuestion`.

For normal reviews (`large_review=false`):

```
question: "What should I do with this review?"
header:   "Review action"
options:
  - label: "Apply fixes"
    description: "Hand findings directly to /ycc:quick-fix. No review file is written. (recommended)"
  - label: "Save to file"
    description: "Write docs/prps/reviews/quick-<timestamp>-review.md and stop."
  - label: "Discard"
    description: "Write nothing, exit"
```

For large reviews (`large_review=true`):

```
question: "This is a larger quick review. What should I do?"
header:   "Review action"
options:
  - label: "Apply fixes"
    description: "Hand findings directly to /ycc:quick-fix. No review file is written."
  - label: "Write file and apply fixes"
    description: "Write docs/prps/reviews/quick-<timestamp>-review.md, then use /ycc:review-fix for an audit trail. (recommended)"
  - label: "Save to file"
    description: "Write docs/prps/reviews/quick-<timestamp>-review.md and stop."
  - label: "Discard"
    description: "Write nothing, exit"
```

Mark "Apply fixes" with `(Recommended)` when `large_review=false` and
`critical_count + high_count > 0`. Mark "Write file and apply fixes" with
`(Recommended)` when `large_review=true`.

**Text-mode fallback** (no question tool, chat turn available): follow the shared
fallback in `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/question-policy.md`.
Reply synonyms (case-insensitive):

- `yes` / `apply` / `apply fixes` / `fix` -> "Apply fixes"
- `write and apply` / `write file and apply fixes` / `file and fix` / `artifact and fix` -> "Write file and apply fixes"
- `save` / `save to file` / `write` / `file` -> "Save to file"
- `no` / `discard` / `cancel` / `skip` -> "Discard"
- Anything else -> re-prompt once, then default to `Discard` if still ambiguous.

---

## Phase 5 — HAND-OFF

Branch on the user's selection (or auto-confirm flag). If `PARALLEL_MODE=true`
(Path B was used), remove the `docs/prps/reviews/.review-scratch/quick-<TIMESTAMP>/`
scratch directory before exiting — **regardless of which branch below is
taken**, including "Discard" and "Apply fixes".

### Selection: "Discard"

Print `Discarded. No artifact written.` and exit. Do NOT write any file.

### Selection: "Apply fixes"

Invoke the `ycc:quick-fix` skill inline via the `Skill` tool. Do NOT write an
artifact first.

- `skill`: `"ycc:quick-fix"`
- `args`: `"[--parallel] [--severity <level>] <INLINE_REVIEW_PAYLOAD>"`

Forward `--parallel` if `PARALLEL_MODE=true`. Forward `--severity <level>` when
`MIN_SEVERITY != HIGH` (HIGH is the default on quick-fix).

After the Skill call returns, print:

```
Fixes complete. No review artifact was written.
```

Exit.

### Selection: "Save to file"

Write the artifact to disk using the Phase 3 content plus the canonical header
block:

```bash
mkdir -p docs/prps/reviews
TIMESTAMP=$(date +%Y%m%d-%H%M%S)    # reuse the Path C timestamp if set
REVIEW_FILE="docs/prps/reviews/quick-${TIMESTAMP}-review.md"
```

Write the same artifact content that was printed in Phase 3, but set
`**Decision**: COMMENT` in the header (since a review was produced but no
GitHub decision is being posted).

Print:

```
Quick review written to: docs/prps/reviews/quick-<TIMESTAMP>-review.md
Findings: [C] {critical_count}  [H] {high_count}  [M] {medium_count}  [L] {low_count}

Next steps:
  /ycc:review-fix docs/prps/reviews/quick-<TIMESTAMP>-review.md              # apply fixes {recommended_single if 1-2 Open findings}
  /ycc:review-fix docs/prps/reviews/quick-<TIMESTAMP>-review.md --parallel   # fan out fixes {recommended_parallel if 3+ Open across 2+ files}
```

Annotate ONE command with `# <- recommended`:

- 1-2 Open findings -> recommend the single-pass form.
- 3+ Open findings spanning 2+ files -> recommend the `--parallel` form.
- Otherwise default to the single-pass form.

Exit.

### Selection: "Write file and apply fixes"

Step 1 — write the artifact to disk exactly as in "Save to file".

Step 2 — invoke the `ycc:review-fix` skill inline via the `Skill` tool:

- `skill`: `"ycc:review-fix"`
- `args`: `"<REVIEW_FILE> [--parallel] [--severity <level>]"`

Forward `--parallel` if `PARALLEL_MODE=true`. Forward `--severity <level>` when
`MIN_SEVERITY != HIGH`.

Step 3 — after the Skill call returns, print:

```
Fixes complete. Review artifact updated in place: docs/prps/reviews/quick-<TIMESTAMP>-review.md
```

Step 4 — exit.

**Note**: `--team` from quick-review is NOT forwarded to either fix workflow
automatically. The review-phase fan-out is about finding issues quickly; the
fix phase has its own execution decision.

---

## Important Notes

- **Apply fixes is artifact-free**: direct apply routes to `/ycc:quick-fix`
  without writing `docs/prps/reviews/quick-*.md`.
- **Scratch is the one ephemeral exception**: when Path B (`--parallel`) is
  used, the calling skill persists each valid inline return to its scratch copy
  at `docs/prps/reviews/.review-scratch/quick-<TIMESTAMP>/<reviewer-name>.md`
  during the `Agent` dispatch in Phase 2. It is always deleted at the end of
  Phase 5 before the skill returns control to the user — including on
  "Discard" and "Apply fixes" — so the "no file written" guarantee still
  holds for anything the user can observe afterward.
- **Large reviews are advisory**: `5+` findings or `3+` finding files adds a
  "Write file and apply fixes" choice. It does not force artifact creation.
- **Explicit artifact-backed apply**: only `--write-and-apply` or the matching
  prompt choice writes the artifact and invokes `/ycc:review-fix`.
- **Idempotent filename**: the `quick-{YYYYMMDD-HHMMSS}-review.md` pattern
  produces a new file per artifact-writing invocation — no overwrites.
- **Not a replacement for `/ycc:code-review`**: if you need toolchain
  validation (typecheck/lint/test/build), a `## Validation Results` block,
  worktree isolation, or a GitHub review posted, use `/ycc:code-review`
  without `--quick`.

---

## Integration with ycc

- `/ycc:code-review --quick` delegates to this skill.
- `/ycc:quick-fix` consumes inline findings for artifact-free fixing.
- `/ycc:review-fix` consumes written artifacts only.
- `/ycc:prp-commit` or `/ycc:git-workflow --commit` can commit the fixes afterward.
