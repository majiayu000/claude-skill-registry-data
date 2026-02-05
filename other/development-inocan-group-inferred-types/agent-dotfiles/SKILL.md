---
name: agent-dotfiles
description: Centralize coding agent configuration with dotfiles and link it into Codex/Claude/Gemini locations on Windows, macOS, or Linux. Use when asked to manage AGENTS.md or CLAUDE.md globally, set up symlinks or hardlinks for agent configs, or bootstrap a dotfiles-based agent setup.
---

# Agent Dotfiles

## Overview

Use this skill to set up a dotfiles repo for agent configuration and safely link files or folders into their tool-specific locations across Windows, macOS, and Linux.

## Workflow (Setup -> Link -> Verify)

1) Identify OS and environment:
- Windows: read `references/windows.md`
- macOS: read `references/macos.md`
- Linux: read `references/linux.md`

2) Choose dotfiles root:
- Default: `~/dotfiles` (macOS/Linux), `C:\Users\<user>\dotfiles` (Windows)
- Create it if missing and decide whether to version it with Git

3) Decide scope:
- Start with AGENTS.md only (safe default)
- Add other agent configs only if the user asks
- Do not link secrets (tokens, auth files, history logs)

4) Build a mapping file:
- Create `mappings.txt` in the dotfiles root
- Format: `source:destination` per line
- Use `references/mappings.example.txt` as a template

5) Run the linking script:
- Windows: `scripts/link_dotfiles.ps1`
- macOS/Linux: `scripts/link_dotfiles.sh`

6) Verify:
- Ensure links exist and the tools pick up changes
- If a target already exists, the scripts skip it unless force is enabled

## Safety Rules

- Do not delete existing target files by default.
- Use the force option only if a backup is acceptable.
- Avoid linking sensitive files (auth.json, tokens, history, cache).

## Resources

- `scripts/link_dotfiles.ps1` (Windows)
- `scripts/link_dotfiles.sh` (macOS/Linux)
- `references/mappings.example.txt`
- `references/windows.md`
- `references/macos.md`
- `references/linux.md`
