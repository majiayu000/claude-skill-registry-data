---
name: forge-security
description: Enforces security guardrails for Claude Code. Blocks access to secrets, credentials, and sensitive files. Requires confirmation for network requests and infrastructure changes. Use when accessing files, making network requests, or running infrastructure commands.
---

# Security Guardrails

## Blocked Operations (NEVER do these)

The following are blocked without exception:

- Reading or writing `.env` files
- Accessing files matching: `*secret*`, `*credential*`, `*password*`, `.aws/*`, `.ssh/*`, `*token*`
- Running destructive IaC commands without explicit user request

See [reference/blocked-patterns.md](reference/blocked-patterns.md) for complete list.

## Ask First (require user confirmation)

These operations require explicit user approval:

- Network requests (WebFetch)
- Git push, merge, rebase operations
- Infrastructure commands: terraform plan/apply, kubectl apply, ansible-playbook

See [reference/ask-patterns.md](reference/ask-patterns.md) for complete list.

## When Uncertain

If unsure whether an operation is safe:

1. Stop and explain what you're about to do
2. List what files/systems will be affected
3. Wait for explicit user confirmation

Never assume permission. When in doubt, ask.
