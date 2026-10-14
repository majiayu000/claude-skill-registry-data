---
name: craft-readme
description: How to craft a README. Direct, minimal, clear.
---

# Skill: Craft README

> "Every word earns its place."

## The Voice

From `output-styles/craftsman.md`:

- **Direct** — Say what you mean. No hedging.
- **Brief** — Trust the reader. Don't over-explain.
- **Specific** — Name the problem. Name the solution.
- **Show** — Code speaks louder than prose.

## The Anti-Patterns

| Don't                                           | Do                             |
|-------------------------------------------------|--------------------------------|
| "This is a belief system—a conviction that..."  | State what it does.            |
| "We don't build features. We craft solutions."  | Show the solution.             |
| "The patient, deliberate pursuit of excellence" | Be excellent. Don't say it.    |
| Walls of text explaining why                    | Short paragraph + code example |
| Tables for everything                           | Code blocks for lists          |

## The Check

Before finishing:
- Can any sentence be deleted without losing meaning?
- Is there preaching? Remove it.
- Are there examples? There should be.
- Would the reader approve?

## Templates

| Template                               | Use When                 |
|----------------------------------------|--------------------------|
| [namespace.md](templates/namespace.md) | domain or support README |
| [plugin.md](templates/plugin.md)       | Plugin README            |

## Registration

Add `craft-readme` to agents that write documentation:
- `agents/architect.md`
