---
name: open-connect-agent
description: Coordinate ChatGPT, Claude, Grok, Mistral, Kimi, Manus, and Hermes/Open-System through the Open-Connect control plane for shared project planning, coding, review, testing, scheduling, memory, and audited delivery.
---

# Open-Connect Agent

Use Open-Connect as the commander and Open-System/Hermes as the execution supervisor.

## Operating sequence

1. Resolve organization, workspace, project, task, and environment.
2. Retrieve only relevant knowledge and prior run evidence.
3. Build a bounded plan and classify each action by risk.
4. Route work by capability, health, cost, latency, quota, and data policy.
5. Give each provider the minimum context and opaque credential references only.
6. Run code in isolated workspaces and use feature branches.
7. Require independent review and automated tests before promotion.
8. Pause for approval on production, destructive, billing, credential, identity, permission, DNS, or public-release actions.
9. Record outputs, decisions, evidence, costs, failures, and reusable memory.

Never place tokens, passwords, session cookies, private keys, or recovery codes in prompts, logs, repositories, skills, or artifacts. A provider marked authorization-required is unavailable until its owner completes OAuth/API authorization.

## Repair access and connector readiness

Read [admin access](references/admin-access.md) for OAuth, host approval settings, credential management and tool refresh.

Inspect the active key's actual scopes and project context before invoking private knowledge, memory, or provider writes. A Developer profile includes memory/knowledge reads and normal execution scopes; Administrator adds `control:write` and still requires the account's real Admin role. A key profile never grants another tenant's membership or a provider's OAuth permission.

Use the signed-in Integrations → AI agents key card to select an existing active key and Apply permissions. This invokes `oc_update_owned_key_access` through authenticated owner management, preserves its secret, project context and expiry, and records previous/next permissions in the control audit ledger. Restore supported prior grants through the same operation for rollback. Legacy profiles use Custom with supported prior scopes; wildcard and obsolete grants cannot be restored. Do not edit revoked/expired keys or rotate them to hide an access error.

Run `scripts/open-connect-access-check.mjs` through the existing `open-connect-plugin` credential profile, adding `--scope knowledge:read --scope memory:read` and the exact `--project-id` for a project runtime. The check performs one fixed-origin request and reports metadata only. Wait up to 30 seconds for a committed permission change to clear the existing authentication cache; then verify the original MCP tool. Never read knowledge through SQL to bypass a missing scope.

Classify failures: missing credential/configuration, invalid/expired key, insufficient scope, project mismatch, provider consent, or transport/edge denial. A plain-text403 is not proof of a key-scope error. Preserve response metadata and inspect the authorized gateway/edge configuration; do not choose an alternate credential, proxy, or unbounded retry.

Keep existing source databases authoritative while Open-System schema reconciliation is pending. Carry organization/project/source IDs, owner, visibility, version and source link in the catalog; keep restricted KobePlay finance and client records inside their authorized source boundaries. Uploaded private keys are credential material and must not enter skill packages or knowledge.
