---
name: sprint-review
category: scrum-sprint
description: >
  End-of-sprint stakeholder report comparing the sprint's start and end canvases, fitted to
  the standard Scrum Master template. Use when the user says "sprint review", "end of sprint
  report", "sprint stakeholder report", or invokes /sprint-review.
codex-short-description: "End-of-sprint stakeholder report comparing start and end sprint canvases"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
  - AskUserQuestion
  - Skill
related-skills:
  - sprint-snapshot
  - clarity-council
loop-eligible: true
recurrence-hint: on-demand

compatibility: claude-code codex opencode
---
# Sprint Review Report

End-of-sprint stakeholder report comparing **planning** (`start.canvas`) to **sprint close** (`end.canvas`). Read-only on Jira; uses the canvases captured by [sprint-snapshot](../sprint-snapshot/SKILL.md). Writes one report file into the sprint folder, formatted to drop into the SM's stakeholder template.

This skill is the Claude port of the user's "Sprint Review" prompt template. Pairs with [sprint-plan](../sprint-plan/SKILL.md) (start-of-sprint) and [sprint-sos-report](../sprint-sos-report/SKILL.md) (weekly).

## Quick start

```text
/sprint-review                                              → Aurora, current sprint, start vs end
/sprint-review Borealis                                         → single team
/sprint-review Aurora --inc 28 --sprint 2                   → explicit sprint
/sprint-review Aurora --commitment-threshold 0.85           → override default 0.85 commitment-met threshold
/sprint-review Aurora --no-council                          → skip clarity-council
```

## Parameters

