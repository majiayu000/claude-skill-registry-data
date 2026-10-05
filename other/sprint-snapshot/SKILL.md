---
name: sprint-snapshot
category: scrum-sprint
description: >
  Capture a point-in-time snapshot of a scrum team's sprint board into the Obsidian vault.
  Use when the user says "sprint snapshot", "snapshot the sprint", "capture sprint state",
  "sprint planner", "scrum board snapshot", or invokes /sprint-snapshot.
codex-short-description: "Point-in-time snapshot of a scrum team's sprint board into the vault"
related-skills:
  - sprint-plan
  - sprint-review
  - daily-standup-prep
loop-eligible: true
recurrence-hint: weekly
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
  - AskUserQuestion
  - Skill
  - mcp__atlassian__jira_search
  - mcp__atlassian__jira_get_issue
compatibility: claude-code codex opencode
---
# Sprint Snapshot

Point-in-time snapshot of a scrum team's current sprint. Read-only across Jira. Writes three artifacts per run into the team's vault folder so progress can be tracked over time, scrum-of-scrums and end-of-sprint reporting become low-friction, and trends can be forecast.

This skill is a Claude Code port of ``<scripts-repo>\Sprint-Planner.ps1`` + `<scripts-repo>\Get-Jira-Sprint-Planner.ps1` — same canvas layout, same output path convention, same JQL shape. See [REFERENCE.md](REFERENCE.md) for the canvas layout spec, JSONL schema, and matching algorithm. See [EXAMPLES.md](EXAMPLES.md) for invocation parity with the PS scripts.

## Quick start

```text
/sprint-snapshot                                  → Aurora, INC 28, current sprint, auto phase
/sprint-snapshot Borealis                             → single team override
/sprint-snapshot Aurora --sprint 2 --inc 28       → explicit sprint within increment
/sprint-snapshot Aurora --as-of 2026-04-08        → historical snapshot (Jira `updated <= ...`)
/sprint-snapshot Aurora --phase "week 1"          → override the auto-derived phase
```

## Parameters

| Param | Default | Maps to PS |
| :--- | :--- | :--- |
| `Team` | from memory or prompt | `-Team` |
| `Inc` | from sprint-config or prompt | `-Increment` |
| `Sprint` | from sprint-config or prompt | `-Sprint` (1-4) |
| `Phase` | auto-derived from today | `-Label` (`start`/`week 1`/`week 2`/`week 3`/`end`) |
| `AsOf` | none | `-AsOf` |
| `JQL` | auto-built (see Phase 2) | `-JQL` |

JIRA project key, vault root, GitLab base, default team, capacity, and velocity are all **resolved from memory and the per-sprint config note** — never accept them as raw args. See *Config resolution* below.

## Config resolution (run once at the start of every invocation)

