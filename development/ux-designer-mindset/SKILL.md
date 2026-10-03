---
name: ux-designer-mindset
description: Use when building or changing anything a user interacts with - a control, a screen, a flow.
---

## The rule

A feature that compiles and returns the right value can still feel broken. Before you implement, walk the interaction the way the user lives it; after, check the states you didn't design for. A green build tells you the code runs — it tells you nothing about how the thing feels under a real hand.

## Fires when

Building or changing any control, screen, or flow a user interacts with.

## How to apply

Before coding, narrate the interaction: "user does X, sees Y, expects Z" — and flag every gap where Y or Z is missing. After coding, walk the edge states you didn't design for: empty, zero results, a hundred thousand results, rapid repeated clicks, first run versus returning, panel closed versus open. Every clickable control must give feedback (a hover state, a cursor change), and you verify that in the running app — in many UI frameworks a bad style name silently falls back to a default and the build stays green either way. Offer the small touches that show care, like a count on hover or a brief fade.

## Worked example

A toolbar icon is wired to its action and compiles cleanly, but it's drawn with a borderless style — no hover highlight, no cursor change. It works when clicked, yet it reads as dead, and users stop trusting that it does anything. Switching to a real button style and checking the hover and cursor live in the running app fixes the feel. The green build had nothing to say about it, because nothing about feel shows up at compile time.

## Red flags

| Thought | Reality |
|---|---|
| "It compiles and returns the right value" | Correct and broken-feeling are not exclusive. |
| "The button's wired up" | Wired up but dead-looking reads as broken. |
| "I'll just check it built" | A build proves the code runs, not how it feels. |
| "Nobody clicks twice" | Someone always clicks twice. Handle it. |
