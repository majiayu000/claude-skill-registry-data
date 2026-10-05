---
name: wrangler
description: Use when deploying, developing, or managing Cloudflare Workers and related resources with Wrangler.
runtime_projection: true
source_of_truth: registry/skills/wrangler/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/wrangler/SKILL.md`
> Source of truth: `registry/skills/wrangler/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
# Wrangler CLI

## Use This Skill

- When you are working with `wrangler` commands, config, secrets, migrations, or deployment flows.
- When you need a current `wrangler.jsonc` shape, deployment flags, or local-dev workflow.

## First Check

- Run `wrangler --version`.
- If Wrangler is missing, install it with `npm install -D wrangler@latest`.

## Core Rules

- Prefer `wrangler.jsonc` over TOML.
- Keep `compatibility_date` recent.
- Run `wrangler check` before deploys.
- Run `wrangler types` after config changes.
- Use environments for staging and production.
- Use `remote: true` only when you need real bindings during local development.

## Core Commands

- `wrangler dev`
- `wrangler deploy`
- `wrangler deploy --dry-run`
- `wrangler types`
- `wrangler check`
- `wrangler tail`
- `wrangler whoami`

## References

- Use the official Wrangler docs when flags or config fields matter.
- Prefer retrieval over memory for config schema details.

## Related Skills

- Use [cloudflare](../../../registry/skills/cloudflare/SKILL.md) for broader Cloudflare product routing.
- Use [building-mcp-server-on-cloudflare](../../../registry/skills/building-mcp-server-on-cloudflare/SKILL.md) when the Worker is an MCP server rather than a general Worker app.
