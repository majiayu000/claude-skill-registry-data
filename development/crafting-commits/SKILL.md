---
name: crafting-commits
description: Generates git commit messages following conventional commit standards with collaborative attribution. Use when user requests commit message creation, drafting, or help with formatting.
allowed-tools:
  - bash(git:*)
---

# Crafting Git Commits

A professional git commit message drafting service that follows modern conventional commit standards, provides collaborative attribution, and includes quality validation for reliable development workflows.

This skill follows the principle of progressive disclosure. This file contains the core workflow and high-level guidance. For more detailed information, please refer to the linked reference files.

## Core Workflow

1.  **Analysis**: I start by analyzing the staged changes to understand the context.
    -   `git status`
    -   `git diff --staged`
    -   `git log --oneline -5`
2.  **Planning**: I identify the commit type, scope, and assess any potential impact, including breaking changes.
3.  **Validation**: I use a detailed checklist to ensure the commit message meets all quality standards. See [validation.md](validation.md) for the full checklist.
4.  **Execution**: I draft the commit message, add attribution, and execute the commit, verifying it in the git history.

## Reference Documents

For detailed information, please refer to these files:

- **[examples.md](examples.md)**: A comprehensive list of commit message examples for different scenarios (features, bug fixes, docs, etc.).
- **[validation.md](validation.md)**: Detailed checklists for validating commits at all freedom levels.
- **[patterns.md](patterns.md)**: Advanced patterns, formatting best practices, attribution guidelines, and freedom levels.
- **[troubleshooting.md](troubleshooting.md)**: A guide to common Git errors and recovery procedures.

## Utility Scripts

This skill includes executable scripts for validation and analysis.

-   **`scripts/validate_commit.sh`**: Checks if a commit message follows the conventional commit format.
-   **`scripts/check_attribution.sh`**: Validates the `Co-Authored-By` format in a commit message.
-   **`scripts/analyze_changes.sh`**: Provides a summary of staged changes to help draft a commit message.

## System Requirements

-   Git version 2.25.0 or higher
-   Bash shell access
-   Standard Unix tools (`ls`, `grep`, etc.)
