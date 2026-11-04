---
name: setup
description: Interactive first-time project setup that fills missing env values, starts required services, runs migrations and seeds, and verifies the app starts.
disable-model-invocation: true
argument-hint: "/setup"
allowed-tools: "Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion"
sensitive: true
---

## Overview

First-time project setup that detects the stack, installs dependencies, configures the environment, starts required services, runs database migrations and seeds, and verifies the application starts. Interactive: prompts for missing non-secret environment values in chat, hands secret values to a script the user runs, and confirms before starting services.

## When to use

- When cloning a new project and setting it up for the first time.
- When onboarding to a project and the README setup steps are unclear or incomplete.
- When returning to a project after a long time and the environment may be stale.
- When a teammate asks "how do I get this running?"

Neighbouring work has its own skill:

- For managing production infrastructure, use `/infra`.
- For deploying to staging or production, use `/deploy`.
- For generating a README, use `/readme`.
- For updating dependencies, use `/audit deps`.

## Arguments

This skill takes no arguments. Run `/setup` and it walks through everything interactively.

## Steps

1. **Detect the project type.** Read the root directory for manifest files. Check for these in order:
   - `package.json`: Node.js project. Check for `pnpm-lock.yaml`, `yarn.lock`, or `package-lock.json` to determine the package manager.
   - `go.mod`: Go project.
   - `Cargo.toml`: Rust project.
   - `pyproject.toml` or `requirements.txt`: Python project.
   - `Makefile`: check for language-specific targets.
   - `docker-compose.yml` or `compose.yml`: containerized services.
   - If multiple manifest files exist, report all detected project types.

2. **Check prerequisites.** For each detected project type, verify the required runtime is installed. If `which mise` finds `mise` and the project has a `.mise.toml`, `.tool-versions`, `.node-version`, `.nvmrc`, `.python-version`, `.ruby-version`, or `.terraform-version` file, run `mise install` once to install every pinned runtime, then `mise current` to verify resolution. After that, the per-runtime checks below confirm the right version is active:
   - Node.js: `node --version`. Compare against `.node-version`, `.nvmrc`, `.tool-versions`, `.mise.toml`, or the `engines` field in `package.json`.
   - Go: `go version`. Compare against `.tool-versions` or `.mise.toml`.
   - Rust: `rustc --version` and `cargo --version`. Compare against `rust-toolchain.toml`.
   - Python: `python3 --version`. Compare against `.python-version`, `.tool-versions`, `.mise.toml`, or `pyproject.toml` requires-python.
   - Docker: `docker --version` and `docker compose version`.
   - If a prerequisite is missing and `mise` cannot resolve it, report it and stop. Do not install runtimes manually.

3. **Install dependencies.**
   - Node.js with pnpm: `pnpm install`.
   - Node.js with yarn: `yarn install`.
   - Node.js with npm: `npm ci`.
   - Go: `go mod download`.
   - Rust: `cargo build`.
   - Python with `uv.lock` or a `pyproject.toml`: `uv sync`, per [`rules/lang/python.md`](../../rules/lang/python.md). Never a bare `pip install`.
   - Python with only `requirements.txt`: `uv venv` then `uv pip install -r requirements.txt`.
   - Python with poetry: `poetry install`.
   - Report the result: success or failure with the error output.

