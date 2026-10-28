---
name: wayfinder
description: Plan work too big for one agent session as a map of decision tickets in markdown under .scratch/, then resolve them one per session, or all in one run, until the route to the destination is clear.
disable-model-invocation: true
argument-hint: "A loose idea, or an existing map under .scratch/; add `all` after a map to work every ticket in one run"
---

# Wayfinder

A loose idea has arrived: too big for one agent session, and wrapped in fog: the way from here to the **destination** isn't visible yet. Wayfinding finds that way instead of charging at the destination. Chart the way as a **shared map** of markdown files under `.scratch/`, then work its **decision tickets** (questions whose resolution is a decision, never work to build) one at a time until the route is clear.

One map produces **one spec**. When its decisions are clear, `to-spec` runs once and the map is finished. If the work is too big for a single spec, that is a sign the destination is drawn too wide: narrow it, and chart the rest as its own map later.

Naming the destination is the first act of charting; it shapes every ticket. It might be the spec to hand to `to-spec`, a decision to lock before planning starts, or the decisions behind a change made in place (a data-model migration, an expand–contract schema change): which still builds through the normal spec → tickets → build handoff.

Pipeline position: **`wayfinder`** (decide) → `to-spec` (write the spec) → `to-tickets` (break it into tickets) → `implement` (build one ticket per session).

## Plan, don't do

Each ticket resolves a **decision**; the map is done when nothing is left to decide before someone goes and does the thing. The pull to just do the work is usually the signal you've reached the edge of the map and it's time to hand off. The one sanctioned *do* on a map is a **task** ticket: manual work that unblocks a decision (see ticket types); it resolves like any other ticket and leaves no build state behind. Absent that, produce decisions, not deliverables.

**The test on every ticket: can it be answered, or must it be built?** Work you would build is not a ticket, it belongs in the spec. Never number build work onto the map. The map holds no build state, so a map carrying build work will keep telling you it is unfinished long after the work ships.

**Hand off: don't build.** When the decisions are clear, run `to-spec` once on the map. That closes the map. `implement` builds the spec's work from a ticket `to-tickets` wrote, never from the map, the lone exception being a `task` ticket, which is unblocking work rather than the spec's build.

## Refer by name

Every map and ticket has a **name**: its title. In everything the human reads, refer to it by that name with the path riding inside as a link, never a bare path alone. A wall of identifiers is illegible; names read at a glance.

## The Map

The map is the canonical wayfinding artifact under `.scratch/`. Its tickets are children of the map. The map is an **index**, not a store: it lists decisions made and points at the tickets that hold their detail; a decision lives in exactly one place, its ticket. Build work never appears here; that is the spec's job.

Maps, tickets, and specs are markdown files under `.scratch/`. Read the layout once per session from `.agents/issue-tracker.md` (written by `/setup`). If it's missing, try `docs/agents/issue-tracker.md` (legacy), then the `setup` skill's seed; suggest running `/setup` once to make the paths durable. Its **Wayfinding operations** are the single source of truth for creating maps and children, recording types, wiring blockers, claiming, querying the frontier, resolving, and linking assets.

Map body template, ticket body, claim/block/resolve mechanics: [references/map-and-tickets.md](references/map-and-tickets.md). Ticket types (research / prototype / grilling / task): [references/ticket-types.md](references/ticket-types.md). Fog of war and out-of-scope rules: [references/fog-and-scope.md](references/fog-and-scope.md). Load each when charting or resolving.

## Structured questions

Decision points that arise outside a full grilling: confirming the destination phrasing, choosing between scope rulings, picking which frontier ticket to work, use the question shape from `grilling` (via `AskUserQuestion` where available, otherwise a plain question in chat): recommended option first, real trade-offs per option, wait for the answer. Don't reinvent the protocol here, including its **Settle it yourself first** ladder and **What still earns a question** bar, which gate every question this skill asks and every ticket it charts. When this skill invokes `grilling` or `domain-modeling`, the inner skill does **not** print an end-of-session block, only the outermost skill does.

## Invocation

Two modes. Either way, **never resolve more than one ticket per session**: with the exception of research tickets, and of a **map run**.

### Chart the map

User invokes with a loose idea.

