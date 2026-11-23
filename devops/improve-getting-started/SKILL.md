---
name: improve-getting-started
description: >
  Audit and improve the developer onboarding experience -- finds gaps between
  what the README says and what actually works (runtime versions, service
  startup, migrations), then updates the docs so a new developer can go from
  clone to running tests with confidence. Use when someone says "does the README
  still work", "clone to running tests", "onboarding is broken", "our setup docs
  are stale", or "can a new hire get this running". For checking whether env vars
  themselves are fully documented or contain leaked secrets, defer to
  align-env-checklist instead of auditing that here.
---

# improve-getting-started

You are a developer onboarding assistant. Your job is to audit and improve the getting-started experience for new developers on this project: find the gaps between what the README or docs say and what actually works, and update the documentation so someone can go from clone to running tests with confidence.

Run this when onboarding a new developer, after significant project setup changes, or when the "first day" experience is broken.

---

## Step 1 — Find the onboarding documentation

Locate all files that describe the setup process:

```bash
ls README.md README.mdx CONTRIBUTING.md docs/ .github/
cat README.md
cat CONTRIBUTING.md 2>/dev/null
cat docs/development.md 2>/dev/null || cat docs/dev.md 2>/dev/null
```

If there is no onboarding documentation at all, that is itself the primary finding.

Record:

- which file is the canonical "getting started" entry point
- what setup steps it currently describes
- when it was last meaningfully updated (check git log)

---

## Step 2 — Identify the actual setup requirements

Discover what the project actually needs by reading the source of truth:

```bash
# runtime requirements
cat .node-version .nvmrc .tool-versions .python-version .go-version 2>/dev/null
node --version; npm --version; npx tsc --version 2>/dev/null

# dependency manager
ls package.json yarn.lock pnpm-lock.yaml pyproject.toml go.mod Cargo.toml

# infrastructure / services
ls docker-compose.yml docker-compose*.yml Dockerfile

# environment configuration
cat .env.example 2>/dev/null
```

Also inspect the project scripts:

```bash
cat package.json | grep -A 30 '"scripts"'
cat Makefile 2>/dev/null | grep "^[a-z]"
```

Build a checklist of everything a new developer needs to do before running the project:

- install a runtime (Node version, Python version, Go version, etc.)
- install dependencies
- start services (Docker, database, cache)
- configure environment variables
- run migrations or seed the database
- run the app / tests

---

## Step 3 — Walk through the documented steps critically

For each step in the existing documentation:

- can it be followed exactly as written?
- are the commands still accurate?
- are prerequisites stated in the right order?
- are version requirements specified?
- are there any steps that silently fail without a clear error?

Flag:

- outdated commands or package names
- missing prerequisites that are assumed but not stated
- environment variables that are required but not in `.env.example`
- services that need to be running but are not mentioned
- manual steps that are not documented (migrations, DB seeds, etc.)

---

## Step 4 — Identify common first-day failure points

Look for known sources of new-developer friction:

```bash
git log --oneline --diff-filter=M -- README.md CONTRIBUTING.md .env.example 2>/dev/null | head -20
```

Common failure patterns:

- Node version mismatch (missing `.nvmrc` or version not pinned)
- missing services in `docker-compose.yml` vs what the app actually needs
- `.env.example` is out of date or missing new required variables
- database migration step is not documented
- test command requires a running database or seed data
- private registry or internal package not documented

---

## Step 5 — Test the setup flow

If it can be done safely and the environment allows:

- try to follow the documented steps from scratch
- or trace through each step logically to verify it would work

Record any step that would fail or require undocumented prior knowledge.

---

## Step 6 — Update the documentation

Fix the gaps found in Steps 3–4:

Preferred structure for a getting-started guide:

````markdown
## Prerequisites

- Node 20+ (use nvm: `nvm use`)
- Docker and Docker Compose
- ...

## Setup

1. Clone and install dependencies
   ```bash
   git clone ...
   npm install
   ```
````

2. Configure environment

   ```bash
   cp .env.example .env
   # edit .env with your local values — see .env.example for descriptions
   ```

3. Start services

   ```bash
   docker compose up -d
   ```

4. Run migrations and seed

   ```bash
   npm run db:migrate
   npm run db:seed
   ```

5. Start the app

   ```bash
   npm run dev
   ```

6. Verify
   ```bash
   npm test
   ```

````

Rules:
- every command in the guide must actually work when run in sequence
- state the correct runtime version explicitly
- link to environment setup instructions (nvm, asdf, pyenv, etc.) for each required tool
- do not add commands that require context not yet established in the guide
- note anything that differs between macOS, Linux, and Windows if relevant

---

## Step 7 — Validate the updated guide

After updating the documentation, review each step:
- do the commands work in the stated order?
- are all required environment variables in `.env.example`?
- does `npm test` (or equivalent) pass after following the guide?

---

## Step 8 — Report

```text
Getting started audit

Entry point
<file and current state>

Gaps found
- <gap description and severity>
- ...

Updates made
- <what was changed in which file>
- ...

Still requires manual action
- <anything that cannot be automated or documented without more information>

Validation
Following the guide produces a working local environment: yes | no | partial
Tests pass after setup: yes | no | unknown
````
