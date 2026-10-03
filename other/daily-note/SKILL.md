---
name: daily-note
disable-model-invocation: true
allowed-tools: Bash(git log:*), Bash(gh pr list:*), Bash(date:*), Bash(cat:*), Read, Write, Edit, mcp__linear-server__list_issues, mcp__linear-server__list_issue_statuses
description: Create or update daily Obsidian logbook notes with issue-tracker and Git integration.
---

# Daily Logbook Assistant (`--plan`, `--summary`, `--status`, `--checkin`)

You manage the user's daily Obsidian notes, synchronizing tracker issues and Git activity.

> **Setup:** this skill reads an issue-tracker MCP server (examples use a Linear-style API) and
> your Obsidian vault. Fill in your own IDs and paths via `.env` (see `.env.example`) and enable
> the server in `.claude/settings.local.json`. The `mcp__linear-server__*` tool names are
> placeholders — swap them for your tracker's tools.

## Configuration & Context

Read these from `.env` (never hardcode real account IDs or personal paths):

- **Obsidian Path:** `$OBSIDIAN_VAULT/$OBSIDIAN_DAILY_DIR/` (e.g., `Daily Logbook/`)
- **Template:** `$OBSIDIAN_VAULT/Templates/Daily Log.md`
- **Tracker:** Assignee `${TRACKER_ASSIGNEE_ID}`, Team `${TRACKER_TEAM_ID}`.
- **Git Author:** derive from `git config user.name`, e.g. `--author="$(git config user.name)"`.

---

## Execution Modes

### 1. Morning Plan (`--plan`)

_Goal: Create today's note with goals and carryover._

1.  **Date Check:** Get today's date (`YYYY-MM-DD`). If the note exists, ask before overwriting.
2.  **Carryover:** Read yesterday's note. Extract unchecked items from the **Cache** section.
3.  **Tracker Sync:** Fetch `In Progress` and `To Do` issues assigned to the user.
4.  **Note Creation:** Populate the template.
    - **Focus:** Highest priority issue.
    - **Objectives:** Top 3 issues.
    - **Tasks:** All fetched issues + carryover.
5.  **Output:** Write to `$OBSIDIAN_VAULT/$OBSIDIAN_DAILY_DIR/{YYYY-MM-DD}.md`. Confirm with task counts.

### 2. Evening Summary (`--summary`)

_Goal: Update today's note with progress and artifacts._

1.  **Read Note:** Locate today's file. Stop if missing.
2.  **Fetch Activity:**
    - **Git:** `git log --oneline --since="today 00:00" --author="$(git config user.name)"`.
    - **GitHub:** `gh pr list --author=@me --search="created:>=YYYY-MM-DD"`.
    - **Tracker:** Identify issues marked `Done` today.
3.  **Update Sections:**
    - **Tasks:** Mark completed items `[x]`.
    - **Output:** Insert commit hashes and PR links.
    - **Cache:** Move remaining `[ ]` tasks here for tomorrow.
    - **Preserve:** Do NOT overwrite manual user edits in other sections.
4.  **Output:** Write changes and confirm update.

### 3. Quick Status (`--status`)

_Goal: Terminal-only dashboard._

1.  Read today's note (if it exists) and fetch current Git/tracker data.
2.  **Display:**
    - Task completion ratio (e.g., `3/5 completed`).
    - List of Git commits today.
    - Tracker status (Completed vs. In Progress counts/titles).

### 4. Teams Check-in (`--checkin`)

_Goal: Generate plain-text async update for MS Teams (or any chat)._

1.  **Context:** Fetch `In Progress` issues. Read **Focus** and **Blockers** from today's Obsidian note.
2.  **Format:** Output **exactly** as follows (no markdown; name from `git config user.name`):
    ```text
    {User Name}
    Focus: {Issue Title 1} + {Issue Title 2} (Concise & punchy)
    Blocker: {From note or "None"}
    Signal: {Notable news or "None"}
    Links: {Issue URLs or "None"}
    ```

---

## Critical Rules

- **Issue Format:** `- [ ] {title} ([{ID}]({url}))`.
- **Sorting:** Always sort tracker issues by priority (Urgent/High first).
- **Persistence:** Never delete manual user content during `--summary` updates.
