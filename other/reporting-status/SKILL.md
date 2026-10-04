---
name: reporting-status
description: Generate situational awareness report showing new memos, recent commits, decisions, questions, and roadmap work since user's last reporting-status. Use when user asks "what's new", "catch me up", "status update", "what did I miss", or "recent activity". ONLY invoke via /wrangler:reporting-status command.
---

You are the reporting-status workflow coordinator. Your job is to surface what's new since the user's last situational report, ensuring they don't evaluate priorities without knowing the latest learnings.

## Primary Value

**Surface new memos that collaborators created** - so you don't evaluate priorities without knowing the latest learnings.

## Skill Usage Announcement

**MANDATORY**: When using this skill, announce it at the start with:

```
🔧 Using Skill: sitrep | Generating situational awareness report
```

---

## Help Flag Handling

**FIRST:** Check if arguments contain `--help` or `help`.

If help flag is present, output this help text and **stop** (do not proceed to workflow):

````
/wrangler:sitrep - Situational Awareness Report

USAGE:
    /wrangler:sitrep [OPTIONS]

DESCRIPTION:
    Generate a "what's new" report showing activity since your last sitrep.
    Surfaces new memos, recent commits, decisions, open questions, and
    roadmap status to keep you informed before evaluating priorities.

    On first run, shows the last 7 days of activity. Subsequent runs show
    only new activity since your last sitrep (incremental updates).

OPTIONS:
    --full     Ignore cursor, show full 7-day report (like first run)
    --help     Show this help message and exit

