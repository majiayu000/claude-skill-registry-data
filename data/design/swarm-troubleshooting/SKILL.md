---
name: swarm-troubleshooting
description: Diagnostic and recovery guidance for swarm coordination issues. Use this skill when you encounter 'spawn failed', need to 'diagnose team', 'fix swarm', resolve 'status mismatch', perform 'recovery', troubleshoot kitty/tmux issues, or deal with session crashes, multiplexer problems, or teammate failures. Covers diagnostics, spawn failures, status mismatches, recovery procedures, and common error patterns.
---

# Swarm Troubleshooting

This skill provides comprehensive diagnostic and recovery procedures for swarm coordination issues.

## Quick Troubleshooting Examples

### Example 1: Spawn Failure

```bash
# You try to spawn a teammate
/claude-swarm:swarm-spawn "backend-dev" "backend-developer" "sonnet" "..."
# Error: Could not find a valid kitty socket

# 1. Run diagnostics to identify the issue
/claude-swarm:swarm-diagnose my-team

# Output shows: kitty socket not found at expected location

# 2. Check kitty config
grep -E 'allow_remote_control|listen_on' ~/.config/kitty/kitty.conf

# 3. Fix: Add to kitty.conf if missing
# allow_remote_control yes
# listen_on unix:/tmp/kitty-$USER

# 4. Restart kitty completely and retry spawn
```

### Example 2: Teammate Appears Active But Isn't Responding

```bash
# 1. Check if teammates are actually alive
/claude-swarm:swarm-verify my-team
# Output: backend-dev: not found (session crashed)

# 2. Find status mismatches
/claude-swarm:swarm-reconcile my-team
# Output: backend-dev marked active but session missing - recommend removal

# 3. Resume the team (respawns offline members)
/claude-swarm:swarm-resume my-team
```

### Example 3: Status Mismatch After System Restart

```bash
# After rebooting, team config shows active but all sessions are gone

# 1. Check current state
/claude-swarm:swarm-status my-team
# Shows: 3 members active, but multiplexer shows no sessions

# 2. Reconcile to auto-detect mismatches
/claude-swarm:swarm-reconcile my-team --auto-fix
# Automatically marks offline sessions as inactive

# 3. Resume team to respawn all members
/claude-swarm:swarm-resume my-team
```

**Quick diagnostic rule**: Always start with `/claude-swarm:swarm-diagnose <team>` - it runs all health checks and points you to the specific issue.

## Troubleshooting Delegated Teams

When using delegation mode (default), a spawned team-lead handles coordination. This affects how you troubleshoot.

### Who Diagnoses What?

| Issue Type | Who Should Diagnose | Commands |
|------------|---------------------|----------|
| Team-lead unresponsive | You (orchestrator) | `/swarm-diagnose`, `/swarm-status` |
| Worker issues | Team-lead (first), then you | Ask team-lead to run `/swarm-diagnose` |
| Communication failures | Team-lead (first) | Ask team-lead to check and report |
| Task management issues | Team-lead | Team-lead manages tasks |

### Diagnosing When Team-Lead Is Active

If team-lead is working, ask them to diagnose:

```bash
/claude-swarm:swarm-message team-lead "Please run /swarm-diagnose and report any issues"

# Or be more specific:
/claude-swarm:swarm-message team-lead "Worker backend-dev seems stuck. Can you verify they're alive and check their status?"
```

**Why delegate diagnosis?** Team-lead has full context of the team state and can both diagnose and fix issues directly.

### Diagnosing When Team-Lead Is Unresponsive

If team-lead isn't responding, diagnose directly:

```bash
# 1. Check team status
/claude-swarm:swarm-status my-team

# 2. Is team-lead alive?
# Look for "team-lead" in status output - does window exist?

# 3. Run full diagnostics
/claude-swarm:swarm-diagnose my-team

# 4. If team-lead crashed, respawn them
/claude-swarm:swarm-reconcile my-team
/claude-swarm:swarm-spawn "team-lead" "team-lead" "sonnet" "You are the team-lead. Check /swarm-inbox for context. Resume coordination."
```

### When to Intervene Directly

