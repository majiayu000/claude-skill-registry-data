---
name: decision-tracker
description: Git-powered state awareness - track file changes, session context, decisions, and work history. Query what happened in previous sessions and during current session. Auto-activates for state queries and before duplicating work.
keywords:
  - what changed
  - what happened
  - previous session
  - last session
  - what did we
  - what was
  - show changes
  - show status
  - current state
  - file changes
  - git status
  - session status
  - why did we
  - what was the decision
  - should we use
  - which approach
  - research
  - before we start
  - have we already
  - did we already
auto_invoke: true
---

# State Tracker - Git-Powered Session & State Awareness

**Purpose:** Provide Claude with complete awareness of project state using git as source of truth, preventing stale mental models and redundant work.

**What This System Tracks:**

1. **In-Session State** (real-time)
   - File modifications (git diff)
   - Uncommitted changes (git status)
   - Current branch and commit

2. **Between-Session Context** (differential)
   - What happened since last session
   - Commits made (by you or others)
   - Files changed externally
   - Branch switches

3. **Historical Decisions** (queryable)
   - Past research findings
   - Architectural decisions
   - Implementation plans

**Token Overhead:**
- In-session checks: ~200-500 tokens (only when files change)
- Between-session context: ~1-2K tokens (differential only)
- Decision queries: ~2-5K tokens (selective loading)
- **Total:** <5K tokens vs 50K+ full reload

---

## When This Skill Activates

**Auto-activates when you detect:**

**State Queries:**
- "what changed since last session?"
- "show me what happened"
- "what's the current state?"
- "what files did we work on?"
- "what commits were made?"

**Before File Operations:**
- PreToolUse hook activates automatically
- Checks if file changed externally
- Warns before Edit/Write if file is stale

**Before Duplicating Work:**
- "research X" → Check if already researched
- "decide on Y" → Check if already decided
- "plan Z" → Check if plan exists

---

## Your Workflow When This Skill Activates

### If User Asks "What Changed?"

**Run the manual status script:**
```bash
./scripts/session-status.sh
```

**This shows:**
- Git activity since last session
- Current working directory status
- Decision tracking summary

**Token cost:** ~500 tokens for complete state summary

### If You're About to Edit a File

**Trust the PreToolUse hook:**
- It automatically checks git status
- If file changed externally, you'll see warning
- Follow the recommendation: Re-read before editing

**Don't manually check git status** - hook does it automatically!

### If Starting Research or Planning

**Query decisions.yaml first:**
```bash
# Before research
uv run scripts/decision-query.py --topic "{topic}" --type research

# Before planning
uv run scripts/decision-query.py --topic "{topic}" --type plans

# Before deciding
uv run scripts/decision-query.py --topic "{topic}" --type decisions
```

**If found:** Load existing context (2-5K tokens)
**If not found:** Proceed with new work

###If User Made External Changes

**User says:** "I made some changes" or "I committed something"

**Your response:**
```bash
# Check what changed
./scripts/session-status.sh
```

Then summarize what you found for the user.

---

## The Complete State Awareness System

### Component 1: In-Session State Sync (Automatic)

**PreToolUse Hook** checks git state before file operations:

```bash
# Happens automatically when you try to Edit/Write
PreToolUse: Intercepts tool call
  → Runs: git status <file>
  → If changed: "⚠️ File modified externally - Re-read before editing"
  → Always continues (non-blocking)
```

**What you see:**
```
⚠️ File State Change Detected

File: hooks/user_prompt_submit.py
Status: MODIFIED
Git Says: File has uncommitted changes

Recommendation:
- Re-read file to see current state
- Use Read tool before Edit

Continuing with your Edit operation...
```

**Token cost:** ~300 tokens (only when file actually changed)

### Component 2: Between-Session Context (Automatic)

**SessionStart Hook** injects git context automatically:

```
Session starts:
  → SessionStart reads .contextune/last_session.yaml
  → Runs: git log <last_commit>..HEAD
  → Runs: git diff --stat <last_commit>..HEAD
  → Generates differential summary
  → Injects as additionalContext
```

