---
name: audit-project
description: Runs a systematic audit of a project — checking dependency health, security vulnerabilities, config integrity, code consistency, disk usage, and environment portability. Produces a report with findings prioritized by severity.
---

# Audit Project Skill

## Problem it solves

Projects accumulate issues silently: outdated dependencies, known vulnerabilities, inconsistent configs, environment drift, bloated caches on the system drive. These are only discovered when something breaks. A structured audit finds them before they cause failures.

## Protocol

### 1. Scope the audit

Determine the project type and set audit scope:

| Detection | Audit scope |
|-----------|-------------|
| `package.json` present | npm dependencies, scripts, config |
| `pyproject.toml` or `requirements.txt` | Python deps, venv status, uv/pip |
| `pubspec.yaml` | Flutter/Dart deps, SDK version |
| `Cargo.toml` | Rust deps, target/ size |
| `.sln` or `.csproj` | .NET deps, NuGet packages |
| Any project | Disk usage, git health, stale files |

### 2. Dependency audit

Check each dependency file for known vulnerabilities:

- **npm**: `npm audit` (or `pnpm audit` / `yarn audit`)
- **Python**: `uv pip list --outdated` or `pip-audit`
- **Flutter**: `flutter pub outdated`
- **Rust**: `cargo audit` (requires `cargo install cargo-audit`)
- **.NET**: `dotnet list package --vulnerable`

Report: number of vulnerabilities by severity (critical/high/medium/low).

### 3. Configuration audit

Check config files for inconsistencies:

- `package.json` scripts vs actual available commands
- `.env` / `.env.example` drift (keys present in one but not the other)
- `pyproject.toml` vs `requirements.txt` duplication
- `.gitignore` for missing common entries (`.venv/`, `node_modules/`, `target/`, `.env`)
- Linter/formatter config files and whether they're actually being used

### 4. Disk usage audit

Check project-local and system drive usage:

```powershell
# Project size breakdown
Get-ChildItem -Path . -Directory | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB
    [PSCustomObject]@{ Directory = $_.Name; SizeMB = [math]::Round($size, 1) }
} | Sort-Object SizeMB -Descending

# System drive free space
$free = (Get-PSDrive -Name (Get-Location).Drive.Name).Free / 1GB
if ($free -lt 10) { Write-Warning "Only $free GB free on system drive" }
```

Flag directories over 500 MB as bloated.

### 5. Environment portability audit

Check against portable-self-contained rules:

- Are venvs/SDKs project-local or system-global?
- Are there scripts in the root instead of `scripts/`?
- Does a `SETUP.md` or `setup.ps1` exist?
- Are there absolute paths hardcoded in config files?

### 6. Git health audit

```powershell
git fsck --no-dangling           # repo integrity
git stash list                   # unapplied stashes
git log --oneline --since="6 months ago" --until="3 months ago" | Measure-Object | Select-Object Count  # commit gap detection
```

Report: large files in git history, uncommitted changes, stale branches.

### 7. Report format

Write the report to `audit-report.md` with sections:

```markdown
# Audit Report: <project-name>

## Summary
X critical, Y high, Z medium, W low findings.

## 1. Dependencies
### Critical
- issue | path | fix

### High
- ...

## 2. Configuration
...

## 3. Disk Usage
...

## 4. Environment Portability
...

## 5. Git Health
...
```

### 8. Prioritize and offer fixes

After the report, ask the user which findings to fix. Do not fix anything without confirmation.

## Detection triggers

Activate when user says:
- "audit this project"
- "check for issues"
- "run a health check"
- "what's wrong with this project"
- "why is my project so large"

## When NOT to use
- User asks for a specific single check (use the appropriate tool directly)
- CI/CD pipeline already runs automated audits
- User explicitly asks not to modify or report

## Cross-references

- **self-validate** — Both run systematic checks. audit-project is broader (dependencies, disk, git); self-validate focuses on change integrity.
- **security-best-practices** — Audit findings may trigger security best-practice remediation. security-best-practices implements the fixes.
- **portable-self-contained** — Audit checks environment portability against the rules in portable-self-contained.
- **follow-existing-patterns** — Audit should check whether project code follows its own established patterns.
- **verify-and-cite** — Audit findings must cite specific evidence (file paths, versions, command output).

- **toolchain-fallback** — Audit should check that toolchain detection is part of the project's setup and CI configuration.
- **project-backup-status** — Audit should verify backup status and that backup scripts are in place.
- **project-scripts** — Run project-scripts first to catalog scripts before auditing them for consistency and coverage.
- **release-changelog** — Audit should check versioning consistency (single source of truth, version file matches changelog) and that changelog follows the project's established format.
- **skill-loader** — Apply the expanded audit-task cap when deciding which audit-relevant skills should also be active.

## Bundled audit script

A bundled script at `scripts/audit.ps1` (PowerShell) automates a subset of audit checks:

```powershell
.\scripts\audit.ps1 -ProjectPath ".\"
.\scripts\audit.ps1 -ProjectPath ".\" -Report
```

Checks include: npm audit (if package.json found), cargo audit (if Cargo.toml found), config file validity, disk usage, and git health (stashes, commits ahead).

To use as a project-local tool:

```powershell
cp <skill-path>/audit-project/scripts/audit.ps1 .ai_scripts/
.ai_scripts\audit.ps1 -ProjectPath "."
```