| Placeholder | Source | Default / how to populate |
| :--- | :--- | :--- |
| `{{vault_root}}` | `reference_obsidian_vault.md` (`**Vault root:**` line) | `C:\Users\<user>\dev\<vault>\` |
| `{{jira_project}}` | `reference_jira_default_project.md` | `PROJ` |
| `{{default_team}}` | `reference_default_scrum_team.md` (create if missing) | Prompt once — recommend `Aurora` (matches PS script default), then persist |
| `{{rosters_dir}}` | derived | `{{vault_root}}\Scrum Teams\_rosters\` |
| `{{output_root}}` | derived | `{{vault_root}}\Scrum Teams\<Team>\Scrum 📅\INC <Inc>\Sprint <Sprint>\` |
| `{{sprint_config}}` | derived | `{{output_root}}\_sprint.md` (frontmatter holds capacity / start / end / last_velocity / avg_velocity) |
| Default labels for JQL | `reference_team_jira_labels.md` (per-team table) | First run prompts for each team's label set; persist as a table row. Aurora default = `aurora,dev_common,dev_feature,doc_feature` (PS script). |

If a memory file is missing or its value is `<unset>`, **prompt once via `AskUserQuestion`** with the PS-script default as the recommended option, then write the answer back so the next run skips the prompt. Same pattern as `daily-standup-prep`.

## Sprint config note (per-sprint frontmatter)

`{{sprint_config}}` is the durable source of truth for capacity/velocity per sprint. Schema:

```yaml
---
team: Aurora
increment: 28
sprint: 2
start_date: 2026-04-01
end_date: 2026-04-21
capacity: 80.8
last_sprint_velocity: 55
avg_velocity_last_3: 58
labels: [pyrite, dev_common, dev_feature, doc_feature]
---
# Sprint 2 — Aurora (INC 28)
Notes, links, retro pointers go below.
```

If the file doesn't exist when the skill runs, prompt for **start_date, end_date, capacity, last_sprint_velocity, avg_velocity_last_3** via a single `AskUserQuestion` (recommend the PS-script defaults: capacity 80.8, last_velocity 55, avg 0), then write it. Subsequent snapshots in the same sprint reuse it.

## Roster bootstrap (first-run only)

Same pattern as `daily-standup-prep`. Look for `{{rosters_dir}}\<Team>.csv`. If missing, offer to copy from `<scripts-repo>\bin\Teams\<Team>.csv` via `AskUserQuestion`. CSV format and identity-matching cascade are identical — see [daily-standup-prep/REFERENCE.md](../daily-standup-prep/REFERENCE.md#roster-csv-schema).

## Workflow

```text
- [ ] Phase 1: Resolve config, load roster, load/create sprint config
- [ ] Phase 2: Auto-derive phase + build effective JQL (with optional AsOf)
- [ ] Phase 3: Fetch Jira issues + per-issue details
- [ ] Phase 4: Match assignees to roster + bucket by status
- [ ] Phase 5: Render canvas (delegate to obsidian-canvas)
- [ ] Phase 6: Render companion markdown summary
- [ ] Phase 7: Append snapshot row to _snapshots.jsonl (trend log)
- [ ] Phase 8: Console summary
```

### Phase 1 — Config + roster + sprint config

Resolve every `{{placeholder}}` per the table above. Load the roster CSV using the cascade in [daily-standup-prep/REFERENCE.md](../daily-standup-prep/REFERENCE.md#identity-matching-cascade). Read or create `{{sprint_config}}` and parse its frontmatter into `{Team, Inc, Sprint, StartDate, EndDate, Capacity, LastSprintVelocity, AvgVelocityLast3, Labels[]}`.

### Phase 2 — Phase derivation + JQL

**Auto-derive `Phase`** (unless user overrode):

| Days since `StartDate` (Pittsburgh local) | Phase |
| :--- | :--- |
| ≤ 0 | `start` |
| 1–7 | `week 1` |
| 8–14 | `week 2` |
| 15–20 | `week 3` |
| ≥ days_until_end (within last 2 days, or after) | `end` |

State the chosen phase in one short sentence: *"Snapshotting Aurora Sprint 2 (INC 28) — phase: week 1 (day 5 of 21)."*

**Build effective JQL** (port of `<scripts-repo>\Get-Jira-Sprint-Planner.ps1` lines 24, 554-570):

```text
project = {{jira_project}}
  AND labels in ({comma-joined Labels[] from sprint config})
  AND Sprint in openSprints()
  AND Sprint not in futureSprints()
```

If `--as-of <date>` was supplied, append `AND updated <= "{YYYY-MM-DD}"` and parse via standard date handling. Echo the final JQL one line before issuing the search so the user can confirm.

### Phase 3 — Fetch Jira issues

Single call:

```
jira_search(
  jql=<effective JQL>,
  fields="summary,description,status,assignee,priority,issuetype,labels,customfield_10106",
  max_results=200
)
```

`customfield_10106` is **Story Points** (matches the PS script). Don't refetch per-issue unless the search response is truncated. Cap at 200 — warn if hit.

### Phase 4 — Match + bucket

For each issue:

1. Parse story points: treat as `double`; missing → `0`. Track total + per-status running totals.
2. If `assignee` present, run the identity cascade against the roster. Match → `team_member`. No match → `off_team_member` (still tracked, separate group on canvas).
3. Bucket the issue by status:
   - `In Progress` → IN PROGRESS column
   - `In Review` → IN REVIEW column
   - `Done` / `Won't Fix` / `Duplicate` → DONE column
   - everything else → TO DO (split into Assigned vs Unassigned sub-columns based on whether `assignee` is set)
4. Increment per-member workload `(TicketCount, StoryPoints)` for matched team and off-team members.

Compute summary stats: `totalTickets`, `totalStoryPoints`, per-status counts and points, `unassignedTickets/Points`, `ticketsWithPoints`, `ticketsWithoutPoints`, `percentDone` (tickets), `percentPointsDone`.

### Phase 5 — Render the canvas

