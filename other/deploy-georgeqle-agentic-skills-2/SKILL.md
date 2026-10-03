---
name: deploy
description: Deploy the project to a target environment (defaults to staging) with deployment history tracking
type: shipping
version: v0.0
argument-hint: "[staging|production] [--status]"
---

# Deploy

Deploy the current project to the specified environment. Defaults to `staging` if no argument is provided. Maintains a deployment ledger (`tasks/deploys.md`) to track what was deployed when, enabling staleness detection across environments.

If `$ARGUMENTS` contains `--status`, skip deployment and jump to step 7 (staleness report only).

## Process

1. **Determine the target environment** from `$ARGUMENTS` (default: `staging`).
   - If `production` is specified, **ask for explicit confirmation** before proceeding.

2. **Find the deploy configuration.** Check these locations in order:
   - `spec.md` — look for a deployment section
   - `CLAUDE.md` — look for deploy commands or instructions
   - `tasks/roadmap.md` — look for deploy instructions
   - `tasks/todo.md` — look for deploy instructions
   - `Makefile` / `Justfile` — look for deploy targets
   - `package.json` — look for deploy scripts
   - `deploy/`, `infra/`, `scripts/` — look for deploy scripts or IaC
   - `docker-compose*.yml`, `Dockerfile` — container-based deploys
   - **Do NOT look in `.github/workflows/`** — this project does not use GitHub Actions.
   - If no deploy config is found, **stop and ask the user** how to deploy this project.

3. **Pre-flight checks:**
   - Ensure the working tree is clean (`git status`). If dirty, warn and ask whether to proceed or commit first.
   - Resolve the primary branch: prefer `main`; if it does not exist, use `master`. If neither exists, stop and explain the blocker.
   - Ensure the current branch is the primary branch. If not, stop and tell the user to land the work on `main`/`master` first rather than deploying from a feature branch.
   - Ensure the primary branch is pushed to remote.
   - Note the current commit hash for reference.

4. **Compare against last deployment:**
   - Read `tasks/deploys.md` (if it exists) and find the most recent entry for the target environment.
   - If a previous deployment exists, run `git log --oneline <last-deployed-commit>..HEAD` to show exactly which commits will be included in this deploy.
   - Report the commit count, time since last deploy, and a summary of what's changed.
   - If no previous deployment exists, note this is the first tracked deploy for this environment.

5. **Run the deploy** using the project's deploy mechanism.
   - Do not run `aws sso login` preemptively from stale context, old logs, or assumptions. If the deploy method uses an AWS profile and auth status is uncertain, first run `aws sts get-caller-identity --profile <profile>` using the profile from the deploy contract or deploy command.
   - If the AWS identity check succeeds, proceed directly with the deploy and do not run `aws sso login`.
   - If the AWS identity check or the deploy command fails because AWS SSO credentials are missing or expired, do not skip deployment. Run the matching `aws sso login --profile <profile>` command, using the profile from the deploy contract, deploy command, or error output.
   - When `aws sso login` prints a browser URL, device code, or verification instructions, relay them to the user and tell them to navigate to the provided URL and complete the login in their browser. Keep the login command running until it succeeds, fails, or times out.
   - After a successful SSO login, rerun the original deploy command once. This auth recovery is part of the same deploy attempt, not an automatic retry of a failed deploy.
   - If the user cannot complete SSO login or the login command fails, report the deploy as blocked by authentication. Do not report it as skipped.

6. **Post-deploy verification** (if applicable):
   - Check deploy output for errors.
   - If there's a health check URL or status command in the project config, run it.
   - Report success or failure.

7. **Record deployment to ledger:**
   - Read or create `tasks/deploys.md`.
   - Prepend a new entry under the environment heading (most recent first) using this format:

   ```markdown
   ### <environment>

   | Date | Branch | Commit Range | Commits | Status |
   |------|--------|--------------|---------|--------|
   | 2026-04-01 14:30 UTC | main | abc1234..def5678 | 12 | success |
   ```

   - **Date**: UTC timestamp of the deployment.
   - **Branch**: The primary branch that was deployed.
   - **Commit Range**: `<last-deployed>..<current>` (or just the commit hash if first deploy).
   - **Commits**: Number of commits in the range.
   - **Status**: `success` or `failed`.
   - If the deploy failed, still record it with `failed` status — this preserves the attempt history without advancing the "last good deploy" baseline.
   - Below the table, include a collapsed details block with the commit list:

   ```markdown
   <details>
   <summary>Commits in this deploy</summary>

   - `def5678` feat: add user profile page
   - `ccc4444` fix: correct auth redirect
   - ...
   </details>
   ```

8. **Report staleness across all environments:**
   - For each environment that has at least one `success` entry in the ledger, report:
     - Last successful deploy date
     - Commit hash at that deploy
     - Commits behind HEAD: `git log --oneline <last-success-commit>..HEAD | wc -l`
     - Days since last deploy
   - Flag any environment where the last successful deploy is **7+ days old** or **20+ commits behind** as stale.

9. **Output a concise summary:**
   - Environment deployed to
   - Branch and commit range
   - Commits included (count + list)
   - Success/failure status
   - Staleness status for all tracked environments
   - Any warnings or follow-up actions

## Ledger Format

`tasks/deploys.md` is organized by environment, most recent entry first:

```markdown
# Deployment History

## staging

| Date | Branch | Commit Range | Commits | Status |
|------|--------|--------------|---------|--------|
| 2026-04-01 14:30 UTC | main | abc1234..def5678 | 12 | success |
| 2026-03-28 09:15 UTC | main | 9990000..abc1234 | 5 | success |

<details>
<summary>2026-04-01 14:30 UTC — 12 commits</summary>

- `def5678` feat: add user profile page
- `ccc4444` fix: correct auth redirect
- ...
</details>

## production

| Date | Branch | Commit Range | Commits | Status |
|------|--------|--------------|---------|--------|
| 2026-03-25 16:00 UTC | main | 7770000..9990000 | 8 | success |

<details>
<summary>2026-03-25 16:00 UTC — 8 commits</summary>

- `9990000` feat: billing integration
- ...
</details>
```

## Constraints
- Never deploy to production without explicit user confirmation.
- If deploy fails, report the error clearly — do not retry automatically. Still record the failed attempt in the ledger. AWS SSO credential refresh is the only exception: after a live identity check or deploy command proves credentials are missing or expired, prompt the user through `aws sso login --profile <profile>` once, then rerun the original deploy command once.
- Do not modify code as part of the deploy process.
- Never use GitHub Actions for deployment. Only use manual deploy scripts, Makefiles, or CLI commands.
- The ledger (`tasks/deploys.md`) is the only file this skill writes to. Do not modify other task files.
- When computing staleness, only count `success` entries — `failed` deploys do not reset the staleness clock.
- Keep the ledger concise: the table is the primary record, the details block is supplementary. Do not duplicate commit lists in both places.


## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
