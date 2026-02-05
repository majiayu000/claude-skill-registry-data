---
name: ci-images
description: Work with this repo’s GitHub Actions CI and GHCR Docker image publishing workflow. Use when changing generation checks, tests, formatting, or when preparing a release and validating image tags.
license: MIT
compatibility: Local validation requires bash, git, Go, make; Docker publishing runs in GitHub Actions.
metadata:
  repo: mjrwtf
  runner: github-copilot-cli
  version: 1.1
allowed-tools: Bash(git:*) Bash(make:*) Bash(go:*) Bash(docker:*) Read
---

## Tooling assumptions

- Use a terminal runner with bash and git available.
- Prefer `make` targets when available; fall back to direct CLI commands when needed.

## CI overview (local equivalents)

The CI workflow enforces:

- generated code is up to date (templ + sqlc)
- gofmt formatting
- go vet
- go test

Local one-liners:

```bash
make generate
make fmt
make vet
make test
```

## Docker image publishing

Workflow: `.github/workflows/docker-publish.yml`

- Runs on GitHub Release publish (and manually via workflow_dispatch)
- Publishes to GHCR with tags:
  - semver `vX.Y.Z`
  - `X.Y`, `X`
  - `latest` on release

## Suggested pre-release checklist

```bash
make test
make validate-openapi
```

If you changed SQL/templ, ensure `make generate` output is committed.
