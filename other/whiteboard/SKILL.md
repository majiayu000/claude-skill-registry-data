---
name: whiteboard
description: Plan a chunk of work too big for one agent session by putting it on a shared whiteboard — a map of investigation tickets on GitHub Issues — working them until nothing is left to decide, then snapshotting the board into a handoff artifact. Tickets needing nobody are worked back-to-back; the session stops when the human is the blocker. Use only when the user explicitly invokes whiteboard or asks to draw, work, run, or snapshot a whiteboard/map — not for ordinary planning requests.
---

# Whiteboard

A big loose idea just landed — too big for one session, too many unknowns to hold in one head. So it goes on the board. The whiteboard lives on GitHub Issues as a shared artifact: multiple sessions and multiple humans work it without collisions, and the picture survives every context window that touches it.

**The whiteboard is for planning. It does not build.** Every ticket resolves a *decision*. The board is done when nothing is left to decide before someone goes and builds the thing. Feel the pull to just build? Run the test: *is there an open decision left?* No → you're done deciding; switch to Snapshot mode. Yes → that decision is the next ticket. (A board's Notes can explicitly opt execution in; absent that, produce decisions, not deliverables.)

## What's on the board

- **Destination** — what "done" looks like: a spec to hand off, a decision to lock, a migration completed. Written top-corner first — it fixes the scope of everything else.
- **The board** — one GitHub issue labelled `whiteboard:map`. An **index, not a store**: one-line gist per decision, link to the ticket holding the detail. Never restate detail on the board.
- **Tickets** — child issues of the board, one open question each, sized for one session. Each carries a `whiteboard:<type>` label (see Ticket types).
- **Up next** — open tickets that are unblocked (no open blockers) and unclaimed (no assignee). The takeable edge of the board.
- **Parking lot** — the board's section for questions you can tell are coming but can't phrase sharply yet. **The sticky test: could you write the question on one sticky note, precisely, right now?** (Not: could you answer it.) Fits on a sticky → ticket, even if blocked. Still a paragraph of maybes → parking lot. Don't pre-slice parked items into ticket-sized pieces — one parked item may become several tickets later, or none.
- **Out of scope** — work consciously ruled past the destination. Not parked: it never comes off the lot. One board line with the why.

Tracker mechanics — creating the board, sub-issues, blocking edges, up-next query, claiming — live in [references/github-ops.md](references/github-ops.md). Read it before touching the tracker. Body templates: [references/templates.md](references/templates.md). The continue-or-stop rules: [references/run-loop.md](references/run-loop.md). First board? Skim [references/example-board.md](references/example-board.md) — one small board, full lifecycle.

## Ticket types

