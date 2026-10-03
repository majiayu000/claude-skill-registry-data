---
name: ls-omniroute
description: Main OmniRoute router for ambiguous first-response triage, environment/API-key/access preflight, and non-mutating client onboarding. Use only before a task is classified; route classified discovery, mutation, and source-coverage work to their focused OmniRoute skills.
metadata:
  version: "1.1"
extensions:
  omniroute:
    source_kind: localsetup-native
    local_role: main-router
    source_repo: https://github.com/diegosouzapw/OmniRoute
    source_ref: v3.8.48
    source_commit: 7ee5bbc64dbb03e967521227f2afffeb7c9dad1e
    package_version: 3.8.48
    release_package_commit: 7ee5bbc64dbb03e967521227f2afffeb7c9dad1e
---

# OmniRoute

Purpose: keep OmniRoute work grounded in a small LocalSetup-native skill surface. This is an ambiguous-task/preflight router, not a universal OmniRoute terminal owner. Use it for unclassified first-response triage, environment/API-key/access preflight, and non-mutating client onboarding; then route each classified task to its focused terminal owner.

## Start here

1. Classify an unscoped request before acting:
   - unclassified first-response triage, env/API-key/access preflight, or non-mutating client onboarding: stay in this router;
   - classified read-only discovery: use `ls-omniroute-proxy`;
   - classified mutation: use `ls-omniroute-admin-automation`;
   - classified upstream source or LocalSetup coverage maintenance: use `ls-omniroute-update`.
2. Run a preflight before environment registration or non-mutating onboarding:

```bash
python3 "$(python3 ls/tools/localsetup.py --source-root . path package ls-omniroute scripts/omniroute_api.py)" preflight \
  --base-url "${OMNIROUTE_BASE_URL:-http://localhost:20128}" \
  --api-key-env OMNIROUTE_API_KEY \
  --required-access read
```

3. If env vars are missing, print durable user-level registration commands:

```bash
python3 "$(python3 ls/tools/localsetup.py --source-root . path package ls-omniroute scripts/omniroute_api.py)" env-commands \
  --base-url "http://localhost:20128" \
  --api-key-env OMNIROUTE_API_KEY
```

The generated commands intentionally use environment variables and placeholders. They do not print or persist a real key value supplied to the running process. After writing persistent env vars, restart the terminal, tmux session, GUI app, service manager, Codex, OpenCode, or any other already-running process that must inherit them.

## Skill routing

- Use `ls-omniroute-proxy` for every classified read-only discovery task: models/providers, context and compression state, health/usage/resilience, MCP/A2A, CLI tools, plugins, skills, tunnels, webhooks, and agent-client compatibility.
- Use `ls-omniroute-admin-automation` for every classified write or privileged workflow: providers, API keys, aliases, combos, fallbacks, budgets, policy, imports, purges, services, settings, backup/restore, and drift reconciliation.
- Use `ls-omniroute-update` for every classified upstream version, source coverage, freshness, or future OmniRoute skill-pack maintenance task.
- Stay in this skill only for unclassified first-response issue triage, env registration, access compatibility checks, and non-mutating client onboarding. It is not the terminal owner for an already-classified proxy discovery, admin mutation, or update/coverage task.
- The one declared composite exception is discovery before a live mutation: use the ordered sequence `ls-omniroute-proxy → ls-omniroute-admin-automation`. Admin remains the sole mutation terminal owner.

## Preflight CLI

The bundled `omniroute_api.py` tool is the stable LocalSetup CLI surface for this router's environment and access preflight. It is intentionally conservative:

- It reads secrets only from env vars named by `--api-key-env`.
- It rejects base URLs with embedded credentials.
- It redacts authorization material from output.
- It does not make this router the owner of classified model/provider/client/endpoint discovery or any mutation.
- It treats mutation approval as separate from access checks; route all provider settings, API keys, budgets, system prompts, routing rules, Qdrant credentials, shell startup, Codex configuration, or live admin changes to `ls-omniroute-admin-automation`.

Examples:

```bash
python3 "$(python3 ls/tools/localsetup.py --source-root . path package ls-omniroute scripts/omniroute_api.py)" preflight \
  --base-url "${OMNIROUTE_BASE_URL:-http://localhost:20128}" \
  --api-key-env OMNIROUTE_API_KEY \
  --required-access read
```

Use `ls-omniroute-proxy` for classified read-only discovery and `ls-omniroute-admin-automation` for every classified mutation. The main router's CLI examples intentionally stop at preflight and environment setup.

## Codex and client onboarding

- Keep non-mutating onboarding separate from configuration changes. This router may explain the distinction between persistent setup and runtime launch, but it does not write profiles or launch configuration.
- For Codex through OmniRoute, use `wire_api = "responses"` and obtain model IDs from current `ls-omniroute-proxy` discovery.
- Inspect `/api/cli-tools/codex-settings`, `/api/cli-tools/codex-profiles`, and `/api/cli-tools/runtime/{toolId}` only through `ls-omniroute-proxy` before proposing a change.
- Route an approved client-configuration mutation to `ls-omniroute-admin-automation`; do not overwrite `~/.codex/config.toml`, named Codex profiles, shell startup files, or client registration from this router.

## v3.8.48 coverage

LocalSetup intentionally consolidates OmniRoute v3.8.48 into four native skills. The upstream repository has 44 skill documents at immutable commit `7ee5bbc64dbb03e967521227f2afffeb7c9dad1e`; their coverage is tracked in `references/upstream-skill-coverage.md` rather than exposed as 44 separate LocalSetup skills.

Coverage groups:

- Main and onboarding: ambiguous first-response routing, environment/auth preflight, and non-mutating Codex setup/launch distinctions.
- Read-only discovery: models, inference, contexts, compression, resilience, cache, usage, integrations, routes, and normalized model observations.
- Administration: auth, API keys, providers, settings, budgets, imports, purges, backups, sync/cloud, and local services.
- Maintenance: update workflow, source provenance, strict upstream comparison, and release notes.

## Safety defaults

- Do not log raw API keys, management cookies, provider tokens, Qdrant credentials, shell startup contents that contain secrets, or authorization headers.
- Use `OMNIROUTE_BASE_URL` and `OMNIROUTE_API_KEY` by default; allow alternate env var names only after validating that the name is a normal shell identifier.
- Keep live discovery and write operations separate. This router owns neither classified discovery nor writes: `ls-omniroute-proxy` owns discovery and `ls-omniroute-admin-automation` owns mutations, which require explicit user approval.
- For Codex configuration, use `wire_api = "responses"` for OmniRoute Codex routing. Do not present `model_max_output_tokens` as effective Codex config when upstream guidance says it is ignored.

## References

- `references/upstream-skill-coverage.md`
- `scripts/omniroute_api.py`
- `../ls-omniroute-proxy/SKILL.md`
- `../ls-omniroute-admin-automation/SKILL.md`
- `../ls-omniroute-update/SKILL.md`