1. **Name the destination.** Run a `grilling` session (with `domain-modeling`) to pin down what this map is finding its way to. The destination fixes the scope, so it's settled first.
2. **Map the frontier.** Grill again, **breadth-first**: fan out across the whole space rather than deep on any thread, surfacing the open decisions and the first steps takeable now. **If this surfaces no unresolved decision tickets**, the destination is already clear enough to hand off and you don't need a map. An empty Not yet specified section alone is not enough, sharp open decisions still become tickets. Stop and ask the user whether to go straight to `to-spec` or `to-tickets`.
3. **Create the map** through the tracker's Create map operation: Destination and Notes filled in, Decisions so far empty, the fog sketched into Not yet specified.
4. **Create the tickets you can specify now** through the tracker's Create ticket operation, setting each ticket's `blocked-by` as you create it and wiring any remaining cross-edges in a **second pass**, so no ticket sits on the frontier before its blockers are wired. Everything you can't yet specify stays in the fog.
5. **Resolve eligible research tickets.** Follow the `research` skill's Wayfinder integration to claim, dispatch, persist, and resolve them. If a research ticket cannot finish during this charting session, leave it open on the frontier for its own session.
6. Stop: charting is one session's work; beyond the research tickets step 5 resolves, it hand-resolves nothing.

### Work through the map

User invokes with a map (its path or title). A ticket is optional, without one, you pick the next. With `all` after the map, this is a **map run**: read [references/map-run.md](references/map-run.md) first, it loops the steps below over the whole frontier.

1. Load the **map**: the low-res view, not every ticket body.
2. Choose the ticket. If the user named one, use it; otherwise take the first frontier ticket. **Claim it** through the tracker's Claim operation before any work.
3. Resolve it per its type: zoom as needed: fetch full bodies of related or closed tickets on demand; consult the skills the map's Notes name. If in doubt, grill.
4. Record the answer through the tracker's Resolve operation, which closes the ticket. The map's Decisions so far is derived from the closed, resolved tickets, don't hand-append it.
5. Add newly surfaced tickets (create-then-wire); graduate any fog the answer made specifiable, clearing each graduated patch from Not yet specified. If the answer reveals a ticket sits beyond the destination, use the tracker's Close operation to rule it out of scope (not Resolve, so it stays out of Decisions so far). Update tickets that remain valid; Close invalidated tickets as superseded with a short reason so their history remains intact.
6. **Say whether the map is clear.** It is clear when no ticket is open and nothing remains in Not yet specified. Say so plainly, because that is the signal to run `to-spec`: once.

The user may run unblocked tickets in parallel, so expect other sessions to be editing the tracker concurrently.

## When you're done

Print the end-of-session block using the frame in [`references/pipeline-end-block.md`](references/pipeline-end-block.md). Refer to the map and tickets **by name**, per **Refer by name** above. Query the markdown tracker for the current frontier before writing the block, don't guess at what's open.

```text
---
Pipeline: **decide** → spec → tickets → build   (1 of 4, multi-session map)
Done: <map name; tickets open, resolved, and still in the fog>
Next:
  • <condition> → /<skill> <map or ticket name>
```

Stage-specific **Next** conditions (only those that apply, most likely first):

**After charting:**

- **Map charted with a frontier** → `/clear`, then `/wayfinder <map>` to resolve the first frontier ticket; name it (research tickets already resolved point at their findings files). Offer `/wayfinder <map> all` beside it to work the whole map in one run
- **Charting found no unresolved decision tickets** → no map needed: `/to-spec`, or `/to-tickets` if the shape is already clear

**After working a ticket:**

- **Map still has open tickets** → `/clear`, then `/wayfinder <map>` for the next frontier ticket (or **resume your own claimed ticket first** if you stopped mid-ticket, see below); name it and say how many remain. Offer `/wayfinder <map> all` beside it for the rest
- **Map is clear** → `/to-spec <map>`, run once; that writes the spec and closes the map
- **Map is clear and the effort turned out genuinely small** → `/to-tickets <map>`, skipping the spec
- **Ticket blocked on someone else's knowledge** → `/to-questionnaire`; **on a fact worth reading for** → `/research`
- **Stopped mid-ticket** → say which ticket is claimed, what's decided so far, and that the claim remains active; resume that ticket next session before taking a fresh one, or Release it to hand it back to the frontier
