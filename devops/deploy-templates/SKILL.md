---
name: deploy-templates
category: operations
description: Built-in deploy recipes and deploy targets. Use when a task asks you to set up or change a stage/preprod/prod deploy workflow, including the system's "Set up <env> deploy" tasks.
---
# Deploy templates

Deploying is a defined step like build and test, not improvisation. Every environment
(`stage`, `preprod`, `prod`) of a repository has a **deploy target**: a provider, its
variables, a health URL and a rollback policy. Each provider has a **template**: the
workflow to write, the secrets it needs, the smoke check and the rollback.

## Workflow

1. A "Set up `<env>` deploy" task already carries the rendered recipe in its description —
   start from that rather than asking the tools for it again.
2. `get_deploy_target` with the repository id and env to re-read what this repo ships to,
   plus the recipe rendered with its variables, whenever you need it again mid-task.
3. `load_deploy_template` for the full raw recipe (secrets, smoke check, rollback) when the
   rendered version in the task description is not enough, or the task gives no recipe
   (a change to an existing deploy rather than a new one) — `list_deploy_templates`,
   optionally filtered by repo kind, to see what is available first.
4. Write the workflow into `.github/workflows/` exactly as the recipe describes. Keep the
   `workflow_dispatch` trigger: the board dispatches deploys by workflow file.
5. Name the file and the workflow's `name:` per ci-cd-pipeline-authoring so the detector maps
   it to the right slot (`stage_deploy` / `preprod_deploy` / `prod_deploy`). If the slot still
   shows unmapped after that, say so in one comment: mapping the detected slot is the human's
   action, not something you can force from here.

## Non-negotiables

- **A deploy must verify itself.** A green deploy step that never checked the service is a
  lie. Every deploy ends with a smoke check against the environment's health URL.
- **A deploy must be reversible.** Include the rollback step from the recipe (`if: failure()`).
  If a provider cannot roll back automatically, document the exact manual command.
- **Wait for the rollout.** `kubectl rollout status`, `aws ecs wait services-stable` and
  their equivalents are what make the result honest; dropping them for speed hides
  crash-looping releases.
- **No secrets in the workflow.** Use OIDC/Workload Identity Federation and repository
  secrets. Never commit a key file.
- **Concurrency guard.** One deploy per environment at a time (`concurrency.group`),
  otherwise two releases race and the environment ends up in an undefined state.
- If a required variable is missing (the rendered recipe shows `{{key — SET THIS}}`), ask
  for it. Do not guess a project id, region or cluster name.
