---
name: diary
description: Development diary automation for KStoryBridge. This skill should be used when capturing development session insights, generating daily diary entries from Claude Code history and git commits, or managing entries for the public development diary at kstorybridge.com/diary.
---

# Development Diary Skill

Automates the creation and management of development diary entries for KStoryBridge, capturing work sessions from Claude Code history and git commits.

## When to Use This Skill

- At the end of a development session to generate a diary entry
- During sessions to capture important insights or decisions
- To take screenshots of completed features for the diary
- To check diary status and recent entries

## Automated Daily Generation

The diary is automatically generated **daily at 4:00 AM PST** for the previous day's work.

**How it works:**
- A macOS LaunchAgent (`com.kstorybridge.daily-diary`) runs `scripts/daily-diary.sh`
- Collects Claude Code history from `~/.claude/history.jsonl`
- Analyzes git commits from the KStoryBridge repo
- Generates and publishes entry directly to `marketing/development_diary/published/`

**Manage the schedule:**
```bash
# Check if running
launchctl list | grep kstorybridge

# Stop the scheduled job
launchctl unload ~/Library/LaunchAgents/com.kstorybridge.daily-diary.plist

# Start the scheduled job
launchctl load ~/Library/LaunchAgents/com.kstorybridge.daily-diary.plist

# Run manually for a specific date
.claude/skills/diary/scripts/daily-diary.sh 2026-01-25

# View logs
tail -f marketing/development_diary/logs/daily-diary.log
```

**Files:**
- Script: `.claude/skills/diary/scripts/daily-diary.sh`
- LaunchAgent: `~/Library/LaunchAgents/com.kstorybridge.daily-diary.plist`
- Config: `.claude/skills/diary/config.env`
- Logs: `marketing/development_diary/logs/`

### Slack Notifications

When configured, the daily diary sends a rich Slack notification with:
- Date and highlight
- Daily summary
- Session/commit stats
- Link to view on web

**Setup:**
```bash
# Create config file from example
cp .claude/skills/diary/config.env.example .claude/skills/diary/config.env

# Edit and add your Slack webhook URL
# Get one from: https://api.slack.com/messaging/webhooks
```

The Slack message includes:
- Header with date
- Highlight of the day's work
- Summary paragraph
- Stats (sessions, commits, categories)
- Button link to web view

## Commands

### Generate Entry

Generate a diary entry for today or a specific date.

```
/diary generate                    # Generate today's entry
/diary generate --date=2026-01-08  # Generate for specific date
/diary generate --screenshot       # Include screenshot capture
```

### Add Insight

Capture an insight or decision during a session.

```
/diary add "insight text"
/diary add --category=decision "Chose confidence threshold of 0.7"
/diary add --category=learning "Edge function timeout at 25s for large payloads"
```

Categories: `decision`, `learning`, `insight`, `todo`

### Capture Screenshot

Take a screenshot of current app state.

```
/diary screenshot                           # Auto-named
/diary screenshot --name="quality-preview"  # Custom name
/diary screenshot --url=http://localhost:8081/some-page
```

### Manage Entries

```
/diary list                    # List recent entries
/diary status                  # Show today's progress
```

## Generation Workflow

When `/diary generate` is invoked:

### Date Determination

First, determine the target date for the entry:

1. **If user specified `--date=YYYY-MM-DD`:** Use that date (e.g., `/diary generate --date=2026-01-08` → use `2026-01-08`)
2. **If no date specified:** Use today's date in `YYYY-MM-DD` format

Store this as the `TARGET_DATE` to use in all subsequent steps.

### Step 1: Collect Claude Code History

Run `scripts/collect_history.py` to parse `~/.claude/history.jsonl`:

```bash
python3 .claude/skills/diary/scripts/collect_history.py --date={TARGET_DATE}
```

This extracts:
- User prompts from sessions for the KStoryBridge project
- Timestamps and session IDs
- Groupings by session

### Step 2: Analyze Git Commits

Run `scripts/analyze_commits.py` to get git activity:

```bash
python3 .claude/skills/diary/scripts/analyze_commits.py --date={TARGET_DATE}
```

This extracts:
- Commit messages and timestamps
- Files changed (names only, no code)
- Lines added/deleted statistics
- Auto-categorization based on commit messages

### Step 3: Correlate and Categorize

Match prompts with commits by timestamp proximity. Categorize all activities using these keywords:

