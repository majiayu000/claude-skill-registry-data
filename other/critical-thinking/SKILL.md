---
name: critical-thinking
description: Use when about to build something someone proposed, especially when the proposer sounds confident and the idea sounds obviously fine.
---

## The rule

A proposal that sounds reasonable can still be wrong, and the person proposing it, often the user sounding sure, can't always see the flaw. Before you build what was asked, run the idea through one concrete example. If the example breaks, stop and say so. Building first and finding the flaw later wastes everyone's time, and "they sounded confident" is not a reason to skip the check.

This sharpens superpowers' brainstorming: brainstorming explores what to build; this is the one-example probe it doesn't mandate.

## Fires when

Someone proposes a rule, a filter, a UX behavior, or a piece of logic and you're about to implement it. Strongest when the proposer is sure and the idea sounds obviously fine.

## How to apply

Pick one concrete case and walk the proposal through it, out loud. Use a case that stresses the edges, not the happy path. If the proposal produces a wrong or surprising result, name it plainly and explain the case before writing code. Offer the fix or ask the question. Don't implement first and find the flaw in testing.

## Worked example

A user asks for a filter: "show only the highest-severity issue per file." Reasonable on its face. Run one example. A file has one critical bug and one minor one. Now the user switches to cleaning up minor issues and filters for them. That file vanishes from the minor filter, because its highest severity is critical. The filter hides the very things the user is trying to find. You caught a real regression with one example, before a line of code. The confident phrasing of the request didn't make it correct.

## Red flags

| Thought | Reality |
|---|---|
| "They asked for it and they sound sure" | Confidence isn't correctness. Run the example. |
| "It's obviously fine, I'll just build it" | Obvious ideas fail on the case you didn't picture. |
| "I'll catch problems in testing" | Testing a flawed design just confirms the flaw works. |
