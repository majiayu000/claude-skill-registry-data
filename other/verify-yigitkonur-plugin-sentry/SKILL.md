---
name: verify
description: "Prove applied Sentry changes with a live marked event: arrival, readable stack trace, privacy scan of the arrived payload. Claims only the verification rung actually reached."
disable-model-invocation: true
allowed-tools: Bash(sentry-ctx *), Read, Grep, Glob
argument-hint: "[finding ids]"
---
# /sentry:verify

> Codex: the `!` lines below are not run for you. Run each one yourself as `<plugin root>/bin/sentry-ctx ...` (the plugin root is two folders above this file), then follow its output.

!`sentry-ctx flow verify`

Only these findings if given (otherwise every applied one): $ARGUMENTS
