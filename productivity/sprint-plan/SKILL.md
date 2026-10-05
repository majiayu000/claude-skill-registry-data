---
name: sprint-plan
category: scrum-sprint
description: >
  Convert the start-of-sprint canvas into a planning report — committed scope, capacity vs
  commitment, WIP-saturation risk, observations, risks. Use when the user says "sprint
  plan", "sprint planning report", or invokes /sprint-plan.
codex-short-description: "Convert the start-of-sprint canvas into a planning report"
related-skills:
  - sprint-snapshot
  - clarity-council
loop-eligible: false
recurrence-hint: on-demand
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
  - AskUserQuestion
  - Skill
compatibility: claude-code codex opencode
---

# Sprint Plan Report

Read the `start.canvas` snapshot for a sprint and produce a planning markdown report. Read-only on Jira (the canvas is already a frozen snapshot — no fresh fetch needed). Writes one report file into the sprint folder.

This skill is the Claude port of the user's "Sprint Plan" prompt template. It expects [sprint-snapshot](../sprint-snapshot/SKILL.md) has already produced a `start.canvas` for the target sprint. If it hasn't, the skill prompts to invoke `sprint-snapshot` first.

## Quick start

```text
/sprint-plan                                    → Aurora, current sprint (auto-detect newest)
/sprint-plan Borealis                               → single team
/sprint-plan Aurora --inc 28 --sprint 2         → explicit sprint
/sprint-plan Aurora --no-council                → skip clarity-council, LLM-only analysis
```

## Parameters

