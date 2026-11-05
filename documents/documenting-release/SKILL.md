---
name: documenting-release
description: Cross-reference diffs to update README, ARCHITECTURE, CHANGELOG.
phase: 16 (Complete)
role: Lead
---

# Documenting Release

**Role Constraints:** Lead (Write/Bash access allowed).
**File Access:** Do NOT use literal placeholders for file paths. Use the `glob` tool to search for the active feature directory under `.jonggrang/.output/features/`.

## Objective
Ensure every documentation file in the project is accurate, up to date, and written in a friendly, user-forward voice before the feature is fully released.

## Execution Steps

1. **Pre-flight & Diff Analysis:**
   - Use `bash` to run `git diff main...HEAD --stat` (or the appropriate base branch) to understand what changed.
   - Classify changes into features, changed behavior, removals, and infrastructure.
2. **Per-File Documentation Audit:**
   - Locate major documentation files (`README.md`, `ARCHITECTURE.md`, `CHANGELOG.md`, `CONTRIBUTING.md`) using `glob`.
   - Read each file and cross-reference it against the git diff.
3. **Apply Factual Updates:**
   - Use the `edit` or `write` tool to make factual corrections directly (e.g., adding a command to a table, updating counts).
   - Use the `bash` tool if you need to run specific scripts that generate documentation.
4. **CHANGELOG Voice Polish:**
   - If `CHANGELOG.md` exists, review the entry for the current feature.
   - Polish the wording to focus on user capabilities ("You can now...") rather than implementation details. Do NOT delete or regenerate existing entries, only refine them.
5. **Ask About Risky Changes:**
   - If narrative changes, security model descriptions, or massive rewrites are needed, ask the user for confirmation before proceeding.
6. **Cross-Doc Consistency Check:**
   - Ensure the `README` aligns with `ARCHITECTURE` and `CHANGELOG`. Fix any clear factual inconsistencies.

## Completion Signal
When the documentation has been updated and verified, output exactly:

DOCUMENTATION_COMPLETE
