---
name: managing-session-continuity
description: Managing session continuity across Claude conversations by saving structured context (tasks, files, errors, git state) to JSON and loading in new sessions. Use when user asks how session continuity works, explaining session protocol functionality, understanding session state management, describing what gets saved in sessions, ending a session with unfinished work, starting a session with existing session-protocol.json, or when user mentions 'save progress', 'save session', 'save my work', 'continue later', 'session context', 'pick up where left off', 'load session', 'restore session', or explicitly invokes /save-session-protocol or /load-session-protocol commands.
allowed-tools: Read, Write, Bash
---

# Managing Session Continuity

Session state mgmt: context → JSON → restore

## When to Use

- Session end w/ unfinished work
- New session w/ sp.json exists
- User: "save|load|resume session|progress|work"
- `/save-session-protocol` or `/load-session-protocol` invoked

## Core Workflows

### WF1: Save Context

**Purpose**: Capture state → sp.json

**Steps**:

1. **Check session state**
   - Protocol loaded this session? → Skip Read (overwrite)
   - Protocol NOT loaded? → Read sp.json (merge)

2. **Extract context**
   - Pending/in_progress: ALL from TodoWrite
   - Completed: last 5 individual + consolidate older (see consolidation matrix)
   - Context blocks: arch decisions, critical pitfalls, error patterns, plan file refs
   - Git (if `.git` exists):
     ```bash
     [ -d .git ] && {
       git rev-parse --abbrev-ref HEAD 2>/dev/null  # branch
       git rev-parse HEAD 2>/dev/null                # commit
     }
     ```

3. **Consolidate tasks** (decision: 3+ = consolidate)
   - [ ] Same feature/area (e.g., "redesign page X")
   - [ ] >5 related completed tasks
   - [ ] No critical findings to preserve individually
   - [ ] >3 days since last task in group

   If 3+ → group into 1 task w/ consolidated=true + summary

   **Consolidation format**:
   ```json
   {
     "id": "TASK_XXX",
     "title": "Redesign homepage layout",
     "status": "completed",
     "consolidated": true,
     "consolidated_count": 12,
     "context": "Summary: Redesigned nav, hero, footer. Pitfall: CSS grid safari compat. See: docs/homepage-plan.md",
     "completed": "2025-11-26T14:00:00Z"
   }
   ```

4. **Build JSON** (minified, no pretty-print)
   - Schema: see JSON Format
   - Task IDs: TASK_XXX (sequential, unique)
   - Timestamps: ISO8601 UTC (YYYY-MM-DDTHH:MM:SSZ)
   - Privacy: strip usernames from paths (~/project not /Users/john/project)

5. **Write**
   - Write(sp.json) minified format

6. **Report**
   - "Saved X pend, Y done (Z consolidated). Next: TASK_XXX"

### WF2: Load Context

**Purpose**: Parse sp.json → restore state

**Steps**:

1. **Read + parse**
   - Read(sp.json)
   - Extract: metadata, tasks[], context_blocks[]

2. **Validate git** (if metadata has git fields AND .git exists)
   ```bash
   [ -d .git ] && {
     curr=$(git rev-parse HEAD 2>/dev/null)
     curr_br=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
     [ "$curr" != "$saved_commit" ] && warn "Git state changed"
     [ "$curr_br" != "$saved_branch" ] && warn "Branch: $saved → $curr_br"
   }
   ```

3. **Build summary**
   - Age: calc from metadata.created
   - Counts: pend/prog/done (note consolidated count)
   - Next: first pend/prog
   - Warnings: git drift (if any)

4. **Present**
   - Concise: counts, next action, warnings

## JSON Format

### Schema

