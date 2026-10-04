---
name: cdev-status
description: Use when the user asks where a CDev-conditioned repository stands — progress of the active sprint (or a named one) measured on three axes, functional requirements, non-functional requirements and user stories — after several batches have run, before deciding what to run next, or when coming back to a repo. Also when the user invokes /cdev-status or asks "status of the sprint", "where are we", "how far along is this", "status funcional", "por dónde vamos", "qué llevamos del sprint".
---

# CDev Status

A read-only reading of **one** conditioned repository: how far the sprint's intent has been
walked, on three axes. **It edits no file and marks no state.** The single-repo counterpart of
`cdev-monorepo-status`, which applies this skill's method by reference — this file is the
method's single home.

Requires a conditioned repo (`docs/develop/` with `SPRINTS.md`, `AGENT_PROGRESS.md`, protocol).
Not conditioned → propose the `bootstrap` skill and stop; do not improvise a status.

## The idea

The plan holds no list of requirements or user stories, on purpose: a formalized list has to be
kept current while a feature is still being discovered, and that maintenance is what drifts.
The intent lives in free form — the sprint's objective, each batch's text and acceptance, the
decisions, the handoff. This skill engineers the three axes **at read time** from that raw
chain, and says where each item came from.

## Scope

- **No argument** → the `ACTIVE` sprint. None `ACTIVE` → say so, and read the most recently
  closed one.
- **A sprint named** → that sprint.
- **`all`** → one line per sprint (state, batches closed of N, the three percentages); full
  detail only for the `ACTIVE` one.
- **`since <batch|date|commit>`** → adds the delta (§ Delta).

## Read, in this order

1. Repo guide → local protocol (what "verified" means here).
2. `SPRINTS.md` — the sprint's objective; every batch: text, acceptance, state, dependencies.
3. `DECISIONS.md` — the entries about this sprint.
4. `AGENT_PROGRESS.md` — the entries of this sprint's batches: what was done, verification per
   check, blockers.
5. `git log` and `git status` — the commits carrying the sprint's units; work the plan does not
   know about.
6. Whatever the sprint or its batches reference — contracts, reports, a testing document where
   one exists.

Where a later record changes an earlier decision, the newest wins and is the one cited.

**Read narrowly — slices, never fewer sources.** Plans and handoff logs grow for months:
locate the sprint in scope and read that sprint, the decisions about it and the handoff
entries of its batches — not the whole files. Every source in the list above is still read;
what shrinks is how much of each. The reading is one pass by one reader, and its cost should
not grow with the age of the repository. Whatever you did not open, name in the method note.

## Engineer the three axes, in this order

1. **Functional requirements** — what the sprint's objective and its batches commit the system
   to *do*. One line each, in the plan's own terms.
2. **Non-functional requirements** — the qualities and constraints they commit the *system*
   to, wherever the plan, the decisions or the referenced documents state them. The
   repository's working rules — its verification sequence, branch convention, gates — are not
   requirements of the system: they tell you what "verified" means, they are never items.
3. **User stories** — built last, over the first two, against the sprint's objective. First
   person ("As a …, I …"), each marked **new** or **enriched** (a capability that already
   existed and this sprint extends).

Every item cites its source: the sprint objective, a batch, a dated decision, a handoff entry,
a file path.

State per item:

- **met** — every batch carrying it is `DONE` and its handoff entry records the verification;
- **met, unverified** — the batches are `DONE` but a check that covers it is recorded `not-run`;
- **partial** — an estimated percentage, the reason, and the batch that owns the rest;
- **pending** — the owning batch.

Percentages are **estimates**: **one figure per axis** over the sprint's total, one per partial
item. "Met, unverified" items count toward the axis figure; the executive reading says how much
of it rests on them. Say in the method note that the numbers are estimates; never present them
as measured, never give an axis two figures.

## Report

1. **Title** — sprint, date, batches closed X of N.
2. **Method note** — one paragraph: the items were derived at read time from the files read
   (name them); the percentages are estimates.
3. **§1 Functional requirements — ~NN%** — table `State | Requirement | Source`.
4. **§2 Non-functional requirements — ~NN%** — same table.
5. **§3 User stories — ~NN% · N complete · N partial · N empty** — three groups. Complete: the
   story and what proves it. Partial: percentage and reason. Empty: the owning batch.
6. **Executive reading** — batches closed, the three percentages, where the remaining work
   converges, live risks: blocked batches and the human decisions they wait on, verification
   recorded `not-run`.
7. **What is left to reach 100%** — numbered, by owning batch.

Keep it a reading, not an audit: one line per item, the executive reading in a handful of
lines. A disagreement is flagged once, where it bites, not re-argued in every section.

### Delta

With `since`, read `SPRINTS.md` and `AGENT_PROGRESS.md` as they were at that point
(`git show <rev>:<path>`; a batch resolves to the commit that closed it — a bare batch id
means the sprint in scope — and a date to the last commit before it). Apply the **same item
list** to both states, show "(before NN%)" beside each percentage and mark the items whose
state changed. No argument, no delta. Nothing is persisted between runs.

## Rules

- **Read-only, always.** If the conversation surfaces something that belongs in the plan,
  say it is the planner's job; do not write it.
- An axis the repository does not support reads **"not derivable"** and names what is
  missing. Never fill it from general knowledge of what such a product usually needs.
- Disagreement between plan, handoff and git is **flagged, never resolved**: a `DONE` whose
  entry records a check `not-run` reads "met, unverified"; commits belonging to no batch are
  listed as work the plan does not know.
- Answer in the language the human is using.
