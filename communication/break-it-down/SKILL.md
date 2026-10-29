---
name: break-it-down
description: >
  Rewrites the last assistant reply as a plain, short, direct explanation: no
  metaphors. Blunt point, numbered facts, mix-up named, one rule. Use when
  the user types $break-it-down or /break-it-down (bare or with a pointer like 2), or says "break it down", "decode that", "unpack
  that", "no metaphor", "without analogy", "straight explanation",
  "explain without the restaurant thing", or wants the real-system-names
  version of a confusing reply. Bare /break-it-down means: unpack that previous
  message; do not ask them to paste or restate the confusing part. This
  skill is for direct explanations, not requests for an everyday analogy.
---

# Direct Explanation, No Metaphors

Turn one confusing technical idea into a short direct explanation: **no metaphors, no analogies, no fictional settings**.

Use the conversation and the instructions here; no other skill or plugin is required. Preserve complete, readable sentences and the explanation structure below even when a terse writing style is active. Chat around the explanation can stay terse. These instructions shape the chat reply, not durable documents.

## Invocation

In Codex, invoke with `$break-it-down`; in Claude Code, invoke with `/break-it-down`. Treat both spellings identically in the rules below. In follow-up suggestions, use the form the user typed, including any plugin prefix (`/rm0nroe-loadout:break-it-down 2`).

**`/break-it-down` with nothing after it is the full request.** It already means: “I don’t get the last thing you said. Say it straight.”

Do **not** ask them to name the confusing part, paste the prior message, or type “item 1.” That text is already in this chat.

Source, in order:

1. The immediately previous **assistant** message (the thing that confused them).
   If that message is itself a `/break-it-down` or `/simplify` reply, use the message it explained instead: `/break-it-down 2` after one of those means item 2 of the original list.
2. If they added a few words after the slash (`/break-it-down 2` or `/break-it-down the status code part`), use that only as a pointer into that message.
3. If the previous assistant message was a numbered list and they gave no pointer, unpack **item 1** only.

If there is no prior assistant message in this chat, say so in one line and stop.

One idea per reply. If the last message had several numbered items and they did not pick one, unpack item 1, then one line: “Say `/break-it-down 2` for the next.”

## Shape (when source context is available)

1. **First line = the point.** One blunt sentence in plain English. Name the real thing. Not “let me explain.” Example bar: `The HTTP status comes from the controller, not from the error’s name.`
2. **What’s going on, cap 5 numbered lines.** One fact or actor per line. Real names OK; each line = one job or one step. Short sentences.
3. **The mix-up or distinction.** If the source identifies an actual mistake, use “The mix-up:” and name both sides directly. Otherwise use “The distinction:” to explain the difference. Do not claim that the user or agent confused something unless the source says so.
4. **The rule.** One sentence they can reuse.
5. **Stop.** No recap, no “does that help,” no extra concepts.

## Hard rules

- Preserve the source's facts, counts, conditions, and uncertainty. Simplify wording without changing meaning. Keep each number or limit attached to the same quantity, condition, and starting point as in the source. Check the opening sentence and final rule for this too, not just the numbered facts. Distinguish retries from total attempts; do not invent timing, guarantees, or implementation details.

- A time limit bounds one specific span; restate that span, never a nearby one. "Stale for up to 30 seconds" bounds how long a cached entry can lag behind a change to the source after that change happens. It does not bound how old the entry is: an entry cached an hour ago is not stale if the source has not changed since. Write "after the source changes, the cache can keep serving the old value for up to 30 seconds," not "cached data is at most 30 seconds old." The same goes for timeouts versus durations and retry delays versus total wait.

- The two rules above are shared with `simplify`. Keep them in sync when either file changes.

- Assume they are smart and busy, not new to life. Do not baby-talk. Do not lecture CS.
- **No metaphors, analogies, or “imagine a…”**: not even a short one on line 1.
- Plain English over jargon, but keep real system names when they disambiguate (PaymentsController, AlreadyCaptured, BadPaymentRequest). Do not introduce new jargon to explain old jargon; explain necessary terms in plain words.
- Cap at five numbered facts. Split “do now” vs “later” if there are more.
- Do not dump full architecture, file paths, or HTTP tables unless they asked for the receipt too. Default = direct explanation only.
- Do not invent a second framing “for completeness.”

## Gold example (quality bar: match this density)

Apply the pattern to the current topic. The names and facts below are illustrative, not assumptions about the user's system.

They typed only `/break-it-down` after a paragraph about which HTTP status a payment retry returns.

```
The HTTP status comes from the controller, not from the error’s name.

1. A retry on an already-captured payment raises AlreadyCaptured inside PaymentMediator.
2. PaymentMediator refuses the retry before calling StripeGateway, so Stripe is never contacted.
3. PaymentsController is the only place that maps errors to HTTP statuses.
4. PaymentsController maps AlreadyCaptured to 500.
5. BadPaymentRequest is an internal error name. It does not set the status, even though it sounds like 400.

The mix-up: reading BadPaymentRequest and AlreadyCaptured as if they were HTTP statuses and reporting 400. The controller never returns 400 for an already-captured retry.

The rule: read the status mapping in PaymentsController before reporting a status; do not infer it from an error class name.
```

