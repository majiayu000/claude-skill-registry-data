---
name: to-epic
description: Frame a cross-repo effort as an Epic — the r3call table-of-contents issue that indexes the per-repo Specs, fixes the cross-repo Contract, and wires the sub-issue/dependency graph. Run before /to-spec when work spans repos. (r3call)
disable-model-invocation: true
---

# To Epic

Frame a cross-repo effort as an **Epic** — the r3call table-of-contents issue that indexes the per-repo Specs of one ratified Decision, fixes the **Contract** between repos, and wires the sub-issue/dependency graph. Run this before `/to-spec` when — and only when — work spans repos. Single-repo work goes straight to `/to-spec`.

Do NOT interview the user for the goal — synthesize the ratified Decision you are already working from. The repo split and the Contract are **recommendations**; Atila ratifies them at the quiz gate before anything publishes.

The issue tracker vocabulary and the wayfinding operations (the sub-issue and dependency `gh api` calls) live in r3call's `docs/agents/issue-tracker.md` — call the Skill tool with `setup-matt-pocock-skills` in r3call if they are missing.

## Process

### 1. Anchor to the ratified Decision

An Epic implements a Decision that is already **Fact** — an ADR in `docs/adr/`, or a `CONTEXT.md` entry. Cite it; this is the Epic's trace to Fact. If the effort has no ratified Decision behind it, stop: it is still Deliberation. Take it to `/grill-with-docs` first.

### 2. Map the repos in scope

Name every code repo the effort touches and what part of the effort each owns. Prefer the fewest repos that deliver the goal. If one repo carries the whole change, stop and use `/to-spec` — there is no Epic to author.

### 3. Settle the Contract

The load-bearing step. Fix, early and in one place, the cross-repo surface each Spec will build against:

- interfaces and payloads that cross a repo boundary
- shared identifiers, event names, and schema owned jointly
- the sequence in which repos must land — who ships first, and what they expose

The Contract is what lets the per-repo Specs be written and worked in parallel without drifting. Write it as prose plus the minimal shapes (types, payloads) that pin a decision precisely. Avoid file paths — they go stale fast.

### 4. Quiz the user — the ratification gate

Present the repo split, the Contract, and the proposed sequencing as a numbered recommendation. Ask:

- Are these the right repos — any missing, any that should not be here?
- Is the Contract complete and correct at every boundary?
- Is the sequencing right — does each edge reflect a genuine dependency?

Iterate until Atila ratifies. Nothing publishes before ratification.

### 5. Open the Epic issue in r3call

Publish the Epic to r3call's issue tracker using the template below. Open the body with the model-identity prefix r3call requires (`**Name (model-id)** — `). The Epic is a table of contents plus reasoning — it does NOT get the `ready-for-agent` label, and you never implement from it directly.

### 6. Author the Specs and wire the graph

For each repo in scope, in Contract sequence:

- run `/to-spec` in that repo to publish its Spec — one Spec per repo, each referencing the Epic as its parent;
- attach the Spec to the Epic as a native cross-repo **sub-issue**;
- add a native **blocked_by** edge for every Contract dependency, so the Epic surfaces the live gate.

Use the sub-issue and dependency `gh api` calls from r3call's `docs/agents/issue-tracker.md` → "Wayfinding operations" — the single source for the exact endpoints and the database-id gotcha. Work the **frontier**: author a repo's Spec once the repos it depends on are settled.

Done when every repo in scope has a Spec attached as a sub-issue and every cross-repo dependency is a native `blocked_by` edge. Do NOT modify the source Decision or ADR.

<epic-template>

## Goal

What the cross-repo effort achieves, from the ecosystem's perspective — one paragraph.

## Decision

A link to the ratified ADR (`docs/adr/…`) or `CONTEXT.md` entry this Epic implements. The Epic's trace to Fact.

## Repos in scope

One line per code repo, naming what part of the effort it owns.

## Contract

The cross-repo interfaces, payloads, sequencing, and shared identifiers — fixed here so each Spec builds against a stable surface. Include the minimal shapes that pin a decision; avoid file paths.

## Specs

The table of contents — one row per repo, linked as a sub-issue once created:

- [ ] `<repo>` — `<spec issue link>` — <one-line what & why>

## Sequencing

The cross-repo order as blocking edges: `<repo A spec>` blocks `<repo B spec>` because <reason>.

## Out of scope

What this Epic explicitly does not cover.

</epic-template>
