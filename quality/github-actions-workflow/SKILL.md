---
name: github-actions-workflow
description: "World Pulse: When creating or modifying CI/CD workflows in `.github/workflows/`."
---

# GitHub Actions Workflow

**When to use:** When creating or modifying CI/CD workflows in `.github/workflows/`.

---

## Node.js Version Policy

All workflows must use **Node.js 20** with actions pinned to Node.js 24-compatible versions:

| Action | Required version |
|---|---|
| `actions/checkout` | `@v6` |
| `actions/setup-node` | `@v6` |
| `actions/upload-artifact` | `@v7` |
| `actions/github-script` | `@v8` |
| `codecov/codecov-action` | `@v5` |

Never use `@v4` for `checkout`/`setup-node`, `@v4` for `upload-artifact`, or `@v7` for `github-script` — these run on Node.js 20 and will break when GitHub enforces Node.js 24 (June 2 2026).

---

## Main CI Pipeline (`ci.yml`)

Four jobs in order:

```
lint → typecheck → test → build (+ build-electron)
```

`build` has `needs: [lint, typecheck, test]`. `build-electron` runs in parallel with `build` on both `macos-latest` and `ubuntu-latest`.

Standard step pattern:

```yaml
- uses: actions/checkout@v6
- uses: actions/setup-node@v6
  with:
    node-version: '20'
    cache: 'npm'
- run: npm ci
- run: npm run <task>
```

---

## When CI Runs

```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
```

All feature branches trigger CI only when a PR is opened against `main` or `develop`.

---

## Artifact Upload

Use `upload-artifact@v7` with explicit `retention-days`:

```yaml
- uses: actions/upload-artifact@v7
  with:
    name: dist
    path: dist/
    retention-days: 7
```

---

## Secrets

- All secrets go in GitHub repo settings, not in workflow files.
- Reference via `${{ secrets.SECRET_NAME }}`.
- `GITHUB_TOKEN` is auto-provided — do not add it as a custom secret.
- Never echo secrets or pass them as plain env vars to untrusted scripts.

---

## Quality Gates (`quality-gates.yml`)

Runs on PRs and checks:
- No hardcoded secrets (regex on `git diff`)
- Conventional commit format (`feat:`, `fix:`, etc.)
- Issue reference (`#123`) in commit messages
- File structure (docs directories exist)

These gates block PRs — do not bypass them with `|| true` on the fail steps.

---

## Security Scanning (`security.yml`)

Runs weekly + on push to main:
- `npm audit`
- Snyk (via `snyk/actions/node@master`)
- CodeQL analysis (`github/codeql-action@v4`)

Snyk and CodeQL results are uploaded as SARIF to GitHub Security tab.

---

## Anti-Patterns

- Do not add `continue-on-error: true` to critical steps (lint, typecheck, test).
- Do not hardcode `ubuntu-20.04` — use `ubuntu-latest`.
- Do not use `set-output` deprecated syntax — use `$GITHUB_OUTPUT`.
- Do not use `actions/cache` for `node_modules` directly — `setup-node` with `cache: 'npm'` handles this.
- Changes to `.github/workflows/**` are high-risk surface — always get architect review (see `risk_surface` gate in story/bug/docs workflows).
