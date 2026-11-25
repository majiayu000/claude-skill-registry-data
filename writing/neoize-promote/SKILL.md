---
name: neoize-promote
description: Move a project's universal lessons UP into the shared neoize layer, so knowledge that holds for all work with Claude (git discipline, PR flow, verification, writing voice) stops being one project's secret and is read by every session. Product-specific knowledge (a symbol, a structural node, this product's domain) stays in the project and never travels.
when_to_use: The user wants a lesson to apply everywhere, not just here, asks to "promote this to shared", "make this universal", "move this to the shared KB", or is reconciling which lessons belong in the shared layer. Also used during the one-time migration of an existing KB into the shared model.
---

# neoize-promote

You are moving a lesson from a project's own space UP into the **shared** space. The shared space is the
universal layer: knowledge that holds for ALL work with Claude on this machine, read by every session on
top of whatever project it is in. Promotion is how a lesson learned in one product (how you verify a push
landed, how a PR is opened, how an article's voice works) becomes the baseline everywhere.

What may be promoted is the GENERIC half only: a lesson anchored to a Topic or an Operation. What never
goes to shared is product-specific: a lesson about this product's own symbols, files or structural nodes,
because that knowledge is meaningless in another codebase and its anchor would dangle (shared holds no
code). The tool enforces that line, so you never hand-filter the obviously unpromotable.

Promotion is a FILE operation and it MOVES, not copies: the lesson leaves this project's
`.neoize/lessons/*.json` and lands in `~/.neoize/shared/lessons/from-<product>.json`. Moving matters,
because a lesson present in both spaces would show up twice in the shared+project union every session
reads. The move is reversible through git in both the project and the shared store.

## The bar for shared is high

A wrong shared lesson pollutes every future session in every project, so promote only what is genuinely
universal. The test: would this be true and useful in a codebase that shares NONE of this product's stack,
domain or tooling? If it names a framework, a service, a ticket prefix, a domain entity or this product's
own convention, it is project knowledge, keep it where it is. When in doubt, do not promote.

## Driving neoize: call the tools, not a shell path

Every neoize operation runs as a **plugin MCP tool**. The map:

- `promote_lessons`: list this project's promotable lessons, or move chosen ones up to shared.
- `read_neo4j_cypher`: pull a lesson's body so the universality call is informed (scope reads with
  `WHERE n.product IN $products`, pre-bound).
- `check_lessons`: validate the shared store offline after the move.
- `load_shared` / `load_lessons`: load the shared space and re-load the project space.

The CLI equivalent is `neoize promote [--list | --lessons a,b,c] [--copy]`.

## Step 1 - list the candidates and read what matters

Call `promote_lessons` with `list: true`. It returns this project's promotable lessons (anchored to a
Topic or Operation); a lesson anchored only to this product's structure is not listed, so the obviously
project-specific is already gone. Pull a few bodies with `read_neo4j_cypher` so the call is informed: a
lesson can be generic in FORM (anchored to a Topic) yet specific in CONTENT ("our auth uses Keycloak" is a
Topic lesson that is false elsewhere). Form is necessary, not sufficient; universality is a judgement.

## Step 2 - decide, with the user when it is a close call

Present the candidates with their titles and a one-line gist, plus your read on each: universal or
project. Promote only the ones that pass the high bar above. For a close call, surface the body and let
the user decide, rather than promoting on a guess. The tool has already dropped anything anchored only to
structure, so what remains is a judgement about universality.

## Step 3 - promote (moves files, does NOT load yet)

Call `promote_lessons` with `lessons: [<chosen ids>]`. It removes them from this project's lessons files
and appends them to `~/.neoize/shared/lessons/from-<product>.json`, keeping only their Topic/Operation
anchors. A lesson already in the shared store is left alone, not duplicated. Nothing is loaded yet. Use
`copy: true` only for a deliberate reason (it leaves the project copy in place, so the lesson lives in both
spaces and doubles in the union, which you then have to resolve by hand).

## Step 4 - load both spaces and prove

- `check_lessons` on the shared store (`neoize check "$(neoize shared dir)/lessons"`).
- `load_shared` (with prune) so the shared store is the graph's shared space, then `load_lessons` (with
  prune) on this project so the moved lessons leave the project space. Running both with prune in one pass
  is what makes the move land cleanly on both sides.
- Confirm the union: a read of the promoted lesson's Topic or Operation now returns it under
  `product = 'shared'` and no longer under this project's product.

## Finish

Report: which lessons were candidates, which you promoted and why each is universal, which you kept in the
project and why, the files changed in both the project and the shared store, then the load result for both
spaces. If you used `copy`, say so and name what still needs reconciling.