Every ticket is **HITL** (worked *with* the human — never answer the human's side; a hot-seat that answers its own questions has broken the skill) or **AFK** (agent alone). This is also what decides whether a session keeps going or stops — see [run-loop.md](references/run-loop.md).

- **research** (AFK) — docs, APIs, knowledge bases. Produces a linked markdown summary.
- **napkin** (HITL *for the verdict only*) — raise fidelity with a cheap concrete artifact to react to, via the napkin skill. Building it is AFK; judging it is theirs.
- **hot-seat** (HITL) — the default: conversation via the hot-seat + connotation-cop skills, one question at a time.
- **task** (either — **the body must say which**) — manual work that unblocks a decision (provision access, move data so its shape is visible). The one type that *does* — and it earns that by unblocking a decision, not by delivering the destination. Its resolution records what was done plus the facts later tickets need.
  Every task ticket carries `Runs: agent` or `Runs: human`, decided when it's written and the context is fresh. Missing → **treat as `human`.** Task tickets act on the world; guessing that wrong is expensive, and the field is cheap.

## Actually load the sub-skills

Naming a skill is not using it. When a ticket's type points at hot-seat, napkin, or connotation-cop — or a mid-ticket trigger below fires — **load the skill and follow it**: invoke it with the Skill tool if available, otherwise read its SKILL.md from the skills directory (e.g. `~/.claude/skills/hot-seat/SKILL.md`). Working "in the spirit of" a sub-skill from memory is exactly how the sub-skills silently stop being used, and the user notices.

Mid-ticket triggers, any mode:

- About to ask the user a decision question → **hot-seat is loaded first.** Its rules (one question per message, your pick attached, defer handling) govern every question the whiteboard asks.
- Discussion circling, or the user can't judge the options in the abstract ("I'd have to see it") → stop talking, load **napkin**, build the sketch, resume with their reaction.
- Two words fighting over one meaning, or a resolved decision is hard-to-reverse + surprising + a real trade-off → load **connotation-cop** to settle the term or write the ADR.
- A genuine choice surfaces while resolving an **AFK** ticket → don't guess and don't stall. Write it as a new hot-seat ticket, add it to *Waiting on you*, resolve what's still answerable without it, and carry on. The human gets every question at once instead of the first one.

If a sub-skill genuinely isn't installed, degrade gracefully: interview one question at a time with a recommended answer each, record decisions in ticket comments. Never block on a missing skill.

## The sign-off — how a session ends when *you* are the blocker

The user must never have to ask "what's next." But the sign-off is a **stopping artifact**, not a punctuation mark: printing one while the next ticket needs nobody strands the user on a keystroke they never had to type. Before signing off, run the check:

> **Does the next takeable ticket need the human?**
> **No** → don't sign off. Print `✓ <ticket> — <gist> · taking <next ticket>` and keep going.
> **Yes, or nothing is takeable** → sign off. Stop.

Full eligibility table and the other stop conditions — fanout, drift, context — live in [references/run-loop.md](references/run-loop.md).

When you do stop, verbatim in shape:

```markdown
**Board:** <X> closed / <Y> open
**This session:** <what closed — one line each if several>
**Stopped because:** <the human is the blocker | fanout | drift | context>
**Waiting on you:** <ticket name> — <what it needs from them>
**Next up:** <ticket name> — <one line on why it's the pick>
**Say:** "run the board"   (or "snapshot the board" when nothing is left to decide)
```

Pick "Next up" for them: first unblocked, unclaimed ticket in board order — or, when several are takeable, the one that unblocks the most (say so). A stopping session that ends without the sign-off is unfinished, even if the ticket was resolved perfectly.

Draw and Snapshot always sign off — both are terminal by design.

## Hard rules (every mode)

1. **One ticket per iteration, and re-read the board between them.** Each resolution sharpens the board for the next one; resolving from a view fetched before you started works from a board another session may have already moved. Re-fetch the board body and re-query up-next after every close — that's the requirement the old "one ticket per session" rule was standing in for.
2. **Claim before work.** Assignee = claim. The first write of every iteration is assigning yourself the ticket — including the second and third ones, where a collision is likeliest.
3. **Names, not numbers.** Everything the human reads refers to boards and tickets by title, link riding inside — `[Pick the queue tech](url)` — never a bare `#42`. Number walls are illegible.
4. **Stale claims.** Claimed + zero activity for 3+ days = presumed abandoned. Presumed, not proven — ask the human before unclaiming. Never silently steal.
5. **Never delete a claimed ticket.** A resolution invalidates someone's claimed ticket? Comment the invalidation and move on — their call. Unclaimed invalidated tickets: close, with a comment naming the decision that killed them.
6. **Split, don't swell.** Resolving surfaces 3+ distinct sub-questions? The ticket was mis-sized. Create the sharp sub-questions as new tickets (blocking this one if needed), resolve what's still *this ticket's* question, leave the rest for up-next.
7. **Stop for the human, not for the ticket.** A session ends when the human is the blocker (or a stop condition fires) — never merely because a ticket closed. When it does end, it ends with the sign-off block. No session ends with silence.

## Mode: Draw

*User arrives with a loose idea.*

1. **Write the destination** — hot-seat + connotation-cop session pinning down what this board is working toward. Scope gets fixed first.
2. **Fill the board** — hot-seat again, **breadth-first**: fan out across the whole space surfacing open decisions and takeable first steps; no deep dives yet. Nothing lands in the parking lot and the journey fits one session? You don't need a board — say so, ask how they want to proceed.
3. **Create the board** (per github-ops): destination + notes filled, decisions empty, the dim stuff written into *Parking lot*.
4. **Create the sticky-sharp tickets** as sub-issues, then wire blocking edges in a **second pass** (issues need ids before they can reference each other). Check for cycles — a cycle means two "blockers" are really one question.
   Every `task` ticket gets `Runs: agent` or `Runs: human` in its body, decided here — this is the one moment the context is fresh enough to know. Skip it and later sessions must assume `human` and stop for a chore they could have done.
5. **Stop.** Drawing the board is a full session's work. Don't also resolve tickets.

## Mode: Work

*User arrives with a board (URL or number), maybe a ticket.*

1. **Load the board body** — the low-res view, not every ticket. Open with a one-line status: "Board: X closed / Y open — taking [ticket name]."
2. **Choose the ticket**: the one the user named, else the first up-next ticket in board order *that this session can actually take* — see [run-loop.md](references/run-loop.md) for what that means. **Claim it.**
3. **Resolve it** — first load the sub-skill the ticket's type names (see "Actually load the sub-skills"), then work it. Zoom on demand: fetch related/closed ticket bodies as needed, invoke the skills the board's Notes name.
4. **Record**: answer as a resolution comment → close the ticket → append gist + link to the board's *Decisions so far*.
5. **Tend the board**: create newly-surfaced tickets (create, then wire); promote parked items the answer sharpened — a promoted item leaves the *Parking lot* and lives only as its new ticket; rule newly-exposed past-destination work out of scope (close ticket, add board line); flag invalidated tickets per hard rule 5.
6. **Continue or stop** — re-fetch the board, re-query up-next, and apply the check in "The sign-off". Next takeable ticket needs nobody → take it, back to step 2. Needs the human, or a stop condition fired → sign off. Up-next empty + no open tickets + empty parking lot → say so and recommend Snapshot mode next.

Other sessions may be editing the tracker right now. Re-query; don't trust a list fetched before you started resolving.

"Work one ticket" (or a named ticket) means exactly that: resolve it, sign off, stop.

## Mode: Run

*Same as Work — the user is just saying up front that they're walking away.*

`run the board` is Work mode with the intent stated: keep taking tickets until the human is genuinely the blocker. There is no behavioral difference from `work the board`; the loop is the default either way. What changes is what the user expects to come back to — a queue of real questions, not a keystroke.

Read [references/run-loop.md](references/run-loop.md) before starting: eligibility per ticket type, the `Runs:` field on task tickets, the five stop conditions, and the bookkeeping the sign-off needs.

Two things a run must never do, because there's no human present to ask: **unclaim a stale ticket** (hard rule 4) and **answer the human's side of a hot-seat** (they're the whole point).

## Mode: Snapshot

*Up next empty, parking lot empty, no open tickets — nothing left to decide. Before anyone erases a whiteboard, they photograph it. That's this mode.*

1. **Verify the board is really done**: query open children *including claimed ones* — an open claimed ticket means someone's mid-flight; don't close under them. Anything still parked? Drawing isn't done — promote it or move it out of scope, with the user.
2. **Take the photo**: walk *Decisions so far*, zoom into each resolution, and write the thing the destination named — spec, locked decision record, handoff doc. Synthesis, not concatenation: organize by the shape of the answer, not the order the tickets closed.
3. **Deliver it** where the destination says (repo file, final board comment, handoff doc). Link it from the board body.
4. **Erase the board**: close the board issue with a closing comment naming the artifact. A closed board with a linked snapshot is the effort's front door forever.

Snapshotting is its own session. Arriving at Work step 6 means *recommending* Snapshot — not rolling into it.
