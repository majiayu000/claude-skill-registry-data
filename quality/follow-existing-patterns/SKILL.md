---
name: follow-existing-patterns
description: Enforces that all new code, docs, and config match the existing codebase conventions, structure, and style — preventing inconsistent implementations that get reworked each session.
---

# Follow Existing Patterns Skill

## Problem it solves

Each session produces code that looks different from what's already in the codebase. New commands don't match existing command patterns, docs use different formatting, menu items have inconsistent descriptions. This accumulates into a mess that gets rewritten every session.

Root cause: writing code based on assumptions rather than reading the existing conventions first.

## Protocol

### 1. Before writing any new code, doc, or config

Read the existing patterns:

- **For a new command**: Read 2-3 existing command implementations end-to-end. Note the structure: error handling style, status prefix format (`[+]`/`[!]`/`[-]`/`[ERROR]`), verification steps, prompt patterns, flow order.
- **For docs**: Read the existing doc sections. Note heading levels, flow description format, code block style, table formatting.
- **For menu items**: Read the existing menu formatting. Note numbering, indentation, description style.

### 2. Pattern checklist before implementing

Verify your planned implementation matches:

- **Structure** — Same label format (`:command`), same sections (header, description, steps, verification, next step)
- **Error handling** — Same `%errorlevel%` check style, same `pause` / `goto :end` pattern
- **Status messages** — Same prefix usage: `[*]` for actions, `[+]` success, `[!]` warning, `[-]` info, `[ERROR]` failure
- **User interaction** — Same prompt style (`set /p "var=Prompt? (Y/n): "`), same `if /i "!var!"=="n"` pattern
- **Non-blocking windows** — Same `start "Title" cmd /c "command & pause"` + `pause` pattern if used
- **Verification** — Same command-after-command verification with status reporting
- **Cancel windows** — Same `timeout /t N /nobreak >nul` duration and placement

### 3. For each new addition, cite which existing pattern you followed

In your response, specify: "Followed pattern from `:existing_label`" so the user can verify consistency without re-explaining.

### 4. When renaming or restructuring

Do not change existing patterns. If an existing pattern is wrong, add the new thing correctly and note the inconsistency — do not fix both at once.

## Detection triggers

Activate when:
- Adding a new command, menu option, or doc section
- Writing any new code in an existing file
- User has previously corrected inconsistencies in the session

## When NOT to use
- Greenfield projects with no existing code
- User explicitly requests a different style from existing patterns


## Cross-references

- **anti-sycophancy** — Following patterns prevents repeated corrections that trigger sycophancy loops.
- **universal-format-lint** — Both enforce consistency. follow-existing-patterns covers code structure and style; universal-format-lint covers formatting and lint rules.
- **dont-kill-tokens** — Reading existing patterns first reduces trial-and-error, saving tokens.


- **self-validate** — After implementing, validate that the new code actually matches the patterns.

- **audit-project** — Use audit to verify the project consistently follows its own patterns across all files.
- **self-validate** — Validate that new code matches existing patterns after implementation.
- **project-scripts** — Generated scripts must match the project's existing script patterns. Run project-scripts after script creation to catalog and verify consistency.
- **release-changelog** — Before cutting a release, read 2-3 prior changelog entries to match the project's changelog style and versioning conventions.
- **skill-loader** — Cross-referenced skills may have their own patterns. Follow the most specific one for the current subtask.
- **test-driven-development** — Tests must follow the project's existing test framework, naming conventions, and file layout patterns.
- **code-review** — Review checks that new code matches the project's existing patterns as part of the architecture axis.
- **incremental-implementation** — Each slice must follow the project's existing patterns. Don't start with perfect patterns — refactor toward them across slices.
- **adr-and-documentation** — ADRs must match the project's existing ADR format and numbering scheme.
- **receiving-code-review** — When implementing review feedback, check that the change follows existing patterns.
- **writing-quality-anti-slop** — Writing style should match the project's existing documentation voice and tone.
- **code-simplification** — Simplicity is relative to the project. Don't simplify a complex pattern if it's the project's established style.
- **context-engineering** — Reading existing patterns is a context engineering decision. Load 2-3 examples, not all of them.
- **api-contract-design** — API contracts must match the project's existing API conventions (naming, versioning, error format).
- **performance-optimization** — Performance optimizations should match the project's existing approach (caching strategy, query patterns, etc.).

## Bundled pattern checker

A bundled script at `scripts/check-patterns.ps1` (PowerShell) detects code style inconsistencies:

```powershell
.\scripts\check-patterns.ps1 -ProjectPath ".\"
```

Checks: mixed indentation (tabs vs spaces per extension), inconsistent license headers, mixed naming conventions (snake_case vs camelCase). Reports all issues found.

To use as a project-local tool:

```powershell
cp <skill-path>/follow-existing-patterns/scripts/check-patterns.ps1 .ai_scripts/
.ai_scripts\check-patterns.ps1 -ProjectPath "."
```
