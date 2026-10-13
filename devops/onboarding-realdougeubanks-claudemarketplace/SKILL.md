---
name: onboarding
description: "Generates a comprehensive developer onboarding guide (ONBOARDING.md) by reading the codebase: directory map, entry points, environment variables, key commands, and architecture overview."
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Onboarding

Generate a comprehensive developer onboarding guide for an unfamiliar codebase and write it to `docs/ONBOARDING.md`.

## Instructions

1. Use Read on `README.md`, then attempt to read whichever of the following exist: `package.json`, `pyproject.toml`, `go.mod`, `CLAUDE.md`, `docs/assumptions.md`.

2. Use Glob to map the top-level directory structure (`*`). For each top-level folder found, describe its purpose based on its name and contents (e.g., `src/` → application source, `scripts/` → automation scripts, `docs/` → project documentation).

3. Use Glob to find entry points matching: `index.*`, `main.*`, `server.*`, `app.*`, `cmd/**/*`. Read the primary entry point to understand how the application starts.

4. Use Read on any Makefile, `package.json` (scripts section), or `Taskfile.yml` to identify key commands: install, run, test, build, lint.

5. Use Glob to find `.env.example` or any env var documentation files. List all required environment variables with their descriptions.

   > **SECURITY:** Read `.env.example` only — never read `.env` or any file containing real credential values, and never include actual secret values in the generated guide. Document variable names and descriptions only.

6. Use Bash to count files by detected language type. Adapt the command to the language detected:
   - TypeScript/JavaScript: `find . -name "*.ts" -o -name "*.js" | grep -v node_modules | wc -l`
   - Python: `find . -name "*.py" | grep -v __pycache__ | wc -l`
   - Go: `find . -name "*.go" | wc -l`

7. **Generate architecture diagram.**

   a. Use Read on the primary entry point file identified in step 3 to understand how the application initializes and what it connects to.

   b. Use Glob to find configuration files that reveal infrastructure: `docker-compose.yml`, `*.env.example`, `infrastructure/**`, `terraform/**`, `serverless.yml`, `.github/workflows/**`.

   c. Use Grep to identify major inter-module dependencies: import/require/use statements at the top of the entry point and primary route/handler files.

   d. Generate a Mermaid diagram using the most appropriate type:
      - For web apps with a request flow: `sequenceDiagram` showing Client → Load Balancer → App Server → Database/Cache/Queue
      - For microservices or modular apps: `graph LR` showing service dependencies
      - For simple single-module apps: `graph TD` showing function/module call flow

   e. Include the diagram in the generated `docs/ONBOARDING.md` under a "## Architecture" section, wrapped in a fenced code block with `mermaid` syntax tag.

   f. Add a note: "This diagram was auto-generated and may not capture all relationships. Review and update as the architecture evolves."

   Example output to include in ONBOARDING.md:

   ````markdown
   ## Architecture

   ```mermaid
   sequenceDiagram
       Client->>+ALB: HTTPS Request
       ALB->>+AppServer: Forward
       AppServer->>+PostgreSQL: Query
       PostgreSQL-->>-AppServer: Result
       AppServer->>+Redis: Cache write
       AppServer-->>-ALB: Response
       ALB-->>-Client: HTTPS Response
   ```

   > This diagram was auto-generated and may not capture all relationships. Review and update as the architecture evolves.
   ````

8. Use Glob to check for `docs/agentRoster.md`. If it exists, read it and include the agent roster section in the guide.

9. Write the completed onboarding guide to `docs/ONBOARDING.md` using Write, following the output structure below.

## Output Structure

Write the following document to `docs/ONBOARDING.md`:

```markdown
# Developer Onboarding Guide — <Project Name>

## What This Project Does
<1-2 sentence summary from README>

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Language | ... |
| Framework | ... |
| Database | ... |
| CI/CD | ... |

## Directory Map
| Path | Purpose |
|------|---------|
| `src/` | ... |

## Getting Started
```bash
# 1. Install dependencies
npm install

# 2. Configure environment
cp .env.example .env
# Edit .env: fill in ...

# 3. Run locally
npm run dev
```

## Key Entry Points
- `src/index.ts:1` — Application bootstrap
- `src/routes/` — API route definitions

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| DATABASE_URL | Yes | PostgreSQL connection string |

## Key Commands

| Command | What it does |
|---------|-------------|
| `npm run dev` | Start dev server with hot reload |
| `npm test` | Run test suite |

## Architecture Overview
<brief description of the main data/request flow>

## Agent Roster
<include only if docs/agentRoster.md exists>

## How to Contribute
<derive from the target project's own conventions — see note below>
```

For the "How to Contribute" section: read the target project's `CONTRIBUTING.md`, `CLAUDE.md`, or `.github/PULL_REQUEST_TEMPLATE.md` and summarize *that project's* branching, review, and merge rules. Do not assume any particular branch-prefix or approval policy. If no convention docs exist, fall back to generic guidance: "Create a branch, open a PR, and request review — confirm the team's specific conventions with a maintainer."

After writing the file, confirm to the user that `docs/ONBOARDING.md` has been created and summarize the key sections included.
