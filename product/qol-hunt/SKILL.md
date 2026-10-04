---
name: qol-hunt
description: Hunt quality-of-life features for an app's day-to-day users, each grounded in friction observed in the codebase. Explicit invocation only.
disable-model-invocation: true
---

# QoL hunt

Find **quality-of-life** features for the people who use this app day to day: small friction-removals, sized S or M. An L-effort proposal needs one line justifying why it is still QoL rather than a headline feature.

The invocation text may name a **count** (default 5), a **scope** (a subtree or area; default the whole app), and whether to **write a report** (default chat only).

## Investigate

Identify the audience and the workflows relevant to the requested scope, using project docs and code as needed. For a whole-app hunt, survey the main user-facing areas before narrowing to promising workflows. Scale investigation depth to the scope and requested count.

Choose direct exploration or subagents based on the work. When delegating, give each agent the audience, relevant scope, and a request for observed friction, supporting file or route citations, and any candidate improvements. Use the **Friction** patterns below as leads.

Read the code behind promising workflows and check candidates against **Qualification**. Continue until the requested count qualifies or the promising areas within scope are exhausted.

Use git history when it helps identify areas worth investigating. Repeated fixes are leads; claims about usage frequency or brittleness need supporting evidence.

## Qualification

Each proposal must name a workflow with cited friction that you verify first-hand in the source, including proposals from subagents.

Check for duplicates in the app, prior `**/qol-hunt-*.md` reports, and accessible issue trackers or backlog docs. Exclude features that already exist, were proposed in a prior report, or have an open issue proposing or scheduling the fix. Issues reporting pain can support a proposal without disqualifying it.

If tracker access is unavailable or incomplete, proposals can still qualify. State the limitation and mark tracker duplication as unverified for affected proposals.

## Propose

Rank qualified proposals by expected impact relative to effort, considering workflow frequency and friction cost. Distinguish observed evidence from estimates of usage and impact, and state assumptions that materially affect the ranking.

Return fewer qualified proposals rather than fill the count with weak ones. Report any shortfall and the areas considered.

Open with one line stating your read of the audience, then per feature:

- **Workflow**, naming the route or module
- **Friction observed**, with file, route, or issue citations
- **Proposed change**
- **Effort**, S / M / L

Chat by default. On request, write to `docs/analysis/qol-hunt-YYYY-MM-DD.md`, or the repo's existing analysis convention.

## Friction

Observable patterns to look for:

- Multi-step flows that could be one step
- Re-entering data the app already holds
- Bulk work done one item at a time
- Actions with no feedback: silent saves, missing loading or error states
- Dead ends: the next obvious action is not offered where the user stands
- Forms without sensible defaults
- Data shown without the action that follows from it
