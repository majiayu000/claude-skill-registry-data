---
name: gtm
description: Go-to-market planning — channel strategy, messaging, pricing, launch plan, and early traction tactics
type: research
version: v0.12
required_conventions: [alignment-page]
argument-hint: "[optional: focus area e.g. \"pricing\", \"launch plan\"]"
context_intake: deep
visual_tier: visual
---

## Pack Availability Guard

When recommending a skill from another pack, verify the target pack is installed via `.agents/project.json` `enabled_packs`. If it is not enabled, recommend `npx skillpacks install <pack>` from the project shell. After install, tell Codex users to start a fresh Codex CLI session if the `$` skill list remains stale. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# GTM — Go-to-Market Planning

Invoke as `$gtm`.

## Report-First Approval Gate

Default to scope-first approval: before synthesized research, inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions in a `review` alignment page plus a concise conversation summary.

Do not perform synthesized research, rank candidates, make recommendations, or write working packets or canonical deliverables until final compiled YAML approves the research scope. Minimal pre-approval discovery may identify available files, source categories, and open questions; label it as scope evidence, not findings.

After approved research-scope YAML, perform the research and write only the non-canonical working packet defined in the staged workflow. Then update the `review` alignment page with findings and stop again for feedback-only YAML or final compiled YAML artifact approval before creating or updating canonical research, spec, or task files.

Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language. The approval request itself is the next action. Only emit next-skill routing after the approved artifact has been written or updated.

## Staged Research Workflow

Use this staged workflow for synthesized research or report outputs that would create or update canonical research, spec, or task files.

1. **Stage 1 - Scope discovery and approval.** Inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions. Build the `review` HTML alignment page before synthesized research. The page must render the proposed scope, available source categories, known context, assumptions/confidence, proposed working-packet and canonical output paths, and research-scope approval gates. Stop for final compiled YAML approval of the research scope. Do not perform synthesized research, rank candidates, make recommendations, or write working packets, canonical research, spec, or task files in Stage 1.
2. **Stage 2 - Research and artifact review.** Only after approved research-scope YAML with no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback, perform the synthesized research, run required source/code checks, and write only a non-canonical working packet: flat mode uses `research/_working/preliminary-<skill>-research.md`; product-path mode uses `research/{slug}/_working/preliminary-<skill>-research.md`. Replace `<skill>` with this skill's `name` value. Raw evidence or search logs may remain as supporting evidence where this skill already requires them, but synthesized deliverables stay in the working packet. Update the `review` HTML alignment page so it renders the complete working-packet substance as structured HTML review UI: purpose-built sections, tables, matrices, gates, cards, and tier-appropriate charts or diagrams that preserve every packet section, finding, caveat, and decision detail without summary loss. Raw Markdown packet text may appear only as a supplemental source view after the rendered review UI; do not make a `Full Preliminary Packet` or `Full Working Packet` raw Markdown dump, giant `<pre><code>` block, link-only view, or source-only view the primary review surface. Include the evidence matrix, assumptions/confidence register, source coverage gaps, proposed canonical file changes, and artifact approval gates. Stop for either feedback-only YAML or final compiled YAML. Feedback-only YAML revises the working packet and page, then remains in Stage 2.
3. **Stage 3 - Finalize approved artifacts.** Consume final compiled YAML for artifact approval only when it has no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback. Apply approved edits first, archive the working packet to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, remove the active working packet, write the approved canonical artifacts to the unchanged output paths below, and convert the alignment page to `confirmed` with the approval record preserved.

Canonical output paths remain unchanged. Search logs and other supporting evidence remain allowed only where this skill's output contract already requires them.

## Evidence And Feedback Handling

Treat user feedback as input to evaluate, not as automatic ground truth.

- For factual, evidentiary, technical, or source-backed claims: verify against available evidence. If the user appears to misunderstand the evidence or states something factually incorrect, push back clearly and cite the evidence. Do not rewrite findings merely to agree.
- For taste, brand, positioning preference, risk appetite, prioritization, or other subjective judgment calls: weigh user feedback heavily and adapt the recommendation unless it conflicts with verified evidence.
- When feedback mixes facts and preference, separate them explicitly: correct the factual part, then incorporate the preference where it is a legitimate judgment call.
- When uncertain, say what is known, what is inferred, and what would change the conclusion.

## Prerequisites

