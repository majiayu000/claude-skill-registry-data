---
name: onboard
description: Onboard to a new codebase with structured exploration. Scans the project, generates an architecture map with Mermaid diagrams, identifies entry points, explains the tech stack, lists key patterns and conventions, and produces a "start here" guide. Use when user says "onboard", "new project", "understand this codebase", "what does this project do", "walk me through the project", "project overview", or joins a new team or repository. For explaining a single file, use /explain; for code review, use /review; for assessment, use /assessment.
argument-hint: "/onboard | /onboard <path> --verify | /onboard <path> --trust"
allowed-tools: "Read, Grep, Glob, Bash, AskUserQuestion, Skill"
---

## Overview

Structured codebase exploration that produces a navigable architecture overview and a "Start Here" guide. Designed for the first hour on a new project.

## When to Use

- First session in a repository nobody on the current task has worked in.
- Joining a team, or picking up a take-home, an external repository, or untrusted source that needs the Phase 0 trust scan before anything else runs.
- Refreshing a mental model of a project whose structure moved since it was last read.
- For one file or function, use `/explain`; for a quality score, use `/assessment`; for a single diff, use `/review`.

## Arguments

- No arguments: onboard the current working directory. Phase 0 prompts before running the trust scan.
- `<path>`: onboard the specified path as the project root.
- `--trust`: I trust this project. Skip the trust scan and the prompt. Recorded in the final Start Here guide as a deliberate skip.
- `--verify`: I do not trust this project. Run the trust scan without prompting. Useful for take-homes, external repos, and untrusted source.
- Passing both `--trust` and `--verify` together is a conflict. Reject with an error.

## Process

### Phase 0: Trust decision (asked first)

Before any other action, ask the user whether to trust the project. The trust scan is opt-in per invocation.

**Decision flow:**

| Invocation | Behavior |
|------------|----------|
| `/onboard <path>` with no flag | AskUserQuestion fires. Two options below. Default focus is "No, scan it first" |
| `/onboard <path> --trust` | Skip the prompt. Skip the scan. Continue to Step 1. The Start Here guide records `Safety verdict: SKIPPED (--trust)` |
| `/onboard <path> --verify` | Skip the prompt. Run the scan. Continue per the verdict-to-action table below |
| `/onboard <path> --trust --verify` | Reject with error: conflicting flags |

**Prompt wording:**

> Do you trust this project? Picking "No, scan it first" runs a read-only scan for install-time hooks, credential-theft patterns, and known supply-chain attack signatures. Takes under 30 seconds on most projects.

Options:

| Option | Effect |
|--------|--------|
| Yes, trust it (skip scan) | Skip scan. Continue to Step 1. Start Here guide records `Safety verdict: SKIPPED (user trusts project)` |
| No, scan it first (default focus, Recommended for new or external projects) | Call the Skill tool with `audit` and the arguments `trust --json` against the project root. Apply the verdict mapping below |

**When the scan runs**, map the verdict to action:

| Verdict | `/onboard` action |
|---------|-------------------|
| SAFE | Continue to Step 1 silently. Note the verdict in the final Start Here guide |
| SUSPICIOUS | Present the findings to the user. Ask "Continue with onboarding?" with default no. If yes, proceed to Step 1. If no, abort |
| HIGH-RISK | Block. Present the findings. Require the user to type the literal phrase `I accept the risk` before continuing |
| MALICIOUS | Block. Present the findings. Refuse to continue. Recommend running the project inside a Docker sandbox or deleting the directory. Do not proceed to Step 1 under any circumstance |

**Phase 0 constraints, apply when the scan runs:**

- Never install dependencies. Never run any command defined in the project.
- Never read `.env`, `.env.local`, or `.env.production`. Only `.env.example`.
- Never reveal actual secret values found during the scan. Show file, line, and pattern name only.
- The scan is read-only. The user's trust choice is recorded in the Start Here guide either way.

### Step 1: Detect the project

Read the manifest file to determine language, framework, and runtime version. Check in order: `package.json`, `go.mod`, `Cargo.toml`, `pyproject.toml`, `pom.xml`, `build.gradle`, `mix.exs`, `Gemfile`. Record:

- Language and version
- Framework and version
- Package manager
- Runtime constraints

### Step 2: Map directory structure

Run `ls` on the project root and each top-level directory. Classify each directory by purpose:

| Directory type | Examples |
|---------------|----------|
| Source code | `src/`, `lib/`, `app/`, `pkg/`, `internal/` |
| Tests | `test/`, [`tests/`](../../tests), `__tests__/`, `spec/` |
| Configuration | `config/`, [`.github/`](../../.github), `.husky/` |
| Build output | `dist/`, `build/`, `.next/`, `out/` |
| Documentation | [`docs/`](../../docs), `doc/` |
| Infrastructure | `infra/`, `terraform/`, `k8s/`, `docker/` |
| Database | `prisma/`, `migrations/`, `db/` |
| Scripts | [`scripts/`](../../scripts), `bin/`, [`tools/`](../../tools) |
| Static assets | `public/`, `static/`, `assets/` |

### Step 3: Identify entry points

Find the files where execution begins:

- `main` field in package.json
- Files named `main.ts`, `index.ts`, `app.ts`, `server.ts`, `main.go`, `main.rs`
- Route definitions: search for router setup, controller decorators, API route files
- CLI entry points: `bin` field in package.json, files with shebang lines
- Worker or job entry points: queue consumers, cron handlers

### Step 4: Read configuration

Read these files in parallel when they exist:

