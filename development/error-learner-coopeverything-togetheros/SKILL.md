---
name: error-learner
description: |
  **AUTO-TRIGGER:** Invoked by yolo1 skill after every commit to analyze session errors.

  Analyzes the current session for error patterns, researches solutions, and either:
  1. Updates knowledge files immediately (if pattern repeats 2+ times in session)
  2. Stores findings for cross-session tracking (if one-off error)

  On subsequent invocations, checks for cross-session patterns and promotes findings to knowledge.
---

# Error Learning System

This skill implements continuous learning from session errors to prevent repeated mistakes.

## Trigger Point

Called by `yolo1` skill at Step 8 (after commit, before push) via:
```
Invoke Skill: error-learner
Context: Current session transcript, commit SHA
```

## Core Logic

```
┌─────────────────────────────────────────────────────────────────┐
│                    ERROR LEARNER FLOW                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. SCAN SESSION                                                │
│     ├─ Parse tool outputs for error patterns                    │
│     ├─ Identify: TypeScript, build, git, runtime errors         │
│     └─ Extract error type, message, file, context               │
│                                                                 │
│  2. CHECK SAME-SESSION REPETITION                               │
│     ├─ Count occurrences of each error type in THIS session     │
│     └─ Group by error signature (type + normalized message)     │
│                                                                 │
│  3. BRANCH: USER-REPORTED, REPETITIVE, OR ONE-OFF?              │
│     │                                                           │
│     ├─ IF user explicitly reports a process error:              │
│     │   ├─ Treat as CONFIRMED PATTERN immediately               │
│     │   ├─ Skip occurrence counting (user feedback = pattern)   │
│     │   ├─ Research + document + update KB                      │
│     │   └─ Record with trigger: "user-reported" in JSON         │
│     │                                                           │
│     ├─ IF 2+ same-type errors in session:                       │
│     │   ├─ Research root cause                                  │
│     │   ├─ Determine best practice / solution                   │
│     │   ├─ Report to main assistant with:                       │
│     │   │   - Error pattern description                         │
│     │   │   - Root cause analysis                               │
│     │   │   - Recommended KB update                             │
│     │   └─ Main assistant updates knowledge files               │
│     │                                                           │
│     └─ IF one-off error (< 2 occurrences):                      │
│         ├─ Store in .claude/data/session-errors.json            │
│         └─ Include: error signature, context, timestamp         │
│                                                                 │
│  4. CHECK CROSS-SESSION PATTERNS                                │
│     ├─ Load .claude/data/session-errors.json                    │
│     ├─ Check if current error matches previous session errors   │
│     └─ IF match found (same error in different session):        │
│         ├─ Promote to "pattern" status                          │
│         ├─ Research solution                                    │
│         └─ Report to main assistant for KB update               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Error Detection Scope

### What to Scan

1. **TypeScript Errors**
   - `TS####:` error codes
   - `Cannot find module`, `Property does not exist`
   - `Type 'X' is not assignable to type 'Y'`
   - Path alias resolution failures

2. **Build Errors**
   - `npm run build` failures
   - Webpack/Vite compilation errors
   - Module resolution errors

3. **Git Errors**
   - Push/pull failures (403, 401, conflicts)
   - Branch operation failures
   - Merge conflicts

4. **Runtime Errors**
   - API endpoint failures
   - Database connection issues
   - Environment variable missing

### Error Signature Format

```json
{
  "type": "typescript|build|git|runtime",
  "code": "TS2339|BUILD_FAIL|GIT_403|...",
  "pattern": "normalized error message pattern",
  "example": "actual error message",
  "file": "path/to/file.ts (if applicable)",
  "context": "what operation was being performed"
}
```

## Session Errors JSON Schema

File: `.claude/data/session-errors.json`

```json
{
  "version": "1.0.0",
  "errors": [
    {
      "id": "uuid",
      "signature": {
        "type": "typescript",
        "code": "TS2339",
        "pattern": "Property .* does not exist on type .*"
      },
      "occurrences": [
        {
          "session_date": "2025-01-15",
          "commit_sha": "abc123",
          "file": "apps/web/app/test/page.tsx",
          "message": "Property 'foo' does not exist on type 'Bar'",
          "context": "Adding test page component"
        }
      ],
      "status": "watching|pattern_detected|resolved",
      "first_seen": "2025-01-15T10:30:00Z",
      "last_seen": "2025-01-15T10:30:00Z",
      "occurrence_count": 1
    }
  ],
  "resolved_patterns": [
    {
      "signature": { "type": "...", "code": "...", "pattern": "..." },
      "resolution": "Description of fix applied to knowledge base",
      "kb_file_updated": ".claude/knowledge/error-learnings.md",
      "resolved_date": "2025-01-15T12:00:00Z"
    }
  ],
  "last_updated": "2025-01-15T10:30:00Z"
}
```

## Workflow Steps

### Step 1: Scan Current Session

Parse the session transcript for errors. Look in:
- Bash tool outputs (build logs, git errors)
- File read/write operations that failed
- Any error messages in assistant responses

Extract error signatures for each unique error encountered.

### Step 2: Count Same-Session Occurrences

For each error signature found:
```
count = number of times this error type appeared in THIS session
```

Group errors by their normalized signature (ignore specific variable names, line numbers).

### Step 3: Process Based on Repetition

#### IF Repetitive (count >= 2 in same session):

**Research the error (MANDATORY WEB SEARCH):**

1. **Use WebSearch tool** to find latest documentation:
   - Search: `"[error code] [framework] best practice 2025"` (e.g., "TS2339 TypeScript best practice 2025")
   - Search: `"[error message] fix solution"` for specific fixes
   - Search: `"[library name] [version] breaking changes"` if version-related

