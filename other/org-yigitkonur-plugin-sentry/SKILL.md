---
name: org
description: Audit the Sentry organization behind this repo (projects, keys, filters, scrubbing, spike protection, alerts, monitors, releases, source maps, ownership, usage, Seer settings) with read-only probes, then apply only the org changes you approve.
disable-model-invocation: true
allowed-tools: Bash(sentry-ctx *), Read, Grep, Glob
argument-hint: "[org-slug] [project ...]"
---
# /sentry:org

> Codex: the `!` lines below are not run for you. Run each one yourself as `<plugin root>/bin/sentry-ctx ...` (the plugin root is two folders above this file), then follow its output.

!`sentry-ctx flow org`

Org and projects if given (otherwise detect them): $ARGUMENTS
