---
name: stack-detection
description: Identify a project's technology stack from file signals — canonical signal-to-stack table.
---

# Stack Detection

Use file signals to infer the project's primary stack before making technology decisions.

## Signal → Stack Table

The canonical table is `scripts/lib/stack-signals.json` (installed: `.dev-team-agents/scripts/lib/stack-signals.json`). It is the single source of truth read by `devteam detect`; edit rows there, never here. `devteam detect --json` returns the result as `stack.primary`, `stack.all` and `stack.signals`, so prefer running it over matching files by hand.

| Stack | Typical signals (summary — the JSON is authoritative) |
|-------|--------------------------------------------------------|
| Python | `pyproject.toml`, `requirements.txt`, `setup.py`, `*.py` in root |
| TypeScript/Node.js | `package.json` + `tsconfig.json`, `*.ts`/`*.tsx` in `src/` |
| JavaScript/Node.js | `package.json` without tsconfig, `*.js` in `src/` |
| Rust | `Cargo.toml` |
| PHP | `composer.json`, `*.php` in root or `src/` |
| Ruby | `Gemfile`, `*.rb` in `app/` |
| Go | `go.mod` |
| Java | `pom.xml`, `build.gradle`, `*.java` in `src/` |
| Kotlin | `build.gradle.kts`, `*.kt` in `src/` |
| C#/.NET | `*.csproj`, `*.sln`, `Program.cs` |
| Flutter/Dart | `pubspec.yaml`, `*.dart` in `lib/` |
| React Native | `app.json` with `expo`, or `package.json` with `react-native` |

## Multi-stack Projects

If multiple signals coexist (e.g., `package.json` + `go.mod`), identify the PRIMARY stack:
1. Check `CLAUDE.md` or project README for explicit stack declaration
2. Count files: the stack with the most source files is primary (`devteam detect` does this)
3. Check for API/service separation (e.g., `backend/` in Go, `frontend/` in TS)

## Tooling Detection

Some facts cannot be read from a file signal — they depend on what is installed on the machine. Probe once, record the answer, and never re-detect.

### Docker Compose command form

Compose v2 is a Docker CLI plugin (`docker compose`); v1 is a standalone binary (`docker-compose`). The two are not interchangeable in scripts.

```bash
if docker compose version >/dev/null 2>&1; then
    DOCKER_COMPOSE="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
    DOCKER_COMPOSE="docker-compose"
else
    DOCKER_COMPOSE=""
fi
```

| Result | Meaning | Action |
|--------|---------|--------|
| `docker compose` | Compose v2 plugin available | Use this form in all commands and docs |
| `docker-compose` | Legacy v1 standalone binary | Use this form; note the version in project docs |
| empty | Compose not installed | Do not emit compose commands; tell the user what to install |

Record the result in the project's `CLAUDE.md` as `DOCKER_COMPOSE: docker compose` (or `docker-compose`) so every agent uses the correct form without re-probing.

## Usage

After detecting the stack, load the appropriate platform-specific skills (e.g., `skills/devops/`, `skills/integrations/`).
