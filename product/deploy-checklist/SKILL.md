---
name: deploy-checklist
description: Produce a repository-specific deployment checklist with a pre-deploy GO/NO-GO verdict and post-deploy checks covering validation, migrations, feature flags, monitoring, communication, and rollback. Use when the user plans a deployment, release to production, or shipping event, for example "we are deploying to production", "deploy checklist", "can we deploy".
license: MIT
compatibility: "Claude Code"
---

# Deploy checklist

Mark an item UNVERIFIED when its evidence is unavailable (no CI status, no dashboard access). Never infer it as passed.

## Pre-deploy

1. Detect the package manager from the lockfile and run the repository's actual test, lint, typecheck, and build commands. Require green CI and the intended release branch.
2. For migrations, verify local/staging execution, backward compatibility, backup, expected lock/runtime, and tested rollback.
3. Verify feature-flag defaults and rollout percentages for risky behavior.
4. Confirm dashboards, error tracking, alerts, and explicit abort thresholds.
5. Draft deployment/client/status communication when needed, but do not send without explicit authorization.
6. Write the exact rollback command, estimated recovery steps, and trigger metrics.
7. Confirm an appropriate deployment window and an owner available for at least one hour of monitoring.
8. Return `GO` or `NO-GO`. Any failed or UNVERIFIED item from steps 1–7 means `NO-GO`; list what would turn it into `GO`.

## Post-deploy

1. Monitor error rate and latency against the abort thresholds.
2. Inspect new exceptions.
3. Run a critical-flow smoke test.
4. Record the result (stable, or rolled back with the trigger) in the closing status block; when `docs/runbooks/` has a deploy runbook, offer the line for it.

Never invent provider-specific commands. Derive them from repository configuration or ask for the missing deployment target.

End by offering the `brain-capture` skill when the deployment taught a lasting lesson.

## Stop point

Stop at the `GO`/`NO-GO` verdict before the deployment; after it, stop at the result recorded in the closing status block. The user runs the deployment.

## Never

- Deploy, run a production migration, or change a feature flag.
- Send deployment, client, or status communication without explicit authorization.
- Mark an item passed without evidence.
- Invent provider-specific commands.
