---
name: conversion-ux-review
description: Walk the path from a page's first screen to the action that matters (sign up, book, buy), find where people hesitate or get lost, and fix the friction without dark patterns. Use when traffic is fine but conversions aren't, or before launching a pricing, sign-up or checkout flow.
---

# /conversion-ux-review

Run this in a real browser at 375px and at desktop width, as a first-time visitor, with the network throttled to "Fast 4G".

## 1. Name the action and the path

Write the single action that matters and every screen and step between landing and done: hero → pricing → sign-up → verify → first use. Count the clicks and fields.

## 2. First screen

- **Pass when** the screen says what the product is, who it is for, and the primary action, without scrolling.
- The primary action is the most visible element, worded as an outcome ("Start a free trial"), and stays consistent everywhere.
- There is one primary action per screen; the others are visibly secondary.

## 3. Friction audit, step by step

For each step, record:

- **Doubt:** what might make someone stop here? Price unclear, commitment unclear, missing proof. Answer it right there with a line of copy, a guarantee or an FAQ entry.
- **Effort:** count fields, decisions and waits. Remove optional fields, prefill what you know, and defer what can wait until after sign-up (for example `one-field-sign-in` or `passkey-sign-in` patterns).
- **Errors:** submit empty, invalid and edge-case input. Errors must be specific, appear next to the field, and keep what was typed.
- **Speed:** time each interaction. Anything over ~100ms needs feedback, and anything long needs progress (`relay-button`-style state).

## 4. Pricing clarity

- The price, its period, what's included and what happens at the end of a trial are all visible before sign-up.
- Comparison takes one glance (`subtractive-pricing`, `usage-ruler`), and the recommended plan is marked with a reason.

## 5. No dark patterns

No pre-checked upsells, fake urgency or countdowns, confirm-shaming, hidden cancellation, or a "No" that is harder to find than "Yes". These lift numbers briefly and cost trust; remove any you find.

## 6. Measure

Define the event for each step, and confirm it fires once, at the right moment, in the production build. A review without measurement is a guess.

## Output

The path map with click and field counts, a friction table (step · issue · evidence · fix), the fixes applied, and the before/after counts.
