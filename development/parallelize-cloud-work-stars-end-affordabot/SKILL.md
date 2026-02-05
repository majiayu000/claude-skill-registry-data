---
name: parallelize-cloud-work
description: |
  Delegate independent work to Claude Code Web cloud sessions for parallel execution. Generates comprehensive session prompts with context exploration guidance, verifies Beads state, provides tracking commands. Use when user says "parallelize work to cloud", "start cloud sessions", or needs to execute multiple independent tasks simultaneously, or when user mentions cloud sessions, cloud prompts, delegate to cloud, Claude Code Web, generate session prompts, parallel execution, or asks "how do I use cloud sessions".
tags: [workflow, cloud, parallelization, dx]
---

# Parallelize Cloud Work Skill

**Purpose:** Generate comprehensive prompts for Claude Code Web cloud sessions with strong context exploration guidance.

## Activation

**Triggers:**
- "parallelize work to cloud"
- "start cloud sessions for these issues"
- "delegate these to the cloud"
- "generate cloud sessions"
- "create cloud session prompts"
- "generate session prompts"

**User provides:** Issue IDs (bd-xyz, bd-abc, ...)

## Key Innovation: Context-First Prompts

**Problem from PR #196 (bd-205):**
Cloud Session C immediately implemented ticker normalization without discovering:
- `security_resolver_eodhd_first.py` had better existing logic
- `eodhd.py` already had `search_by_cusip()` and `search_by_isin()` methods
- Result: 2 commits, wasted effort, wrong approach

**Root Cause:** No context exploration before implementation.

**Solution:** Generated prompts MUST include:

```
🚨 CRITICAL: EXPLORE BEFORE IMPLEMENTING 🚨

Before writing ANY code, you MUST:

1. **Identify relevant context skills**
   - List all .claude/skills/context-*/ directories
   - Match skill descriptions to your task keywords
   - Invoke ALL relevant context skills (usually 2-3)

2. **Explore existing code**
   - Read context skill file lists
   - Use Serena to search for related functionality
   - Check for existing implementations you can extend

3. **Document discoveries**
   - List existing files that relate to your task
   - Note existing APIs/functions you can reuse
   - Identify patterns to follow

4. **Plan approach**
   - Decide: extend existing code OR create new?
   - If extending: which files/functions?
   - If new: why can't existing code be reused?

**Example for Symbol Resolution task:**
- Invoke: context-symbol-resolution (covers security resolver)
- Invoke: context-eodhd-integration (EODHD API patterns)
- Explore: backend/services/security_resolver_eodhd_first.py
- Discover: search_by_cusip(), search_by_isin() already exist
- Plan: Use existing methods, don't reimplement

**Rule:** If you implement something that already exists in codebase,
you've failed the exploration phase. Start over.
```

## Workflow

### 1. Analyze Issues

For each issue ID:
```bash
bd show <issue-id>
```

Check:
- **Dependencies:** `bd show <id> | grep -A 5 "Dependencies"`
  - If issues depend on each other → ERROR, not parallelizable
  - Must be fully independent
- **Status:** Must be `open`
- **Assignee:** Suggest `claude-code` if unassigned

### 2. Verify Beads in Master

**Critical:** Cloud needs latest Beads state.

```bash
# Export current state
bd export --force

# Check for uncommitted changes
git status .beads/issues.jsonl
```

**If uncommitted changes exist:**
```
⚠️ Beads JSONL has uncommitted changes!

Cloud sessions will NOT see these issues unless they're in master.

REQUIRED STEPS:
1. Commit: git add .beads/issues.jsonl && git commit -m "chore: Update Beads issues"
2. Push: git push origin master
3. Verify: GitHub shows .beads/issues.jsonl updated
4. THEN start cloud sessions

Why: Cloud clones master branch, needs committed Beads state.
```

### 3. Identify Context Skills for Each Issue

**Use semantic matching from Beads description:**

| Issue Keywords | Context Skills to Invoke |
|----------------|-------------------------|
| "security resolver", "symbol", "CUSIP", "ISIN" | context-symbol-resolution, context-eodhd-integration |
| "Plaid", "account linking" | context-plaid-integration, context-brokerage |
| "SnapTrade", "brokerage" | context-snaptrade-integration, context-brokerage |
| "database", "schema", "migration" | context-database-schema |
| "API endpoint", "REST" | context-api-contracts |
| "frontend", "UI", "component" | context-ui-design |
| "analytics", "metrics" | context-analytics |
| "portfolio", "holdings" | context-portfolio |
| "EODHD", "market data", "prices" | context-eodhd-integration |
| "CI", "Railway", "deployment" | context-infrastructure |
| "authentication", "Clerk" | context-clerk-integration |

**Add to prompt:**
```
**STEP 1: INVOKE CONTEXT SKILLS**

Based on your task keywords, invoke these skills FIRST:
- <skill-name-1>: <reason>
- <skill-name-2>: <reason>

After invoking, read the file lists and explore related code.
```

### 4. Generate Session Prompts

