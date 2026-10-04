---
name: experience-first
description: "Use when a product, UX, or scope tradeoff comes up. Pick what's better for the person using it over what's easier to build. Ship fewer things done well. Remember that many users now bring their own agents."
disable-model-invocation: true
kind: principle
---

# Experience first

The product is what it's like to use it. Every technical decision makes that better or worse. When the easy way to build something makes it worse to use, build it the harder way.

## Who the user is

Whoever ends up with the work. For a UI, the person clicking. For a library or an API, the colleague who imports it. For an MCP or CLI, the agent calling it. The next engineer who maintains the code is a user too. Weigh all of them, and when you explain a change, explain it from their seat.

## Say no

- **Every feature has to earn its place.** Every control, every option, every setting. Default to no.
- **Ship less, ship better.** Three features that feel finished beat ten that feel rough.
- **Their agents will build the rest.** Users have agents now. Before building a feature, ask whether an agent could do it from the pieces you already expose. A reporting feature probably doesn't need to exist. A clean way to pull the data does. Build the pieces, not the feature.
- **Everything serves the core loop.** If a feature doesn't help the main thing people come here to do, it gets out of the way.

## Sweat the details

- **Prototype before you commit.** A design decision is cheaper to make in throwaway HTML than in production code.
- **The small stuff is the experience.** Transitions, alignment, spacing, feedback when something happens.
- **Empty, loading, and error states are real states.** Design them. They're what the user sees first and what they see when things go wrong.
- **Errors are written for the person reading them.** Plain words, name the thing on their screen, keep whatever they typed. "The SPA contract is broken" is a message for us sitting in the user's error slot. If the cause really is internal, say so honestly with a reference ID and put the real cause in the logs.
- **The mouse isn't the only input.** A web flow isn't done until it works keyboard-only. Tab reaches everything in a sensible order, focus is visible, Enter and Space activate, Escape dismisses.

## How this fits with structure-first

Structure first decides the order of the work. This decides what the work is for. Foundations exist to serve the experience, not the other way around.
