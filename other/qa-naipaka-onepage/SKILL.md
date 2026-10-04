---
name: qa
description: Run the project's verification harness (analyze, lint, format, tests) after code changes. Use after editing Dart code to verify the change before declaring it complete.
argument-hint: "[quick|standard|full]"
---

# QA Verification Harness

Run the appropriate verification tier based on `$ARGUMENTS`. If `$ARGUMENTS` is empty, run **standard**.

---

## Tier 1 — quick

Minimum check. Run from the repository root — do NOT `cd` into subdirectories, because this is a Pub Workspaces project and `fvm dart analyze` at the root inspects all packages in one pass.

```bash
fvm dart analyze
```

Expected output: `No issues found!`

If issues are found, fix them and re-run before proceeding.

---

## Tier 2 — standard (default when $ARGUMENTS is empty)

Pre-PR baseline. Run all three steps in sequence; stop and fix before continuing if any step fails.

```bash
# Step 1 — static analysis across all packages
fvm dart analyze

# Step 2 — format check (read-only, does NOT modify files)
fvm dart run melos run format:ci --no-select
```

Expected output for each: `No issues found!` (analyze) or a clean exit (format:ci).

If `format:ci` reports a diff, fix formatting with:

```bash
fvm dart format packages/
```

Then re-run `fvm dart run melos run format:ci --no-select` to confirm the diff is gone.

---

## Tier 3 — full

Heavy verification including tests. Run standard first, then add:

```bash
# All packages
fvm dart run melos run test:ci --no-select

# Or, for a specific package only
fvm dart run melos exec --scope=<package_name> -- flutter test
```

All tests must pass. Do not declare the task complete while any test is red.

---

## Code-generation prerequisite

If the change touches any of the following, run `fvm dart run melos run gen` **before** running any QA tier:

- Riverpod providers annotated with `@riverpod`
- Drift database table definitions
- i18n YAML files (`app_en.yaml` / `app_ja.yaml`)
- Freezed data classes

```bash
fvm dart run melos run gen
```

For i18n changes only:

```bash
fvm dart run melos run slang
```

---

## Completion criteria

Do NOT declare the task complete until **all** of the following are true for the chosen tier:

- `fvm dart analyze` → `No issues found!`
- `fvm dart run melos run format:ci --no-select` → clean (standard / full)
- `fvm dart run melos run test:ci --no-select` → all tests pass (full only)
