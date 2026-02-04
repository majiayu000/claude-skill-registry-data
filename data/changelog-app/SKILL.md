---
name: changelog-app
description: Update app ChangeLog entries under apps/*/ChangeLog and keep app version metadata in sync. Use when updating app versions or recording app-level changes; touches apps/*/ChangeLog and apps/*/src/*.app.src.
---

# Changelog App

## Overview

Update app ChangeLog entries and keep each app's `vsn` in sync.

## Workflow

1. Identify the target app under `apps/<app>/` and open `apps/<app>/ChangeLog`.
2. Read the top entry and check whether it is `UNRELEASED`.
3. Determine the desired next version from the latest released version (first dated entry) and the change type.
4. If an `UNRELEASED` entry exists:
   - If its version is lower than the desired next version, update the `* VERSION:` line (never lower it).
   - Update `apps/<app>/src/<app>.app.src` `{vsn, "X.Y.Z"}` to match the resulting `UNRELEASED` version.
   - Append the new change line(s) under the version line.
5. If no `UNRELEASED` entry exists:
   - Insert a new `UNRELEASED` entry at the top with the version line.
   - Update `apps/<app>/src/<app>.app.src` `{vsn, "X.Y.Z"}` to match.
   - Add the change line(s) under the version line.
6. Do not replace `UNRELEASED` with a date; only do that at release time.

## Versioning Rules

Use semantic versioning:
- Patch: fixes or small maintenance changes.
- Minor: new features or notable behavior changes.
- Major: breaking changes.

Never downgrade an existing `UNRELEASED` version; only raise it when needed.

If an existing `UNRELEASED` version is too low for the change (example: `0.1.1` but a feature is added and last release is `0.1.0`), update it and sync the `vsn`.

## Formatting Rules

Use the existing ChangeLog formatting:
- Use a header line like `UNRELEASED  ts-klassen  <qrpc@su-shiki.com>` or `YYYY-MM-DD  ts-klassen  <qrpc@su-shiki.com>`.
- Keep a blank line after the header.
- Use tabs for indentation and `*` bullets, matching the file.
- Use 2 new lines in between entries.

## Example Requests

You will mainly update the app code (Erlang, Rust, HTML, CSS, JavaScript) and write what you changed to ChangeLog

- "Please add a new erlang module `q_tut_hello_world`"
- "Add a new function `hello_world/0` to `q_tut.erl`"
- "Fix a bug in this file"

## Related skills

- changelog-root
  - After updating subsystem ChangeLog, update repository root ChangeLog
