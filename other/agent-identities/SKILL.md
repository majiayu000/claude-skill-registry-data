---
name: agent-identities
description: Apply per-archetype Git identity and visible posting identity conventions for delivery agents. Use when agents make commits, PR updates, or issue comments so authorship and responsibility remain obvious to human reviewers.
---

# Agent identities

## Purpose
Make it obvious which agent archetype authored a commit or GitHub-visible post.

## Git commit identity rule
Each agent should use a Git identity in this format:

`<Name> (<Archetype>) <bot-<archetype-slug>@<operator-email-domain>>`

Example:
- `Orchestrator (Orchestrator) <bot-orchestrator@example.com>`

The operator email domain comes from `config/framework.yaml`.

## GitHub comment/post signature rule
Every issue comment, PR comment, or substantive PR body update posted by an agent should begin with a visible header:

`> _posted by **<Archetype>**_`

Example:
- `> _posted by **Orchestrator**_`

## Guidance
- keep the visible header at the top of each substantive comment or post
- use the archetype name, not just the agent's personal name
- keep Git identity and visible post signature consistent with each other
- treat these conventions as part of delivery traceability, not cosmetic garnish
