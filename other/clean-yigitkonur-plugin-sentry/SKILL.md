---
name: clean
description: Remove the plugin's artifacts from this repo (.sentry-plugin/, leftover temporary trigger files, the .gitignore line it added). Shows what would go first.
disable-model-invocation: true
allowed-tools: Bash(sentry-ctx *)
---
# /sentry:clean

> Codex: the `!` lines below are not run for you. Run each one yourself as `<plugin root>/bin/sentry-ctx ...` (the plugin root is two folders above this file), then follow its output.

Dry run (nothing is deleted yet):

!`sentry-ctx clean`

Show the user exactly what would be removed and what is kept. Ask (AskUserQuestion): delete everything / keep only `policy.md` /
keep everything (reports) / cancel. Then run `sentry-ctx clean --yes` with `--keep policy` or `--keep all` as chosen. If the output
says the `.gitignore` line was added by the plugin and the folder is gone, ask whether to remove that line too
(`--gitignore-line remove`).
