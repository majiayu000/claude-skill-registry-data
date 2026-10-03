---
name: retro
description: Strategic decision retrospective — review research decisions against actual outcomes, update confidence levels
type: analysis
version: v0.5
required_conventions: [alignment-page]
argument-hint: "[optional: focus area e.g. \"ICP\", \"pricing\", \"channels\"]"
context_intake: scoped
---

## Pack Availability Guard

When recommending a skill from another pack, verify the target pack is installed via `.agents/project.json` `enabled_packs`. If it is not enabled, recommend `npx skillpacks install <pack>` from the project shell. After install, tell Claude users to run `/reload-skills`, then `/clear` or restart if the skill remains invisible. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# Retro — Strategic Decision Retrospective

Reviews decisions made in research docs against actual outcomes. Was the primary ICP right? Did pricing work? Did the launch channel deliver? Captures lessons and updates confidence levels across all research documents.

## Prerequisites

- **Hard**: At least 2 research docs must exist, AND at least one source of outcome data must exist (`research/customer-feedback.md`, `research/cohort-review-*.md`, or `research/runway-model.md`). If no outcome data exists, tell the user there's nothing to retrospect against yet and stop.
- **Soft**: The more research + outcome data exists, the richer the retro. Reads all of: `research/icp.md`, `research/competitive-analysis.md`, `research/journey-map.md`, `research/metrics.md`, `research/gtm.md`, `research/monetization.md`, `research/positioning.md`, `research/assumption-tracker.md`, `research/customer-feedback.md`, `research/cohort-review-*.md`, `research/runway-model.md`, `research/experiments/*.md`.

## Process

### 0. Product-Path Scope Resolution

Resolve research scope by product path before using code or app structure as a hint:

1. If `$ARGUMENTS` names a non-archived `research/{slug}/` directory or a product-path ID whose `scope_path` points there, use that path. Treat `{slug}` as the product/app name, not the ICP, audience, or segment label.
2. If `$ARGUMENTS` names only `research/_archive/{slug}/` or a manifest entry with `status: archived` or legacy `status: abandoned`, stop and warn that the path is archived; do not write or update scoped outputs there.
3. Read `research/.progress.yaml` when present. Normalize legacy `active_path` to `active_paths` on read and write back `active_paths` on manifest updates. Treat legacy `abandoned` as `archived`; exclude `archived`, `abandoned`, `deferred`, `revisit_candidate`, `promoted`, and any `scope_path` under `research/_archive/` from active target selection.
4. If active product paths exist in the manifest, use those paths. If multiple active paths exist, ask which one to target unless this skill explicitly supports cross-path output.
5. If no active manifest target exists, list non-archived product directories under `research/`, excluding `research/_archive/` and dot directories. Auto-select only when exactly one exists; ask when multiple exist.
6. If no product directories exist, use flat `research/` single-product mode.
7. Detect monorepo/app/package structure only as a secondary hint. Suggest creating a missing `research/{slug}/` product path when code clearly exposes an app, but do not require code or monorepo detection before using `research/{slug}/`.

When product path `{slug}` is active, read and write research under `research/{slug}/`, specs under `specs/{slug}/`, and treat top-level `research/*.md` files as flat-mode documents or cross-path summaries.

### 1. Load Everything

Read ALL research documents and outcome data. Build a map of:
- **Decisions made**: Key choices documented in each research file (primary ICP, pricing model, launch channel, positioning, etc.)
- **Predictions/targets**: Expected outcomes (metric targets, revenue projections, conversion estimates)
- **Actual outcomes**: Real data from customer feedback, cohort reviews, runway model, experiment results

### 2. Decision-by-Decision Review

For each major decision found in research docs:

#### A. ICP Decisions (from `research/icp.md`)
- Was the primary ICP selection correct?
- Did the pain points rank correctly?
- Were the trigger events accurate?
- Did the market sizing hold up?

#### B. Competitive Decisions (from `research/competitive-analysis.md`)
- Did the competitive landscape change?
- Were the identified gaps real?
- Did differentiation hold?

#### C. Journey Decisions (from `research/journey-map.md`)
- Did users follow the mapped journey?
- Was the aha moment correctly identified?
- Were the churn triggers right?

#### D. Metrics Decisions (from `research/metrics.md`)
- Were targets realistic?
- Was the North Star metric the right choice?
- Which metrics turned out to be leading vs. lagging indicators?

#### E. GTM Decisions (from `research/gtm.md`)
- Did the primary channel work?
- Was the messaging effective?
- Did the launch plan execute as designed?

#### F. Monetization Decisions (from `research/monetization.md`)
- Was the pricing model correct?
- Were price points right?
- Did unit economics match estimates?

#### G. Positioning Decisions (from `research/positioning.md`)
- Was the market category right?
- Did the competitive framing resonate?
- Was the target segment correct?

For each decision, classify:
- **Correct** — the decision was right, outcomes match
- **Partially correct** — directionally right but details were off
- **Wrong** — the decision was incorrect and outcomes show it
- **Unknown** — insufficient outcome data to judge

### 3. Pattern Analysis

