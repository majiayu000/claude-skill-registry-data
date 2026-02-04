---
name: smart-docs-updater
description: |
  Comprehensive documentation updater that tracks work sessions and updates ALL relevant docs.
  Accumulates multiple related changes into ONE coherent entry instead of fragmented updates.

  **Mandatory updates:** CHANGELOG.md, Build Records (if significant work)
  **Case-dependent:** Sprint plans, Bug reports, ROADMAP.md, Briefs/PRDs, QA/Testing docs

  Use this when:
  - User says "start working on X" or "fixing Y" (session start)
  - User says "done", "ship it", "finished with X" (session end - trigger docs update)
  - User asks to update changelog after multiple commits

  DO NOT update docs after every small change. Wait for session completion.
aliases:
  - changelog-readme-updater
  - docs-updater
---

# Smart Documentation Updater

## File Locations

### Documentation Index

**Start here to understand the full documentation structure:**
- **[docs/DOCUMENTATION.md](./docs/DOCUMENTATION.md)** — Master index of all documentation
- **[docs/DOCUMENTATION-MAP.md](./docs/DOCUMENTATION-MAP.md)** — How CLAUDE.md, docs/, and SOPs connect

### Mandatory Updates (Always Check)

| File | Path | Purpose |
|------|------|---------|
| **CHANGELOG.md** | `./CHANGELOG.md` (project root) | All notable changes |
| **Build Records** | `./docs/product/builds/{feature-name}/BUILD_RECORD.md` | Per-feature architecture docs |

### Conditional Updates (If Doc Exists for This Feature)

**Rule:** If a doc exists for the specific feature/bug/sprint being worked on → UPDATE IT.

| File | Path | Condition | Update Action |
|------|------|-----------|---------------|
| **Sprint Plans** | `./docs/product/sprints/active/{SPRINT}/` | Sprint doc exists for this work | Update progress, mark tasks complete |
| **Sprint Handovers** | `./docs/product/sprints/templates/HANDOVER_*.md` | Handover exists for this sprint | Add discovered patterns, gotchas |
| **Bug Reports** | `./docs/bugs/*.md` | Bug report exists for this fix | Add Resolution section |
| **Briefs** | `./docs/product/briefs/*-BRIEF.md` | Brief exists for this feature | Update if scope changed, add outcome |
| **PRDs** | `./docs/product/PRD/*.md` | PRD exists for this feature | Update if requirements evolved |
| **ROADMAP.md** | `./docs/product/ROADMAP.md` | Milestone complete, scope changed, or learnings | Update status, scope, or add learnings |
| **QA/Testing** | `./docs/product/sprints/qa/*.md` | QA doc exists for this area | Document test patterns, coverage |
| **Architecture Docs** | `./docs/architecture/*.md` | Prompt system changes (lib/ai/prompts/, coaching/, advisory/) | Update relevant architecture doc |
| **Design Docs** | `./docs/design/*.md` | UI component changes (components/ui/, components/crm/) | Update DESIGN-LANGUAGE.md or CRM-SYSTEM.md |
| **SOPs** | `./advisory/clients/CLIENT_SOP.md`, `.claude/skills/*/SKILL.md` | Workflow procedure changes | Update relevant SOP |

**IMPORTANT:** Always use the project root CHANGELOG.md, not any other location.

## Philosophy

**Problem:** Multiple commits for one fix = fragmented changelog entries
**Solution:** Session-based tracking + intelligent summarization

## Session Lifecycle

### 1. Session Start (Implicit or Explicit)

**Explicit start:**
- User says: "I'm going to fix the login bug" or "Starting work on feature X"
- Record the current git HEAD as session baseline

**Implicit start:**
- First code change in a conversation = session start
- Track from that point

**State tracking** (in memory or `.claude/session-state.json`):
```json
{
  "session_id": "2025-12-25-login-fix",
  "started_at": "2025-12-25T12:00:00Z",
  "baseline_commit": "abc1234",
  "work_description": "Fixing login authentication flow",
  "changes_made": []
}
```

### 2. During Session (Accumulate, Don't Update)

As user works:
- Track files modified (from Edit/Write tool calls)
- Track commits made
- Note the problem being solved
- **DO NOT update CHANGELOG.md yet**

If user asks "update the changelog" mid-session:
- Ask: "Are you done with this work session, or still making changes?"
- If still working: "I'll wait until you're done to create one coherent entry"
- If done: Proceed to session end

