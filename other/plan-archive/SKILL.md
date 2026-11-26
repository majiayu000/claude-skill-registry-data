---
name: plan-archive
allowed-tools: >-
  Read, Write, Edit, Glob, AskUserQuestion, Bash(mkdir:*), Bash(cp:*), Bash(mv:*), Bash(rm:*),
  Bash(echo $PPID), Bash(echo $COPILOT_AGENT_SESSION_ID), Bash(kill -0:*), Bash(find:*), Bash(ls:*)
description: >-
  Archive a completed or abandoned plan for future reference. Use when the user runs /plan-archive or asks to
  archive a finished plan.
license: MIT
disable-model-invocation: true
---

On Codex, invoke skills with `$skill-name` (for example, `$plan-create`). Use that form when giving Codex
commands; other clients use `/skill-name`.

You are archiving the user's completed (or abandoned) plan for future reference.

To do this, follow these steps precisely:

1. Resolve `plansFolder` from config:
   Check the active agent's config file first (`.codex/plan-critique-config.json` for Codex,
   `.claude/plan-critique-config.json` for Claude Code,
   `.gemini/plan-critique-config.json` for Agy/Gemini, or `.copilot/plan-critique-config.json` for Copilot CLI),
   falling back to reading the other agent configs. If no config exists or `plansFolder` is not set or is empty:
   Respond with "No plans folder configured. Run `/plan-create` first to set up."
2. Get the active session id:
   - On Copilot CLI (or when `COPILOT_AGENT_SESSION_ID` is set): read `COPILOT_AGENT_SESSION_ID` via
     `echo $COPILOT_AGENT_SESSION_ID` (macOS/Linux) or `$env:COPILOT_AGENT_SESSION_ID` (Windows); if empty, use the
     literal value `default`. Store as `sessionId`.
   - Otherwise (Codex, Claude Code / Agy): run `echo $PPID` and store as `sessionId`.
3. Clean up stale sessions in `[plansFolder]/.sessions/` (non-blocking, never abort because of cleanup):
   - For numeric PID filenames, check `kill -0 [PID] 2>/dev/null` and delete if the process is no longer running.
   - For non-PID session files (e.g. `default` or UUIDs), delete files not modified in the last 7 days.
4. Read the current session's plan from `[plansFolder]/.sessions/[sessionId]` if it exists. Store as `sessionPlan`.
5. Scan `[plansFolder]/` for subdirectories (each subdirectory is a plan).
   Exclude `archived/` and `.sessions/` folders and any files, only list plan directories.
   If no plan folders exist: Respond with "No plans found. Nothing to archive."
6. Select the plan to archive:
   - If `sessionPlan` exists and matches a plan folder, auto-select it. Inform the user:
     "Using current session plan: [sessionPlan]"
   - Else if only one plan exists, auto-select it and inform user.
   - Otherwise, ask the user to select a plan from the list.
     Example:
     ```
     Available plans:
     1. add-user-authentication
     2. refactor-database-layer
     3. implement-caching

     Which plan would you like to archive? [1-3]
     ```
7. Check prerequisites. If `[plansFolder]/[selected-plan]/plan.md` does not exist or is empty:
   Respond with "Nothing to archive. Plan file is missing or empty."
8. Ensure `[plansFolder]/archived/` exists, create it if not.
9. Extract metadata:
   - Read `plan.md` to get the plan title (first H1 heading). If no title, use folder name.
   - Read `critique.md` to get keywords (if available)
   - Read `execution-log.md` to get execution status (if available)
10. Generate archive folder name using format: `YYYY-MM-DD_HH-MM-SS_[slug]/`
    Example: `2026-01-12_14-30-00_add-user-authentication/`
11. Create the archive folder at `[plansFolder]/archived/[folder-name]/`
12. Copy contents from `[plansFolder]/[selected-plan]/` to the archive:
    - Include: `plan.md`, `execution-log.md` (if exists), all other files (SQL, images, etc.)
    - Exclude: `critique.md`, `execution-state.json`
13. Create `archive-info.md` in the archive folder using [archive-info-format.md](archive-info-format.md).
14. Delete the original plan folder `[plansFolder]/[selected-plan]/` entirely.
15. Clean up session references to the archived plan:
    - Delete `[plansFolder]/.sessions/[sessionId]` if it contains the archived plan slug.
    - Scan all other session files and delete any that reference the archived plan (handles stale references).
16. Respond with confirmation:
    ```
    Plan archived to: [plansFolder]/archived/[folder-name]/

    The original plan folder has been removed.
    Create a new plan with `/plan-create`.
    ```

Notes:

- Never include critique.md in the archive (only keywords are preserved in archive-info.md)
- Always include the full original plan and all supporting files
- Include execution log only if the plan was executed
- Use current timestamp for the archive folder name
- Preserve the original file structure within the archived folder
- Always delete the original plan folder after archiving
- It is valid to archive a plan that was never executed (abandoned, reference, or superseded plans).
  In this case, the execution status will be `NOT_EXECUTED`.
