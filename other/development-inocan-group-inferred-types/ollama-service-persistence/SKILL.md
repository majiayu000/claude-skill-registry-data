---
name: ollama-service-persistence
description: "Create, update, and validate a persistent Windows service for Ollama (auto-start on boot), including setting OLLAMA_MODELS and managing the service lifecycle. Use when Ollama must be always-on or models must live in a custom directory."
---

# Ollama Service Persistence (Windows)

Use this skill to install or update a Windows Service that runs `ollama serve` with a fixed `OLLAMA_MODELS` path.

## Quick start (admin PowerShell)

1) Install/update persistence (try Task Scheduler first; Startup fallback if tasks are blocked) and point models to the repo store:

```powershell
.\skills\operations\ollama-service-persistence\scripts\ollama_service_manager.ps1 -Action Install -Mode Task -TaskScope Auto -ModelsDir "C:\Users\usuario\Business\CLI_A1_GHR\CLI-main\models" -OllamaHost "127.0.0.1:11435"
```

Startup fallback (no Task Scheduler needed):

```powershell
.\skills\operations\ollama-service-persistence\scripts\ollama_service_manager.ps1 -Action Install -Mode Startup -ModelsDir "C:\Users\usuario\Business\CLI_A1_GHR\CLI-main\models" -OllamaHost "127.0.0.1:11435"
```

2) Check status:

```powershell
.\skills\operations\ollama-service-persistence\scripts\ollama_service_manager.ps1 -Action Status -Mode Task
```

Startup status:

```powershell
.\skills\operations\ollama-service-persistence\scripts\ollama_service_manager.ps1 -Action Status -Mode Startup
```

3) Verify models:

```powershell
ollama list
```

## Notes

- Requires admin privileges (service create/config + system env var).
- The script writes/updates `scripts\ollama_service.ps1` in the repo root and uses it as the service runner.
- If `sc.exe` returns 1053, use `-Mode Task` (Task Scheduler). `ollama.exe` is not a native Windows service.
- `-TaskScope Auto` tries SYSTEM at boot, then falls back to USER at logon if SYSTEM is denied.
- If Task Scheduler is blocked, use `-Mode Startup` to drop a user logon launcher in the Startup folder.
- If `sc.exe` returns “Access denied,” run the command in an elevated PowerShell session.
- Manual fallback: `ollama serve` is non-persistent and must be started after reboot.

## Removal

```powershell
.\skills\operations\ollama-service-persistence\scripts\ollama_service_manager.ps1 -Action Remove
```
