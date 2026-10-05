---
name: temp
description: Make temporary code changes for testing that can be easily undone.
  Use when user says "temp", "temporary change", "temporarily enable/disable/show/hide",
  or needs to force a UI state, bypass a guard, or flip a feature flag for local testing.
  Also handles "temp undo" to revert all temporary changes, and "temp list" to show them.
effort: low
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Temp

Make quick, reversible code changes for local testing. Every change is marked with a `TEMP:` comment so it can be found and undone later.

## Modes

### 1. Make a temporary change (default)

Usage: `temp always show questionnaire`

1. Search the codebase for code related to the user's description.
2. Make the **minimal** change needed — flip a boolean, comment out a guard, force a condition, hardcode a value. Prefer the smallest diff possible.
3. Mark every modified line with a comment containing `TEMP:` and the reason. Use the appropriate comment syntax for the language.

**Marking rules:**
- Add `// TEMP: <reason>` (or `# TEMP:`, `/* TEMP: */`, `-- TEMP:`, etc.) at the end of each changed line, or on the line above if end-of-line isn't practical.
- If commenting out code, wrap it like:
  ```
  // TEMP: always show questionnaire — commented out guard
  // if (!hasSeenQuestionnaire) {
  ```
- If changing a value:
  ```
  const showOnboarding = true; // TEMP: always show onboarding (was: false)
  ```
- Always include what the original value was when replacing a value, using `(was: ...)`.

4. Tell the user what was changed and how to undo (`temp undo`).

### 2. Undo all temporary changes

Usage: `temp undo`

1. Grep the project for `TEMP:` markers.
2. If no markers found, tell the user there are no temporary changes.
3. For each file with markers, use `git checkout` or `git restore` to revert the file. If the file has other unstaged changes mixed in, restore only the TEMP-marked lines manually by reading the original from git and editing surgically.
4. Confirm what was reverted.

### 3. List current temporary changes

Usage: `temp list`

1. Grep the project for `TEMP:` markers.
2. Display each one with file path, line number, and the marker text.
3. If none found, say "No temporary changes active."

## Examples

### Example 1: Force a questionnaire to always show

User says: `temp always show questionnaire`

Actions:
1. Search for questionnaire-related display logic (e.g., `hasSeenQuestionnaire`, `showQuestionnaire`, `questionnaire` + conditional).
2. Find: `if (!user.hasCompletedQuestionnaire) { showQuestionnaire(); }`
3. Change to: `if (true) { showQuestionnaire(); } // TEMP: always show questionnaire (was: !user.hasCompletedQuestionnaire)`
4. Report the change.

### Example 2: Disable auth check

User says: `temp skip auth`

Actions:
1. Find auth middleware or guard.
2. Comment out or force-pass the check, marking with `// TEMP: skip auth`.

### Example 3: Undo

User says: `temp undo`

Actions:
1. Search the codebase for `TEMP:` markers.
2. Found markers in `src/components/Questionnaire.tsx:42` and `src/middleware/auth.ts:15`.
3. Restore original code for each marked line (read original from git or use the `(was: ...)` hint).
4. Confirm: "Reverted 2 files, removed all TEMP markers."

## Troubleshooting

### Can't find relevant code
**Cause:** The description is too vague or uses different terminology than the codebase.
**Solution:** Ask the user for more specific terms, file names, or feature names to search for.

### Undo reverts more than TEMP changes
**Cause:** The file had other unstaged modifications mixed with TEMP changes.
**Solution:** Instead of reverting the whole file, surgically restore only the TEMP-marked lines by reading the original from `git show HEAD:<file>` and editing just those lines back.
