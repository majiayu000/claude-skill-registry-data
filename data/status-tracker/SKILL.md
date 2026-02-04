---
name: status-tracker
description: |
  **AUTO-TRIGGER when user says:** "update progress", "track status", "what's our progress", "generate progress report", "update next steps", "update Notion memory", "create session page"

  Manages TogetherOS progress tracking, Notion memory updates, and status reporting. Updates module progress, manages next steps, syncs to Notion, and maintains session memory.

  Use proactively without asking permission when task matches skill purpose.
---

# TogetherOS Progress & Status Tracking

This skill manages all progress tracking, status updates, and Notion memory for TogetherOS development sessions.

## What This Skill Does

- Updates module progress in `docs/STATUS_v2.md`
- Manages module next steps
- Creates and updates Notion session memory
- Generates progress reports
- Maintains timestamped milestone log
- Triggers `sync-to-main` skill at 5% progress milestones

## Core Files

- **docs/STATUS_v2.md** - Module percentage dashboard (auto-updated via PR markers)
- **STATUS/progress-log.md** - Timestamped milestone log (appended by automation)
- **docs/modules/{module}/** - Individual module docs with Next Steps sections

**See full guide:** `docs/dev/progress-tracking-automation.md`

## Workflow Steps

### 0. Session Memory (Notion) - **RECOMMENDED**

**When:** At session start and end (especially for complex work or yolo1 workflows)

**Flow:**
- **Start:** Create page in "Claude Memory" → `Nov 10, 25 14:30 - Session`
- **During:** Update on achievements/discoveries (continuous, not end-dump)
- **End:** Finalize with summary, rename title with theme
- **Cleanup:** Keep 6 most recent, archive oldest when adding #7

**Quick Start:**
```
Use Notion API: mcp__notion__API-post-page
Parent page ID: 296d133a-246e-80a6-a870-c0d163e9c826
Title: "Nov 10, 25 14:30 - Session"
```

**Format:**
```
# Session: Nov 10, 25 14:30

## Work Completed
- [achievements]
- Example: "Created test page at /test/profiles with component showcase"

## Discoveries
- [findings, decisions, blockers]

## Status
Branch: [name] | Commit: [hash] | Build: [status]

## Next Steps
- [2-3 actions]
```

**At session end, update title:**
```
"Nov 10, 25 14:30 - {module} {feature} implementation"
```

### 1. Progress Tracking During Implementation

**When to Track:**
- After completing a feature or slice
- When a module reaches a milestone
- During PR creation (automatic via marker)
- When user explicitly requests update

**Estimation Guide:**
- **Scaffold/Setup**: +5-10% (foundational structure)
- **Core Feature**: +10-20% (major functionality)
- **Enhancement**: +5-10% (improvements to existing features)
- **Polish/Refine**: +2-5% (UI tweaks, minor fixes)
- **Testing/Docs**: +5% (comprehensive testing or documentation)

### 2. Update Module Next Steps

Use `scripts/update-module-next-steps.sh` to manage tasks:

```bash
# Initialize Next Steps section (if doesn't exist)
./scripts/update-module-next-steps.sh bridge init

# Add new task
./scripts/update-module-next-steps.sh bridge add "Task name"

# Mark task complete
./scripts/update-module-next-steps.sh bridge complete "Task name"

# List all tasks
./scripts/update-module-next-steps.sh bridge list
```

**Best Practice:** Update next steps during implementation as you discover new tasks or complete existing ones.

### 3. Manual Progress Updates (if needed)

Update progress manually when not using PR markers:

```bash
# Set specific percentage
./scripts/update-progress.sh bridge 75 "Completed streaming UI"

# Increment by percentage
./scripts/update-progress.sh bridge +10 "Added citations feature"
```

**Note:** Most updates happen automatically via PR markers. Manual updates are rare.

### 4. PR Progress Markers (Primary Method)

**Always include progress markers in PR body** for automatic tracking:

```markdown
## Progress
progress:bridge=+10
```

**Syntax:**
- `progress:MODULE=XX` - Set to specific percentage (e.g., `progress:auth=75`)
- `progress:MODULE=+XX` - Increment by percentage (e.g., `progress:auth=+15`)

**This triggers `auto-progress-update.yml` GitHub Action on merge** to update both:
- `docs/STATUS_v2.md` (module percentages)
- `STATUS/progress-log.md` (timestamped entry)

### 5. Trigger sync-to-main at Milestones

**When progress reaches 5% milestones** (5%, 10%, 15%, 20%, etc.):

1. **Invoke sync-to-main skill (Phase 1 only)**
   ```
   Use Skill: sync-to-main
   Action: Create WIP marker in main branch
   ```

2. **Skill automatically**:
   - Checks out main branch
   - Updates STATUS_v2.md with 🔄 marker: `- [module] 🔄 XX% - In active development (yolo branch)`
   - Commits and pushes to main
   - Returns to yolo branch

3. **Notify user**:
   ```
   WIP marker created in main for [module] (XX%).
   Contributors will see this module is in active development.

   To sync code after production testing: "sync [module] to main"
   ```

**Note:** This only creates the WIP marker. Actual code sync (Phase 2) happens when user approves after production validation.

### 6. Notion Memory Updates - **RECOMMENDED FOR ALL YOLO1 WORKFLOWS**

**When to Update Notion:**
- **Session start** (create page)
- During implementation (append updates)
- After PR creation
- Major milestone completion
- **Session end** (finalize summary)
- User requests it

**Quick Handoff Page:**
- What we did (3-5 bullets)
- Where we are (branch, commit, status)
- Next steps (2-3 items)
- Keep it minimal: 10-15 lines total, easy to scan

**Detailed Session Pages:**
- Create with date format: `Nov 10, 25 14:30`
- Update continuously during session (not end-dump)
- Keep only 6 most recent
- Archive oldest when adding #7

**Integration with yolo1:**
- Step 0: Create session page at workflow start
- Step 13: Finalize session page after deployment
- See yolo1 skill for exact API call examples

**⚠️ Notion API Version Notice:**
- Current MCP server may use pre-2025-09-03 API version
- Works fine for single-source databases (current setup)
- **Risk**: If "Claude Memory" database gets second data source added, operations will fail
- **Future migration needed**: Switch from `database_id` to `data_source_id` when MCP server updates
- **Monitor**: Check `@modelcontextprotocol/server-notion` for 2025-09-03 API support
- **Reference**: https://developers.notion.com/docs/upgrade-guide-2025-09-03
- **Action**: Document as tech debt if operations fail after Notion workspace changes

### 7. Generate Progress Reports

For comprehensive status overview:

```bash
./scripts/generate-progress-report.sh
```

Outputs:
- Current module percentages
- Recent progress changes
- Completion forecasts
- Blocked/at-risk modules

## Module Progress Keys

From `docs/STATUS_v2.md`:

**Core Modules:**
- scaffold, ui, auth, profiles, groups, forum, governance, social-economy
- reputation, onboarding, search, notifications, docs-hooks
- observability, security

**Path Modules:**
- path-education, path-governance, path-community, path-media
- path-wellbeing, path-economy, path-technology, path-planet

**DevEx:**
- devcontainer, ci-lint, ci-docs, ci-smoke, deploy, secrets

## Automation Details

### Auto-Progress on PR Merge

When a PR with `progress:module=+X` marker merges to `yolo`:
1. GitHub Action `auto-progress-update.yml` triggers
2. Parses progress marker from PR body
3. Updates module percentage in `docs/STATUS_v2.md`
4. Appends timestamped entry to `STATUS/progress-log.md`
5. Commits changes with message: `chore(progress): update {module} progress`

**No manual intervention needed** - progress stays in sync automatically.

### Next Steps Automation

The `update-module-next-steps.sh` script:
- Manages HTML comment markers in module READMEs
- Preserves formatting and indentation
- Handles task completion with strikethrough
- Safe idempotent operations

## Example Usage

### Example 1: Update Progress After Implementation
```
Use Skill: status-tracker
Context: Just completed bridge streaming UI implementation
Action: Update progress for bridge module (+10%), update next steps
```

### Example 2: Create Notion Session Memory
```
Use Skill: status-tracker
Context: Starting new session
Action: Create new session page in Notion with today's date
```

### Example 3: Track Status During PR Creation
```
Use Skill: status-tracker
Context: Creating PR for governance module
Action: Add progress marker to PR body, update next steps
```

## Integration with Other Skills

**With yolo1:**
- yolo1 calls status-tracker after implementation to add progress marker to PR
- yolo1 updates next steps before creating PR

**With pr-formatter:**
- pr-formatter includes progress marker in formatted PR body
- Ensures correct syntax for automation

**With sync-to-main:**
- status-tracker calls sync-to-main Phase 1 when progress hits 5% milestone
- sync-to-main creates WIP marker in main branch
- User later invokes sync-to-main Phase 2 manually for code sync

**Standalone:**
- Check current status: "what's our progress?"
- Update Notion: "update session memory"
- Manual progress update: "mark bridge at 75%"

## Safety Guidelines

1. **Never decrease progress** - Only increment or set higher values
2. **Keep progress realistic** - Small features = 5-10%, major features = 15-20%
3. **Update next steps synchronously** - Do it during implementation, not after
4. **Notion cleanup** - Always maintain exactly 6 session pages
5. **Progress markers must be exact syntax** - `progress:module=+X` (no spaces around `=`)

## Troubleshooting

**Progress not updating on merge?**
- Check PR body has exact syntax: `progress:module=+10`
- Verify module key exists in STATUS_v2.md
- Check GitHub Actions log for errors

**Next steps script fails?**
- Ensure module README exists at `docs/modules/{module}/README.md`
- Run `init` command first if section doesn't exist
- Check HTML comment markers are intact

**Notion updates not working?**
- Verify Notion API connection in MCP settings
- Check "Claude Memory" parent page exists
- Ensure proper permissions for page creation

**Notion UUID validation error?**
- **Symptom**: `"path.block_id should be a valid uuid, instead was \"29fd133a-246e-811db872-eccf65334c38\""`
- **Cause**: Claude Code internal bug (issue #5504) - occasionally corrupts UUIDs by removing one dash
- **Pattern**: Dash removed at position 18 (e.g., `811d-b872` becomes `811db872`)
- **Fix**: Simply retry the operation with the original correct UUID - second attempt usually succeeds
- **Not our bug**: This is a Claude Code serialization issue, not our code or the MCP server
- **Status**: No workaround needed beyond manual retry - track as known issue

## Reference

**Full Documentation:**
- Progress tracking flow: `docs/dev/progress-tracking-automation.md`
- PR checklist (includes progress): `docs/dev/pr-checklist.md`
- Module structure: `docs/modules/README.md`

**Related Skills:**
- **yolo1**: Full implementation workflow (calls this skill)
- **pr-formatter**: PR body formatting (includes progress markers)
- **sync-to-main**: Branch synchronization (called by this skill at 5% milestones)