| Param | Default | Notes |
| :--- | :--- | :--- |
| `Team` | from memory or prompt | Same `reference_default_scrum_team.md` source as sprint-snapshot |
| `Inc` | latest from `Scrum 📅/INC <N>/` | Scan vault for newest |
| `Sprint` | latest from `INC <N>/Sprint <N>/` | Scan vault for newest |
| `Personas` | `statistics-expert,scrum-master,product-owner,infographics-expert` | Comma-separated; `--no-council` disables. `infographics-expert` is included by default per the [always-add-charts feedback](#charts-required-section); their output drops Mermaid charts directly into the report body. |

## Workflow

```text
- [ ] Phase 1: Resolve config (vault, team, inc/sprint, sprint config, team rules)
- [ ] Phase 2: Locate and load start.canvas + _snapshots.jsonl (start row)
- [ ] Phase 2.5: Locate previous sprint's end.canvas → derive carry-over set
- [ ] Phase 3: Convert canvas to structured markdown (issue table by status + by member, carry-over annotated)
- [ ] Phase 4: Apply team rules (overhead, wedge, in-review overhead, carry-over) to derive effective capacity
- [ ] Phase 5: Run clarity-council (observations + risks, with carry-over context) unless --no-council
- [ ] Phase 6: Render and write the report (date-stamped per run)
- [ ] Phase 7: Console summary
```

### Phase 1 — Config

Resolve `{{vault_root}}`, `{{jira_project}}`, `{{default_team}}`, `{{output_root}}`, `{{sprint_config}}`, and `{{team_rules}}` per the contracts in [sprint-snapshot/SKILL.md](../sprint-snapshot/SKILL.md#config-resolution-run-once-at-the-start-of-every-invocation) and [sprint-snapshot/REFERENCE.md](../sprint-snapshot/REFERENCE.md#team-rulesmd-shared-with-sprint-plan--sprint-sos-report--sprint-review). Bootstrap missing files via the same `AskUserQuestion` patterns.

### Phase 2 — Locate the start canvas

1. Look for `{{output_root}}\start.canvas`.
2. If missing, `AskUserQuestion`: `Run /sprint-snapshot --phase start now (recommended)` / `Pick a different phase canvas` / `Cancel`. Don't fabricate.
3. Read the canvas as JSON. Filter nodes to issue cards (`id` matches `^issue-`); parse the markdown body for `KEY`, `Summary`, `Assignee`, `Points`, `Type`, `Status` (status comes from the column the card is in — derive from x-coord using the column constants in [REFERENCE.md](../sprint-snapshot/REFERENCE.md#sprint-board-section-ps-lines-436-520) or, simpler, from the card's `color` field).
4. Also read `_snapshots.jsonl` and grab the row where `phase == "start"` for the totals (matches what's already on the canvas; faster to use directly).

### Phase 2.5 — Previous sprint's end → carry-over set

Carry-over from the previous sprint is the planning skill's most load-bearing context — the team didn't get to choose all of this sprint's scope; they inherited part of it. Compute the carry-over set so the council, capacity math, and report all reflect reality.

1. **Locate the previous sprint folder.** `{{output_root}}` is `…\INC <Inc>\Sprint <Sprint>\`. The previous sprint is:
   - `…\INC <Inc>\Sprint <Sprint - 1>\` if `Sprint > 1`
   - `…\INC <Inc - 1>\Sprint 4\` (or the highest `Sprint N` folder in the prior INC) if `Sprint == 1`
2. **Load the previous sprint's `end.canvas`.** If it's missing, fall back in this order: latest `week 3.canvas`, latest `week 2.canvas`, latest `week 1.canvas`. If none exists, skip carry-over derivation and surface a console warning + a frontmatter flag (`carry_over: unavailable`). **Do not invoke `sprint-snapshot` from here** — the previous sprint is closed; if the SM forgot to capture an `end` snapshot, that's a process gap to surface, not silently paper over.
3. **Parse issue cards** from the previous-sprint canvas the same way as `start.canvas` (key, status, points).
4. **Carry-over set** = tickets present in **both** `current_start.canvas` **and** `previous_end.canvas` whose `previous_end.status ∉ {Done, Won't Fix, Duplicate}`. Per the user's planning convention: *all unclosed items from the previous sprint are assumed to carry into this one.* If a ticket was in the previous sprint, was unclosed at end, and **isn't** in this sprint's start, surface a console warning — that's an unusual planning decision the SM should confirm wasn't a mistake.
5. **Sub-classify carry-over** by previous-sprint end-status:
   - `carry_over.in_progress` — was IN PROGRESS at previous end; resume work, expect faster close
   - `carry_over.in_review` — was IN REVIEW at previous end; should close early this sprint
   - `carry_over.todo` — was TO DO at previous end; full sprint of work still ahead
6. **Carry-over points** = sum of points of carry-over tickets at *current sprint start* (use the new estimate if it changed). Track separately as `carry_over_points`.

State the result in one short sentence: *"Carry-over from Sprint 1: 4 tickets (11 pts) — 1 in-progress, 2 in-review, 1 to-do."*

### Phase 3 — Canvas → markdown

Build the structured backbone before any narrative. Two views:

**By status** (kanban cross-section). Annotate carry-over rows with a `🔄` glyph in the leading column and a `(carry-over: <prev-status>)` suffix in the Summary cell so the SM can scan-find them:

```markdown
## Committed Scope by Status

### TO DO (Unassigned) — N tickets, P pts
| | Key | Summary | Type | Points |
| :-: | :--- | :--- | :--- | --: |
| | JIRA:PROJ-1234 | Summary | Story | 3 |
| 🔄 | JIRA:PROJ-1100 | Summary (carry-over: in-review) | Story | 2 |

### TO DO (Assigned) — N tickets, P pts
…
### IN PROGRESS — N tickets, P pts
…
### IN REVIEW — N tickets, P pts
…
### DONE — N tickets, P pts (typically 0 at sprint start)
…
```

**By member** (workload view):

```markdown
## Committed Scope by Member

### [[@First Last]] — N tickets, P pts (effective capacity: C pts)
| Key | Summary | Status | Points |
| :--- | :--- | :--- | --: |
| JIRA:PROJ-1234 | Summary | TO DO | 3 |

### Off-team
…
### Unassigned
…
```

Use `JIRA:KEY` on its own table cell so the Obsidian Jira plugin auto-links each row.

### Phase 4 — Apply team rules

Compute the derived numbers the report depends on:

- **Overhead-adjusted capacity per member** = `nominal_capacity × (1 - overhead_pct/100)`. For overhead members listed in `_team-rules.md`, surface both nominal and effective.
- **In-review overhead identification** — scan IN REVIEW issues; flag any whose summary matches a `_team-rules.in_review_overhead.title_patterns` entry. Tag these in the by-status table with a `(overhead)` suffix and a footnote: *"Excluded from velocity; counted toward capacity."*
- **Wedge ticket detection** — find the wedge ticket in the canvas (key matches `_team-rules.wedge.ticket_key`); record its starting points. Used by `sprint-sos-report` later to detect scope creep.
- **Velocity-relevant points** = `committed - in_review_overhead_points`. This is the number the team is actually expected to deliver.
- **Carry-over capacity math** — split `velocity_relevant_points` into `carry_over_points` and `new_commit_points = velocity_relevant_points - carry_over_points`. The headline numbers in the report should make both visible: a sprint that committed 60 pts of which 25 are carry-over has very different planning implications than 60 pts of fresh work. Surface carry-over as a percentage of velocity-relevant commit (`carry_over_points / velocity_relevant_points`).
- **Carry-over WIP risk** — count `carry_over.in_progress + carry_over.in_review` tickets. If this is > 30% of total committed tickets, the sprint starts already-WIP-saturated; flag for the council.

### Phase 5 — Clarity-council

Unless `--no-council`, invoke `clarity-council` via `Skill` with the personas list. Pass:

- The `Phase 3` markdown view (both by-status and by-member, with carry-over annotations)
- The `Phase 4` derived numbers (effective capacity, velocity-relevant points, carry-over points + percentage, carry-over WIP risk)
- The `Phase 2.5` carry-over set (full list with `JIRA:KEY` and previous-end status)
- The `_sprint.md` frontmatter (capacity, last_sprint_velocity, avg_velocity_last_3)
- Their assignment: *"Produce **three** short markdown sections: `## Key Observations` (3-7 bullets), `## Risks` (3-7 bullets, each with severity High/Med/Low and a one-sentence mitigation), **and `## Infographics` (3-5 Mermaid charts that visualize the headline numbers)**. The statistics-expert weighs commitment vs velocity history **and explicitly addresses carry-over: how much of the committed velocity is already-spoken-for, and what that implies for new-work throughput** (with a prediction interval). The scrum-master weighs team load distribution, carry-over WIP risk (sprint starts WIP-saturated?), and re-planning signals. The product-owner weighs scope coherence, dependency surface, and whether carry-over items are still the right priorities or stale. **The infographics-expert produces the chart block — see Required charts below.** Strict rule: cite issue keys (JIRA:KEY format) for any specific claim — including every carry-over item the council references. No fluff."*

#### Charts required (`## Infographics` section) {#charts-required-section}

The `infographics-expert` persona must produce **at minimum** these Mermaid charts, each with a one-line caption. (don't ship reports as numbers-only narratives when a chart would land it faster).

| # | Chart | Type | Series |
| --- | --- | --- | --- |
| 1 | **Capacity vs commit** | Mermaid `xychart-beta` (bar) | Capacity (line/reference), gross committed, velocity-relevant, last-sprint velocity, 3-sprint avg velocity |
| 2 | **Carry-over share of velocity-relevant commit** | Mermaid `pie showData` | carry-over points vs new-commit points |
| 3 | **Per-member workload (% of capacity)** | Mermaid `xychart-beta` (bar) | one bar per assigned member, sorted desc; flag any >25% with a marker note in the caption |
| 4 | **Status mix at sprint start** | Mermaid `pie showData` | Done / In Review / In Progress / To Do points |
| 5 | **Velocity trend** | Mermaid `xychart-beta` (line) | S1, S2, S3 (assumed/actual), S4 commit (point), with a horizontal reference at capacity |

Only skip a chart if the underlying data is genuinely empty (e.g. no carry-over → skip chart #2 with a note "no carry-over data"). Never skip silently. If the persona claims a chart can't be drawn, render the same data as a markdown table and label it "fallback (chart unavailable)."

If `--no-council` skips clarity-council entirely, the skill MUST still render the Infographics section directly via inline LLM rendering — the chart requirement is independent of the council orchestration.

If `clarity-council` is unavailable or `--no-council`, render a simpler `## Key Observations` and `## Risks` block from a direct LLM analysis using the same input — but flag in the console summary that the council was skipped.

### Phase 6 — Render and write

Output path: `{{output_root}}\reports\sprint-plan-{{YYYY-MM-DD}}.md` (Pittsburgh local date). Create `reports/` if missing.

**Re-run semantics:**

- **Same-day re-run** → overwrite today's `sprint-plan-YYYY-MM-DD.md` **silently**. The newer run reflects the latest snapshot data; the user expects this to "refresh today's report." No prompt.
- **Different-day re-run** → write a new dated file. Prior days' reports stay untouched on disk — they are the historical record of how the plan looked at that point in time.
- **Symlink-style "latest" pointer** → after writing, also update (overwrite) `{{output_root}}\reports\sprint-plan-latest.md` to be a single-line pointer file containing `[[sprint-plan-{{YYYY-MM-DD}}]]`. This gives the SM a stable wikilink target for dashboards and bases without chasing the date.

This per-day cadence pairs with `sprint-snapshot`'s per-phase cadence: snapshot is *what the board looked like at this phase*, sprint-plan is *how I interpreted the plan on this date* — both are point-in-time records that shouldn't be silently overwritten across days. Within a day, however, the planning report just gets refreshed.

Template:

The planning report: [REPORT_TEMPLATE.md](REPORT_TEMPLATE.md) — fill every placeholder, keep section order and frontmatter keys.

If extending the template with callouts, dataview blocks, or embeds, delegate to `obsidian-markdown` via `Skill`.

### Phase 7 — Console summary

```text
=== Aurora Sprint 2 (INC 28) — Sprint Plan ===
Source:           Sprint 2/start.canvas (snapshot_at 2026-04-01T09:14:00-04:00)
Carry-over base:  Sprint 1/end.canvas (snapshot_at 2026-03-31T17:42:00-04:00)
Tickets / Points: 24 / 62.5  (4 tickets / 11 pts carry-over 🔄)
Capacity:         80.8 (committed 62.5; velocity-relevant 47.5 after 15 pts in-review overhead)
Carry-over share: 11 / 47.5 = 23% of velocity-relevant commit
Carry-over WIP:   3 of 24 tickets start already-WIP (12%) — within tolerance
Council:          statistics-expert + scrum-master + product-owner + infographics-expert ✅
Charts rendered:  5 Mermaid blocks (capacity-vs-commit, carry-over share, per-member workload, status mix, velocity trend)
Saved:            [sprint-plan-2026-04-01.md](Scrum Teams/Aurora/Scrum 📅/INC 28/Sprint 2/reports/sprint-plan-2026-04-01.md)
                  [sprint-plan-latest.md] → updated pointer
```

If this is the second run today: `Saved: refreshed sprint-plan-2026-04-01.md (silent overwrite — same-day re-run)`.

## Rules

- **Read-only.** Read the canvas, the JSONL, the sprint config, and the team rules. Don't modify any of them. Don't call Jira directly — the canvas is the snapshot.
- **Never fabricate ticket data.** If a card's metadata is malformed, surface the parse failure in the console summary; don't invent values.
- **Council citations are mandatory.** Personas must reference `JIRA:KEY` for any claim about a specific ticket. Reject council output that fails this rule and re-prompt.
- **Carry-over assumption is unconditional.** All unclosed items from the previous sprint's `end.canvas` (or best-available fallback snapshot) are treated as carried into this sprint. The skill does not negotiate with the user about which items carried — that is already reflected in `start.canvas`. Surface, don't decide.
- **Same-day re-runs overwrite silently; cross-day runs create new dated files.** This is the *opposite* of `sprint-snapshot`'s overwrite-prompt rule because the planning report is a daily refresh, not a phase-locked snapshot. Prior days' planning reports are historical record and never touched.
- **The `sprint-plan-latest.md` pointer is the canonical wikilink target** for dashboards and bases. Always update it on every run.
- **Prefer the JSONL row over re-counting from the canvas** for headline totals — it's the canonical record. Use canvas parsing only for the per-issue table.
- **Wikilink team members only when the vault note exists.** Same `Glob("{{vault_root}}/🤼 Team/**/@*.md")` rule as sprint-snapshot.
- **Charts are mandatory.** Every sprint-plan report MUST contain the `## Infographics` section with the Mermaid charts spec'd in [Charts required](#charts-required-section). This applies whether the council ran or not. Numbers-only narratives are a regression.
- **`_team-rules.md` lookup search order**: (1) `{{output_root}}/_team-rules.md` (sprint-level override, rare), (2) `{{output_root}}/../_team-rules.md` (INC-level, also rare), (3) **`{{vault_root}}/Scrum Teams/<Team>/_team-rules.md`** (canonical team-root location, where Pyrite's lives). Do not declare team-rules missing without searching all three.

## Edge cases

- **No `start.canvas`** — prompt to run `sprint-snapshot --phase start` first; do not fall back to `week 1` or invent a start state.
- **No previous sprint `end.canvas`** — fall back to `week 3.canvas`, then `week 2.canvas`, then `week 1.canvas` from the previous sprint folder. If none exist, set `carry_over: unavailable` in the frontmatter, render the report without a Carry-over section but with a `> ⚠️ Carry-over could not be derived — previous sprint had no captured snapshots.` callout near the top, and surface in the console summary. The council should be told carry-over data is unavailable so it doesn't hallucinate one.
- **First sprint of a new INC (Sprint 1) with no prior INC** — same as "no previous sprint" — set `carry_over: not_applicable` and skip the section entirely (no warning, this is expected).
- **Carry-over ticket present in previous-end but not in current-start** — surface as a console warning: *"⚠️ JIRA:PROJ-1100 was unclosed at end of Sprint 1 but is not in Sprint 2 start.canvas. Confirm with PO this was intentional (de-scoped, moved to backlog) and not a planning oversight."* Don't fail; record in the report's "Stale-priority check" footnote.
- **Carry-over ticket re-estimated between sprints** — use the `start.canvas` (current sprint) point value, not the previous-end value. Note the change in the carry-over table: `prev: 3 pts → now: 5 pts`.
- **Same-day re-run — third+ run** — same as the second: silent overwrite of today's file. The `sprint-plan-latest.md` pointer doesn't need re-updating (it already points to today) but rewrite it anyway for idempotency.
- **Run on a day spanning a date boundary (after midnight)** — Pittsburgh local date determines the filename. A run started 11:55 PM ET that finishes 12:05 AM ET writes to the date the run *started* — same convention `daily-briefing` uses, prevents off-by-one filenames.
- **`_team-rules.md` missing** — only declare missing after exhausting all three lookup paths (sprint folder, INC folder, **team root** `Scrum Teams/<Team>/`). The team-root location is canonical for Pyrite; sprint/INC overrides are rare. If genuinely missing across all three, prompt to bootstrap (per [sprint-snapshot/REFERENCE.md](../sprint-snapshot/REFERENCE.md#bootstrap)). Run anyway with empty overhead/wedge if the user picks "Skip"; flag in the console that the report is less accurate.
- **Wedge ticket key in `_team-rules.md` doesn't appear on the canvas** — surface a warning ("Wedge ticket PROJ-9999 not in sprint — wedge accounting will be skipped this sprint"); continue.
- **Council unavailable / `--no-council`** — degrade to direct-LLM observations + risks; mark `council_personas: [none]` in the frontmatter so consumers can filter.
- **Sprint with 0 committed points** — render the report; the observations section will (correctly) flag it.
- **Multi-team run is not supported in v1** — single team only. (Multi-team would loop the workflow per team and write one report per team. Add later if needed.)

## Related skills

| Skill | Use it for |
| :--- | :--- |
| `sprint-snapshot` | Produces the `start.canvas` this skill consumes. **Run first** if it's missing. |
| `sprint-sos-report` | Sibling — weekly comparison report. Reads the same `_team-rules.md` and snapshots. |
| `sprint-review` | Sibling — end-of-sprint stakeholder report. Reuses the same scaffolding. |
| `clarity-council` | Phase 5 delegates to it for the observations + risks analysis. **statistics-expert** is the load-bearing persona for capacity-vs-velocity reasoning; **scrum-master** for team-load and re-planning signals; **product-owner** for scope coherence. Add **`infographics-expert`** to the council when the report needs embedded visuals (carry-over Sankey, capacity-vs-commit bar, per-member workload small-multiple) — they consult statistics-expert for uncertainty rendering and produce the SVG/Mermaid that drops into the report body. |
| `obsidian-canvas` | Use if extending the report with embedded canvas snippets or sub-canvases. |
| `obsidian-markdown` | Use when extending the report template with callouts, dataview, embeds. |
| `obsidian-vault` | Use for batch wikilink verification (>15 names). |
| `obsidian-bases` | Use when the user wants a `.base` aggregating sprint plans across an INC (e.g. "show committed vs avg velocity for every Aurora sprint in INC 28"). |

## Quality Loop

Before returning, check the output against these criteria. If two or more fail, revise and re-check — at most two passes, then note what still falls short.

- Carry-over vs new-commit split is explicit and the numbers reconcile to total committed points
- Capacity-vs-commitment is stated with the WIP-saturation risk called out when over capacity
- Observations and risks come from the council pass, not filler
- Output is date-stamped and the -latest pointer updated

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/sprint-plan.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
