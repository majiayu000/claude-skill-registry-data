---
name: Terminal / Shell
description: Execute system commands on the server.
---

# Terminal Skill

## Capabilities
- **Execute Command**: Run shell commands (`git`, `ls`, `grep`, `npm test`) via `terminal.execute`.

## Usage
- Use when the user asks to "run a system check", "check git status", or "list files detailed".
- Primary user: **Deebo (Enforcer)** for auditing and diagnostics.

## Security & Constraints
- **CRITICAL**: This provides direct access to the underlying OS shell.
- Confined to the permissions of the running node process.
- Operations are performed in the project root by default.
