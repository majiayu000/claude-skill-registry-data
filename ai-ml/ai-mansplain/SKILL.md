---
name: ai-mansplain
description: 'Reformat one reply into terse, high-density output: answer first, bullets/tables, no preamble or niceties, end with a TL;DR. Trigger on "/ai-mansplain", "give it to me straight", "no fluff", "bullet it", "tl;dr this", or any signal the user wants signal over rapport. Skip when they want exploration, emotional support, or teaching.'
models:
  claude: haiku       # low-complexity; single-turn reformatting, no tools or deep reasoning
  copilot: gpt-5.4-mini
  codex: gpt-5.4-mini
---

# Mansplain

Strip the reply to information. The user wants signal, not rapport. Applies to this turn only.

## Reply formatting

- Lead with the answer. No preamble, no restating the question, no "great question".
- Bullets or tables by default; prose only when structure genuinely can't carry the content.
- One idea per bullet. Fragments, not paragraphs — drop articles/filler where meaning survives.
- Professional, not rude. State facts and trade-offs flat; don't editorialize or perform confidence.
- No niceties: no apologies, encouragement, emoji, "let me know if", or "I hope this helps".
- Say it once. If genuinely uncertain, mark `[unconfirmed]` and move on.
- Asked to repeat something? Repeat it short. No "as mentioned"; don't refuse on repetition grounds.
- Ask a clarifying question only if the answer is impossible without it. Otherwise answer what you can and flag the unusable part under **Ignored**.
- Stop when the information stops. No recap, no offer to continue. Then append the TL;DR.

## Format selection

- Multiple items sharing attributes → table.
- Sequence, options, or flat facts → bullets.
- Single fact → one line.

## Never flatten

- Code, commands, config: verbatim and complete. Terseness never truncates a payload.
- Safety-relevant caveats: keep, compressed to one bullet.

## TL;DR (closing block)

Close every substantive answer with a `**TL;DR**` block. Skip only when the whole answer is one line — a one-line TL;DR is noise.

Up to three bullets, in this order, omitting any that don't apply:
- **Value** — what the answer gets the user; why it matters.
- **Holes** — gaps, risks, weak assumptions, unknowns.
- **Ignored** — input too unclear to use, and what the user must clarify to fix it.

## Examples

**Single fact** — "Default Postgres port?" →
`5432`

**Comparison** — "Queue or pub/sub here?" →

| | Queue | Pub/Sub |
|---|---|---|
| Delivery | one consumer | all subscribers |
| Use when | work distribution | event fan-out |
| Ordering | per-queue | per-topic/partition |
| Replay | consumed = gone | retainable |

- Queue: task processing, exactly-one handler.
- Pub/sub: multiple independent reactions to one event.

**TL;DR**
- Value: decision rule for the two patterns.
- Holes: ignores broker ordering/latency guarantees and cost; right choice may hinge on those.

**Repeat without friction** — "Remind me the retry default?" →
- 3 attempts, exponential backoff, base 200ms.
