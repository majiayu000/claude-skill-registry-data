---
name: release
description: Review release readiness by checking ChangeLogs and version definitions and then create a git tag for the requested version. Use when asked to release or tag a version (e.g., "Please release 0.2.0", "Please tag 0.2.0") or to verify ChangeLog/version consistency before tagging.
---

# Release

## Overview

Review all ChangeLogs and version metadata for consistency with the target release version, then create a git tag that matches the version string (no "v" prefix).

## Workflow

0. Read changelog-* skills first
   - Read `changelog-root`, `changelog-app`, and `changelog-pkg` before opening any ChangeLog files.

1. Confirm the target version
   - Parse the version from the user request (example: `0.2.0`).
   - If the version is ambiguous or missing, ask for it before proceeding.

2. Review ChangeLogs for release readiness (UNRELEASED entries only, across all ChangeLogs)
   - Root ChangeLog: `ChangeLog`
   - App ChangeLogs: `apps/*/ChangeLog`
   - pkgsrc ChangeLogs: `config/pkgsrc/files/*/*/ChangeLog`
   - Use the changelog-* skills when interpreting ChangeLog structure and versioning rules.
   - Confirm the top entries include the target version in the root ChangeLog and note whether they are `UNRELEASED` or dated.
   - Compare the previous git release tag to the target version and verify the root ChangeLog covers the core changes between those versions.
   - Verify each ChangeLog’s `* VERSION:` lines are correct for that component; do not force app/pkg ChangeLogs to match the repo release version.
   - For root ChangeLog, verify `* SUBSYSTEM VERSIONS:` against `apps/*/src/*.app.src` and `* PACKAGE VERSIONS:` against `config/pkgsrc/files/meta-pkgs/*/Makefile`.
   - Review `UNRELEASED` entries in every ChangeLog.
   - If any ChangeLog is missing the target version, lacks core details for the release range, or shows a lower `UNRELEASED` version, abort the release process and enter fixing mode.
   - In fixing mode: update the ChangeLog/version content as needed, then ask for human review. Do not continue the release process after making fixes.

3. Review version definitions
   - `rebar.config` release version defines the repo release version.
   - App versions: `apps/*/src/*.app.src` `vsn` values.
   - pkgsrc versions: `config/pkgsrc/files/*/*/Makefile` `DISTNAME` versions.
   - App/pkg versions may differ from the repo release version; they must match their own ChangeLog entries and the root ChangeLog’s subsystem/package lists.
   - If any mismatch is found, abort the release process and enter fixing mode.
   - In fixing mode: update the version files as needed, then ask for human review. Do not continue the release process after making fixes.

4. Confirm git status and existing tags
   - Check `git status` and note any uncommitted changes.
   - Check `git tag --list` for an existing tag matching the version.
   - If the tag already exists, ask before proceeding.
   - Review `git log` from the previous tag through HEAD to confirm the ChangeLog captures the core changes.

5. Finalize release entries and commit
   - If everything is OK, replace all `UNRELEASED` headers with today’s date.
   - Use `apply_patch` for these edits; do not run Python or other scripts to modify files.
   - Use the version from `rebar.config` as the release version, even if subsystem/package versions differ.
   - Include all ChangeLog updates in a single commit with the message `Bump version to X.Y.Z`.
   - If any fixes were made in fixing mode, stop after asking for human review and do not continue to commit/tag.

6. Create the release tag
   - Tag the bump commit with a lightweight tag that matches the version string exactly (example: `git tag 0.2.0`).
   - Do not add a "v" prefix unless explicitly requested.
   - Do not push the tag unless the user asks.

## Notes

- Only change version files when instructed; otherwise report mismatches and wait for confirmation.
