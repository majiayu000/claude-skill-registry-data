---
name: release-gate
description: Check deployment, staging, rollback, and health verification before release. Use for user-facing, infrastructure, CI/CD, integration, or high-risk changes.
---

# Release Gate

Use this before staging or production release.

## Workflow

1. Confirm the reviewed commit or artifact being released.
2. Confirm environment and deployment mechanism.
3. If the release introduces or changes a required config/secret name, reconcile required config/secret names against the target environment and block on any gap (`reconcile_config`) — see [configuration preflight](references/configuration-preflight.md).
4. If a secret-delivery path is new or changed, run a non-secret canary through that path and block until the canary confirms delivery works (`run_canary`) — see [configuration preflight](references/configuration-preflight.md).
5. Run the smallest deployment validation available.
6. Smoke-test the critical route or workflow.
7. Record rollback path.
8. Create a HITL issue if deployment needs missing human-held access. This is for access that does not exist yet and only a human can create or grant it (e.g., nobody has been given the third-party account/credential itself) — distinct from step 3's reconciliation, which is for config/secret names already obtainable through an existing provisioning process that simply haven't been set in the target environment yet.

## Scope & Exemption Rules

Apply this gate selectively based on risk level to prevent release gridlock:
- **Exempt (Skip this gate)**: Low-risk changes per `AI_ENGINEERING_WORKFLOW.md` (documentation-only edits, comments, minor styling/CSS tweaks, test-only additions, and narrow bug fixes with no business-rule change, data schema, auth, or infrastructure changes) skip the full staging/rollback release gate.
- **Mandatory (Do not skip)**: Medium and High-risk changes (user-facing features, business logic changes, migrations, authentication/permissions, deployment pipelines, and third-party integrations) must satisfy all checks below before release.

## Required For Medium/High Risk

- CI status
- Review status
- Target environment
- Smoke test command
- Rollback command or previous artifact
- Health check signal
- Configuration completeness and secret-delivery verification, for changes that introduce or change required config/secrets (see [configuration preflight](references/configuration-preflight.md))

## Guardrails

- Prefer deploying reviewed artifacts over rebuilding unreviewed source.
- Do not deploy production from unreviewed PRs.
- Do not silently work around missing secrets, DNS, or account permissions.
- Test database safety (disposable/dedicated storage, staging backup timing) follows `system-level/core.md` (Test Database Safety) — this gate does not relax it.
