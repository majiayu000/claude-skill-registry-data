---
name: automation
description: "Repeatable infrastructure: CI/CD pipelines, GitHub Actions, deploy and release scripts, dev-server orchestration, cron and scheduled jobs, container builds, backups, rollback. Use when setting up or fixing CI, writing a Dockerfile or deploy script, or on any deploy, release, pipeline, or schedule request."
license: MIT
metadata:
  display-name: "Automation"
  version: "1.1"
  platforms: "claude-code codex"
  tags: "ci-cd deploy scripts infrastructure"
---

# Automation

Manual steps are a bug. Anything done more than twice - install, build, test, deploy, backup, restore - gets a script. Anything done on a schedule gets a job runner.

Stack recipes - GitHub Actions layout, deploy-script shape, container builds, scheduled jobs, dev-server orchestration, release workflow, backups, observability - live in `references/recipes.md`; read it when writing the actual pipeline or script.

## Principles

- **Idempotent.** Running the script twice should produce the same outcome as running it once.
- **Fail loud.** `set -euo pipefail` in bash; exit non-zero on any unhandled error; never `|| true` to swallow failures.
- **Reproducible from a clean checkout.** No "you also need to install X manually" - that goes in the script.
- **One thing per script.** `build.sh`, `test.sh`, `deploy.sh`. A 600-line `do-everything.sh` is a footgun.
- **Inputs via flags or env, outputs to stdout, errors to stderr.** The Unix way composes; a script that writes to random paths doesn't.

## When to automate

- Twice is a coincidence; the third manual run is a bug - script it.
- Automate the check before the action: a deploy script without a smoke check automates the outage too.
- One workflow per concern (`ci.yml`, `deploy.yml`, `nightly.yml`); required checks either block merge or don't exist - no "advisory only" gates.
- Prefer boring, inspectable scripts committed to the repo over bespoke tooling; the runbook is the script's `--help` output and the README.
- Never publish from a laptop - build artifacts come from CI.

## Rollback principles

- Every deploy script needs a documented rollback. "Just run the previous version's deploy again" is a documented rollback - write it down.
- Keep N previous releases on disk. Rolling back is `ln -sfn` to the previous one, not a full re-deploy.
- Migrations run *before* the new app version starts and stay forward-compatible with the *previous* app version, so rollback works.
- A failed post-deploy health check triggers the rollback path, not a debugging session on prod.

## Agent and local harness patterns

- Keep project-local automation close to the project: commands, hooks, and routing registries live under the repo, not in a global dotfile, when they encode project rules.
- Hook-style guardrails should be grounded in a documented rule, path-gated, advisory by default, and robust enough that a hook bug never blocks normal work.
- Blocking hooks are for narrow, high-confidence safety rules only, such as refusing `git commit` or `git push` on `main`/`master` unless the user explicitly asks for that workflow.
- Prefer trigger registries over hardcoded prompt logic when routing skills or specialist agents. Match by keyword, intent regex, and mentioned path globs; keep project-specific rules in the project.
- Slash-command equivalents should be thin wrappers around repeatable scripts or read-only status checks: build check, diff recap, status, scaffold, backup, deploy.

## Anti-patterns

- "Run this on the prod server" - write it in the deploy script.
- "Set this env var manually" - put it in the secret store with provisioning automation.
- Manual DB migrations in production - wrap in a script with a dry-run mode.
- `kubectl edit` / `vim` on a running config - change in version control, redeploy.
- "We'll write the runbook later" - the runbook is the deploy script's `--help` output and the README.

## Verification before declaring done

- Run the script on a clean machine (or container) - no leftover state from your dev box.
- Read the logs of a successful run. Are they useful for an oncall who has never seen this project?
- Read the logs of a failed run (force one). Does the error tell you what to do?
- Time it. If the happy path takes > 10 minutes, that cost is real.
