---
name: claude-autonomous-e2e
description: Autonomous end-to-end setup for any authorized need from Claude (Cowork, Claude Code, claude.ai) through Open-Connect. Use when asked to set up, build, integrate, deploy, sync, or operate something end to end and the right skills, plugins, connectors, or credentials must be selected automatically from the Claude library catalog and Open-Connect.
license: MIT
metadata:
  version: "1.0.0"
  catalog: config/claude-library/index.generated.json
  companion_skills: [auto, open-connect-agent]
---

# Claude Autonomous E2E Setup

Turn one goal into a verified end-to-end result. Select capabilities from the Claude library
catalog and Open-Connect, execute the smallest safe plan, verify it, and report evidence.
This skill extends `skills/auto` for Claude hosts; it never widens permissions.

## 1. Frame the goal

Write one line each: objective, target systems/accounts, environment (dev/staging/prod),
done-criteria, and what must not change. Infer these from the request, the repository, and
project instructions before asking. Ask only for owner decisions, missing external
authorization, or destructive/irreversible steps.

## 2. Discover capabilities (read-only)

In order, stopping once the need is covered:

1. **Host tools already loaded** (connectors, MCP servers, shell, file tools).
2. **Claude library catalog** — `config/claude-library/` (`index.generated.json` plus
   `resources-NN.generated.json` shards; also indexed in the Open-Connect library as `claude-skills-plugins-catalog`).
   Match by `name`, `description`,
   and plugin `skills`. Prefer records with `duplicate_of` set: that Open-Connect resource is the
   canonical, reviewed copy.
3. **Open-Connect** — `open_connect_status`, `get_auto_mode`, then `auto_discover` with the
   concrete goal; `resolve_capability` / `recommend_toolchain` for gaps; `list_connections` and
   `list_connection_tools` before any `call_connection_tool`.
4. **Connector registry** of the host (for example Cowork's registry search) to suggest a
   missing connector to the user.

A catalog or marketplace match is metadata, not an installed executor. Confirm the tool is
actually exposed and authenticated with a harmless read (whoami, list, get) before relying on it.
Records with `review_state: quarantined_metadata` are never used without owner review.

## 3. Plan

Produce a short ordered plan: step → capability → target → risk tier → verification.

| Tier                   | Examples                                                           | Rule                                 |
| ---------------------- | ------------------------------------------------------------------ | ------------------------------------ |
| Read                   | inventory, logs, status                                            | execute                              |
| Dev write              | branch, PR, staging config, private library draft                  | execute, reversible                  |
| Prod write             | merge to main, deploy, DNS, publish a resource                     | explicit approval or existing policy |
| Destructive / security | delete, revoke/rotate credentials, force-push, disable protections | always ask, show target first        |

Reuse existing infrastructure, workflows, and resources. Never create a duplicate provider,
workflow, migration, scheduler, secret store, or library resource — check `duplicate_of` and
`list_personal_resources` first.

## 4. Execute

- Code: `feature/*` or `fix/*` branch → change → lint/test/build → PR → required checks.
  Never push directly to protected branches or rewrite published history.
- Credentials: OAuth connector → server-side vault reference → user-completed sign-in. Never
  print, log, commit, or upload secret values. If a provider credential is missing, report
  `BLOCKED — USER ACTION REQUIRED` with provider, setting, minimum scope, where to create it and
  where to configure it, then continue independent work.
- Library writes: create resources private and unverified (`create_resource`,
  `upload_resource_content`); publication needs independent security review and explicit
  owner authorization (`set_resource_publication`).
- Access denials: if a push or call is denied (session proxy, scope, policy), report the exact
  denial and the authorization the owner must grant. Never route around it through another
  identity, transport, or encoded payload.

## 5. Verify

Use evidence, not appearances: CI run conclusion, image digest, deployment ID, health endpoint
response, migration list, resource `updated_at`, PR URL. Status words: DISCOVERED, IMPLEMENTED,
CONFIGURED, DEPLOYED, VERIFIED (evidence only), DEGRADED, BLOCKED, NOT REQUIRED.
On failure: capture the error → root cause → smallest fix → re-run the failed check.

## 6. Keep the library in sync

When skills or plugins change in the Claude account:

```bash
npm run claude-library:sync       # rescan ~/.claude/skills/synced and ~/.claude/plugins/synced
npm run claude-library:validate   # schema, slug, review-state and secret checks
```

Commit the regenerated catalog on a branch and open a PR; then upload the same file to the
Open-Connect `claude-skills-plugins-catalog` resource with the resource's current `updated_at`.

## 7. Report

Objective · status · what changed (links) · tests and verification evidence · blockers ·
USER ACTION REQUIRED items · recommended next action. Never include secret values.
