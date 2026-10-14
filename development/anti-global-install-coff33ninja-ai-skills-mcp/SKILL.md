---
name: anti-global-install
description: Never install tools/packages into global system locations. Always detect and use the project's existing environment (venv, node_modules, target, vendor, etc.) or create a project-local one. Applies to all languages.
---

# Anti-Global-Install Skill

## Problem

AI agents routinely install packages into global system locations instead of the project's local environment. This causes:
- Polluting global store, breaking other projects
- Permission errors on modern systems
- Version conflicts between projects
- C drive filling up with cached packages across every language
- Environments that can't be reproduced or shared

## Rule: never install globally. Always project-local.

For EVERY language, detect what the project already has and use that. If no environment exists, create one inside the project directory.

## Language-specific protocol

### Python

**Install uv** (if not already installed):
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Installs to `~/.local\bin\` — add to PATH: `$env:Path = "$env:USERPROFILE\.local\bin;$env:Path"`

| Don't | Do |
|---|---|
| `pip install <pkg>` (global) | `uv add <pkg>` (project, updates pyproject.toml + lockfile) |
| `pip install -r requirements.txt` | `uv sync` or `uv pip sync requirements.txt` |
| `python -m pip install <pkg>` | `uvx <tool>` (one-off, no install) |
| `sudo pip install` | `uv run <cmd>` (auto-activates .venv) |
| `pipx install <tool>` | `uv tool install <tool>` |
| `pyenv install 3.12` | `uv python install 3.12` |

**Quick reference:**
| Task | Command |
|---|---|
| New project | `uv init my-project` |
| Add dep | `uv add requests` |
| Add dev dep | `uv add --dev pytest` |
| Create venv | `uv venv` |
| Run script | `uv run main.py` |
| Format code | `uv format` |
| Lint code | `uv check` |
| Build dist | `uv build` |
| Publish | `uv publish` |

Detect order: `uv.lock` > `pyproject.toml` > `.venv/` > `requirements.txt` > `Pipfile`

### Node.js / JavaScript
| Don't | Do |
|---|---|
| `npm install -g <pkg>` (global) | `npm install <pkg>` (project, adds to package.json) |
| `npm install` in wrong dir | `npm install` at project root (has package.json) |
| `yarn global add <pkg>` | `yarn add <pkg>` (project-local) |
| `pnpm add -g <pkg>` | `pnpm add <pkg>` (project-local) |

Detect order: `pnpm-lock.yaml` > `yarn.lock` > `package-lock.json` > `package.json`
Cache on C: `%APPDATA%\npm\cache`, `%LOCALAPPDATA%\pnpm\cache`

### Rust
| Don't | Do |
|---|---|
| `cargo install <tool>` (global, slow) | Use existing `Cargo.toml` dependencies |
| `rustup default` changes | Don't modify rustup config |

Detect order: `Cargo.toml` > `Cargo.lock`
Cache on C: `%USERPROFILE%\.cargo`

### Go
| Don't | Do |
|---|---|
| `go install <pkg>` (global bin) | `go get <pkg>` inside the module (updates go.mod) |
| `go install` outside module | Use existing `go.mod` |

Detect order: `go.mod` > `go.sum`
Cache on C: `%GOPATH%\pkg\mod` or `%USERPROFILE%\go\pkg\mod`

### Java / JVM
| Don't | Do |
|---|---|
| Globally install Maven/Gradle deps | Let Maven/Gradle manage their own local repos |

Detect: `pom.xml` > `build.gradle` > `build.gradle.kts`
Cache on C: `%USERPROFILE%\.m2\repository` (can grow to 10GB+)

### .NET
| Don't | Do |
|---|---|
| `dotnet tool install -g` unless needed | `dotnet add package <pkg>` (project-local) |

Detect: `*.csproj` > `*.fsproj` > `packages.config`
Cache on C: `%USERPROFILE%\.nuget\packages`

## C drive space: redirect caches off C:

Every language ecosystem caches packages on C by default. These can accumulate to 20-50GB+.

### Universal approach — set once, forget
```powershell
# Add to PowerShell profile ($PROFILE) to apply to all terminals:
$env:LANG_CACHE = "D:\.lang-cache"

# Per-language redirects (set as User environment vars):
[Environment]::SetEnvironmentVariable("UV_CACHE_DIR", "$env:LANG_CACHE\uv\cache", "User")
[Environment]::SetEnvironmentVariable("UV_PYTHON_INSTALL_DIR", "$env:LANG_CACHE\uv\python", "User")
[Environment]::SetEnvironmentVariable("UV_TOOL_DIR", "$env:LANG_CACHE\uv\tools", "User")
[Environment]::SetEnvironmentVariable("UV_TOOL_BIN_DIR", "$env:LANG_CACHE\uv\bin", "User")
[Environment]::SetEnvironmentVariable("PNPM_STORE_PATH", "$env:LANG_CACHE\pnpm\store", "User")
[Environment]::SetEnvironmentVariable("YARN_CACHE_FOLDER", "$env:LANG_CACHE\yarn", "User")
[Environment]::SetEnvironmentVariable("CARGO_HOME", "$env:LANG_CACHE\rust", "User")
[Environment]::SetEnvironmentVariable("GOPATH", "$env:LANG_CACHE\go", "User")
[Environment]::SetEnvironmentVariable("NUGET_PACKAGES", "$env:LANG_CACHE\nuget", "User")
[Environment]::SetEnvironmentVariable("GRADLE_USER_HOME", "$env:LANG_CACHE\gradle", "User")
[Environment]::SetEnvironmentVariable("MAVEN_OPTS", "-Dmaven.repo.local=$env:LANG_CACHE\maven", "User")
```

### Windows trick — auto-detect drive
Set `UV_CACHE_DIR=\.uv` (no drive letter). uv uses whatever drive the terminal is on. Projects on D: use `D:\.uv`, on E: use `E:\.uv`.

### Cross-drive hardlink warning
If cache and project are on different drives, tools may warn about hardlink fallback. Fix: `setx UV_LINK_MODE copy`

## Checklist before any package operation
- [ ] Checked for project config file (pyproject.toml, package.json, Cargo.toml, go.mod, etc.)?
- [ ] Using project-local install/add, not global (-g, --global, --system)?
- [ ] Not modifying system Python / Node / etc.?
- [ ] Cache directory redirected off C drive if this is a big dependency?
- [ ] Using the SAME package manager the project already uses (npm vs yarn, pip vs uv)?

## Cross-references

- **uv** — Dedicated skill with full command reference, flags, and env vars for the uv Python package manager.
- **portable-self-contained** — Both enforce using project-local environments over global installs.

- **os-awareness** — OS-aware install paths are critical to avoiding global installs on Windows.

- **audit-project** — Audit detects global installs that violate this rule.

- **toolchain-fallback** — Fallback toolchain installs must avoid global/system paths, using project-local or user-scoped locations instead.
- **portable-self-contained** — Both enforce project-local installs. anti-global-install's scanner detects violations.
- **skill-loader** — Apply the capped selection policy when deciding which environment skills should also be active for install checks.

## Bundled detection script

A bundled script at `scripts/detect-global-installs.ps1` (PowerShell) scans for global packages:

```powershell
.\scripts\detect-global-installs.ps1
```

Scans: npm global packages, pip --user installs, cargo --root installs, dotnet global tools. Reports each with source path and recommends project-local alternatives.

To use as a project-local tool:

```powershell
cp <skill-path>/anti-global-install/scripts/detect-global-installs.ps1 .ai_scripts/
.ai_scripts\detect-global-installs.ps1
```
