---
name: update-go-deps
description: Update all direct Go module dependencies to their latest versions, tidy the module graph, verify tests pass, and commit the result. Use when you want to bump deps, address CVEs, or do routine dependency maintenance.
user-invocable: true
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Update Go Dependencies

Update all direct Go module dependencies to their latest versions, clean up the module graph, verify the build still works, and commit.

## Instructions

### Phase 0: Prepare

1. Confirm the working tree is clean: `git status`. If there are uncommitted changes, stop and ask the user how to proceed.
2. Identify all Go modules in the repo: `find . -name go.mod -not -path '*/vendor/*'`. Work through each module directory in turn.

### Phase 1: Update dependencies

For each module directory:

1. `cd` into the directory.
2. Run `go get -u ./...` to upgrade all direct dependencies to their latest minor/patch versions.
3. Run `go mod tidy` to prune unused indirect deps and update `go.sum`.
4. If a `vendor/` directory exists, run `go mod vendor` to sync it.

### Phase 2: Verify

1. Run `go build ./...` — fix any compilation errors before continuing.
2. Run `go test ./...` — if tests fail, investigate whether the failure is pre-existing or caused by the update.
   - Pre-existing failure: note it and continue.
   - Regression from the update: attempt to pin the offending dependency to the last working version using `go get <module>@<version>`, then re-tidy.
3. If a linter is configured (e.g. `golangci-lint`, `make check-style`), run it and fix new issues introduced by the updated deps.

### Phase 3: Summarise changes

Generate a human-readable summary of what changed:

```bash
git diff -- '*/go.mod'
```

Group changes by type:
- **Upgraded** — version bumped
- **Added** — new indirect dep pulled in
- **Removed** — dep no longer required

### Phase 4: Commit

1. Stage only `go.mod`, `go.sum`, and `vendor/` (if present): do **not** stage unrelated files.
2. Commit with a message like:

```text
chore(deps): update Go dependencies

<paste summary of notable upgrades here>
```

3. Print the commit hash and ask the user if they want to push or open a PR.

## Notes

- This skill upgrades to the **latest** version within each module's declared Go version constraint. It does not change the `go` directive in `go.mod` — use `/dev-workflows:update-go-version` to update the module's go directive.
- If the repo uses a `replace` directive in `go.mod`, preserve it unless the user explicitly asks to remove it.
- Security-sensitive upgrades (CVE fixes) should be called out explicitly in the commit message.
