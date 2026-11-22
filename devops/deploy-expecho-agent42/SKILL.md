---
name: deploy
description: Deploy Agent42 to Azure — explain, trigger, or monitor the GitHub Actions "Deploy" workflow (preflight → shared infra → build → ACR → Bicep).
user-invocable: true
argument-hint: "[status | trigger | watch]"
---

# Deploy Agent42

Deployment is fully owned by `.github/workflows/deploy.yml` (workflow name: **Deploy**).
There is no manual deploy path — never run `az deployment group create` or
`docker push` by hand against production.

## How it deploys

1. **Trigger:** push to `main` touching `src/**`, `infra/**`, `Directory.Packages.props`,
   `.dockerignore`, or the workflow file — or a manual `workflow_dispatch`. Merging a PR into
   `main` is the normal deploy, but a PR touching none of those paths does NOT deploy.
2. **preflight:** fails closed when a repository variable is missing or would change what is deployed
   (an absent variable expands to an empty string; a missing custom domain would unbind the live one).
3. **build-and-push:** deploys `infra/shared.bicep` (registry and Container Apps environment, reused or created),
   builds `src/Agent42.Backend/Dockerfile`, tags with the first 12 chars of the SHA, pushes to the ACR.
4. **deploy:** `az deployment group create` of `infra/main.bicep` into the resource group. The registry, environment,
   resource group, domain and Cosmos region come from repo variables (ADR 0128); they are documented in
   `docs/features/azure-deployment.md` and set in the repository's Actions variables. Quirks are in `.agentic/gotchas.md` — read those entries before
   changing anything in this pipeline.

## Commands

| Intent | Command |
|--------|---------|
| Status of latest deploy | `gh run list --workflow Deploy --limit 5` |
| Trigger manually | `gh workflow run Deploy` (then `gh run watch`) |
| Watch a running deploy | `gh run watch` |
| Logs of a failed deploy | `gh run view <run-id> --log-failed` |

## Guardrails

- IAM/RBAC failures in the deploy: per CLAUDE.md hard rule 5, never fix by running
  role-assignment writes yourself — prepare the exact command and hand it to the user.
- If the deploy unbinds the custom domain, the managed certificate name drifted — see
  the "Custom domain must stay declared in Bicep" gotcha.