### 3. Session End (Trigger Documentation Update)

**Trigger phrases:**
- "done", "finished", "ship it", "that's it", "complete"
- "update the docs now", "wrap this up"
- "commit and document this"

**Process:**

#### Step 1: Analyze All Changes Since Baseline
```bash
# Get all commits since session start
git log --oneline ${baseline_commit}..HEAD

# Get consolidated diff
git diff ${baseline_commit}..HEAD --stat

# Get detailed changes
git diff ${baseline_commit}..HEAD --name-status
```

#### Step 2: Intelligently Categorize

Group changes by TYPE (not by commit):

| Category | When to Use |
|----------|-------------|
| **Added** | New features, new files, new capabilities |
| **Fixed** | Bug fixes, error corrections |
| **Changed** | Refactors, behavior changes, updates |
| **Removed** | Deprecated features, deleted code |
| **Security** | Security-related fixes |
| **Performance** | Optimization changes |

#### Step 3: Create ONE Coherent Entry

**Bad (fragmented):**
```markdown
### Fixed
- Fix login button click handler
- Add null check to auth function
- Update error message for login
- Fix edge case in token validation
```

**Good (intelligent summary):**
```markdown
### Fixed
- **Authentication flow**: Resolved login failures caused by null token handling and edge cases in validation. Improved error messaging for failed attempts. (lib/auth/, components/login/)
```

#### Step 4: Update CHANGELOG.md

Insert under `## [Unreleased]` section:

```markdown
## [Unreleased]

### Fixed
- **Authentication flow**: Resolved login failures caused by null token handling
  and edge cases in validation. Improved error messaging.
  ([#issue] if applicable)
```

#### Step 5: Update README.md (If Applicable)

Only update if:
- New user-facing features added
- API changes that affect usage
- New dependencies or requirements
- Installation steps changed

Skip if:
- Internal refactors
- Bug fixes with no API changes
- Performance improvements

### 4. Multi-Problem Sessions

If user works on MULTIPLE unrelated issues in one session:

**Detection:**
- Commits touch completely different areas
- User explicitly mentions multiple issues
- Long time gaps between commit clusters

**Handling:**
- Create SEPARATE changelog entries for each logical unit
- Group by feature/area, not by time

**Example output:**
```markdown
## [Unreleased]

### Fixed
- **Authentication**: Resolved token validation edge cases (lib/auth/)
- **CRM Display**: Fixed company name truncation in sidebar (components/crm/)

### Changed
- **Memory System**: Optimized compression for large conversations (lib/memory/)
```

## Commands Reference

| User Says | Action |
|-----------|--------|
| "I'm fixing X" | Start session, record baseline |
| "Working on feature Y" | Start session, record baseline |
| "Done" / "Ship it" | End session, update docs |
| "Update changelog" | Ask if done, then update |
| "What have I changed?" | Summarize changes since baseline |
| "Nevermind, discard" | Clear session, no docs update |

## Quality Guidelines

### Changelog Entries Should Be:

1. **User-focused**: What impact does this have?
2. **Concise**: One line summary, details optional
3. **Grouped**: Related changes = one entry
4. **Traceable**: Include file paths or issue numbers
5. **Present tense**: "Fix X" not "Fixed X"

### Avoid:

- Entry per commit
- Implementation details users don't care about
- Duplicate entries for the same fix
- Updating docs before work is complete

## Edge Cases

### User Forgets to "End" Session
- If new unrelated work starts, auto-close previous session
- Or ask: "Should I document the previous work before we start this?"

### Work Spans Multiple Days
- Session state persists across conversations
- Use git history as source of truth
- Baseline commit is the key reference point

### Merge Conflicts in CHANGELOG
- Always read current CHANGELOG.md before updating
- Insert new entries at the TOP of [Unreleased]
- Preserve existing entries

## Integration with Sprint System

If project uses sprint tracking (like this one):
- Cross-reference sprint IDs in changelog entries
- Link to sprint docs where applicable

```markdown
### Added
- **Company Brain context optimization** (M50): Token-efficient company
  chats with searchable files. See [sprint docs](docs/product/sprints/completed/M50/)
```

## Build Record Integration

Build Records capture per-feature architecture, decisions, and progress. They complement the CHANGELOG by providing deep context.

### When to Create/Update Build Records