4. **Environment setup.** Check for `.env.example` or `.env.template` in the project root; the commands below name `.env.example`, so substitute the template file when that is the one present. Never read `.env` values into the conversation; work with key names only.
   - If `.env` does not exist, create it from the example with owner-only permissions: `(umask 077 && cp .env.example .env)`.
   - List the keys that are missing, empty, or still equal to the example value. This prints names, never values:

     ```bash
     awk -F= 'NR == FNR && /^[A-Za-z_][A-Za-z0-9_]*=/ { example[$1] = substr($0, length($1) + 2); next } NR == FNR { next } $1 in example { present[$1] = 1; value = substr($0, length($1) + 2); if (value == "" || value == example[$1]) { print $1 } } END { for (key in example) { if (!(key in present)) { print key } } }' .env.example .env
     ```

   - Classify each listed key. A key is secret-shaped when its name contains `KEY`, `SECRET`, `TOKEN`, `PASSWORD`, `PASS`, `PWD`, `PRIVATE`, `CREDENTIAL`, `AUTH`, `SALT`, or `DSN`, or when it holds a connection string that can carry credentials, such as `DATABASE_URL` or `REDIS_URL`. When unsure, treat the key as secret-shaped.
   - For each non-secret key, ask in chat: show the variable name, the description from comments in `.env.example` if available, and the default value if one exists. Accept the default if the user presses enter, and write the answer to `.env`.
   - For the secret-shaped keys, generate a wizard script so the values never pass through the conversation. Write it to the project workspace as `setup-env.sh`, resolving the root with [`hooks/_lib/project_workspace.py`](../../hooks/_lib/project_workspace.py) the same way [`/checkpoint`](../checkpoint/SKILL.md) does, or to the scratchpad directory outside a git repository. Fill `KEYS` with the secret-shaped names and leave the rest of the template unchanged:

     ```bash
     #!/usr/bin/env bash
     set -euo pipefail

     ENV_FILE="${ENV_FILE:-.env}"
     MAX_ATTEMPTS=3
     KEYS=(DATABASE_URL STRIPE_SECRET_KEY)

     has_value() {
       [[ -f "$ENV_FILE" ]] && grep -qE "^${1}=.+" "$ENV_FILE"
     }

     write_env() {
       local key="$1" value="$2" tmp sq="'\\''"
       [[ -e "$ENV_FILE" ]] || (umask 077 && : >"$ENV_FILE")
       tmp=$(umask 077 && mktemp)
       grep -vE "^${key}=" "$ENV_FILE" >"$tmp" || true
       printf "%s='%s'\n" "$key" "${value//\'/$sq}" >>"$tmp"
       cat "$tmp" >"$ENV_FILE"
       rm -f "$tmp"
     }

     ask_secret() {
       local key="$1" value attempt rc
       for ((attempt = 1; attempt <= MAX_ATTEMPTS; attempt++)); do
         value=""
         rc=0
         if has_value "$key"; then
           printf '%s [Enter keeps the saved value]: ' "$key"
         else
           printf '%s: ' "$key"
         fi
         IFS= read -rs value || rc=$?
         printf '\n'
         if [[ -z "$value" ]] && has_value "$key"; then
           printf 'Kept %s.\n' "$key"
           return 0
         fi
         if [[ -n "$value" ]]; then
           write_env "$key" "$value"
           printf 'Saved %s.\n' "$key"
           return 0
         fi
         if ((rc != 0)); then
           printf 'Input closed before %s was entered.\n' "$key" >&2
           return 1
         fi
         printf '%s is required.\n' "$key" >&2
       done
       return 1
     }

     main() {
       local key missing=""
       for key in "${KEYS[@]}"; do
         ask_secret "$key" || missing="$missing $key"
       done
       if [[ -n "$missing" ]]; then
         printf 'Still missing:%s\n' "$missing" >&2
         return 1
       fi
       printf 'Every value is saved in %s.\n' "$ENV_FILE"
     }

     main "$@"
     ```

   - Check the script with `bash -n` and `shellcheck`, then tell the user to run `bash <path>` from the project root in their own terminal window. Never suggest the `!` prefix: a `!` command gets no terminal input, so `read -rs` hits end of file and every key is reported missing. Input is hidden with `read -rs`, a new `.env` is created under `umask 077`, a re-run offers each saved value as the Enter default without showing it, a closed input stream ends the loop instead of spinning, and no value is ever echoed.
   - After the user reports the script finished, rerun the key-name listing above to confirm every key now has a value. The script holds key names only, so it may stay in the workspace for a later re-run.
   - Never overwrite values the user has already set in `.env`.

5. **Detect required services.** Scan these sources for service dependencies:
   - `docker-compose.yml` or `compose.yml`: list all services defined.
   - `.env.example`: look for connection strings or host variables that imply services: `DATABASE_URL`, `REDIS_URL`, `MONGODB_URI`, `ELASTICSEARCH_URL`, `RABBITMQ_URL`, `KAFKA_BROKERS`.
   - For each detected service, check if it is already running:
     - PostgreSQL: `pg_isready -h localhost` or check the port.
     - Redis: `redis-cli ping`.
     - MongoDB: `mongosh --eval "db.runCommand({ping:1})"` or check the port.
     - Docker services: `docker compose ps`.

6. **Offer to start services.** For each service that is not running:
   - If a docker-compose file defines the service, offer to start it: `docker compose up -d <service>`.
   - Wait for health checks to pass before proceeding. Use `docker compose ps` to verify the service reports as healthy.
   - If the service is not in docker-compose, inform the user that the service needs to be started manually and provide the typical connection details from the env vars.

