---
name: context-grooming
description: >
  Review and prune the project context — archive completed work,
  summarize stale entries, and propose disabling unused skills.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-context-grooming
    version: "1.0.0"
    created: 2026-04-07T00:00:00Z
    category: processkit
    layer: 4
    uses:
      - skill: event-log
        purpose: Log events to keep the audit trail accurate after every write.
      - skill: index-management
        purpose: Query existing entities and keep the SQLite index fresh after writes.
    provides:
      primitives: []
      templates: [grooming-report]
    commands:
      - name: pk-groom
        args: ""
        description: "Run a context grooming pass to prune and compact project context"
---

# Context Grooming

## Intro

`context-grooming` is the periodic-cleanup skill. Once a week or once a
month, the agent walks the project's `context/` directory against a set
of rules and produces a report listing what could be archived, summarized,
or disabled. The user approves each item before any file moves. This is
how the project keeps its session context lean over time.

## Overview

### When to run

Triggered by:
- An explicit user request: "groom the context", "let's clean up"
- A cadence configured in `processkit.toml`:
  ```toml
  [context.grooming]
  cadence = "weekly"     # weekly | monthly | quarterly | never
  ```
  The agent checks the cadence at session start. If the last grooming was
  more than the cadence ago, it surfaces:
  > "Context grooming was last run 5 weeks ago. Want me to do a pass?"
- A noticeable session-context bloat: more than ~16k tokens loaded at
  session start (if the agent can detect this — depends on the runtime).

### What grooming does

Grooming is a **review-then-act** workflow:

1. **Walk** — agent walks `context/` against the ruleset (see Level 3).
2. **Report** — agent produces a `grooming-report.md` document listing
   proposed actions, organized by category.
3. **Review** — user reads the report and approves items individually
   (or in groups).
4. **Act** — agent moves/archives/disables only the approved items.
5. **Record** — appends a `LogEntry` (`event_type: context.groomed`) and
   updates the report's status field.

**Nothing is moved silently. Nothing is deleted, ever** — the worst that
can happen is "moved to `context/archive/`" which is reversible.

This skill also provides the `/pk-groom` command for direct invocation —
see `commands/pk-groom.md`.

### The grooming report

The report lives at `context/grooming-reports/<date>.md`. Sample shape:

```markdown
---
apiVersion: processkit.projectious.work/v2
kind: Context
metadata:
  id: GROOM-2026-04-07
  privacy: project-private
spec:
  state: pending  # pending | approved | applied
  generated: 2026-04-07T10:00:00Z
---

# Grooming report — 2026-04-07

## Workitems eligible for archive (12)

| ID | Title | State | Last touched |
|---|---|---|---|
| BACK-foo | ... | done | 2026-02-01 |
| ... | ... | ... | ... |

[ ] Approve all
[ ] Approve individually: ...

## Standups eligible for summarization (8)

8 standup entries from Q1 2026 can be summarized into a single quarterly
summary:
- 2026-01-05.md → 2026-03-30.md

[ ] Approve summarization

## Unused skills (3)

These skills have not been invoked in any session for 60+ days:
- `pixijs-gamedev` (last used: 2026-01-12)
- `flutter-development` (last used: never since project init)
- `latex-authoring` (last used: 2026-02-08)

[ ] Approve disabling (move from context/skills/ to context/skills/.disabled/)
```

### The default ruleset

| Rule | Action proposed |
|---|---|
| WorkItem in terminal state (`done` / `cancelled`) for >30 days | Move to `context/archive/workitems/` |
| LogEntry older than 90 days, not referenced by any current entity | Move to `context/archive/logs/` |
| Standup entry older than current quarter | Summarize all entries from a quarter into one quarterly summary; archive originals |
| DecisionRecord superseded for >180 days | Move both the old and the new together to `context/archive/decisions/` |
| File over 500 lines that hasn't been edited in 30 days | Propose splitting or summarizing |
| Skill in `context/skills/` not invoked in any session for 60 days | Propose disabling (move to `context/skills/.disabled/`) |
| Migration in `applied/` older than 1 year | Archive (rare — kept for historical reference) |

These are defaults. Projects can override in `processkit.toml`:

