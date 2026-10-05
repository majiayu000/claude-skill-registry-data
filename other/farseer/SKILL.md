---
name: farseer
description: Plan a new project or a chunk of work too big for one agent session as a shared map of decision tickets on your issue tracker, then resolve them one at a time until the path to the destination is clear.
disable-model-invocation: true
---

# Farseer Skill

A loose idea has arrived. It's too big for one agent session, and the way from here to the destination isn't visible yet. Farseer finds that way instead of charging ahead towards the destination. It charts the way as a **shared map** on the repo's issue tracker, then works the map's **decision tickets** one at a time until the route is clear. A decision ticket is a question whose resolution is a decision. It is never a slice of a build to execute.

The destination differs per effort, and naming it is the first act of charting because it shapes every ticket. It might be a spec to hand off and iterate on, a decision to lock-in before planning starts, or a change made in place, like a data-structure migration. The map is domain-agnostic. Engineering work and course content both fit.

## Plan, Don't Do

Farseer plans by default. Each ticket resolves a decision, and the map is done when nothing is left to decide before someone goes and does the thing. When you feel the pull to just do the work, you've usually reached the edge of the map and it's time to hand off. An effort can override this in its notes and carry execution into the map itself. Absent that, produce decisions, not deliverables.

## Refer by Name

Every map and ticket is an issue, so it has a name, its title. Use that name everywhere the human reads, in narration and in the map's decisions-so-far. Never use a bare ID, number, or slug. A wall of `#42, #43, #44` is illegible. Names read at a glance. The ID and URL don't vanish. The name wraps its link, so they ride _inside_ the name instead of standing in for it.

## The Map

The map is one issue on the repo's issue tracker, labeled `farseer:map`. It is the record of the effort. Its tickets are child issues of the map.

The map is an **index**, not a store. It lists the decisions made and points at the tickets that hold their detail. A decision lives in exactly one place, its ticket. The map explains the gist and links to it, never restates it.

Where the map, its child tickets, blocking, and frontier queries live depends on the tracker. The issue tracker should have been provided to you. If it wasn't, tell the user to run `/farseer:repo-setup`. Consult the tracker doc's "Farseer Operations" section for how _this_ repo expresses them. If no tracker has been provided, default to the local-markdown tracker.

### The Map Body

The whole map at low resolution, loaded once per session. Open tickets are **not** listed. They are open child issues, found by query.

```markdown
## Destination

<what reaching the end of this map looks like: the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<domain; skills every session should consult; standing preferences for this effort>

## Decisions So Far

<!-- the index: one line per closed ticket, enough to judge relevance, then zoom the link for the detail the ticket holds -->

- [<closed ticket title>](link): <one-line gist of the answer>

## Not Yet Specified

<!-- see "Fog of war": in-scope fog you can't ticket yet; graduates as the frontier advances -->

## Out of Scope

<!-- see "Out of scope": work ruled beyond the destination; closed, never graduates -->
```

### Tickets

Each ticket is a child issue of the map, and the tracker's issue ID is its identity. Its body is the question, sized to fit one 100K-token agent session:

```markdown
## Question

<the decision or investigation this ticket resolves>
```

