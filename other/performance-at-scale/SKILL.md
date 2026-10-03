---
name: performance-at-scale
description: Use when writing code that runs per item, per frame, or per event, or building a cache or lookup over a collection that can grow large.
---

## The rule

Hot-path code meets your data at production scale, not at the handful of rows in your test fixture. A linear scan that's instant on ten items freezes the UI on a hundred thousand. The cost is invisible in the test and brutal in the field. Design the hot path for the largest realistic input before you write it, not after a user reports a freeze.

## Fires when

Writing code that runs per item, per frame, or per event. Building a cache or a lookup. Iterating a collection that could grow large. Rebuilding a whole list when one entry changed.

## How to apply

Before writing data-path code, ask "does this hold at the largest realistic input?"

Use O(1) lookups with an early exit — a map keyed by the thing you're asking about, so 99% of queries return immediately. Prefer incremental point updates (remove one, add one) over rebuilding the whole structure. Keep allocations and copies out of tight loops. Verbose logging in a hot loop is fine, but only after the early exit, never before it.

If the answer is "no, it won't scale", redesign before you write it, not after.

## Worked example

A handler runs once per tile and scans a flat list of issues linearly to find the ones that match. With a dozen issues in the test, it's instant. In a real project the list holds four thousand issues, and every tile now costs a one-to-two second freeze. Keyed into a map by tile, each query early-exits in O(1) and the freeze is gone. The scan looked fine because the test never had enough data to make it hurt.

## Red flags

| Thought | Reality |
|---|---|
| "It's fast enough" | Fast on the fixture, frozen at scale. |
| "I'll rebuild the whole list, it's simpler" | Simpler to write, O(N) to run every time. |
| "Just loop and find it" | A linear scan on a hot path is a freeze waiting for data. |
