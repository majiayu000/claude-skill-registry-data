---
name: connotation-cop
description: Police the project's vocabulary — bust vague terms, keep the CONTEXT.md glossary sharp, and lock in decisions worth remembering as ADRs. Use when the user debates naming, says "what should we call this", asks to pin down terminology, wants a decision recorded, or when another skill (hot-seat, whiteboard) surfaces a decision that clears the ADR bar. Just reading the glossary for vocabulary is NOT this skill — trigger only when the words or decisions are being changed.
---

# Connotation Cop

Half of every design argument is two people using one word for two things. The cop ends that: challenge terms, sharpen them, book them into the glossary the second they're settled. This is the *active* beat — you're changing the shared vocabulary, not just reading it.

## Where the records live

- **`CONTEXT.md`** at the repo root — the glossary. Format: [references/context-format.md](references/context-format.md).
- **`docs/adr/`** — numbered decision records. Format: [references/adr-format.md](references/adr-format.md).
- **`CONTEXT-MAP.md`** at the root only when a repo genuinely has multiple bounded contexts — it points at each context's own glossary and ADRs. Layout in context-format.

Create everything **lazily**. First settled term creates `CONTEXT.md`. First real decision creates `docs/adr/`. An empty scaffold is a promise nobody keeps.

## On the beat

**Enforce the glossary.** User's term conflicts with `CONTEXT.md`? Call it on the spot: "Your glossary says *cancellation* means X — you're using it as Y. Which is it?" An unenforced glossary is a dead file.

**Bust the mush.** Vague or overloaded term? Propose the precise one: "You keep saying *account* — Customer or User? Different things here." One question at a time — hot-seat rules apply.

**Run the ugly scenario.** When concepts and their relationships are on the table, invent the nasty case and push it through: "Customer cancels after the shipment left but before delivery — what state is the Order in?" People agree on abstractions while holding different models. Scenarios expose it.

**Check the code before you nod.** User says how it works? Verify. The code disagreeing is a finding, not an awkward moment: "Code cancels whole Orders. You just said partial cancellation exists. Which is right?"

**Book it immediately.** Term settled → glossary entry, right now, mid-conversation. Batching means skipping, and the session ends with the model still trapped in heads.

`CONTEXT.md` is a glossary, full stop. No implementation details, no specs, no scratch notes. Implementation decisions go in ADRs; everything else goes nowhere.

## The ADR bar — all three or skip it

1. **Hard to reverse** — changing your mind later actually costs something
2. **Surprising without context** — a future reader would ask "why on earth?"
3. **A real trade-off** — genuine alternatives existed, one got picked for reasons

Miss one, skip it. Easy-to-reverse just gets reversed. Unsurprising never gets questioned. No-alternative records nothing but "we did the obvious thing." The bar is strict because an ADR folder full of trivia trains everyone to ignore it — and then the one ADR that matters dies unread.

Bar cleared? Write it now, format in [references/adr-format.md](references/adr-format.md). Same immediacy as glossary entries.

## Plays with

- Mid-**hot-seat**: a decision-log line that clears the bar becomes the ADR's seed.
- Mid-**whiteboard**: a ticket resolution that clears the bar gets an ADR *and* the board's one-line pointer — ADR holds the detail, board holds the index.
