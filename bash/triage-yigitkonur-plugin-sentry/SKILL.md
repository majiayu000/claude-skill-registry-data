---
name: triage
description: "Use when the user asks why something is failing or erroring in production, asks for the top or recent Sentry errors or regressions, mentions a Sentry alert, or names a Sentry issue (short id like API-7 or a sentry.io issues URL). Walks the CLI funnel rank, view, corroborate; Seer only on request. Not for setup or configuration."
allowed-tools: Bash(sentry issue list *), Bash(sentry issue view *), Bash(sentry issue events *), Bash(sentry event view *), Bash(sentry explore *), Bash(sentry log list *), Bash(sentry replay list *), Bash(sentry trace *), Bash(sentry span *), Bash(sentry-ctx *), Bash(jq *), Bash(rm /tmp/*), Read, Grep, Glob
argument-hint: "[issue id, URL or question]"
---
# Triage a production symptom with the sentry CLI

> Codex: the `!` lines below are not run for you. Run each one yourself as `<plugin root>/bin/sentry-ctx ...` (the plugin root is two folders above this file), then follow its output.

!`sentry-ctx ref forge/triage`

Start from: $ARGUMENTS
