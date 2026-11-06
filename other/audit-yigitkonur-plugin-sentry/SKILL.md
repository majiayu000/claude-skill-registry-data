---
name: audit
description: "Audit the Sentry setup in this repo (and optionally the Sentry org): find what is missing, wrong or risky across errors, tracing, profiling, replay, logs, crons, releases, source maps, privacy and more, then offer to fix it."
disable-model-invocation: true
allowed-tools: Bash(sentry-ctx *), Read, Grep, Glob
argument-hint: "[unit ...]"
---
# /sentry:audit

> Codex: the `!` lines below are not run for you. Run each one yourself as `<plugin root>/bin/sentry-ctx ...` (the plugin root is two folders above this file), then follow its output.

!`sentry-ctx flow preamble`

!`sentry-ctx flow audit`

Limit to these units if given (otherwise all): $ARGUMENTS
