---
name: singular-detect
description: Detect a project's tech stack — languages, frameworks, databases, cloud and tooling — and compare it with installed singularskills skills to recommend skills to find, adapt or create. Use when the user asks which skills would help with their stack, or what skills are missing for the codebase they are working in.
---

# Detect

Scan the current project and identify its tech stack, frameworks, tools, and databases. Compare against installed singularskills skills and suggest what's missing.

## Prerequisites

None — run anytime in any project.

## Process

1. **Scan for tech stack signals:**
   - Read project root for config files:
     - `package.json` → Node.js (check for Next.js, React, Vue, Angular, Express, etc.)
     - `pubspec.yaml` → Flutter/Dart
     - `Cargo.toml` → Rust
     - `go.mod` → Go
     - `requirements.txt` / `pyproject.toml` → Python (check for Django, Flask, FastAPI, etc.)
     - `Gemfile` → Ruby (check for Rails, Sinatra, etc.)
     - `Dockerfile` / `docker-compose.yml` → Docker
     - `terraform/` / `*.tf` → Terraform
     - `.github/workflows/` → GitHub Actions
     - `tsconfig.json` → TypeScript
     - `biome.json` / `.eslintrc` → Linting tools
     - `vitest.config` / `jest.config` → Testing frameworks
   - Check for databases: Prisma, Drizzle, SQLAlchemy, ActiveRecord, etc.
   - Check for cloud providers: AWS (CDK, SAM), GCP, Azure, Vercel, Netlify
   - Say whether a shipped stack profile matches, in one line: `matches profile: bun-react-ts` when `package.json` has `packageManager` starting with `bun@` and both `next` and `react` among its dependencies; `matches profile: rust-gpui` when a Cargo workspace member depends on `gpui`; else `matches profile: none` (the profiles are the stack files in the pack's references folder; `singular-init` writes the Stack section)

2. **Inventory existing skills:**
   - Check the agent's skills folder for installed skills: `.agents/skills/` (Codex, OpenCode, Cursor, GitHub Copilot, Gemini CLI and others) or `.claude/skills/` (Claude Code), in the project and in the user's home directory; the pack's skills are the `<domain>-<skill>` folders there
   - Note any other folders there as custom skills
   - List what's already available

3. **Identify skill gaps:**
   - Based on detected tech, suggest skills that would be useful
   - Examples: Flutter project → "Dart best practices", "Widget testing", "State management patterns"
   - Categorize as: available in marketplace, can be adapted, needs to be created

4. **Write the artifact** to `.singularskills/detect.md` with sections:
   - **Tech Stack** — languages, frameworks, databases, tools detected
   - **Installed Skills** — what singularskills skills are already available
   - **Recommended Skills** — what's missing, organized by: find, adapt, or create
   - **Suggested Next Steps** — specific commands to run

## Output

The detection report written to `.singularskills/detect.md`. Present a summary to the user highlighting:
- Tech stack identified
- Top 3-5 skill recommendations
- Suggested `/singular-find-skill` or `/singular-create-skill` commands to run