| Scenario | Action |
|----------|--------|
| New feature implementation | Create new build record in `docs/product/builds/{feature-name}/` |
| Bug fix sprint | Create build record documenting what was fixed and why |
| Significant refactor | Create build record with design decisions |
| Session completion | Check if relevant build record needs progress update |

### Build Record Workflow

#### Step 1: Check for Existing Build Record
```bash
# Check if build record exists for current work
ls docs/product/builds/*/BUILD_RECORD.md
```

#### Step 2: Create if Needed
If working on a feature without a build record:
1. Create directory: `docs/product/builds/{feature-name}/`
2. Copy template: `cp docs/product/builds/BUILD_RECORD_TEMPLATE.md docs/product/builds/{feature-name}/BUILD_RECORD.md`
3. Fill in sections as you work

#### Step 3: Update on Session End
When session ends, update the build record with:
- **Progress Log**: What was accomplished this session
- **Design Decisions**: Any trade-offs or choices made
- **Key Files**: New files added or modified
- **Retrospective**: (if marking complete) Lessons learned

### Build Record vs CHANGELOG

| CHANGELOG | Build Record |
|-----------|--------------|
| What changed (user-facing) | Why it was built this way |
| Brief, one-line entries | Detailed architecture |
| Chronological | Per-feature |
| For users/reviewers | For future developers |

### Example Session End Workflow

1. **Update CHANGELOG.md** with user-facing changes
2. **Check for build record** at `docs/product/builds/{feature}/BUILD_RECORD.md`
3. **If exists**: Append to Progress Log, update Key Files
4. **If doesn't exist and significant work**: Create one
5. **Commit both together**

### Commit Tracking Hook

A PostToolUse hook logs commits to `.context/state/commits-pending-build-record.json`.
Check this file when user says "done" to see if build records need updating.

```bash
# Check pending commits
cat .context/state/commits-pending-build-record.json 2>/dev/null || echo "No pending commits"
```

---

## Comprehensive Session-End Checklist

When user says "done", "ship it", or similar, run through this checklist.

**Core Principle:** Understand WHAT was built → Cross-reference ROADMAP → Find ALL related docs → Update them.

### Step 1: Context Discovery (Understand the Work)

First, understand the scope of work completed:

```bash
# 1. Get recent commits to understand what was done
git log --oneline -10

# 2. Extract identifiers from commits (sprint IDs, feature names)
# Look for patterns like: M138, feature-name, bug-fix-name
git log --oneline -10 | grep -oE 'M[0-9]+|feat\([^)]+\)|fix\([^)]+\)'

# 3. Get all files changed to understand scope
git diff --name-only $(git log --oneline -10 | tail -1 | cut -d' ' -f1)..HEAD
```

### Step 2: Cross-Reference ROADMAP

Read the ROADMAP to understand where this work fits:

```bash
# Read the roadmap to understand milestones and features
cat docs/product/ROADMAP.md
```

**Questions to answer:**
- Is this work part of a tracked milestone (e.g., "M138: Tool Feedback Loop")?
- Does this complete a feature listed in the roadmap?
- Is this a bug fix for a known issue?
- Is this part of an ongoing sprint?

**Extract keywords from roadmap that match your work:**
- Sprint/milestone IDs: M138, M137, etc.
- Feature names: "tool feedback loop", "knowledge review", etc.
- System areas: "company brain", "context intelligence", etc.

### Step 3: Find ALL Related Docs

Using keywords from Steps 1-2, search across all doc types:

```bash
# Set your feature identifiers (from Steps 1-2)
FEATURE="m138"
KEYWORDS="tool feedback loop provenance"

# Search across all doc locations
echo "=== Sprint Docs ==="
ls docs/product/sprints/active/ 2>/dev/null | grep -iE "$FEATURE|feedback|provenance" || echo "None"
ls docs/product/sprints/completed/ 2>/dev/null | grep -iE "$FEATURE|feedback|provenance" || echo "None"

echo "=== Bug Reports ==="
ls docs/bugs/ 2>/dev/null | grep -iE "$FEATURE|feedback|provenance" || echo "None"

echo "=== Briefs ==="
ls docs/product/briefs/ 2>/dev/null | grep -iE "$FEATURE|feedback|provenance" || echo "None"

echo "=== PRDs ==="
ls docs/product/PRD/ 2>/dev/null | grep -iE "$FEATURE|feedback|provenance" || echo "None"

echo "=== Build Records ==="
ls docs/product/builds/ 2>/dev/null | grep -iE "$FEATURE|feedback|provenance" || echo "None"

echo "=== QA/Testing ==="
ls docs/product/sprints/qa/ 2>/dev/null | grep -iE "$FEATURE|feedback|provenance" || echo "None"

echo "=== Architecture Docs ==="
ls docs/architecture/ 2>/dev/null | grep -iE "$FEATURE|prompt|coaching|advisory" || echo "None"

echo "=== Design Docs ==="
ls docs/design/ 2>/dev/null | grep -iE "$FEATURE|design|crm|ui" || echo "None"

echo "=== SOPs ==="
ls advisory/clients/ 2>/dev/null | grep -iE "SOP|procedure" || echo "None"
ls .claude/skills/ 2>/dev/null | grep -iE "$FEATURE" || echo "None"

echo "=== ROADMAP References ==="
grep -in "$FEATURE" docs/product/ROADMAP.md || echo "Not in roadmap"
```