```toml
[context.grooming.rules]
workitem_archive_age_days = 60       # default 30
log_archive_age_days = 180           # default 90
unused_skill_age_days = 90           # default 60
disable_skills_automatically = false # default false (always proposes, never auto-disables)
```

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Moving or deleting files without user approval.** Grooming is a propose-then-act workflow: generate the report, surface it to the user, act only on approved items. Silently moving files based on the ruleset — even files that clearly qualify — bypasses the user's judgment. Nothing moves without approval.
- **Proposing to disable a skill that is currently being used.** The "not invoked in 60 days" rule may fire on a skill that was used extensively until recently, or that is central to a project the user is about to resume. Before proposing to disable a skill, check recent session notes and the backlog for references to that skill.
- **Grooming the current quarter's standups or in-progress work.** The ruleset explicitly skips anything in-progress or less than 30 days old. Proposing to archive a standup from last week, or a workitem currently being worked on, produces a report that damages trust in the grooming process. Always apply the age and status filters strictly.
- **Summarizing standups without preserving specific work item references.** A quarterly summary that replaces eight individual standup entries must retain all workitem IDs, decision references, and blocker resolutions mentioned in the originals. A summary that says "worked on various items" loses the audit trail. Summarizations are compressions, not erasures.
- **Running grooming too frequently, making every report feel like noise.** If the user is asked to approve a grooming report every session, they will start ignoring or dismissing them reflexively. Respect the configured cadence. If the user has declined grooming three sessions in a row, offer to change the cadence rather than repeating the offer.
- **Treating the default ruleset as mandatory even when the project has overrides.** The `processkit.toml` configuration can change thresholds — a project may archive workitems after 60 days instead of 30, or may never disable skills. Always read the configuration before applying any rule, and apply the project-specific values.
- **Not recording the grooming event in the event log.** Every grooming session that results in file moves must be recorded as a `LogEntry` with `event_type: context.groomed`, listing which items were moved and when. Without this, the next grooming pass cannot determine when the last grooming ran.

## Full reference

### Configuration

```toml
[context.grooming]
cadence = "monthly"           # weekly | monthly | quarterly | never (default: never)
report_dir = "context/grooming-reports"   # default

[context.grooming.rules]
# Override individual rules. All have safe defaults.
workitem_archive_age_days = 30
logentry_archive_age_days = 90
standup_archive_age_days = 90
decision_archive_age_days = 180
oversize_file_threshold_lines = 500
unused_skill_age_days = 60
```

### Archiving entities vs. archiving files

In the entity-sharded world, "archiving" an entity means **transitioning
it to a terminal state** in its state machine — `done`, `cancelled`, or
`archived` depending on the kind. This is the primary archive operation:

- WorkItem → `done` or `cancelled`
- DecisionRecord → `superseded` or `archived`
- Note → `archived` or `promoted`

Once in a terminal state, the entity is filtered out of active queries
by the MCP server (`query_entities(state=active)` returns nothing in
terminal states). The file stays in place — no move needed for functional
purposes.

**Physical compaction** (moving terminal-state files to
`context/<kind>/archive/`) is an optional aesthetic operation that
context-grooming can propose when directories grow unwieldy for human
browsing. The threshold is configured via `oversize_file_threshold_lines`
or a simple entity count. Propose compaction — never act without approval.

### What grooming will NOT touch

To stay safe and predictable, grooming explicitly skips:

- Anything in `context/owner/` (the personal context portfolio)
- Anything in any `private/` directory (user-private content)
- The current quarter's standups (only previous quarters get summarized)
- Currently in-progress work (Migration in `in-progress/`, WorkItem in
  `in-progress` state, etc.)
- Files less than 30 days old (regardless of size)
- The `context/migrations/` directory (migrations have their own lifecycle)

### When to override the cadence

Some projects benefit from rare grooming (long-running R&D where
historical context matters); some benefit from frequent grooming (fast-
moving sprints). The cadence config is per-project.

If the user repeatedly says "skip grooming" three sessions in a row, the
agent should propose:
> "You've skipped grooming three times. Do you want me to switch the
> cadence to a longer interval (or `never`)?"

### Relationship to context budget (in `agent-management`)

Grooming reduces the LIVE size of the context. The `[context.budget]`
section in `processkit.toml` (documented in `agent-management/SKILL.md`) tells
the agent how much context to load per session. The two work together:
grooming makes the corpus smaller; budget tells the agent how to load
selectively.

### Ideas for future versions

- **Ranking**: instead of binary "archive or not", rank files by
  "loading-cost vs information-value" and propose the bottom 10%.
- **Compaction**: instead of archive, the agent could rewrite a 500-line
  workitem-with-history into a 20-line summary + a link to the archived
  full version.
- **Auto-grooming for reversible moves only**: a low-risk subset of the
  rules could be applied automatically (still logged for review). v1
  ships with always-propose, never-auto.
