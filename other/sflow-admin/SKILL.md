---
name: sflow-admin
description: Diagnose and administer Singularity Flow configuration, workspace upgrades, agents, Jira, state planes, and recovery.
disable-model-invocation: true
argument-hint: "[doctor|configuration|migrate-schemas|reinitialize [WORKSPACE]|agents|jira|state|recovery]"
---
# Administer Singularity Flow

<!-- sflow-output-contract: guided-actions -->
**Output contract:** Use read-only CLI evidence, preserve warnings and ordered actions, and change nothing unless explicitly requested.
<!-- sflow-execution-boundary -->
**Boundary:** machine-local; no repository or Story required. Use explicit arguments or SFlow-returned paths; never search `$HOME` or infer a repository.

1. Route configuration to `singularity-flow configuration`, workspace selection to `/sf-workspace`, agents to `singularity-flow agents status`, and Jira to `singularity-flow jira doctor`.
2. For schema migration or compatibility, run `singularity-flow workspace migrate-schemas --json` once. It checks every active registered workspace repository and migrates supported records in memory. Show coverage, migrations, skips, and blockers. State that stored records remain unchanged; machine-local, workspace-private, content-addressed, and unmapped records are excluded.
3. For reinitialize or post-install upgrades, run `singularity-flow workspace list --json` and `singularity-flow workspace current --json`. Ask for one scope: all registered workspaces, one returned workspace ID, or returned repository IDs. Never infer the scope from the current directory, active Story, chat history, or similar names.
4. Build the preview from that exact selection and run it once:

   `singularity-flow workspace reinitialize [WORKSPACE-ID] [--repository REPOSITORY-ID]... --dry-run --json`

5. Show scope, plan ID, changes, collisions, census, migrations, blockers, warnings, and next action. Preview changed nothing. Reinitialize restores only missing or exact registered framework seeds and preserves user-created or user-modified workflows, phases, artifact sets, templates, prompts, and agents; historical durable records are never rewritten. Never offer `--resolve ...=bundled` or `--accept-bundled-conflicts` here. For deliberate replacement of repository-owned content, present `/sf-refresh-configuration` (Shell: `singularity-flow workspace refresh-configuration`) as a separate preview and decision.
6. Apply only after the contributor reviews the preview, asks to proceed, and supplies its exact plan ID. Rerun the same scope once with `--confirm-plan <EXACT-PLAN-ID> --json` instead of `--dry-run`. Reject abbreviated, old, different-scope, or ownership-transfer plan IDs.
7. On stale plan, refusal, partial publication, or changed authority, stop and relay exact CLI remediation. Never retry an apply, widen scope, add `--resolve`, substitute `--accept-bundled-conflicts`, invoke factory reset, or hand-edit configuration/state files.
8. Otherwise run `singularity-flow workspace current --json`, require its exact `repositoryPath`, and use it as cwd for `singularity-flow doctor --json` and `singularity-flow state planes --json`. Refuse without a selection; never fall back to the home directory or parent search. Show authority, revision, pending publication, ledger/outbox status, and affected files.
9. Start read-only. For approved repair, run the narrowest deterministic command. Factory reset requires its own preview and exact confirmation.