- **Hard**: `research/icp.md` (or `research/{slug}/icp.md` in product-path mode) must exist. If not, tell the user to run `$customer-discovery` first and stop.
- **Soft**: Read `research/competitive-analysis.md` (or `research/{slug}/competitive-analysis.md`), `research/journey-map.md` (or `research/{slug}/journey-map.md`), `research/customer-feedback.md` (or `research/{slug}/customer-feedback.md`) if they exist — these improve specificity but aren't required.

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

### 1. Product Path Manifest

Read `research/.progress.yaml` when present. Normalize `active_path` (singular legacy) to `active_paths` (plural list) when reading; treat legacy `abandoned` as `archived` and exclude archived/deferred/revisit/promoted paths plus `research/_archive/` scopes from active target selection. Scope GTM strategy to the active product path by default. When GTM channels or messaging would serve a deferred product path better than the active one, add a `## Product Path Implications` section recommending `$product-line fork` or noting the impact.

### 2. Load Context

- Read `research/icp.md` (or `research/{slug}/icp.md`) — ICP segments, pain points, value props, trigger events, current-state journey
- Read `research/competitive-analysis.md` (or `research/{slug}/competitive-analysis.md`) if it exists — competitor positioning, pricing, channels, market gaps
- Read `research/journey-map.md` (or `research/{slug}/journey-map.md`) if it exists — customer journey stages, discovery channels, conversion triggers
- Read `research/customer-feedback.md` (or `research/{slug}/customer-feedback.md`) if it exists — real customer language, validated/invalidated assumptions
- Read `research/positioning.md` (or `research/{slug}/positioning.md`) if it exists — positioning framework that messaging should flow from
- Read CLAUDE.md and README if they exist — product context

### 3. Interview

Codex interview cadence is one primary decision question per turn by default. Use short follow-up bullets only when they clarify the same GTM decision, not to batch unrelated questions. If the session is already in Plan mode, `request_user_input` may present 2-3 concrete choices for the current decision; otherwise ask one concise plain-text question.

**Research and recommend by default.** For each decision point, use web search, upstream research docs (`research/*.md`), and codebase analysis to gather evidence before asking the user. Assume the user has no insider knowledge unless they explicitly provide it. Present findings with data, define any relevant terms, state a recommendation with reasoning, and ask the user to approve, adjust, or override based on hard constraints, proprietary facts, or corrections. Only ask the user to choose without a recommendation when the decision genuinely depends on internal constraints, personal preferences, or strategic bets that cannot be inferred from evidence.

Cover these areas (skip or abbreviate areas the user has already addressed in `$ARGUMENTS`):

#### A. Channel Strategy
- Where does the ICP hang out? (communities, platforms, events, publications)
- Which channels do competitors use? Where are the gaps?
- What's the primary acquisition channel? (content, community, outbound, product-led, partnerships)
- What's the secondary/backup channel?
- What's the budget and resource constraint? (bootstrapped, funded, team size)

#### B. Messaging Framework
- IF `research/positioning.md` exists: use positioning statement, market category, unique attributes, and value mapping as the foundation for messaging — do not contradict positioning decisions
- What's the one-liner? (the sentence that makes the ICP lean in — should flow from positioning statement)
- What's the primary value prop framing? (save time, save money, reduce risk, unlock capability — should align with positioning value mapping)
- What pain point does the headline address? (from ICP pain map)
- What proof points exist? (metrics, testimonials, case studies, demos)
- How does positioning differ from competitors? (from positioning.md if it exists, otherwise from competitive analysis)

#### C. Pricing Strategy
- What's the pricing model? (freemium, free trial, paid-only, usage-based, seat-based)
- What's the entry price point? What does the ICP currently pay for alternatives?
- What triggers the upgrade? (usage limits, team features, advanced capabilities)
- Are there pricing tiers? What differentiates them?
- How does pricing compare to competitors?

#### D. Launch Plan
- What's the launch timeline? (soft launch, beta, public launch)
- What's the launch channel? (Product Hunt, Hacker News, Twitter, email list, direct outreach)
- What's the launch goal? (signups, revenue, feedback, press)
- What launch assets are needed? (landing page, demo, video, blog post)
- Who are the first 10 customers? (specific names or types)

#### E. Early Traction Tactics
- What's the 30-day post-launch plan?
- What manual/unscalable things will you do? (concierge onboarding, personal outreach, hand-holding)
- What's the feedback loop? (how will you learn from early users?)
- What's the one metric that matters for the first 90 days?
- When do you pivot from manual to scalable?

### 4. Present Findings & Validate

