---
name: ideate
description: Generate startup ideas grounded in Hamza's portfolio patterns + current trends. Wraps the idea-generator agent.
---

# /ideate

Usage: `/ideate` or `/ideate <theme>`

## What this does
1. Reads `products/*/product.config.json` to understand portfolio patterns.
2. Invokes `agents/idea/idea-generator/SKILL.md`.
3. Returns 5–10 ranked ideas with the standard format.
4. Ends with one direct recommendation.

## What you do as the assistant when this is invoked
- Read `agents/idea/idea-generator/SKILL.md` and execute its protocol.
- If user provided a theme argument, use it as the constraint; otherwise ask one question about constraint and proceed.
