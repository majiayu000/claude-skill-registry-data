---
description: Scan the project and identify tech stack, frameworks, and skill gaps
---

# Detect

Scan the current project and identify its tech stack, frameworks, tools, and databases. Compare against installed Metapowers skills and suggest what's missing.

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

2. **Inventory existing skills:**
   - Check `.metapowers/plugins/` for installed domain plugins
   - Check `.metapowers/plugins/custom/` for custom skills
   - List what's already available

3. **Identify skill gaps:**
   - Based on detected tech, suggest skills that would be useful
   - Examples: Flutter project → "Dart best practices", "Widget testing", "State management patterns"
   - Categorize as: available in marketplace, can be adapted, needs to be created

4. **Write the artifact** to `.metapowers/detect.md` with sections:
   - **Tech Stack** — languages, frameworks, databases, tools detected
   - **Installed Skills** — what Metapowers skills are already available
   - **Recommended Skills** — what's missing, organized by: find, adapt, or create
   - **Suggested Next Steps** — specific commands to run

## Output

The detection report written to `.metapowers/detect.md`. Present a summary to the user highlighting:
- Tech stack identified
- Top 3-5 skill recommendations
- Suggested `/metapowers:find-skill` or `/metapowers:create-skill` commands to run
