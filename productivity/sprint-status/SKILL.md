---
name: sprint-status
description: "Fast sprint status check. Reads the current sprint plan, scans story files for status, and produces a concise progress snapshot with burndown assessment and emerging risks. Run at any time during a sprint for quick situational awareness. Use when user asks 'how is the sprint going', 'sprint update', 'show sprint progress'."
argument-hint: "[sprint-number or blank for current]"
user-invocable: true
allowed-tools: Read, Glob, Grep
model: haiku
---

## QA policy, facts and authority

Apply `standards/evidence-lifecycle.md`, `standards/notes-adr-sync.md` and existing
collaboration authority. Read actual `workflow/workflow-catalog.yaml`, domain,
current transition and established project QA scope, including initialized
`memory_bank/t1_axioms/qa_context.md` or the existing owning Story/plan/decision.
QA orchestration is optional by default; strict obligations need explicit source,
authority and exact checks/scope. Review mode does not select strict QA. Absent
optional Memory Bank/QA Context with no actual strict selection uses the catalog's
default optional orchestration; disclose absence without requiring initialization.
Unknown applies to unresolved actual required applicability or conflicting policy,
not optional context absence. Resolve that affected scope before dependent claims;
Honor actual user-specified per-effect approval conditions when determining coverage;
do not invent strict obligations or passing results.
Optional orchestration never waives required Story AC, governing DoD, decisions,
evidence or required review. Type tables are starting points; actual owners decide
requirements. Each required check retains PASS/FAIL/NotRun/Blocked/Pending; N/A
needs a governing applicability reason and cannot erase a failure.

Separate sufficiency, actual execution, independence, acceptance and completion.
Files/keywords/counts, planning cases and self-checks prove none of the other facts.
Read relied-on bodies and minimum required direct/indirect dependency closure;
retain full SHA-256/byte sizes, recoverable originals and original-path witnesses.
Disclose reading omissions. Exact bound historical results may be reused only
where selected workflow permits, labeled historical with original runtime/observer,
inputs and scope; never call them this run's execution. Missing required originals
or observations leave affected checks incomplete. Risk acceptance is a separate
scoped record; it cannot change FAIL/NotRun/Blocked/Pending to PASS or completion.

Reuse named paths/effects authority across roles/retries; before new authority show
draft and complete effect set, asking only for material new scope. Review-only
invokes no write entrypoint. Report-only writes its new report, excluding inputs,
indexes, session/sprint/stage state and closure. Existing report paths require a
new revision with prior evidence preserved; index effects need their own covered
scope and historical links. Optional Memory Bank absence uses Story/report/
conversation fallback without initialization, publication or activation.

## User Guide

