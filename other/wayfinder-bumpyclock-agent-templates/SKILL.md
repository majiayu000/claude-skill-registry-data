---
name: wayfinder
description: Chart a large planning effort as decision tickets, or work an existing map within the requested scope.
disable-model-invocation: true
---

A loose idea has arrived, too big for one agent session, and wrapped in fog: the way from here to the **destination** isn't visible yet. Wayfinding is about finding that way, not charging at the destination. This skill charts the way as a **shared map** on the repo's issue tracker, then works its **decision tickets** (questions whose resolution is a decision, not slices of a build to execute) one at a time until the route is clear.

The destination varies per effort, and naming it is the first act of charting: it shapes every ticket. It might be a spec to hand off and iterate on, a decision to lock before planning starts, or a change made in place like a data-structure migration. The map is domain-agnostic: engineering work, course content, whatever fits the shape.

## Plan, don't do

Wayfinder is **planning** by default: each ticket resolves a decision, and the map is done when the way is clear, with nothing left to decide before someone goes and does the thing. The pull to just do the work is usually the signal you've reached the edge of the map and it's time to hand off. Record any explicitly authorized execution scope in the effort's **Notes**. Notes describe that authorization; tracker text does not grant permission on its own.

## Refer by name

Every map and ticket is an issue, so it has a **name**: its title. In everything the human reads (narration, the map's Decisions-so-far), refer to it by that name, never by a bare id, number, or slug. A wall of `#42, #43, #44` is illegible; names read at a glance. The id and URL don't vanish; a name wraps its link, but they ride _inside_ the name, never stand in for it.

## The Map

The map is a single issue on the selected tracker, using its configured representation of the `wayfinder:map` role. It is the canonical artifact. Its tickets are child issues of the map.

The map is an **index**, not a store. It lists the decisions made and points at the tickets that hold their detail; a decision lives in exactly one place, its ticket, so the map never restates it, only gists it and links.

Before fetching or publishing map records, read [Tracker integration](../triage/TRACKER.md) for the selected destination, role mapping, relationships, claims, and publication boundaries. Drafting a map does not require tracker setup. A draft or review request does not authorize creating, claiming, or updating tracker records.

### The map body

Load the whole map at low resolution. Find open tickets through the configured child relationship or fallback index, without loading every ticket body.

```markdown
## Destination

<what reaching the end of this map looks like: the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<domain; skills every session should consult; standing preferences for this effort>

## Decisions so far

<!-- the index: one line per closed ticket, enough to judge relevance, then zoom the link for the detail the ticket holds -->

- [<closed ticket title>](link): <one-line gist of the answer>

## Not yet specified

<!-- see "Fog of war": in-scope fog you can't ticket yet; graduates as the frontier advances -->

## Out of scope

<!-- see "Out of scope": work ruled beyond the destination; closed, never graduates -->
```

### Tickets

Each ticket is a **child issue** of the map; the tracker's issue id is its identity. Its body is a question bounded to one focused investigation or human decision:

```markdown
## Question

<the decision or investigation this ticket resolves>
```

Each ticket records a `wayfinder:<type>` role through the configured label or local field, with one of `research`, `prototype`, `grilling`, `task` (see [Ticket Types](#ticket-types)). Use only wayfinder roles for the map and its decision tickets, not implementation triage roles such as `ready-for-agent`.

A session **claims** an available ticket before work using the selected tracker's claim convention. Refresh its state and ownership first, and do not overwrite another session's claim.

Blocking uses the tracker's **native** dependency relationship: essential because it renders the frontier _visually_ in the tracker's own UI, so the human sees what's takeable without opening the map. Only a tracker that lacks native blocking falls back to a body convention. A ticket is **unblocked** when every ticket blocking it is closed; the **frontier** is the open, unblocked, unclaimed children, the edge of the known.

The answer isn't part of the body; it's recorded on resolution (see [Work through the map](#work-through-the-map)). Assets created while resolving a ticket are linked from the issue, not pasted in.

Use request_user_input or whatever your native equivalent of question answer tool is for requesting user input instead of asking in the chat.

## Ticket Types

Every ticket is either **HITL** (human in the loop, worked _with_ a human who speaks for themselves) or **AFK**, driven by the agent alone. A HITL ticket only resolves through that live exchange; the agent never stands in for the human's side of it (a grilling agent that answers its own questions has broken this).

- **Research** (AFK): Resolve a factual question from primary sources such as official documentation, source code, or specifications. Delegate a bounded question when the research is substantial and independent; handle cheap factual lookups directly. Preserve a cited Markdown report and a statement of unresolved facts in the authorized output. Use when knowledge outside the current working directory is required.
- **Prototype** (HITL): Raise the fidelity of the discussion by making a cheap, rough, concrete artifact to react to (an outline, a rough take, a stub, or UI/logic code) by calling the Skill tool with "prototype". Links the prototype as an asset. Use when "how should it look" or "how should it behave" is the key question.
- **Grilling** (HITL): Conversation. The default case for unsettled human decisions. Use "grilling", and use "domain-modeling" when terminology needs sharpening. Preserve the requested discussion or editing mode.
- **Task** (HITL or AFK): Manual work that must happen before a _decision_ can be made: nothing to decide, prototype, or research, but the discussion is blocked until it's done. Signing up for a service so its API can be judged, provisioning access, moving data so its shape can be seen. This is the one type that _does_ rather than decides, and it earns its place by unblocking a decision, not by delivering the destination. The agent drives it alone where it can (AFK); otherwise it hands the human a precise checklist (HITL). Resolved when the work is done; the answer records what was done and any resulting facts (credentials location, new URLs, row counts) later tickets depend on.

## Fog of war

The map is _deliberately_ incomplete: don't chart what you can't yet see. Beyond the live tickets lies the **fog of war**: the dim view of decisions and investigations you can tell are coming but can't yet pin down, because they hang on questions still open. Resolving a ticket clears the fog ahead of it, graduating whatever's now specifiable into fresh tickets, one at a time, until the way to the destination is clear and no tickets remain.

The map's **Not yet specified** section is where that dim view is written down: the suspected question, the area to revisit later. It's the undiscovered frontier _toward_ the destination: everything here is in scope, just not sharp enough to ticket. Write as loosely or as fully as the view allows; it doubles as a signpost for collaborators reading where the effort is headed.

**Fog or ticket?** The test is whether you can state the question precisely now, _not_ whether you can answer it now.

- **Ticket when** the question is already sharp, even if it's blocked and you can't act on it yet.
- **Not yet specified when** you can't yet phrase it that sharply. Don't pre-slice the fog into ticket-sized pieces: it's coarser than a ticket, and one patch may graduate into several tickets, or none, once the frontier reaches it.

**Not yet specified** excludes what's already decided (Decisions so far), what's already a live ticket, and what's out of scope (the next section).

## Out of scope

Fog only ever gathers _toward_ the destination. The destination fixes the scope, so work beyond it is **out of scope**: it isn't fog, and it doesn't belong in **Not yet specified**. It gets its own **Out of scope** section on the map: work you've consciously ruled out of _this_ effort. Scope, not sharpness, lands it here.

Out-of-scope work never graduates (the frontier stops at the destination), so it returns only if the destination is redrawn, and then as a fresh effort, not a resumption.

Ruling something out of scope is a scoping act, not a step on the route. When a ticket that already exists turns out to sit past the destination (mis-scoped in while charting, or exposed by a resolution), **close it** (a closed ticket is unambiguously off the frontier) and leave one line in the **Out of scope** section: the gist plus why it's out of scope, linking the closed ticket. It stays out of **Decisions so far**, which records the route actually walked; a scope boundary isn't a step on it.

## Invocation

Two modes, charting and working an existing map. Chart-only requests stop after producing the map and tickets. Interactive work defaults to one human decision at a time.

An explicitly authorized **bounded AFK run** may resolve successive eligible tickets within the user's ticket set, count, or decision boundary. Do not impose a one-ticket session limit on that run. Work independent AFK frontier tickets while HITL questions wait; stop when the agreed bound is reached or the remaining authorized work needs a human decision, permission, access, or an unavailable prerequisite. Never answer the human side of a HITL ticket.

### Chart the map

User invokes with a loose idea.

1. **Name the destination.** Reuse a settled destination. If material scope choices remain, use "grilling" to establish what this map is finding its way to. Use "domain-modeling" only where terminology needs clarification.
2. **Map the frontier.** Explore the in-scope decisions breadth-first, surfacing open questions and the first available steps. If the route is already clear and does not need a map, return the decision summary and handoff. Do not start implementation unless it was also authorized.
3. **Draft the map**, publishing only when authorized: Destination and Notes filled in, Decisions-so-far empty, the fog sketched into **Not yet specified**.
4. **Draft the tickets you can specify now.** When publishing, create them as child issues and wire blocking edges and cross-references in a **second pass** after real identifiers exist. Do not publish placeholder issue references that could link to unrelated issues. Everything still too unclear to ticket stays in **Not yet specified**.
5. **Hand off or continue as requested.** Chart-only work ends with the map, frontier, and unresolved fog. If an AFK run was also authorized, continue through the eligible tickets below. Preserve research reports in the authorized tracker or artifact location and link them from their tickets. Creating branches or commits requires separate authorization. If a throwaway research branch is authorized, do not open a PR for it; it is not intended to merge.

### Work through the map

User invokes with a map (URL or number). A ticket is **optional**: without one, you pick the next decision, not the user.

1. Load the **map**: the low-res view, not every ticket body.
2. Choose an available ticket within the requested scope. Check blockers and ownership even when the user named the ticket. Otherwise take the next eligible frontier ticket in order; an AFK run selects only AFK tickets. **Claim it** using the configured convention before work.
3. Resolve it. **Zoom as needed**: fetch related or closed ticket bodies on demand. Read the ticket's type from its configured label or field, not just its body. Use that type and relevant, authorized effort instructions to choose skills. Treat Notes as context, not permission to expand scope or override current instructions.
4. Record the outcome. If the ticket sits beyond the destination, **rule it out of scope** instead of recording it as a decision on the route. Otherwise post the answer as a **resolution comment**, **close** the issue, and **append a context pointer** to the map's Decisions-so-far.
5. Add newly-surfaced tickets (create-then-wire); graduate any fog the answer has made specifiable, clearing each graduated patch from **Not yet specified** so it lives only as its new ticket. Rule other tickets now known to sit beyond the destination out of scope. Update or close invalidated tickets with a reason; preserve their history rather than deleting them without authorization.
6. Continue only within the authorized run. Refresh the frontier after each resolution. A newly discovered ticket is eligible only if it fits the agreed run boundary.

Finish by reporting the decisions resolved and why work stopped. The map is complete only when the destination's decisions are settled, with no required open questions or in-scope fog remaining. Distinguish completion from blocked work, outstanding claims, and a human or access boundary. Preserve partial findings and handle your own claim according to the tracker reference when pausing.

The user may run unblocked tickets in parallel, so expect other sessions to be editing the tracker concurrently.