Run:
```bash
poetry run python scripts/generate-cloud-prompts.py <issue-id-1> <issue-id-2> ...
```

**Prompt Structure:**

```
================================================================================
SESSION {A/B/C} PROMPT - Copy everything below this line
================================================================================

CLOUD SESSION {A/B/C} - {issue_title} ({issue_id})

Repository: stars-end/prime-radiant-ai
Branch Strategy: feature-{issue_id}-session-{a/b/c}

🚨 CRITICAL: EXPLORE BEFORE IMPLEMENTING 🚨

Before writing ANY code, you MUST:

1. **Identify relevant context skills**
   - Run: ls .claude/skills/context-*/
   - Match skill descriptions to your task
   - Invoke ALL relevant skills

   **For this task, invoke:**
   {context_skills_list}

2. **Explore existing code**
   - Read context skill file listings
   - Use Serena search_for_pattern to find related code
   - Check for existing implementations

3. **Document discoveries**
   - List existing files related to your task
   - Note existing APIs you can reuse
   - Identify code patterns to follow

4. **Plan approach**
   - Extend existing code OR create new? Why?
   - Which existing functions can you reuse?
   - What NEW code is actually needed?

**Example (Symbol Resolution):**
- Invoke context-symbol-resolution + context-eodhd-integration
- Explore: backend/services/security_resolver_eodhd_first.py
- Discover: search_by_cusip(), search_by_isin() exist
- Plan: Use existing, don't reimplement

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ISSUE: {issue_id} - {issue_title}

Priority: P{priority}
Type: {issue_type}
Assignee: {assignee}

{description}

{design_section if exists}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BRANCH INSTRUCTIONS:

**Create branch:**
```bash
git checkout -b feature-{issue_id}-session-{session_letter}
```

**For additional commits (fixes, iterations):**
- Use SAME branch: feature-{issue_id}-session-{session_letter}
- Do NOT create new branches
- Push to same branch → GitHub auto-updates PR

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WORKFLOW:

1. Clone repo: git clone https://github.com/stars-end/prime-radiant-ai.git
2. Checkout master: git checkout master
3. **EXPLORATION PHASE** (see above)
4. Create branch: git checkout -b feature-{issue_id}-session-{session_letter}
5. Implement changes
6. Commit with format:
   ```
   <type>: <summary> ({issue_id} session-{session_letter})

   <body>

   Feature-Key: {issue_id}
   Agent: claude-code
   Role: <appropriate-role>
   Session: {session_letter}
   ```
7. Push: git push origin feature-{issue_id}-session-{session_letter}
8. Create PR:
   ```bash
   gh pr create \
     --title "[Session {session_letter}] <type>: <summary> ({issue_id})" \
     --body "<detailed description>"
   ```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUCCESS CRITERIA:

- ✅ Context skills invoked BEFORE implementation
- ✅ Existing code discovered and reused
- ✅ PR created with "Session {session_letter}" identifier
- ✅ Feature-Key: {issue_id} in commit
- ✅ CI passes
- ✅ Changes match technical spec

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ESTIMATED TIME: {estimated_time}

================================================================================
END SESSION {A/B/C} PROMPT
================================================================================
```

### 5. Provide Copy/Paste Ready Prompts to User

**CRITICAL:** After generating all prompts, output each session prompt in a copy/paste ready format.

**Format:**
```
## SESSION A - Copy everything below this line

[Full prompt from step 4, including all separator lines]

---

## SESSION B - Copy everything below this line

[Full prompt from step 4, including all separator lines]

---

## SESSION C - Copy everything below this line

[Full prompt from step 4, including all separator lines]
```

**User Experience:**
- User should NOT have to open a file or manually extract prompts
- Each session block should be self-contained (includes all separators)
- User simply copies each block and pastes to Claude Code Web
- No manual editing required

**Why This Matters:**
- Reduces friction (one paste per session vs opening file + finding section)
- Prevents copy errors (missing lines, wrong session)
- Faster workflow (user can start all 3 sessions in <2 minutes)

### 6. Output Tracking Commands

```bash
# List all session PRs
gh pr list --search "session in:title"

# Check CI for all session PRs
gh pr list --search "is:open session in:title" --json number,title,url,statusCheckRollup

# View specific session PR
gh pr view <number>

# Monitor CI progress
gh pr checks <number> --watch
```

## Implementation Details

### scripts/generate-cloud-prompts.py

**Inputs:**
- Issue IDs from command line
- Beads issue metadata via `bd show --json`
- Git repo info via `git remote`

**Outputs:**
- Session prompts (A, B, C, ...) for each issue
- Each prompt includes:
  - Context skill guidance (matched from issue keywords)
  - Branch naming convention
  - Commit message format
  - Exploration checklist
  - Success criteria

**Context Skill Matching:**

