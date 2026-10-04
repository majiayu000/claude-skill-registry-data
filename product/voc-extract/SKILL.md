---
model_tier: inherit
name: voc-extract
description: "Use when extracting Voice-of-Customer themes from existing artefacts — GH issues, PR threads, Sentry patterns. Triggers on 'what are users saying', 'recurring complaints', 'top themes'."
status: active
tier: senior
domain: product
context_spine: [product]
recommended_for_user_types: [gtm, creator]
workspaces:
  - product
packs:
  - product-discovery
trust:
  level: professional
install:
  default: false
  removable: true
---

# voc-extract

## When to use

- A backlog or planning round needs grounded user-voice signal, not anecdotes.
- A round of bug reports / feature requests / Sentry events has accumulated and the team needs themes with citation per theme.
- A roadmap proposal needs a "what users keep telling us" backing section.

Do NOT use this skill for live interviews
([`discovery-interview`](../discovery-interview/SKILL.md)) or for
quantitative funnel diagnosis ([`funnel-analysis`](../funnel-analysis/SKILL.md)).

## Bounded scope

- **Read-only on artefacts the host already has** — local repo issues
  (`gh issue list`), PR discussions (`gh pr view`), Sentry projects
  the team owns. No external scrape, no SaaS API calls.
- **Chat-export sourcing (Discord, Slack) is deferred** pending
  privacy review (council Q5, SHIP-WITHOUT). If a request asks for
  chat-derived VoC, refuse and route the user to a privacy review.
- **No PII surfacing** — quotes are paraphrased to remove names,
  emails, tenant identifiers; verbatim is reserved for product-team
  artefacts inside the repo.

## Cognition cluster

- **Mental model 15 — Signal vs noise.** A loud single reporter
  swamps quiet recurring patterns; rank by **distinct authors**, not
  comment count. See
  [`docs/contracts/mental-models.md`](../../../docs/contracts/mental-models.md) § 15.
- **Mental model 14 — Pareto.** Roughly 20% of themes carry 80% of
  the contact volume; cut the long tail explicitly so the team acts
  on the head. See `mental-models.md` § 14.
- **Mental model 22 — Data-informed, not data-driven.** Issue counts
  are evidence, not voting; weight by recency, severity, and segment
  before recommending. See `mental-models.md` § 22.
- **Product context-spine slot.** Read **product** for segments,
  non-goals, and focal jobs; do not surface themes that fall outside
  the declared scope without a scope-violation flag. See
  [`context-spine`](../../../docs/contracts/context-spine.md).

## Procedure

### 1. Inventory the source artefacts

Identify what is in scope **for this run**:

- `gh issue list --state all --limit N` per repo.
- `gh pr list --state all --limit N` per repo.
- Sentry project names + date window.

Capture counts and date window in the output header so the verdict
is reproducible.

### 2. Inspect each artefact and tag

Per artefact, capture:

- **Theme tag** (free-text, normalised in step 3).
- **Author** (distinct identity).
- **Severity** — blocking / friction / wish / praise.
- **Segment** — derived from the **product** spine slot.
- **Citation** — `repo#123`, PR URL, Sentry issue ID.

### 3. Normalise and rank

Cluster theme tags into 5–12 themes max. For each:

- **Distinct-author count** (the rank key).
- **Severity mix** (blocking-share matters more than wish-share).
- **Recency** — last 90 days vs older; weight 2× recent.
- **Segment skew** — does the theme cluster in one segment?

Drop themes with `< 3` distinct authors **unless** severity is
blocking or the theme is brand-new in the recency window.

### 4. Build the theme report and validate

One row per theme. Columns: **theme · distinct authors · severity
mix · recency · segment skew · representative citations (≤ 3) ·
proposed next step (refine / probe / defer)**.

Validate the report before handing back: verify each row cites
≥ 1 artefact, check that distinct-author counts match the source
inventory from step 1, confirm no PII leaked into the citations,
and ensure no theme rated `defer` lacks a written rationale.

### 5. Surface scope violations

Themes that fall outside the **product** spine slot's declared scope
go into a `scope-violation.md` block, never silently into the main
report. The team decides whether to expand scope or close the door.

### 6. Hand back

Route refine candidates to [`refine-ticket`](../refine-ticket/SKILL.md);
route probe candidates (need live interview) to
[`discovery-interview`](../discovery-interview/SKILL.md); defer the
rest with explicit rationale.

## Related Skills

**WHEN to use this**

- The signal needs to come from existing repo / Sentry artefacts.
- The output is a theme list with citation, not narrative summary.
- A roadmap proposal needs grounded VoC backing.

**WHEN NOT to use this**

- The signal needs a live conversation — route to
  [`discovery-interview`](../discovery-interview/SKILL.md).
- The artefacts are chat-export sourced (Discord, Slack) — refuse
  and route to a privacy review (deferred per bounded scope).
- The output is a quantitative funnel — route to
  [`funnel-analysis`](../funnel-analysis/SKILL.md).
- A theme is already a ticket candidate — route directly to
  [`refine-ticket`](../refine-ticket/SKILL.md).

## When the agent should load this

- "Was sagen die User wirklich?"
- "Top-Themen aus den letzten 90 Tagen Issues."
- "Welche Sentry-Patterns sind recurring?"
- "Backe der Roadmap-Phase ein VoC-Block dazu."
- "Gibt es ein Segment, das uns überproportional pingt?"

## Output

1. **Header** — sources scanned, counts, date window, scope notes.
2. **Theme report table** — themes, distinct authors, severity mix,
   recency, segment skew, citations, next step.
3. **Scope-violation block** — themes outside the product spine
   slot, explicit, never collapsed into the main table.
4. **Routing list** — refine / probe / defer rows with the named
   downstream skill per theme.

## Gotcha

- One articulate user can own three themes; rank by distinct authors
  or you ship their backlog.
- A theme with no recency (all > 90 days) is archaeology, not VoC;
  flag it explicitly.
- Chat-export requests are tempting (Discord copy-paste); refuse
  per bounded scope until the privacy review lands.

## Do NOT

- Do NOT scrape external sources or hit SaaS APIs the team does not
  already own.
- Do NOT surface PII; paraphrase before quoting.
- Do NOT collapse scope-violations into the main table.
- Do NOT lock decisions inside this skill — hand off to
  `refine-ticket` or `decision-record`.
