---
name: code-health
description: "Night-shift code review: dispatch, apply findings, track."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "Agent"]
argument-hint: (no arguments needed)
---

# Code Health — Night Shift Commit Review

The "night shift colleague." Queries today's completion entries to identify surfaces that saw
recorded work, dispatches a Sonnet reviewer with `--problems-only`, applies findings inline,
defers complex findings to the debt backlog, updates the health ledger, writes a morning-ready
summary. Results wait at the next workstream-start.

**Announce at start:** "I'm using /code-health to review recent commits."

**Run on every committed day, regardless of commit count.** A small commit count is exactly when
a review gets skipped and is exactly where the adjacent-path regression hides — the cost-benefit
is asymmetric. The only valid skip: zero completion entries today AND zero fallback commits (see
Failure Modes).

## Step 1: Identify Surfaces

Invoke through the `.exe` launcher by absolute path via the PowerShell call operator (Shape W).
Ladder and shapes: `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`.

    `& "$env:COORDINATOR_SETTINGS_HOME\bin\query-completions.exe" --where "created=<YYYY-MM-DD>" --format json`

Extract file paths / subsystem names from `title`, `description`, `files`. No entries for today:
read `state/health-ledger.md`'s `Last daily check:` date, fall back to
`git log --since="<last-check-date>" --oneline --stat`, update the timestamp, report the fallback,
continue with the commit-based scope.

## Step 2: Diff Scope

`coordinator-invoke review.freeze_diff '{"range":"HEAD","worktree":true,"slice_id":"<id>","paths":[<Step 1 paths>]}'`
(a directory prefix if Step 1 yielded a subsystem name; `"range":"<last-check-commit>..HEAD"`, no `worktree`, on the fallback path). Summarize
which files/systems changed — this drives the reviewer's vocabulary/emphasis in Step 3, not
reviewer selection.

## Step 3: Dispatch the Reviewer

> **Do not ask whether to dispatch** — invoking this skill IS the request for the dispatch this
> step names; it dissolves no gate this skill's own body names.

Always the Sonnet `coordinator:code-reviewer`, never a persona — personas are Opus-only, reserved
for the weekly arch pass and explicit architectural decisions; a finding that genuinely needs one
gets flagged for `/workweek-complete` Step 7.5, not escalated here. Tell it what to weight by
dominant change type (UE idioms / component-token-reuse-accessibility / numeric-correctness /
coupling-and-interface-seams) — vocabulary only, never identity.

First register the reviewed file list: `review-findings-ledger targets --add` for Step 1's
surfaces. Then dispatch unattended: `coordinator:code-reviewer`, UNNAMED, `run_in_background:
true`, `--problems-only`. Its sidecar is spawn-provisioned (arrives as `sidecar_path:` in its
brief) — no EM pre-scaffold. Read the returned `DONE: <sidecar-path> | verdict: <OK|WARN|BLOCKED> |
findings: <N>` and pass the path to Step 4.

## Step 4: Reviewer Applies Findings

The reviewer applies and verifies its ledger — inline fixes and annotations against its own
sidecar, `review-findings-ledger verify` passing before it reports done. Findings needing 3+
interacting files or new abstractions go to Step 5 instead. No findings: skip to Step 6.

## Step 4.5: Commenting Lint Sweep

Non-blocking. Run alongside the reviewer dispatch, never as a gate: `& "$env:COORDINATOR_SETTINGS_HOME\bin\coordinator-invoke.exe" ci.run_commenting_sweep '{"repo_root":"<repo-root>"}'`.
Passing no `paths` (this call) scopes the sweep to files changed against the default branch plus
untracked files — the right size for a nightly pass, never the whole tracked tree. Its `findings`
(a changelog, attribution, task-ref, narration or grep-bait comment shape) file to the debt
backlog the same way Step 5 files a reviewer finding, `source: daily-health/commenting-sweep/{date}`.
No findings: skip. This is reporting only — no hook, no gate, no pre-commit leg.