Look across all decisions for patterns:
- **Systematic biases** — are we consistently too optimistic? Too conservative? Biased toward certain segments?
- **Research gaps** — which decisions had the least evidence and turned out wrong?
- **Compounding errors** — where did one wrong decision cascade into others?
- **Surprising successes** — what worked that we didn't expect?
- **Timing issues** — were decisions right but timing wrong?

### 4. Present & Validate

Use AskUserQuestion to present findings:
- Summary of decisions reviewed and their correctness
- Key patterns identified
- Recommendations for which research docs to re-run

Ask:
- "Does this assessment feel accurate? Any decisions I'm judging too harshly or too generously?"
- "Any context I'm missing about why certain decisions were made?"
- "What surprised you most in practice vs. what the research predicted?"

Incorporate feedback before proceeding.

### 5. Populate Next Steps

Include 3–5 applicable items with "Pick one:" framing:

- IF ICP decisions were wrong: `/customer-discovery` — Re-run customer discovery with what you now know
- IF pricing was wrong: `/monetization` — Revisit pricing with real revenue data
- IF channels underperformed: `/gtm` — Update GTM with actual channel performance
- IF assumptions tracker exists: `/assumption-tracker` — Bulk-update validation status from retro findings
- IF metrics targets were off: `/metrics` — Recalibrate targets based on baseline reality
- IF multiple docs need updating: `/reconcile-research` — Audit all research for consistency after retro findings
- ALWAYS: `/research-roadmap` — Check overall project status

### 6. Write Output

Present final retro to user. Ask:
- "Ready to write this? Anything to adjust?"

Only after confirmation, write the output file.

## Output

### `research/retro-[YYYY-MM-DD].md` (or `research/{slug}/retro-[YYYY-MM-DD].md`)

```markdown
# Strategic Retro: [Date]

> Date: [current date]
> Period reviewed: [timeframe — e.g., "launch through Q1 2026"]
> Research docs reviewed: [count]
> Outcome data sources: [list]

## Summary

[3-5 sentences: the headline findings — what was right, what was wrong, and the biggest lesson]

## Decision Scorecard

| Area | Decision | Status | Evidence | Impact |
|------|----------|--------|----------|--------|
| ICP | [decision] | Correct/Partial/Wrong/Unknown | [data source] | [what it affected] |
| Competitive | [decision] | ... | ... | ... |
| Journey | [decision] | ... | ... | ... |
| Metrics | [decision] | ... | ... | ... |
| GTM | [decision] | ... | ... | ... |
| Monetization | [decision] | ... | ... | ... |
| Positioning | [decision] | ... | ... | ... |

**Score**: [X/Y correct] — [percentage]

## Detailed Analysis

### What We Got Right
[Decisions that were correct and why — what made the research good here]

1. **[Decision]** — [evidence it was right] — [lesson: what to keep doing]
2. ...

### What We Got Wrong
[Decisions that were wrong and why — what the research missed]

1. **[Decision]** — [evidence it was wrong] — [lesson: what to change]
2. ...

### What We Got Partially Right
[Decisions that were directionally correct but details were off]

1. **[Decision]** — [what was right, what was off] — [lesson]
2. ...

## Patterns

### Systematic Biases
[Recurring patterns in how decisions were made — e.g., consistently overestimating market size, underestimating competition]

### Research Gaps
[Where lack of evidence led to wrong decisions — what should have been researched more]

### Compounding Errors
[Where one wrong decision led to others — the chain of consequences]

## Confidence Updates

Research docs that should be re-run based on retro findings:

| Document | Current Confidence | Recommended Action | Why |
|----------|-------------------|-------------------|-----|
| research/icp.md | [High/Med/Low] | [Re-run / Update section / Keep] | [reason] |
| research/gtm.md | [High/Med/Low] | [Re-run / Update section / Keep] | [reason] |
| ... | | | |

## Lessons Learned

1. **[Lesson title]** — [description — specific, actionable, grounded in evidence from this retro]
2. ...

## Next Steps

Pick one:
- [conditional items from step 5]
```

Create the `research/` directory if it doesn't exist.

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- **Evidence-based judgments.** Every "correct" or "wrong" assessment must cite specific outcome data. Don't judge decisions without evidence.
- **No hindsight bias.** Judge decisions based on what was knowable at the time, not what we know now. A decision can be "right process, wrong outcome" — note when this is the case.
- **Present before writing.** Never write output files until findings have been presented and validated.
- **Separate dated files.** Each retro is a new file. Don't modify previous retros.
- **Be constructive.** The goal is learning, not blame. Frame "wrong" decisions as lessons, not failures.
- **Recommend actions.** Every finding should connect to a concrete next step for improving the research.
- **Quarterly or milestone-based.** Designed for periodic use, not continuous. Note the recommended next retro date.

## Context Gathering

**Step 1 — Scope questions.** Before researching, ask the user 1–3 questions via `AskUserQuestion` to understand: their product/service, target audience, and what they hope to learn or decide from this research.

**Step 2 — Research.** Conduct research scoped by the user's answers.

**Step 3 — Findings validation.** Before building the alignment page, present the 3–5 most important findings and ask the user to validate or correct any critical assumptions.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/retro-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