Each ticket carries a `farseer:<type>` label, one of `research`, `prototype`, `interviewing`, or `task` (see [Ticket Types](#ticket-types)).

A session claims a ticket by assigning it to the developer driving the map. Do this first, before any work, so concurrent sessions skip it. The assignee is the claim. An open, unassigned ticket is unclaimed.

Blocking uses the tracker's native dependency relationship. That matters because it renders the frontier in the tracker's own UI, so the human sees what's takeable without opening the map. Only a tracker with no native blocking falls back to a body convention. A ticket is unblocked when every ticket blocking it is closed. The frontier is the set of open, unblocked, unclaimed children.

The answer isn't part of the body. It's recorded on resolution (see [Work Through the Map](#work-through-the-map)). Link assets created while resolving a ticket from the issue rather than pasting them in.

## Ticket Types

Every ticket is either HITL (human in the loop, worked with a human who speaks for themselves) or AFK, driven by the agent alone. A HITL ticket only resolves through that live exchange. The agent never stands in for the human's side of it. An interviewing agent that answers its own questions has broken this.

- **Research** (AFK). Read documentation, third-party APIs, or local resources like knowledge bases to surface a fact a decision waits on. A subagent resolves it by calling the Skill tool with `research`. Use it when the answer lives outside the current working directory.
- **Prototype** (HITL). Raise the fidelity of the discussion with a cheap, rough, concrete artifact to react to. That might be an outline, a stub, or UI or logic code. Make it by calling the Skill tool with `prototype`, and link the prototype as an asset. Use it when "how should it look" or "how should it behave" is the key question.
- **Interviewing** (HITL). Conversation. This is the default case. Always call the Skill tool twice, for `interviewer` and `domain-modeling`.
- **Task** (HITL or AFK). Manual work that must happen before a decision can be made. There is nothing to decide, prototype, or research, but the discussion is stuck until it's done. Examples are signing up for a service so its API can be judged, provisioning access, or moving data so its shape can be seen. This is the one type that does rather than decides, and it earns its place by unblocking a decision, not by delivering the destination. The agent drives it alone where it can (AFK). Otherwise it hands the human a precise checklist (HITL). It resolves when the work is done. The answer records what was done and any facts later tickets depend on, such as where credentials live, new URLs, or row counts.

## Fog of Uncertainty

The map is deliberately incomplete. Don't chart what you can't yet see. Beyond the live tickets lies the fog of uncertainty, the dim view of decisions and investigations you can tell are coming but can't yet pin down, because they hang on questions still open. Resolving a ticket clears the fog ahead of it. Whatever is now specifiable graduates into fresh tickets, one at a time, until the way to the destination is clear and no tickets remain.

The map's Not Yet Specified section is where that dim view is written down, as the suspected question or the area to revisit later. Everything here is in scope, just not sharp enough to ticket. Write as loosely or as fully as the view allows. It doubles as a signpost for collaborators reading where the effort is headed.

**Fog of uncertainty or ticket?** The test is whether you can state the question precisely now, not whether you can answer it now.

- **Ticket** when the question is already sharp, even if it's blocked and you can't act on it yet.
- **Not Yet Specified** when you can't yet phrase it that sharply. Don't pre-slice the fog into ticket-sized pieces. It's coarser than a ticket, and one patch may graduate into several tickets, or none, once the frontier reaches it.

Not Yet Specified excludes what's already decided (Decisions So Far), what's already a live ticket, and what's out of scope (the next section).

## Out of scope

Fog only ever gathers toward the destination. The destination fixes the scope, so work beyond it is out of scope. It isn't fog, and it doesn't belong in Not Yet Specified. It gets its own Out of Scope section on the map, for work you've consciously ruled out of this effort. Scope, not sharpness, lands it here.

Out-of-scope work never graduates, because the frontier stops at the destination. It returns only if the destination is redrawn, and then as a fresh effort, not a resumption.

Ruling something out of scope is a scoping act, not a step on the route. Sometimes an existing ticket turns out to sit past the destination, either mis-scoped in while charting or exposed by a resolution. Close it, since a closed ticket is unambiguously off the frontier, and leave one line in the Out of Scope section with the gist, why it's out of scope, and a link to the closed ticket. It stays out of Decisions so far, which records the route actually walked. A scope boundary isn't a step on it.

## Invocation

Two modes. Either way, never resolve more than one ticket per session. Research tickets are the exception.

### Chart the map

The user invokes with a loose idea.

1. **Name the destination.** Call the Skill tool twice, for "interviewer" and "domain-modeling", to pin down what this map is finding its way to. That's the spec, decision, or change. The destination fixes the scope, so settle it first.
2. **Map the frontier.** Interview again, breadth-first this time. Fan out across the whole space rather than deep on any one thread, surfacing the open decisions and the first steps takeable now. If this surfaces no fog, the way to the destination is already clear and the whole journey fits in one session. You don't need a map. Stop and ask the user how they'd like to proceed.
3. **Create the map** with the label `farseer:map`. Fill in Destination and Notes, leave Decisions So Far empty, and sketch the fog into Not Yet Specified.
4. **Create the tickets you can specify now** as child issues of the map. Then wire blocking edges in a second pass, since issues need IDs before they can reference each other. Wiring sorts them into the frontier and the blocked. Everything you can't yet specify stays in Not Yet Specified.
5. **Fire the research subagents.** For each `research` ticket you just created, spin up a subagent that calls the Skill tool with `research` to resolve it in parallel. It captures its findings on a throwaway `research/<name>` branch with a context pointer from the ticket.
6. **Stop.** Charting is one session's work. It hand-resolves nothing.

### Work Through the Map

The user invokes with a map (URL or number). A ticket is optional. Without one, you pick the next decision, not the user.

1. Load the map. This is the low-res view, not every ticket body.
2. Choose the ticket. If the user named one, use it. Otherwise take the first frontier ticket in order. Claim it by assigning it to yourself before any work.
3. Resolve it. Zoom as needed by fetching the full body of any related or closed ticket on demand. Call the Skill tool for whichever skills the Notes block names. If in doubt, call the Skill tool twice, for `interviewer` and `domain-modeling`.
4. Record the resolution. Post the answer as a resolution comment, close the issue, and append a context pointer to the map's Decisions So Far.
5. Add newly surfaced tickets, create-then-wire. Graduate any fog the answer has made specifiable, clearing each graduated patch from Not Yet Specified so it lives only as its new ticket. If the answer reveals that a ticket, this one or another, sits beyond the destination, rule it out of scope rather than resolving it on the route. If the decision invalidates other parts of the map, update or delete those tickets.

The user may run unblocked tickets in parallel, so expect other sessions to be editing the tracker concurrently.
