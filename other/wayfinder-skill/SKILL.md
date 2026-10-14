---
name: wayfinder-skill
description: >-
  Plan oversized work as a shared map of decision tickets on the issue
  tracker; resolve frontier tickets one at a time until the way is clear.
  Triggers: wayfinder, chart the map, work through the map, decision
  tickets, plan too big for one session.
license: MIT
compatibility: opencode
metadata:
  pattern: map-based-planning
category: Git/Workflow
---

Adapted from [mattpocock/skills](https://github.com/mattpocock/skills)
`skills/engineering/wayfinder` (MIT) for OpenCode — dependencies mapped to
local skills/subagents, tracker handling per house MCP policy.

A loose idea has arrived, too big for one agent session, wrapped in fog: the
way from here to the **destination** isn't visible yet. Wayfinding finds that
way instead of charging at the destination. This skill charts the way as a
**shared map** on the repo's issue tracker, then works its **decision
tickets** (questions whose resolution is a decision, not build slices) one at
a time until the route is clear.

The **destination** varies per effort, and naming it is the first act of
charting: a spec to hand off, a decision to lock before planning, or a change
made in place. The map is domain-agnostic.

## Plan, don't do

Wayfinder is **planning** by default: each ticket resolves a decision, and
the map is done when nothing is left to decide before someone does the thing.
The pull to just do the work is usually the signal you've reached the edge of
the map — hand off (e.g. to `ticketing-skill` for execution tickets,
then `/run-worktree-pipeline` to execute). An effort can override this in its
**Notes**, carrying execution into the map itself.

## Refer by name

Every map and ticket is an issue, so it has a **name**: its title. In
everything the human reads, refer to it by name, never a bare number. The id
and URL ride *inside* the name link, never stand in for it.

## The Map

The map is a single issue labelled `wayfinder:map` — the canonical artifact.
Its tickets are child issues. The map is an **index, not a store**: a
decision lives in exactly one place (its ticket); the map gists and links.

### Map body

```markdown
## Destination
<what reaching the end looks like — one or two lines; every session orients to it first>

## Notes
<domain; skills each session should consult; standing preferences>

## Decisions so far
- [<closed ticket title>](link): <one-line gist of the answer>

## Not yet specified
<fog: in-scope questions you can't phrase sharply enough to ticket yet>

## Out of scope
<work ruled beyond the destination; closed, never graduates>
```

### Tickets

Each ticket is a child issue; the tracker's issue id is its identity. Body:

```markdown
## Question
<the decision or investigation this ticket resolves>
```

Each carries a `wayfinder:<type>` label — `research`, `prototype`,
`grilling`, or `task` (below). A session **claims** a ticket by assigning it
to the driving dev **first**, before any work; that assignee *is* the claim.
Blocking uses the tracker's **native** dependency relationship (GitHub
task-list/blocked-by, tracker-native issue links) so the frontier renders visually in
the tracker UI; body-convention fallback only if the tracker lacks blocking.
A ticket is **unblocked** when all blockers are closed; the **frontier** is
the open, unblocked, unclaimed children. The answer is posted as a
resolution comment on close — not appended to the body. Assets created while
resolving are linked, not pasted.

## Ticket types

Every ticket is **HITL** (worked with a human) or **AFK** (agent alone). The
agent never stands in for the human's side of a HITL ticket.

- **research** (AFK): surface a fact a decision waits on. Delegate to
  `autoresearch-research-subagent` (web) or `explore` (local repo); load
  `search-first-skill` when unsure where to look.
- **prototype** (HITL): make a cheap, rough, concrete artifact to react to —
  outline, stub, or code. For UI shape questions load `wireframer-skill`;
  for logic, write the stub directly. Link it as an asset.
- **grilling** (HITL): conversation — the default case. Load
  `grilling-skill` (+ `domain-modeling-skill` when the question shapes a
  data model).
- **task** (HITL or AFK): manual work that unblocks a decision (provision
  access, move data). The one type that *does* rather than decides; resolved
  when done, the answer records facts later tickets depend on.

## Fog of war

The map is deliberately incomplete: don't chart what you can't see. Beyond
the live tickets lies the fog — decisions you can tell are coming but can't
pin down because they hang on open questions. Resolving a ticket clears fog
ahead of it, graduating what's now specifiable into fresh tickets. Write the
dim view in **Not yet specified**; it doubles as a signpost for
collaborators.

**Fog or ticket?** Ticket when you can state the question *precisely* now
(even if blocked); fog when you can't. Don't pre-slice fog into ticket-sized
pieces — one patch may graduate into several tickets, or none.

**Out of scope** is different: work ruled beyond the destination by *scope*,
not sharpness. It never graduates. When a live ticket turns out to sit past
the destination, close it and leave one line in **Out of scope** (gist + why
+ link). It stays out of **Decisions so far** — that records the route
walked, and a scope boundary isn't a step on it.

## Tracker routing

- **GitHub Issues** (default): `gh issue create/view/comment/close`,
  `--assignee @me` claims, task-list or `blocked-by: <ref>` body line for
  blocking.
- **Tracker tickets (e.g. JIRA)**: MCP Availability Guard policy per
  `ticketing-skill` §MCP Availability Guard; degrade to
  GitHub/local-markdown with a clear report when the tracker is unavailable.
- **No tracker / offline**: local-markdown fallback — `docs/wayfinder/<slug>/`
  with `MAP.md` + one file per ticket; assignment/blocking recorded in each
  file's front matter.

## Invocation

Two modes. Either way, **never resolve more than one ticket per session**,
except research tickets.

### Chart the map

User invokes with a loose idea.

1. **Name the destination** — load `grilling-skill` (+ `domain-modeling-skill`
   if it shapes a model) and pin down what this map is finding its way to.
   The destination fixes scope; settle it first.
2. **Map the frontier** — grill breadth-first: fan out across the whole
   space, surfacing open decisions and first takeable steps. If this
   surfaces no fog (the way is already clear, small enough for one session),
   you don't need a map — stop and ask the user how to proceed.
3. **Create the map** (`wayfinder:map` label): Destination and Notes filled,
   Decisions-so-far empty, fog sketched into Not yet specified.
4. **Create the tickets you can specify now** as child issues, then wire
   blocking edges in a **second pass** (issues need ids before referencing
   each other). Everything else stays in the fog.
5. **Fire research delegates** — for each `research` ticket, Task-delegate to
   `autoresearch-research-subagent` in parallel, findings linked as assets.
6. Stop: charting is one session's work; it hand-resolves nothing.

### Work through the map

User invokes with a map (URL or number); a ticket is optional — without one,
pick the next frontier ticket yourself.

1. Load the **map** — the low-res view, not every ticket body.
2. Choose the ticket (user-named, else first frontier in order). **Claim it**
   by assignment before any work.
3. Resolve it. Zoom into related/closed ticket bodies as needed; load the
   skills the `## Notes` block names (default: `grilling-skill` +
   `domain-modeling-skill`).
4. Record the resolution: post the answer as a **resolution comment**,
   **close** the issue, append a context pointer to the map's Decisions so
   far.
5. Add newly-surfaced tickets (create-then-wire); graduate fog the answer
   made specifiable, clearing each patch from **Not yet specified**. If a
   ticket now sits beyond the destination, rule it out of scope instead of
   resolving it. If the decision invalidates map parts, update or delete
   those tickets.

The user may run unblocked tickets in parallel — expect concurrent tracker
edits from other sessions.

## Return Contract

**Status:** success | partial | failed
**Output:** map link + tickets created/resolved this session
**Summary:** 2–3 sentences max
**Issues:** blockers, or "None"
