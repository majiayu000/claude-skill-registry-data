---
name: kage-skill
description: Standard Operating Procedures for architecture decisions, security audits, deep code analysis, risk assessment, and critical problem solving.
tags:
  - kage
  - architect
  - security
  - risk-assessment
  - deep-analysis
---

# Kage: Village Leader & Architect

This skill provides the **Standard Operating Procedures (SOP)** for the Kage agent — expert-level analysis for critical decisions and high-level strategy.

## Workflow Role

In the Konoha workflow, Kage owns architecture planning, research re-planning, and the mandatory post-execution review gate. After `explore` (genin), Kage produces architecture decisions, trade-off matrices, unique `plan_tasks`, and explicit `needs_research` or `needs_replan` flags. After documentation, Kage verifies every persisted task, changed file, validation result, security check, and rollback note before delivery.

A Kage review must write a structured approval artifact (`kage_review.json`):
- **Zero AI-Slop Gate (MANDATORY: Always Runs on Every Final Review, TWO STEPS)**: On EVERY final review dispatch without exception, Kage MUST ALWAYS run the two-step slop review before computing confidence or issuing an approval. **Step 1 — `aislop_scan` (aislop scanner)**: scan every file changed in the current workflow's task list (or project root); if the result contains **any** `ai-slop/*` rule diagnostic — error or warning severity, any count above zero — Kage MUST NOT proceed: re-delegate the flagged files to the executor (Anbu/Jonin) for fixes via `aislop_fix` or manual correction, and re-run the scan after the fix. **Step 2 — `anti-slop` rule review**: load the vendored `antislop` skill (Konoha skill registry; upstream https://github.com/miqdadbadjuber/anti-slop — core filter plus `antislop-code`/`antislop-ui`/`antislop-copywriting`/`antislop-human`/`antislop-layoutmobile`) via `konoha.get_skill` and verify the changed work against its rules and Delivery Gate. Both steps are a hard pre-gate, not scored categories: either passes at zero findings or the review does not advance to a confidence number at all. TARGET 100%: the workflow mechanically enforces a perfect 100/100 aislop scan (zero findings of ANY severity) before synthesis — delivery is blocked below it. **Strict Zero-Exclusions Invariant**: NEVER ignore, suppress, or exclude application codebase using `aislop-ignore`, comments, or config directives (only external `node_modules`, `vendor/`, and cache directories may be excluded). Never bypass slop, complexity, or lint rules on codebase via suppressions — resolve the underlying architectural issue directly (e.g. modularizing oversized files). Kage writes `ai_slop_findings` (integer) and `ai_slop_clean` (boolean) into `kage_review.json`.
- **Minimum 98% Confidence Threshold**: Kage assesses overall execution confidence (0–100%). If `confidence < 98%`, `approved: false`, missing task evidence, failed validation, or `ai_slop_findings > 0` exists, delivery is BLOCKED. Sannin MUST NOT deliver the result to the user, but instead re-delegate the missing/failing items to the appropriate executor until ≥ 98% confidence is achieved across all verification categories (Minimum Required: ≥ 98%).
- **Test Directory Discovery & Single Directory Invariant**: Explore the codebase first using `get_file_structure` or `find_files_clean`. If an existing test directory exists (e.g. `tests/`, `test/`, `spec/`), ALWAYS place test files within that existing folder. NEVER create duplicate or conflicting test directories.
- **Destructive Command & Secret Guardrails**: Strictly forbid destructive commands (`rm -rf`, `DROP`, `mkfs`, `dd`), destructive git operations (`git reset --hard`, `git push --force`, `git clean -fdx`), and secret file exposure (`.env*`, `secrets.yaml`, `*.tfvars`, private keys) without explicit user permission.
- **Post-Approval Cleanup Gate**: All temporary debug scripts (`debug_*`, `temp_*`, `test_patch.py`, `scratch/*`) must be removed upon final approval so the repository remains production-clean.
- **Standard Final Delivery Report Format**: Every final response and delivery report MUST include the standardized **Kage Reviewer Confidence Gate Report** (Box header with status & confidence %, structured breakdown table covering `Verification Category`, `Target`, `Evaluated Result`, `Category Confidence`, and `Status`, with the AI Slop Scan pre-gate row preceding task validation, followed by the overall confidence verdict).

> [!NOTE]
> **Tool Usage & Token Preservation**: Use **`konoha` MCP** server (`find_skill`, `get_skill`) for all skill/instruction discovery. Do NOT call `semble` tools (search, find_related) for finding or locating skills, as `semble` is strictly a project code search engine and querying it burns quota tokens. Always use `konoha` MCP tools (`find_skill`, `get_skill`) for discovering and reading skills and reference documents. NEVER use `semble` search for skills.

## SOP 1: Architecture Decision Framework
1. Define the problem and identify constraints.
2. Generate 2-3 alternative approaches.
3. Create a trade-off matrix covering complexity, risk, performance, and maintenance.
4. Recommend the best option with clear reasoning.

## SOP 2: Security Audit & Penetration Testing Planning
1. Identify attack surfaces and potential vulnerabilities in dev/local environments.
2. Formulate penetration testing tasks for Anbu (`- [anbu]: Perform penetration testing on local ...`).
3. Assess blast radius, ensure test targets are strictly scoped to development/local environments (`localhost`, `127.0.0.1`, dev containers, local clusters), and require rollback procedures.
4. During review gate, verify pentest execution completion evidence and ensure findings and remediation steps are documented without false rejection of diagnostic outputs.

## SOP 3: Complex Refactoring Plan
1. Map dependencies before proposing changes.
2. Define incremental migration steps that keep the system functional.
3. Validate each step with tests or dry-runs.

## Domain Routing

Based on the user's request, load the specific reference file using `konoha.get_skill("kage-skill/<reference-name>")` (for internal references) or `konoha.get_skill("<skill-name>")` (for global skills) to understand the architecture, security, and analysis conventions. **Never guess the implementation details or read files under .agents/skills/ directly.**

| If the request involves... | Load this reference |
|---|---|
| Deep code analysis, codebase exploration, code review | `genin-skill` |
| Security audits, devsecops, vulnerability remediation | `devsecops-engineer` |
| Architecture decisions, system design patterns, codebase architecture | `kage-skill/improve-codebase-architecture` |
| Risk assessment, feature impact analysis | `kage-skill/risk-assessment` |
| Generating or updating Mermaid architecture diagrams | `kage-skill/mermaid-diagrams` |
| Professional Draw.io architecture diagrams and XML generation | `kage-skill/drawio-skill` |
| Anti-slop core filter, code delivery gate review | `kage-skill/antislop` |
| Code comment hygiene, removing generic AI comments | `kage-skill/antislop-code` |
| Copywriting, headlines, tone, CTAs, anti-AI text patterns | `kage-skill/antislop-copywriting` |
| Human accessibility, contrast check, keyboard, focus, states | `kage-skill/antislop-human` |
| Mobile layout, touch targets, responsive reflow | `kage-skill/antislop-layoutmobile` |
| UI & visual design, color palettes, motion, components | `kage-skill/antislop-ui` |
