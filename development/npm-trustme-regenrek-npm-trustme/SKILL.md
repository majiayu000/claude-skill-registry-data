---
name: npm-trustme
description: Automate npm Trusted Publisher setup via the npm-trustme CLI. Use when configuring or verifying npm Trusted Publishers for GitHub Actions with npx npm-trustme, including browser automation and WebAuthn passkey approval.
---

# npm-trustme

## Overview

Automate npm Trusted Publisher setup in the npm web UI. Requires a one-time WebAuthn approval in a real browser session (passkey or security key).

## CLI Quick Start

- One-time if browsers are missing: `npx playwright install`
- Ensure (create if missing): `npx npm-trustme ensure --yes ...`
- Check only: `npx npm-trustme check ...`
- Generate workflow: `npx npm-trustme workflow init`
- Doctor: `npx npm-trustme doctor`
- Non-interactive install: `npx npm-trustme install --non-interactive ...`

## Required Target Inputs

- Required: `--package`, `--owner`, `--repo`, `--workflow`
- Optional: `--publishing-access`, `--environment`, `--maintainer`

Default inference:
- package: `package.json#name`
- owner/repo: `git remote origin`
- workflow: `.github/workflows/npm-release.yml` or the only workflow file

## Examples

Check:
```
npx npm-trustme check \
  --package <PACKAGE_NAME> \
  --owner <GITHUB_OWNER> \
  --repo <GITHUB_REPO> \
  --workflow <WORKFLOW_FILE> \
  --publishing-access <PUBLISHING_ACCESS>
```

Ensure (create if missing):
```
npx npm-trustme ensure \
  --package <PACKAGE_NAME> \
  --owner <GITHUB_OWNER> \
  --repo <GITHUB_REPO> \
  --workflow <WORKFLOW_FILE> \
  --publishing-access <PUBLISHING_ACCESS> \
  --yes
```

Non-interactive install (single package):
```
npx npm-trustme install --non-interactive \
  --package <PACKAGE_NAME> \
  --owner <GITHUB_OWNER> \
  --repo <GITHUB_REPO> \
  --workflow <WORKFLOW_FILE> \
  --publishing-access disallow-tokens \
  --headless \
  --storage ~/.npm-trustme/storage.json
```

Non-interactive install (monorepo):
```
npx npm-trustme install --non-interactive \
  --all-packages \
  --owner <GITHUB_OWNER> \
  --repo <GITHUB_REPO> \
  --workflow npm-release.yml \
  --publishing-access disallow-tokens
```

Targets file (JSON/YAML):
```
targets:
  - packageName: my-pkg
    owner: my-org
    repo: my-repo
    workflow: npm-release.yml
    environment: npm
    publishingAccess: disallow-tokens
```

Workflow write in non-interactive install:
```
npx npm-trustme install --non-interactive \
  --workflow-init \
  --workflow-file npm-release.yml \
  --workflow-pm pnpm \
  --workflow-node 24 \
  --workflow-trigger release \
  --workflow-dispatch true \
  --workflow-build-command "pnpm build" \
  --workflow-publish-command "npm publish --access public --provenance"
```

Dedicated Chrome (keeps main browser open):
```
npx npm-trustme chrome start
npx npm-trustme ensure --yes
```

## Notes

- `--env-file` can load a specific `.env` path.
- `--storage` can persist Playwright storage state for faster re-runs.
- Inline cookies (Sweet Cookie format) are supported: `--inline-cookies-json`, `--inline-cookies-base64`, or `--inline-cookies-file`.
- Requires Node >= 22 (Sweet Cookie uses node:sqlite).
- Chrome profile reuse (manual session): `--chrome-profile` / `--chrome-profile-dir` / `--chrome-user-data-dir` / `--chrome-path`.
- Connect to an existing Chrome: `--chrome-cdp-url` or `--chrome-debug-port` (Chrome must be launched with remote debugging).
- Cookie import: `--import-cookies` (default true) to copy npm cookies from your main Chrome profile.
- `npm-trustme ensure` prompts for confirmation; use `--yes` in automated/agent runs.
- `npm-trustme install --non-interactive` requires all target fields; use `--targets-file` for per-package overrides.
- For headless runs, provide `--storage` or inline cookies to avoid interactive login/2FA.
