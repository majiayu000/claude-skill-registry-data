---
name: deploy
description: Ship master to staging and check the rollout. Use when the user asks to deploy, whether a change is live on staging, why staging didn't update, or how a merge reaches an environment.
allowed-tools: Bash(gh run list *) Bash(gh run view *) Bash(gh run watch *) Bash(git log *) Bash(kubectl -n boilerplate rollout status *) Bash(kubectl -n boilerplate get *)
---

# Deploy to staging

Merging to `master` is the deploy; nothing is run by hand.

1. CI runs on the merge commit. When it passes, `.github/workflows/deploy.yml` builds
   every image for amd64 and arm64, publishes them as
   `ghcr.io/manasmadan/boilerplate/<image>:sha-<commit>`, signs them (cosign) and
   attests them.
2. Its last job commits the new tag to `deploy/environments/staging/stack.yaml`
   (`chore(infra): deploy sha-<commit> to staging [skip ci]`, as the GitHub App).
3. Argo CD syncs `staging-data` then `staging-stack` in namespace `boilerplate`. The
   migration Job runs first (PreSync hook); if it fails, the services keep the previous
   version.

## Check a rollout

- Workflow: `gh run list --workflow deploy.yml`, `gh run watch <id>`.
- Which commit staging runs: `git log -1 -p -- deploy/environments/staging/stack.yaml`.
- The cluster: `kubectl -n boilerplate rollout status deployment/boilerplate-api` (also
  `-web`, `-worker`, `-notifications`, `-webhooks`, `-ai`, `-ai-worker`), and
  `kubectl -n boilerplate get jobs` for the migration.
- The running release: `curl https://<site host>/api/v1/system` returns `release`, the
  image tag it runs (`sha-<commit>`).

## When staging didn't move

- CI failed on the merge commit: deploy only runs after a green CI on a push.
- The staging job warns about `GITHUB_TOKEN`: the GitHub App isn't set up, or isn't on
  the `master` ruleset's bypass list (docs/repository-settings.md).
- Re-run by hand: `gh workflow run deploy.yml` (builds the current `master`).

Production is not deployed from here: see the release skill.
