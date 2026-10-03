---
name: plan-with-teeth
description: Use when about to write an implementation plan, scope a multi-step change, or enter plan mode - before any plan text exists. Also fires when reviewing a plan that states what code does without evidence behind it.
---

## The rule

A plan is a stack of claims about code, and every claim is either read from the source this session or it is a guess. Plans built on guesses don't fail at the whiteboard; they fail at step 3 of the implementation, where rework is expensive. Read first, label what you didn't read, and attack your own draft before anyone else sees it.

This sharpens superpowers' writing-plans: that skill gives a plan its shape and process, this one keeps its content honest.

## Fires when

Writing an implementation plan or design note, entering plan mode, answering "how would we build this?", estimating the size of a change, reviewing someone else's plan.

## How to apply

1. Read every file the plan touches before writing a step about it. A claim about the codebase carries a file:line reference. Not read this session means not known.
2. Open the plan with an assumptions ledger. Mark each entry [VERIFIED file:line] or [HYPOTHESIS]. A load-bearing hypothesis gets resolved by reading the code or asking; it never gets built on silently.
3. Bring two or three genuinely different approaches, with cost, risk, and blast radius. Say why the losers lose. A one-approach plan is a draft.
4. End every step with how you'll know it worked: a command, a test, an observable behavior. A step with no check is a hope.
5. After drafting, attack the plan: which edge case kills it, which file did you not open, what does rollback look like, what would a reviewer bounce. Fix what you find, then show it.

Anything still unverified in the final plan stays labeled a hypothesis. A wrong plan costs more than a slow one, so think as long as it takes.

## Worked example

Task: "plan rate limiting for our public API." The plan from memory says: add middleware, configure limits, write tests. Three steps, one approach, nothing checked. The plan with teeth starts by reading the request path and finds a response cache sitting above the middleware chain (`gateway/cache.ts:88`), so naive middleware would count cache hits against the limit. Its ledger holds "[HYPOTHESIS] every endpoint goes through the main router" — checked, and false: the websocket upgrade path skips it. It weighs an in-process token bucket against gateway-level limiting and picks the gateway, because the service runs six replicas with no shared state. Each step ends with a check ("hit the endpoint 30 times, read the 429 body and the Retry-After header"). The cache and the websocket path are exactly the two surprises the from-memory plan would have met mid-implementation.

## Red flags

| Thought | Reality |
|---|---|
| "The task is simple, I don't need to read first" | Simple tasks hide the same landmines. Reading costs minutes; a wrong plan costs the rework. |
| "I remember how this code works" | Your memory is from another session or another version. Read it again. |
| "I'll verify the details during implementation" | By then the plan has committed you to an approach. Mid-implementation is the expensive place to be surprised. |
| "The alternatives are obviously worse" | Then writing them down costs two lines and proves it. Write them. |
| "The attack pass is a formality" | The attack pass is where plan bugs die cheaply. Skipping it moves them into the code. |
