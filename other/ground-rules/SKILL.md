---
name: ground-rules
description: "Use before writing or reviewing Sentry configuration or SDK setup: sentry.init, Sentry.init, sentry_sdk.init, sentry.client/server/edge config, instrumentation.ts, .sentryclirc, sentry.properties, SENTRY_DSN or SENTRY_AUTH_TOKEN, sentry or sentry-cli CI steps. How to work with Sentry here: look options up instead of recalling them, keep tokens out of files, claim only what was verified, confirm before org changes. For production incidents use triage."
allowed-tools: Bash(sentry-ctx *), Read, Grep, Glob
---
# Sentry ground rules

> Codex: the `!` lines below are not run for you. Run each one yourself as `<plugin root>/bin/sentry-ctx ...` (the plugin root is two folders above this file), then follow its output.

!`sentry-ctx ref forge/ground-rules`

Commands: `/sentry:start` (guided), `/sentry:audit`, `/sentry:init`, `/sentry:apply`, `/sentry:doctor`, `/sentry:policy`, `/sentry:clean`.
Lookups: `sentry-ctx docs page <path> --section <s>`, `sentry-ctx ref <module>`, `sentry-ctx cli-map`, `sentry-ctx stale`.
