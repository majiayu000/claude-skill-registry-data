---
name: logging-session
description: |
  Record and query AI conversation logs — what users asked, how it was solved, and the result.
  Use when users want to logging conversation, summarize recent work from sessions,
  or want daily/weekly project summaries from past conversations. 
---

# Logging Session

This skill records coding session summaries to a local SQLite database stored in your local path, so you can later query and summarize your work across projects and time periods.

## Why this matters

Coding sessions produce valuable knowledge — decisions made, problems solved, approaches tried and abandoned. Without capturing these, each session starts from scratch. This skill turns conversations into searchable, summarizable records that feed into daily standups, weekly reviews, and long-term project memory.

## Database location

The database path is defined by `db_path` in `config.json`, defaulting to:

```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/vault4life/dev_knowledge.db
```

To customize, edit `<skill-path>/config.json`.

If the database doesn't exist yet, initialize it:

```bash
python3 <skill-path>/scripts/init_db.py
```

The script reads the path from `config.json` automatically. You can also specify a path manually:

```bash
python3 <skill-path>/scripts/init_db.py /path/to/your/dev_knowledge.db
```

## Schema

```sql
CREATE TABLE dev_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    project_name TEXT NOT NULL,
    session_id TEXT NOT NULL,
    parent_id INTEGER DEFAULT NULL,
    task_category TEXT,
    user_query TEXT NOT NULL,
    thought_process TEXT,
    final_result TEXT,
    file_paths TEXT,
    git_hash TEXT,
    extra_metadata TEXT,
    FOREIGN KEY (parent_id) REFERENCES dev_logs (id)
);
```

## When to record

Record a session log entry when:
1. **User explicitly asks** — they say "record this session", "log this conversation", "logging-session", etc.
2. **A meaningful task completes** — when a significant coding task is done (bug fixed, feature added, refactoring completed), and the user wants it captured.
3. **Via Stop hook** — when the hook fires automatically at session end, synthesize the entire conversation into a log entry.

Do NOT record trivial interactions (quick questions, simple lookups, clarifications) unless the user asks.

## How to record a session log

When recording, you need to synthesize the conversation into a structured entry. Don't just copy-paste — distill the essence.

### Step 1: Gather context

Collect these fields from the conversation and environment:

| Field | Source | Notes |
|-------|--------|-------|
| `project_name` | Current working directory's folder name | Use `basename $(pwd)` or equivalent |
| `session_id` | Generate from date + random suffix | Format: `YYYYMMDD_xxxx` (e.g., `20260513_a3f2`) |
| `parent_id` | If this continues a previous log entry, use that entry's ID | Otherwise `null` |
| `task_category` | Classify the task: `bugfix`, `feature`, `refactor`, `debug`, `setup`, `docs`, `test`, `other` | |
| `user_query` | The user's original question or task description | In the user's own words when possible |
| `thought_process` | Your analysis approach, alternatives considered, key decisions | Concise but informative — this is the "how" |
| `final_result` | What was actually done, the outcome | Include key code changes, file paths, or resolution |
| `file_paths` | Files that were created or modified | Comma-separated |
| `git_hash` | Current HEAD commit hash if in a git repo | Run `git rev-parse --short HEAD` |
| `extra_metadata` | Any additional context as JSON | Optional |

### Step 2: Write the entry

Run the save script:
```bash
python3 <skill-path>/scripts/save_log.py \
  --project "<project_name>" \
  --session "<session_id>" \
  --query "<user_query>" \
  --thought "<thought_process>" \
  --result "<final_result>" \
  --category "<task_category>" \
  --files <file1> <file2> \
  --git "<git_hash>"
```

For fields with spaces or special characters, wrap in quotes. The `--parent`, `--category`, `--files`, `--git`, and `--meta` flags are optional.

### Step 3: Confirm

After saving, tell the user:
- The log entry ID
- A brief summary of what was recorded

Example: "Session logged as #5 — recorded the auth bug fix in project my-app."

## Querying session logs

### Summarize recent work

When the user asks for a summary (daily, weekly, or custom range):

