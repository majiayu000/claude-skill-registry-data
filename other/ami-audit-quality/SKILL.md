---
name: ami-audit-quality
description: Performs a deep code quality, security, data schema consistency, and structure audit on modified files using both test execution and code inspection.
allowed-tools: Bash, Read, Grep, Edit, Write
---

# Skill: Push Quality Auditor

When invoked, act as a strict Code Reviewer focused on code verification by execution, security, data schema consistency, structural integrity, and linguistic consistency.

Everything else reviews by reading; this skill begins by reviewing through execution.

## Workflow

### 1. Scope and Execution Verification (Run What the Repo Declares)

Before reading code heuristically, verify whether the repository's own tooling passes on the modified changes:

1. **Discover Declared Tooling:**
   Inspect the repository's configuration manifests for declared verification commands:
   - `package.json` (`scripts`: `typecheck`, `lint`, `format:check`, `test`)
   - `pyproject.toml` or `setup.cfg` (`[tool.mypy]`, `[tool.ruff]`, `[tool.pytest]`)
   - `Makefile` (`check`, `lint`, `test`)
   - `Cargo.toml` (`cargo check`, `cargo test`, `cargo clippy`)
   - `.pre-commit-config.yaml`
   *Rule:* Run only what the repository declares. Do not invent or globally install unconfigured linters. Prefer local project binaries (`node_modules/.bin/`, `.venv/Scripts/`).

2. **Run in Increasing Order of Cost:**
   - **Type-Check / Compile:** The cheapest non-gameable signal.
   - **Lint / Format Check:** Run in check mode only (do not auto-format mid-verification).
   - **Test Suite:** Run the tests covering modified components. Note whether failures pre-existed on the base commit before reporting them.
   - **Mechanical Dead Code / Duplication:** Run available static analyzers (`ts-prune`, `vulture`, `jscpd`) if declared.

3. **Execution Signal Requirements:**
   - Every detected failure MUST provide the exact one-line command to reproduce it.
   - **Mandatory `gaps:` line:** Any check that could not run (tool missing, test suite skipped) MUST be explicitly listed as a gap. A check that did not run is never a silent pass.

### 2. Static Security & Structural Quality Check

Inspect the code diffs (`git diff` or changed files) across core dimensions:

1. **Security & Hygiene:**
   - Ensure there are no exposed credentials, API keys, private tokens, or dangerous raw shell executions.
   - Guarantee exception handlers and diagnostic loggers do not log sensitive data (PII, authorization tokens).
   - Ensure no local machine absolute paths (e.g., user home directory paths) leak into committed files.

2. **Failure Path Resilience & State Safety:**
   - **State Cleanup & Rollback:** Verify that failures mid-execution (timeouts, thrown exceptions, network drops) trigger proper cleanup to avoid corrupted state.
   - **Retry Idempotency:** Ensure operations subjected to retries do not produce duplicated side effects or inconsistent state.

3. **Duplication & Dead Code:**
   - Verify that new code does not duplicate existing utilities or domain helpers. Enforce centralizing reusable logic.

4. **Data Schema, ORM & Migration Consistency (When Data Models Are Modified):**
   - If the diff modifies database schemas, ORM models, raw SQL queries, or serialized API payloads, verify that all referencing queries, connections, and callers structurally match the updated definitions.
   - **Temporal Compatibility & Two-Phase Migrations:** Confirm that renamed or dropped fields do not break in-flight/cached payloads, enforce validation at entry boundaries (no de-facto gating), and check whether destructive schema changes require a dual read/write migration phase.

5. **Agentic AI & Declarative Code Integrity (.md / .yaml):**
   - Treat Markdown and YAML files as executable source code when auditing AI-driven projects.
   - **Structural Debt:** Scan for duplicated instructions or contradictory rules across related files.
   - **DRY Principle:** Procedural steps belong in skills, while agent profiles contain high-level roles and constraints.
   - **Token Efficiency & Bloat:** Ensure prompt instructions are concise and skimmable.

6. **UI & Design System Consistency (When Interface Files Are Modified):**
   - If the diff touches UI files (`.tsx`, `.jsx`, `.xaml`, `.vue`, `.svelte`, `.html`, `.dart`), adhere to `skills/ami-audit-ui-consistency/SKILL.md`.
   - **Zero Raw Hex in New Code:** Reject unconfigured hexadecimal or RGB colors outside theme files.
   - **Component & Asset Hygiene:** Enforce max 1 primary CTA button per view, standard interactive states (`hover`, `focus-visible`, `disabled`), single icon family, zero duplicate glyphs for the same action, and accessible labels on icon buttons.

### 3. Adversarial Verification Gate (Fresh-Context Review)

For changes touching critical domain logic, algorithms, or API boundaries, conduct or invoke an adversarial check (`ami-adversarial-verifier`):
- Evaluate the change strictly against the stated requirement and its existing callers, ignoring self-justifications.
- Verify boundary conditions: empty inputs, null values, concurrent executions, and caller compatibility.
- Ensure the change does not introduce behavioral regressions in existing interfaces.

### 4. Linguistic & Comment Consistency

1. **Comments & Docstrings:**
   - Ensure comments explain *why* something is done, not *what*. Avoid commenting obvious lines.
   - Actively audit docstrings for conciseness; avoid narrative bloat.
2. **Zero Internal Planning References:**
   - Comments and docstrings MUST NEVER reference internal phases, stages, steps, or design options (e.g., 'Phase 1', 'Stage 2', 'Etapa 3', 'Option A', 'Opción B').
   - All code documentation must describe technical rationale, domain invariants, and contracts from a permanent domain perspective.
3. **Language Consistency:**
   - Source code, docstrings, and inline comments must strictly be in English.

### 5. Reporting

Emit a structured verdict:

- **If failures or defects are found:** Reject the check. Provide:
  - Exact command to reproduce execution failures.
  - Line numbers and triggers for code or security defects.
  - Concrete remediations required.
  - Await explicit user approval before applying any fixes.
- **If all checks pass:** Emit the clean verdict including executed checks and reported `gaps:`, then terminate the skill.

---
**Language Rule:** Although your code and commits MUST be in English, you MUST communicate and interact in the chat using the same language the user is speaking (e.g., Spanish, French, etc.).
