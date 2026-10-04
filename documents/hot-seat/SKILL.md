---
name: hot-seat
description: Put the user in the hot seat — one question at a time until their plan, decision, or idea actually holds up. Use whenever the user says "hot seat me", "grill me", "stress-test this", "poke holes in this", "am I missing anything", or drops a plan and wants it challenged before anyone acts on it — even if they never say the words. Also used as a sub-procedure by the whiteboard and connotation-cop skills.
---

# Hot Seat

The user has a plan. Your job: find out if it survives contact. Ask questions until you both hold the same picture — then, and only then, act on it.

## Rule zero

**One question per message.** Ask. Wait. Then ask the next. The answer to question 1 changes question 2 — batching questions burns that. Writing "Also," means you're about to break this rule. Cut it.

## Facts are yours, decisions are theirs

- Answer discoverable in the code, filesystem, or docs? **Look it up.** Never spend the user's attention on something grep can answer.
- Genuine choice? **It goes to them.** Every time, even when you're sure. Your confidence goes in the recommendation, not into silently deciding for them.

## Every question ships with your pick

> Cancelled orders — keep the invoice or void it?
> **My pick:** keep it. Voiding breaks the audit trail you said you need.

The pick is a service, not a lead. They choose differently? Take it and move. Only push back when their answer contradicts something they already said — and then the contradiction IS the next question.

## Order matters

Upstream decisions first. If B only makes sense after A, ask A — never ask B wearing an "assuming A..." costume. When an answer kills questions in your queue, drop them silently.

## When they stop deciding

Two "whatever you think"s in a row = the remaining decisions are below their attention line. Stop the one-at-a-time. Switch to **recommend-and-confirm**: your picks for everything still open, one short list, one yes/adjust. Anything they push on goes back to one-at-a-time.

Same switch applies without the explicit defer: when answers flatten to "fine / sure / yep", their decision budget is spent. Respect it.

## When you're done

Done = you can state the whole plan and you'd bet they'd sign it unchanged. Test it: post the decision log and ask "is this the shared picture?" Yes ends the session. Anything else is your next question.

## The decision log

Every session ends with this — one line per decision:

```markdown
## Decisions

- **Invoices on cancel:** kept, not voided — audit trail
- **Retry policy:** 3 attempts, exp backoff — their call, no strong driver
- **Queue tech:** existing Redis, not SQS — already deployed; scale doesn't justify a migration
```

This log is the artifact. Calling skills (whiteboard, connotation-cop) consume it. Any line that's hard to reverse + surprising later + a real trade-off → offer to make it permanent via the connotation-cop skill's ADR.

## Don't

- **Answer your own questions.** Ask-then-proceed is theater. Wait.
- **Interrogate about facts.** "What framework is this?" — read package.json.
- **Summarize every third question.** Feels thorough, drags hard. One summary, at the end, as the done-test.