| Param | Default | Notes |
| :--- | :--- | :--- |
| `Team` | from memory or prompt | Same source as sprint-snapshot |
| `Inc` | latest from `Scrum 📅/INC <N>/` | |
| `Sprint` | latest from `INC <N>/Sprint <N>/` | |
| `From` | `start` | Canvas filename to compare from |
| `To` | `end` | Canvas filename to compare to |
| `CommitmentThreshold` | `0.85` | Done velocity-relevant pts ÷ committed velocity-relevant pts ≥ threshold → "commitment met" |
| `Personas` | `statistics-expert,scrum-master,product-owner,knowledge-manager` | `--no-council` disables |
| `ScrumMaster` | from memory or prompt (recommended `Jane Doe`) | Goes in the report header. Persisted to `reference_default_scrum_master.md`. |
| `ConfluenceUserUrl` | from memory (recommended the user's own profile URL) | Used to wikilink the SM name in the header. |

## Workflow

```text
- [ ] Phase 1: Resolve config + load _sprint.md + _team-rules.md + SM identity
- [ ] Phase 2: Locate start.canvas + end.canvas + JSONL rows for both
- [ ] Phase 3: Diff (added / removed / status-changes / completed / not-completed / wedge delta)
- [ ] Phase 4: Apply team rules (overhead-adjusted velocity, in-review overhead, wedge balancing, commitment math)
- [ ] Phase 5: Run clarity-council (Sprint Accomplishments + Status + Impediments + PI Confidence) unless --no-council
- [ ] Phase 6: Render template-shaped report and write
- [ ] Phase 7: Console summary
```

### Phase 1 — Config

Same resolution as `sprint-plan`/`sprint-sos-report` Phase 1. Additionally:

- **`{{scrum_master_name}}`** — `reference_default_scrum_master.md` (`**Default Scrum Master:**` line). If missing, prompt with `Jane Doe` as the recommended option (matches the prompt template); persist.
- **`{{scrum_master_confluence_url}}`** — `reference_default_scrum_master.md` (`**Confluence profile URL:**` line). If missing, prompt; persist.

### Phase 2 — Locate canvases

1. Look for `{{output_root}}\{{from}}.canvas` and `{{output_root}}\{{to}}.canvas` (default `start.canvas` and `end.canvas`).
2. If `end.canvas` is missing, `AskUserQuestion`: `Run /sprint-snapshot --phase end now (recommended)` / `Use latest available phase as end (e.g. week 3)` / `Cancel`. Don't fabricate.
3. If `start.canvas` is missing, refuse — the report is meaningless without the planning baseline. Surface the path that's expected.
4. Read both canvases as JSON; parse issue cards as `sprint-plan` Phase 3.
5. Read `_snapshots.jsonl` and grab the rows where `phase == "start"` and `phase == "end"` (or the `from`/`to` overrides).

### Phase 3 — Diff

Same five sets as `sprint-sos-report` Phase 3 (`added`, `removed`, `moved_status`, `changed_points`, `assignee_changed`), plus two end-of-sprint specifics:

- **`completed`** — tickets present in both `start` and `end` whose `end.status ∈ {Done, Won't Fix, Duplicate}`. Sub-split by velocity-relevant vs in-review-overhead.
- **`not_completed`** — tickets present in both whose `end.status ∉ {Done, Won't Fix, Duplicate}`. These become carry-over candidates and feed the Impediments section.

Per-status point flow at the **sprint** boundary (not per-week):

```text
done.points (end)         - done.points (start)         = sprint velocity (raw)
                                                       — subtract in-review overhead → velocity-relevant
not_completed.points                                   = carry-over candidate volume
```

### Phase 4 — Apply team rules

- **Velocity-relevant velocity** — `done.points (end) − sum(in_review_overhead matched in done at end)`. This is the number reported as the team's actual sprint velocity.
- **Sprint commitment math** — let `committed_vr = committed.points (start) − in_review_overhead.points (start)` and `delivered_vr = velocity-relevant velocity`. Commitment met iff `delivered_vr / committed_vr ≥ CommitmentThreshold`. Surface both ratios (raw and velocity-relevant) when they differ.
- **Wedge final accounting** — total wedge consumed during the sprint = `wedge.points (start) − wedge.points (end)`. Total scope added = `sum(added.points)`. Verdict: balanced iff `added ≤ wedge`; else scope creep with delta.
- **Carry-over identification** — `not_completed` tickets become the carry-over list. Surface count, points, and per-member breakdown.
- **In-review overhead at end** — these are *expected* to close on sprint end date. If any are still in IN REVIEW at end-of-sprint snapshot, flag as a notable deviation (the team rule says they should close, so this is signal).

### Phase 5 — Clarity-council

Unless `--no-council`, invoke `clarity-council` via `Skill` with the personas list. Pass:

- The Phase 3 diff sets (full lists with `JIRA:KEY`)
- The Phase 4 derived numbers (velocity-relevant velocity, commitment ratio, wedge verdict, carry-over)
- Both `_snapshots.jsonl` rows (`start`, `end`)
- The trailing `_snapshots.jsonl` window (last 5 sprints' `end` rows for trend context — feeds the PI Confidence section)
- Their assignment: *"Produce four short markdown sections matching this contract:*

  1. **`### Summary of Sprint Accomplishments`** — 5-9 bullets. Each names a delivered ticket via `JIRA:KEY`, the user-visible outcome, and the owning member as `[[@First Last]]`. Group by theme if 2+ tickets share one. The product-owner leads here.
  2. **`### Status`** — table or short paragraph. Includes commitment-met verdict (with both raw and velocity-relevant ratios), velocity-this-sprint vs avg, wedge verdict, and carry-over volume. The statistics-expert leads with prediction intervals where relevant.
  3. **`### Did team meet their Sprint Commitment?`** — explicit yes/no based on the threshold + a one-paragraph why.
  4. **`### Confidence level in team meeting their PI Commitment`** — `High / Medium / Low` + a one-paragraph why grounded in the trailing-5-sprint window. The statistics-expert provides the calibration; the scrum-master frames the team-dynamics context.
  5. **`### Impediments`** — list. Each entry: severity (High/Med/Low), one-sentence description, the ticket(s) blocked (`JIRA:KEY`), and a proposed next step. Include carry-over root causes here, not just the carry-over list.
  6. **`### Retro learnings (durable)`** — 2-4 bullets owned by the **knowledge-manager**. Each captures a learning from this sprint that should outlive the report: a pattern worth repeating, a failure mode the team now recognises, a runbook/ADR/CONTEXT entry that should be created or updated. Each bullet names the artifact that should change (`[[path]]` or "new ADR-NNNN: …") and the persona's confidence that the learning generalises beyond this sprint (High/Med/Low). The knowledge-manager's purpose here is to keep retro insight from evaporating with the report — stakeholder reports are normally read once and forgotten, so this section is the durable hook.

  *Strict rules: cite `JIRA:KEY` for every ticket-specific claim; no fluff; no statistics-expert claim without uncertainty rendering; no knowledge-manager learning without a concrete artifact to update."*

If `--no-council`, degrade to direct-LLM and flag in console + frontmatter.

### Phase 6 — Render template-shaped report

Output path: `{{output_root}}\reports\sprint-review.md`. Same overwrite-prompt rule. The report **must** match the SM's standard template (from the user's "Sprint Review" prompt template) so it can be pasted directly into Confluence:

The sprint review report (the SM's standard template — keep its shape so it pastes into Confluence): [REPORT_TEMPLATE.md](REPORT_TEMPLATE.md) — fill every placeholder, keep section order and frontmatter keys.

The four placeholders that the SM is expected to refine before publishing — `Significant customer meetings`, and any council output the SM disagrees with — are clearly marked with `_italics_` placeholders so the SM doesn't accidentally publish them as-is.

If extending the template (adding callouts, dataview, embeds), delegate to `obsidian-markdown`.

### Phase 7 — Console summary

```text
=== Aurora Sprint 2 (INC 28) — Sprint Review ===
Comparing:        start (2026-04-01) → end (2026-04-21)
Committed:        62.5 pts raw / 47.5 pts velocity-relevant
Delivered:        58 pts raw / 43 pts velocity-relevant
Commitment:       0.91 (vr) ≥ 0.85 → MET ✅
Sprint velocity:  43 pts (vr); avg-3 was 58 → ↘️ below trend
Scope:            +8 pts added; 6 pts wedge consumed → ⚠️ +2 pts scope creep
Carry-over:       3 tickets (8 pts)
Council:          statistics-expert + scrum-master + product-owner ✅
Saved:            [sprint-review.md](Scrum Teams/Aurora/Scrum 📅/INC 28/Sprint 2/reports/sprint-review.md)
```

## Rules

- **Read-only.** Read snapshots, JSONL, sprint config, team rules. Don't modify any of them; don't call Jira directly.
- **Template fidelity is mandatory.** The output's section headers must match the SM's standard template (`### Summary of Sprint Accomplishments` etc.) so it pastes cleanly into Confluence. Don't reorder, rename, or skip headers — leave a placeholder if data is missing.
- **`Significant customer meetings` is always a placeholder.** This skill has no source for that data; the SM fills it in manually. Render the placeholder line as italicized text so the SM sees it before publishing.
- **`Feature Demos` auto-population is a best-effort heuristic.** If the auto-extraction yields nothing or feels wrong, render the placeholder line. Never invent demos.
- **Cite ticket keys for every ticket-specific claim** — both in the council output and in the appendix tables.
- **Statistics-expert calibration is load-bearing for the PI Confidence section.** Reject council output where the confidence verdict isn't grounded in the trailing-5-sprint window or where the prediction lacks an uncertainty render.
- **Commitment threshold is configurable but the default is 0.85.** Don't change without the user opting in.
- **Both raw and velocity-relevant numbers are reported when they differ.** Never silently use one over the other.
- **Never overwrite without confirmation.** Same prompt pattern as siblings.

## Edge cases

- **`start.canvas` missing** — refuse. The skill is meaningless without the planning baseline.
- **`end.canvas` missing** — prompt to capture or use latest available phase as a stand-in (with a clear "this is not a true end snapshot" warning written into the report header).
- **`_team-rules.md` missing** — bootstrap; if user picks Skip, run with empty wedge/overhead and flag in console + frontmatter.
- **Sprint with 0 committed points** — refuse; the commitment math is undefined. Surface as an explicit message.
- **Trailing-5-sprint window has fewer than 3 prior `end` rows** — the statistics-expert's PI Confidence section uses what's available and labels the prediction as "low-data".
- **Carry-over with no clear owner** (assignee was off-team or unset) — list under "Unassigned" in the carry-over appendix; the council should flag in Impediments.
- **Wedge ticket missing from start or end** — fall back to "wedge accounting unavailable" warning; commitment math still works.
- **`Feature Demos` heuristic mis-fires** — render placeholder. The SM can update before publishing.
- **In-review overhead items still in IN REVIEW at end-of-sprint** — flag in the Impediments section (the team rule expects them to close on sprint end date, so deviation is signal).
- **Council unavailable / `--no-council`** — degrade to direct-LLM analysis; mark `council_personas: [none]` in the frontmatter so consumers can filter.

## Related skills

| Skill | Use it for |
| :--- | :--- |
| `sprint-snapshot` | Captures the `start.canvas` and `end.canvas` this skill consumes. **Run `--phase start` at sprint kickoff and `--phase end` at sprint close** for a clean review. |
| `sprint-plan` | Sibling — start-of-sprint planning report. Same `_team-rules.md` and `_sprint.md`. The PI Confidence verdict here is informed by patterns the planning report flagged earlier. |
| `sprint-sos-report` | Sibling — weekly comparison reports. Their `Trends` sections feed the PI Confidence reasoning here. |
| `clarity-council` | Phase 5 delegates to it. **statistics-expert** is load-bearing for commitment ratios and PI Confidence calibration; the persona's "no point estimate without uncertainty" rule is enforced. **product-owner** leads Sprint Accomplishments themes; **scrum-master** leads Impediments framing. Stakeholder reports almost always benefit from visuals — add **`infographics-expert`** to the council to produce a sprint-burndown SVG, a commitment-vs-actual bar, a carry-over-flow Sankey, or a 5-sprint trailing-velocity sparkline for the PI Confidence section. They consult statistics-expert for uncertainty rendering and product-owner for the takeaway-shaped chart titles. Pull-list for stakeholder-facing visuals: `statistics-expert + product-owner + infographics-expert + scrum-master`. |
| `obsidian-markdown` | Use when extending the report template with callouts, dataview, embeds. |
| `obsidian-vault` | Use for batch wikilink verification (>15 names). |
| `obsidian-bases` | Use when the user wants a `.base` aggregating reviews across an INC — e.g. "show commitment ratio + carry-over per sprint for Aurora this PI". Strong forecasting input. |
| `daily-standup-prep` | Pattern parent for vault-write conventions and identity matching. |

## Quality Loop

Before returning, check the output against these criteria. If two or more fail, revise and re-check — at most two passes, then note what still falls short.

- Every template section is present (Accomplishments / Status / Sprint Commitment / PI Confidence / Impediments)
- Accomplishments are traced to start.canvas vs end.canvas deltas, not narrated from memory
- Team-specific overhead and wedge-balancing rules were applied
- Impediments are concrete and actionable, not vague

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/sprint-review.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
