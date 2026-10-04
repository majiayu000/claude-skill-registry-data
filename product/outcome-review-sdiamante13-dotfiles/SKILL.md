---
name: outcome-review
description: Post-launch review of a shipped PRD against the brief's success metrics. Did we move the metric? What did the data actually show? Which assumptions held, which broke? Which accepted-gap decisions resolved (confirmed vs. invalidated)? What would we do differently? Triggers on "outcome review", "did it work", "post-launch review", "did we move the metric", "retro the feature", "was it worth it". Produces a Confluence outcome-review page and updates the brief + linked decisions.
metadata:
  author: Fishbowl Team
  version: "0.1"
  tags: planning, product-management, outcome-review, retrospective
---

# Outcome Review — did it work?

## Prerequisites

- A PRD that has shipped (or reshaped) exists in Confluence.
- **jira plugin** (required); **Atlassian MCP** authorized.
- Ideally, access to whatever dashboards / data the brief's success metrics depend on.

Load references:

- [references/persona.md](../../references/persona.md)
- [references/cagan-methodology.md](../../references/cagan-methodology.md) — outcomes over output.
- [references/interview-tactics.md](../../references/interview-tactics.md)
- [references/artifact-templates/outcome-review.md](../../references/artifact-templates/outcome-review.md)
- [references/confluence-destinations.md](../../references/confluence-destinations.md)
- [references/decision-log.md](../../references/decision-log.md)

## Step 1 — Locate the PRD and brief

From `$ARGUMENTS`: PRD page ID or title. If none, CQL-survey the user's shipped PRDs:

```
creator = currentUser() AND label = "prd"
```

Filter client-side for `status = shipped` or `status = ready-for-tickets` (for PRDs where tickets are filed but the work hasn't been explicitly marked shipped). AskUserQuestion if multiple.

Read PRD → extract `brief_ref` + `linked_jira` + `linked_decisions`. Read the brief → extract the success metrics and the four-risks assumptions.

Fetch each linked Jira ticket's current status via `getJiraIssue`. Produce a short summary of which shipped and when.

## Step 2 — Session scratch

Seed `${CLAUDE_PLUGIN_DATA}/sessions/<session-id>/outcome-review.md` from template. Pre-fill the brief's success metrics and current Jira states.

## Step 3 — Interview

### Q1 — Metric movement

AskUserQuestion, based on the brief's primary success metric:

- "Yes — the metric moved in the intended direction and at roughly the expected magnitude"
- "Partially — some movement but below target, or in the right direction on a leading indicator without the lagging indicator following"
- "No — the metric did not move (or moved the wrong way)"
- "Too early — we don't have enough data yet"
- "Can't tell — the instrumentation / data is missing or noisy"

### Q2 — What the data shows

Open text. *"In specifics: what did you actually see?"* Push for numbers, not impressions. Push for *sources*: a dashboard link, a query result, a report.

If the answer is *"I haven't looked,"* note that as a follow-up item — this review is premature and should be rescheduled.

### Q3 — Assumptions: which held?

Walk through the brief's four-risks assumptions one by one. For each:

AskUserQuestion:
- "Held — the assumption turned out to be correct"
- "Broke — the assumption was wrong, and we can say in what way"
- "Untested — the feature didn't stress this assumption enough to know"

Open text follow-up: *"What happened? What did we learn?"*

### Q4 — Decisions: which resolved?

For each decision page in the PRD's `linked_decisions`:

Read the decision page → show the user the original `risk_accepted` text.

AskUserQuestion:
- "Confirmed — the risk we accepted did not cause problems (or the gap was closed in practice)"
- "Invalidated — the risk bit us, in the specific way described or differently"
- "Still pending — we can't tell yet"

Open text follow-up for the "what actually happened" detail.

These answers will update each decision page's `outcome` field in Step 6.

### Q5 — What would we do differently?

Open text. Look for concrete process or scoping lessons, not vague *"we should have done more research"* platitudes. Push for specifics: *"What specifically would you change about how you ran this?"*

### Q6 — What's the next step on this feature?

AskUserQuestion:
- "Ship as-is, monitor — done for now"
- "Iterate — plan V2 based on what we learned"
- "Reshape — the outcome suggests the solution should change materially"
- "Kill / roll back — the outcome doesn't justify the maintenance cost"
- "Too early — revisit in <X weeks>"

This becomes the `next_step` note at the bottom of the review.

## Step 4 — Summary + sentiment

Show the user the full review. Ask for edits. Sentiment + free-text prompt.

## Step 5 — Publish to Confluence

Default: PE › *Retrospectives* (ID 352157716), label `outcome-review`.

Resolve helper, render, `createConfluencePage`. No `draft` label (outcome reviews are one-shot artifacts — either published or not).

## Step 6 — Update linked artifacts

1. **Brief Page Properties:** set `status` to `shipped` (if reviewed) or `reshaped` / `killed` based on Q6. Add a link to the outcome review.
2. **PRD Page Properties:** same status update; add link to outcome review.
3. **Each decision page:** update `outcome` to match Q4 answer; add a link to the outcome review in its body.
4. **Jira tickets (if user confirmed):** optionally append a comment on each linked ticket pointing to the outcome review.

## Step 7 — Telemetry

Log session via MCP `updateConfluencePage` per [references/telemetry.md](../../references/telemetry.md). Skill = `outcome-review`, artifact_type = `outcome-review`.

One extra signal worth capturing: did this outcome review change the decision-log outcomes? If yes, that's a real data point for the spike-learnings doc — append an entry under the "Hook-acceptance feedback loop" dimension noting whether the decisions we forced to be recorded paid off.

## Never

- Never skip Q4 (decisions resolved). The whole point of the decision log is to close this loop.
- Never let Q1 "Yes" through without Q2 specifics. A yes without data is a wish.
- Never write an outcome review that simply says *"it shipped, everyone seems happy."* If the interview produces no specifics, that is itself the finding — record it and propose next steps to instrument the feature.
- Never silently downgrade an invalidated assumption. Flag it visibly so V2 planning sees it.