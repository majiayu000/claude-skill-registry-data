---
name: ami-discover-automations
description: Scans repositories for existing automations (CI/CD, scripts, domain jobs) and discovers high-ROI automation opportunities from manual friction.
allowed-tools: Bash, Read, Grep, Write
---

# Skill: Discover Automations

When invoked, act as an **Automation & Workflow Architect**.

## Scope & Target Domains

This skill operates in **Dual Mode** across three architectural automation domains:
1. **CI/CD & GitOps:** Workflows (`.github/workflows/`, GitLab CI, Azure Pipelines), git hooks (`.husky/`, `.pre-commit-config.yaml`, native hooks), release scripts, and automated dependency updaters (Dependabot, Renovate).
2. **Development, Build & Maintenance Scripts:** Manifest scripts (`package.json`, `pyproject.toml`, `Cargo.toml`), task runners (`Makefile`, `justfile`, `Taskfile`), and shell/PowerShell maintenance scripts (`scripts/`).
3. **Domain & Code Automations:** Application cronjobs, queues and background workers (BullMQ, Celery, Sidekiq, Daemons), and automated database lifecycles (migrations, seeds, schema validation).

---

## Workflow

### 1. Step 0 - Anti-Duplication & Context Ingestion
- Read `README.md` and repository architecture documentation (`docs/`) to understand the tech stack, deployment targets, and operational context.
- Check if an automation inventory already exists in `docs/automations.md` or prior audits. If up to date, use it as a baseline instead of redundant scanning.
- If documentation is missing or ambiguous, ask the user for brief clarification on the project's runtime stack.

### 2. Phase 1 - Existing Automation Inventory & Health Audit
- Scan the repository structure for configured automations:
  - **CI/CD Workflows:** Inspect `.github/workflows/`, `.gitlab-ci.yml`, or equivalent pipelines. Check trigger events (`push`, `pull_request`, `schedule`), secret usage, and outdated third-party action versions.
  - **Task Runners & Package Scripts:** Inspect `package.json` (`scripts`), `Makefile`, `justfile`, `Taskfile.yml`, `scripts/`, or build configs. Identify what commands developers frequently execute.
  - **Git Lifecycle Hooks:** Inspect `.husky/`, `.githooks/`, or `.pre-commit-config.yaml` for pre-commit, pre-push, or commit-msg quality gates.
  - **Domain Workers & Scheduled Tasks:** Inspect codebase for cron expressions, background queue workers, and migration runner scripts.
- Evaluate the operational health of each discovered automation:
  - `[HEALTHY]`: Functional, well-scoped, maintained actions/commands.
  - `[NEEDS_UPDATE]`: Deprecated action versions, unpinned actions, duplicated commands, or lack of caching.
  - `[BROKEN]`: Syntax errors, dead scripts pointing to non-existent files, or missing environment secrets.

### 3. Phase 2 - Manual Toil & Opportunity Discovery
- Cross-reference documented procedures (`README.md`, `CONTRIBUTING.md`, runbooks) and commit history against discovered automations to identify repetitive manual friction:
  - **Missing CI/CD Quality Gates:** Codebase has test suites, linters, or typecheckers but lacks automated CI runs on Pull Requests.
  - **Manual Release/Packaging Friction:** Release steps described as manual compilation, version tagging, or distribution without automated workflows.
  - **Orphaned Repetitive Tasks:** Common development multi-step commands (e.g. clean build, local database reset, fixture loading) that developers run manually without an aggregated script.
  - **Missing Housekeeping:** Absence of automated dependency audits, lint fixes, or cache pruning scripts.

### 4. Phase 3 - Prioritized Classification & ROI Matrix
- Formulate the findings into two distinct tables directly in chat:
  1. **Existing Automations Inventory:**
     - Component / Path
     - Category (`CI/CD`, `Build/Dev`, `Domain/Job`)
     - Status (`[HEALTHY]`, `[NEEDS_UPDATE]`, `[BROKEN]`)
     - Key Risk / Observation
  2. **Automation Opportunities (Ranked by ROI):**
     - Proposal Title & Description
     - Target Execution (`[CI/CD]`, `[DEV_SCRIPT]`, `[GIT_HOOK]`, `[DOMAIN_JOB]`)
     - **Impact / ROI:** (`[HIGH]`, `[MEDIUM]`, `[LOW]`)
     - **Implementation Effort:** (`[EASY]`, `[MODERATE]`, `[HARD]`)
     - Concrete Actionable Snippet or Configuration Template

### 5. Phase 4 - Confirmation Gate
- **CONFIRMATION 1 - Persistence & Execution:**
  - STOP and present the complete findings to the user.
  - Ask the user whether they want to:
    1. Persist the complete inventory and opportunities report to `docs/automations.md`.
    2. Immediately proceed with implementing any of the high-ROI proposed automations.
  - Await explicit user instruction before creating or editing files.

---
**Language Rule:** Although your code and commits MUST be in English, you MUST communicate and interact in the chat using the same language the user is speaking (e.g., Spanish, French, etc.).
