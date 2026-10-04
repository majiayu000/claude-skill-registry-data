---
name: thrunt-audit-evidence
description: Cross-phase audit of all outstanding Evidence Review and findings validation items
allowed-tools: Read, Glob, Grep, Bash
---

<objective>
Scan all phases for pending, skipped, blocked, and human_needed Evidence Review items. Cross-reference against codebase to detect stale documentation. Produce prioritized human test plan.
</objective>

<execution_context>
@.github/thrunt-god/workflows/audit-evidence.md
</execution_context>

<context>
Core planning files are loaded in-workflow via CLI.

**Scope:**
Glob: .planning/phases/*/*-EVIDENCE_REVIEW.md
Glob: .planning/phases/*/*-FINDINGS.md
</context>
