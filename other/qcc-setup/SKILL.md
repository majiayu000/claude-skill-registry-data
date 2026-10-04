---
name: Qcc-setup
user_invocable: true
description: Sets up Claude Code and Codex shell shortcuts. Use when asked for Claude or Codex terminal aliases, cc/cx shortcuts, shell launcher setup, or restoration of the Qcc-setup workflow.
allowed-tools: Read, Write, Edit, Bash(uname:*), Bash(source:*), Bash(powershell:*)
invocation_trigger: When the user wants to inspect or install Claude Code and Codex shell aliases.
recommendedModel: haiku
---

# Qcc-setup — Claude Code and Codex Shell Shortcuts

## Role

Inspect and install short shell launchers for Claude Code and Codex without
changing unrelated shell configuration.

## Alias Sets

### Safe default

| Alias | Command |
|---|---|
| `cc` | `claude` |
| `ccc` | `claude --chrome` |
| `cx` | `codex` |

### Permission bypass — explicit opt-in only

| Alias | Command |
|---|---|
| `ccd` | `claude --dangerously-skip-permissions --chrome` |
| `cxd` | `codex --dangerously-bypass-approvals-and-sandbox` |
| `cxde` | `codex exec --dangerously-bypass-approvals-and-sandbox` |

The bypass aliases disable normal safety boundaries. Never install them from a
generic "set up shortcuts" request. Require the user to name the bypass aliases
or explicitly approve them after seeing the exact commands and risk.

## Execution Procedure

### Step 1: Detect environment

Detect the operating system and active shell. Select one target only:

- zsh: `${HOME}/.zshrc`
- bash: `${HOME}/.bashrc`
- fish: `${HOME}/.config/fish/config.fish`
- PowerShell: `$PROFILE`

If the shell or profile cannot be identified reliably, stop and report the
candidate paths instead of guessing.

### Step 2: Inspect existing definitions

Read the target profile and find existing definitions for `cc`, `ccc`, `ccd`,
`cx`, `cxd`, and `cxde`. Report conflicts with their current commands. Do not
overwrite a conflicting user definition without explicit approval.

### Step 3: Confirm scope

Show the target file and exact aliases to add or replace. Obtain confirmation
before writing the shell profile. Safe aliases and bypass aliases are separate
decisions; approval for the safe set does not authorize the bypass set.

### Step 4: Apply idempotently

Add only missing approved definitions. Use shell-appropriate syntax:

```bash
# Claude Code shortcuts
alias cc="claude"
alias ccc="claude --chrome"
# Codex shortcuts
alias cx="codex"
```

For fish, use `abbr -a`; for PowerShell, use functions because `Set-Alias`
cannot preserve arguments. Add approved bypass definitions in a separately
labelled block. Do not duplicate an identical definition.

### Step 5: Verify

Parse the updated profile to confirm every approved alias resolves to the exact
command. Report how to reload the profile or restart the terminal. Do not claim
the current parent shell changed merely because a child process sourced it.

## Will

- Detect zsh, bash, fish, and PowerShell profiles
- Preserve unrelated configuration and user-owned aliases
- Install safe launchers independently from permission-bypass launchers
- Verify the persisted definitions after writing

## Will Not

- Install any alias without confirmation
- Install `ccd`, `cxd`, or `cxde` without explicit opt-in
- Remove or silently overwrite conflicting aliases
- Change shell defaults, permissions, or unrelated profile settings
