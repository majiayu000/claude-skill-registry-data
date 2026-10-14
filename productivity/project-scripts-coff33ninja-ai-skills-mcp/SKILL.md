---
name: project-scripts
description: Discovers, catalogs, and manages project scripts (install, download, build, setup, clean). Scans conventional script locations, detects AI-generated and user-created scripts, and generates missing standard scripts. Use when setting up a new project, looking for available scripts, or ensuring script consistency.
---

# Project Scripts

## Problem it solves

Projects accumulate scripts in inconsistent locations — some in `scripts/`, some in the root, some as `package.json` entries, Makefile targets, or CI workflow steps. AI agents and users both create scripts, but there's no catalog of what exists, what each script does, or which standard scripts are missing. This leads to duplicated effort, forgotten utilities, and confusion about how to build/test/run the project.

## Protocol

### 1. Discover scripts from all conventional locations

Scan these locations in order:

| Location | What to look for |
|---|---|
| `scripts/` directory | `.ps1`, `.sh`, `.bat`, `.py` files |
| Project root | `.ps1`, `.sh`, `.bat`, `.py`, `.cmd` files |
| `package.json` | `scripts` section (npm tasks) |
| `Makefile` | Top-level targets (install, build, test, clean) |
| `Justfile` / `Taskfile.yml` | Named tasks |
| `.github/workflows/` | CI job names and run steps |
| `tools/` or `bin/` | Executable scripts and wrappers |

### 2. Classify each script by category

Group discovered scripts into standard categories:

| Category | Common names | Purpose |
|---|---|---|
| **Install** | `install.ps1`, `install.sh`, `setup.ps1` | Install dependencies, SDKs, tooling |
| **Download** | `download.ps1`, `fetch.ps1` | Download assets, data, binaries |
| **Build** | `build.ps1`, `build.sh`, `Makefile` | Compile, bundle, or build the project |
| **Setup** | `setup.ps1`, `bootstrap.sh`, `init.ps1` | First-time environment setup |
| **Test** | `test.ps1`, `test.sh`, npm `test` | Run test suite |
| **Lint** | `lint.ps1`, npm `lint` | Run linters and formatters |
| **Clean** | `clean.ps1`, `clean.sh` | Remove build artifacts |
| **Deploy** | `deploy.ps1`, `deploy.sh`, npm `deploy` | Deploy to environments |
| **Utility** | Any other helper script | Ad-hoc automation |

### 3. Detect undocumented or orphaned scripts

For each discovered script, check:
- Does it have a description in a `scripts/README.md` or doc comment?
- Is it referenced in the project README or SETUP.md?
- Is it still needed (check `git log` for recent usage)?
- Is it duplicated (same purpose as another script in a different location)?

Report undocumented scripts as warnings, not errors — they may still be useful.

### 4. Generate missing standard scripts

If the project is missing common standard scripts, offer to create them:

- `install.ps1` / `install.sh` — install project dependencies
- `build.ps1` / `build.sh` — build the project
- `clean.ps1` / `clean.sh` — remove build artifacts
- `setup.ps1` / `setup.sh` — full environment bootstrap

Generated scripts should follow the project's existing patterns (same language, same status prefix format, same error handling style).

### 5. Present a script catalog

When asked about available scripts, present them in a structured format:

```markdown
## Available Scripts

| Script | Category | Description | Source |
|---|---|---|---|
| `scripts\install.ps1` | Install | Install Python dependencies via uv | user-created |
| `scripts\build.ps1` | Build | Build the project | ai-generated |
| `package.json → test` | Test | Run pytest | user-created |
```

Indicate whether each script is user-created (written by the developer) or AI-generated (created by an agent in a prior session).

## Detection triggers

Activate when:
- Setting up a new project environment
- User asks "how do I build/test/run this?"
- User asks "what scripts are available?"
- Starting work on a project for the first time
- User reports a missing or broken script
- After generating new scripts for a project

## When NOT to use

- Project has no scripts and doesn't need them (pure library with standard build tools)
- User explicitly asks about a single known script (use direct file read instead)
- Already familiar with the project's script layout from prior session

## Cross-references

- **portable-self-contained** — Section 6 defines the `scripts/` folder convention. This skill discovers scripts wherever they are; portable-self-contained prescribes where they should go.

- **follow-existing-patterns** — Generated scripts must match the project's existing script patterns (language, style, error handling).

- **audit-project** — Script discovery is part of a project audit; run this skill first to catalog scripts before auditing them.

- **release-changelog** — Before cutting a release, discover build, test, and deploy scripts.

- **self-validate** — After generating or modifying scripts, validate they actually run.

- **project-backup-status** — Discover scripts before backup to ensure all scripts are captured in the backup scope.

- **universal-format-lint** — After creating or modifying scripts, run formatters for consistent style.

- **toolchain-fallback** — Install and build scripts should use the detected toolchain; this skill catalogs what exists.

- **uv** — The ensure-uv.ps1 script is a project install script this skill would discover and catalog.
- **ci-cd-automation** — Use to discover existing build/test/deploy scripts before writing the pipeline configuration.
