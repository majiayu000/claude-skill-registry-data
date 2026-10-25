---
name: ami-scan-tech-debt
description: Analyzes repository code for technical debt, including dead code, duplication, constants centralization, and architectural inconsistencies. Provides a classified report based on criticality, effort, and risk.
allowed-tools: Bash, Read, Grep, Write
---

# Skill: Tech Debt Scanner

When invoked, act as a **Tech Debt Analyst**.

## Workflow

### 1. Understand the Repository Context
- Begin by reading the `README.md` and any other available architectural or goal-oriented documentation to deeply understand the purpose and architecture of the repository.
- If the documentation is missing, insufficient, or unclear regarding the repository's goals, **STOP and ask the user** to clarify the purpose and context of the repo before proceeding with the analysis.

### 2. Scope Demarcation & Dependency Boundary
- **Code Debt Specialization:** This skill specializes strictly in source code technical debt: dead code, duplicated logic, centralization opportunities, pending intention markers (TODOs/FIXMEs), type erosion, and latent architectural contract drift.
- **Avoid Redundant Scans (Teamwork Principle):**
  - If invoked by an orchestrator agent (such as `ami-repo-auditor`), bypass dependency analysis completely, as dependency hygiene is evaluated by its dedicated parallel worker (`ami-analyze-dependencies`).
  - Only if invoked standalone by the user without prior dependency checks, you may optionally consult `__AMIGA_CODEX_SKILLS_DIR__/ami-analyze-dependencies/SKILL.md` to incorporate library findings into a unified report.

### 3. Code Quality and Architecture Audit
- Scan the codebase to identify:
  - **Dead code:** Unused variables, functions, components, or files.
  - **Duplicated code:** Similar logic or structures repeated across multiple areas.
  - **Centralization opportunities:** Hardcoded values, repeated constants, or utility functions that should be unified.
  - **Pending intentions:** Comments marked as `TODO`, `FIXME`, `HACK`, `XXX`, or similar markers indicating unfinished work, workarounds, or deferred functionality.
  - **Latent Architectural Debt & Contract Erosion:**
    - **Type Erosion & Permissive Contracts:** Overuse of generic/permissive types (`any`, un-schematized dicts/objects) or missing contract boundaries.
    - **De-facto vs. Enforced Gating:** Components relying on caller assumptions rather than self-enforced guards.
    - **Silenced Patches & Swallowed Exceptions:** Exception blocks that swallow errors silently or return empty fallbacks to mask underlying integration failures.
  - **Other technical debt:** Code smells, bad practices, overly complex functions, or architectural antipatterns.

### 4. Classify and Report Findings
- If no technical debt is found during your audit, you MUST simply output **"NO TECH DEBT FOUND"**. Do not list anything, and do not proceed to step 5.
- If technical debt is found, compile all findings into a structured report grouped by categories (e.g., Dependencies, Dead Code, Duplicated Code, Centralization Opportunities, Pending Intentions, and Other Technical Debt).
- Within each category, sort the findings by **Criticality** (from highest/most urgent to lowest).
- For EACH finding, you MUST explicitly classify it across these three dimensions:
  - **Criticality:** (e.g., `[HIGH]`, `[MEDIUM]`, `[LOW]`)
  - **Ease of Resolution:** (e.g., `[EASY]`, `[MODERATE]`, `[HARD]`)
  - **Implementation Risk:** (e.g., `[HIGH RISK]`, `[MEDIUM RISK]`, `[LOW RISK]`)
- Provide a clear explanation of the debt, why it is problematic, and a recommended approach to resolve it.
- **CRITICAL:** You MUST output this complete list of findings directly to the user in the chat interface before doing anything else.

### 5. Store Findings (Optional)
- If no technical debt was found, do NOT offer to document anything.
- After showing the list of found debt to the user, you MUST ask for their explicit permission to save this report to the `docs/tech-debt.md` file. DO NOT create or update the file automatically.
- If the user approves, write the complete structured list of findings into the file.
- You MUST include the current Date and Time of the scan at the very top of the file.

---
**Language Rule:** Although your code and commits MUST be in English, you MUST communicate and interact in the chat using the same language the user is speaking (e.g., Spanish, French, etc.).