### Step 4: Mandatory Updates (Always)

```bash
# 1. CHANGELOG.md - Always update
# Insert entry under ## [Unreleased]

# 2. Build Record - Create or update if significant work
ls docs/product/builds/*/BUILD_RECORD.md | grep -i "{feature-keyword}"
# If exists: Update Progress Log
# If not and significant: Create new
```

### Step 5: Update ALL Found Docs

For each doc found in Step 3, apply the appropriate update:

#### Sprint Plans/Handovers (if found)
- Update "Daily Progress" section with accomplishments
- Mark completed tasks with [x] in "Backlog" section
- Add discovered gotchas to handover

#### Bug Reports (if found)
Add a "Resolution" section:
```markdown
## Resolution (YYYY-MM-DD)

**Fixed in:** commit-hash or sprint-id
**Root cause:** Brief explanation
**Solution:** What was done
**Files changed:** List key files
```

#### Briefs (if found)
Add an "Outcome" section at the bottom:
```markdown
## Outcome (YYYY-MM-DD)

**Implemented in:** M138 / commit-hash
**Final approach:** Brief description of what was built
**Deviations from brief:** Any scope changes or approach changes
**Build Record:** [Link to build record if exists]
```

#### PRDs (if found)
- Update status field if PRD has one
- Add implementation notes if requirements evolved
- Link to build record

#### ROADMAP.md (if milestone tracked OR scope changed OR learnings)
Update the roadmap when:
1. **Milestone completed** → Mark status as Complete, add date
2. **Scope changed** → Update milestone description, add/remove items
3. **New learnings** → Add notes about discovered complexity, dependencies, or blockers

```markdown
## M138: Tool Feedback Loop
**Status:** ✅ Complete (Jan 24, 2026)
**Scope change:** Originally included UI integration; deferred to M140
**Learnings:** Feedback loop was implemented but never wired up - audit discovered disconnected code
```

#### QA/Testing Docs (if found)
- Document new test patterns
- Update coverage notes
- Add test utilities documentation

#### Architecture Docs (if prompt system changed)
When modifying files in `lib/ai/prompts/`, `lib/ai/coaching/`, `lib/ai/advisory/`, or `lib/ai/chat/`:
- Update relevant doc in `docs/architecture/`
- For module changes: Update `01-prompt-module-system.md`
- For coaching/advisory: Update `05-coaching-advisory.md`
- For context changes: Update `03-context-intelligence.md`

#### Design Docs (if UI changed)
When modifying files in `components/ui/`, `components/crm/`, or `app/` pages:
- Update `docs/design/DESIGN-LANGUAGE.md` for new patterns
- Update `docs/design/CRM-SYSTEM.md` for CRM-specific changes
- Add new CVA variants or component patterns discovered

#### SOPs (if workflow procedures changed)
When modifying operational workflows:
- Update `advisory/clients/CLIENT_SOP.md` for client procedures
- Update relevant `.claude/skills/*/SKILL.md` for agent procedures
- Update `docs/modules/infrastructure/crm-system/migration-sop.md` for data migrations

---

## Quick Reference: Intelligent Doc Update Flow

