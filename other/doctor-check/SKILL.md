---
name: doctor-check
description: Coverage gap analysis for the bashdep public API plus a bashdep::doctor audit
allowed-tools: Read, Bash, Grep, Glob
---

# Doctor Check

Two-part health check:

1. **Test coverage** - every public `bashdep::*` command must have tests
    for its happy path, mode flags, and failure modes.
2. **Runtime invariants** - `bashdep::doctor` itself reports lockfile vs
    filesystem inconsistencies; verify it covers every relevant directory.

## Workflow

### 1. Enumerate the Public API

```bash
grep -nE '^function bashdep::[a-z]' bashdep | grep -v '::_'
```

That list is the source of truth for what needs coverage.

### 2. Map Functions to Tests

For each public function:

```bash
grep -nE "bashdep::<name>\b" tests/unit/bashdep_test.sh
```

For each, check coverage of:
- Happy path
- `BASHDEP_DRY_RUN=true`
- `BASHDEP_SILENT=true`
- `BASHDEP_VERBOSE=true`
- `BASHDEP_FORCE=true` (when relevant)
- At least one failure mode (bad arg, missing file, IO error)

### 3. Categorize Coverage

- **Well tested** - happy path + mode flags + ≥1 failure mode
- **Partially tested** - happy path only
- **Not tested** - no test references the function

### 4. Identify Critical Gaps

**Priority 1:** Any public `bashdep::*` function with zero tests
**Priority 2:** Mutating commands missing `dry-run` coverage (silently
breaking the contract is the easiest regression to ship)
**Priority 3:** Failure paths (`return 1`) with no test
**Priority 4:** Snapshot drift - re-run the suite; if any snapshot
mismatch appears, decide drift vs regression

### 5. Run the Runtime Doctor

In the demo workspace (`example/`) or a scratch dir:

```bash
( cd example && bash demo.sh )
# Then, from the same dir:
source bashdep && bashdep::doctor
```

Confirm `bashdep::doctor`:
- Reports `OK` when lockfile and dir match
- Reports `missing file` when the lockfile entry has no on-disk file
- Reports `orphan file` when a file in the dir has no lockfile entry
- Honors `BASHDEP_SILENT` (errors still on stderr)

### 6. Generate Report

Output a markdown report with:
- Summary (total public functions, tested, % with mode coverage)
- Coverage table by function (✅ happy / 🟡 partial / ❌ none)
- Critical gaps with line references in `bashdep`
- Recommended new tests with proposed function names

## Coverage Goals

- 100% of public `bashdep::*` functions have ≥1 test
- 100% of mutating commands have `dry-run` coverage
- ≥1 failure-mode test per public function
- `bashdep::doctor` exercised in the test suite for: missing file,
  orphan file, OK case
