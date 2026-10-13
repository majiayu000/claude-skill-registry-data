---
name: preview
description: Give a pull request its own running environment, or find out why a preview isn't up. Use when the user wants to try, demo or share a branch before merging, or mentions the preview label or a pr-<number> URL.
argument-hint: <pull request number>
allowed-tools: Bash(gh pr view *) Bash(gh run list *) Bash(gh run view *) Bash(kubectl -n pr-* get *)
---

# Pull-request previews

1. Add the `preview` label (maintainers only): `gh pr edit <number> --add-label preview`.
   Only branches of this repository get previews, never forks.
2. `.github/workflows/preview.yml` builds the head commit's images (amd64) as
   `sha-<commit>` and pushes them to GHCR.
3. Argo CD's `previews` ApplicationSet (`deploy/argocd/appsets/previews.yaml`) polls
   labelled pull requests every two minutes and deploys `pr-<number>-data` then
   `pr-<number>-stack` into namespace `pr-<number>`, with
   `deploy/environments/preview/*.yaml`: its own Postgres and Valkey, secrets under the
   `boilerplate-preview-` prefix. Migrations run before the services, as everywhere.
   The charts, values and secrets come from the target branch; only the images come
   from the pull request, so a PR's own `deploy/` changes don't show in its preview.
   Once the stack is running and healthy, Argo CD's notifications comment the address
   on the pull request: `https://pr-<number>.preview.<the cluster's domain>`.
4. Each push rebuilds and redeploys. Removing the label or closing the pull request
   deletes the preview and its namespace.

## When it doesn't come up

- No images: the workflow didn't run (`gh run list --workflow preview.yml`); check the
  label and that the branch isn't from a fork.
- Running but no comment: the preview cluster's `argocd-notifications-secret` (the
  GitHub App's `github-appID`, `github-installationID`, `github-privateKey`; the app
  needs Pull requests: write), and the notifications controller's logs
  (`kubectl -n argocd logs deploy/argocd-notifications-controller`).
- Images pushed but nothing deployed: the preview cluster needs the label
  `boilerplate.dev/previews: "true"` and the `github-token` Secret in `argocd`
  (a SOPS file in `deploy/platform/secrets/<env>/`; see deploy/README.md), and GHCR packages must be
  pullable (docs/repository-settings.md, Packages).
- Deployed but failing: `kubectl -n pr-<number> get pods`, then the debug skill.