**Present the complete GTM plan to the user before writing.** Summarise with evidence:
1. Channel strategy — primary and secondary channels, with ICP behavior data supporting each choice
2. Messaging framework — one-liner, value prop framing, proof points, citing specific ICP pain points addressed
3. Pricing strategy — model, entry point, tiers, with competitor pricing benchmarks as anchors
4. Launch plan — timeline, channels, goals, assets needed, citing trigger events that inform timing
5. Early traction tactics — 30/60/90 day plan, the one metric that matters, with journey data supporting the traction approach

If the session is already in Plan mode, prefer `request_user_input`; otherwise ask in plain text:
- "Does this capture the go-to-market plan? What constraints, missing facts, or weak assumptions should I adjust?"

Continue until the user confirms. Only then proceed to writing.

### 5. Populate Next Steps

Before writing, check which files exist to populate the `## Next Steps` section contextually. Include a **Recommended** item (the single highest-impact next step given current project state) with a one-line reason, followed by **Other options** (2–4 alternatives). Use this format in the output:

## Next Steps

**Recommended:** [recommended skill] — [one-line reason why this is the highest-impact next action given current state]

Other options:
- `$skill` — [description]
- ...

**Recommendation priority:**
1. IF downstream impact is **Major**: recommend `$reconcile-research` — [N] conflicts found in downstream docs need resolution before other work
2. Otherwise, recommend the first applicable from this list:
   - IF no `research/growth-model.md`: `$growth-model` — design compounding growth loops to make the GTM strategy sustainable
   - IF `specs/` exist and no `tasks/roadmap.md`: check `.agents/project.json.enabled_packs` for `agent-work-admin` — if `agent-work-admin` is not enabled, recommend `npx skillpacks install agent-work-admin` first; if `agent-work-admin` is enabled, recommend `$roadmap` — plan the build with launch milestones from above
   - IF no `research/metrics.md`: `$metrics` — define success metrics for the launch goals
   - IF open questions need research: `$experiment [top question]` — validate the most critical open question
   - IF `tasks/roadmap.md` exists: `$exec` — start executing — the GTM plan is set

**Other options** (include all applicable items not chosen as recommended):
- IF `specs/` exist and no `tasks/roadmap.md`: check `.agents/project.json.enabled_packs` for `agent-work-admin` — if `agent-work-admin` is not enabled, recommend `npx skillpacks install agent-work-admin` first; if `agent-work-admin` is enabled, recommend `$roadmap` — Plan the build with launch milestones from above
- IF no `research/metrics.md`: `$metrics` — Define success metrics for the launch goals
- IF open questions need research: `$experiment [top question]` — Validate the most critical open question
- IF `tasks/roadmap.md` exists: `$exec` — Start executing — the GTM plan is set
- IF no `research/journey-map.md`: check `.agents/project.json.enabled_packs` for `customer-lifecycle` — if `customer-lifecycle` is not enabled, recommend `npx skillpacks install customer-lifecycle` first; if `customer-lifecycle` is enabled, recommend `$journey-map` — Map the customer journey to validate funnel assumptions
- IF no `research/growth-model.md`: `$growth-model` — Design compounding growth loops to sustain GTM momentum
- IF no `research/positioning.md`: check `.agents/project.json.enabled_packs` for `business-discovery` — if `business-discovery` is not enabled, recommend `npx skillpacks install business-discovery` first; if `business-discovery` is enabled, recommend `$positioning` — Define strategic positioning — messaging should flow from positioning

**Impact-aware adjustments:**
- IF downstream impact is **Minor**: annotate relevant skill suggestions with "(stale — [brief description])"
- If downstream impact has not been classified yet, run the downstream impact check against the proposed output before selecting the final recommendation. Do not emit a Minor/Major impact recommendation speculatively.

### 6. Write Output

Only after the user has validated the findings, write the output files.

### 7. Downstream Impact Check

After writing, check for downstream research documents that may be affected by what was just decided. Only check documents that exist on disk.

**Downstream documents to check** (use `{slug}/` prefix when product-path scope is active):
- `research/monetization.md`

For each existing downstream document:
1. Read it — focus on `> Based on:` header, `## Summary`, and sections that reference concepts this skill just defined or changed
2. Identify **specific conflicts**: claims, assumptions, or references that contradict what was just decided. Examples:
   - A pricing model reference that contradicts the pricing strategy just defined
   - Channel strategy assumptions that have shifted
   - Launch timeline or traction targets that no longer align
3. Note each conflict: downstream file, section, the stale claim (quote it), and what it should now say

