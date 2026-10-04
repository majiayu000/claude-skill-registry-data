---
name: build-primitives-not-features
description: "Use when scoping a product or deciding whether to build a feature. Users have agents. Expose the data and the operations, and let their agents build the feature. Say no to the feature, yes to the primitive that makes it possible."
disable-model-invocation: true
kind: principle
---

# Build primitives, not features

Our users have agents. Most of what used to be a feature request is now something their agent can do, if we give it the pieces. So before building a feature, ask whether an agent could build it from what we already expose. If yes, don't build the feature. Build the missing piece, if any, and stop.

This sounds like the opposite of bold. It isn't. Bold is building the pieces nobody else has. Timid is building the same reporting screen everyone else has.

## The example

Every project eventually wants reporting. Should we build a reports feature? Probably not. Should we expose a way to pull the data efficiently, with filters, in a shape an agent can work with? Yes. The user's agent then builds the report they want, which is never the one we would have guessed.

## What a primitive looks like

- **Data out, in a useful shape.** Filtered, paged, typed. JSON an agent can parse, not a table it has to scrape.
- **Operations in, one thing each.** Create, update, delete, run. Small, composable, safe to retry.
- **Errors an agent can act on.** A stable code, what was wrong, what was expected, a corrected example.
- **Nothing that assumes a human is clicking.** No wizard, no multi-step modal, no "are you sure". The agent will ask its human if it needs to.

## What this is not

It isn't an excuse to ship nothing. Some things are a feature because the experience is the point and an agent can't provide it: a polished editor, a fast search box, the core loop of the product. Those get built, and built well. This rule is about the long tail around the core, where most feature creep lives.

## The test

Describe the feature request as an agent prompt. "Pull last month's usage per customer and make a chart." If our product already gives an agent everything it needs for that, the feature exists. If one call is missing, build that call. If the prompt can't be written because the experience is the point, it's a real feature.
