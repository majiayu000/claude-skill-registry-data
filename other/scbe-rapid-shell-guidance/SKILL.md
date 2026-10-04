---
name: scbe-rapid-shell-guidance
description: Deliver fast, low-friction PowerShell coaching for SCBE workflows with exact copy-paste commands, shell labeling (Shell A server, Shell B client), and single-step execution checks. Use when users ask for short command-first help for browser-agent startup, API tests, MCP setup, port/process fixes, or GitHub CLI operations.
---

# SCBE Rapid Shell Guidance

Use this skill to run SCBE operations quickly with minimal reading and low error rate.

## Execution Contract

- Use shell labels in every response.
- Give one command block per step.
- Keep text to one short line before each command.
- Avoid line continuations that break in PowerShell.
- Ask for pasted output after each step before advancing.

## Shell Model

- `Shell A`: Long-running service process.
- `Shell B`: API calls, test calls, and diagnostics.

## Standard Workflow

1. Define shell roles first.
2. Start service in `Shell A`.
3. Run health check in `Shell B`.
4. Run one real task call in `Shell B`.
5. If failed, run one diagnostic command and branch.
6. End with exact "what works now" and next command.

## Output Format

Use this pattern exactly:

```powershell
# Shell A
<single command>
```

```powershell
# Shell B
<single command>
```

## Recovery Rules

- If port conflict, kill listener and restart.
- If missing API key error, include header in same `Invoke-RestMethod` call.
- If `claude.exe` fails, continue with `codex mcp` commands.
- If user is fatigued, collapse to 3-step minimum: start, health, one task.

## References

- Read `references/powershell_patterns.md` for known-good commands.
