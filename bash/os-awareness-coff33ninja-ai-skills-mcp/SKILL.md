---
name: os-awareness
description: Forces the AI to detect, confirm, and remember the host operating system before any command execution, file operation, or path construction. Prevents Linux-isms on Windows, wrong path separators, incorrect shebangs, and incompatible shell syntax.
---

# OS Awareness

## Rule 1: Detect Before You Act

Before running any command, reading any file, or writing any path, explicitly know what OS you're on. Do not assume.

If you don't know, run one of these at the very start of the session:
- **Windows**: `[System.Environment]::OSVersion.VersionString`
- **macOS / Linux**: `uname -a`

## Rule 2: Remember the OS for the Entire Session

Once detected, keep it in context. Do not re-detect unless you're in a new session or a subagent that wasn't told.

Key differences to track:

| Aspect | Windows (PowerShell) | Linux / macOS (bash) |
|---|---|---|
| Path separator | `\` | `/` |
| Environment variable | `$env:VAR` | `$VAR` or `${VAR}` |
| Home dir | `$env:USERPROFILE` | `$HOME` |
| Temp dir | `$env:TEMP` | `/tmp` |
| Line ending | CRLF | LF |
| Case sensitivity | Case-insensitive paths | Case-sensitive (Linux) |
| Executable extension | `.exe`, `.ps1` | no extension |
| Shell syntax | `&&`, `||`, `;` all work in pwsh | same but different quoting |
| Quoting | double for interpolation, single for literal | same |
| File tools | backtick escape, double-quote paths with spaces | single-quote paths |

## Rule 3: OS-Specific Gotchas

### Windows-Specific
- Always quote paths with spaces: `"C:\Program Files\..."` — pwsh will split on spaces without quotes
- Use `New-Item`, `Remove-Item`, `Get-ChildItem` instead of `mkdir`, `rm`, `ls` for scripted operations
- Prefer `Test-Path` over `[ -f ]` or `[ -d ]`
- Git: LF/CRLF warnings are cosmetic — don't worry about them
- Node/Python: use `npx.cmd` / `python` not `npx` / `python3`
- Never use `sudo`, `apt`, `brew`, `chmod`, `chown`, `systemctl`, or `kill -9`

### Linux-Specific
- Always prefer single quotes for paths to avoid shell expansion
- `~` expands to home directory
- Use `/tmp` for temp work
- Never use `C:\` paths, `$env:`, or `Get-ChildItem`
- No `.exe` extension needed
- Be careful with case-sensitive filenames

### macOS-Specific
- Same as Linux but note `brew` may be available
- `$TMPDIR` instead of `/tmp` (usually)
- Case-insensitive filesystem by default (like Windows)

## Rule 4: Subagents Must Be Told

When spawning a subagent via `task`, include the OS info in the prompt so the subagent doesn't have to re-detect.

*Example: "The host OS is Windows 11 (pwsh). Use PowerShell syntax and Windows paths."*

## Cross-references

- **anti-global-install** — OS detection prevents wrong install paths on Windows.

- **portable-self-contained** — Portable environment setup depends on OS-aware paths.

- **toolchain-fallback** — Toolchain paths and fallback strategies differ per OS; OS-aware detection is required.
- **anti-global-install** — OS detection determines correct install paths vs global defaults.
- **skill-loader** — Apply the capped selection policy when deciding which platform-aware skills should also be active for cross-platform tasks.

## Bundled OS detection script

A bundled script at `scripts/detect-os.ps1` (PowerShell) returns the host OS environment:

```powershell
.\scripts\detect-os.ps1                    # human-readable report
.\scripts\detect-os.ps1 -Json              # JSON for programmatic use
```

Returns: platform (Windows/macOS/Linux), shell, path separator, case sensitivity, line ending convention, and syntax notes for each OS.

To use as a project-local tool:

```powershell
cp <skill-path>/os-awareness/scripts/detect-os.ps1 .ai_scripts/
.ai_scripts\detect-os.ps1 -Json
```
