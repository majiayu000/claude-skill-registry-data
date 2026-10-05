---
name: setup-diagnosis
description: This skill should be used when the user mentions "setup", "getting started", "install dependencies", "dev environment", "onboarding", "won't run", "version mismatch", "devcontainer", "env vars", "works on my machine", or a failing local install/build. It maps where a repo declares its runtime needs and how to diagnose and fix the common setup failures that block a green build on day one.
---

# Setup Diagnosis

## Purpose
The biggest day-one sink is getting a green build: missing dependencies, the wrong runtime version, OS-specific breakage, missing env vars, and silently outdated README steps. This skill provides two things, a **map of where a repo declares what it needs** (so you stop guessing) and a **catalog of the common failure modes and their fixes**: so bootstrapping becomes detect → run → diagnose → verify, not trial and error.

## Principle: read the declared requirements, don't guess
A repo almost always tells you what it needs, in machine-readable files. Trust those over prose READMEs, which drift. Reconcile pins across files before running anything.

## Where requirements live (quick map)
| Need | Look in |
|------|---------|
| Runtime version | `.nvmrc`, `.tool-versions`, `mise.toml`, `.python-version`, `.ruby-version`, `engines`, `go.mod`, `<java.version>` |
| Package manager | `packageManager` field, lockfile kind, `Gemfile`/`poetry.lock`/`Pipfile.lock` |
| Dependencies | `package.json`, `pyproject.toml`/`requirements*.txt`, `Gemfile`, `go.mod`, `pom.xml`/`build.gradle`, `Cargo.toml` |
| Backing services | `docker-compose.yml`, `.devcontainer/`, infra manifests |
| Env vars / config | `.env.example`, `.env.sample`, `config/*.example`, the code that reads config |
| The blessed path | `Makefile`/`justfile`/`Taskfile.yml` setup targets, `scripts/setup`, `CONTRIBUTING` |

See `setup-signals.md` for the full precedence and reconciliation rules.

## The bootstrap loop
1. **Detect** every requirement from the files above; cite the file for each.
2. **Prefer the project's own setup target** (`make setup`, `just bootstrap`, `./scripts/setup`) over hand-assembled steps.
3. **Establish the runtime first** with a version manager, not a global install.
4. **Start backing services**, and wait for readiness before install/migrate/seed.
5. **Run install/build/migrate/seed**, capturing real output.
6. **On failure, classify then fix** (see `setup-failures.md`); apply the least-invasive safe fix.
7. **Verify boot** with a smoke step, then record only confirmed-working steps in `SETUP.md`.

## Failure triage (first cut)
| Symptom | Likely class |
|---------|--------------|
| `engine incompatible`, modern-syntax `SyntaxError`, major class-file version | Wrong runtime version |
| `node-gyp`, `pg_config not found`, linker/headers error | Missing system lib / native build |
| Crashes on an undefined config key | Missing env var |
| `EADDRINUSE`, `address already in use` | Port conflict |
| `CRLF`, `fsevents`, path/case errors | OS-specific difference |
| lockfile/peer-dep conflict, yanked version | Dependency resolution |

## Additional Resources
### Reference Files
- **`references/setup-signals.md`**: every place a repo declares runtime/version/service/env requirements, the precedence between them, and how to reconcile conflicting pins (e.g. `.nvmrc` vs `engines` vs a stale README).
- **`references/setup-failures.md`**: the common failure modes (wrong runtime version, missing system libs, missing env vars, native build failures, port conflicts, OS differences, dependency resolution) with the tell-tale error strings and their concrete fixes.
