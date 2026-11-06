---
name: apply
description: Implement the approved Sentry findings (one commit per group, fix-safety protocol), then verify them with a live event and clean up.
disable-model-invocation: true
allowed-tools: Bash(sentry-ctx *), Read, Grep, Glob
argument-hint: "[finding ids]"
---
# /sentry:apply

> Codex: the `!` lines below are not run for you. Run each one yourself as `<plugin root>/bin/sentry-ctx ...` (the plugin root is two folders above this file), then follow its output.

!`sentry-ctx flow apply`

Only these findings if given (otherwise every approved one): $ARGUMENTS
