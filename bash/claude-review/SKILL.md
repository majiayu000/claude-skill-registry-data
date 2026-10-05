---
name: claude-review
description: Review the current worktree or a base diff with Claude.
---

You are the thin skill wrapper for Claude Companion review runs.

Supported flags:

- `--base <ref>`
- `--model <alias>`
- `--effort <level>`
- `--json`

Pass only the flags listed above, placed before any review focus text. Never add Claude Code CLI flags such as `--dangerously-skip-permissions`; the script manages the Claude Code invocation itself and rejects unknown flags.

This command runs the user's locally installed Claude Code CLI under the user's own Anthropic account. The data flow is the same as the user running `claude` in their own terminal in this workspace.

1. Treat the remaining user text after the skill mention as raw command arguments.
2. Resolve `<plugin-root>` as the directory two levels above this `SKILL.md` file; it is the directory containing `scripts/`, `skills/`, `prompts/`, and `schemas/`.
3. Run `node <plugin-root>/scripts/claude-companion.mjs review <remaining arguments>` from the user's current workspace.
4. Return stdout verbatim.
5. If the command exits non-zero, surface stderr verbatim.
6. Do not implement logic in this skill.
