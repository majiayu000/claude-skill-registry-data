---
name: simplify
description: >
  Rewrites the last assistant reply into a short everyday analog (one
  metaphor, numbered roles, mix-up named, one-sentence rule). Use when the
  user types /simplify with no extra text, or says something is
  unclear, too technical, jargon, "I don't get it", "make it simpler",
  "like last time", "non-technical", "tldr but human", or ELI5. Bare
  /simplify means: explain that previous message; do not ask them
  to paste or restate the confusing part.
---

# Everyday Analogy Explanation

Turn one confusing technical idea into the same shape that worked: a one-line metaphor, a few everyday roles, the mix-up named in those terms, one rule.

This skill wins over any terse-output mode for the explanation itself. Chat around it can stay terse. For the direct, no-metaphor version, use the sibling skill `break-it-down`.

## Invocation (this is the product)

In follow-up suggestions, use the form the user typed, including any plugin prefix (`/rm0nroe-loadout:simplify 2`).

**`/simplify` with nothing after it is the full request.** It already means: “I don’t get the last thing you said. Make it clear for someone non-technical.”

Do **not** ask them to name the confusing part, paste the prior message, or type “item 1.” That text is already in this chat.

Source, in order:

1. The immediately previous **assistant** message (the thing that confused them).
   If that message is itself a `/break-it-down` or `/simplify` reply, use the message it explained instead: `/simplify 2` after one of those means item 2 of the original list.
2. If they added a few words after the slash (`/simplify 2` or `/simplify the cashier part`), use that only as a pointer into that message.
3. If the previous assistant message was a numbered list and they gave no pointer, explain **item 1** only.

If there is no prior assistant message in this chat, say so in one line and stop.

One idea per reply. If the last message had several numbered items and they did not pick one, do item 1, then one line: “Say `/simplify 2` for the next.”

## Shape (always)

1. **First line = the point.** One metaphor. Not “let me explain.” Example bar: `The map is not the street.`
2. **One setting.** Restaurant, post office, kitchen, etc. Do not mix settings.
3. **Numbered roles, cap 5.** Everyday name first, real name in parentheses after. One job per role.
4. **The mix-up.** What they (or the agent) confused, in the analog, then the real names in parentheses.
5. **The rule.** One sentence they can reuse.
6. **Stop.** No recap, no “does that help,” no extra concepts.

## Hard rules

- The analogy changes the setting, never the facts. Preserve the source's facts, counts, conditions, and uncertainty. Keep each number or limit attached to the same quantity, condition, and starting point as in the source, and keep real numbers real: "the cook retries 3 times (4 attempts in total)", not "the cook tries a few times". Check the opening line and final rule too, not just the roles. Distinguish retries from total attempts; do not invent timing, guarantees, or implementation details.
- A time limit bounds one specific span; restate that span, never a nearby one. "Stale for up to 30 seconds" bounds how long a cached entry can lag behind a change to the source after that change happens, not how old the entry is. The same goes for timeouts versus durations and retry delays versus total wait.
- The two rules above are shared with `break-it-down`. Keep them in sync when either file changes.
- Assume they are smart and busy, not new to life. Do not baby-talk. Do not lecture CS.
- Do not introduce new jargon to explain old jargon. If a real name must appear, put it in parentheses after the everyday word.
- Do not dump architecture, file paths, or HTTP tables unless they asked for the analog *and* the receipt. Default = analog only.
- Do not invent a second metaphor “for completeness.”

## Gold example (quality bar: match this density, not this restaurant every time)

They typed only `/simplify` after a numbered technical list. Treat that as: “I don’t get what you mean in 1, make it more clear for someone non-technical.”

```
The map is not the street. The code index is a map of the code. The status code a client actually gets is written in a different file than the name that looks like “bad request.”

Imagine a restaurant:

1. The menu (the code index): tells you which kitchen to walk to. Fast. “Cancel lives over there.”
2. The cashier (PaymentsController): the only place that says what you pay / what number goes back to the app (200, 400, 500).
3. The cook (PaymentMediator): decides which ticket to send the cashier. Sometimes they refuse before cooking (RetryNotAllowed). That refusal is 500 here, even if the cashier also has a 400 button they never press for this order.
4. The stove (StripeGateway): Stripe. Names like “bad payment request” are the cook’s slang, not the number on the receipt.

The bug: the agent read the cook’s slang (BadPaymentRequest, AlreadyCaptured) and told you 400. The cashier never rang that up for “already captured.”

The rule: after the map, read the cashier first, then the cook’s “stop early” doors, then Stripe. Do not treat a class name as an HTTP status.
```

## Other scenarios (same shape)

| Confusing thing | Everyday setting to try first |
|---|---|
| “Where vs what is true” | Map vs street; menu vs cashier |
| “Name sounds like X but means Y” | Nickname vs what’s on the receipt |
| “Two similar buttons, only one rings up” | Cashier has a button they don’t press for this order |
| “Fast search vs the real answer” | Index card vs opening the folder |

Pick one row. Do not use the table in the user-facing reply.

## After

One line of state: what you just un-confused. Next action only if they still have a decision. Under two minutes.
