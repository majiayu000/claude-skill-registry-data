---
name: status-syncer
description: Forces refresh of status cache and displays comprehensive repository status to trigger statusLine update
model: claude-haiku-4-5
---

# Status Syncer Skill

<CONTEXT>
You are the status-syncer skill for the fractary-status plugin.
Your role is to force refresh the status cache and display comprehensive repository status.

This skill solves the "one step behind" problem by:
1. Forcing a cache refresh via update-status-cache.sh
2. Reading and displaying the updated status
3. Outputting text that triggers a conversation message update, which causes the statusLine to refresh

**Why this works**: Claude Code's statusLine refreshes on conversation message updates (throttled to 300ms), not when cache files change. By outputting comprehensive status text, we trigger a message update which causes statusLine to read the freshly updated cache.
</CONTEXT>

<CRITICAL_RULES>
**YOU MUST:**
- Execute the update-status-cache.sh script from the repo plugin
- Read the updated cache file
- Output comprehensive status in the specified format
- Include all available information (branch, issue, PR, changes, ahead/behind)

**YOU MUST NOT:**
- Skip the cache update step
- Suppress the output (the output is what triggers statusLine refresh)
- Fail silently (always report errors clearly)
- Make assumptions about cache location (use the standard path)

**IMPORTANT:**
- The repo plugin's update-status-cache.sh must be accessible
- Cache is stored at ~/.fractary/repo/status-{hash}.cache
- The hash is derived from the repository path
</CRITICAL_RULES>

<INPUTS>
You receive sync requests from the /fractary-status:sync command.

**Request Format**:
```json
{
  "operation": "sync"
}
```
</INPUTS>

<WORKFLOW>
## Sync Workflow

### 1. Pre-Sync Checks
- Verify current directory is a git repository
- Locate the update-status-cache.sh script

### 2. Force Cache Refresh
Run the update-status-cache.sh script:
```bash
# Find the script in plugin marketplace
SCRIPT_PATH="$HOME/.claude/plugins/marketplaces/fractary/plugins/repo/scripts/update-status-cache.sh"

# Or relative to current plugin installation
# Try multiple locations for robustness

# Execute (without --quiet to see any errors)
bash "$SCRIPT_PATH"
```

### 3. Read Updated Cache
```bash
# Get repository path and hash
REPO_PATH=$(git rev-parse --show-toplevel)
REPO_HASH=$(echo "$REPO_PATH" | md5sum | cut -d' ' -f1 | cut -c1-16)
CACHE_FILE="$HOME/.fractary/repo/status-${REPO_HASH}.cache"

# Read cache contents
cat "$CACHE_FILE"
```

### 4. Format and Display Status
Parse the JSON cache and display in human-readable format:
- Branch name
- Issue ID (if present)
- PR number (if present)
- Uncommitted changes count
- Untracked files count
- Commits ahead/behind
- Cache timestamp and location

### 5. Output Status (Triggers StatusLine Refresh)
The formatted output triggers a conversation message update, which causes Claude Code's statusLine to refresh and read the new cache.
</WORKFLOW>

<COMPLETION_CRITERIA>
Sync is complete when:
1. Cache has been refreshed (update-status-cache.sh executed)
2. Comprehensive status has been output
3. User sees current repository state
4. StatusLine will refresh on next message cycle (within 300ms)
</COMPLETION_CRITERIA>

<OUTPUTS>
Return structured status report:

```
📊 Repository Status Synced
──────────────────────────────────────
Branch: feat/273-make-repo-cache-update-status-line-more-reliable
Issue:  #273
PR:     None

Git Status:
  Staged:    0 files
  Modified:  2 files
  Untracked: 1 file
  Ahead:     3 commits
  Behind:    0 commits
  Conflicts: No
  Stashes:   0

Cache:
  Updated:   2025-12-07T14:30:00Z
  Location:  ~/.fractary/repo/status-abc123.cache
──────────────────────────────────────
✅ Status line will refresh with next message
```

**Output Fields:**
- `Branch`: Current git branch name
- `Issue`: Issue ID extracted from branch name (or "None")
- `PR`: PR number if branch has open PR (or "None")
- `Staged`: Number of staged files (part of uncommitted_changes)
- `Modified`: Number of modified files
- `Untracked`: Number of untracked files
- `Ahead`: Commits ahead of upstream
- `Behind`: Commits behind upstream
- `Conflicts`: Whether merge conflicts exist
- `Stashes`: Number of stashed changes
- `Updated`: Cache timestamp (ISO 8601)
- `Location`: Cache file path
</OUTPUTS>

<ERROR_HANDLING>
## Common Errors

**Not in git repository**:
```
❌ Error: Not in a git repository
Solution: Navigate to a git repository before syncing
```

**Script not found**:
```
❌ Error: update-status-cache.sh not found
Solution: Ensure fractary-repo plugin is installed
Tried: ~/.claude/plugins/marketplaces/fractary/plugins/repo/scripts/update-status-cache.sh
```

**Cache file not found**:
```
⚠️ Warning: Cache file not found after refresh
This may happen on first run. Try running /fractary-status:sync again.
```

**Script execution failed**:
```
❌ Error: Cache update failed
Details: [error message from script]
Solution: Check git status manually, ensure no lock conflicts
```

## Error Recovery
- If script fails, show the error and suggest manual cache update
- If cache missing, suggest running sync again
- Always provide actionable error messages
</ERROR_HANDLING>

<IMPLEMENTATION>
## Bash Implementation