- TypeScript config: `tsconfig.json`
- Linter config: `.eslintrc*`, `biome.json`, `.prettierrc*`
- Docker: `Dockerfile`, `docker-compose.yml`
- CI: `.github/workflows/*.yml`, `.gitlab-ci.yml`, `Jenkinsfile`
- Environment: `.env.example`
- Database: `prisma/schema.prisma`, migration files

### Step 5: Generate architecture diagram

Produce a Mermaid diagram showing:

- Modules and their responsibilities
- Dependencies between modules
- External services and integrations
- Data flow direction

Use `graph TD` for layered architectures, `graph LR` for pipeline architectures. Label edges with the type of interaction: HTTP, event, import, query.

### Step 6: Identify patterns

Search the codebase for structural patterns:

| Pattern | How to detect |
|---------|--------------|
| Repository | Files named `*.repository.ts`, `*.repo.go`, data access abstractions |
| Service layer | Files named `*.service.ts`, `*.svc.go`, business logic classes |
| Controller | Files named `*.controller.ts`, route handlers |
| Middleware | Files in `middleware/` directories, request interceptors |
| Event handlers | Files subscribing to events, queue consumers |
| State machines | Enum-based state transitions, status fields with defined flows |
| DTOs | Files named `*.dto.ts`, input/output shapes at boundaries |
| Guards/interceptors | Auth guards, validation interceptors, logging interceptors |

### Step 7: Read existing documentation

Read in parallel: [`README.md`](../../README.md), `CONTRIBUTING.md`, `ARCHITECTURE.md`, [`docs/`](../../docs) directory contents, [`CLAUDE.md`](../../CLAUDE.md). Note what is documented and what is missing.

### Step 8: Detect conventions

Identify the project's conventions by sampling 5-10 source files:

- Naming: camelCase vs snake_case, file naming patterns
- File structure: one export per file, barrel files, feature-based vs layer-based
- Test patterns: co-located tests vs separate test directory, naming convention
- Import style: relative vs absolute, path aliases
- Error handling: exceptions vs Result types, error classes

### Step 9: Output the Start Here guide

Produce a structured guide with these sections:

1. **What This Project Does**: one paragraph summary of the project's purpose
2. **Tech Stack**: language, framework, database, key dependencies
3. **Architecture**: the Mermaid diagram from Step 5 with a brief explanation
4. **Key Patterns**: list each pattern found in Step 6 with an example file
5. **How to Run**: commands to install, configure, and start the project
6. **How to Test**: test commands, test database setup, coverage commands
7. **Where to Start Reading**: the 3-5 most important files to read first, ordered
8. **Conventions to Follow**: the conventions detected in Step 8

### Step 10: Suggest next steps

Recommend running `/retro discover` to capture the detected conventions as durable rules in the project's configuration.

## Rules

- Phase 0 prompts the user before any scan runs. The default option in the prompt is "No, scan it first", aligned with the protective intent for unknown projects.
- The user can pre-decide non-interactively with `--trust`, skip scan or `--verify`, run scan. Passing both is a conflict.
- When the scan runs and returns HIGH-RISK or MALICIOUS, abort onboarding even if the user pressures to continue. The HIGH-RISK override path requires the explicit phrase. MALICIOUS has no override.
- Never modify any project files during onboarding. This is a read-only exploration.
- Do not install dependencies or run build commands unless the user asks.
- When documentation is incomplete or contradicts the code, trust the code.
- Flag discrepancies between docs and code as findings.
- Keep the Start Here guide under 200 lines. Link to files instead of inlining code.
- The Start Here guide must include a "Safety verdict" line near the top, summarizing the trust decision and the scan result if applicable.

## Common Rationalizations

- "The repository comes from a well-known organization, the trust question is noise": Phase 0 asks on every run without a flag, and the default focus is the scan.
- "An install would let me read the generated types": onboarding installs nothing and runs no project command unless the user asks.
- "The README says the service uses X, so it does": when the docs and the code disagree, the code wins, and the mismatch becomes a finding.
- "Inlining the key functions saves the reader a click": the guide links to files and stays under 200 lines.
- "The user insists, so the MALICIOUS verdict can be waived": MALICIOUS has no override, and HIGH-RISK continues only on the literal phrase `I accept the risk`.

## Red Flags

- Stop and ask the trust question when no flag was passed and no other step has run.
- Stop and reject the invocation when both `--trust` and `--verify` were passed.
- Stop and wait for the literal phrase `I accept the risk` when the scan returns HIGH-RISK.
- Stop onboarding and recommend a Docker sandbox or deleting the directory when the scan returns MALICIOUS.
- Stop and read `.env.example` instead when the next read targets `.env`, `.env.local`, or `.env.production`.

## Verification

- The Start Here guide carries a `Safety verdict` line near the top that matches the Phase 0 outcome.
- The guide has all eight sections from Step 9 and stays under 200 lines.
- Every file named under Where to Start Reading exists on disk.
- The Mermaid diagram labels every edge with its interaction type.
- `git status` shows no project file modified by the onboarding run.
- Every mismatch found between the docs and the code is listed as a finding.

## Related skills

- `/audit trust` -- Untrusted-project safety scan. Runs automatically as Phase 0. Can also be invoked standalone before adding a new dependency or considering a third-party project.
- `/explain` -- Deep explanation of a specific file or function.
- `/assessment` -- Full quality assessment of the codebase.
- `/retro discover` -- Capture conventions as rules.
- `/review` -- Review specific code changes.