**What you see at session start:**
```
📋 Git Context Since Last Session (2 hours ago)

**Git Activity:**
- 5 new commits
- 8 files changed (+250, -30)
- Branch: master

**Recent Commits:**
  a95478f feat: add three-layer git enforcement
  1e1a15a feat: add plan extraction support
  ... and 3 more

**Files Changed:**
  Added (2):
    - commands/ctx-git-commit.md
    - hooks/pre_tool_use_git_advisor.py
  Modified (6):
    - hooks/user_prompt_submit.py
    - hooks/hooks.json
    ... and 4 more

**Current Status:** 2 uncommitted changes

Ready to continue work!
```

**Token cost:** ~1-2K tokens (only NEW information since last session)

### Component 3: Manual Status Check

**When user asks "what changed?" or you need to check state:**

```bash
# Run the status script
./scripts/session-status.sh
```

**Shows:**
- Current git state (branch, commit, uncommitted files)
- Changes since last session (commits, files, diff stats)
- Decision tracking status
- Full git summary

**When to use:**
- User asks "what's the current state?"
- You need to verify what happened
- Before major operations
- After user says "I made some changes"

**Token cost:** ~500 tokens

---

## Complete Workflow Examples

### Example 1: File Modified Externally (In-Session)

```
10:00 - You: Read hooks/user_prompt_submit.py
        [File contents loaded into context]

10:15 - User edits file in VS Code
        [Makes changes, saves]

10:20 - You: Edit hooks/user_prompt_submit.py

        PreToolUse Hook: ⚠️ File State Change Detected
          File: hooks/user_prompt_submit.py
          Status: MODIFIED
          Recommendation: Re-read before editing

You: "I see the file was modified externally. Let me re-read it first."
     [Read hooks/user_prompt_submit.py]
     [Now have current state]
     [Proceed with Edit]
```

**Token saved:** Prevented edit conflict + re-work

### Example 2: New Session After External Changes

```
Session 1 ends:
  SessionEnd: Records metadata to .contextune/last_session.yaml
    - session_id, timestamp, last_commit, branch, files_worked_on

[User works outside Claude]
  - Commits via terminal: git commit -m "quick fix"
  - Edits 3 files manually
  - Switches to develop branch

Session 2 starts:
  SessionStart: Loads .contextune/last_session.yaml
    → git log <last_commit>..HEAD
    → git diff --stat <last_commit>..HEAD
    → Generates summary

Claude sees:
  📋 Git Context Since Last Session (3 hours ago)

  **Git Activity:**
  - 1 new commit: "quick fix"
  - 3 files changed
  - Branch: master → develop (switched)

  **Current Status:** Clean ✅

Claude: "I see you made a commit and switched to develop branch.
        The 3 files that changed are now in my context. Ready to continue!"
```

**Token cost:** ~1.5K (vs 50K+ full reload)

---

## The Decision Tracking System

### Structure

**decisions.yaml** - YAML database with 3 types of entries:

```yaml
research:
  entries:
    - id: "res-001-authentication-libraries"
      topic: "Authentication libraries for Node.js"
      findings: "Compared Passport.js, Auth0, NextAuth..."
      recommendation: "Use NextAuth for React apps"
      created_at: "2025-10-28"
      expires_at: "2026-04-28"  # 6 months
      tags: [authentication, libraries, nodejs]

plans:
  entries:
    - id: "plan-001-jwt-implementation"
      title: "JWT Authentication Implementation"
      summary: "5 tasks: AuthService, middleware, tokens..."
      status: "completed"
      created_at: "2025-10-28"
      tags: [authentication, implementation]

decisions:
  entries:
    - id: "dec-001-dry-strategy"
      title: "Unified DRY Strategy"
      status: "accepted"
      context: "CHANGELOG grows unbounded..."
      alternatives_considered: [...]
      decision: "Use scripts for git workflows"
      consequences: {positive: [...], negative: [...]}
      tags: [architecture, cost-optimization]
```

