---
name: aiwf-windows-local-dev
description: Use for Windows local development involving PowerShell, drive and long paths, environment variables, Python virtual environments, processes, ports, DLL or PATH failures, Docker Desktop, WSL boundaries, localhost services, launchers, logs, and reproducible runtime diagnostics.
---

# AIWF Windows Local Development

## Core Rule

Map the active shell, executable, environment, process owner, port, filesystem root, and host boundary before changing configuration. On Windows, the same command name can resolve to a different Python, Node, CUDA tool, or service than the project expects.

## Workflow

1. Verify the real project path and guidance. Inspect launch scripts, environment files, lock files, service configs, Docker or WSL notes, and current processes.
2. Resolve tools instead of trusting `PATH`: use `Get-Command`, `py -0p`, explicit virtual-environment executables, and version probes.
3. Separate Windows host, WSL, container, emulator, physical device, and remote machine. State what `localhost` means for the failing process.
4. Capture the failing command, exit code, logs, process ID, bind address, and port owner before reinstalling or killing anything.
5. Apply the smallest scoped fix, then rerun the original command and a bounded health check.

## Guardrails

- Prefer process-scoped environment changes. Do not persistently modify user or machine `PATH`, execution policy, registry, firewall, or services unless Shawn explicitly asks.
- Treat Python virtual environments as disposable and path-bound. Recreate them after moving a project instead of copying or repairing absolute launcher paths blindly.
- Stop only processes proven to belong to the requested project. Do not kill by broad process name when multiple projects may be running.
- Start background helpers hidden unless interactive control is required, and record how they will be stopped.
- Keep file operations on resolved absolute paths. Verify recursive move or delete targets remain inside the intended root.
- Use Docker, WSL, and native Windows commands within their own boundary; do not assume mounted paths, GPU access, or ports cross automatically.
- Add `aiwf-gpu-runtime-diagnostics` for CUDA or driver failures and `aiwf-networking-iot` for device or site networking.

## Useful Probes

```powershell
Get-Command python,node,nvcc -ErrorAction SilentlyContinue
py -0p
Get-NetTCPConnection -State Listen
Get-Process
Test-NetConnection 127.0.0.1 -Port <port>
docker compose config
```

Run only the probes relevant to the task and redact secrets from environment or command output.

## Primary Sources

- PowerShell environment variables: https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_environment_variables
- Python virtual environments: https://docs.python.org/3.12/library/venv.html
- Docker Compose GPU support: https://docs.docker.com/compose/how-tos/gpu-support/
