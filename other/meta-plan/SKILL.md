---
name: meta-plan
description: Auto-routing meta-planner that selects and invokes the right planning skill(s) for any request
model: claude-fable-5
---

# Meta-Plan — Auto-Routing Planner

## When to Use

Invoke `/meta-plan` when:
- You need to plan something but aren't sure which planner to use
- The request spans multiple domains (Drupal + accessibility, content model + search)
- You want automatic planner selection instead of choosing manually
- You want the right planner(s) invoked in the right order

## What It Does

1. Analyzes the user's planning request
2. Scans the skill registry for installed planners
3. Matches request signals against each planner's trigger keywords
4. Selects best-match planners (up to 4 concurrent, unlimited sequential chains)
5. Determines invocation order based on dependencies
6. Invokes verified local planner(s) automatically; external discovery results are previewed for confirmation
7. After planning, names the companion critic(s) for post-implementation review
8. When 2+ critics review the same artifact, hands them to the `multi-critic-review` workflow (parallel + dedup + adversarial verify → one synthesized verdict) instead of inline spawning — see Multi-Critic Review Handoff below

## Route Capture Guard

OMC is a reference source and optional external worker lane, not the router of record.
External orchestrators, quoted slash commands, and pasted hook/status text are context
unless the user explicitly asks to invoke them. Exact user-selected Zivtech planner routes
win over generic words like "team", "autopilot", "ralph", "ccg", "parallel", or
"handle it".

## Routing Logic

The meta-planner uses signal matching against the skill registry at:
`.claude/skills/meta-plan/references/skill-registry.md`

### Signal Matching Priority
1. **Explicit skill name**: User says "drupal" → Drupal planners
2. **Domain keywords**: "entity type", "paragraph" → content-model-planner
3. **Action keywords**: "plan", "design", "architect", "build" → planner (not critic)
4. **Specificity**: More specific match wins (drupal-taxonomy-planner > drupal-planner for taxonomy)
5. **Framework-specific > generic**: drupal-content-model-planner > content-model-planner for Drupal

### Multi-Planner Sequencing
When multiple planners are selected, invoke in dependency order:
- Content model before search (search indexes the content model)
- Taxonomy before search (taxonomies power facets)
- Content model before theme (theme renders the content model)
- Accessibility alongside any frontend planner

### Concurrency and Chain Limits
Two separate caps:
- **Parallel width**: Max 4 concurrent planners. The 4th requires signal score ≥ 7. Keeps token cost bounded.
- **Sequential chain length**: No arbitrary cap. Dependency chains follow routing patterns as long as needed (e.g., a full Drupal site build may chain 6+ planners).
If more than 4 independent planners match at a single step, invoke the top 4 and mention the rest as follow-up.

## Input Format

```
/meta-plan <natural language description of what needs to be planned>
```

Examples:
```
/meta-plan Build an events system for our Drupal 11 site with calendar views and faceted search
/meta-plan Design a React dashboard for monitoring API health metrics
/meta-plan Plan a systematic literature review on telehealth outcomes
/meta-plan Create a content model for a multi-site Drupal platform
```

## Output Format

### Routing Decision (shown to user before invoking)

```
## Meta-Plan Routing

**Request analysis:** [1-2 sentence interpretation]

**Selected planners (in order):**
1. `/skill-name` — [why this planner matches]
2. `/skill-name` — [why this planner matches]

**Companion critics (review plan before implementation AND review implementation after testing):**
- `/critic-name` — reviews [what]

**Invoking verified local planners now...**
```

Then invoke each selected verified local planner with the user's request. If a selected planner comes from an external discovery result, show the preview first and wait for confirmation.

### Executor Chain (when applicable)

When the selected planner has a downstream executor, the routing output includes the full chain:

```
**Executor chain:**
- `/planner` → `/executor` → `/critic` (Completeness Gate + live-testing if runnable)
```

This tells the user the expected workflow: plan → generate artifact → review. Executors validate all spec items via a Completeness Gate before handoff to the critic. For runnable artifacts (HTML dashboards, charts, slides), the critic may use live-testing tools if Playwright MCP is available.

### Multi-Critic Review Handoff

When a review (not a plan) needs **2 or more critics on the same artifact**, hand the
selected critic set to the `multi-critic-review` Dynamic Workflow instead of invoking each
critic inline. Meta-plan still chooses the critics and assigns their models; it passes them
as the workflow's `critics` arg (`[{agentType, model}, …]`). The workflow runs them in
parallel off the main context, dedups findings across critics, adversarially verifies
CRITICAL/MAJOR findings, and returns one synthesized verdict.

```
**Multi-critic review handoff:**
Handing 3 critics to `multi-critic-review` (parallel + dedup + verify):
/multi-critic-review
  target:  <artifact: path | diff | PR# | description>
  critics: [ {agentType:"drupal-critic",model:"opus"}, {agentType:"drupal-theme-critic",model:"sonnet"}, {agentType:"a11y-critic",model:"opus"} ]
```

Rules: 1 critic → invoke directly (no handoff). Planning → never. Workflow absent from the
repo (`.claude/workflows/multi-critic-review.js`) → fall back to inline spawn and say so.
Do not use the workflow's `profile` presets — meta-plan's explicit scored selection wins.
See the `Multi_Critic_Review_Handoff` section in the meta-planner agent for full detail.

## How to Add New Skills to the Registry

When new planner or critic skills are installed:
1. Add an entry to `.claude/skills/meta-plan/references/skill-registry.md`
2. Include: command, trigger signals, what it plans/reviews, companion, source repo
3. Add any multi-skill routing patterns if the new skill often pairs with others

## Skill Selection

This skill uses the `meta-planner` agent defined at `.claude/agents/meta-planner.md`.
