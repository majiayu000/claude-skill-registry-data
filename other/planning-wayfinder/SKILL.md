---
name: planning-wayfinder
description: Use when an effort is too large or too unclear for one agent session and must be charted as a map of decision items, then resolved one decision per session until the way to a named destination is clear.
license: MIT
---

# Planning Wayfinder

## Purpose

Plan an effort that no single session can hold. Name the **destination** (a spec, a locked decision, or a change such as a data migration), chart a **map** of the decisions between here and there, and resolve them one at a time. Wayfinding produces decisions, not deliverables: when the pull to start building appears, the map has reached its edge and it is time to hand off to `planning-spec` or `planning-tickets`.

## Activate when

- a loose idea is too big for one session, such as "move billing to its own engine" or "support multiple currencies"
- several unknowns block each other and the order to resolve them is unclear
- the user brings back a map to continue

## Repository inspection

- read the glossary and decision records, so the map does not reopen settled decisions;
- inspect the areas the destination touches, enough to see which questions are real;
- resolve the tracker backend with `planning-tracker`.

## Decision rules

### The map

The map is one `kind: map` item. It is an index, not a store: each decision lives in its own item, and the map only gists and links it. Its body:

```markdown
## Destination
One or two lines: what reaching the end of this map looks like.

## Notes
Domain, skills every session should load, and standing preferences.

## Decisions so far
- [Decide the refund ledger entry](link): one entry per tax line.

## Not yet specified
Questions you can see coming but cannot yet phrase precisely.

## Out of scope
- [Closed item](link): why it is beyond the destination.
```

### Decision items

Each decision is a `kind: decision` child of the map. Its body is the question, sized to one session. Label it with its type:

- `research` (agent alone): gather a fact from documentation, source code, or the resolved Rails version. Record sources with each claim.
- `interview` (with the user): settle a decision through `planning-interview`. The agent never answers the user's side.
- `prototype` (with the user): build a throwaway artifact to react to, such as a runner script or a scratch migration on a branch, and link it.
- `task` (either): work that must happen before a decision can be made, such as getting access or measuring data volume. Record what was done and the facts later decisions need.

**Question or fog?** Create a decision item when you can state its question precisely now, even if it is blocked. Leave it in `Not yet specified` when you cannot.

### Charting a new map

1. Name the destination with `planning-interview`; it fixes the scope.
2. Interview breadth-first across the whole space to find the open decisions and the first ones takeable now. If there is no fog, because the path is clear and small, stop: no map is needed, so go to `planning-spec`.
3. Create the map, then the decision items you can state, then wire blocking edges in a second pass.
4. Stop. Charting is one session's work.

### Working the map

1. Load the map, not every item body.
2. Take the named decision, or the first item on the frontier, and claim it.
3. Resolve it, loading related items and the skills the map's Notes name.
4. Record the answer as a comment, close the item, and add one line to `Decisions so far`.
5. Create newly visible decisions, move anything now statable out of `Not yet specified`, and close items that turn out to be beyond the destination, listing them under `Out of scope`.

Resolve at most one decision per session. The exception is research, which may run in parallel.

## Critical invariants

- One decision per session; research is the only exception.
- The map indexes decisions and never restates them; each answer lives in its item.
- Out-of-scope work is closed and listed, never parked in `Not yet specified`.
- Claim an item before working on it; other sessions may be working the same map.

## Reference example

```text
Map: Multiple currencies for invoices
Destination: a spec for invoicing in the customer's currency with correct ledger totals.

Frontier:
  Decide where the exchange rate is fixed (at issue or at payment)   interview
  Find which payment provider APIs accept non-USD amounts           research
Blocked:
  Decide the ledger's reporting currency       blocked by: exchange-rate decision
Not yet specified:
  How existing USD invoices are presented after the change.
Out of scope:
  Multi-currency payouts to suppliers (a separate effort).
```

## Agent review checklist

- [ ] destination named before any decision items
- [ ] every decision item states a precise question and carries a type
- [ ] fog kept in `Not yet specified`, not pre-sliced into items
- [ ] one decision resolved this session (plus any research)
- [ ] answer recorded, item closed, map updated with one line and a link
- [ ] out-of-scope items closed and listed

## Failure modes

- building the destination inside the map instead of deciding the way to it
- slicing fog into vague items that nobody can resolve
- restating decisions in the map, so the map and items disagree
- resolving several interview decisions in one session and answering for the user
- leaving an item open after it proved out of scope

## Verification

After each session, the map's `Decisions so far` matches the closed decision items, and the frontier (for local Markdown, `ruby scripts/tracker.rb frontier --root <root> --parent <map id>` from the `planning-tracker` skill) lists the next takeable decisions.

## Source foundation

Adapted, in this repository's words, from the `wayfinder` skill in https://github.com/mattpocock/skills (MIT License, Copyright (c) 2026 Matt Pocock). Tracker operations go through this repository's backend-neutral `planning-tracker`; interviews go through `planning-interview`.
