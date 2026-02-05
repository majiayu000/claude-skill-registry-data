---
name: terminal-workspace
description: Terminal workspace management with Zellij. Use when user mentions terminal sessions, workspaces, Zellij, terminal layouts, or persistent terminal environments. Covers session management, layout saving, and the zp quick-access alias.
---

# Terminal Workspace Management

Persistent terminal workspaces per project using Zellij.

## Core Concepts

- **Sessions**: Working state (ephemeral, survives disconnects)
- **Layouts**: Workspace recipes (permanent, recreatable)
- **Real persistence**: Lives in applications (vim sessions, git)

## Quick Access

```bash
# In ~/.zshrc or ~/.bashrc
alias zp='zellij attach $(basename "$PWD") || zellij -s $(basename "$PWD")'
```

Run `zp` in any project directory to create/attach its workspace.

## Save Important Layouts

```bash
# If you have a complex setup worth preserving
zellij action dump-layout > ~/.config/zellij/layouts/project-name.kdl
```

## Philosophy

Zellij sessions for convenience, not critical state. If it matters, it's in a file.