**Delegate to `obsidian-canvas` via `Skill`** for actual JSON authoring, ID generation, and validation — do not hand-author canvas JSON inline. The canvas layout (groups, node positions, sizes, colors, edges) is fully specified in [REFERENCE.md](REFERENCE.md#canvas-layout). Pass the rendered structure to `obsidian-canvas`.

Issue card content uses the `JIRA:KEY` convention so each card auto-links to the live ticket via the user's Obsidian Jira plugin:

```markdown
## [PROJ-1234] Summary line truncated to ~80 chars

JIRA:PROJ-1234

**Assignee:** Alex Rivera
**Points:** 3
**Type:** Story
```

The `JIRA:KEY` line goes on its own line — the plugin auto-renders. Do **not** wrap it in a wikilink. Team-member cards use the wikilink form `[[@First Last]]` (verify the vault note exists via `Glob("{{vault_root}}/🤼 Team/**/@*.md")`; if missing, fall back to bold plain text — same rule as `daily-standup-prep`).

Output path: `{{output_root}}\<phase>.canvas` — e.g. `…\Sprint 2\week 1.canvas`. Phase label is preserved literally including the space.

**Never overwrite silently.** If `<phase>.canvas` exists, prompt: `Overwrite` / `Save with timestamp suffix (week 1 (HH-MM).canvas)` / `Skip canvas`. Same pattern as `daily-standup-prep`.

### Phase 6 — Companion markdown summary

Write `{{output_root}}\<phase>.md` next to the canvas. Schema is the Sprint Summary table from the PS script (lines 973-996) plus a small header. **Delegate to `obsidian-markdown`** if extending with callouts, dataview, or new constructs. Template:

The companion markdown summary: [SUMMARY_TEMPLATE.md](SUMMARY_TEMPLATE.md) — fill every placeholder, keep section order and frontmatter keys.

Same overwrite-prompt rule as Phase 5.

### Phase 7 — Append to trend log

Append a single JSON line to `{{output_root}}\_snapshots.jsonl`. Create the file if missing — never overwrite. Schema is in [REFERENCE.md](REFERENCE.md#snapshots-jsonl-schema). Minimum fields:

```json
{"snapshot_at":"2026-04-08T09:14:00-04:00","as_of":null,"phase":"week 1","team":"Aurora","inc":28,"sprint":2,"capacity":80.8,"committed":62.5,"remaining":18.3,"totals":{"tickets":24,"points":62.5},"by_status":{"todo":{"tickets":8,"points":21},"in_progress":{"tickets":6,"points":15.5},"in_review":{"tickets":4,"points":11},"done":{"tickets":6,"points":15}},"unassigned":{"tickets":3,"points":8},"velocity":{"last":55,"avg3":58}}
```

This append-only log is what enables forecasting and trend analysis without parsing canvas files. Keep one row per snapshot — never rewrite history.

### Phase 8 — Console summary

Print a brief block (matches the PS `Write-Verbose` summary, lines 893-903):

```
=== Aurora Sprint 2 (INC 28) snapshot — phase: week 1 ===
JQL:        project = PROJ AND labels in (pyrite,dev_common,...) AND Sprint in openSprints()...
Issues:     24 total / 6 done (25%) / 4 in review / 6 in progress / 8 to do
Points:     62.5 total / 15 done / 11 in review / 15.5 in progress / 21 to do
Unassigned: 3 tickets (8 pts)
Capacity:   80.8 (committed 62.5, remaining 18.3)
Saved:      [week 1.canvas](Scrum Teams/Aurora/Scrum 📅/INC 28/Sprint 2/week 1.canvas)
            [week 1.md](Scrum Teams/Aurora/Scrum 📅/INC 28/Sprint 2/week 1.md)
            [_snapshots.jsonl] (+1 row, 4 total)
```

## Rules

- **Read-only across Jira.** Never transition issues, post comments, change assignees, or touch the API beyond `jira_search` / `jira_get_issue`.
- **Append-only on `_snapshots.jsonl`.** Never rewrite or compact. The whole point is point-in-time history.
- **Never overwrite an existing canvas or markdown summary silently.** Always confirm via `AskUserQuestion`.
- **Confirm before persisting to memory or to the sprint config note.** When populating a missing value, use the PS-script default as the recommended option but let the user override before writing.
- **Phase label is preserved literally** including the space (`week 1`, not `week-1`) — the PS script's filenames are the canonical convention and other tools may consume them.
- **Pittsburgh local time** for snapshot timestamps and phase derivation. Jira `updated` cutoffs use ISO date (`YYYY-MM-DD`).
- **No fabricated data.** If Jira fails, surface the failure in the console summary and abort. Do not invent issues. (Unlike daily-standup-prep, partial outputs aren't useful here — a snapshot must reflect real Jira state.)
- **Wikilinks for team members only when the vault person note exists.** Use `Glob("{{vault_root}}/🤼 Team/**/@*.md")` to verify before writing `[[@First Last]]`. Fall back to bold plain text otherwise — never invent a wikilink.
- **`JIRA:KEY` for issue references.** This is the Obsidian Jira plugin's auto-link convention — do not wrap in a wikilink, do not add the URL inline.
- **Story Points = `customfield_10106`.** This is the PS-script's hardcoded ID and it matches the user's Jira instance. If the field is missing for an issue, treat as `0` and increment `ticketsWithoutPoints`.
- **Auto-derived phase is a suggestion.** Always echo the derived phase in Phase 2 output so the user can rerun with `--phase` if they disagree.

## Edge cases

- **Sprint config note missing or incomplete** — prompt once for the missing fields, write the file, continue. Don't run with synthetic capacity/velocity.
- **Roster CSV missing** — offer to copy from the upstream PowerShell scripts repo (same pattern as `daily-standup-prep`); if neither path exists, abort the team.
- **`labels in (...)` returns 0 issues** — render an "empty sprint" canvas (groups + columns, no issue cards), still write the markdown summary and JSONL row. Surface the empty result clearly so the user can fix the label set.
- **`AsOf` date is in the future** — reject with an `AskUserQuestion`: did you mean today, or a different date? Don't silently fall through to "current".
- **Issue without an assignee** — goes in TO DO (Unassigned) column; counted in `unassignedTickets/Points`.
- **Assignee not on roster** — goes in the off-team group on the right of the canvas; tracked separately in `offTeamMembersWorkload`. Don't pollute the team workload total with off-team points.
- **Vault `🤼 Team` folder missing the person note** — render bold plain text instead of a broken wikilink. Same rule as `daily-standup-prep`.
- **Re-run on the same phase** — overwrite/timestamp/skip prompt for `.canvas` and `.md`. The JSONL row is always appended (it's the point-in-time history).
- **`customfield_10106` field name differs in the user's Jira** — the field ID is the user's confirmed Story Points field per the PS script. If a future Jira config change breaks it, the skill will count everything as 0 points and surface the anomaly in the console summary; the fix is to update the field ID in `reference_jira_default_project.md` (add a `**Story Points field:**` line).
- **Pre-sprint snapshot (`AsOf` = sprint start)** — the PS script's intended use case for `start` phase. JQL filter still works because the issues already have the sprint label by then.

## Related skills

This skill writes into the user's Obsidian vault and reads from Jira. Delegate to the relevant sibling skills via `Skill` rather than reimplementing.

| Skill | Use it for |
| :--- | :--- |
| `obsidian-canvas` | **Canonical canvas authoring.** Phase 5 delegates to it for ID generation, JSON shape, and validation. Do not hand-write canvas JSON. |
| `obsidian-markdown` | Use when extending the companion `.md` template with callouts, dataview, embeds, or block IDs beyond the base summary table. |
| `obsidian-vault` | Use for batch wikilink target verification (e.g. validating every roster member has a vault person note). Prefer over repeated `Glob` calls when checking >15 names. |
| `obsidian-cli` | Use for property/task queries against the snapshot — e.g. "show me all snapshots for Aurora where committed > capacity". |
| `obsidian-bases` | Use when the user wants a dashboard `.base` file aggregating snapshots across sprints (e.g. "velocity trend per team", "carry-over rate per increment"). Do not hand-author `.base` YAML. |
| `daily-standup-prep` | **Pattern parent.** Same memory-driven config, same roster CSV format, same identity matcher, same vault-write conventions. Reuse [its REFERENCE.md](../daily-standup-prep/REFERENCE.md) for roster + identity cascade. |
| `issue-feature-breakdown` | Pattern reference for Jira context-gathering depth and read-only discipline. |
| `issue-suggest-component` | Pattern reference for memory-driven default Jira project + bulk pacing if the snapshot ever expands to multi-team. |
| `clarity-council` | Future extension: stand up a "sprint health council" persona session that reviews the latest JSONL trend log and flags risks. Out of scope for v1. When that lands, the council pull-list is **`statistics-expert + scrum-master + infographics-expert`** — statistics-expert reads the trend with uncertainty rendering, infographics-expert chooses the chart format (sparklines per metric? small-multiple per team?) and produces the SVG/Mermaid output that embeds back into the canvas or companion markdown. |

## Quality Loop

Before returning, check the output against these criteria. If two or more fail, revise and re-check — at most two passes, then note what still falls short.

- Canvas, companion markdown, and JSONL trend log are all written
- Sprint phase was auto-detected (or honored --as-of) correctly
- Every board issue is represented as a card with its status column
- Team workload totals reconcile with the per-member card sums

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/sprint-snapshot.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
