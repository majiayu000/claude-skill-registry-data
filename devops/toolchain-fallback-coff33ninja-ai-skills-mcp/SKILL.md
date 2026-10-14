---
name: toolchain-fallback
description: Detects available build toolchains (MSYS2, Zig, GCC, Clang, Visual Studio) and falls back to a working alternative when none are found. Any implementation scripts follow the project's scripts/ folder convention.
---

# Toolchain Fallback Skill

## Problem it solves

Builds fail because the required toolchain isn't installed. MSYS2 users assume everyone has GCC. Zig users assume everyone has Zig. The project has no detection logic, so errors are cryptic (`'gcc' is not recognized`). The CI and the developer machine disagree on what's available.

## Detection triggers

Activate when:
- A build step requires a C/C++ compiler, linker, or build system
- Setting up a new development environment
- Adding CI/CD build steps
- User reports "command not found" or "not recognized" for a build tool

## Protocol

### 1. Detect available toolchains

Run detection commands to inventory what's on the system. Check in this preferred order:

| Toolchain | Detection | Fallback priority |
|-----------|-----------|-------------------|
| MSYS2 | `where gcc`, check `C:\msys64\`, `C:\msys32\`, scoop installs | 1 (Windows native) |
| Zig | `where zig`, check `%LOCALAPPDATA%\zig\` | 2 (cross-platform, portable) |
| Clang/LLVM | `where clang`, `where ld.lld` | 3 |
| GCC (standalone) | `where gcc` (not MSYS2 path) | 4 |
| Visual Studio | `vswhere -latest` | 5 (Windows only, heavy) |
| Make / Ninja | `where make`, `where ninja` | — |

### 2. Fallback strategy

If zero toolchains are found:

- **Preferred fallback: Zig** — single self-contained binary with a bundled C/C++ cross-compiler. Works on Windows, Linux, macOS. No installer needed — download and extract. Follows the portable-self-contained pattern of project-local installs.
- **If Zig is unsuitable** (e.g., project specifically needs MSYS2 makefiles): fall back to MSYS2 via `winget install MSYS2.MSYS2` or Scoop.
- **CI/CD fallback**: Use `ubuntu-latest` or `windows-latest` runner images which include GCC/MSVC by default.

### 3. Scripting convention

Any automated detection or install logic goes in `scripts/` (per project convention):

```
scripts/
├── ensure-toolchain.ps1     # detect + install fallback
├── build.ps1                # uses detected toolchain
└── ci-setup.ps1             # ensures CI has what it needs
```

Scripts should:
- Accept `-InstallMissing` flag to auto-install the fallback
- Accept `-DryRun` to show what would happen without changing anything
- Report each toolchain found with `[+]` / `[-]` status prefixes
- Not modify global system state (per portable-self-contained)
- Add Zig or other tools to user-scoped PATH, not system-wide

### 4. Verification

After detection or install, verify by running a trivial compile:

- **Zig**: `zig build-exe hello.zig` or `zig version`
- **GCC**: `gcc --version && echo 'int main(){}' | gcc -x c - -o test`
- **MSVC**: `cl /?` or `msbuild /version`

Report the verified toolchain version in the output.

### 5. CI/CD integration

In GitHub Actions workflows, use the detection script as a setup step:

```yaml
- name: Ensure toolchain
  shell: pwsh
  run: ./scripts/ensure-toolchain.ps1 -InstallMissing
```

The `-InstallMissing` flag allows the same script to work both locally (where you may have nothing) and in CI (where the runner may have partial tooling).

## When NOT to use
- Pure Python/JS/Rust projects with no native compile step
- Docker-based builds where the toolchain is in the image
- User explicitly specifies a single required toolchain and accepts the manual install burden

## Cross-references

- **portable-self-contained** — Section 6 defines the `scripts/` folder convention for all tooling scripts. toolchain-fallback's detection and install scripts must be placed there and follow project-local install rules.
- **os-awareness** — Toolchain detection paths and fallback logic differ by OS (MSYS2 on Windows, apt/homebrew on Linux/macOS).
- **audit-project** — The audit should include toolchain availability as part of environment portability checks.
- **anti-global-install** — Fallback installs (e.g. Zig) must use project-local or user-scoped paths, never system-wide.
- **project-scripts** — Install and build scripts discovered by project-scripts should use the detected toolchain for consistency.
- **self-validate** — Validate that the installed toolchain actually works after fallback install.
- **skill-loader** — Apply the capped selection policy when deciding which environment and validation guardrails should also be active for toolchain setup.
- **ci-cd-automation** — Use together to detect available toolchains before writing pipeline configs. toolchain-fallback detects tools; ci-cd-automation wires them into pipelines.

## Bundled detection script

A bundled script at `scripts/ensure-toolchain.ps1` (PowerShell) automates detection and fallback install:

```powershell
.\scripts\ensure-toolchain.ps1                    # detect only
.\scripts\ensure-toolchain.ps1 -InstallMissing     # install zig if nothing found
.\scripts\ensure-toolchain.ps1 -DryRun             # preview without changes
```

Checks: MSYS2, Zig, Clang, GCC, Visual Studio, Make/Ninja. Reports `[+]`/`[-]` status for each.

To use as a project-local tool:

```powershell
cp <skill-path>/toolchain-fallback/scripts/ensure-toolchain.ps1 .ai_scripts/
.ai_scripts\ensure-toolchain.ps1 -InstallMissing
```
