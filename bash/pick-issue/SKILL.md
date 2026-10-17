---
name: pick-issue
description: Choose and claim one finfocus-plugin-azure-public roadmap issue, implement it through the repository workflow, open a pull request, and release the claim. Use when the user invokes pick-issue or asks to pick up a roadmap issue, optionally with an issue number.
---

# Pick a Roadmap Issue

Read and follow [the shared command](../../../.claude/commands/pick-issue.md)
before starting. That file is the maintained workflow; resolve its relative
links from `.claude/commands/` and run its shell commands from the repository
root unless a step changes directories.

Treat any issue number or other arguments in the user's invocation as inputs
to the command. This repository's OpenSpec workflow lives in the skills under
`.claude/skills/openspec-*` (Claude Code names them `/opsx:propose` and so on);
read those `SKILL.md` files when no corresponding Codex skill is available, and
run the CLI as `mise exec -- openspec ...`. Map `/code-review` and `/scout` to the corresponding
available skills; report unavailable capabilities without claiming to run them.

Apply the current session's instructions and authorization when interpreting
Claude-specific tool or permission notes. Loading or migrating this skill alone
does not authorize claiming an issue or other external actions.
