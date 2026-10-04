---
name: whiteboard-help
description: Show the quick-reference guide for the whiteboard planning system (whiteboard, hot-seat, napkin, connotation-cop) — the flow, what to say, and the rules. Use when the user asks "whiteboard help", "how do I use the whiteboard", "what's the flow", "remind me how whiteboard works", "which skill do I use", or seems unsure how to start or continue a whiteboard effort. This skill only DISPLAYS the guide — it never starts a board, resolves tickets, or does any work.
---

# Whiteboard Help

Display the guide below to the user, adapted to what they asked. If they asked a specific question ("how do I close a board?"), answer it from the guide and show just the relevant part. If they asked generally, show the whole thing. **Do not start any work** — this skill is a cheat-sheet, nothing else. If they want to actually begin, tell them what to say and let them say it.

---

## The one-liner

Big fuzzy idea → put it on the **whiteboard** → work the tickets, stopping only when it needs *you* → **snapshot** the board into a spec when nothing's left to decide.

## The flow

**1. Draw** — one session, run once per effort
Say: **"whiteboard this: [your idea]"** (in a repo with GitHub Issues)
What happens: Claude hot-seats you to pin the destination, creates the board issue + tickets, parks the blurry stuff in the parking lot. Then stops.

**2. Work** — repeat until nothing's left to decide
Say: **"work the board"** — or **"run the board"** when you're walking away, or "work one ticket" for exactly one.
What happens: Claude claims the next open ticket and resolves it. Ticket type decides the tool, and whether it needs you:

- hot-seat ticket → Claude questions you, one at a time, with its pick attached — **needs you**
- napkin ticket → Claude builds a throwaway sketch; the verdict is yours — **build alone, judge with you**
- research ticket → Claude reads docs alone, links a summary — **doesn't need you**
- task ticket → a prep chore that unblocks a decision; the ticket says `Runs: agent` or `Runs: human`

Then it updates the board and checks what's next. **Next ticket needs nobody → it just keeps going.** Next ticket needs you → it stops and tells you what it wants. You should never come back to a session idling on a ticket it could have done itself.

**3. Snapshot** — one session, run once at the end
Say: **"snapshot the board"**
What happens: Claude verifies nothing's left (no open tickets, empty parking lot), writes the spec from all the decisions, links it, closes the board. Done — hand the spec to whoever builds.

## Solo use (no board needed)

- **"hot seat me on [decision]"** — stress-test any plan, one question at a time
- **"napkin this: [design question]"** — throwaway code that answers one question
- **"connotation-cop: [term fight]"** — settle what a word means, book it in the glossary

## The rules that matter

- **The sticky test:** can you write the question on one sticky note, precisely? Yes → it's a ticket. Still a paragraph of maybes → parking lot.
- **It stops for you, not for tickets.** A session ends when you're the blocker — never just because a ticket closed. Between every ticket it re-reads the board, so the picture stays current.
- **The board plans, it doesn't build.** Open decision left? That's the next ticket. None left? Snapshot.
- **Claim before work.** Assignee on the ticket = claimed. Unassigned + unblocked = up for grabs.
- **Decisions live on tickets.** The board only gists and links — never holds detail.
- **Every *stop* ends with a sign-off:** board count, what got done, **why it stopped**, what's waiting on you, and what to say. You should never have to ask "what's next" — if a session stops without the sign-off, say "sign off" and you'll get it.

## Where things live

- The board: a GitHub issue labelled `whiteboard:map`; tickets are its sub-issues
- Decisions: resolution comments on closed tickets, indexed on the board
- Big permanent decisions: ADRs in `docs/adr/` (connotation-cop writes them)
- Vocabulary: `CONTEXT.md` at the repo root
- The final spec: wherever the board's Destination says

## Stuck?

- "Which ticket next?" → say "work the board" — Claude picks the first unblocked, unclaimed one
- "It stopped and I don't know why" → the sign-off's **Stopped because** line says: you're the blocker, the board is fanning out faster than it's closing, a ticket drifted off the destination, or context ran thin. Only the first one needs an answer from you — the rest just need "run the board" again
- "It stopped on something it could have done itself" → that's a bug now, not the design. The rule is: needs you → stop, doesn't → keep going
- "Ticket feels huge" → it was mis-sized; Claude splits it into sharp sub-tickets
- "Someone abandoned a ticket" → claimed + 3 days silent = presumed dead; Claude asks you before unclaiming
- "New idea mid-effort but it's past the destination" → it goes to Out of scope, not the board