| Category | Keywords |
|----------|----------|
| Research | research, investigate, explore, analyze, study, compare |
| Planning | plan, design, architect, structure, decide, spec |
| Implementation | implement, create, add, build, develop, feature |
| Bug Fix | fix, bug, issue, error, crash, resolve, debug |
| Refactoring | refactor, cleanup, reorganize, simplify, improve |
| Documentation | doc, document, readme, update docs |
| Testing | test, e2e, playwright, unit test, coverage |

### Step 4: Load Manual Insights

Check for insights added during the day via `/diary add`:

```
marketing/development_diary/drafts/.insights-{TARGET_DATE}.json
```

### Step 5: Capture Screenshots (if --screenshot)

Use Playwright MCP to capture current app state:

```
mcp__plugin_playwright_playwright__browser_navigate
mcp__plugin_playwright_playwright__browser_take_screenshot
```

Save to: `marketing/development_diary/screenshots/{TARGET_DATE}/`

### Step 6: Generate Entry

Use the template at `marketing/development_diary/templates/daily-entry.md` to generate a complete entry with:

- YAML frontmatter (date, status, categories, etc.)
- Daily summary (2-3 sentences)
- Work sessions with timestamps
- Categorized activity lists
- Screenshots with captions
- Statistics table
- Tomorrow's focus section

### Step 7: Publish Entry

Write directly to: `marketing/development_diary/published/YYYY/MM/{TARGET_DATE}.md`

Create the directory structure (`published/YYYY/MM/`) if it doesn't exist. Set `status: published` in the frontmatter.

## Privacy Guidelines

**DO NOT include in entries:**
- Actual code snippets
- API keys, secrets, or credentials
- Internal business logic details
- User data or PII

**DO include:**
- Feature names and descriptions
- File counts and change statistics
- High-level architectural decisions
- Public-facing UI screenshots

## Output Locations

| Type | Path |
|------|------|
| Published | `marketing/development_diary/published/YYYY/MM/YYYY-MM-DD.md` |
| Screenshots | `marketing/development_diary/screenshots/YYYY-MM-DD/` |
| Insights | `marketing/development_diary/drafts/.insights-YYYY-MM-DD.json` |

## Web Dashboard

- Public: `kstorybridge.com/diary`
- Admin: `kstorybridge.com/marketing/diary`

## Example Generated Entry

```markdown
---
date: 2026-01-09
status: published
author: Sung Ho Lee
session_count: 3
commit_count: 7
categories: [Implementation, Bug Fix, Documentation]
highlight: "Shipped quality assessment feature for AI design generation"
tags: [ai-design, quality, gemini]
---

# Development Diary - January 9, 2026

## Daily Summary

Focused on implementing quality assessment for AI-generated designs. Added server-side validation to catch hallucinations before returning results to users. Also fixed a background removal edge case and updated documentation.

---

## Work Sessions

### Session 1: Morning Research (8:00 AM - 10:30 AM)

**Focus:** Quality Assessment Research

Activities:
- Researched Gemini image generation hallucination patterns
- Analyzed existing design results for failure modes

**Key Prompts:**
- "Research Gemini hallucination patterns for image generation"
- "What quality checks can we add to detect bad generations?"

---

### Session 2: Implementation (11:00 AM - 3:00 PM)

**Focus:** Quality Service Implementation

Activities:
- Created quality service for assessing generated designs
- Added database migration for quality tracking
- Integrated quality checks into design generation flow

**Files Changed:** 5 files (+342/-28 lines)

---

## Categorized Work

### Implementation
- Quality service for design assessment
- Database migration for quality tracking

### Bug Fix
- Fixed background removal edge case for transparent images

### Documentation
- Updated CLAUDE.md with quality service documentation

---

## Screenshots

![Quality Preview](/marketing/development_diary/screenshots/2026-01-09/quality-preview.png)
*Quality assessment UI showing confidence scores*

---

## Insights & Learnings

> **Decision:** Chose to implement retry logic on client side rather than server to reduce Gemini API costs.

> **Learning:** Background removal API fails silently on very low contrast images.

---

## Statistics

| Metric | Value |
|--------|-------|
| Sessions | 3 |
| Commits | 7 |
| Files Changed | 12 |
| Lines Added | 487 |
| Lines Deleted | 56 |
| Primary Category | Implementation |

---

## Tomorrow's Focus

- Complete quality service integration tests
- Deploy to staging for user testing

---

*Generated with KStoryBridge Development Diary*
```

## Related Skills

- `/deploy-staging` - Often used together after implementation sessions
- `/health-check` - Verify system health after deployments
- `/cost-report` - Track API costs mentioned in diary entries
