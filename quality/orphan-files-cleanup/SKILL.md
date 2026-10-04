---
id: quality.no-dead-code.orphan-files-cleanup
name: Orphan Files Cleanup
description: >
  Detects and removes orphan files that no longer participate in build, tests, runtime, or documented configuration paths without breaking dynamic loading or convention-based usage.
stack:
  - JavaScript
  - TypeScript
category: no-dead-code
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - orphan files
  - dead files
  - file cleanup
  - unused file
  - stale file
compatibility:
  runtime:
    browser: true
    node: true
---

# Orphan Files Cleanup

## Purpose

Use this skill to detect and remove orphan files safely.

The goal is to clean files that no longer participate in build, tests, runtime, or documented configuration paths.

The core rule is simple:

```txt
Do not delete what you cannot verify.
```

## When to Use

Use this skill when:

- migrations leave stale files behind
- features were removed
- tests or mocks are obsolete
- assets or modules are disconnected
- generated files are no longer referenced
- refactors leave alternate copies, backups, or dead entry points

## Do

Check:

- imports
- build config
- test config
- runtime config
- glob-based loaders
- dynamic loading paths

Also verify:

- barrel exports
- router lazy-loading references
- code generation inputs or outputs
- assets referenced from HTML, CSS, JSON, or manifest files
- package scripts and custom tooling
- documentation or operator runbooks when files are used manually

Use a bounded procedure:

1. Identify candidate orphan files.
2. Verify direct references with search.
3. Verify indirect references through config, globbing, loaders, or runtime conventions.
4. Remove only files proven orphaned.
5. Validate the repository using existing commands.

Prefer deleting one verified cluster at a time instead of broad cleanup across unrelated areas.

## Do Not

Avoid deleting files that are loaded dynamically by convention or runtime configuration unless the path is verified.

Avoid assuming the absence of imports means the file is dead.

Avoid deleting generated files before checking whether they are recreated by the build or required by CI.

Avoid mixing dead-file cleanup with unrelated refactors.

## Review Checklist

- [ ] The file is verified orphaned.
- [ ] Dynamic or convention-based loading was checked.
- [ ] Build, test, runtime, and tooling references were checked.
- [ ] Public or operator-facing paths were checked when relevant.
- [ ] Build and tests still pass.

## Expected Output

1. Verify the file is orphaned.
2. Check dynamic loading paths.
3. Remove dead files safely.
4. Validate the repo.
5. Keep the cleanup bounded.

## Validation

Read `package.json`, build config, and test config before deleting files.

Prefer existing repository commands such as:

- `build`
- `test`
- `lint`

If asset or runtime loading is involved, also verify the relevant app path or documented deployment path when possible.

## Exit Criteria

This skill is complete only when:

- each removed file was verified orphaned through direct or indirect reference checks
- dynamic and convention-based loading risks were reviewed
- the cleanup remained bounded to the verified orphan set
- repository validation passed or concrete blockers were reported