FILES READ:
    .wrangler/cache/{user}-sitrep.json    Your sitrep cursor state
    .wrangler/memos/*.md                  Memo files for surfacing
    .wrangler/ROADMAP_NEXT_STEPS.md       Roadmap completion status
    .wrangler/issues/*.md                 Issue status (via MCP)

FILES WRITTEN:
    .wrangler/cache/{user}-sitrep.json    Updated cursor after each run

STATE FILE FORMAT:
    {
      "cursor": { "commit": "abc123" },   # Last commit you saw
      "stats": { "runs": 5, ... }         # Cumulative stats
    }

WORKFLOW:
    1. Detect user from git config (email prefix)
    2. Load cursor from state file (or default to 7 days)
    3. Gather data in parallel:
       - Git commits since cursor
       - New memos with decisions/questions
       - Issue and roadmap status
    4. Generate report with:
       - NEW MEMOS (read first!)
       - Recent activity by author
       - Decisions made
       - Open questions
       - Roadmap status & high-priority issues
    5. Update cursor to latest commit

EXAMPLES:
    /wrangler:sitrep              # Incremental: what's new since last run
    /wrangler:sitrep --full       # Full overview: last 7 days
    /wrangler:sitrep --help       # Show this help

SEE ALSO:
    /wrangler:issues              # View issue/spec status
    /wrangler:help                # Full wrangler documentation
````

**After displaying help, STOP.** Do not proceed to the multi-phase workflow.

---

## Multi-Phase Workflow

```
Phase 1: User Detection & State Loading (Sequential)
    ↓
Phase 2: Data Gathering (3 Parallel Subagents)
    ↓
Phase 3: Analysis & Synthesis (Sequential)
    ↓
Phase 4: Report Generation (Sequential)
    ↓
Phase 5: State Update (Sequential)
```

---

## Phase 1: User Detection & State Loading

**Purpose:** Establish identity and load cursor position

### 1.1 Detect User

Run this command to get the user's identity:

```bash
git config user.email
```

Extract username: everything before the `@` symbol.

**Example:** `samjhecht@gmail.com` → `samjhecht`

**Fallback:** If git config fails, use `anonymous` as username.

### 1.2 Load State File

State files are stored in `.wrangler/cache/{username}-reporting-status.json`

**State file format:**
```json
{
  "created_at": "2026-01-10T09:00:00Z",
  "updated_at": "2026-01-15T18:30:00Z",
  "cursor": {
    "commit": "7313e60"
  },
  "stats": {
    "runs": 12,
    "memos_surfaced": 47,
    "decisions_found": 23,
    "questions_found": 8
  }
}
```

### 1.3 Handle Arguments

Check if `--full` flag was passed in arguments:

- **`--full` present:** Ignore cursor, treat as first-run (show last 7 days)
- **No flag:** Use cursor from state file

### 1.4 Handle Edge Cases

| Case | Handling |
|------|----------|
| No state file exists | First-run: show last 7 days, announce "First reporting-status for {username}" |
| `--full` flag | Ignore cursor, treat as first-run |
| State file corrupted/invalid JSON | Delete file, treat as first-run |
| Username detection fails | Fallback to `anonymous` |

### 1.5 Determine Time Range

Based on state and flags, determine:

```
cursor_commit = state.cursor.commit OR null
cursor_date = date of cursor commit OR "7 days ago"
```

**Output from Phase 1:**
- `username` - User identity
- `cursor_commit` - Last commit seen (or null for first-run)
- `cursor_date` - Human-readable start date
- `is_first_run` - Boolean

---

## Phase 2: Data Gathering (Parallel Subagents)

**Why parallel:** Three independent data sources with no dependencies.

Launch **three parallel subagents** using the Task tool in a **single message**:

### Subagent A: Git History Analysis

**Task prompt:**

```
Analyze git history for reporting-status report.

Cursor: {cursor_commit or "7 days ago"}

Commands to run:
- If cursor commit exists:
  git log {cursor_commit}..HEAD --format="%H|%ae|%s|%ai" --no-merges
- If no cursor (first-run):
  git log --since="7 days ago" --format="%H|%ae|%s|%ai" --no-merges

Output needed:
1. Latest commit hash (for new cursor)
2. Commits grouped by author with counts
3. Decisions extracted from commit messages

Decision extraction - look for:
- Messages containing: "decided", "chose", "switched to", "migrated"
- Conventional commits: feat:, fix: (these represent decisions)
- Breaking changes: BREAKING CHANGE

Return JSON format:
{
  "latest_commit": "abc123...",
  "commit_count": 15,
  "authors": [
    {"email": "user@example.com", "count": 5, "representative_messages": ["msg1", "msg2"]}
  ],
  "decisions": [
    {"summary": "Switched to TypeScript", "commit": "abc123", "author": "user@example.com"}
  ]
}
```

---

### Subagent B: Memo Surfacing (CRITICAL)

**Task prompt:**

```
Surface new memos for reporting-status report. This is the MOST IMPORTANT subagent task.

Cursor date: {cursor_date}

Steps:
1. List memos with modification times:
   ls -lt .wrangler/memos/*.md 2>/dev/null || echo "No memos"

2. For each memo newer than cursor date, extract:
   - Title (first H1 heading or filename)
   - 2-3 sentence summary (first paragraph after title)
   - Decisions (look for "## Decision", "we decided", "decided to")
   - Open questions (look for "## Open Questions", "??" in headers, "TBD:", "TODO:")

3. Categorize memos by type based on filename patterns:
   - RCA-*.md → Root Cause Analysis
   - SUMMARY-*.md → Summary/Recap
   - ANALYSIS-*.md → Analysis
   - DECISION-*.md → Decision Record
   - Other → General memo

Return JSON format:
{
  "new_memos": [
    {
      "filename": "2026-01-15-auth-failure-rca.md",
      "title": "Authentication Failure Root Cause",
      "type": "RCA",
      "date": "2026-01-15",
      "summary": "JWT validation was failing due to clock skew...",
      "decisions": ["Switched to asymmetric JWT verification"],
      "questions": ["Should we add clock tolerance?"]
    }
  ],
  "decisions_from_memos": [...],
  "open_questions": [...]
}

If no memos directory or no new memos, return:
{
  "new_memos": [],
  "decisions_from_memos": [],
  "open_questions": [],
  "note": "No memos in workspace" OR "No new memos since cursor"
}
```

---

### Subagent C: Issue & Roadmap Status

**Task prompt:**

```
Gather issue and roadmap status for reporting-status report.

Use MCP tools to query:
1. issues_list({ status: ["open"] }) - Count open issues
2. issues_list({ status: ["in_progress"] }) - Count in-progress issues
3. issues_list({ priority: ["critical", "high"], status: ["open"] }) - High-priority open items

Read roadmap file:
- .wrangler/ROADMAP_NEXT_STEPS.md - Extract current phase and completion %

Return JSON format:
{
  "issues": {
    "open_count": 5,
    "in_progress_count": 3,
    "high_priority_open": [
      {"id": "000001", "title": "Fix auth bug", "priority": "critical"}
    ]
  },
  "roadmap": {
    "current_phase": "Phase 2: Core Features",
    "completion_pct": 65,
    "note": "Extracted from ROADMAP_NEXT_STEPS.md"
  }
}

If no issues or roadmap file:
{
  "issues": {"open_count": 0, "in_progress_count": 0, "high_priority_open": []},
  "roadmap": {"current_phase": "Unknown", "completion_pct": null, "note": "No roadmap file found"}
}
```

---

### Parallel Execution

**CRITICAL:** All three Task tool calls must be in a **single message** to execute truly in parallel.

```
I'm launching three parallel reporting-status data gathering agents:

[Task tool - Subagent A: Git History Analysis]
[Task tool - Subagent B: Memo Surfacing]
[Task tool - Subagent C: Issue & Roadmap Status]

All three agents are now running in parallel...
```

---

## Phase 3: Analysis & Synthesis

**Why sequential:** Needs results from all Phase 2 subagents.

### 3.1 Aggregate Results

Collect and parse JSON results from all three subagents.

### 3.2 Deduplicate Decisions

Decisions may appear in both commits and memos. Deduplicate by:
1. Normalize decision text (lowercase, strip punctuation)
2. Check for similar decisions (fuzzy match)
3. Keep one entry, note source as "commit and memo" if both

### 3.3 Priority Re-evaluation Heuristics

Analyze new information for priority implications:

| Trigger | Suggested Change |
|---------|------------------|
| New RCA memo about component X | Related issues → higher priority |
| Specification closed | Child issues → review for obsolescence |
| Critical bug in recent commits | Related issues → may be blocked |
| Decision changes architecture | Related issues → may need update |

**Important:** Sitrep SUGGESTS priority changes. Human decides.

### 3.4 Calculate Stats

For state file update:
```
new_memos_count = len(new_memos)
decisions_count = len(deduplicated_decisions)
questions_count = len(open_questions)
```

---

## Phase 4: Report Generation

**Read `templates/report.md`** for the full report template and variable reference.

Generate the reporting-status report by:
1. Reading the template from `templates/report.md`
2. Substituting all variables with data from Phases 1-3
3. Outputting the formatted markdown report

### Priority Emoji Mapping (Quick Reference)

| Priority | Emoji |
|----------|-------|
| `critical` | 🔴 |
| `high` | 🟠 |
| `medium` | 🟡 |
| `low` | 🟢 |

---

## Phase 5: State Update

### 5.1 Ensure Cache Directory Exists

```bash
mkdir -p .wrangler/cache
```

### 5.2 Write Updated State File

Write to `.wrangler/cache/{username}-reporting-status.json`:

```json
{
  "created_at": "{original_created_at OR now if first run}",
  "updated_at": "{now ISO8601}",
  "cursor": {
    "commit": "{latest_commit_hash from Subagent A}"
  },
  "stats": {
    "runs": {previous_runs + 1},
    "memos_surfaced": {previous + new_memos_count},
    "decisions_found": {previous + decisions_count},
    "questions_found": {previous + questions_count}
  }
}
```

### 5.3 Confirm State Saved

Announce: "Sitrep state saved. Next reporting-status will start from commit {latest_commit_hash}."

---

## Edge Cases

| Case | Handling |
|------|----------|
| No git repo | Skip git analysis, warn user, continue with memos/issues |
| No memos directory | "No memos in workspace" in report |
| No .wrangler directory | "Wrangler not initialized - run session-start hook" |
| No issues | "No issues tracked yet" |
| Cursor commit rebased away | `git log {cursor}..HEAD` will fail; fall back to last 30 days |
| Empty workspace | Generate report with all "No new..." messages |
| Subagent fails | Report partial data, note which source failed |

### Handling Rebased Cursor

If git log with cursor fails:

```bash
# Check if cursor commit exists
git cat-file -t {cursor_commit} 2>/dev/null
```

If not found:
1. Log warning: "Previous cursor commit not found (rebased?)"
2. Fall back to: `git log --since="30 days ago"`
3. Note in report: "Using 30-day fallback due to rebased history"

---

## Verification Checklist

After implementation, verify these scenarios work:

1. **First-run:** No state file → shows 7 days, creates state file
2. **Incremental:** Add memo, run reporting-status → only new memo appears
3. **--full flag:** Ignores cursor, shows everything
4. **Multi-user:** Switch git user → separate state files
5. **Decision extraction:** Memo with `## Decision` → appears in report
6. **Empty workspace:** No errors, graceful messages
7. **State persistence:** Run twice → second run shows "since" first run's cursor

---

## Important Notes

### Read-Only Operations

This skill is **read-only** for governance files:
- Does NOT invoke refreshing-metrics
- Does NOT update roadmap files
- Does NOT modify issues

Only writes to: `.wrangler/cache/{username}-reporting-status.json`

### Subagent Types

When launching parallel subagents, use:
- `subagent_type: "Explore"` for Subagent A (git analysis) and Subagent B (memo surfacing)
- `subagent_type: "general-purpose"` for Subagent C (uses MCP tools)

### Model Selection

For efficiency, subagents can use `model: "haiku"` since tasks are straightforward data gathering.

---

## Usage Examples

### Example 1: First Sitrep on Project

**User:** `/wrangler:reporting-status`

**Agent Response:**
1. "First reporting-status for samjhecht - showing last 7 days..."
2. Launches 3 parallel subagents
3. Generates report with all activity from past week
4. Creates state file with current cursor

### Example 2: Daily Check-in

**User:** `/wrangler:reporting-status`

**Agent Response:**
1. "Loading reporting-status state from 2 days ago..."
2. Launches 3 parallel subagents (filtered to since cursor)
3. "2 new memos since last reporting-status!"
4. Generates focused report
5. Updates state file

### Example 3: Full Overview

**User:** `/wrangler:reporting-status --full`

**Agent Response:**
1. "Full reporting-status requested - ignoring cursor, showing last 7 days..."
2. Same as first-run flow
3. Updates cursor but doesn't reset stats

---

## Success Criteria

Sitrep is successful when:

- [ ] User identity detected or gracefully defaulted
- [ ] State file loaded or first-run handled
- [ ] All 3 subagents launched in parallel
- [ ] New memos prominently surfaced
- [ ] Decisions extracted and deduplicated
- [ ] Open questions listed
- [ ] Roadmap status shown
- [ ] Priority re-evaluation suggestions provided if applicable
- [ ] State file updated with new cursor
- [ ] Report is concise and actionable

---

## Related Skills

- **housekeeping** - Uses similar multi-phase parallel subagent pattern
- **refreshing-metrics** - Reference for MCP tool usage patterns
- **issues-housekeeper** - Validates project state (reporting-status is read-only complement)
