---
name: onboarding
description: "Generate a comprehensive developer onboarding guide from your codebase. Triggers: you need a getting started guide, developer setup docs, CONTRIBUTING."
version: "2.0.1"
category: docs
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Analyze the project
codebase and produce a comprehensive developer onboarding guide.

INPUT:
$ARGUMENTS

Accepted arguments:
- No arguments: generate a complete onboarding guide.
- `contributing`: focus on generating/updating CONTRIBUTING.md only.
- `setup`: focus on environment setup instructions only.
- `architecture`: focus on architecture overview only.

============================================================
PHASE 1: CODEBASE ANALYSIS
============================================================

Step 1.1 -- Tech Stack Detection

Scan for config files to determine: primary language and version, framework,
package manager (npm/yarn/pnpm/pip/poetry/cargo/go/bundler), runtime requirements,
database (from config, ORM, or docker-compose), and key dependencies a new
developer must understand.

Step 1.2 -- Project Structure Analysis

Map the directory structure (top-level + one level into src/lib/app dirs).
Identify the architectural pattern (MVC, Clean, Hexagonal, Layered, Feature-based).
Identify entry points and configuration files.

Step 1.3 -- Build and Run Commands

Extract from config files and scripts: install, build, dev, test (unit/integration/e2e),
lint/format, database migration, and any custom scripts (Makefile, package.json scripts).

Step 1.4 -- Environment Setup Requirements

Detect: .env.example variables, docker-compose service dependencies, required
external tools (Docker, cloud SDKs, platform SDKs), and pre-commit hooks
(.husky/, .pre-commit-config.yaml).

Step 1.5 -- Code Conventions

Detect from config: linter (.eslintrc, .pylintrc, golangci-lint), formatter
(.prettierrc, black, rustfmt), TypeScript strictness, .editorconfig, import
ordering rules, and naming conventions inferred from code patterns.

Step 1.6 -- Git and PR Workflow

Detect: branch naming patterns, PR templates, issue templates, commit message
conventions, CI checks on PRs, and CODEOWNERS.

Step 1.7 -- Key Architectural Patterns

Read 3-5 representative source files to identify: dependency injection, error
handling, logging, auth patterns, API response format, database access patterns,
and testing patterns (naming, fixtures, mocks).

============================================================
PHASE 2: GUIDE GENERATION
============================================================

Generate the onboarding guide with these sections. Output to `docs/onboarding.md`
for comprehensive guide, and optionally `CONTRIBUTING.md` in root if it does not exist.

Required sections:

1. **Prerequisites** -- Table of required tools with versions and install instructions.

2. **Environment Setup** -- Step-by-step: clone, install deps, copy .env.example,
   configure required variables (table with variable, description, how to obtain),
   set up database, verify setup works.

3. **Running Locally** -- Dev server command and URL, Docker alternative if applicable,
   table of common development commands (start, test, lint, build).

4. **Running Tests** -- How to run full suite, single test, with verbose output.
   Test file naming convention and organization.

5. **Project Architecture** -- 2-3 sentence overview, directory tree with one-line
   descriptions, data flow explanation, key patterns with example file references.

6. **Coding Conventions** -- Style rules from linter/formatter config, naming conventions,
   import ordering, where to put new features/tests/endpoints.

7. **Git Workflow** -- Branch naming pattern, commit message convention with repo examples,
   PR process (create, CI checks, review requirements, merge strategy).

8. **Common Tasks** -- Step-by-step recipes for: adding a new API endpoint, adding a new
   database model, adding a new UI screen (adapt to project type).

9. **Troubleshooting** -- Tables of common setup and runtime problems with solutions.

If CONTRIBUTING.md does not exist, write a concise version to project root covering:
fork, branch, make changes, run tests, submit PR. Link to full onboarding guide.

If CONTRIBUTING.md already exists, read it first and merge new content.

============================================================
PHASE 3: VALIDATE AND WRITE
============================================================

For each command in the guide:
- Confirm it matches the project's actual config
- Confirm file paths reference actual files
- Confirm version numbers match config files

Write files:
- `docs/onboarding.md` -- Comprehensive developer onboarding guide
- `CONTRIBUTING.md` -- Concise contribution guidelines (if created)


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing documentation, validate completeness:

1. Verify all required sections are present and non-empty.
2. Verify internal cross-references and links resolve correctly.
3. Verify no placeholder text remains ("{TODO}", "[TBD]", "...", "etc.").
4. Verify code examples are syntactically valid.

IF VALIDATION FAILS:
- Identify which sections are incomplete or contain placeholders
- Re-generate only the deficient sections
- Repeat up to 2 iterations

============================================================
OUTPUT
============================================================

## Onboarding Guide Generated

### Project Profile
- **Language:** [language + version]
- **Framework:** [framework + version]
- **Database:** [database or "none"]
- **Package Manager:** [manager]
- **Test Framework:** [framework]

### Files Written
- `docs/onboarding.md` -- Comprehensive developer onboarding guide
- `CONTRIBUTING.md` -- Concise contribution guidelines (if created)

### Sections Included
- [ ] Prerequisites
- [ ] Environment setup
- [ ] Running locally
- [ ] Running tests
- [ ] Architecture overview
- [ ] Coding conventions
- [ ] Git workflow
- [ ] Common tasks
- [ ] Troubleshooting


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /onboarding — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT fabricate setup steps. Every command must come from actual config files.
- Do NOT include internal team info (Slack channels, emails) unless found in existing docs.
- Do NOT include passwords, API keys, or secrets -- reference .env.example instead.
- Do NOT write a generic guide. Every section must be specific to this project.
- Do NOT duplicate content from README.md -- link to it instead.
- Do NOT overwrite an existing CONTRIBUTING.md without reading it first.

NEXT STEPS:

After generating the onboarding guide:
- "Run `/document` to check overall documentation health."
- "Run `/readme` to ensure the README links to the onboarding guide."
- "Run `/diagram` to generate architecture diagrams for the guide."