```
Session End Triggered ("done", "ship it")
        │
        ▼
┌─────────────────────────────────────────────────────┐
│  STEP 1: CONTEXT DISCOVERY                          │
│  - Review recent commits                            │
│  - Extract sprint IDs (M138, M137...)               │
│  - Extract feature keywords                         │
└─────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────┐
│  STEP 2: CROSS-REFERENCE ROADMAP                    │
│  - Read docs/product/ROADMAP.md                     │
│  - Find matching milestones/features                │
│  - Understand where this work fits                  │
└─────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────┐
│  STEP 3: SEARCH ALL DOC LOCATIONS                   │
│  Using keywords from Steps 1-2, search:             │
│  - docs/product/sprints/active/                     │
│  - docs/product/sprints/completed/                  │
│  - docs/bugs/                                       │
│  - docs/product/briefs/                             │
│  - docs/product/PRD/                                │
│  - docs/product/builds/                             │
│  - docs/product/sprints/qa/                         │
│  - docs/architecture/                               │
│  - docs/design/                                     │
│  - advisory/clients/ (SOPs)                         │
│  - .claude/skills/ (Skill SOPs)                     │
└─────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────┐
│  STEP 4: MANDATORY UPDATES                          │
│  ✅ CHANGELOG.md → Always update                    │
│  ✅ Build Record → Create/update if significant     │
└─────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────┐
│  STEP 5: UPDATE ALL FOUND DOCS                      │
│                                                     │
│  For EACH doc found in Step 3:                      │
│  ┌─────────────────────────────────────────────┐    │
│  │ Sprint Plan exists?  → Update progress/tasks│    │
│  │ Sprint Handover?     → Add gotchas/patterns │    │
│  │ Bug Report exists?   → Add Resolution       │    │
│  │ Brief exists?        → Add Outcome section  │    │
│  │ PRD exists?          → Update status/notes  │    │
│  │ ROADMAP reference?   → Update status/scope  │    │
│  │ QA Doc exists?       → Document patterns    │    │
│  │ Architecture Doc?    → Update system design │    │
│  │ Design Doc exists?   → Update UI patterns   │    │
│  │ SOP exists?          → Update procedures    │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

**Key Insight:** Don't ask "should I update X?" — Instead, **search for X** and if it exists for this feature, update it.

---

## Example Complete Session End

### Example 1: Feature with Existing Docs

```markdown
## Session End: M138 Tool Feedback Loop

### Step 1: Context Discovery
Commits: 9aa4c78, e0f1d4d
Keywords extracted: M138, tool feedback loop, provenance

### Step 2: Cross-Reference ROADMAP
Found in ROADMAP.md: "M138: Tool Feedback Loop - Provenance Tracking"
Status: In Progress → Should mark Complete

### Step 3: Found Related Docs
- Sprint: docs/product/sprints/active/M138-TOOL-FEEDBACK/ ✅ Found
- Brief: docs/product/briefs/CONTEXT-MEMORY-INTEGRATION-BRIEF.md ✅ Found (related)
- Bug Report: None
- Build Record: docs/product/builds/m138-tool-feedback-provenance/ ✅ Found

### Step 4: Mandatory Updates
- [x] CHANGELOG.md - Added M138 entry
- [x] Build Record - Updated progress log

### Step 5: Updated Found Docs
- [x] Sprint Plan - Marked tasks complete, updated daily progress
- [x] Brief - Added Outcome section linking to build record
- [x] ROADMAP.md - Marked M138 as Complete with date

### Commits
- 9aa4c78 feat(M138): Add provenance tracking to tool feedback loop
- e0f1d4d docs(M138): Add build record with audit findings
- abc1234 docs: Update sprint/brief/roadmap for M138 completion
```

### Example 2: Bug Fix with Report

```markdown
## Session End: Fix stuck chat context building

### Step 1: Context Discovery
Commits: b42adc7 fix(M135)
Keywords extracted: M135, stuck chat, context building, timeout

### Step 2: Cross-Reference ROADMAP
Found: M135 Chat Reliability sprint

### Step 3: Found Related Docs
- Bug Report: docs/bugs/CRITICAL-stuck-chat-context-building-failure.md ✅ Found
- Sprint: docs/product/sprints/active/M135-CHAT-RELIABILITY/ ✅ Found
- Build Record: None (should create)

### Step 4: Mandatory Updates
- [x] CHANGELOG.md - Added bug fix entry
- [x] Build Record - Created new for M135

### Step 5: Updated Found Docs
- [x] Bug Report - Added Resolution section with root cause and fix
- [x] Sprint Plan - Marked fix task complete

### Commits
- b42adc7 fix(M135): Prevent stuck chats with timeouts
- xyz9876 docs: Add resolution to bug report, update sprint
```
