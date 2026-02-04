---
name: prompt-shaping
description: Propose structured interpretations of underspecified requests. Use when a user's request is vague or incomplete but reasonable assumptions can be made. Rapidly prototypes intent by restating, structuring, and committing to a next action.
---

# Prompt Shaping

Rapid prototyping of user intent through structured proposals.

## When to Apply

User request is underspecified but agent can infer plausible intent.

## Process

1. **Restate in natural language** - Articulate what you understand the user wants, making assumptions explicit
2. **Bullet the structure** - Break the restatement into scannable components
3. **Propose a grounding loop** - Define how you will verify the work is complete
4. **State the next action** - Commit to a concrete step if the interpretation is correct

## Grounding Loop

Before committing to action, propose how you will verify completion:

- **Define success criteria** - What observable outcome proves the request is fulfilled?
- **Propose a verification method** - A concrete check the agent can execute (test, command, assertion)
- **Commit to iteration** - Run the verification repeatedly until it passes

The grounding loop ensures the agent doesn't just claim success—it demonstrates success through executable feedback.

Example proposals:
> "I'll add the API endpoint, then write a test that calls it and asserts the expected response. I'll iterate until the test passes."

> "I'll fix the bug by first writing a failing test that reproduces it, then modifying the code until the test passes."

> "I'll refactor the module, running the existing test suite after each change to ensure no regressions."

The loop terminates when the verification passes, not when the agent believes the work is done.

## Example

> **User**: "I want to add some kind of caching"
>
> **Agent**: "It sounds like you want to reduce redundant computation or network calls by storing results temporarily. I'm assuming:
> - In-memory cache (not distributed)
> - Cache invalidation on write
> - For the API layer, not the database layer
>
> If this is correct, I'll start by adding a simple LRU cache wrapper around the API client."

## Context Grounding

Before proposing, orient to the environment:

- Scan for existing patterns that inform reasonable defaults
- Note what's present that the proposal should integrate with
- Identify constraints the user may not have stated but likely expects