```json
{
  "metadata": {
    "version": "2.0",
    "created": "2025-11-26T10:00:00Z",
    "updated": "2025-11-26T14:00:00Z",
    "git_branch": "feature/auth",
    "git_commit": "abc123f5d2e8a1b4c6e9f3a7"
  },
  "tasks": [
    {
      "id": "TASK_001",
      "title": "Fix auth middleware",
      "status": "pending",
      "priority": "P1",
      "category": "BUGFIX",
      "created": "2025-11-26T10:00:00Z",
      "completed": null,
      "consolidated": false,
      "consolidated_count": 0,
      "context": "JWT RS256 validation fails. PEM format req. See: src/auth/middleware.ts:45",
      "files": ["src/auth/middleware.ts:45", "config/jwt.ts:12"]
    },
    {
      "id": "TASK_010",
      "title": "Redesign homepage",
      "status": "completed",
      "priority": "P2",
      "category": "FEATURE",
      "created": "2025-11-20T09:00:00Z",
      "completed": "2025-11-24T18:00:00Z",
      "consolidated": true,
      "consolidated_count": 12,
      "context": "Redesigned nav, hero, footer (12 tasks). Pitfall: CSS grid Safari compat fixed with -webkit-. Plan: docs/homepage-plan.md",
      "files": ["docs/homepage-plan.md"]
    }
  ],
  "context_blocks": [
    {
      "title": "JWT Auth Setup",
      "content": "RS256 algo. Pub key: ~/config/jwt-keys/public.pem. TTL: 1h access, 7d refresh. Rotation: monthly",
      "updated": "2025-11-26T14:00:00Z",
      "related_tasks": ["TASK_001"]
    }
  ]
}
```

### Fields

**metadata** (req):
- version: "2.0"
- created/updated: ISO8601
- git_branch/git_commit: str|null

**tasks** (req, arr, ≥1):
- id: "TASK_XXX"
- title: str
- status: "pending"|"in_progress"|"completed"
- priority: "P1"|"P2"|"P3" (opt)
- category: BUGFIX|FEATURE|CONFIG|DOCS|TEST|REFACTOR (opt)
- created: ISO8601
- completed: ISO8601|null
- consolidated: bool (true if grouped from multiple)
- consolidated_count: int (# of original tasks if consolidated)
- context: str (opt, include: summary, pitfalls, plan refs, file refs)
- files: arr[str] (opt, path:line format, rel or ~/)

**context_blocks** (opt, arr):
- title: str
- content: str (arch decisions, error patterns, critical pitfalls)
- updated: ISO8601
- related_tasks: arr[task_id] (opt)

### Format Rules

- **Minified JSON**: no whitespace, single line
- **Timestamps**: UTC w/ Z suffix
- **Completed limit**: ≤5 individual + consolidated groups (no hard limit on consolidated)
- **Privacy**:
  - Paths: ~/ or relative (never /Users/username/ or C:\Users\username\)
  - No emails, API keys, tokens, credentials, personal info
- **Task IDs**: sequential (TASK_001, TASK_002...)

## Consolidation Matrix

Decision (3+ = consolidate):
- [ ] Same feature/area
- [ ] >5 related completed tasks
- [ ] No critical findings to preserve individually
- [ ] >3 days since last task in group

If 3+ → create consolidated task:
- title: feature/area name
- consolidated: true
- consolidated_count: N
- context: summary + pitfalls + file refs
- completed: last task completion ts

**Keep individual** (never consolidate):
- Critical bugs w/ specific fixes
- Tasks w/ unique pitfalls/lessons
- Recent (<3 days) completed
- Tasks referenced by pending work

## Tool Usage

- **Write**: sp.json (minified)
- **Read**: sp.json (if not loaded this session) or existing (if merge needed)
- **Bash**: git ops (only if .git exists)

## Integration

Invoked by:
- `/save-session-protocol` → WF1
- `/load-session-protocol` → WF2

## Examples

**Save (fresh session)**:
```
User: "Save progress"
Claude: [Check: protocol not loaded → skip Read]
        [Extract: 3 pend, 8 done → consolidate 5 old → 3 remain]
        [Git: .git exists → capture state]
        Saved 3 pend, 3 done (5 consolidated). Next: TASK_001 - Fix auth
```

**Load**:
```
User: "Load session"
Claude: Loaded (2d old)
        - 3 pend, 3 done (5 consolidated into 1)
        - Next: TASK_001 - Fix auth middleware
        - Git: state changed (2 commits ahead)
```

## Error Handling

- No .git → skip git (no error)
- Invalid JSON → error "Cannot load: invalid JSON"
- Missing metadata → error "Cannot load: missing metadata"
- Never fail silently

## Output Format

**Save**:
```
Saved → sp.json
- 5 pend (2 P1, 3 P2)
- 8 done (3 individual, 1 consolidated from 12)
- Git: feature/auth @ abc123f
Next: TASK_001 - Fix JWT validation
```

**Load**:
```
Loaded sp.json (2d old)
- 3 pend, 1 prog, 8 done (1 consolidated from 12)
- Git: feature/auth @ abc123f (2 commits ahead)
Next: TASK_001 - Fix JWT validation
```