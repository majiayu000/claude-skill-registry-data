---
name: ct-debug-skill
description: Debug and troubleshoot claude-threads, orchestrator, and agent issues
allowed-tools: Bash,Read,Grep,Glob
user-invocable: true
version: "1.0.0"
---

# Claude Threads Debug Skill

Diagnose and troubleshoot issues with claude-threads, orchestrator, threads, worktrees, and agent coordination.

## When to Use

Activate this skill when:
- Threads are stuck, blocked, or not starting
- Orchestrator won't start or crashes
- Worktrees are orphaned or inconsistent
- Events aren't being delivered
- Database is corrupted or inconsistent
- Agents aren't coordinating properly
- PR lifecycle management isn't working

## Quick Diagnostics

### System Health Check

```bash
# Overall system status
ct orchestrator status
ct api status

# Database integrity
ct db check

# List all threads with status
ct thread list --all

# List worktrees and check for orphans
ct worktree list
ct worktree reconcile
```

### Thread Diagnostics

```bash
# Thread status and details
ct thread status <thread-id>
ct thread status <thread-id> --verbose

# Thread logs (last 100 lines)
ct thread logs <thread-id> --tail 100

# Follow logs in real-time
ct thread logs <thread-id> -f

# Find stuck threads
ct thread list blocked
ct thread list running  # Check if actually running
```

### Orchestrator Diagnostics

```bash
# Check orchestrator process
ps aux | grep -E "orchestrator|ct"

# Check orchestrator logs
cat .claude-threads/logs/orchestrator.log | tail -100

# Check for lock files
ls -la .claude-threads/*.lock 2>/dev/null

# Remove stale lock (if orchestrator crashed)
rm -f .claude-threads/orchestrator.lock
```

### Worktree Diagnostics

```bash
# List all worktrees
ct worktree list

# Check for orphaned worktrees
ct worktree reconcile

# Auto-fix orphaned worktrees
ct worktree reconcile --fix

# Check git worktree status directly
git worktree list

# Check specific worktree
ct worktree status <worktree-id>
```

### Base + Fork Diagnostics

```bash
# List base worktrees
sqlite3 .claude-threads/threads.db "SELECT * FROM pr_base_worktrees;"

# List forks
sqlite3 .claude-threads/threads.db "SELECT * FROM pr_worktree_forks;"

# Check base status for a PR
ct worktree base-status <pr-number>

# List forks for a PR
ct worktree list-forks <pr-number>

# Check for stale locks
ls -la .claude-threads/worktrees/*.lock 2>/dev/null
```

### Event Diagnostics

```bash
# List recent events
ct event list --limit 50

# Filter by type
ct event list --type THREAD_FAILED --limit 20
ct event list --type ESCALATION_NEEDED --limit 20

# Filter by source
ct event list --source <thread-id> --limit 20

# Watch events in real-time
ct event watch --types "FAILED,BLOCKED,ESCALATION"
```

### Database Diagnostics

```bash
# Check database file
ls -la .claude-threads/threads.db

# Check database integrity
sqlite3 .claude-threads/threads.db "PRAGMA integrity_check;"

# Check schema version
sqlite3 .claude-threads/threads.db "SELECT * FROM schema_migrations ORDER BY version DESC LIMIT 5;"

# Count records
sqlite3 .claude-threads/threads.db "
SELECT 'threads' as table_name, COUNT(*) as count FROM threads
UNION ALL
SELECT 'events', COUNT(*) FROM events
UNION ALL
SELECT 'pr_watches', COUNT(*) FROM pr_watches
UNION ALL
SELECT 'pr_base_worktrees', COUNT(*) FROM pr_base_worktrees
UNION ALL
SELECT 'pr_worktree_forks', COUNT(*) FROM pr_worktree_forks;
"

# Find threads in bad state
sqlite3 .claude-threads/threads.db "
SELECT id, name, status, updated_at
FROM threads
WHERE status IN ('blocked', 'failed', 'error')
ORDER BY updated_at DESC;
"
```

### API Diagnostics

```bash
# Check API health
curl -s http://localhost:31337/api/health | jq .

# Check API status
curl -s http://localhost:31337/api/status | jq .

# Check with auth
curl -s -H "Authorization: Bearer $CT_API_TOKEN" \
  http://localhost:31337/api/status | jq .

# Check API process
lsof -i :31337
```

### PR Shepherd Diagnostics

```bash
# List watched PRs
ct pr list

# Check specific PR status
ct pr status <pr-number>

# Check PR comments
ct pr comments <pr-number>

# Check PR conflicts
ct pr conflicts <pr-number>

# Check PR shepherd logs
cat .claude-threads/logs/pr-shepherd.log | tail -100
```

## Common Issues and Fixes

### Issue: Thread Stuck in "running" but not executing

**Symptoms:**
- Thread shows "running" in `ct thread list`
- No activity in logs
- Process may have crashed

**Diagnosis:**
```bash
ct thread status <thread-id> --verbose
ps aux | grep <thread-id>
cat .claude-threads/logs/thread-<thread-id>.log | tail -50
```

**Fix:**
```bash
# Force stop and restart
ct thread stop <thread-id> --force
ct thread start <thread-id>
```

### Issue: Orchestrator won't start

**Symptoms:**
- `ct orchestrator start` hangs or fails
- "Already running" but no process