7. **Run database setup.** Detect the ORM or migration tool:
   - Prisma: `pnpm exec prisma migrate dev` or `pnpm exec prisma db push` depending on the project stage. Then `pnpm exec prisma db seed` if a seed script exists.
   - Knex: `pnpm exec knex migrate:latest` then `pnpm exec knex seed:run` if seeds exist.
   - TypeORM: `pnpm exec typeorm migration:run`.
   - Django: `python manage.py migrate` then `python manage.py loaddata` if fixtures exist.
   - SQLAlchemy with Alembic: `alembic upgrade head`.
   - If no ORM is detected but `DATABASE_URL` exists, inform the user that manual database setup may be needed.

8. **Verify the application starts.** Detect the start command:
   - Node.js: check `package.json` scripts for `dev`, `start:dev`, or `start`.
   - Go: `go run .` or check a Makefile target.
   - Python: check for a `main.py`, `app.py`, or framework-specific entry point.
   - Start the application. Wait up to 15 seconds for a health check endpoint or for the process to stabilize.
   - If the app starts and responds to a health check, report success.
   - If the app crashes, capture the error output and report it with diagnostic suggestions.
   - Stop the application after verification. This is a setup check, not a long-running process.

9. **Present the setup report.**

   ```
   ## Setup Complete

   **Project:** <detected type and framework>
   **Runtime:** <version>
   **Package manager:** <name and version>

   ### Dependencies
   Installed successfully.

   ### Environment
   - .env created from .env.example
   - N variables configured

   ### Services
   | Service | Status |
   |---------|--------|
   | PostgreSQL | running on localhost:5432 |
   | Redis | running on localhost:6379 |

   ### Database
   - Migrations applied: N
   - Seed data loaded: yes/no

   ### Application
   Started successfully on http://localhost:3000

   ### Next steps
   - Run `pnpm dev` to start development
   - Run `pnpm test` to verify tests pass
   ```

## Rules

- Never overwrite an existing `.env` file. Merge missing values only.
- Never read, print, or ask in chat for a secret-shaped value. The wizard script collects it in the user's terminal, per [`rules/security.md`](../../rules/security.md).
- Always check if services are already running before attempting to start them. Starting a second instance on the same port causes errors.
- Always verify the application actually starts. "Dependencies installed" is not "setup complete."
- Never install runtimes or system-level tools automatically. Report what is missing and let the user decide how to install.
- When a step fails, report the error clearly and continue with the remaining steps where possible. A failed database migration should not prevent reporting what else was configured.
- Use `pnpm` for every JavaScript and TypeScript project. A project with `package-lock.json` or `yarn.lock` is converted: `pnpm import`, delete the old lockfile, and pin `packageManager`.
- When docker-compose starts a service, wait for its health check before running migrations. A started container is not a ready service.

## Common Rationalizations

- "Pasting the API key in chat is faster than running a script": a value in chat is in the transcript and counts as disclosed. The wizard script reads it with `read -rs` in the user's terminal.
- "The key name looks harmless, so ask for it in chat": the classification in step 4 decides, and an unsure call counts as secret-shaped.
- "Dependencies installed, so setup is done": setup is done when the app starts and answers its health check in step 8.
- "The container is up, so run the migrations": `docker compose ps` must report the service healthy first.
- "The runtime is missing, so install it quickly": runtimes come from `mise` or from the user. Report the gap and let the user choose.

## Red Flags

- Stop and switch to the wizard script when the next message would ask for, print, or echo a secret-shaped value.
- Stop and merge only missing keys when the next write would replace a value already set in `.env`.
- Stop and report the missing prerequisite when `mise` cannot resolve a pinned runtime.
- Stop and report the crash output with diagnostic suggestions when the app exits during step 8.

## Verification

- The key-name listing from step 4 prints nothing after the wizard script finishes.
- No secret-shaped value appears anywhere in the conversation.
- Every detected service reports healthy or running before migrations ran.
- The app started, answered a health check or stayed up for the 15-second window, and was stopped afterward.
- The setup report lists every step, with the error output for any step that failed.

## Related skills

- `/onboard` - Understand the codebase structure and architecture.
- `/infra` - Manage infrastructure for local development.
- `/test` - Run the suite, coverage, and lint once setup is complete.
