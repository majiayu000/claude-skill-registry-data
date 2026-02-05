---
name: devops-dx
description: |
  GitHub/Railway housekeeping for CI env/secret management and DX maintenance.
  Use when setting or auditing GitHub Actions variables/secrets, syncing Railway env → GitHub, or fixing CI failures due to missing env.
tags: [devops, github, env, ci]
allowed-tools:
  - Bash(gh:*)
  - Bash(railway:*)
  - Read
---

# DevOps DX Helper

Lightweight playbook for CI/Railway env hygiene. Examples use this repo's Beads prefix (bd-); swap for your repo.

## Common Tasks

- **Set GitHub Actions variables** (non-secret paths, stub fixtures):
  - `gh variable set CLERK_TEST_JWKS_PATH --body "frontend/e2e-smoke/fixtures/clerk-test-jwks.json"`
  - `gh variable set CLERK_TEST_PRIVATE_KEY_PATH --body "frontend/e2e-smoke/fixtures/clerk-test-private.pem"`

- **Set GitHub Actions secrets** (API keys, tokens):
  - `gh secret set ZAI_API_KEY <<<"…"`
  - `gh secret set OPENAI_API_KEY <<<"…"`

- **Sync Railway → GitHub secrets** (if already stored in Railway):
  - `scripts/sync_env_to_github.sh <environment> [service]`
    - Copies Railway env vars to GitHub repo secrets (keys sanitized for GH).

## When CI Fails for Missing Env

1) Identify missing var from logs (e.g., `CLERK_TEST_JWKS_PATH missing`).
2) Decide scope:
   - CI-only → set via `gh variable/secret set`.
   - Runtime (Railway) → set in Railway dashboard or `railway variables set`.
3) Re-run the affected workflow: `gh workflow run CI --ref master`.

## Notes

- Keep stub/test fixtures in GH Actions vars, not Railway.
- Use Railway for production secrets; keep CI-only secrets separate.
- For multi-repo, reuse this skill and adjust variable names/prefixes per repo.
