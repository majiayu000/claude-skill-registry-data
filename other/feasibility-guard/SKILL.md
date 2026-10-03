---
name: feasibility-guard
description: Use when about to build or agree to build a feature, test, or check, especially when the request sounds big or clever.
---

## The rule

Not every request should be built as asked. Before you start, weigh the cost against the value. If the feature is over-engineered, say so and propose the smaller thing. Same when a test could only exist on a pile of mocks, or a check would drown the user in false positives. Agreeing to bad work quickly is not helping.

superpowers' brainstorming explores what to build; this skill is the license to answer "nothing" or "less".

## Fires when

About to build a feature, write a test, or add a check — especially when the request sounds big or clever, or you catch yourself reaching for a lot of mocking and scaffolding.

## How to apply

Ask "is this worth the effort, and will it actually work?" before you start.

Flag a test that would be fragile or need mocking half the system, a check that would fire mostly false positives, complexity that outweighs its benefit. Offer the smaller version, or say skip it.

Don't just agree because it was asked.

## Worked example

You're asked to add a test for a function, but covering it properly would mean mocking the database, the clock, the network, and three collaborators, and the test would break on any refactor. That's a fragile test that protects almost nothing. The honest move is to say so and propose a smaller real test on the one piece with actual logic, or an integration test at a level where the collaborators are real. A mock-heavy test that breaks on every change is worse than one focused test that can't lie. (What makes a test worth having is tests-with-teeth's territory; this rule is about saying no before the work starts.)

## Red flags

| Thought | Reality |
|---|---|
| "They asked for it, so build it" | Asked is not the same as worth it. |
| "I'll just mock everything" | A test held up by ten mocks is testing the mocks. |
| "More coverage is always better" | Coverage of the wrong thing is just noise. |
