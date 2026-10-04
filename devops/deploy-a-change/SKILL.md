---
name: deploy-a-change
description: Deploy or ship a code change to production, redeploy a stack, or roll back a bad deploy — merge for CI, then a manual workflow_dispatch deploy (never hand-run cdk deploy).
---
# Deploy a change

After go-live, shipping is two separate steps: merge a PR to `main` (the
`*-ci.yml` workflows test it — merging deploys nothing), then dispatch the
matching `*-deploy.yml` workflow, which ships through the `wos-github-deploy`
OIDC role. Deploys stopped auto-running on merge in July 2026. There is
deliberately no hand-run `cdk deploy` recipe anywhere.

## Read first
- docs/DELIVERY.md — §1 "The CI path" and §2 "Deploying is a decision", plus the FAQ (rollback, broker-address history, why no laptop deploys).
- .github/workflows/ — app-ci.yml, backend-ci.yml, backend-deploy.yml, flink-ci.yml, flink-deploy.yml, web-ci.yml, web-deploy.yml (they are short).

## Commands
- Merge: open a PR, merge to `main`. CI runs; nothing deploys.
- Deploy: `gh workflow run backend-deploy.yml --ref main` (also `web-deploy.yml`, `flink-deploy.yml`), or the "Run workflow" button on the Actions tab. Watch with `gh run watch`.
- Roll back: `git revert <commit>` merged through a PR, then dispatch the matching deploy workflow — the revert is not live until you dispatch. No automated rollback exists.
- Verify: `curl https://api.travel.michaelwheeler.ai/v1/health` → check `sha`.

## Gotchas
- Merged is not deployed: the AWS account keeps running the last dispatched deploy until you dispatch again.
- The deploy workflows do not re-run tests — confirm the CI runs on `main` are green before dispatching.
- Never run `cdk deploy` by hand — it skips the account guard and drifts from CI. Break-glass repairs go through `just bootstrap-*` (see the first-deploy skill).
- Which CI workflow runs is path-filtered: `services/**`/`infra/**`/`tools/**`/root `package.json` → backend-ci, `web/**` → web-ci, `flink/**` → flink-ci, `app/**` → app-ci (CI never deploys the app; `just flash` puts it on a phone).
- A dispatch on any ref other than `main` is skipped by the `github.ref` guard, not shipped.
- The web sync uses `--delete` but excludes `trips/*` — published trip pages are written by `just publish`, not the deploy workflow.
- A new Flink JAR uploads on `flink-deploy.yml` dispatch but only takes effect at the next `just live-up` (or a stop/start cycle).
- The post-deploy smoke needs repo vars `WOS_API_URL`/`WOS_LEDGER_TABLE` and secret `WOS_OWNER_TOKEN` (`WOS_MCP_URL` additionally enables the MCP assertion); missing any of the three prints `SMOKE SKIPPED` and stays green — do not mistake that for a pass.
