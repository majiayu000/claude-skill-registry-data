---
name: pre-release
description: Run a comprehensive pre-release validation checklist for bashdep
allowed-tools: Read, Bash, Grep, Glob
---

# Pre-Release Validation

Run all checks before releasing a new bashdep version.

## Checklist

### 1. Version Consistency

```bash
grep -n 'BASHDEP_VERSION="' bashdep
awk '/^## \[/{print; exit}' CHANGELOG.md
git tag --list --sort=-v:refname | head -3
```

`bashdep`'s `BASHDEP_VERSION` is the source of truth. The release script
bumps it; verify it matches the intended target version.

### 2. Full Test Suite

```bash
make test
```

Run 3-5 times to catch flaky tests. All must pass.

### 3. Static Analysis & Lint

```bash
make sa      # ShellCheck - zero warnings
make lint    # editorconfig-checker - clean
```

### 4. Documentation

- `CHANGELOG.md` `## [Unreleased]` section is complete and reflects
  every user-visible change since the last tag
- `docs/api.md` reflects every public `bashdep::*` function
- `docs/behavior.md` reflects current lockfile / dev-dep / error semantics
- `docs/releasing.md` is current
- `README.md` examples copy-paste cleanly
- No remaining `TODO` / `FIXME` in docs

### 5. Bash 3.2+ Compatibility (must return no results)

```bash
grep -nE 'declare -A' bashdep
grep -nE '\$\{[A-Za-z_][A-Za-z0-9_]*,,\}'  bashdep
grep -nE '\$\{[A-Za-z_][A-Za-z0-9_]*\^\^\}' bashdep
grep -nE '\bmapfile\b|\breadarray\b' bashdep
grep -nE '&>>' bashdep
grep -nE '\$\{[A-Za-z_][A-Za-z0-9_]*\[-1\]\}' bashdep
```

### 6. Runtime Dependency Audit

```bash
grep -nwE 'jq|python|node|yq' bashdep || echo "OK"
```

Library code must only call `curl` / `awk` / `mktemp` / POSIX builtins.

### 7. Mode-Flag Coverage

Every public mutating command honors `BASHDEP_DRY_RUN`,
`BASHDEP_SILENT`, `BASHDEP_VERBOSE`, `BASHDEP_FORCE`. Spot-check each
in the test suite:

```bash
grep -nE 'BASHDEP_(DRY_RUN|SILENT|VERBOSE|FORCE)=true' tests/unit/bashdep_test.sh
```

### 8. Release Script Dry Run

```bash
./release.sh --dry-run
```

Verify:
- Version bump target matches expectation
- CHANGELOG roll preview is correct
- Compare links at the bottom of CHANGELOG would update correctly

### 9. Breaking Changes

Review `git log <last-tag>..HEAD` for any breaking changes. Each must be
called out in `CHANGELOG.md` under `### Changed` or `### Removed` with a
brief migration note.

### 10. Git & CI Status

- Working tree clean (`git status --short` empty)
- On `main`
- All CI checks green: `gh run list --limit 5 --branch main`
- Target tag does not yet exist:
  `git tag --list <X.Y.Z>` returns empty

### 11. Smoke Test

```bash
( cd "$(mktemp -d)" \
  && cp /path/to/bashdep . \
  && source ./bashdep \
  && bashdep::version )
```

## Output

Report each check as ✅ pass / ❌ fail / ⚠️  warning. Only proceed to
`/release` when all checks are ✅.
