---
name: fake-the-affordance-not-the-contract
description: "Use when building anything an agent will use: an MCP, a CLI, an API, a sandbox, a mock environment. It's fine to give the agent a familiar interface that's simpler underneath than it looks. It's never fine to fake durability, isolation, security, persistence, or production readiness."
disable-model-invocation: true
kind: principle
---

# Fake the affordance, not the contract

Agents need tools and instructions, not accurate implementation details or real environments. Agents like working a certain way. Give them that way and they work well. What's underneath can be a mirage as long as the agent gets what it expects and we get outputs that work.

This sounds wrong until you've built for agents. Then it's obvious.

## What you can fake

- **A familiar interface over a different implementation.** An agent expects a filesystem, give it something that answers like one. It expects a database, give it something that takes SQL. What's behind it is your business.
- **A simpler world than the real one.** A "deploy" command that writes to a staging directory. A "send" that logs. A "user" that's a fixture. The agent works the way it knows how.
- **Affordances it asks for.** If agents keep reaching for a command that doesn't exist, build it. It doesn't have to do what the real one would. It has to give the agent what it needed to move on.

## What you can never fake

The contract. These are promises the agent acts on. If a promise is false, the agent's work is wrong in ways nobody catches until it matters.

- **Durability.** If something says it saved, it's saved. If it isn't, say so.
- **Isolation.** If something says this is your sandbox, nothing else can see it or touch it.
- **Security.** If something says this is safe, it's safe. A fake auth check is worse than none.
- **Persistence.** If the agent will assume it's still there next session, it's still there.
- **Production readiness.** If it looks shippable, it's shippable. A mock that could pass for the real thing has to say it's a mock.

## The test

Ask what the agent will do next based on what it just saw. If a false belief about the implementation changes nothing about its next step, fake it freely. If a false belief would make the agent skip a step, trust something it shouldn't, or tell a human something untrue, that's contract, and it has to be real.