### CLI Tools

**Query existing context:**
```bash
# Check if we already researched a topic
uv run scripts/decision-query.py --topic "authentication" --type research

# Check for existing decisions
uv run scripts/decision-query.py --topic "DRY" --type decisions

# Check for active plans
uv run scripts/decision-query.py --type plans --status active

# Query by tags
uv run scripts/decision-query.py --tags architecture cost-optimization
```

**Output format:**
```yaml
# Filtered entries matching your query
# Load only relevant context (2-5K tokens vs 150K full CHANGELOG)
```

---

## Your Workflow (IMPORTANT!)

### Before Starting Research

**ALWAYS query first:**

```bash
# Check if we already researched this topic
uv run scripts/decision-query.py --topic "{research_topic}" --type research
```

**If found:**
- Load the existing findings (2K tokens)
- Check expiration date (research expires after 6 months)
- If recent → Use existing research
- If expired → Research again, update entry

**If NOT found:**
- Proceed with research
- SessionEnd hook will auto-extract to decisions.yaml

**Savings:**
- Skip $0.07 redundant research
- Load 2K tokens instead of researching again

### Before Making Decisions

**ALWAYS query first:**

```bash
# Check for existing decisions on this topic
uv run scripts/decision-query.py --topic "{decision_topic}" --type decisions
```

**If found:**
- Load the decision context
- Check status (accepted, rejected, superseded)
- If accepted → Follow existing decision
- If superseded → Find superseding decision
- If rejected → Understand why, avoid same approach

**If NOT found:**
- Proceed with decision-making
- SessionEnd hook will auto-extract to decisions.yaml

**Savings:**
- Skip 15-30 min re-discussion
- Consistent decisions across sessions

### Before Planning

**ALWAYS query first:**

```bash
# Check for existing plans on this topic
uv run scripts/decision-query.py --topic "{feature_name}" --type plans
```

**If found:**
- Load existing plan (2-3K tokens)
- Check status (active, completed, archived)
- If active → Continue existing plan
- If completed → Reference, don't recreate

**If NOT found:**
- Create new plan with /ctx:plan
- Plan will be auto-extracted to decisions.yaml

---

## Auto-Population

**decision-sync.py** scans conversation history and auto-populates decisions.yaml:

```bash
# Scan all conversations for decisions (run once)
uv run scripts/decision-sync.py

# Result: Populates decisions.yaml with historical context
```

