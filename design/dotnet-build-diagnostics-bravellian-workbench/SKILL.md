---
name: dotnet-build-diagnostics
description: Capture dotnet environment and CI-style build diagnostics with binlog and summary output.
---

# dotnet-build-diagnostics

Collect build diagnostics, including a binlog and a summary log suitable for sharing in chat.

## Outputs
- `artifacts/codex/build.binlog`
- `artifacts/codex/build-summary.txt`

## Requirements
- `dotnet` CLI
- `python3` (bash script only)
- PowerShell (`pwsh`) for Windows

## Run

Bash:
```bash
bash .codex/skills/dotnet-build-diagnostics/scripts/run-build-diagnostics.sh
```

PowerShell:
```powershell
pwsh -File .codex/skills/dotnet-build-diagnostics/scripts/run-build-diagnostics.ps1
```

## Guidance for sharing errors
- Open `artifacts/codex/build-summary.txt` and paste only the error list and the first few lines of any stack trace into chat.
- If the log is large, include the first error block and the last 50 lines of the build output.
- We will iterate by fixing one error at a time and re-running the script to confirm progress.