- When to use: Fast sprint status check. Reads the current sprint plan, scans story files for status, and produces a concise progress snapshot with burndown assessment and emerging risks. Run at any time during a sprint for quick situational awareness. Use when user asks 'how is the sprint going', 'sprint update', 'show sprint progress'.
- Inputs: Command arguments: `/sprint-status [sprint-number or blank for current]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None (read-only).
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Routing

Detect the project domain before reporting status:
- `design/cdd/game-concept.md` -> **[Game]** report progress in terms of game systems, player-facing stories, playtest blockers, content/assets, engine risks, and release gates.
- `design/cdd/product-concept.md` -> **[Product]** report progress in terms of product modules, user-facing workflows, API/CLI/UI stories, test evidence, deployment risk, and operational readiness.
- If unclear, keep status domain-neutral and label domain-specific fields as unknown.

Game status fields remain valid. Product status fields are added where applicable.
# Sprint Status

This is a fast situational awareness check, not a sprint review. It reads the
current sprint plan and story files, scans for status markers, and produces a
concise snapshot in under 30 lines. For detailed sprint management, use
`/sprint-plan update` or `/milestone-review`.

**This skill is read-only.** It never proposes changes, never asks to write
files, and makes at most one concrete recommendation.

---

## 1. Find the Sprint

**Argument:** `$ARGUMENTS[0]` (blank = use current sprint)

- If an argument is given (e.g., `/sprint-status 3`), search
  `production/sprints/` for a file matching `sprint-03.md`, `sprint-3.md`,
  or similar. Report which file was found.
- If no argument is given, find the most recently modified file in
  `production/sprints/` and treat it as the current sprint.
- If `production/sprints/` does not exist or is empty, report: "No sprint
  files found. Start a sprint with `/sprint-plan new`." Then stop.

Read the sprint file in full. Extract:
- Sprint number and goal
- Start date and end date
- All story or task entries with their priority (Must Have / Should Have /
  Nice to Have), owner, and estimate

---

## 2. Calculate Days Remaining

Using today's date and the sprint end date from the sprint file, calculate:
- Total sprint days (end minus start)
- Days elapsed
- Days remaining
- Percentage of time consumed

If the sprint file does not include explicit dates, note "Sprint dates not
found — burndown assessment skipped."

---

## 3. Scan Story Status

**First: check for `production/sprint-status.yaml`.**

If it exists, read it as machine-readable status projection and use its declared
sprint/goal/dates. For every claimed done row read the linked exact Story closure,
required review/evidence and input binding under `/story-done`. Mutable YAML rows
are not independent completion proof. Conflicting/missing/incomplete required
closure is Unverified/Blocked and excluded from verified done count.

If absent, read actual Story status/header and closure section, or owning inline
task record. Arbitrary body words, quotes/examples/recommendations are not status.
Legacy Complete/Done/RISKS labels remain claimed until required closure is verified.
RISKS maps to COMPLETE WITH NOTES only with all required PASS/review/authority facts.
Missing paths are MISSING; ambiguous state Unknown, not automatically Not Started.

Keep this fast and read-only: unavailable complete evidence means Unverified with
missing dependency and a closure-owner recommendation, never certification/repair.
Implementation path names are hints only. Disclose the absent YAML projection.

### Stale Story Detection

After collecting status for all stories, check each IN PROGRESS story for staleness:

- For each story that has a referenced file, read the file and look for a
  `Last Updated:` field in the frontmatter or header (e.g., `Last Updated: 2026-04-01`
  or `updated: 2026-04-01`). Accept any reasonable date field name: `Last Updated`,
  `Updated`, `last-updated`, `updated_at`.
- Calculate days since that date using today's date.
- If the date is more than 2 days ago, flag **STALE metadata / date age** for attention; this does not establish absent progress, a hidden blocker or a risk verdict.
- If no date field is found, note "no timestamp — cannot check staleness." A date/mtime alone proves neither activity nor absence of intervening writes.
- If the story has no referenced file (inline task), note "inline task — cannot check staleness."

STALE stories are included in the output table and collected into an "Attention Needed"
section (see Phase 5 output format).

**Activity-based escalation**: an old timestamp alone adds a date-age attention
hint. Only actual relevant activity/dependency evidence establishing stalled work
or a blocker can support a no-progress/At Risk assessment; cite the actual scope,
observed interval and evidence source. With only date/mtime, activity is Unknown
and burndown follows other verified completion, deadline and blocker facts. Do
not assert "no progress in N days" or upgrade At Risk solely from an old date.

---

## 4. Burndown Assessment

Calculate:
- Verified complete tasks (eligible exact COMPLETE or COMPLETE WITH NOTES closure); display claimed/unverified totals separately
- Tasks in progress (IN PROGRESS)
- Tasks blocked (BLOCKED)
- Tasks not started (NOT STARTED or MISSING)
- Completion percentage: (complete / total) * 100

Assess burndown by comparing completion percentage to time consumed percentage:

- **On Track**: completion % is within 10 points of time consumed % or ahead
- **At Risk**: completion % is 10-25 points behind time consumed %
- **Behind**: completion % is more than 25 points behind time consumed %

If dates are unavailable, skip the burndown assessment and report "On Track /
At Risk / Behind: unknown — sprint dates not found."

---

## 5. Output

Keep the total output to 30 lines or fewer. Use this format:

```markdown
## Sprint [N] Status — [Today's Date]
**Sprint Goal**: [from sprint plan]
**Days Remaining**: [N] of [total] ([% time consumed])

