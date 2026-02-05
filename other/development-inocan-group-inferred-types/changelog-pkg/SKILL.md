---
name: changelog-pkg
description: Update pkgsrc ChangeLog entries under config/pkgsrc/files/*/*/ChangeLog and keep Makefile version metadata in sync. Use when updating qrpc-devel or qrpc-prod ChangeLogs, updating their versions, or recording dependency changes.
---

# Changelog Pkg

## Overview

Update pkgsrc ChangeLog entries and keep Makefile versions consistent. Only meta-pkgs are reflected in the repository root ChangeLog.

## Workflow

1. Identify the target package (example: `qrpc-devel` or `qrpc-prod`) under `config/pkgsrc/files/<category>/<pkg>/` and open `config/pkgsrc/files/<category>/<pkg>/ChangeLog`.
2. Read the top entry in `ChangeLog` and check whether it is `UNRELEASED`.
3. Determine the desired next version from the latest released version (first dated entry) and the change type.
4. If an `UNRELEASED` entry exists:
   - If its version is lower than the desired next version, update the `* VERSION:` line (never lower it).
   - Update `DISTNAME` in the package `Makefile` to match the resulting `UNRELEASED` version.
   - If the ChangeLog includes a `* PACKAGE VERSIONS:` list (meta-pkgs), update it to match the `DEPENDS` versions in the `Makefile` and keep the same order.
   - Append the new change line(s) under the version list.
5. If no `UNRELEASED` entry exists:
   - Insert a new `UNRELEASED` entry at the top with the version line and package list (meta-pkgs only).
   - Update `DISTNAME` in the `Makefile` to match the new `UNRELEASED` version.
   - Add the change line(s) under the list.
6. Do not replace `UNRELEASED` with a date; only do that at release time.

## Versioning Rules

Use semantic versioning:
- Patch: fixes or small maintenance changes.
- Minor: new features or notable behavior changes.
- Major: breaking changes.

Never downgrade an existing `UNRELEASED` version; only raise it when needed.

If an existing `UNRELEASED` version is too low for the change (example: `0.1.1` but a feature is added and last release is `0.1.0`), update it and sync `DISTNAME`.

## Formatting Rules

Use the existing ChangeLog formatting:
- Use a header line like `UNRELEASED  ts-klassen  <qrpc@su-shiki.com>` or `YYYY-MM-DD  ts-klassen  <qrpc@su-shiki.com>`.
- Keep a blank line after the header.
- Use tabs for indentation and `*` bullets, matching the file.
- Use 2 new lines in between entries.

## Root ChangeLog Impact

Only ChangeLogs under `config/pkgsrc/files/meta-pkgs/*/ChangeLog` are reflected in the repository root ChangeLog. Other packages (example: `config/pkgsrc/files/audio/voicevox_core/ChangeLog`) do not trigger a root ChangeLog update.

## Example Requests

You will be asked to update the Makefile mainly.

- "Add this package to devel package."
- "Add this package to prod package."
- "Update version of rust-bin package to x.x.x."

## Related skills

- changelog-root
  - After updating meta-pkgs ChangeLog, update repository root ChangeLog
