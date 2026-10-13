---
name: wayfinder
description: Map and resolve material decision dependencies across a multi-session effort.
disable-model-invocation: true
---

# Wayfinder

Map a multi-session effort whose material decisions are not yet settled. This is
a decision graph, not an implementation backlog unless execution was explicitly
included. If the route is already clear, use ordinary planning or execution.

## Map and tickets

Use Beads: one map issue labelled `wayfinder:map`, with decision tickets as children
and native prerequisite edges. The map contains Destination, Notes, Decisions so
far, Not yet specified, and Out of scope. Keep resolution detail on the ticket;
the map carries a named pointer and short gist. Reference names with IDs/links so
readers can understand the map without opening every item.

A ticket asks one bounded question with a resolution criterion. Use a
`wayfinder:<type>` label: research, prototype, grilling or task. Size by decision
coherence and dependencies, not an assumed context-window size.

- Research establishes missing facts; direct lookups are fine, delegation optional.
- Prototype raises fidelity for a decision; use the prototype skill when useful.
- Grilling involves a live participant when an interview is requested.
- Task performs authorized prerequisite work that unblocks a decision.

Do not substitute the agent's answer for a required human decision. Documentation
and memory follow task authority; domain-modeling is optional, not automatic.
If Beads is unavailable, report the blocker and continue safe investigation;
do not silently create a competing Markdown tracker.

## Chart and resolve

Settle the destination from supplied context and material questions. Create sharp
questions as tickets even if blocked; leave only questions not yet expressible in
Not yet specified. Create IDs before wiring genuine dependencies.

Choose the requested ticket or a ready unclaimed child; claim it before working.
Load detail as needed. Record the answer and supporting artifacts, close with
evidence, and append its resolution pointer to the map. Graduate newly expressible
questions into tickets and update invalidated dependencies without deleting history.
Out-of-scope tickets close with an explicit exclusion reason, not a claim of delivery.

Continue through additional authorized ready tickets while useful; there is no
one-ticket-per-session limit. Parallel work needs disjoint ownership and shared
delegation policy. Stop at a required human decision, unavailable prerequisite or
the settled destination. Prepare concrete options before requesting a final gate.
