---
name: ground-discovery
description: Research before implementation. Reading before writing.
---

# Skill: Discovery

> "The elegant solution exists. It is waiting to be discovered."

## When

Before writing any code. Before proposing any solution. Always.

## The Protocol

1. **Official Docs**: "What does the documentation say?" -> Read the official source first.
2. **Framework**: "How does the framework solve this?" -> Read the framework source.
3. **Project**: "How did we solve this elsewhere?" -> `grep` the domain.
4. **Package**: "How does the package expect to be used?" -> Read source, not assumptions.
5. **MCP**: If available, use `model-info`, `search-docs`.

## One sample is not a state

A thing read once is a moment, never a condition. **Read it twice before you name it.**

Stuck and slow look identical in one look. So do finished and dead. Naming the wrong one sends the
next hour after a cause that was never there.

If it moved, it is working. If it did not, say what you expected to move and by when.

## The Verification Rule

> **Never assume. Always verify.**

Before claiming something works a certain way:
- Fetch the official documentation
- Read the actual implementation
- Test the behavior if uncertain

A confident wrong answer is worse than admitting uncertainty.

## The Anti-Patterns

- **Assuming**: Believing you know how something works without checking.
- **Guessing**: Assuming a capability exists without verification.
- **Hallucinating**: Inventing configuration options or behaviors.
- **Copy-Pasting**: Using generic examples instead of project patterns.
- **Rushing**: Proposing solutions before understanding the problem.

## The Marination

Complex problems need time to settle. Before proposing:
1. **Pause**: Is this the right approach?
2. **Research**: What do the docs say?
3. **Verify**: Does it actually work this way?
4. **Then propose**: With evidence, not assumptions.

## The Output

State: "Discovered: [N] patterns in `Domain/X`. Using `Y` as reference."
Or: "Verified against [source]: [finding]."
