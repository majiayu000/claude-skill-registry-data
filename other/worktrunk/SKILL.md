---
name: worktrunk
description: Use native Worktrunk commands for explicit Git worktree operations when requested. Distinguish repository selection from worktree selection, and inspect command help before changing configuration or hooks.
---

# Worktrunk

This is a small Codex adaptation of the [upstream Worktrunk skill](https://github.com/max-sixty/worktrunk/blob/5ba6f148e8505c20794f2d8bc706aa4f26335c95/skills/worktrunk/SKILL.md). Use `wt --help` and the relevant subcommand's `--help` for current syntax. The pinned release includes `wt` and `git-wt`.

`wt -C PATH` selects the repository or working directory for a command. A branch argument selects a worktree; do not treat it as a path or assume that `-C` selects that branch. Inspect `wt list` and the selected branch before switching, creating, or removing a worktree.

Worktrunk has user and project configuration. Inspect the relevant configuration and native help before changing either. Hooks may run commands and may require trust; request explicit approval before enabling or changing hooks. Do not use `--yes` to bypass that decision. Do not set up agent multiplexers or create LLM commits unless requested.

Follow the repository's own worktree and Git rules. If Improve owns a worktree, use its `codex-improve` lifecycle rather than independently changing that worktree.
