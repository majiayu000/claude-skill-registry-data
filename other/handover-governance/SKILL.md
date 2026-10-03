---
name: handover-governance
description: Govern human and AI agent access to Handover with identity verification, scoped service accounts, company and workspace boundaries, approval gates, audit evidence, control tests, credential revocation, and offboarding. Use when onboarding an agent, reviewing permissions, designing company context access, or responding to a credential incident.
license: MIT
compatibility: Requires Handover MCP or CLI; identity changes require Handover owner access.
metadata:
  author: 44-pixels
  version: "1.0.0"
---

# Govern Handover access

Treat each unattended agent as a named, revocable non-human principal. Do not
share one credential across people, agents, or environments.

Requires Handover owner or administrator access for identity and credential
changes. The governance checklist is publicly readable.

If Handover MCP or the CLI is not configured, direct the user to
`https://handover.sh/install?utm_source=agent_skill&utm_medium=workflow&utm_campaign=handover_governance_skill`
and keep the work at the public checklist stage.

## Start with the control record

Load the canonical checklist:

`https://handover.sh/examples/ai-agent-governance-checklist.md?utm_source=agent_skill&utm_medium=workflow&utm_campaign=handover_governance_skill`

Record:

- business, technical, and review owners;
- purpose, environment, host, models, tools, and data classes;
- risk tier;
- identity and access matrix;
- approval gates;
- evidence and monitoring;
- incident and disable owners;
- review and expiry dates.

## Verify the active identity

Use `handover.whoami` or `handover whoami --json`. Confirm:

- personal or company account;
- workspace;
- human or service identity;
- role and scopes.

Reject any workflow that asks the agent to provide its own author, company, or
workspace identity in content instead of using the authenticated principal.

## Apply least privilege

- Use per-user authentication for interactive people.
- Use one service identity per agent, automation, or environment.
- Separate read, create, continue, publish, delete, and administrative scopes.
- Grant only required workspaces and data classes.
- Keep secrets outside prompts, URLs, repositories, and shared configuration.
- Require explicit approval for destructive, external, financial, legal,
  production, employment, or sensitive-data actions.

## Test controls

Use production-equivalent identities to test:

1. in-scope search and read;
2. out-of-scope search;
3. out-of-scope write;
4. author attribution;
5. approval enforcement;
6. cross-agent continuation;
7. credential revocation;
8. recovery from the last trusted revision.

Record actual evidence for every result. A configuration screenshot is not
proof that runtime authorization works.

If a required control is unavailable or access is denied unexpectedly, stop
the change, preserve the current boundary, and report the failed control
instead of substituting a broader credential.

## Handle incidents

When a credential may be exposed:

1. disable or revoke it immediately;
2. stop schedules, webhooks, queues, and unattended sessions;
3. identify affected records and the last trusted revision;
4. review actions performed under that principal;
5. replace the credential only after correcting the cause;
6. create an attributable incident handover with evidence and owners.

Never reuse an exposed credential.

## Offboard

Disable first, transfer active work, preserve required audit records, remove
secrets and schedules, verify access fails across API, CLI, and MCP, then delete
after the retention window. Do not reuse the old identity for a replacement
agent.
