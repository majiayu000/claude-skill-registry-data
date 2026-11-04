---
name: update-from-starter-template
description: Update Mattermost plugin repositories with common files from mattermost-plugin-starter-template and fix all linter issues. Use when syncing build tooling, updating golangci-lint config, or fixing linter errors in a Mattermost plugin.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch, mcp__github-server__get_file_contents
---

# Update from Starter Template

Update this Mattermost plugin repository with common build/config files from the [mattermost-plugin-starter-template](https://github.com/mattermost/mattermost-plugin-starter-template) and fix all linter issues.

## Instructions

### Phase 0: Prepare the repository

1. Switch to the main branch: `git checkout master` (or `main`)
2. Pull latest changes: `git pull`
3. Create a new branch for the updates: `git switch -c update-from-starter-template`

### Phase 1: Update common files from starter template

Fetch and compare these files from `mattermost/mattermost-plugin-starter-template` (master branch):

**Build files:**
- `build/manifest/*.go`
- `build/pluginctl/*.go`
- `build/setup.mk`
- `Makefile`

**Config files:**
- `.editorconfig`
- `.gitattributes`
- `.github/workflows/ci.yml`
- `.gitignore`
- `.golangci.yml`
- `.nvmrc`
- `go.mod` (for Go version only)
- `server/.gitignore`

When updating:
- Preserve plugin-specific customizations (plugin ID, custom targets)
- Update tool versions (golangci-lint, gotestsum, Node.js)
- Adopt new linter configurations
- Update Go version in `go.mod` if the starter template uses a newer version (compare the `go` directive). Also update the Go version in `.github/workflows/ci.yml` to match. After updating, run `go mod tidy` to update `go.sum`
- Preserve license headers
- Some plugins use `github.com/mattermost/mattermost-govet` in their Makefile to check for license headers. Do NOT remove that linter. If it reports missing license headers, add them to the affected source files.

### Phase 2: Fix linter issues

1. Run `make check-style` to identify issues
2. Install gofumpt if needed: `go install mvdan.cc/gofumpt@latest`
3. Run `gofumpt -w server/` to auto-fix formatting
4. Fix remaining issues manually

### Phase 3: Verify and commit

1. Run `make test` to verify all tests pass
2. Run `make check-style` to confirm 0 issues
3. Create a descriptive commit and PR. Use the pull request template from https://github.com/mattermost/.github/blob/master/PULL_REQUEST_TEMPLATE.md.

### Phase 4: Update Go dependencies (optional)

Ask the user if they want to update all direct Go dependencies. If yes:

1. Run `go get -u ./...` to update all direct dependencies
2. Run `go mod tidy` to clean up `go.sum`
3. Run `make test` to verify all tests still pass
4. Run `make check-style` to confirm 0 issues
5. Create a separate commit for the dependency updates

## Example commit message

```
Update common files from starter template and fix linter issues
```

## Troubleshooting

**Mock files have linter errors:**
- Generated mocks may need regeneration: `go generate ./...`
- Or exclude from linting if they're third-party generated
