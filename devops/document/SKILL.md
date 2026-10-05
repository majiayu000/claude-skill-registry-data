---
name: document
description: "Audit your project's documentation health and identify gaps. Scans for README, changelog, API docs, ADRs, runbooks, onboarding guides, and diagrams. Triggers: you need a documentation audit, want to check doc coverage, find missing documentation, or assess documentation quality."
version: "2.0.1"
category: docs
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Analyze the project's
documentation landscape and produce a comprehensive health report.

INPUT:
$ARGUMENTS

If no arguments provided, perform a full documentation audit of the current project.
If a specific doc type is mentioned (e.g., "api", "adr", "runbook"), focus the audit
on that area and route to the appropriate sub-skill.

============================================================
PHASE 1: AUTO-DETECT PROJECT CONTEXT
============================================================

Detect the project's tech stack and maturity level:

Step 1.1 -- Tech Stack Detection

Scan for config files to determine the stack:
- package.json, tsconfig.json (Node.js / TypeScript)
- pubspec.yaml (Flutter / Dart)
- Cargo.toml (Rust)
- go.mod (Go)
- pyproject.toml, requirements.txt, setup.py (Python)
- Gemfile (Ruby)
- pom.xml, build.gradle (Java / Kotlin)
- docker-compose.yml, Dockerfile (containerized)
- .github/workflows/ (CI/CD)

Step 1.2 -- Maturity Assessment

Classify the project into a maturity tier:

| Tier | Criteria |
|------|----------|
| Greenfield | < 20 commits, no tests, no CI |
| Active Development | 20-200 commits, some tests, basic CI |
| Mature | 200+ commits, test suite, CI/CD, deployments |
| Production | All of Mature + monitoring, runbooks, on-call |

Record the tier -- it determines which docs are expected.

============================================================
PHASE 2: DOCUMENTATION INVENTORY
============================================================

Scan the project for existing documentation artifacts:

Step 2.1 -- Core Docs

Check for each of these files/directories and record status (present/missing/stale):

| Document | Paths to Check |
|----------|---------------|
| README | README.md, README, readme.md |
| Changelog | CHANGELOG.md, CHANGES.md, HISTORY.md |
| Contributing | CONTRIBUTING.md, docs/contributing.md |
| License | LICENSE, LICENSE.md, COPYING |
| Code of Conduct | CODE_OF_CONDUCT.md |

Step 2.2 -- API Documentation

Check for:
- OpenAPI/Swagger specs: openapi.yaml, openapi.json, swagger.yaml, swagger.json
- docs/api/, api-docs/ directories
- Inline API doc comments (JSDoc @route, Python docstrings with endpoint info)
- GraphQL schema files: schema.graphql, *.graphqls
- Postman collections: *.postman_collection.json

Step 2.3 -- Architecture Docs

Check for:
- docs/adr/, adr/, decisions/ directories
- Architecture diagrams: docs/diagrams/, docs/architecture/
- Mermaid files: *.mmd, *.mermaid
- Draw.io files: *.drawio
- C4 model files

Step 2.4 -- Operations Docs

Check for:
- Runbooks: docs/runbook/, runbook/, playbooks/
- Deployment docs: docs/deployment/, DEPLOYMENT.md
- Incident response: docs/incidents/, INCIDENT.md
- Monitoring: docs/monitoring/, alerts/

Step 2.5 -- Onboarding Docs

Check for:
- CONTRIBUTING.md, docs/onboarding.md, docs/getting-started.md
- .env.example, .env.template (environment setup docs)
- Makefile, scripts/ (developer workflow tooling)
- docs/development.md, DEVELOPMENT.md

============================================================
PHASE 3: GAP ANALYSIS
============================================================

Score each documentation area based on project maturity tier:

SCORING MATRIX:

| Document Type | Greenfield | Active Dev | Mature | Production |
|--------------|-----------|-----------|--------|-----------|
| README | Required | Required | Required | Required |
| Changelog | Optional | Recommended | Required | Required |
| API Docs | Optional | Recommended | Required | Required |
| ADRs | Optional | Optional | Recommended | Required |
| Runbook | N/A | Optional | Recommended | Required |
| Onboarding | Optional | Recommended | Required | Required |
| Diagrams | Optional | Optional | Recommended | Required |
| License | Required | Required | Required | Required |

For each doc type, assign a status:
- PASS: Document exists and appears current (modified within last 30 days or content matches code)
- STALE: Document exists but may be outdated (last modified 90+ days ago)
- MISSING: Document does not exist but is Required/Recommended for this tier
- N/A: Not expected for this maturity tier

Calculate coverage score: (PASS count / Required+Recommended count) * 100

============================================================
PHASE 4: ROUTE TO SUB-SKILLS
============================================================

Based on identified gaps, recommend specific sub-skills to run:

| Gap | Sub-Skill | Command |
|-----|-----------|---------|
| Missing/stale README | /readme | Generate comprehensive README |
| Missing API docs | /api-docs | Auto-generate OpenAPI spec |
| Missing changelog | /changelog | Generate from git history |
| Missing ADRs | /adr | Create ADR directory + retrospective ADRs |
| Missing runbook | /runbook | Generate operations runbook |
| Missing onboarding | /onboarding | Generate developer onboarding guide |
| Missing diagrams | /diagram | Generate architecture diagrams |

If $ARGUMENTS specifies a particular doc type, execute that sub-skill's work
inline rather than just recommending it.

============================================================
PHASE 5: DOCUMENTATION HEALTH REPORT
============================================================

OUTPUT:

## Documentation Health Report

### Project Context
- **Project:** [name from config]
- **Tech Stack:** [detected stack]
- **Maturity Tier:** [tier]
- **Total Commits:** [count]

### Coverage Score: [X]%

### Documentation Inventory

| Document | Status | Path | Last Updated | Notes |
|----------|--------|------|-------------|-------|
| README | PASS/STALE/MISSING | path or -- | date or -- | details |
| Changelog | ... | ... | ... | ... |
| API Docs | ... | ... | ... | ... |
| ADRs | ... | ... | ... | ... |
| Runbook | ... | ... | ... | ... |
| Onboarding | ... | ... | ... | ... |
| Diagrams | ... | ... | ... | ... |
| License | ... | ... | ... | ... |

### Priority Actions

Ordered list of documentation gaps to address, highest priority first:

1. **[MISSING/STALE] [Doc Type]** -- [Why it matters for this project]
   Run: `/[sub-skill]`
2. ...

### Documentation Quality Notes

- [Any observations about existing doc quality, consistency, accuracy]
- [Suggestions for improving existing docs that are present but weak]


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
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /document — {{YYYY-MM-DD}}
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

- Do NOT create or modify any documentation files in this orchestrator skill.
  Only audit and report. Sub-skills handle the actual generation.
- Do NOT guess about project features. Only report what you can verify.
- Do NOT count auto-generated files (lock files, build output) as documentation.
- Do NOT recommend docs that are genuinely unnecessary for the project type
  (e.g., runbooks for a CLI tool with no deployment).

NEXT STEPS:

After reviewing the health report:
- "Run `/api-docs` to generate OpenAPI documentation for your API."
- "Run `/changelog` to generate a changelog from git history."
- "Run `/adr retrospective` to create ADRs from existing codebase decisions."
- "Run `/runbook` to generate an operations runbook."
- "Run `/onboarding` to generate a developer onboarding guide."
- "Run `/diagram` to generate architecture diagrams."