**Diagnosis:**
```bash
ls -la .claude-threads/orchestrator.lock
ps aux | grep orchestrator
```

**Fix:**
```bash
# Remove stale lock
rm -f .claude-threads/orchestrator.lock
ct orchestrator start
```

### Issue: Worktrees out of sync with database

**Symptoms:**
- Worktrees exist on disk but not in database (or vice versa)
- Fork operations fail

**Diagnosis:**
```bash
ct worktree reconcile
```

**Fix:**
```bash
ct worktree reconcile --fix
```

### Issue: Fork merge-back fails

**Symptoms:**
- `ct worktree merge-back` returns error
- Conflict during merge

**Diagnosis:**
```bash
cd $(ct worktree fork-path <fork-id>)
git status
git diff
```

**Fix:**
```bash
# Option 1: Retry with updated base
ct worktree remove-fork <fork-id> --force
ct worktree base-update <pr-number>
# Re-fork and retry

# Option 2: Manual merge
cd $(ct worktree base-path <pr-number>)
git merge --no-commit $(ct worktree fork-path <fork-id>)
# Resolve conflicts manually
git add .
git commit -m "Merge fork with manual conflict resolution"
ct worktree remove-fork <fork-id> --force
```

### Issue: Events not being delivered

**Symptoms:**
- Agent publishes event but listener never receives
- Events stuck in queue

**Diagnosis:**
```bash
ct event list --limit 50
sqlite3 .claude-threads/threads.db "
SELECT type, COUNT(*), MAX(created_at)
FROM events
GROUP BY type
ORDER BY MAX(created_at) DESC;
"
```

**Fix:**
```bash
# Check if event TTL is too short
cat .claude-threads/config.yaml | grep -A5 events

# Manually trigger event processing
ct event process
```

### Issue: Database locked

**Symptoms:**
- "database is locked" errors
- Operations fail intermittently

**Diagnosis:**
```bash
lsof .claude-threads/threads.db
```

**Fix:**
```bash
# Stop all threads and orchestrator
ct orchestrator stop
ct thread list running | xargs -I {} ct thread stop {}

# Wait for locks to release
sleep 5

# Restart
ct orchestrator start
```

### Issue: API returns 401/403

**Symptoms:**
- Remote connections fail with auth errors
- "Unauthorized" responses

**Diagnosis:**
```bash
# Check token configuration
grep api_token .claude-threads/config.yaml
echo $CT_API_TOKEN
echo $N8N_API_TOKEN

# Test with token
curl -v -H "Authorization: Bearer $CT_API_TOKEN" \
  http://localhost:31337/api/health
```

**Fix:**
```bash
# Reconnect with correct token
ct remote disconnect
ct remote connect localhost:31337 --token $CT_API_TOKEN
```

## Advanced Debugging

### Enable Verbose Logging

```bash
# Set debug mode
export CT_DEBUG=1
export CT_LOG_LEVEL=debug

# Restart orchestrator with debug
ct orchestrator restart
```

### Trace Event Flow

```bash
# Watch all events
ct event watch

# In another terminal, trigger action and observe
ct spawn test-thread --template developer.md
```

### Database Queries

```bash
# Find all threads for a PR
sqlite3 .claude-threads/threads.db "
SELECT t.id, t.name, t.status, t.created_at
FROM threads t
WHERE t.context LIKE '%\"pr_number\":123%'
ORDER BY t.created_at DESC;
"

# Find recent failures
sqlite3 .claude-threads/threads.db "
SELECT id, name, status, error_message, updated_at
FROM threads
WHERE status = 'failed'
ORDER BY updated_at DESC
LIMIT 10;
"

# Check event delivery
sqlite3 .claude-threads/threads.db "
SELECT e.type, e.source_thread_id, e.created_at,
       substr(e.data, 1, 100) as data_preview
FROM events e
ORDER BY e.created_at DESC
LIMIT 20;
"
```

### Process Tracing

```bash
# Find all claude-threads related processes
ps aux | grep -E "ct|claude|orchestrator" | grep -v grep

# Check process tree
pstree -p $(pgrep -f orchestrator)

# Check file descriptors
lsof -p $(pgrep -f orchestrator)
```

### Git State Recovery

```bash
# If worktree is corrupted
cd .claude-threads/worktrees/<worktree-id>
git fsck
git gc --prune=now

# Remove and recreate worktree
git worktree remove .claude-threads/worktrees/<worktree-id> --force
ct worktree cleanup
```

## Cleanup Commands

```bash
# Stop everything
ct orchestrator stop
ct api stop

# Clean up all threads
ct thread list --all | xargs -I {} ct thread delete {}

# Clean up all worktrees
ct worktree cleanup --force

# Clean up orphaned forks
ct worktree reconcile --fix

# Reset database (DESTRUCTIVE)
rm .claude-threads/threads.db
ct db migrate

# Full reset (DESTRUCTIVE)
rm -rf .claude-threads
ct init
```

## Documentation

- [ARCHITECTURE.md](../../docs/ARCHITECTURE.md) - System architecture
- [AGENT-COORDINATION.md](../../docs/AGENT-COORDINATION.md) - Agent coordination
- [WORKTREE-GUIDE.md](../../docs/WORKTREE-GUIDE.md) - Worktree management
- [EVENT-REFERENCE.md](../../docs/EVENT-REFERENCE.md) - Event types
