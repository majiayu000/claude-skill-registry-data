---
name: hardening-resilience
description: Evaluate error handling, i18n, text overflow, and edge cases.
phase: 10 (Compliance)
role: Reviewer
---

# Hardening & Resilience Review

**Role Constraints:** Reviewer (STRICTLY READ-ONLY for application code). You MAY NOT modify, fix, or write to application source code.
**File Access:** Use the `glob` tool to search for the active feature directory under `.jonggrang/.output/features/`. You may only use the `write` tool to save your audit report inside this specific directory.

## Objective
Evaluate the codebase for interface and backend resilience: proper error handling, i18n support, edge case management, and graceful degradation.

## Execution Steps

1. **Discover Context:** Use `glob` and `read` to explore the application code modified or created for the current feature.
2. **Review Dimensions:**
   - **Error Handling:** Are exceptions caught? Are user-friendly error messages returned? Do APIs fail gracefully?
   - **Edge Cases:** Are empty states handled? What happens with extremely long inputs, unexpected nulls, or network timeouts?
   - **Internationalization (i18n):** Are strings hardcoded or localized?
   - **Data Validation:** Is boundary testing applied to inputs?
3. **Generate Hardening Report:**
   - Document specific files and line numbers where resilience gaps exist.
   - Detail the impact of the missing hardening measure.
   - Propose exactly how the code should be fixed (do not fix it yourself).
4. **Save Report:**
   - Write the findings using the `write` tool to `.jonggrang/.output/features/<active-feature-dir>/hardening-report.md`.

## Completion Signal
When the hardening report is saved, output exactly:

HARDENING_REVIEW_COMPLETE