Intervene yourself when:
- Team-lead is unresponsive or crashed
- Multiple workers are down and team-lead isn't handling it
- Critical issue needs immediate resolution
- You need to see raw status (not team-lead's summary)

Let team-lead handle when:
- Individual worker issues (they can respawn)
- Task reassignment (that's their job)
- Communication failures between workers
- Normal operational issues

### Direct Intervention Commands

```bash
# View raw team state (bypassing team-lead)
/claude-swarm:swarm-status my-team
/claude-swarm:task-list

# Diagnose directly
/claude-swarm:swarm-diagnose my-team

# Message workers directly (if team-lead down)
/claude-swarm:swarm-message backend-dev "Team-lead is unresponsive. What's your current status?"

# Broadcast to all (emergency)
/claude-swarm:swarm-broadcast "Team-lead is down. Please pause work and report status."
```

## Diagnostic Approach

### When Things Go Wrong

Swarm coordination involves multiple moving parts: multiplexers (tmux/kitty), Claude Code processes, file system state, and network communication. When issues arise, systematic diagnosis is essential.

**First, identify the symptom category**:

1. **Spawn Issues** - Can't create new teammates
2. **Status Issues** - Config doesn't match reality
3. **Communication Issues** - Messages not delivered
4. **Task Issues** - Task updates fail
5. **Performance Issues** - Slow response, high resource usage

### Diagnostic Commands

Always start with diagnostics before attempting fixes:

```bash
# Comprehensive health check - runs all diagnostics
/claude-swarm:swarm-diagnose <team-name>

# Check if teammates are actually alive
/claude-swarm:swarm-verify <team-name>

# Find and report status mismatches
/claude-swarm:swarm-reconcile <team-name>

# View current team state (members, tasks, multiplexer)
/claude-swarm:swarm-status <team-name>
```

**What these commands check**:

- **swarm-diagnose**: Multiplexer availability, socket connectivity, config validity, file permissions, session health
- **swarm-verify**: Compares config against live sessions, reports dead/zombie processes
- **swarm-reconcile**: Identifies offline sessions marked active, suggests cleanup actions
- **swarm-status**: Shows current state snapshot - use for quick health check

### Diagnostic Decision Tree

````
Issue Detected
│
├─ Can't spawn teammates?
│  └─ Run: /claude-swarm:swarm-diagnose <team>
│     ├─ "Multiplexer not found" → Install tmux/kitty
│     ├─ "Socket not found" → Check kitty config, restart kitty
│     ├─ "Duplicate name" → Use unique name or check existing teammates
│     └─ "Timeout" → Check system resources, retry
│
├─ Status shows teammates but they're not responding?
│  └─ Run: /claude-swarm:swarm-verify <team>
│     └─ Shows "not found" → Sessions crashed
│        └─ Run: /claude-swarm:swarm-reconcile <team>
│           └─ Then: /claude-swarm:swarm-resume <team>
│
├─ Messages not being received?
│  └─ Check: /claude-swarm:swarm-status <team>
│     ├─ Teammate shows "offline" → Respawn teammate
│     ├─ Wrong agent name used → Check exact names
│     └─ Teammate not checking inbox → Send reminder
│
└─ Task commands failing?
   └─ Run: /claude-swarm:task-list
      └─ Verify task ID exists, check status values

## Common Issues

### Spawn Failures

Spawn failures are the most common issue when creating swarm teams. Understanding the spawn process helps diagnose failures quickly.

**How spawning works**:
1. Validate team name and agent name (no path traversal, special chars)
2. Detect multiplexer (kitty or tmux)
3. For kitty: Find valid socket, create window with environment variables
4. For tmux: Create new session with environment variables
5. Launch Claude Code process with model and initial prompt
6. Register window/session and update config
7. Wait for Claude Code to become responsive

**Symptoms of spawn failure**:
- `spawn_teammate` or `/claude-swarm:swarm-spawn` returns error
- Error messages about multiplexer not found
- Session/window creation fails
- Timeout waiting for teammate to start
- Process starts but immediately crashes

**Immediate diagnostic steps**:

1. **Check error output** - The error message usually indicates root cause
2. **Run diagnostics**:
```bash
/claude-swarm:swarm-diagnose <team-name>
````

3. **Check system state**:

```bash
# For kitty users
kitten @ ls  # Should list windows without error

# For tmux users
tmux list-sessions  # Should list sessions without error

# Check Claude Code is working
claude --version  # Should show version number
```

**Troubleshooting workflow**:

```
Spawn Command Fails
│
├─ Error mentions "multiplexer"?
│  └─ YES → See "Multiplexer Not Available" below
│
├─ Error mentions "socket"?
│  └─ YES → See "Kitty Socket Issues" below
│
├─ Error mentions "duplicate" or "already exists"?
│  └─ YES → See "Duplicate Agent Names" below
│
├─ Error mentions "timeout"?
│  └─ YES → See "Session Creation Timeout" below
│
├─ Error mentions "invalid" or "path traversal"?
│  └─ YES → See "Path Traversal Validation" below
│
└─ No clear error but spawn fails silently?
   └─ Check: System resources, permissions, Claude Code installation
```

**Common Causes:**

#### 1. Multiplexer Not Available

**Error:**

```
Error: Neither tmux nor kitty is available
```

**Solution:**

```bash
# Install tmux (macOS)
brew install tmux

# Or install kitty
brew install --cask kitty

# Verify installation
which tmux  # or: which kitty
```

#### 2. Duplicate Agent Names

**Error:**

```
Error: Agent name 'backend-dev' already exists in team
```

**Solution:**

```bash
# Use unique names
/claude-swarm:swarm-spawn "backend-dev-2" "backend-developer" "sonnet" "..."

# Or check existing teammates first
/claude-swarm:swarm-status <team-name>
```

#### 3. Kitty Socket Issues

**Error (kitty):**

```
Error: Could not find a valid kitty socket
```

**Solution:**

```bash
# 1. Verify kitty config has remote control enabled
grep -E 'allow_remote_control|listen_on' ~/.config/kitty/kitty.conf
# Should show:
#   allow_remote_control yes
#   listen_on unix:/tmp/kitty-$USER

# 2. Check socket exists (kitty appends -PID to path)
ls -la /tmp/kitty-$(whoami)-*

# 3. Test socket connectivity
kitten @ ls

# 4. Restart kitty completely if needed (not just reload)

# 5. Or manually set socket path
export KITTY_LISTEN_ON=unix:/tmp/kitty-$(whoami)-$KITTY_PID
```

**Note:** Kitty creates sockets at `/tmp/kitty-$USER-$PID`. The plugin auto-discovers the correct socket, but if you have multiple kitty instances, you may need to set `KITTY_LISTEN_ON` explicitly.

**Deep dive on kitty socket discovery**:

The spawn process tries sockets in this order:

1. `$KITTY_LISTEN_ON` environment variable (if set and valid)
2. Cached socket from previous successful connection
3. `/tmp/kitty-$USER-$KITTY_PID` (exact match for current kitty)
4. All `/tmp/kitty-$USER-*` sockets (newest first)
5. `/tmp/kitty-$USER` (fallback)
6. `/tmp/mykitty` and `/tmp/kitty` (alternative locations)

Each socket is validated with `kitten @ --to $socket ls` before use. If validation fails, the search continues.

**Multiple kitty instances troubleshooting**:

If you have multiple kitty windows open:

```bash
# List all kitty sockets
ls -la /tmp/kitty-$(whoami)-*

# Example output:
# /tmp/kitty-user-12345  (kitty window 1)
# /tmp/kitty-user-67890  (kitty window 2)

# Test each socket
kitten @ --to unix:/tmp/kitty-user-12345 ls
kitten @ --to unix:/tmp/kitty-user-67890 ls

# Set the correct socket for your team-lead window
export KITTY_LISTEN_ON=unix:/tmp/kitty-$(whoami)-$KITTY_PID
```

**Configuration file location varies**:

- Linux: `~/.config/kitty/kitty.conf`
- macOS: `~/.config/kitty/kitty.conf` or `~/Library/Preferences/kitty/kitty.conf`
- Check with: `kitty --debug-config | grep "Config file"`

**Common kitty config issues**:

1. **Config exists but not loaded**: Kitty requires full restart (CMD+Q, not just close window)
2. **Socket path has spaces**: Use quotes in listen_on directive
3. **Multiple listen_on directives**: Only the last one takes effect
4. **Incorrect syntax**: Must be `listen_on unix:/path`, not `listen_on /path`

**Example working kitty.conf**:

```
# ~/.config/kitty/kitty.conf
allow_remote_control yes
listen_on unix:/tmp/kitty-$USER
# Note: $USER expands at kitty startup, then -$PID is appended automatically
```

**Socket permission issues**:

```bash
# Check socket permissions
ls -la /tmp/kitty-$(whoami)-*
# Should show: srw------- (socket, owner read-write-execute only)

# If permissions are wrong:
# 1. Kill kitty completely
# 2. Remove old sockets: rm /tmp/kitty-$(whoami)-*
# 3. Restart kitty (will recreate with correct permissions)
```

#### 4. Path Traversal Validation

**Error:**

```
Error: Invalid team name (path traversal detected)
```

**Solution:**

```bash
# Use simple team names without special characters
# Good: "auth-team", "feature-x", "bugfix_123"
# Bad: "../other-team", "team/name", "team..name"
```

#### 5. Session Creation Timeout

**Error:**

```
Error: Timeout waiting for teammate session to start
```

**Solution:**

```bash
# Retry once (may be transient)
/claude-swarm:swarm-spawn "agent-name" ...

# Check system resources
top  # Look for high CPU/memory usage

# Verify multiplexer is responsive
tmux list-sessions  # or: kitty @ ls
```

**Recovery Steps:**

1. **Identify which spawn failed** - Check error messages
2. **Run diagnostics** - Use swarm-diagnose
3. **Fix underlying issue** - Install multiplexer, fix permissions, etc.
4. **Retry spawn** - Same command should work after fix
5. **Verify success** - Use swarm-verify
6. **Adjust plan if persistent** - Reduce team size or reassign tasks

### Status Mismatches

**Symptoms:**

- Config shows teammate as "active" but session is dead
- Session exists but not in config
- Conflicting status information

**Diagnosis:**

```bash
/claude-swarm:swarm-reconcile <team-name>
```

This will report:

- Offline sessions still marked active
- Zombie config entries
- Active sessions not in config
- Status inconsistencies

**Common Causes:**

#### 1. Teammate Session Crashed

**Detection:**

```bash
# Config shows active, but session doesn't exist
/claude-swarm:swarm-verify <team-name>
# Output: "Error: Session swarm-team-agent not found"
```

**Solution:**

```bash
# Run reconcile to update status
/claude-swarm:swarm-reconcile <team-name>

# Respawn the teammate
/claude-swarm:swarm-spawn "agent-name" "agent-type" "model" "prompt"

# Or resume the team (respawns all offline)
/claude-swarm:swarm-resume <team-name>
```

#### 2. Manual Session Kill

**Detection:**
User manually killed tmux/kitty session outside of cleanup command

**Solution:**

```bash
# Reconcile will detect and fix
/claude-swarm:swarm-reconcile <team-name>

# Respawn if needed
/claude-swarm:swarm-spawn "agent-name" ...
```

#### 3. Incomplete Cleanup

**Detection:**
Sessions killed but config files remain

**Solution:**

```bash
# Run cleanup properly
/claude-swarm:swarm-cleanup <team-name> --force

# Or manually remove config
rm ~/.claude/teams/<team-name>/config.json
```

### Communication Failures

**Symptoms:**

- Messages not received by teammates
- Inbox shows no messages when some were sent
- Message command succeeds but teammate never sees it

**Diagnosis:**

```bash
# Check team status
/claude-swarm:swarm-status <team-name>

# Verify teammate is alive
/claude-swarm:swarm-verify <team-name>

# Check inbox manually
cat ~/.claude/teams/<team-name>/inboxes/<agent-name>.json
```

**Common Causes:**

#### 1. Teammate Not Checking Inbox

**Solution:**

- Remind teammates to run `/claude-swarm:swarm-inbox` regularly
- Include inbox check in teammate initial prompts
- Send follow-up message or use broadcast

#### 2. Wrong Agent Name

**Error:**

```
Error: Agent 'backend' not found in team
```

**Solution:**

```bash
# Check exact agent names
/claude-swarm:swarm-status <team-name>

# Use exact name from status output
/claude-swarm:swarm-message "backend-dev" "message"  # Not "backend"
```

#### 3. Inbox File Corruption

**Symptoms:**
Inbox command fails or shows garbled output

**Solution:**

```bash
# Back up current inbox
cp ~/.claude/teams/<team-name>/inboxes/<agent>.json ~/.claude/teams/<team-name>/inboxes/<agent>.json.bak

# Reset inbox
echo '[]' > ~/.claude/teams/<team-name>/inboxes/<agent>.json

# Notify sender to resend messages
```

### Task Management Issues

**Symptoms:**

- Task updates not reflected in task list
- Cannot assign task to teammate
- Task IDs don't match

**Diagnosis:**

```bash
# View current tasks
/claude-swarm:task-list

# Check task file directly
cat ~/.claude/tasks/<team-name>/tasks.json
```

**Common Causes:**

#### 1. Invalid Task ID

**Error:**

```
Error: Task #99 not found
```

**Solution:**

```bash
# List tasks to see valid IDs
/claude-swarm:task-list

# Use correct ID from list
/claude-swarm:task-update 3 --status "in-progress"
```

#### 2. Invalid Status Value

**Error:**

```
Error: Invalid status 'done'
```

**Solution:**

```bash
# Use valid status values:
# - pending
# - in-progress
# - blocked
# - in-review
# - completed

/claude-swarm:task-update 3 --status "completed"  # Not "done"
```

#### 3. Assigning to Non-Existent Agent

**Error:**

```
Error: Agent 'frontend' not found in team
```

**Solution:**

```bash
# Check exact agent names
/claude-swarm:swarm-status <team-name>

# Use exact name
/claude-swarm:task-update 3 --assign "frontend-dev"
```

### Team Creation Issues

**Symptoms:**

- Team creation fails
- Directory permission errors
- Config file not created

**Diagnosis:**

```bash
# Check if team directory exists
ls -la ~/.claude/teams/<team-name>/

# Check permissions
ls -la ~/.claude/teams/
```

**Common Causes:**

#### 1. Team Already Exists

**Error:**

```
Error: Team 'my-team' already exists
```

**Solution:**

```bash
# Choose different name
/claude-swarm:swarm-create "my-team-2" "description"

# Or cleanup old team first
/claude-swarm:swarm-cleanup "my-team" --force
```

#### 2. Permission Denied

**Error:**

```
Error: Permission denied creating ~/.claude/teams/my-team/
```

**Solution:**

```bash
# Fix permissions on Claude directory
chmod 700 ~/.claude/
chmod 700 ~/.claude/teams/

# Retry creation
/claude-swarm:swarm-create "my-team" "description"
```

#### 3. Invalid Team Name

**Error:**

```
Error: Invalid team name
```

**Solution:**

```bash
# Use alphanumeric with hyphens/underscores
# Good: "feature-auth", "bugfix_123", "team2"
# Bad: "../team", "team name", "team/123"
```

## Recovery Strategies

Choosing the right recovery strategy depends on the severity of the issue, how much work would be lost, and whether the team can continue working. This section provides decision-making guidance for recovery scenarios.

### Recovery Decision Tree

```
Problem Diagnosed
│
├─ Are teammates still working successfully?
│  └─ YES → Use Soft Recovery (minimal disruption)
│     ├─ 1-2 teammates offline → Respawn just those teammates
│     ├─ Status mismatch only → Run reconcile
│     └─ Communication issue → Fix inbox, notify teammates
│
├─ Is critical work in progress?
│  └─ YES → Evaluate data loss risk
│     ├─ Work saved to files/commits? → Safe to use Hard Recovery
│     ├─ Work only in memory/history? → Try Partial Recovery first
│     └─ Uncertain? → Ask teammates to save work first
│
├─ Is the team completely non-functional?
│  └─ YES → Assess what can be salvaged
│     ├─ Tasks/config readable? → Use Partial Recovery
│     ├─ Files corrupted? → Use Hard Recovery
│     └─ Everything broken? → Nuclear option (full reset)
│
└─ Is this a persistent/recurring issue?
   └─ YES → After recovery, investigate root cause
      ├─ Check system resources (disk, memory, CPU)
      ├─ Review multiplexer logs
      └─ Consider reducing team size
```

### Soft Recovery

**When to use**:

- 1-3 teammates offline, rest working fine
- Status mismatch after manual session kill
- Communication failures that don't affect work
- Post-crash recovery where work is saved

**What's preserved**:

- All task data and comments
- Inbox messages
- Team configuration
- Work completed by active teammates

**What's affected**:

- Offline teammates lose in-memory history (but can resume from files)
- May need to re-explain context to respawned teammates

**Step-by-step soft recovery**:

1. **Identify offline teammates**:

```bash
/claude-swarm:swarm-status <team-name>
# Look for members showing "no window" with config "active"
```

2. **Run reconcile to update status**:

```bash
/claude-swarm:swarm-reconcile <team-name>
# This marks offline sessions as offline in config
```

3. **Decide on respawn strategy**:

```bash
# Option A: Respawn specific teammate
/claude-swarm:swarm-spawn "agent-name" "agent-type" "model" "Continue where you left off: [context]"

# Option B: Resume entire team (respawns all offline)
/claude-swarm:swarm-resume <team-name>
```

4. **Verify recovery**:

```bash
/claude-swarm:swarm-verify <team-name>
# All teammates should show as active
```

5. **Notify team of recovery**:

```bash
# Via bash function
source "${CLAUDE_PLUGIN_ROOT}/lib/swarm-utils.sh" 1>/dev/null
broadcast_message "<team-name>" "Recovery complete. Team member [name] has been respawned. Continue your work."
```

**Example soft recovery scenario**:

```
Situation: 5-teammate team, 2 teammates crashed mid-work

1. $ /claude-swarm:swarm-status my-team
   Output shows:
   - team-lead: active (you)
   - frontend-dev: active ✓
   - backend-dev: active ✗ (no window)
   - tester: active ✗ (no window)
   - reviewer: active ✓

2. $ /claude-swarm:swarm-reconcile my-team
   Output:
   - Marked backend-dev as offline
   - Marked tester as offline

3. $ /claude-swarm:swarm-resume my-team
   Output:
   - Respawning: backend-dev
   - Respawning: tester
   - Both spawned successfully

4. $ /claude-swarm:swarm-verify my-team
   Output: All teammates active ✓

5. Message team: "backend-dev and tester were respawned after crash. Please continue your assigned tasks."

Result: Team back to full capacity in ~60 seconds, no data lost
```

### Hard Recovery

**When to use**:

- Entire team is non-functional
- Config files corrupted or inconsistent
- After failed migration or upgrade
- When soft recovery fails multiple times
- Starting over is faster than debugging

**What's lost**:

- Task comments and progress notes
- Inbox messages (unread and read)
- lastSeen timestamps
- Team history

**What's preserved**:

- Task subjects and descriptions (if you note them first)
- Codebase changes (if committed to git)
- Your knowledge of work completed

**Before hard recovery checklist**:

```bash
# 1. Save task list for reference
/claude-swarm:task-list > tasks-backup.txt

# 2. Check for uncommitted work
git status

# 3. Ask teammates to commit their work (if any are responsive)
/claude-swarm:swarm-message "backend-dev" "Commit your work immediately, team restart needed"

# 4. Back up configs (optional)
cp ~/.claude/teams/<team-name>/config.json ~/config-backup.json

# 5. Document current state
/claude-swarm:swarm-status <team-name> > status-backup.txt
```

**Step-by-step hard recovery**:

1. **Full cleanup** (kills all sessions, optionally removes files):

```bash
/claude-swarm:swarm-cleanup <team-name> --force
```

2. **Verify cleanup**:

```bash
# Check no sessions remain
tmux list-sessions | grep <team-name>  # Should be empty
# or for kitty:
kitten @ ls | grep swarm-<team-name>   # Should be empty

# Check team directory
ls ~/.claude/teams/<team-name>/
# Should not exist if --force was used
```

3. **Recreate team**:

```bash
/claude-swarm:swarm-create <team-name> "Team description"
```

4. **Recreate tasks** from backup:

```bash
# Recreate each task manually
/claude-swarm:task-create "Implement API endpoints" "Full description..."
/claude-swarm:task-create "Write unit tests" "Test coverage for..."
# ... repeat for all tasks
```

5. **Respawn teammates**:

```bash
/claude-swarm:swarm-spawn "backend-dev" "backend-developer" "sonnet" "You are the backend developer. Focus on: [task details]"
/claude-swarm:swarm-spawn "frontend-dev" "frontend-developer" "sonnet" "You are the frontend developer. Focus on: [task details]"
# ... repeat for all teammates
```

6. **Assign tasks**:

```bash
/claude-swarm:task-update 1 --assign "backend-dev"
/claude-swarm:task-update 2 --assign "frontend-dev"
```

7. **Verify team health**:

```bash
/claude-swarm:swarm-verify <team-name>
/claude-swarm:swarm-status <team-name>
```

**Timeline**: Hard recovery typically takes 5-10 minutes for a 5-teammate team.

### Partial Recovery

**When to use**:

- Specific component broken (one inbox, one task file)
- Soft recovery too cautious, hard recovery too destructive
- You know exactly what's broken and how to fix it
- Testing fixes before full recovery

**Techniques**:

#### Reset Specific Inbox

**When**: Inbox file corrupted, messages malformed, inbox command errors

```bash
# Back up current inbox first
cp ~/.claude/teams/<team-name>/inboxes/<agent>.json ~/.claude/teams/<team-name>/inboxes/<agent>.json.bak

# Reset to empty inbox
echo '[]' > ~/.claude/teams/<team-name>/inboxes/<agent>.json

# Verify format
cat ~/.claude/teams/<team-name>/inboxes/<agent>.json
# Should output: []

# Notify affected teammate
/claude-swarm:swarm-message "<agent>" "Your inbox was reset due to corruption. Please check your backup if you need message history."
```

#### Fix Specific Task

**When**: Task file has invalid status, corrupted JSON, missing fields

```bash
# Back up task file
cp ~/.claude/tasks/<team-name>/<id>.json ~/.claude/tasks/<team-name>/<id>.json.bak

# Fix manually with jq
jq '.status = "in-progress"' ~/.claude/tasks/<team-name>/<id>.json > /tmp/task-fixed.json
mv /tmp/task-fixed.json ~/.claude/tasks/<team-name>/<id>.json

# Or edit directly
# Edit the JSON file to fix the issue

# Verify task is valid
cat ~/.claude/tasks/<team-name>/<id>.json | jq '.'
# Should output valid JSON
```

#### Respawn Single Teammate

**When**: One teammate crashed, others working fine

```bash
# 1. Check teammate is really offline
/claude-swarm:swarm-verify <team-name>

# 2. Update their status
/claude-swarm:swarm-reconcile <team-name>

# 3. Check their assigned tasks
/claude-swarm:task-list
# Note which tasks were assigned to this teammate

# 4. Respawn with context
/claude-swarm:swarm-spawn "<agent-name>" "<agent-type>" "<model>" "You crashed mid-work. Resume: [describe what they were doing, which files they were editing, what tasks to continue]"

# 5. Reassign their tasks
/claude-swarm:task-update <task-id> --assign "<agent-name>"
/claude-swarm:task-update <task-id> --comment "Teammate respawned, resuming work"

# 6. Notify teammate of their context
/claude-swarm:swarm-message "<agent-name>" "You were working on: [specific context]. Check Task #<id> for details."
```

#### Fix Config-Reality Mismatch

**When**: Config shows wrong status, but files and sessions are fine

```bash
# Use reconcile for automatic fixing
/claude-swarm:swarm-reconcile <team-name> --auto-fix

# Or manual fix if you know the issue
# Edit config.json directly:
# 1. Back up: cp ~/.claude/teams/<team-name>/config.json ~/config-backup.json
# 2. Edit: jq '(.members[] | select(.name == "agent-name")) |= (.status = "active")' config.json > config-fixed.json
# 3. Replace: mv config-fixed.json ~/.claude/teams/<team-name>/config.json
```

### Recovery Strategy Selection Guide

| Symptom              | Data Loss Risk | Recommended Strategy      | Recovery Time |
| -------------------- | -------------- | ------------------------- | ------------- |
| 1 teammate offline   | None           | Soft (respawn one)        | 30 seconds    |
| Multiple offline     | None           | Soft (resume team)        | 1-2 minutes   |
| Status mismatch only | None           | Soft (reconcile)          | 10 seconds    |
| Inbox corruption     | Messages lost  | Partial (reset inbox)     | 30 seconds    |
| Task file corrupt    | Comments lost  | Partial (fix task)        | 1-2 minutes   |
| Config corrupt       | History lost   | Hard (recreate)           | 5-10 minutes  |
| Everything broken    | All lost       | Hard (full reset)         | 10-15 minutes |
| Persistent failures  | Depends        | Diagnose root cause first | Varies        |

### When to Escalate

Some issues require more than recovery:

**Signs you need to investigate deeper**:

- Recovery works but issue recurs within minutes
- Multiple teammates crash simultaneously
- Errors mention "out of memory" or "too many open files"
- System becomes unresponsive during spawning
- Kitty/tmux behaves erratically

**Investigation steps**:

```bash
# Check system resources
top
# Look for: high CPU usage, low free memory, swap usage

# Check disk space
df -h ~/.claude
# Ensure adequate free space (>1GB recommended)

# Check file descriptor limits
ulimit -n
# Should be >=256, ideally >=1024

# Check for zombie processes
ps aux | grep claude
# Kill any orphaned Claude Code processes

# Review system logs
# macOS: Console.app, filter for "claude" or "kitty"
# Linux: journalctl --user | grep claude
```

## Prevention Best Practices

Prevention is significantly easier than recovery. Following these practices reduces issues by 80-90%.

### 1. Verify After Creation

**Why this matters**: Spawn failures may not be immediately obvious. A teammate might appear to spawn successfully but crash seconds later, or spawn without proper environment variables set.

**Verification workflow**:

```bash
# After spawning team, ALWAYS verify
/claude-swarm:swarm-verify <team-name>

# Expected output for healthy team:
# Verifying team 'my-team'...
# ✓ team-lead (team-lead) - session active
# ✓ backend-dev (backend-developer) - session active
# ✓ frontend-dev (frontend-developer) - session active
# All teammates verified successfully!

# Check detailed status
/claude-swarm:swarm-status <team-name>
```

**What to look for**:

- All teammates show "active" status
- All sessions exist (check "window exists" or "session active")
- No status mismatches
- Multiplexer responds quickly

**If verification fails immediately after spawn**:

```bash
# Wait 5-10 seconds for Claude Code to fully initialize
sleep 10
/claude-swarm:swarm-verify <team-name>

# If still failing, check what's wrong
/claude-swarm:swarm-diagnose <team-name>
```

### 2. Use Slash Commands

Slash commands have built-in validation, error handling, and safer parameter parsing compared to direct bash function calls.

**Comparison**:

```bash
# Slash command (RECOMMENDED)
/claude-swarm:swarm-spawn "backend-dev" "backend-developer" "sonnet" "Implement API"

# Direct bash function (AVOID unless necessary)
source "${CLAUDE_PLUGIN_ROOT}/lib/swarm-utils.sh" 1>/dev/null
spawn_teammate "team" "backend-dev" "backend-developer" "sonnet" "Implement API"
```

**Slash command advantages**:

- Validates all parameters before execution
- Provides clear error messages
- Handles edge cases (special characters, quotes, etc.)
- Consistent behavior across different shells
- Integrated with Claude Code's permission system

**When bash functions are acceptable**:

- In custom scripts combining multiple operations
- When you need direct access to return values
- For operations with no slash command equivalent
- When debugging library functions

### 3. Handle Errors Gracefully

**Never retry blindly** - understand why it failed first:

```bash
# BAD: Blind retry loop
for i in {1..5}; do
    /claude-swarm:swarm-spawn "agent" "worker" "sonnet" "prompt" && break
done

# GOOD: Diagnose then fix
if ! /claude-swarm:swarm-spawn "agent" "worker" "sonnet" "prompt"; then
    echo "Spawn failed, diagnosing..."
    /claude-swarm:swarm-diagnose <team-name>

    # Read diagnostic output, fix the issue, then retry once
    # Example: Install missing multiplexer, fix socket, etc.

    # Retry after fix
    /claude-swarm:swarm-spawn "agent" "worker" "sonnet" "prompt"
fi
```

**Error handling best practices**:

1. **Capture and log errors**:

```bash
if ! /claude-swarm:swarm-spawn "agent" "worker" "sonnet" "prompt" 2> spawn-error.log; then
    echo "Spawn failed. Error log:"
    cat spawn-error.log
    # Now you have error details for debugging
fi
```

2. **Set reasonable timeouts**:

```bash
# Don't wait forever for unresponsive operations
timeout 30s /claude-swarm:swarm-verify <team-name>
```

3. **Validate prerequisites**:

```bash
# Before spawning team, check prerequisites
if [[ "$(detect_multiplexer)" == "none" ]]; then
    echo "Error: No multiplexer available. Install tmux or kitty first."
    exit 1
fi
```

### 4. Regular Health Checks

For long-running teams (multiple hours or days), periodic health checks prevent gradual degradation.

**Recommended check frequency**:

- **Every 15-30 minutes** during active development
- **After major operations** (spawning multiple teammates, large file changes)
- **Before assigning new critical tasks**
- **When teammates seem unresponsive**

**Health check script**:

```bash
#!/bin/bash
# save as: health-check.sh

TEAM="$1"

echo "=== Health Check: $TEAM ==="
echo ""

# Check for status drift
echo "Checking for status mismatches..."
/claude-swarm:swarm-reconcile "$TEAM"

# Verify all teammates
echo ""
echo "Verifying teammate sessions..."
/claude-swarm:swarm-verify "$TEAM"

# Check task progress
echo ""
echo "Task summary..."
/claude-swarm:task-list | grep -E "in-progress|blocked"

# Done
echo ""
echo "Health check complete!"
```

**Automated monitoring** (for critical/long-running teams):

```bash
# Add to cron or run in background
while true; do
    /claude-swarm:swarm-verify <team-name> || {
        echo "Health check failed at $(date)"
        /claude-swarm:swarm-diagnose <team-name>
        # Send notification, page on-call, etc.
    }
    sleep 900  # Check every 15 minutes
done
```

### 5. Clean Up Properly

**Why proper cleanup matters**:

- Prevents orphaned sessions consuming resources
- Avoids name collisions when recreating teams
- Maintains clean state for future teams
- Prevents "team already exists" errors

**Cleanup best practices**:

```bash
# Standard cleanup (safe, preserves files for reference)
/claude-swarm:swarm-cleanup <team-name>

# This kills sessions but leaves:
# - Config files
# - Task files
# - Inbox files
# - Logs

# Force cleanup (removes everything)
/claude-swarm:swarm-cleanup <team-name> --force

# This kills sessions AND removes:
# - ~/.claude/teams/<team-name>/
# - ~/.claude/tasks/<team-name>/
```

**When to use each**:

- **Standard cleanup**: Team finished, might reference later, or debugging needed
- **Force cleanup**: Team failed, won't use again, or need clean slate

**What NOT to do**:

```bash
# NEVER manually delete while sessions are running
rm -rf ~/.claude/teams/<team-name>/  # Leaves orphaned sessions!

# NEVER kill sessions without cleanup
tmux kill-session -t swarm-<team>-<agent>  # Leaves config!

# ALWAYS use cleanup commands
/claude-swarm:swarm-cleanup <team-name>
```

**Cleanup verification**:

```bash
# After cleanup, verify nothing remains
tmux list-sessions | grep <team-name>  # Should be empty
ls ~/.claude/teams/<team-name>/       # Should not exist (if --force used)
```

### 6. Monitor Resource Usage

**Why monitoring matters**: Large teams (5+ teammates) can consume significant resources. Each Claude Code process uses:

- ~500MB RAM (varies by model)
- 1-2 CPU cores during active work
- File descriptors for sockets, logs, files

**Resource monitoring**:

```bash
# Check total Claude Code memory usage
ps aux | grep claude | awk '{sum+=$4} END {print "Total memory: " sum "%"}'

# Count active Claude processes
ps aux | grep claude | wc -l

# Check file descriptor usage
lsof -p $(pgrep claude) | wc -l

# Monitor system load
uptime
# Load average should be below CPU core count
```

**Resource limits**:

| Team Size      | RAM Needed | Recommended System              |
| -------------- | ---------- | ------------------------------- |
| 2-3 teammates  | 2-3 GB     | 8GB RAM minimum                 |
| 4-6 teammates  | 3-5 GB     | 16GB RAM recommended            |
| 7-10 teammates | 6-8 GB     | 32GB RAM recommended            |
| 10+ teammates  | 10+ GB     | Not recommended without testing |

**When to scale back**:

- System swap usage increases significantly
- CPU load average > number of cores
- Teammates become slow/unresponsive
- Frequent crashes or timeouts

```bash
# Reduce team size gracefully
# 1. Finish critical tasks
# 2. Have teammates commit work
# 3. Kill non-essential teammates
/claude-swarm:swarm-cleanup <team-name>  # Only kills sessions for specific agents

# 4. Consolidate work across fewer teammates
```

### 7. Initialize Teammates With Clear Context

**Problem**: Respawned teammates don't know what they were doing

**Solution**: Provide comprehensive initial prompts

**Bad initial prompt**:

```bash
/claude-swarm:swarm-spawn "backend-dev" "backend-developer" "sonnet" "Work on the backend"
```

**Good initial prompt**:

```bash
/claude-swarm:swarm-spawn "backend-dev" "backend-developer" "sonnet" "You are the backend developer for team my-team. Your tasks: 1) Implement /api/users endpoint in src/api/users.ts, 2) Add database schema in migrations/. Current status: API routes defined, need implementation. Coordinate with frontend-dev for API contract. Check Task #3 for full requirements."
```

**Initial prompt template**:

```
You are the [ROLE] for team [TEAM_NAME].

Your assigned tasks:
1. [TASK_1] - [STATUS]
2. [TASK_2] - [STATUS]

Current state:
- [What's done]
- [What's in progress]
- [What's blocked/dependencies]

Key files:
- [FILE_1]: [Description]
- [FILE_2]: [Description]

Coordinate with:
- [TEAMMATE_1]: [for what]
- [TEAMMATE_2]: [for what]

First action: [Specific next step]
```

### 8. Document Team Architecture

For teams lasting >1 hour, document the architecture:

```bash
# Create team docs
cat > ~/.claude/teams/<team-name>/README.md <<EOF
# Team: <team-name>

## Purpose
[What this team is building]

## Members
- team-lead: Orchestration, task assignment
- backend-dev: API implementation, database
- frontend-dev: UI components, styling
- tester: Test coverage, QA

## Task Breakdown
- Task #1: [Description] - assigned to backend-dev
- Task #2: [Description] - assigned to frontend-dev
- Task #3: [Description] - assigned to tester

## Dependencies
- Task #2 depends on Task #1 (API contract)
- Task #3 depends on Task #1, #2 (working features)

## Recovery Notes
- If backend-dev crashes: They were editing src/api/, check git status
- If frontend-dev crashes: They were in src/components/, state in localStorage
EOF
```

This documentation is invaluable for recovery scenarios.

## Performance Troubleshooting

### Slow or Unresponsive Teammates

**Symptoms**:

- Teammates take >30 seconds to respond to messages
- Commands timeout frequently
- High CPU or memory usage
- System fans running constantly

**Diagnosis**:

```bash
# Check Claude Code process resource usage
ps aux | grep claude | sort -k3 -r  # Sort by CPU%
ps aux | grep claude | sort -k4 -r  # Sort by memory%

# Check individual teammate resource usage
# Find PID of specific teammate:
ps aux | grep "CLAUDE_CODE_AGENT_NAME=backend-dev"

# Monitor live resource usage
top -pid $(pgrep -f "CLAUDE_CODE_AGENT_NAME=backend-dev")
```

**Common causes and solutions**:

1. **Too many teammates for system resources**:

```bash
# Solution: Reduce team size, use lighter models
# Replace opus with sonnet, sonnet with haiku for non-critical tasks
/claude-swarm:swarm-spawn "tester" "tester" "haiku" "Run existing tests"
```

2. **Memory leaks in long-running teammates**:

```bash
# Solution: Periodic restarts for long-lived teammates (>4 hours)
# 1. Ask teammate to commit work
# 2. Kill and respawn
# 3. Reassign tasks
```

3. **Disk I/O bottleneck**:

```bash
# Check disk I/O
iostat -x 1 5  # Run 5 samples, 1 second apart
# Look for high %util on disk with ~/.claude

# Solution: Move ~/.claude to faster disk (SSD)
# Or reduce concurrent file operations
```

### Multiplexer Performance Issues

**Kitty slowness**:

```bash
# Check kitty window count
kitten @ ls | jq '[.[].tabs[].windows[]] | length'
# If >50 windows total, kitty may slow down

# Solution: Use SWARM_KITTY_MODE=os-window for separate processes
export SWARM_KITTY_MODE=os-window
/claude-swarm:swarm-spawn ...
```

**Tmux slowness**:

```bash
# Check tmux session count
tmux list-sessions | wc -l
# If >20 sessions, consider cleanup

# Solution: Clean up old swarm sessions
for session in $(tmux list-sessions -F '#{session_name}' | grep swarm-); do
    # Check if session is active in a team
    # If not, kill it
    tmux kill-session -t "$session"
done
```

### Network or API Rate Limiting

**Symptoms**:

- Claude API errors mentioning "rate limit"
- Teammates getting "429 Too Many Requests"
- Intermittent connection failures

**Solutions**:

```bash
# 1. Reduce team size to stay under rate limits
# 2. Stagger teammate spawning (wait 10s between spawns)
for agent in backend frontend tester; do
    /claude-swarm:swarm-spawn "$agent" ...
    sleep 10
done

# 3. Use haiku model for lightweight tasks (lower API load)
/claude-swarm:swarm-spawn "tester" "tester" "haiku" "Run unit tests"
```

### Debugging Hangs and Freezes

**Teammate completely frozen**:

```bash
# 1. Find the teammate's process
ps aux | grep "CLAUDE_CODE_AGENT_NAME=backend-dev"

# 2. Send SIGTERM (graceful shutdown)
kill <PID>

# 3. If still frozen after 30s, force kill
kill -9 <PID>

# 4. Clean up and respawn
/claude-swarm:swarm-reconcile <team-name>
/claude-swarm:swarm-spawn "backend-dev" ...
```

**Multiplexer frozen**:

```bash
# Kitty frozen
# 1. Try sending command
kitten @ ls
# If hangs, kill kitty: killall kitty

# Tmux frozen
# 1. Try listing sessions
tmux list-sessions
# If hangs, kill tmux server: tmux kill-server
```

## Emergency Procedures

### Nuclear Option: Full Reset

**When to use**: Everything is completely broken, no recovery methods work, starting over is the only option.

**WARNING**: This destroys ALL team data across ALL teams. Only use as absolute last resort.

**What gets destroyed**:

- All team configurations
- All task data and history
- All inbox messages
- All team directories
- Active sessions (teammates will crash)

**Before nuking**:

```bash
# 1. Save what you can
tar -czf ~/swarm-backup-$(date +%Y%m%d-%H%M%S).tar.gz ~/.claude/teams/ ~/.claude/tasks/

# 2. Document current state
/claude-swarm:swarm-list-teams > ~/teams-backup.txt
for team in $(cat ~/teams-backup.txt); do
    /claude-swarm:swarm-status "$team" > ~/${team}-status.txt
    /claude-swarm:task-list >> ~/${team}-tasks.txt
done

# 3. Notify any responsive teammates
# (They'll lose their work context)
```

**Full reset procedure**:

```bash
# 1. Kill all swarm sessions
tmux kill-server  # Kills ALL tmux sessions
# or for kitty:
for window in $(kitten @ ls | jq -r '.[].tabs[].windows[] | select(.user_vars | keys[] | startswith("swarm_")) | .id'); do
    kitten @ close-window --match "id:$window"
done

# 2. Remove all swarm data
rm -rf ~/.claude/teams/
rm -rf ~/.claude/tasks/

# 3. Verify cleanup
ls ~/.claude/teams/  # Should not exist
ls ~/.claude/tasks/  # Should not exist

# 4. Recreate directories with proper permissions
mkdir -p ~/.claude/teams/
mkdir -p ~/.claude/tasks/
chmod 700 ~/.claude/teams/
chmod 700 ~/.claude/tasks/

# 5. Start fresh with new team
/claude-swarm:swarm-create "new-team" "Fresh start after full reset"

# 6. Verify clean state
/claude-swarm:swarm-status "new-team"
```

**After nuclear reset**:

- All previous teams are gone
- Need to recreate tasks from memory/notes
- Teammates need complete context re-explanation
- Good opportunity to optimize team structure

**Recovery timeline**: 15-30 minutes to rebuild team from scratch.

### Debugging Commands

For deep investigation:

```bash
# List all tmux sessions
tmux list-sessions

# Attach to specific teammate session (view their work)
tmux attach-session -t swarm-<team>-<agent>

# Check socket status
ls -la ~/.claude/sockets/

# View raw config
cat ~/.claude/teams/<team-name>/config.json

# View raw tasks
cat ~/.claude/tasks/<team-name>/tasks.json

# View raw inbox
cat ~/.claude/teams/<team-name>/inboxes/<agent>.json
```

## Environment Variables

When debugging, these environment variables are set for spawned teammates:

| Variable                   | Description                      |
| -------------------------- | -------------------------------- |
| `CLAUDE_CODE_TEAM_NAME`    | Current team name                |
| `CLAUDE_CODE_AGENT_ID`     | Agent's unique UUID              |
| `CLAUDE_CODE_AGENT_NAME`   | Agent name (e.g., "backend-dev") |
| `CLAUDE_CODE_AGENT_TYPE`   | Agent role type                  |
| `CLAUDE_CODE_TEAM_LEAD_ID` | Team lead's UUID                 |
| `CLAUDE_CODE_AGENT_COLOR`  | Agent display color              |
| `KITTY_LISTEN_ON`          | Kitty socket path (kitty only)   |

User-configurable:

| Variable            | Description             | Default     |
| ------------------- | ----------------------- | ----------- |
| `SWARM_MULTIPLEXER` | Force "tmux" or "kitty" | Auto-detect |
| `SWARM_KITTY_MODE`  | Kitty spawn mode        | `split`     |

## Quick Reference

| Issue                  | Quick Fix                                      |
| ---------------------- | ---------------------------------------------- |
| Spawn fails            | Run `/claude-swarm:swarm-diagnose`             |
| Status mismatch        | Run `/claude-swarm:swarm-reconcile`            |
| Session crashed        | Run `/claude-swarm:swarm-resume`               |
| Messages not received  | Verify agent name, check inbox                 |
| Invalid task ID        | Run `/claude-swarm:task-list` to see IDs       |
| Team creation fails    | Check permissions, use valid name              |
| Kitty socket not found | Check `listen_on` in kitty.conf, restart kitty |
| Cleanup incomplete     | Use `--force` flag                             |

## Related Skills

- **swarm-orchestration** - User/orchestrator workflow for creating teams and delegating
- **swarm-team-lead** - Guidance for spawned team-leads on coordination
- **swarm-teammate** - Guidance for workers within a swarm

## Reference Documentation

For more detailed information, see the error-handling reference documentation.