2. **Use WebFetch tool** to read official docs:
   - TypeScript errors → fetch typescript-lang.org docs
   - Next.js errors → fetch nextjs.org docs
   - React errors → fetch react.dev docs
   - Git errors → fetch git-scm.com docs

3. **Extract from research:**
   - What causes this error type?
   - What is the current best practice (as of latest docs)?
   - Is there a pre-flight check that would catch it?
   - Has the solution changed in recent versions?

4. **Update knowledge with latest info:**
   - Include version numbers where relevant
   - Note if behavior differs between versions
   - Link to official documentation source

**Generate KB update recommendation:**
```markdown
## Error Pattern: [Error Code/Type]

**Trigger:** What causes this error
**Prevention:** Pre-flight check or workflow change
**Fix:** How to resolve when encountered

**Add to:** .claude/knowledge/[appropriate-file].md or .claude/workflows/[workflow].md
```

**Report to main assistant** with the recommendation. Main assistant will:
1. Review the recommendation
2. Edit the appropriate knowledge file
3. Add the pattern to `resolved_patterns` in session-errors.json

#### IF One-Off (count < 2 in same session):

**Store for future tracking:**
1. Load `.claude/data/session-errors.json`
2. Check if this error signature already exists
3. If exists: increment occurrence_count, add new occurrence
4. If new: create new error entry with status "watching"
5. Save updated JSON

### Step 4: Cross-Session Pattern Check

On every invocation:
1. Load session-errors.json
2. For each error with status "watching":
   - If occurrence_count >= 2 AND occurrences span multiple sessions:
     - Mark as "pattern_detected"
     - **Perform web search research** (same as Step 3 - use WebSearch and WebFetch)
     - Report to main assistant for KB update with latest documentation findings

## Knowledge File Targets

Based on error type, recommend updates to:

| Error Type | Target File |
|------------|-------------|
| TypeScript patterns | `.claude/knowledge/error-learnings.md` |
| Build workflow issues | `.claude/workflows/typescript-verification.md` |
| Git operations | `.claude/knowledge/ci-cd-discipline.md` |
| API/runtime errors | `.claude/knowledge/error-learnings.md` |
| SQL/database errors | `.claude/knowledge/error-learnings.md` |
| UX/CSS errors | `.claude/knowledge/error-learnings.md` |
| Infrastructure/deployment | `.claude/knowledge/infrastructure-incidents.md` |
| New error category | Add to `.claude/knowledge/error-learnings.md` |

## Output Format

### When Updating KB (Repetitive Pattern)

```
## Error Pattern Detected (Same-Session)

**Pattern:** [error type] - [description]
**Occurrences:** [count] times in this session
**Root Cause:** [analysis]
**Prevention:** [recommended pre-flight check]

### Recommended KB Update

**File:** .claude/knowledge/[file].md
**Section:** [section name]
**Add:**

```markdown
[content to add]
```

**Action:** Main assistant should apply this update now.
```

### When Storing for Future (One-Off)

```
## Error Logged for Cross-Session Tracking

**Pattern:** [error type] - [description]
**Status:** Watching (first occurrence)
**File:** .claude/data/session-errors.json updated

No KB update needed yet. Will promote to pattern if seen in future sessions.
```

### When Cross-Session Pattern Found

```
## Cross-Session Pattern Detected

**Pattern:** [error type] - [description]
**Sessions affected:** [count] sessions
**First seen:** [date]
**Last seen:** [date]
**Root Cause:** [analysis]

### Recommended KB Update

**File:** .claude/knowledge/[file].md
**Section:** [section name]
**Add:**

```markdown
[content to add]
```

**Action:** Main assistant should apply this update now.
```

## Integration with yolo1

In `yolo1` Step 8 (after commit), add:

```markdown
### 8. Git Operations + Error Learning

- Commit with message: `feat({module}): {slice} - {scope}`
- **Invoke error-learner skill:**
  - Analyze session for error patterns
  - Check cross-session error history
  - If patterns found: Apply KB updates before push
- Push branch: `git push -u origin feature/{module}-{slice}`
```

## Example: TypeScript Error Pattern

**Session has 3 occurrences of:**
```
TS2339: Property 'status' does not exist on type 'Response'
```

**Error Learner Output:**
```
## Error Pattern Detected (Same-Session)

**Pattern:** TS2339 - Property access on incorrect type
**Occurrences:** 3 times in this session
**Root Cause:** Using Response type instead of specific API response type
**Prevention:** Always read type definitions before accessing properties

### Recommended KB Update

**File:** .claude/knowledge/error-learnings.md
**Section:** Add new err-XXX entry or update existing pattern
**Add:**

```markdown
**Error Pattern:** `Property 'X' does not exist on type 'Response'`
- **Root Cause:** Generic `Response` type doesn't have custom properties
- **Solution:** Import and use specific response type (e.g., `ApiResponse<T>`)
- **Pre-flight:** Check type definition before accessing properties
```

**Action:** Main assistant should apply this update now.
```

## Maintenance

### Cleanup Old Entries

Entries in session-errors.json with:
- `status: "watching"` AND
- `last_seen` > 30 days ago AND
- `occurrence_count` == 1

Can be removed (truly one-off errors that didn't repeat).

### Archive Resolved Patterns

When an error is resolved:
1. Move from `errors` array to `resolved_patterns`
2. Include resolution details and KB file updated
3. Keep resolved_patterns for reference (prevents re-adding same fix)
