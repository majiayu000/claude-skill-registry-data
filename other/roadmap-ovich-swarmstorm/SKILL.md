---
name: roadmap
description: Use when a project has to be declared above its pieces of work, from nothing or from the boards, plans and prototypes already made, when a slot has landed or the picture has changed and the roadmap must be redrawn, or when someone asks where the project stands. Produces and keeps the roadmap (iterations of deliverable slots, each slot's state derived from what exists for it) and the foundation reference (the technology decisions). Not for designing a slot (brainstorm), planning it (write-plan) or building it (execute-plan).
---

# Roadmap

The **roadmap** is the one document above the pieces of work: what is delivered in what order, what exists for each piece, what must be decided before the next one starts.

- **A slot is something the customer can use or a system that can be deployed.** Nothing smaller: a screen, a service, a migration, a board are pieces of work under a slot.
- **A slot is done when the feature is delivered and working**, never when its last plan finished.
- **An iteration groups the slots delivered together.**
- **The first iteration of a project from scratch is usually one slot, the foundation**: the smallest deployable system the features build on, reachable at the product's own domain, its first piece of work the repository itself, created at the provider the foundation names with its conventions file, before any code.
- **No big design up front.** The next iteration has its slots named precisely; later iterations carry a title, the outcome and at most a rough list. A slot is split into its pieces of work, or a new piece opened for a brainstorm, when the work reaches it.

## The two documents

- **`YYYY-MM-DD-<project>.roadmap.md`, kind `roadmap`**, dated at declaration and kept for the life of the project.
- **`foundation.reference.md`, kind `reference`**, undated, never retiring: the technology decisions, one row each; tags project and `roadmap`.
- **Their contents and rows: `references/documents.md`**, read before drafting or redrawing either.
- **Both are registered and served via the `aiview` skill** in the product's group, the one its product-level boards and prototypes share, created and titled after the product when none exists, the roadmap started when the declaration began.
- **Documents in the project's folder that are not the product's are linked apart**, as not its slots.

## Slots and their state

- **Every document of a slot carries the slot's slug as a tag**, whatever group it sits in.
- **The state is derived from what the tag finds, never typed**: **empty** (nothing), **in design** (a board, or a plan not yet approved), **drawn** (prototypes), **planned** (an approved plan), **in progress** (a plan's tracker has a ▶), **landed** (the person confirmed the feature delivered and working, with the evidence: a URL, a deployment, a customer).
- **In the tracker only in progress is ▶ and only landed is ✅**; in design, drawn and planned stay ⬜ with the state written in the slot row.
- **At declaration the draft derives each state from the reading**, and the tags are applied when the interview confirms which slot a document serves.
- **A board serves a slot, or the roadmap itself when the idea is product-level**, and its tag says which.
- **The roadmap resolves its own decisions through the `interview` skill**, never through a board of its own, and keeps the exchange in its interview log: the question with its options and recommendation, then the answer as given.

## Declare

1. **Read everything that exists for the project**: its documents in aiview, its code and conventions file, any register the person names.
2. **Name what is missing**: slots no document covers (accounts and login, billing, the foundation itself are the usual absences), foundation rows no decision covers, dependencies between slots that nothing states.
3. **Draft both documents whole**, a recommendation in every open place with its reason, register and serve them, tell the person the URLs, and hand them over as something to correct.
4. **Interview on the draft.** The tree: the order of iterations, which slot each existing piece belongs to, the foundation rows the first slot needs. Rows a later slot needs stay open with that slot named. Every answer lands in the documents as it is given. For the name and domain rows, run `scripts/domains.mjs <name>... --tld <the TLDs the product needs>` on the person's suggestions before asking; each option carries its domains as available, registered or unknown, and a name whose domain is taken is never the recommended one.
5. **Close.** The state node names the first slot and its next step. Say so in chat.

## Redraw

**Run when a slot lands, a plan finishes, a board opens for a slot, or the person says the picture changed.**

- **Derive every state again.** Mark landed only with the person's evidence.
- **Split the slot the work has reached into its pieces of work**, each a group.
- **Ask the foundation rows the next slot needs and refuse to start it while one is open.**
- **Deviate from the earlier drawing when the last slot taught something**, and write what changed and why in the redraw log.
- **Retire the landed slot's groups** as the aiview contract asks.

## Status

**Read-only, in chat**: the iteration, the slot in progress, what blocks, the foundation rows still open for the slot ahead, the pieces of work the next slot still lacks.

## The diagram

**The roadmap opens on its tracker, drawn to the tracker protocol of the `write-plan` skill** (its `references/tracker.md`, the Slots section): one subgraph per iteration, one node per slot with the glyph of its derived state, dependency edges, the state node with the iteration, the slot in progress, next, blocked and the open rows. The coarse iterations share one subgraph, "later", their order carried by the edges alone. Parse it after every edit with `aiview mermaid-check`.

## Red flags

| Thought | Reality |
|---|---|
| "The stack can be decided when the first plan is written" | Then it is decided in one plan, and the second slot inherits it without seeing it. Rows close in the foundation, before the slot. |
