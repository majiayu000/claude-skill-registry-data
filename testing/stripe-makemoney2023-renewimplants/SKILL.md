---
name: stripe
description: >-
  Use when integrating or reviewing Stripe payments, Connect, or billing patterns via Stripe plugin skills.
---

# Stripe

Thin adapter for digital workers. See `skills/org/TOOL-REGISTRY.md`.

## Preferred access
Stripe plugin skills (`skills/plugins/stripe/`)

## Env / secrets
Stripe secret/publishable keys via secrets — never hardcode

Resolve via `skills/integrations/obsidian-secrets/` then `.env.local`.

## MCP
Stripe plugin MCP if configured

## Primary ops
1. Follow stripe-best-practices skill before code changes
2. Use test mode keys unless production explicitly requested
3. Finance seats: reconcile with exports, not guessed MRR

## Fallback
Stripe Dashboard exports

## Common failures
Live key in client → stop and rotate
