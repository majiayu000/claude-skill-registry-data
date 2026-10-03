---
name: github-repo-management
description: "Clone, create, fork repos; manage remotes, releases."
allowed-tools:
  - bash
enabled: true
related-skills: [github-auth, github-pr-workflow, github-issues]
license: MIT
author: Adapted from hermes-agent (Nous Research, MIT)
---

# GitHub Repository Management

Create, clone, fork, configure, and manage GitHub repositories.

## Prerequisites

- Authenticated with GitHub (see `github-auth` skill)

## 1. Clone

```bash
# HTTPS
git clone https://github.com/owner/repo.git

# SSH
git clone git@github.com:owner/repo.git

# With gh (auto-forks if you don't have push access)
gh repo clone owner/repo

# Clone + set up remote for fork
gh repo clone owner/repo -- --origin upstream
git remote add origin https://github.com/$GH_USER/repo.git
```

## 2. Create New Repository

```bash
# With gh (creates on GitHub + clones locally)
gh repo create my-project --public --clone --description "My project"

# Private
gh repo create my-project --private --clone

# With git + curl
mkdir my-project && cd my-project && git init
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user/repos \
  -d '{"name":"my-project","private":true,"description":"My project"}'
git remote add origin https://github.com/$GH_USER/my-project.git
git push -u origin main
```

## 3. Fork

```bash
# With gh (forks + clones + sets up remotes)
gh repo fork owner/repo --clone

# With curl
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/repo/forks

# Manual fork setup
git remote add upstream https://github.com/owner/repo.git
git remote set-url origin https://github.com/$GH_USER/repo.git
```

## 4. Manage Remotes

```bash
# List remotes
git remote -v

# Add remote
git remote add upstream https://github.com/owner/repo.git

# Change remote URL
git remote set-url origin git@github.com:owner/repo.git

# Remove remote
git remote remove upstream

# Sync fork with upstream
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

## 5. Releases

```bash
# Create release with gh
gh release create v1.0.0 --title "v1.0.0" --notes "First stable release"

# Create release with assets
gh release create v1.0.0 ./dist/app.tar.gz ./dist/app.zip --title "v1.0.0"

# List releases
gh release list

# View release
gh release view v1.0.0

# Download release assets
gh release download v1.0.0 --pattern "*.tar.gz"

# With curl
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/releases \
  -d '{"tag_name":"v1.0.0","name":"v1.0.0","body":"First stable release"}'
```

## 6. Repository Settings

```bash
# With gh
gh repo edit --description "New description"
gh repo edit --enable-issues=false
gh repo edit --default-branch main

# With curl
curl -s -X PATCH \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO \
  -d '{"description":"New description","default_branch":"main"}'
```

## 7. Secrets (for GitHub Actions)

```bash
# With gh
gh secret set MY_SECRET --body "secret_value"
gh secret set MY_SECRET < secret_file.txt
gh secret list
gh secret delete MY_SECRET

# With curl (requires public key encryption)
# See https://docs.github.com/en/rest/actions/secrets
```

## 8. Delete Repository

```bash
# With gh (requires --yes for confirmation)
gh repo delete owner/repo --yes

# With curl
curl -s -X DELETE \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO
```

## Pitfalls

- **Fork visibility**: forks inherit the parent's visibility. Can't make a
  private fork of a public repo (without enterprise).
- **Release tags**: tags must exist before creating a release. `gh release
  create` auto-creates the tag if it doesn't exist.
- **Secret encryption**: API secrets require RSA encryption with the repo's
  public key. Use `gh secret set` instead of raw curl.
- **Delete permissions**: deleting a repo requires admin access + cannot be
  undone.
- **Rate limits**: creating many repos rapidly may hit secondary rate limits.
  Add delays.