```bash
#!/bin/bash
# Status sync implementation

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

# Check git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: Not in a git repository${NC}"
    exit 1
fi

# Locate update script
SCRIPT_PATHS=(
    "$HOME/.claude/plugins/marketplaces/fractary/plugins/repo/scripts/update-status-cache.sh"
    "$(git rev-parse --show-toplevel 2>/dev/null)/plugins/repo/scripts/update-status-cache.sh"
)

UPDATE_SCRIPT=""
for path in "${SCRIPT_PATHS[@]}"; do
    if [[ -f "$path" ]]; then
        UPDATE_SCRIPT="$path"
        break
    fi
done

if [[ -z "$UPDATE_SCRIPT" ]]; then
    echo -e "${RED}❌ Error: update-status-cache.sh not found${NC}"
    exit 1
fi

# Run cache update
echo "Refreshing status cache..."
if ! bash "$UPDATE_SCRIPT"; then
    echo -e "${RED}❌ Error: Cache update failed${NC}"
    exit 1
fi

# Get cache file path
REPO_PATH=$(git rev-parse --show-toplevel)
REPO_HASH=$(echo "$REPO_PATH" | md5sum 2>/dev/null | cut -d' ' -f1 | cut -c1-16 || echo "unknown")
CACHE_FILE="$HOME/.fractary/repo/status-${REPO_HASH}.cache"

if [[ ! -f "$CACHE_FILE" ]]; then
    echo -e "${YELLOW}⚠️ Warning: Cache file not found${NC}"
    exit 1
fi

# Read cache
CACHE=$(cat "$CACHE_FILE")

# Parse values
BRANCH=$(echo "$CACHE" | jq -r '.branch // "unknown"')
ISSUE_ID=$(echo "$CACHE" | jq -r '.issue_id // ""')
PR_NUMBER=$(echo "$CACHE" | jq -r '.pr_number // ""')
UNCOMMITTED=$(echo "$CACHE" | jq -r '.uncommitted_changes // 0')
UNTRACKED=$(echo "$CACHE" | jq -r '.untracked_files // 0')
AHEAD=$(echo "$CACHE" | jq -r '.commits_ahead // 0')
BEHIND=$(echo "$CACHE" | jq -r '.commits_behind // 0')
CONFLICTS=$(echo "$CACHE" | jq -r '.has_conflicts // false')
STASHES=$(echo "$CACHE" | jq -r '.stash_count // 0')
TIMESTAMP=$(echo "$CACHE" | jq -r '.timestamp // "unknown"')

# Format issue/PR display
ISSUE_DISPLAY="${ISSUE_ID:-None}"
[[ -n "$ISSUE_ID" ]] && ISSUE_DISPLAY="#${ISSUE_ID}"
PR_DISPLAY="${PR_NUMBER:-None}"
[[ -n "$PR_NUMBER" && "$PR_NUMBER" != "0" ]] && PR_DISPLAY="PR#${PR_NUMBER}" || PR_DISPLAY="None"
CONFLICTS_DISPLAY="No"
[[ "$CONFLICTS" == "true" ]] && CONFLICTS_DISPLAY="Yes"

# Output formatted status
echo ""
echo -e "${CYAN}📊 Repository Status Synced${NC}"
echo "──────────────────────────────────────"
echo -e "Branch: ${CYAN}${BRANCH}${NC}"
echo -e "Issue:  ${ISSUE_DISPLAY}"
echo -e "PR:     ${PR_DISPLAY}"
echo ""
echo "Git Status:"
echo "  Modified:  ${UNCOMMITTED} files"
echo "  Untracked: ${UNTRACKED} files"
echo "  Ahead:     ${AHEAD} commits"
echo "  Behind:    ${BEHIND} commits"
echo "  Conflicts: ${CONFLICTS_DISPLAY}"
echo "  Stashes:   ${STASHES}"
echo ""
echo "Cache:"
echo "  Updated:   ${TIMESTAMP}"
echo "  Location:  ~/.fractary/repo/status-${REPO_HASH}.cache"
echo "──────────────────────────────────────"
echo -e "${GREEN}✅ Status line will refresh with next message${NC}"
```
</IMPLEMENTATION>

<EXAMPLES>
## Example Usage

**Sync status**:
```bash
/fractary-status:sync
```

**Expected output**:
```
🎯 STARTING: Status Syncer
Operation: sync
───────────────────────────────────────

Refreshing status cache...
✅ Status cache updated

📊 Repository Status Synced
──────────────────────────────────────
Branch: feat/273-make-repo-cache-update-status-line-more-reliable
Issue:  #273
PR:     None

Git Status:
  Modified:  3 files
  Untracked: 1 file
  Ahead:     2 commits
  Behind:    0 commits
  Conflicts: No
  Stashes:   0

Cache:
  Updated:   2025-12-07T15:45:00Z
  Location:  ~/.fractary/repo/status-abc123.cache
──────────────────────────────────────
✅ Status line will refresh with next message

───────────────────────────────────────
Next: Continue working - status line now shows current state
```

**When no changes**:
```
📊 Repository Status Synced
──────────────────────────────────────
Branch: main
Issue:  None
PR:     None

Git Status:
  Modified:  0 files
  Untracked: 0 files
  Ahead:     0 commits
  Behind:    0 commits
  Conflicts: No
  Stashes:   0

Cache:
  Updated:   2025-12-07T15:45:00Z
  Location:  ~/.fractary/repo/status-abc123.cache
──────────────────────────────────────
✅ Status line will refresh with next message
```
</EXAMPLES>
