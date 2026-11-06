---
name: start
description: Set up, check or fix Sentry in this repo. Detects the stack, decides between auditing an existing setup and initializing a missing one, and walks it through to a verified result.
disable-model-invocation: true
allowed-tools: Bash(sentry-ctx *), Read, Grep, Glob
argument-hint: "[what you want, optional]"
---
# /sentry:start

> Codex: the `!` lines below are not run for you. Run each one yourself as `<plugin root>/bin/sentry-ctx ...` (the plugin root is two folders above this file), then follow its output.

!`sentry-ctx flow start`

User request (may be empty): $ARGUMENTS

Read `sentry-ctx flow preamble`, `sentry-ctx flow audit` and `sentry-ctx flow init` with Bash when the flow above tells you to run them,
then follow them step by step.
