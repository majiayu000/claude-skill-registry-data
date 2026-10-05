---
name: qruiq-github-ci
description: |
  Add GitHub Actions CI/CD pipeline that builds Docker images, pushes to Tencent TCR, and deploys to TKE.
  Tag-triggered: dev-tag/v* for dev, v* for production. PR triggers lint+typecheck only.
  Use when asked to "add CI/CD", "setup GitHub Actions", "auto deploy", or "add pipeline".
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# qruiq-github-ci

> Tag-triggered CI/CD: push tag → build Docker image → push to TCR → deploy to TKE.

## Prerequisites

**Check before proceeding. Stop and prompt user if any fail:**

### 1. Detect user shell

```bash
echo $SHELL
```

### 2. Verify dependencies

| Command | Check | If missing |
|---|---|---|
| `gh` | `command -v gh` | `brew install gh` |
| `gh` logged in | `gh auth status` | `gh auth login` |
| `git` | `command -v git` | Install git |

### 3. Auto-detect parameters

```bash
gh api user --jq .login
gh api user/orgs --jq '.[].login'
git remote get-url origin 2>/dev/null
cat package.json | grep '"name"'
cat ~/.kube/config | base64 | tr -d '\n'
echo $TCR_USERNAME; echo $TCR_PASSWORD
```

## Parameters

**Auto-detect first, only ask user for values that cannot be detected.**

| Parameter | Required | Auto-detect method | Example |
|---|---|---|---|
| `APP_NAME` | Yes | `package.json` name field | `my-app` |
| `TCR_NAMESPACE` | Yes | `.env` files or default `qruiq` | `qruiq` |
| `GITHUB_ORG` | Yes | `gh api user/orgs` — let user pick | `my-org` |
| `DOMAIN` | No | `k8s/ingress.yaml` host field | `my-app.qruiq.app` |
| `TCR_USERNAME` | Yes | `$TCR_USERNAME` env var or `.env` | `100012345678` |
| `TCR_PASSWORD` | Yes | `$TCR_PASSWORD` env var or `.env` | `xxx` |
| `KUBE_CONFIG_DEV` | Yes | `cat ~/.kube/config \| base64` | `LS0t...` |

## Steps

**Execute all steps directly. Do not list as TODOs.**

### 1. Copy template files

```bash
mkdir -p .github/workflows
cp ~/.qruiq/skills/skills/qruiq-github-ci/template/.github/workflows/deploy-tke.yml .github/workflows/
cp ~/.qruiq/skills/skills/qruiq-github-ci/template/Dockerfile .
```

### 2. Replace placeholders in workflow

```bash
sed -i '' "s/__APP_NAME__/<APP_NAME>/g" .github/workflows/deploy-tke.yml
sed -i '' "s/__TCR_NAMESPACE__/<TCR_NAMESPACE>/g" .github/workflows/deploy-tke.yml
sed -i '' "s/__IMAGE_NAME__/<APP_NAME>/g" .github/workflows/deploy-tke.yml
sed -i '' "s/__DOMAIN__/<DOMAIN>/g" .github/workflows/deploy-tke.yml
```

### 3. Enable standalone output in `next.config.mjs`

```mjs
const nextConfig = {
  output: "standalone",
};
export default nextConfig;
```

### 4. Ensure `public/` has a file (prevent Docker build failure)

```bash
touch public/.gitkeep
```

### 5. Create GitHub repo and push

```bash
gh repo create <GITHUB_ORG>/<APP_NAME> --private
git remote add origin https://github.com/<GITHUB_ORG>/<APP_NAME>.git
git add .
git commit -m "chore: init project"
git push -u origin main
```

### 6. Configure GitHub Actions Secrets

**First, check if the org already has these secrets configured. Skip any that already exist at org level (the repo will inherit them automatically). Only set the missing ones at the repo level — and only ask the user for values that are still missing after this check.**

```bash
# List org-level secrets (requires admin:org scope; if it errors with 403, fall back to repo-level for all)
gh secret list --org <GITHUB_ORG> 2>/dev/null
```

For each of `TCR_USERNAME`, `TCR_PASSWORD`, `KUBE_CONFIG_DEV`, `KUBE_CONFIG_PROD`:
- If present in org-level list **and** visibility covers this repo (`all`, `private`, or `selected` with this repo included) → skip, the repo inherits it.
- If missing → ask the user for the value (unless already auto-detected) and set at repo level:

```bash
gh secret set <SECRET_NAME> --repo <GITHUB_ORG>/<APP_NAME> --body "<VALUE>"
```

If `gh secret list --org` returns 403 (token lacks `admin:org` read), tell the user: "Can't read org secrets — they may already be configured at org level. Skip repo secrets and rely on org inheritance, or provide values to set at repo level?" before falling back.

### 7. Verify secrets

```bash
gh secret list --repo <GITHUB_ORG>/<APP_NAME>      # repo-level
gh secret list --org <GITHUB_ORG> 2>/dev/null      # org-level (inherited)
```

### 8. Trigger first dev deploy

```bash
git tag dev-tag/v0.1.0
git push origin dev-tag/v0.1.0
```

Wait ~30s then check:
```bash
gh run list --repo <GITHUB_ORG>/<APP_NAME> --limit 5
```

## Tag conventions

| Tag format | Target environment |
|---|---|
| `dev-tag/v0.1.0` | Dev |
| `v1.0.0` | Production |
| PR to `main`/`develop` | Tests only, no deploy |

## Pipeline flow

```
push tag (v* / dev-tag/v*)
    │
    ├─ test (PR only): lint + tsc --noEmit
    ├─ build: Docker image → push to TCR
    │
    ├─ deploy-dev        (tag: dev-tag/v*)
    └─ deploy-production (tag: v*)
```

## Notes

- `deploy-dev` must use `always()` — when test job is skipped (tag push), GitHub Actions skips all downstream jobs by default
- Dev health check uses `kubectl exec` (not curl) — GitHub runner cannot reach cluster internal IPs
- `prisma db push` for dev (fast schema sync), `prisma migrate deploy` for prod (strict migration)
- `cache-from: type=gha` leverages GitHub Actions cache for faster Docker builds
- `platforms: linux/amd64` — TKE nodes are x86_64

## GitHub Secrets required

| Secret | Description |
|---|---|
| `TCR_USERNAME` | TCR credentials username (Tencent CAM) |
| `TCR_PASSWORD` | TCR credentials password |
| `KUBE_CONFIG_DEV` | Dev cluster kubeconfig (base64) |
| `KUBE_CONFIG_PROD` | Production cluster kubeconfig (base64) |
