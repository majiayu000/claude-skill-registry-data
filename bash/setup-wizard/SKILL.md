---
name: setup-wizard
description: Use when the user needs to diagnose and install runtime environment dependencies (Python, Node.js, uv) for running LibrAgent or MCP servers. Use on new machines, MCP "command not found" errors, or missing Python/Node runtime failures. LibrAgent 실행에 필요한 Python, Node.js 등의 환경을 자동으로 진단하고 설치하도록 안내하는 마법사입니다.
license: Complete terms in LICENSE.txt
---

# System Setup for MCP Servers

Automated installation and verification of MCP runtime dependencies.

## Path conventions

Paths in this skill are relative to this skill's Base Directory. Replace `<skill-base-dir>` with its absolute path in commands.

## Workflow

1. **Detect OS** — identify platform via terminal
2. **Check installations** — run verification commands below
3. **Install missing components** — use platform scripts or [installation-guide.md](references/installation-guide.md)
4. **Verify** — run `verify_setup` script or manual checks; confirm Python 3.11+, Node 18+, uv available

## Quick Verification

**Windows (PowerShell):**

```powershell
Get-Command python -ErrorAction SilentlyContinue
Get-Command node -ErrorAction SilentlyContinue
Get-Command uv -ErrorAction SilentlyContinue
```

**Linux/macOS:**

```bash
which python3 && python3 --version
which node && node --version
which uv && uv --version
```

Report what is missing, then load only the relevant section from the installation guide.

## Automated Scripts

Prefer scripts when the user wants hands-off install:

```powershell
# Windows examples
& "<skill-base-dir>/scripts/verify_setup.ps1"
& "<skill-base-dir>/scripts/install_python.ps1"
& "<skill-base-dir>/scripts/install_node.ps1"
& "<skill-base-dir>/scripts/install_uv.ps1"
```

```bash
# Linux/macOS examples
bash "<skill-base-dir>/scripts/verify_setup.sh"
bash "<skill-base-dir>/scripts/install_python.sh"
bash "<skill-base-dir>/scripts/install_node.sh"
bash "<skill-base-dir>/scripts/install_uv.sh"
```

## Advanced Topics

- **PATH configuration:** [PATH_CONFIG.md](references/PATH_CONFIG.md)
- **Virtual environments:** [VENV_GUIDE.md](references/VENV_GUIDE.md)
- **Offline installation:** [OFFLINE_INSTALL.md](references/OFFLINE_INSTALL.md)
- **OS-specific commands:** [installation-guide.md](references/installation-guide.md)

## Integration with LibrAgent

LibrAgent MCP servers require:

- **Python 3.11+** for Python-based MCP servers
- **Node.js 18+** for TypeScript-based MCP servers
- **uv** for fast Python dependency management

After setup, re-run the verification script before retrying failed MCP servers.
