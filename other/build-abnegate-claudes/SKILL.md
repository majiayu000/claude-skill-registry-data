---
name: build
description: Build the project (auto-detects build system)
argument-hint: "[target]"
---

# Build Project

Build the project using the detected build system.

## Arguments

- `$ARGUMENTS` - Optional build target or arguments to pass to the build command

## Build System Detection (Parallel)

Launch parallel agents to check for multiple build system files simultaneously:

**Agent 1 — JVM Build Systems**:
Check for: `build.gradle.kts`, `build.gradle`, `pom.xml`

**Agent 2 — Native/Systems Build Systems**:
Check for: `Cargo.toml`, `go.mod`, `Makefile`, `CMakeLists.txt`, `build.zig`

**Agent 3 — Web/Scripting Build Systems**:
Check for: `package.json`, `deno.json`, `bun.lockb`, `composer.json`, `Gemfile`, `mix.exs`, `setup.py`, `pyproject.toml`

**Agent 4 — Container Build Systems**:
Check for: `compose.yaml`, `compose.yml`, `docker-compose.yaml`, `docker-compose.yml`, `Dockerfile`

Use the first match from the combined results, prioritized in the order below.

### Detection Priority Table

| File | Build System | Build Command | Test Command |
|------|--------------|---------------|--------------|
| `build.gradle.kts` | Gradle (Kotlin DSL) | `./gradlew build` | `./gradlew test` |
| `build.gradle` | Gradle (Groovy) | `./gradlew build` | `./gradlew test` |
| `pom.xml` | Maven | `mvn package` | `mvn test` |
| `Cargo.toml` | Cargo (Rust) | `cargo build` | `cargo test` |
| `package.json` | Node.js | `<pm> run build` | `<pm> test` |
| `go.mod` | Go | `go build ./...` | `go test ./...` |
| `Makefile` | Make | `make` | `make test` |
| `CMakeLists.txt` | CMake | `cmake --build .` | `ctest` |
| `setup.py` / `pyproject.toml` | Python | `pip install -e .` | `pytest` |
| `Gemfile` | Ruby | `bundle install` | `bundle exec rake test` |
| `mix.exs` | Elixir | `mix compile` | `mix test` |
| `build.zig` | Zig | `zig build` | `zig build test` |
| `deno.json` | Deno | `deno task build` | `deno test` |
| `bun.lockb` | Bun | `bun run build` | `bun test` |
| `composer.json` | PHP (Composer) | `composer install` | `composer test` or `./vendor/bin/phpunit` |
| `compose.yaml` / `docker-compose.yml` | Docker Compose | `docker compose build` | `docker compose run --rm test` |
| `Dockerfile` | Docker | `docker build -t <image> .` | N/A |

## Execution

1. **Detect**: Run parallel detection agents above
2. **Report**: Tell user which build system was detected
3. **Build**: Run the appropriate build command
   - If `$ARGUMENTS` provided, append to build command or use as target
4. **Verify (Parallel)**: After successful build, launch TWO parallel agents:
   - **Agent 1 — Run Tests**: Execute the test command for the detected build system
   - **Agent 2 — Run Lint**: Execute the lint/format-check command if one exists for the detected build system (e.g., `./gradlew ktlintCheck`, `<pm> run lint`, `cargo clippy`, `go vet ./...`)
5. **Report**: Show build status, test results, lint results, and summary

### Node.js Specifics (Parallel Detection)

For Node.js projects, launch TWO parallel agents to determine configuration:

**Agent 1 — Detect Package Manager** (check for lock files in priority order):
- `bun.lockb` -> use `bun`
- `pnpm-lock.yaml` -> use `pnpm`
- `yarn.lock` -> use `yarn`
- Otherwise -> use `npm`

**Agent 2 — Check package.json Scripts**:
- Read `package.json` and determine available scripts
- If `build` script exists: `<pm> run build`
- If `build` script doesn't exist but it's a TypeScript project: `<pm> exec tsc` or `npx tsc`
- Note available `test` and `lint` scripts for verification phase

### Gradle Specifics

- Use `./gradlew` wrapper if present, otherwise `gradle`
- For multi-module projects, `./gradlew build` builds all modules

### Rust Specifics

- Use `--release` flag for production builds: `cargo build --release`
- If `$ARGUMENTS` is "release", build in release mode

### PHP Specifics

For PHP projects with `composer.json`:

1. **Install dependencies**: `composer install`
2. **Run tests**:
   - If `test` script exists in `composer.json` scripts: `composer test`
   - Otherwise, check for PHPUnit: `./vendor/bin/phpunit`
   - Or PHPStan for static analysis: `./vendor/bin/phpstan analyse`
3. **Build** (if applicable):
   - If `build` script exists: `composer run build`
   - Laravel: `php artisan optimize`
   - Symfony: `php bin/console cache:clear`

### Docker Specifics

**Docker Compose** (preferred when present):

1. **Check for compose files** (in order):
   - `compose.yaml` (modern standard)
   - `compose.yml`
   - `docker-compose.yaml`
   - `docker-compose.yml`

2. **Build**: `docker compose build $ARGUMENTS`
   - Arguments passed directly (e.g., `/build --no-cache`, `/build api`)

3. **Run tests** (if test service exists): `docker compose run --rm test`

**Dockerfile only** (no compose file):

1. **Determine image name**: Use directory name as default tag

2. **Build**: `docker build -t <dirname> . $ARGUMENTS`
   - Arguments passed directly (e.g., `/build --no-cache`, `/build -f Dockerfile.dev`)
   - If multiple Dockerfiles exist, ask user which to build (unless `-f` specified)

## Test Failures

**IMPORTANT:** If any tests fail during or after the build, fix them. There is no such thing as a "pre-existing" test failure - all test failures must be resolved before the task is considered complete. The task always completes with completely passing tests.

## Error Handling (Parallel Diagnosis)

If the build fails, launch TWO parallel agents to diagnose:

**Agent 1 — Analyze Error Output**:
- Parse the build error output
- Identify the root cause (missing dependency, syntax error, type error, etc.)
- Propose a specific fix

**Agent 2 — Search for Similar Patterns**:
- Grep the codebase for similar patterns that compile successfully
- Check recent git history for changes that may have introduced the breakage
- Look for related configuration or dependency changes

Once both agents complete, synthesize their findings to apply the fix, then re-run the build. Repeat until the build succeeds.

If no build system detected:
- Report to user that no recognized build system was found
- List the files checked
- Ask user how to build the project
