---
name: install
description: Run Skadi's dual installer to sync Claude Code and Codex configuration into each registered paired profile.
user_invocable: true
args: ""
---

# Install Skadi Agent Config

Syncs the Skadi repository into paired Claude Code and Codex homes. The shared
registry is `~/.skadi/install/roots.tsv`, with one tab-separated row per
`profile`, `claude-root`, and `codex-root`.

## Workflow

### 1. Resolve config roots

Read `~/.skadi/install/roots.tsv`.

**If the registry exists and has valid rows**, use them.

**If the registry is missing or empty**, explain that `--all` registers one
pair and installs it:

```
default  ~/.claude  ~/.codex
```

An extra profile is never taken by default — the run closes by printing how to
add one, how to launch it (`CLAUDE_CONFIG_DIR` / `CODEX_HOME`), and the aliases
that bind each to a word. Pass that closing text on rather than restating it.

For a custom mapping, ask for the paired Claude and Codex roots, then use
`install.sh --pair`; that command records the pair.

### 2. Run the installer

Resolve the repo root via `git rev-parse --show-toplevel`. The skill is loaded from `.claude/skills/install/`, so the working directory is inside the skadi repo by definition.

For all registered roots:

```bash
"$(git rev-parse --show-toplevel)/install.sh" --all
```

Show the script's output.

### 3. Report paths

For each pair, print:

```
<profile>:
  Claude          <claude-root>/CLAUDE.md, settings.json, hooks/, skills/
  Codex           <codex-root>/AGENTS.md, hooks.json, rules/, hooks/, skills/
```

## Rules

- Use only `--all`, `--pair`, `--claude`, or `--codex` as documented by
  `install.sh --help`.
- If `git rev-parse --show-toplevel` fails, the working directory is not inside a git repo — stop and ask the user to `cd` into the skadi repo before invoking `/install`
- If the resolved repo root has no `install.sh` at its top, stop and tell the user this isn't the skadi repo
- If the registry looks malformed, stop and report the bad row; do not guess.
- After a Codex install, remind the user to start a new session and review the
  new or changed hooks with `/hooks`.