**How it works:**
1. Scans `~/.claude/projects/*/conversation/` for transcripts
2. Uses extraction patterns to detect decisions/research/plans
3. Extracts and appends to decisions.yaml
4. Deduplicates (won't add same decision twice)

**Already populated:** Check current state:
```bash
# See what's already in decisions.yaml
uv run scripts/decision-query.py --all
```

---

## Token Efficiency

### Context Loading Comparison

**Old approach (CHANGELOG.md):**
```
Import entire CHANGELOG: 150K tokens
Problem: Loads everything, most irrelevant
Cost: High context usage
```

**New approach (decisions.yaml with queries):**
```
Query specific topic: 2-5K tokens (83-97% reduction!)
Example: decision-query.py --topic "authentication"
Loads: Only relevant 2-3 entries
```

### Selective Loading Strategy

**Scenario 1: Starting authentication work**
```bash
# Query for authentication context
uv run scripts/decision-query.py --topic "authentication"

# Loads:
- Research: Authentication libraries (if exists)
- Decisions: Auth approach decisions (if exists)
- Plans: Auth implementation plans (if exists)

# Total: ~3K tokens vs 150K full CHANGELOG
```

**Scenario 2: User asks "why did we choose X?"**
```bash
# Query for specific decision
uv run scripts/decision-query.py --topic "DRY strategy"

# Loads: Single decision with full context
# Total: ~1K tokens
```

---

## Integration with Hooks

### SessionEnd Hook (Automatic)

**session_end_extractor.py** already extracts to decisions.yaml:
- Detects decisions in conversation (## Decision: pattern)
- Extracts structured data
- Appends to decisions.yaml automatically

**You don't need to do anything** - it happens automatically at session end!

### What You Should Do

**During conversation:**
1. Output decisions in extraction-optimized format (see output style)
2. SessionEnd hook extracts automatically
3. Next session, query for context if needed

---

## Examples

### Example 1: Before Researching Libraries

```
User: "Research best state management libraries for React"

You: Let me check if we already researched this.

[Run decision-query.py --topic "state management" --type research]

Result: Found existing research from 2 months ago
  - Compared: Redux, Zustand, Jotai, Valtio
  - Recommendation: Zustand for simple apps, Jotai for complex
  - Tags: [react, state-management, libraries]

You: We already researched this! Here's what we found:
     [Load 2K tokens vs spending $0.07 to research again]
```

### Example 2: Before Making Architecture Decision

```
User: "Should we use microservices or monolith?"

You: Let me check if we already decided on architecture approach.

[Run decision-query.py --topic "architecture" --type decisions]

Result: Found decision "dec-002-monolith-first"
  - Decision: Start with modular monolith
  - Rationale: Team size <5, single deployment simpler
  - Status: accepted
  - Date: 2025-09-15

You: We already decided this! Here's the context:
     [Load 1K tokens vs re-discussing for 30 minutes]
```

### Example 3: Before Planning Feature

```
User: "Plan implementation for user dashboard"

You: Let me check for existing plans.

[Run decision-query.py --topic "dashboard" --type plans]

Result: Found plan "plan-005-dashboard-v1"
  - Status: completed
  - Summary: "5 tasks implemented, merged to main"
  - Created: 2025-10-01

You: We already implemented this! Let me load the existing plan.
     [Load 3K tokens, reference existing work]
```

---

## Lifecycle Management

**Research entries expire after 6 months:**
- Rationale: Technology evolves, best practices change
- Old research becomes stale (2024 → 2025 practices differ)
- Expired entries moved to archives

**Plans archive 90 days after completion:**
- Rationale: Useful during implementation, less useful after
- Completed plans moved to docs/archive/

**Decisions never auto-expire:**
- Unless explicitly superseded by new decision
- Architectural decisions stay relevant

**Check lifecycle status:**
```bash
# See active vs expired entries
uv run scripts/decision-query.py --show-expired
```

---

## Cost Impact

**Annual savings (assuming 50 research sessions):**
```
Old: 50 × $0.07 = $3.50 in redundant research
New: Query first (free), research only if needed
Savings: ~$3.00/year + avoid 25 hours of redundant work
```

**Token savings per query:**
```
Load full CHANGELOG: 150K tokens
Load specific query: 2-5K tokens
Savings: 97% reduction per lookup
```

---

## Quick Reference

**Check before researching:**
```bash
uv run scripts/decision-query.py --topic "{topic}" --type research
```

**Check before deciding:**
```bash
uv run scripts/decision-query.py --topic "{topic}" --type decisions
```

**Check before planning:**
```bash
uv run scripts/decision-query.py --topic "{topic}" --type plans
```

**See all active context:**
```bash
uv run scripts/decision-query.py --all
```

---

## Integration Points

1. **Before /ctx:research** - Query for existing research first
2. **Before /ctx:plan** - Query for existing plans first
3. **Before /ctx:design** - Query for existing decisions first
4. **When user asks "why"** - Query for decision rationale
5. **At SessionEnd** - Automatic extraction (no action needed)

---

## Summary

**Key principle:** Query before doing work that might already be done.

**Benefits:**
- 83-97% token reduction for context loading
- Avoid $0.07 redundant research
- Consistent decisions across sessions
- Queryable, structured context
- Auto-populated from conversation history

**Remember:** decisions.yaml is plugin-local, works for all users who install Contextune!
