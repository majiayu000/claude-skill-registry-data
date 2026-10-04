---
name: asking-questions
description: Use when about to ask the user a weighted decision or a choose-between-options question via AskUserQuestion, buttons, or any pick-one/pick-many UI. Especially when tired, moving fast, batching several questions, or tempted to "just fire the buttons."
---

# Asking Questions

## Core principle

The decision context lives in **chat prose**. The question tool (`AskUserQuestion` and any button UI) is ONLY the clickable capture of a choice the user can already make from the prose above it. If the buttons carry the reasoning, the user decides blind.

**Users often answer through the question card — on mobile especially — where they cannot read long button text and cannot see `preview` fields.** The prose in the transcript is what they actually read. Never make the tool call the place the reasoning lives.

## Configuration (injected at SessionStart)

This skill reads two values from the resolved agentflow config (`environment.md`, injected into context by the SessionStart hook — never hardcode them):

- **`question_style`** — `mobile-two-turn` (default) or `inline`. Selects which protocol below applies.
  - `mobile-two-turn` — the default. A client may render ONLY the cards in a turn that contains an `AskUserQuestion` call; use the strict two-turn protocol below.
  - `inline` — the opt-out, for a client that shows prose and cards together: prose and the `AskUserQuestion` call may live in the **same turn** (prose first, then the call).
- **`person.name`** — the user's display name, used only for addressing. When the config is unavailable, address the user neutrally ("you"); never substitute a hardcoded name.

If `question_style` is not present in the injected config, treat it as `mobile-two-turn`.

## The recipe — every weighty question

Write a normal chat message FIRST, containing, in order:

1. **The question**, stated plainly — name the thing being decided (+ id/priority if it has one).
2. **Why it matters** — what this choice gates or changes (1–3 sentences).
3. **Each option** — a short label, then its **PRO** and its **CON/RISK**. A paragraph or tight bullet, not a bare label.
4. **Your recommendation** — which option, one line of why. Lead with it.

THEN call the question tool: option labels match the prose, one-line `description`s just echo it, recommended option first with "(Recommended)" in the label.

Batch up to 4 questions per call — but the prose must cover **all** of them first, in the same order.

## Sequencing (mechanical)

The prose and the tool call must be **adjacent, in this order, with nothing between**:

1. Finish ALL other tool work first (spec writebacks, edits, greps, task updates) — before the prose.
2. Output the complete decision prose as plain chat text.
3. Invoke `AskUserQuestion` as the **immediate next action** — no tool call between the prose and
   the question, and nothing else after the prose except the question call itself.

Prose interleaved with tool calls reads as working-narration and can fail to render where the user
is answering — they then see bare button cards and decide blind, even though the prose exists
somewhere in the turn. If you notice pending tool work after drafting
the prose: stop, do the work, then output the prose fresh, then call.

Under `question_style: inline` the prose and the `AskUserQuestion` call may share one turn (prose
immediately followed by the call). Under `question_style: mobile-two-turn` they must NOT — see below.

## `question_style: mobile-two-turn` — the two-turn protocol

Applies whenever the injected `question_style` is `mobile-two-turn`, which is the default. It is
built for a client — a mobile one, typically — where **a turn that contains an `AskUserQuestion`
call shows ONLY the cards — any prose in that same turn is invisible to the user.** The shape that
WORKS:

1. **Prose turn:** output the complete recipe (question + why it matters + lettered A/B/C options
   with pro/con + recommendation) as plain chat text and **END THE TURN** — no tool call after it.
2. **Button turn:** after their next reply (an ack, a comment, anything), fire `AskUserQuestion` as
   the capture — SHORT question string, short letter-prefixed labels
   (`A: Propose + one-tap (Recommended)`), minimal/no descriptions. Zero reasoning in the card.
3. The user may also just answer free-text from the prose turn — then skip the buttons entirely.

NEVER put decision prose and the `AskUserQuestion` call in the same turn under this style. The
buttons are still wanted — but always a turn behind the prose.

## Do NOT

- Fire the question tool with only terse `description`s and no preceding prose.
- Cram the reasoning into `preview` blocks or dense `description`s as a *substitute* for the prose. This is the tempting over-correction — it still hides the reasoning from a mobile reader, and it's the wrong shape. Prose in chat, then a plain button call.
- Treat a question as exempt because it feels "small" or "obvious." If it has options and a tradeoff, it gets the prose.

## When the full treatment is NOT needed

- A bare yes/no with no tradeoff to weigh.
- A trivial naming/formatting pick.

For those, a one-line question — or just stating an assumption ("assuming X, correct me") — is fine.

## Red flags — you're about to violate this

- "The descriptions are enough."
- "I explained the context a few messages ago." (Re-state it *with* the question.)
- "There are several questions; prose for each is too long." (Batched decisions are exactly where blind-answering hurts most.)
- "I'll put the detail in the option previews instead."

**All of these mean: write the prose.**

## Rationalization table

| Excuse | Reality |
|---|---|
| "The description echoes the point" | Two lines can't carry pro + con + recommendation. The user decides blind. |
| "Context is in the transcript above" | On mobile they answer from the question card, not the transcript. Put it with the question. |
| "Batching 4, prose is too much" | Batched decisions are where blind answers hurt most. Prose all four. |
| "Previews solve the mobile problem" | A preview still isn't the chat message the user reads, and it's the wrong shape. Prose. |

## Example

> **Decision — auth provider for v1.** We need to pick who owns login; this gates the whole migration and every downstream user lookup.
> - **Supabase GoTrue (self-hosted)** — *pro:* self-hostable, GitHub OAuth built in, no per-seat cost; *con:* brings a small Postgres to run.
> - **WorkOS** — *pro:* enterprise SSO/SCIM ready; *con:* per-seat pricing, and you don't need SSO for self-serve/SMB.
> **Recommendation: GoTrue** — fits self-serve/SMB + self-hosting; WorkOS's edge is the one thing you don't need.

Then `AskUserQuestion`: labels `GoTrue (Recommended)` / `WorkOS`, one-line descriptions echoing the above.