```python
def identify_context_skills(issue: dict) -> list[tuple[str, str]]:
    """
    Match issue description/title keywords to context skills.

    Returns: [(skill_name, reason), ...]
    """
    description = issue.get('description', '').lower()
    title = issue.get('title', '').lower()
    combined = f"{title} {description}"

    skill_matches = []

    # Symbol resolution
    if any(kw in combined for kw in ['security resolver', 'symbol', 'cusip', 'isin', 'ticker']):
        skill_matches.append(('context-symbol-resolution', 'Symbol/security resolution'))

    # EODHD
    if any(kw in combined for kw in ['eodhd', 'market data', 'price', 'fundamental']):
        skill_matches.append(('context-eodhd-integration', 'EODHD API integration'))

    # Plaid
    if any(kw in combined for kw in ['plaid', 'account linking']):
        skill_matches.append(('context-plaid-integration', 'Plaid integration'))

    # SnapTrade
    if any(kw in combined for kw in ['snaptrade', 'brokerage']):
        skill_matches.append(('context-snaptrade-integration', 'SnapTrade integration'))

    # Database
    if any(kw in combined for kw in ['database', 'schema', 'migration', 'table']):
        skill_matches.append(('context-database-schema', 'Database schema'))

    # API
    if any(kw in combined for kw in ['api', 'endpoint', 'rest']):
        skill_matches.append(('context-api-contracts', 'API contracts'))

    # UI
    if any(kw in combined for kw in ['frontend', 'ui', 'component', 'react']):
        skill_matches.append(('context-ui-design', 'UI/UX design'))

    # Analytics
    if any(kw in combined for kw in ['analytics', 'metrics', 'tracking']):
        skill_matches.append(('context-analytics', 'Analytics'))

    # Portfolio
    if any(kw in combined for kw in ['portfolio', 'holdings', 'positions']):
        skill_matches.append(('context-portfolio', 'Portfolio management'))

    # Infrastructure
    if any(kw in combined for kw in ['ci', 'railway', 'deployment', 'infrastructure']):
        skill_matches.append(('context-infrastructure', 'Infrastructure'))

    # Clerk auth
    if any(kw in combined for kw in ['auth', 'clerk', 'authentication']):
        skill_matches.append(('context-clerk-integration', 'Clerk authentication'))

    # Brokerage
    if any(kw in combined for kw in ['brokerage', 'broker', 'account linking']):
        skill_matches.append(('context-brokerage', 'Brokerage connections'))

    # Testing
    if any(kw in combined for kw in ['test', 'ci', 'playwright']):
        skill_matches.append(('context-testing-infrastructure', 'Testing infrastructure'))

    return skill_matches
```

### Session Tracking

**Branch Convention:** `feature-bd-xyz-session-{a,b,c}`
- Lowercase session letter
- Tied to specific Beads issue
- Allows multiple sessions on same issue (rare but possible)

**PR Title:** `[Session A] <type>: <summary> (bd-xyz)`
- Session identifier in title for easy filtering
- GitHub search: `is:pr session in:title`

**Commit Message:**
```
<type>: <summary> (bd-xyz session-a)

<body>

Feature-Key: bd-xyz
Agent: claude-code
Role: <role>
Session: A
```

## Error Handling

### Issue Dependencies

```bash
# Check dependencies
bd show bd-xyz | grep -A 10 "Dependencies"
```

**If dependencies found:**
```
❌ ERROR: Issues have dependencies, cannot parallelize

bd-abc depends on bd-xyz (blocks)

You must:
1. Complete bd-xyz first
2. THEN work on bd-abc
3. Or re-scope issues to be independent
```

### Uncommitted Beads State

**If `.beads/issues.jsonl` has uncommitted changes:**

```
⚠️ Cloud sessions need committed Beads state!

Current: .beads/issues.jsonl modified locally
Problem: Cloud clones master, won't see your local issues

REQUIRED STEPS:
1. git add .beads/issues.jsonl
2. git commit -m "chore: Update Beads state for cloud sessions"
3. git push origin master
4. Verify: Check GitHub shows updated .beads/issues.jsonl
5. THEN paste cloud prompts

Why: Cloud sessions clone master branch on startup.
```

## Iterative Work Pattern

**Scenario:** Cloud PR needs additional commits (CI fixes, feedback)

**Solution:** Prompt already includes:

```
**For additional commits:**
- Use SAME branch: feature-bd-xyz-session-a
- Make changes and commit
- Push to same branch
- GitHub automatically updates PR
```

**Providing Feedback:**
1. Human reviews cloud PR on GitHub
2. Leaves comments with specific feedback
3. Update Beads issue with findings: `bd update bd-xyz --notes "CI failed: <details>"`
4. Regenerate prompt (includes updated notes)
5. Paste updated prompt to cloud
6. Cloud reads issue, implements fixes on same branch

## Success Criteria

- ✅ Generates N prompts for N issues
- ✅ Each prompt includes context skill guidance
- ✅ Exploration checklist prominent and required
- ✅ Branch reuse instructions clear
- ✅ Tracking commands provided
- ✅ Error handling for dependencies
- ✅ Verifies Beads state in master

## Related

- **bd-205:** Context skill activation analysis (why this matters)
- **context-dx-meta:** DX workflow patterns
- **sync-feature-branch:** Local commit workflow
- **create-pull-request:** PR creation pattern
