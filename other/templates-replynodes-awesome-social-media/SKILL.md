---
name: Skill Name
description: One sentence describing what this skill does and the outcome it produces.
version: 0.1.0
author: your-name-or-handle
license: MIT
category: content-strategy
platforms: [x, linkedin, instagram, tiktok, youtube, threads, reddit, facebook, bluesky, mastodon, agnostic]
agent_compatibility: [agent-agnostic]
tags: [tag-one, tag-two, tag-three]
---

# Skill Name

## Purpose

What this skill does and the specific outcome it produces. One or two
sentences — a reader should know whether this is the skill they need
without reading further.

## When to use

- The situation or trigger where this skill applies
- A second situation, if relevant
- What this skill is *not* for (optional, if there's a common mix-up)

## Inputs

What the agent or user needs to provide before running this skill.

| Input | Required | Description |
|---|---|---|
| `example_input` | Yes | What it is and where it comes from |
| `optional_input` | No | What it changes when provided |

## Instructions

Step-by-step instructions an agent can follow directly. Be specific enough
that two different agents running this skill on the same inputs produce
comparable output.

1. First step
2. Second step
3. Third step

## Output format

The exact structure the skill should produce — field names, format, length
constraints. Show the shape, not just a description of it.

```text
Example output structure
```

## Examples

A realistic input and the output it produces. At least one full example.

**Input:** ...

**Output:** ...

## Safety and quality checks

- What the agent should verify before finalizing output (facts, claims, tone, length limits)
- What this skill must never claim or promise (e.g. no guaranteed engagement or virality)
- Any platform policy or compliance considerations relevant to this skill

## Related skills

- [`related-skill-one`](../category/related-skill-one.md) — how it connects
- [`related-skill-two`](../category/related-skill-two.md) — how it connects