### Progress: [complete/total] tasks ([%])

| Story / Task         | Priority   | Status      | Owner   | Blocker        |
|----------------------|------------|-------------|---------|----------------|
| [title]              | Must Have  | DONE        | [owner] |                |
| [title]              | Must Have  | IN PROGRESS | [owner] |                |
| [title]              | Must Have  | BLOCKED     | [owner] | [brief reason] |
| [title]              | Should Have| NOT STARTED | [owner] |                |

### Attention Needed
| Story / Task         | Status      | Last Updated   | Days Stale | Note           |
|----------------------|-------------|----------------|------------|----------------|
| [title]              | IN PROGRESS | [date or N/A]  | [N days]   | [STALE / no timestamp — cannot check staleness / inline task — cannot check staleness] |

*(Omit this section entirely if no IN PROGRESS stories are stale or have timestamp concerns.)*

### Burndown: [On Track / At Risk / Behind]
[1-2 sentences. If behind: which Must Haves are at risk. When on track: confirm
and note any Should Haves the team could pull.]

### Must-Haves at Risk
[List any Must Have stories that are BLOCKED or NOT STARTED with less than
40% of sprint time remaining. If none, write "None."]

### Emerging Risks
[Any risks visible from the story scan: missing files, cascading blockers,
stories with no owner. If none, write "None identified."]

### Domain Lens
[Game: mention playtest/content/asset/engine risks if present. Product: mention
API/CLI/UI/data workflow, contract, migration, docs/help, deployment, security,
or operational-readiness risks if present. If domain-neutral, write "No
domain-specific risks detected."]

### Recommendation
[One concrete action, or "Sprint is on track — no action needed."]
```

---

## 6. Fast Escalation Rules

Apply these rules before outputting, and place the flag at the TOP of the
output if triggered (above the status table):

**Critical flag** — if Must Have stories are BLOCKED or NOT STARTED and
less than 40% of the sprint time remains:

```
SPRINT AT RISK: [N] Must Have stories are not complete with [X]% of sprint
time remaining. Recommend replanning with `/sprint-plan update`.
```

**Completion flag** — only if every Must Have has an exact verified eligible closure:

```
All Must Have closure conditions verified; consider Should Have backlog. Sprint/stage transition still needs separate obligations and authority.
```

**Missing stories flag** — if any referenced story files do not exist:

```
NOTE: [N] story files referenced in the sprint plan are missing.
Run `/story-readiness sprint` to validate story file coverage.
```

**Product contract flag** — if Product stories mention API, CLI, schema,
migration, config, package, deployment, or docs work but no matching test or
evidence path is visible:

```
PRODUCT VALIDATION RISK: [N] Product story(ies) lack visible contract,
workflow, migration, docs, deployment, or operational evidence. Recommend
`/story-readiness [path]` or `/test-evidence-review` before closing.
```

**Product deployment flag** — if Product release, migration, config, package,
or deployment stories are BLOCKED/NOT STARTED late in the sprint:

```
PRODUCT RELEASE RISK: operational readiness work is behind. Check migration,
config, package, monitoring, rollback, and support handoff before continuing.
```

---

## Collaborative Protocol

This skill is read-only. It reports observed facts from files on disk.

- It does not update the sprint plan
- It does not change story status
- It does not write T3 memory-bank snapshots; `/story-done`, `/retrospective`,
  and `/milestone-review` maintain `memory_bank/t3_archive/sprint_snapshots/`
  when approved closure artifacts exist
- It does not propose scope cuts (that is `/sprint-plan update`)
- It makes at most one recommendation per run
- For Product projects, it reports visible API/CLI/UI/data/migration/docs/
  deployment evidence gaps but does not certify readiness; use
  `/test-evidence-review`, `/smoke-check`, `/team-qa`, or `/gate-check` for
  validation.

For more detail on a specific story, the user can read the story file directly
or run `/story-readiness [path]`.

For sprint replanning, use `/sprint-plan update`.
For end-of-sprint retrospective, use `/milestone-review`.
