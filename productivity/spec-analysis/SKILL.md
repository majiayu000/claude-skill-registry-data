---
name: spec-analysis
description: Perform a non-destructive cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md. Identifying inconsistencies, duplications, ambiguities, and underspecified items.
---

# Specification & Planning Analysis

## Overview

Identify inconsistencies, duplications, ambiguities, and underspecified items across the three core artifacts (`spec.md`, `plan.md`, `tasks.md`) before implementation.

**STRICTLY READ-ONLY**: Do **not** modify any files. Output a structured analysis report. Offer an optional remediation plan.

**Constitution Authority**: The project constitution (`.specify/memory/constitution.md`) is **non-negotiable**.

## Execution Steps

1.  **Initialize Analysis Context**:
    *   Load `FEATURE_DIR/spec.md` (or `specs/spec.md`).
    *   Load `FEATURE_DIR/plan.md` (or `specs/plan.md`).
    *   Load `FEATURE_DIR/tasks.md` (or `specs/tasks.md`).
    *   Ensure all files exist; if not, report which are missing (though tasks might not exist yet if only planning).

2.  **Load Artifacts (Progressive Disclosure)**:
    *   Load only necessary portions relevant to the feature.
    *   Load `.specify/memory/constitution.md` for validation.

3.  **Build Semantic Models**:
    *   **Requirements inventory**: Functional + non-functional requirements.
    *   **User story/action inventory**: User actions + acceptance criteria.
    *   **Task coverage mapping**: Map task to requirement/story.
    *   **Constitution rule set**: Principle names and MUST statements.

4.  **Detection Passes**:
    *   **Duplication**: Near-duplicate requirements.
    *   **Ambiguity**: Vague adjectives ("fast", "robust") without metrics. Unresolved placeholders (TODO, ???).
    *   **Underspecification**: Verbs missing objects/outcomes. User stories missing acceptance criteria.
    *   **Constitution Alignment**: Conflict with MUST principles. Missing mandated sections.
    *   **Coverage Gaps**: Requirements with zero tasks. Tasks with no mapped requirement.
    *   **Inconsistency**: Terminology drift. Data entities in plan but absent in spec. Task order contradictions.

5.  **Severity Assignment**:
    *   **CRITICAL**: Violates constitution, missing core artifact, blocking requirement with zero coverage.
    *   **HIGH**: Duplicate/conflicting requirement, ambiguous security/performance, untestable AC.
    *   **MEDIUM**: Terminology drift, missing non-functional task coverage, underspecified edge case.
    *   **LOW**: Style/wording improvements.

6.  **Produce Compact Analysis Report**:
    *   Output a Markdown report with a findings table: | ID | Category | Severity | Location | Summary | Recommendation |
    *   **Coverage Summary Table**: Requirement Key | Has Task? | Task IDs | Notes
    *   **Metrics**: Total Requirements, Total Tasks, Coverage %, Ambiguity Count.

7.  **Provide Next Actions**:
    *   Recommend resolving CRITICAL issues before implementation.
    *   Provide explicit suggestions (e.g., "Refine spec", "Adjust plan").

8.  **Offer Remediation**:
    *   Ask if the user wants concrete remediation edits for top N issues.

## Operating Principles

*   **Context Efficiency**: Focus on actionable findings.
*   **NEVER modify files** automatically (read-only analysis).
*   **NEVER hallucinate missing sections**.
*   **Prioritize constitution violations**.
