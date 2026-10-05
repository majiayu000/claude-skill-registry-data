---
name: doctor
description: Check the codex-claude-loop substrate (codex CLI, jq, git, repo, verdict schema)
allowed-tools: Bash, Read
---

Load the `codex-claude-loop` skill, source its lib, and run `cl_doctor`.

Report each check plainly. If `codex` is missing, point at `npm install -g @openai/codex`
then `codex login`. If the repo resolved is not the one the user means, tell them to set
`CL_REPO`. Do not start a wave until every check passes.

If the user is running this harness for the first time, offer `cl_selfreview` — Codex
adversarially reviewing this harness before they trust it with their tree.