```bash
# Last 7 days for current project
python3 <skill-path>/scripts/query_logs.py \
  --project "<project_name>" \
  --days 7 \
  --format markdown

# Today's logs across all projects
python3 <skill-path>/scripts/query_logs.py \
  --days 1 \
  --format markdown

# Specific date range (YYYYMMDD format, inclusive)
python3 <skill-path>/scripts/query_logs.py \
  --start-date 20260501 \
  --end-date 20260515 \
  --format markdown

# Specific session's full thread
python3 <skill-path>/scripts/query_logs.py \
  --session "<session_id>" \
  --format ai
```

### Output formats

- `markdown` — structured Markdown with headers by date (good for reports and Obsidian)
- `ai` — plain text blocks, compact (good for feeding back to AI)
- `json` — raw JSON array (good for programmatic processing)

### Weekly Project Summary (项目周报)

When the user asks to summarize work by project for the past week or generate a weekly report, use `weekly_summary.py`. This script groups entries by project, shows task category breakdowns, and lists individual session details — all in a clean markdown table format.

**Trigger phrases**: "总结过去一周的工作", "本周工作总结", "生成周报", "项目周报", "weekly summary", "summarize past week's work"

```bash
# All projects, past 7 days
python3 <skill-path>/scripts/weekly_summary.py --days 7 --format markdown

# Single project, past 14 days
python3 <skill-path>/scripts/weekly_summary.py --project "my-app" --days 14

# Specific date range (YYYYMMDD format, inclusive)
python3 <skill-path>/scripts/weekly_summary.py \
  --start-date 20260501 \
  --end-date 20260515 \
  --format markdown

# Export to Obsidian
python3 <skill-path>/scripts/weekly_summary.py \
  --format markdown \
  --output ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/vault4life/周报-$(date +%Y-W%V).md

# JSON for programmatic use
python3 <skill-path>/scripts/weekly_summary.py --format json
```

The markdown output includes an overview section (total entries, projects involved, time period) and per-project sections with task category distribution tables and session detail tables.

### Saving to Obsidian

When the user wants to save the summary as an Obsidian note:
```bash
python3 <skill-path>/scripts/query_logs.py \
  --days 7 \
  --format markdown \
  --output ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/vault4life/Weekly-$(date +%Y-W%V).md
```

## Automatic logging via Stop hook

When triggered by the Stop hook (session is ending), you are the last action in this conversation. Your job: synthesize the entire conversation into one log entry and write it to the database.

### What to do when the Stop hook triggers you

1. **Review the full conversation** — identify the user's main question/task, your approach, and the outcome.
2. **Gather context** — project name from CWD, git hash, files touched.
3. **Classify the task** — pick the most fitting category.
4. **Write one log entry** using the save script with all fields populated.
5. **Keep it brief** — this is a summary, not a transcript. One sentence each for thought_process and final_result is fine.
6. **Do NOT ask the user for confirmation** — just save and done. The session is ending.

### Hook configuration

The Stop hook is configured in `~/.claude/settings.json`. See `references/hooks-guide.md` for full setup details.

## Task categories

| Category | Description |
|----------|-------------|
| `bugfix` | Fixed a bug or error |
| `feature` | Added new functionality |
| `refactor` | Restructured code without changing behavior |
| `debug` | Investigated an issue (may not have fixed it) |
| `setup` | Project setup, configuration, dependencies |
| `docs` | Documentation work |
| `test` | Writing or fixing tests |
| `other` | Anything else |

## Tips for good session logs

- **user_query**: Capture the intent, not just the literal question. "How do I fix the login crash?" is better than "login crash".
- **thought_process**: Focus on the *why*, not the *what*. "Tried approach A but it conflicted with the existing auth flow, so switched to B" is valuable. "Changed 3 files" is not.
- **final_result**: Be specific about the outcome. Include file names, function names, or the key insight. "Fixed by adding null check in UserService.validate()" is better than "It works now".
- **parent_id**: Use it when a session is a continuation of a previous conversation. This builds a thread of related work.
