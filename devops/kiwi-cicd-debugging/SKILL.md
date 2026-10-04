---
name: kiwi-cicd-debugging
description: Use when a deploy.yml run fails on Kiwi's prod CI/CD pipeline, bootstrap-cicd.sh fails against real GCP, or you're modifying deploy.yml/bootstrap-cicd.sh and want to avoid gotchas already hit. Covers gcloud beta run jobs, Cloud Run canary/ingress 404s, IAM instance-scope restrictions, OS Login setup, and a required-status-check merge blocker.
---

# Kiwi CI/CD Debugging

## Overview

`.github/workflows/deploy.yml` deploys Kiwi's real prod (GCP project
`kiwi-prod-502913`) on every merge to `main`: `verify` → `build-and-push` →
`migrate` → `deploy-api` → `deploy-orchestrator` → `deploy-frontend` →
`refresh-fleet`. One-time GCP identity setup is
`deploy/gcp/bootstrap-cicd.sh` (human-run, not invoked by CI). Full design
history and every amendment below is also recorded in
`docs/superpowers/specs/2026-08-10-prod-cicd-design.md` — keep that file and
this skill in sync when you find something new.

## Pulling real failure logs

`gh run view --job <id> --log` sometimes returns nothing (seen for jobs
belonging to a reusable workflow). The REST API always works and is not
truncated:

```bash
gh run list --repo RunKiwi/kiwi --workflow deploy.yml --limit 5
gh run view <RUN_ID> --repo RunKiwi/kiwi                     # which job failed
gh api repos/RunKiwi/kiwi/actions/jobs/<JOB_ID>/logs | tail -150
```

`gh run watch <RUN_ID> --repo RunKiwi/kiwi --exit-status --interval 15`
streams a run to completion — run it with `run_in_background`, a full run
can take 10+ minutes.

## Known failure modes

All of these were hit for real against `kiwi-prod-502913` (2026-08-10/11,
PRs #333-#337) and are already fixed in the current `deploy.yml`/
`bootstrap-cicd.sh` — listed here in case a similar change reintroduces one,
or a new environment hits the same class of issue.

| Symptom | Cause | Fix |
|---|---|---|
| `ERROR: (gcloud.run) Invalid choice: 'jobs'` | `gcloud run jobs` isn't in the GA command track | Use `gcloud beta run jobs ...` everywhere (migrate job, bootstrap script) |
| Migrate job hangs then fails: "not in an interactive session" / "requires the installation of components: [beta]" | gcloud auto-installs the `beta` component on first use; its confirmation prompt hangs forever on a non-interactive runner | `setup-gcloud` step needs `with: install_components: beta` |
| `bootstrap-cicd.sh` fails: "Role roles/iap.tunnelResourceAccessor is not supported for this resource" | Compute Engine's instance-level IAM only accepts a curated allowlist — OS Login roles (`osLogin`/`osAdminLogin`) are on it, IAP tunnel accessor and most custom roles are not | Grant at **project** level instead: `gcloud projects add-iam-policy-binding $PROJECT --role roles/iap.tunnelResourceAccessor --condition=None`. Same fix for a custom role hitting the same error. |
| `refresh-fleet`'s SSH step fails: "Required 'compute.instances.setMetadata' permission" | OS Login IAM roles were granted, but OS Login itself was never enabled on the instance — gcloud silently falls back to legacy metadata-based SSH keys, which need a permission this identity deliberately lacks | `gcloud compute instances add-metadata <vm> --metadata enable-oslogin=TRUE` — one-time, non-disruptive to a running instance. Granting the IAM role is necessary but not sufficient. |
| Canary health check 404s forever on a Cloud Run service's direct `*.run.app` tag URL, even though the app's `/healthz` works fine through its real domain | The 404 is Google's own edge page (generic "That's an error", not the app's) — the service is ingress-restricted to load-balancer-only traffic (fronted by a serverless NEG + external HTTPS LB), so direct Cloud Run URLs never reach the container | Don't chase the curl. Deploy with a plain `gcloud run deploy` (no `--no-traffic`, no tag) — it already blocks until the new revision is Ready before routing traffic, and never touches traffic if the revision fails. No HTTP check needed. All three Cloud Run services deploy this way today; there is no canary workflow in this pipeline anymore. |
| `gcloud artifacts docker images describe` fails: "Permission 'containeranalysis.occurrences.list' denied" | That command pulls container-analysis metadata even when the format filter only asks for `image_summary.digest` | Don't grant the permission. Add `id: <name>` to the `docker/build-push-action` step and read `steps.<name>.outputs.digest` — it already has the digest from the push. |
| Frontend image push fails: "failed to authorize: DeadlineExceeded" right after "pushing layers ...s done" | Transient — a registry auth token refresh timing out mid-push on the largest of the three images | Retry: `gh run rerun <RUN_ID> --repo RunKiwi/kiwi --failed`. Safe by default here since nothing downstream (migrate, any deploy) starts until `build-and-push` fully succeeds. |
| A workflow-only PR can't merge: `gh pr merge` says "the base branch policy prohibits the merge" | The repo's branch ruleset requires "Lint & Build" (Frontend CI) as a status check, but that workflow is path-filtered to `frontend/**` — it never runs for a PR that doesn't touch frontend, so the required check sits "expected" forever | Label the PR `skip-readme-check` (use `gh api repos/RunKiwi/kiwi/issues/<PR>/labels -f "labels[]=skip-readme-check"` — `gh pr edit --add-label` can fail here with an unrelated "Projects (classic)" GraphQL error), then merge with `gh pr merge --admin` (repo-admin privileges required) or have someone with them merge it. This is a real gap in the ruleset, not something to route around silently — flag it if it comes up often. |
| `gh workflow run deploy.yml` / `workflow_dispatch` returns 404, workflow missing from `gh workflow list` | GitHub only registers `workflow_dispatch` for workflows that exist **on the default branch** — a workflow that only exists on a feature branch cannot be manually triggered at all, even with `--ref` pointing at that branch | No pre-merge workaround. The first real test of a new/changed `deploy.yml` is either the merge's own push trigger, or `workflow_dispatch` immediately after merging. |

## Debugging something not in this table

1. Pull the real log with `gh api .../logs` above — the job summary in
   `gh run view` truncates and can hide the actual error.
2. Classify it: IAM/permissions ("Permission ... denied", "is not supported
   for this resource"), a genuine app/config bug, or transient
   (timeouts, `DeadlineExceeded`) — that determines whether to fix, retry,
   or dig further.
3. If it's IAM, check what's already granted in `bootstrap-cicd.sh` first,
   and remember the instance-vs-project scope restriction above before
   adding a new `gcloud compute instances add-iam-policy-binding` call —
   it may need to be a project-level binding instead.
4. Fix it, then update both the code/script **and** the "Amendments"
   section(s) of `docs/superpowers/specs/2026-08-10-prod-cicd-design.md` —
   that file and this skill should never drift apart.
5. Branch the fix off latest `main` (not a stale branch), expect the
   required-status-check gotcha above, and watch the next run with
   `gh run watch`.
