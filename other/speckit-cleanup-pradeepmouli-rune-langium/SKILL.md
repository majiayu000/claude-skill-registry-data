---
name: speckit-cleanup
description: Validate and reorganize spec-kit artifacts with proper numbering and
  structure
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: workflows:commands/cleanup.md
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

## Purpose

This workflow validates the organization of all spec-kit artifacts in the `specs/` directory, checking for:
- Sequential numbering (001, 002, 003, etc.)
- Proper directory structure based on workflow type
- Required files presence
- No gaps or duplicate numbers

**IMPORTANT**: This workflow only validates and reorganizes documentation in `specs/`. It **NEVER** moves or modifies code files.

## Instructions

1. **Understand the request**: Parse the user input for:
   - Whether they want a dry-run (validate only) or to apply fixes
   - The reason for cleanup (for documentation)
   - Whether to auto-fix issues or just report them

2. **Run the cleanup script** from the repo root:

   **For validation only (dry-run):**
   ```bash
   .specify/extensions/workflows/scripts/bash/create-cleanup.sh --json --dry-run "$ARGUMENTS"
   ```

   **For validation with auto-fix:**
   ```bash
   .specify/extensions/workflows/scripts/bash/create-cleanup.sh --json --auto-fix "$ARGUMENTS"
   ```

   **For validation only:**
   ```bash
   .specify/extensions/workflows/scripts/bash/create-cleanup.sh --json "$ARGUMENTS"
   ```

3. **Parse the JSON output** which includes:
   - `status`: "success" or "issues_found"
   - `message`: Summary message
   - `issues`: Array of issues found (with severity)
   - `actions`: Array of actions taken or suggested

4. **Present the results** to the user:

   If status is "success":
   ```
   Spec structure validation complete

   No issues found - all spec-kit artifacts are properly organized!
   ```

   If status is "issues_found":
   ```
   Spec structure validation found issues

   **Issues detected: [count]**
   [List issues from JSON with severity badges]

   **Actions [taken/suggested]: [count]**
   [List actions from JSON]

   **Next Steps:**
   - Review the issues and actions
   - Apply fixes (`--auto-fix` or agent-driven) after user confirmation
   - Rerun the script in `--dry-run` mode to verify it reports no issues
   - Repeat fix + dry-run until clean, then commit the cleanup separately from feature work
   ```

5. **Provide guidance based on issues (automatic vs. agent-driven fixes)**:

   - **Misplaced workflow directories (ERROR, automatic)**: Workflow-prefixed dirs at the wrong level (e.g., `bugfix-001-*` under `specs/` instead of `specs/bugfix/001-*`). The agent should: inspect contents, propose the target path, ask for confirmation, then move.
   - **Duplicate numbers within a workflow (ERROR, agent-driven)**: Same numeric prefix reused inside a workflow directory. The agent should inspect both dirs, propose a renumbering plan, ask for confirmation, then apply.
   - **Invalid directory names (ERROR, agent-driven)**: Entries inside workflow folders that do not start with a 3-digit prefix. The agent should suggest a compliant `NNN-description` rename, ask for confirmation, then apply.
   - **Unrecognized directories (WARNING, agent-driven)**: Items in `specs/` that are neither numbered specs nor known workflow folders (e.g., `specs/copilot/`). The agent should summarize contents and ask whether to move/rename/ignore.
   - **Non-sequential numbering / gaps (INFO, automatic)**: Numbering within a workflow skips values (001, 002, 005...). The agent should propose a renumbering plan, confirm, then apply unless blocked by unresolved errors (e.g., duplicates).
   - **Missing spec file (WARNING, agent-driven)**: Required spec file for the workflow type is absent (e.g., `bug-report.md`, `refactor-spec.md`, or `spec.md`). The agent should suggest creating the required file and ask before doing so.

## Example Usage

**Validation before release:**
```
/speckit.workflows.cleanup "validate before v2.0 release"
```

**Fix numbering after merge:**
```
/speckit.workflows.cleanup --auto-fix "fix numbering after merge"
```

**Dry-run to see what would change:**
```
/speckit.workflows.cleanup --dry-run --auto-fix "check organization"
```

## Safety Notes

Remind users that:
- Only affects documentation in `specs/` directory
- Code files are never touched
- Changes are reversible (git history preserved)
- Dry-run mode available to preview changes
- Detailed report generated for every run

## Common Scenarios

**After merging branches**: Specs from different branches may have overlapping numbers. Cleanup detects duplicates and can renumber automatically.

**Before releases**: Validate that all specs are properly organized before tagging a release.

**Periodic maintenance**: Monthly or quarterly cleanup runs help keep specs organized as the project grows.

**After reorganization**: If you manually moved or renamed specs, run cleanup to validate the new structure.

---

*Remember: This workflow is about organization and validation, not content. It ensures specs are numbered and located correctly but doesn't change what's written in them.*