---
name: doctor
description: "Check that this machine is ready for Sentry work: which CLI is installed, login and scopes, org region, git state, and whether Sentry's own plugins are present."
disable-model-invocation: true
allowed-tools: Bash(sentry-ctx *)
---
# /sentry:doctor

> Codex: the `!` lines below are not run for you. Run each one yourself as `<plugin root>/bin/sentry-ctx ...` (the plugin root is two folders above this file), then follow its output.

Environment report from the plugin engine:

!`sentry-ctx doctor`

Explain it to the user in plain words: what is ready, what is missing, and the one command to fix each gap (the user runs
logins and installs themselves; never install anything and never ask for a token). Say what each missing piece costs: without a
login every org-side audit row is reported UNVERIFIED; with only `sentry-cli` 3.x the plugin uses the v3 command names from
`sentry-ctx cli-map`.
