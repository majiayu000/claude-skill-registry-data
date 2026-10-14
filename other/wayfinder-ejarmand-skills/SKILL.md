---
name: wayfinder
description: Plan a huge chunk of work — more than one agent session can hold — as a shared map of decision tickets on GitHub, and resolve them one at a time until the way to the destination is clear.
disable-model-invocation: true
---

A loose idea has arrived — too big for one agent session, and the way from here to the **destination** isn't visible yet. Wayfinding charts the way as a **shared map** of GitHub issues, breaking down decision forks until a clear implementation path remains.

The destination is variable, and shapes every ticket. It might be a spec to hand off and iterate on, a decision to lock before planning starts, or a change made in place like a data-structure migration. The map is domain-agnostic.

## Plan, don't do

Wayfinder is **planning**: resolve decisions until none stand between here and implementation. The pull to just do the work is usually the signal you've reached the edge of the map and it's time to hand off.

## Refer by name

Every map and ticket is an issue, and its title should be a descriptive, referrable **name**. Describe goals and decisions in those names, with the numerical issue id attached.

## The Map

The map is a single issue with a child issue for each ticket. The work-record contract, [WORK-RECORDS.md](WORK-RECORDS.md), defines the mechanics: creating tickets, wiring blocking edges, querying the frontier, claiming a ticket, and resolving it.

The map is an **index**: each decision lives in its ticket, and the map only gists and links it.

### The map body

The whole map at low resolution, loaded once per session. Open tickets are **not** listed — they are open child issues, found by query.

```markdown
## Destination

<what reaching the end of this map looks like — the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<domain; skills every session should consult; standing preferences for this effort>

## Decisions so far

<!-- the index — one line per closed ticket: enough to judge relevance, then zoom the link for the detail the ticket holds -->

- [<closed ticket title>](link) — <one-line gist of the answer>

## Downstream decisions

<!-- in-scope decisions downstream of open tickets, too vague to ticket yet; they graduate as upstream work resolves -->

## Out of scope

<!-- work ruled beyond the destination; never graduates -->
```

### Tickets

A ticket's body is the question, sized to a single independent concern:

```markdown
## Question

<the decision or investigation this ticket resolves>
```

Each ticket carries a `wayfinder:<type>` label — one of `research`, `prototype`, `grilling`, `task` (see [Ticket Types](#ticket-types)).

The answer isn't in the body — it's recorded when the ticket resolves. Assets created along the way are linked from the issue, not pasted in.

## Ticket Types

Every ticket is either **HITL** — human in the loop, worked *with* a human responsible for resolving it — or **AFK**, driven by the agent alone.

- **Research** (AFK): Reading documentation, third-party APIs, or local resources like knowledge bases to surface a fact a decision waits on. Resolved by a research **subagent**. Use when knowledge outside the current working directory is required.
- **Prototype** (HITL): Raise the fidelity of the discussion with a cheap, concrete artifact to react to — an outline, a rough take, a stub, or UI/logic code via the `/prototype` skill. Link the prototype as an asset. Use when "how should it look" or "how should it behave" is the key question.
- **Grilling** (HITL): Conversation via `/grill`, one question at a time, settling the decision and any domain terms it depends on. The default case.
- **Task** (HITL or AFK): Manual work a decision is blocked on — nothing to decide, just something that must exist first: signing up for a service so its API can be judged, provisioning access, moving data so its shape can be seen. The one type that *does* rather than decides; it earns its place by unblocking a decision, not by delivering the destination. The agent drives it alone where it can (AFK); otherwise it hands the human a precise checklist (HITL). The answer records what was done and the facts later tickets depend on (credential locations, new URLs, row counts).

## Downstream decisions

The map is _deliberately_ incomplete: don't chart what you can't yet see. Some decisions and investigations are visibly coming but can't be pinned down yet — they sit **downstream** of open questions. Those go in the map's **Downstream decisions** section: the suspected question, the area to revisit later. Everything here is in scope, just not sharp enough to ticket. Write as loosely or as fully as current knowledge allows; the section doubles as a signpost for collaborators reading where the effort is headed. As upstream tickets resolve, entries sharpen and **graduate** into tickets of their own, until the way to the destination is clear.

**Ticket or downstream?** The test is whether you can state the question precisely now — _not_ whether you can answer it now.

- **Ticket** when the question is already sharp — even if it's blocked and you can't act on it yet.
- **Downstream** when you can't yet phrase it that sharply. Don't pre-slice an entry into ticket-sized pieces: it's coarser than a ticket, and may graduate into several tickets, or none.

**Downstream decisions** excludes what's already decided (Decisions so far), what's already a live ticket, and what's out of scope (the next section).

## Out of scope

The destination fixes the scope. Work beyond it is **out of scope** — excluded by scope, not by sharpness — and goes in the map's **Out of scope** section, never in **Downstream decisions**.

Out-of-scope work never graduates; it returns only if the destination is redrawn, and then as a fresh effort.

When an existing ticket turns out to sit past the destination — mis-scoped while charting, or exposed by a resolution — **close it** and add one line here: the gist, why it's out of scope, and a link to the closed ticket. It stays out of **Decisions so far**, which records only the route actually walked.

## Invocation

Two modes. Either way, **never resolve more than one ticket per session** — research tickets excepted.

### Chart the map

User invokes with a loose idea.

1. **Name the destination.** Run `/grill` to pin down the spec, decision, or change this map is finding its way to, including the domain terms needed to describe it. It fixes the scope, so settle it first.
2. **Map the frontier.** Grill again, **breadth-first**: fan out across the whole space, surfacing the open decisions and the first steps takeable now. **If nothing lands in Downstream decisions** — the way to the destination is already clear, the whole journey small enough for one session — you don't need a map. Stop and ask the user how they'd like to proceed.
3. **Create the map**: Destination and Notes filled in, Decisions-so-far empty, what you can't yet ticket sketched into **Downstream decisions**.
4. **Create the tickets you can specify now** as child issues of the map, then wire blocking edges in a **second pass** (issues need ids before they can reference each other). Wiring sorts them into the frontier and the blocked.
5. **Fire the research subagents.** For each `research` ticket, spin up a research subagent to resolve it in parallel, capturing findings on a throwaway `research/<name>` branch with a context pointer from the ticket.
6. Stop — charting is one session's work; it hand-resolves nothing.

### Work through the map

User invokes with a map (URL or number). A ticket is **optional** — without one, you pick the next decision, not the user.

1. Load the **map** — the low-res view, not every ticket body.
2. Choose the ticket — the user's, or the first frontier ticket in order. **Claim it** before any work.
3. Resolve it — **zoom as needed**: fetch the full body of any related or closed ticket on demand; invoke the skills the `## Notes` block names. If in doubt, use `/grill` to clarify the decision and its domain terms.
4. Record the resolution — the contract's resolve operation.
5. Add newly-surfaced tickets (create-then-wire); graduate whatever the answer has made specifiable — each entry leaves **Downstream decisions** and becomes a ticket. If the answer reveals a ticket — this one or another — sits beyond the destination, **rule it out of scope**. If it invalidates other parts of the map, update or delete those tickets.
6. When no open tickets remain and **Downstream decisions** is empty, publish the agreed implementation scope and acceptance criteria as a GitHub issue, linking the map and relevant decisions. Follow the work-record contract and mark it `ready-for-agent` when fully specified.

The user may run unblocked tickets in parallel, so expect other sessions to be editing the map and its tickets concurrently.
