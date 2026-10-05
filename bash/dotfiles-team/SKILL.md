---
name: dotfiles-team
description: Spawn a dotfiles team for changes spanning chezmoi templates, mise config, and system validation. Use when adding tools that need both mise config and shell config changes.
user-invocable: true
argument-hint: <dotfiles-change-description>
context: fork
agent: mise-specialist
---

# Dotfiles/Config Team Spawn Recipe

## Team Composition

| Role | Model | Tools | Purpose |
|------|-------|-------|---------|
| **Lead/Coordinator** (you) | inherit | All | Coordinate cross-system changes |
| **Mise Specialist** | Haiku | Read, Glob, Grep, Bash | Handle mise.toml changes |
| **Chezmoi Specialist** | Haiku | Read, Glob, Grep, Bash | Handle chezmoi template changes |
| **Validator** | Haiku | Read, Glob, Grep, Bash | Run validation after changes |

## Spawn Protocol

1. **Analyze** the change: Does it need mise config, chezmoi templates, or both?
2. **Spawn mise-specialist** and **chezmoi-specialist** in parallel:
   - Mise: tool version changes, backend selection, task runner updates
   - Chezmoi: template edits under `home/`, OS-conditional logic
3. **Spawn validator** after both complete:
   - `uv run mde-py validate --all`
   - `mise doctor`
   - `chezmoi doctor`
4. **Coordinate** any conflicts between mise and chezmoi changes

## File Ownership (No Conflicts)

| Owner | Owns | Cannot Touch |
|-------|------|-------------|
| Mise Specialist | `.mise.toml`, `mise.toml`, `mise.lock` | `home/` |
| Chezmoi Specialist | `home/**/*` | `.mise.toml` |
| Validator | Nothing (read + run) | Config files |
| Lead | `Brewfile`, `pyproject.toml` | Delegates config |

## Decision Tree

```
Does this change need...
├── Only mise config? → mise-specialist alone
├── Only shell/dotfile config? → chezmoi-specialist alone
├── Both? → both in parallel, then validator
└── Also Brewfile? → add brew-specialist
```

## Key Rules
- mise config at `~/.config/mise/config.toml` is chezmoi-managed
- Changes MUST go through `home/dot_config/mise/config.toml.tmpl`
- Full lifecycle: edit template -> `chezmoi apply` -> `mise install` -> `mise lock` -> `mise reshim`