**Audit-cadence (whole-repo) form**, for `/architecture-audit` or a periodic full sweep only —
never the nightly default above: `... ci.run_commenting_sweep '{"repo_root":"<repo-root>","paths":[<every tracked path from "git ls-files">]}'`.
Passing an explicit `paths` list is what scans the whole tree; this is a heavier, occasional pass,
not the per-run default.

## Step 5: Debt Backlog

    `& "$env:COORDINATOR_SETTINGS_HOME\bin\coordinator-queue-append.exe" --schema debt-backlog`

One YAML file per finding under `state/debt-backlog/`. Required: `title`, `body` (block scalar:
observation, structural gap, context), `source: daily-health/code-reviewer/{date}`, `risk`,
`proposed_action`, `status: open`, `created`. Stage each: `git add state/debt-backlog/<date>-<slug>.yaml`.

## Step 6: Health Ledger

Create `state/health-ledger.md` from template if absent (header `Last daily check:`/`Last full
audit:`/`Next rotation target:`, then a `## System Index` table: System | Grade | Status | Last
Audited | Open P0/P1/P2 | Lines | Notes). Update `Last daily check` to today. If findings changed
a grade, update that row; a system touched but rowless gets grade `?`.

The health ledger is the single source of truth for grades — `/architecture-audit` also writes
here after weekly audits. Read the existing grade before changing it; don't downgrade a
just-upgraded system absent new P0/P1s.

<!-- engine-gap: field=health_ledger.grade_from_findings producer=unknown memo=engine-gap-markers-name-a-memo-that-was-never-filed.md -->
Grading anchors, status-trigger definitions, and the reviewer-emphasis-by-change-type mapping
this step and Step 3 apply by eye have no engine producer yet — apply the calibration in the
wiki page for this skill until one lands.

## Step 7: Health Summary

    `& "$env:COORDINATOR_SETTINGS_HOME\bin\coordinator-doc-new.exe" --type health-status --title "Health Summary"`

Via Edit, fill `health:` (`HEALTHY|WATCH|ACTION|CRITICAL`), `summary:` (one-line), and body
sections `## Systems Graded`, `## Findings Summary`, `## Action Items for Next Session`. Worked
example: wiki.

## Step 8: Commit

Commit per `snippets/scoped-commit-route.md`, subject `daily-code-health: review of surfaces from
completion entries [date]`, pathspec exactly `state/health-ledger.md` and
`state/health/<YYYY-MM-DD>-health-summary.md`.

Nothing else this run touched. Post-commit hook pushes automatically.

## Failure Modes

| Situation | Action |
|---|---|
| No health ledger on first run | Create from template, use last 24h as scope |
| No completion entries for today | Fall back to `git log --since=<last-check>` scope; report fallback |
| `query-completions` not found | Fall back to git-log scope; note missing binary |
| No new commits since last check (fallback path) | Update timestamp, report, exit — no dispatch |
| Reviewer returns no findings | Skip Steps 4-5, go to Step 6 |
| Debt backlog doesn't exist | Create from template first |
| Complex finding can't be fixed inline | Debt backlog, with severity and effort estimate |
| Git commands fail (no commits, detached HEAD) | Report the error and stop |

## Cost

1 Sonnet `code-reviewer` dispatch (`--problems-only`), applying its own findings inline. No
persona, no Opus at this cadence.

## Relationship to Other Commands

`/workday-complete` is the primary trigger — let it invoke this rather than running standalone.
`/workstream-start`'s cockpit snapshot and record queries surface `state/health/*.md` at the top
of the next session (nested path, not the stale flat `state/health-summary.md`). `/review-code`'s
full feature-review workflow is a different tool — this dispatches `--problems-only` directly.
`pipelines/daily-code-health/PIPELINE.md` is the pipeline definition this command executes.
