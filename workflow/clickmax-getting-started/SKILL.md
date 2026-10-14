---
name: clickmax-getting-started
description: Use when the user asks what to do next, how far along the account setup ("Primeiros passos") is, or right after the conversation finished a setup task (product, offer, page, funnel, channel, automation, quiz, lesson, pipeline, opportunity) and the next pending setup task may be offered.
---

## When this applies

- The user asks what to do next, where to start, or how much of the setup is left.
- A setup task was just completed in this conversation (created the first product or offer, published a page, created a funnel, connected a channel, created an automation, published a quiz, added a lesson, created a pipeline or an opportunity) and the task the user asked for is fully done.

Not this skill:

- how to do each task -> the domain skill (`clickmax-products`, `clickmax-offers`, `clickmax-pages`, `clickmax-funnels`, `clickmax-flows`, `clickmax-forms-quizzes`, `clickmax-members-area`, `clickmax-pipelines`)
- whether payments can be received yet -> `clickmax-wallet-receivables`

## Key assumptions

- The checklist has four steps in a fixed order: have something to sell -> build the storefront -> talk to whoever arrives -> close the sale. `next` is always the first pending task in that order.
- Progress is recorded by the platform when the action happens, not when the user says so. A task done a moment ago may take a few seconds to show as done; never argue with the user about it.
- `allDone = true` means every visible task is done — there is nothing to offer.

## Thought process

1. Finish what the user asked first. The next-task offer is an optional closing line, never a replacement for the requested work.
2. Only after a setup task completed (or when asked about progress), read `mcp__plugin_clickmax_clickmax__onboarding_progress_get`.
3. IF the user's request was unrelated to setup (analytics, support, a question about a lead) -> do not read progress and do not offer anything.
4. IF `next` is the task just completed (not yet reflected) -> skip the offer this turn instead of repeating it.

## Execute guide

- Read progress with `mcp__plugin_clickmax_clickmax__onboarding_progress_get` (no input). Use `next.task` as the basis of the one-line explanation, rewritten in the user's language.
- Progress question -> answer with done/total per step in order, then the next task.
- After a completed setup task -> end the reply with ONE short call to action offering `next`: what it is in one line and an offer to do it now. Example shape: "Next step: publish a sales page for this product. Want to do it now?"
- If the user accepts, switch to the domain skill for that task.

## Report

- At most one call to action per reply, as the last line, opt-in only.
- Describe tasks in plain words; never show milestone keys, step ids, or raw counts payloads.
- `allDone` -> say nothing about the checklist (no congratulations banner, no "all done" line) unless the user asked about progress.

## Warnings

- Never push the next task when the user asked for something else, is mid-task, or just declined it in this conversation.
- Never offer more than one task, and never list the whole checklist unprompted.

## Anti-patterns

- Opening the reply with the checklist instead of the requested result.
- Offering the task that was just completed because progress had not refreshed yet.

---

Clickmax skill revision: `b8294822a4d6`