**Classify the impact**:
- **None**: No downstream documents exist, or no conflicts found. Skip display entirely.
- **Minor** (1–2 small conflicts): Display conflicts to user inline.
- **Major** (3+ conflicts OR a foundational assumption changed — e.g., pricing model changed, primary channel shifted, launch timeline moved significantly): Display conflicts and strongly recommend `$reconcile-research`.

Display to the user after showing the written file confirmation. This should be quick — one read per downstream doc, scan for conflicts against key decisions. Not a deep reconciliation.

## Output

### `research/gtm.md` (or `research/{slug}/gtm.md`)

```markdown
# Go-to-Market Plan

> Based on: research/icp.md (or research/{slug}/icp.md)[, research/competitive-analysis.md, research/journey-map.md, research/customer-feedback.md]
> Date: [current date]

## Summary
[2-3 sentences: the core GTM thesis — who you're targeting, how you'll reach them, and what makes this approach viable]

## Channel Strategy

### Primary Channel: [channel name]
**Why**: [rationale grounded in ICP behavior and competitive gaps]
**How**: [specific tactics]
**Cost**: [budget/resource requirement]
**Timeline**: [when this ramps up]

### Secondary Channel: [channel name]
**Why**: [rationale]
**How**: [specific tactics]

### Channels Explicitly Deprioritized
[Channels considered and rejected, with reasoning — prevents revisiting]

## Messaging Framework

### One-Liner
[The sentence that makes the ICP lean in]

### Value Prop Framing
**Primary frame**: [save time / save money / reduce risk / unlock capability]
**Pain point addressed**: [from ICP pain map]
**Proof points**: [metrics, testimonials, demos]

### Positioning vs. Competitors
[How messaging differentiates from top 2-3 competitors]

## Pricing Strategy

### Model
[Freemium / free trial / paid-only / usage-based / seat-based]

### Entry Point
**Price**: [amount]
**Comparable**: [what the ICP currently pays for alternatives]
**Includes**: [what's in the base tier]

### Tiers (if applicable)
| Tier | Price | Target Segment | Key Differentiator |
|------|-------|----------------|-------------------|
| ... | ... | ... | ... |

### Upgrade Triggers
[What causes users to move up tiers]

## Launch Plan

### Timeline
[Soft launch → beta → public launch dates and goals]

### Launch Channel(s)
[Where and how — specific platforms and tactics]

### Launch Assets Needed
- [ ] [Asset 1]
- [ ] [Asset 2]

### First 10 Customers
[Who they are, how to reach them, why they'd say yes]

## Early Traction — 30/60/90 Days

### First 30 Days
[Manual, unscalable tactics — concierge onboarding, personal outreach]

### Days 30-60
[Start systematizing what works — templates, automation, repeatable processes]

### Days 60-90
[Scale what's working, drop what isn't — the metric that decides]

### The One Metric That Matters
[The single metric for the first 90 days, with target]

## Open Questions
[Decisions deferred, experiments to run, things that need real-world data]

<!-- Only include this section when downstream impact is Minor or Major. Omit entirely for None. -->
## Downstream Impact

> Checked: [list of downstream docs checked]
> Impact: Minor | Major

### Conflicts Found

1. **research/[file].md** — [Section Name]
   - **Stale**: "[exact quote from downstream doc]"
   - **Now**: [what this skill's output says instead]

[For Major only:]
> **Recommended action**: Run `$reconcile-research` to audit and fix all affected downstream documents.

## Next Steps

**Recommended:** `$skill` — [one-line reason]

Other options:
- [conditional items from step 4 — only include items whose conditions are met]
```

### `research/gtm-interview.md` (or `research/{slug}/gtm-interview.md`)
Raw interview log — questions, options presented, user responses, and a closing summary of key decisions.

Create the `research/` directory if it doesn't exist.

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- **Requires ICP.** Cannot build a GTM plan without knowing who you're selling to.
- **Ground in research.** Every channel, message, and pricing decision should trace back to ICP insights, competitive gaps, or customer feedback.
- **Be specific.** "Use social media" is not a channel strategy. "Post weekly technical deep-dives on Twitter targeting DevOps engineers who follow [competitor]" is.
- **Present before writing.** Never write output files until findings have been presented and validated.
- **Don't prescribe product changes.** GTM is about reaching and converting the market with what exists. Product gaps belong in `$mvp-gap` or `$brainstorm`.
- **Do not overwrite existing `research/gtm.md`** (or `research/{slug}/gtm.md`) without asking the user first.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/gtm-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
