---
name: go-continuous-integration
description: "CI/CD pipeline configuration for Golang projects using GitHub Actions. Covers testing, linting, security scanning, and releases."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 05:45:00 GMT
---

## CI Pipeline Checklist

1. **Test with Race Detection** — Always run `go test -race ./...`.
2. **Linting** — Run `golangci-lint` on every PR.
3. **Vulnerability Scanning** — Include `govulncheck` to catch CVEs in dependencies.
4. **Tidy Check** — Ensure `go mod tidy` has been run and committed.
5. **Coverage** — Report code coverage to a service like Codecov.
6. **Matrix Builds** — Test against multiple Go versions (e.g., stable and stable-1).
7. **Release Automation** — Use GoReleaser for tagging and publishing binaries.

## Example GitHub Action: Test & Lint

```yaml
name: test
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        go-version: ['1.22', '1.23']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: ${{ matrix.go-version }}
      - run: go mod tidy && git diff --exit-code
      - run: go test -v -race -coverprofile=coverage.out ./...
      - name: golangci-lint
        uses: golangci/golangci-lint-action@v4
```

## Security Scanning

Add a dedicated job for security:
```yaml
security:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-go@v5
    - run: go install golang.org/x/vuln/cmd/govulncheck@latest
    - run: govulncheck ./...
```

## Release with GoReleaser

Create a `.goreleaser.yml` and a release workflow:
```yaml
name: release
on:
  push:
    tags: ["v*"]
jobs:
  goreleaser:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: actions/setup-go@v5
      - uses: goreleaser/goreleaser-action@v5
        with:
          args: release --clean
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Anti-patterns

- ❌ **Missing `-race` in CI** — Data races are silent and dangerous.
- ❌ **Ignoring `go mod tidy`** — Leads to inconsistent dependency trees.
- ❌ **No automated linting** — Results in "nitpick" comments in PRs.
- ❌ **Slow CI feedback loops** — Optimize with caching (`actions/setup-go` handles this).
- ❌ **Not pinning action versions** — Always use `@vN` (e.g., `@v4`) for stability.
- ❌ **Testing only on one OS** — If you build cross-platform tools, test on Linux, macOS, and Windows.
