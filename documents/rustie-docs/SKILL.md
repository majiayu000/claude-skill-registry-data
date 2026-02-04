---
name: rustie-docs
description: Documentation management skill for audit, creation, and maintenance. Enforces documentation standards, checks for staleness and broken references, auto-fixes issues, and ensures docs are created in correct locations. Use when user says "check docs", "audit docs", "fix docs", "create doc", "archive docs", or when scattered .md files are detected.
---

# Rustie Docs Skill

Documentation management for Rustie Method projects. Ensures docs are:
- In correct locations (agent-docs/ structure)
- Have proper frontmatter
- Not stale or broken
- Clearly marked as permanent or ephemeral

## Quick Reference - All Modes

| Mode | Trigger | Purpose |
|------|---------|---------|
| `audit` | "check docs", "audit docs" | Find issues (stale, broken refs, misplaced) |
| `fix` | "fix docs", "clean docs" | Auto-fix issues from audit |
| `create` | "create doc for X" | Create new doc in correct location |
| `archive` | "archive docs", "cleanup old docs" | Archive ephemeral docs |
| `sync` | "sync docs", "update readme" | Sync README pointers, check consistency |

---

## Documentation Structure

### Allowed Locations

```
project-root/
├── README.md           ✅ Front door (required)
├── CLAUDE.md           ✅ AI instructions (optional)
├── CONTRIBUTING.md     ✅ Contribution guide (optional)
├── LICENSE.md          ✅ License (optional)
├── CHANGELOG.md        ✅ Changes (optional)
├── *.md                ❌ BLOCKED - must go in agent-docs/
│
└── agent-docs/
    ├── AI.md                   ✅ Required: How AI uses this repo
    ├── architecture.md         ✅ Required: System map
    ├── glossary.md             ✅ Optional: Domain terms
    │
    ├── features/               ✅ Feature documentation
    │   └── [feature]/
    │       ├── PRD.md          (permanent)
    │       ├── plan.md         (permanent until archived)
    │       ├── assumptions.md  (permanent until archived)
    │       ├── active-context.md (session)
    │       ├── sessions/       (ephemeral - archivable)
    │       ├── decisions/      (permanent ADRs)
    │       └── _ephemeral/     (auto-cleanable)
    │
    ├── decisions/adrs/         ✅ Global ADRs (permanent)
    ├── lessons/                ✅ Lessons learned (permanent)
    ├── instructions/           ✅ How-to guides (permanent)
    ├── reference/              ✅ Reference docs (permanent)
    ├── templates/              ✅ Doc templates (permanent)
    ├── archives/               ✅ Archived content
    └── _ephemeral/             ✅ Auto-cleanable scratch space
```

### Document Lifecycles

Every doc in agent-docs/ MUST have a `lifecycle:` field in frontmatter:

| Lifecycle | Meaning | Location Examples |
|-----------|---------|-------------------|
| `permanent` | Kept until explicitly deleted | PRD.md, ADRs, lessons |
| `session` | Valid for current feature work | active-context.md, handoffs |
| `ephemeral` | Auto-archivable after threshold | verify-reports, screenshots |

### Required Frontmatter

```yaml
---
title: Document Title
lifecycle: permanent | session | ephemeral
created: YYYY-MM-DD
updated: YYYY-MM-DD
owner: feature-name | global
references:              # Optional: files this doc references
  - src/auth/index.ts
  - agent-docs/decisions/adrs/ADR-001.md
---
```

---

## Mode: Audit

**Triggers**: "check docs", "audit docs", "audit documentation", "doc health"

Find issues in project documentation.

### What Gets Checked

| Check | Type | Description |
|-------|------|-------------|
| Root .md files | ERROR | .md in root except allowed list |
| Missing frontmatter | ERROR | No YAML frontmatter |
| Missing lifecycle | ERROR | No lifecycle field |
| Broken references | ERROR | Referenced files don't exist |
| Stale docs | WARNING | Updated > 30 days ago |
| Old ephemeral | WARNING | In `_ephemeral/` or `sessions/` > 7 days |
| Missing AI.md | WARNING | No agent-docs/AI.md |
| Missing architecture.md | WARNING | No agent-docs/architecture.md |

### Steps

1. **Run audit script**:
   ```bash
   python3 ~/.claude/scripts/rustie-doc-audit.py
   ```

2. **Parse results** and categorize:
   - Errors (blocking - must fix)
   - Warnings (recommended fixes)
   - Info (suggestions)

3. **Display report**:
   ```
   RUSTIE DOCS AUDIT
   ═══════════════════════════════════════════════════════════════

   Scanned: 47 documents
   Issues: 8 found (3 errors, 5 warnings)

   ERRORS:
     [E1] agent-docs/features/auth/plan.md
          Missing lifecycle field in frontmatter
          Fix: Add "lifecycle: permanent" to frontmatter

     [E2] design-notes.md (in root)
          Should be in agent-docs/
          Fix: git mv design-notes.md agent-docs/reference/design-notes.md

   WARNINGS:
     [W1] agent-docs/features/auth/sessions/session-20251201/handoff.md
          28 days old - consider archiving

   AUTO-FIXABLE: 5 issues
   Run "/rustie-docs fix" to apply automatic fixes
   ═══════════════════════════════════════════════════════════════
   ```

4. **Ask about fixes**:
   - If errors found: "Would you like me to fix these issues?"
   - If only warnings: "No blocking issues. Archive old docs?"

---

## Mode: Fix

**Triggers**: "fix docs", "clean docs", "fix documentation issues"

Auto-fix issues found during audit.

### What Can Be Fixed Automatically

| Issue | Fix |
|-------|-----|
| Missing frontmatter | Add template frontmatter (prompt for lifecycle) |
| Missing lifecycle | Prompt user to select, then add |
| Misplaced root .md | `git mv` to agent-docs/reference/ |
| Broken references | Remove from frontmatter (with confirmation) |
| Old ephemeral docs | Move to archives/ |

### What Requires Manual Action

| Issue | Why |
|-------|-----|
| Stale content | Human must verify if content is still accurate |
| Ambiguous destination | Multiple valid locations |
| ADR conflicts | Requires decision |

### Steps

1. **Run audit first** (if not already run):
   ```bash
   python3 ~/.claude/scripts/rustie-doc-audit.py --json
   ```

2. **Group fixable issues**:
   - Frontmatter additions
   - File moves
   - Reference cleanups
   - Archive operations

3. **For each fixable issue**, apply fix:
   ```bash
   # Adding frontmatter
   # (prepend YAML block to file)

   # Moving files
   git mv old/path.md new/path.md

   # Archiving
   mkdir -p agent-docs/archives/ephemeral-$(date +%Y%m%d)
   git mv agent-docs/features/x/_ephemeral/* agent-docs/archives/ephemeral-$(date +%Y%m%d)/
   ```

4. **Commit changes**:
   ```bash
   git add agent-docs/
   git commit -m "docs: fix documentation issues (rustie-docs)"
   ```

5. **Report results**:
   ```
   RUSTIE DOCS FIX COMPLETE
   ═══════════════════════════════════════════════════════════════

   Fixed: 5 issues
     ✓ Added frontmatter to 2 files
     ✓ Moved 1 file from root to agent-docs/reference/
     ✓ Archived 2 old session directories

   Remaining: 3 issues (require manual action)
     • agent-docs/architecture.md may be stale (45 days)
     • agent-docs/reference/old-guide.md references deleted file

   ═══════════════════════════════════════════════════════════════
   ```

---

## Mode: Create

**Triggers**: "create doc for X", "new doc", "add documentation for X"

Create new documentation in the correct location with proper structure.

### Steps

1. **Ask document type** (use AskUserQuestion):
   ```
   What type of document?

   1. Feature PRD - Requirements for a new feature
   2. Feature Plan - Implementation plan with tasks
   3. ADR - Architecture Decision Record
   4. Lesson - Lessons learned from failure
   5. Reference - General reference documentation
   6. Subsystem README - Documentation for a code module
   7. Instruction/Checklist - How-to guide
   ```

2. **Based on type, gather info**:

   **For Feature PRD/Plan**:
   - Feature name
   - Create feature directory if needed
   - Copy from template

   **For ADR**:
   - Decision title
   - Feature-specific or global?
   - Get next ADR number

   **For Lesson**:
   - Lesson title
   - Severity (high/medium/low)
   - Trigger keywords

   **For Subsystem README**:
   - Module path (src/X/)
   - Module name
   - Dependencies

3. **Create file with frontmatter**:
   ```yaml
   ---
   title: [Title]
   lifecycle: permanent
   created: [today]
   updated: [today]
   owner: [feature or global]
   ---
   ```

4. **Apply appropriate template** (from agent-docs/templates/)

5. **Report**:
   ```
   Created: agent-docs/features/auth/PRD.md

   Next steps:
   1. Fill in the [TODO] sections
   2. Run "/rustie-docs audit" to verify
   ```

---

## Mode: Archive

**Triggers**: "archive docs", "archive old docs", "cleanup docs"

Move old ephemeral and session docs to archives.

### What Gets Archived

| Category | Threshold | Destination |
|----------|-----------|-------------|
| Session handoffs | 7+ days | archives/sessions/ |
| Verify reports | 7+ days | archives/verify-reports/ |
| Test screenshots | 7+ days | archives/test-screenshots/ |
| Completed features | Manual | archives/features-completed/ |
| Scratch notes | 7+ days | archives/scratch/ |

### Steps

1. **Scan for archivable items**:
   ```bash
   # Find old sessions
   find agent-docs -path "*sessions/*" -name "*.md" -mtime +7

   # Find old ephemeral
   find agent-docs -path "*_ephemeral/*" -mtime +7

   # Find completed features (100% in plan.md)
   ```

2. **Display candidates**:
   ```
   RUSTIE DOCS ARCHIVE
   ═══════════════════════════════════════════════════════════════

   Archivable items:

   SESSIONS (7+ days old):
     [1] features/auth/sessions/session-20251215/ (14 days)
     [2] features/auth/sessions/session-20251210/ (19 days)

   EPHEMERAL:
     [3] features/auth/_ephemeral/verify-reports/ (23 files)
     [4] _ephemeral/scratch/design-ideas.md (30 days)

   COMPLETED FEATURES:
     [5] features/user-onboarding/ (100% complete)

   Archive: [all / 1,2,3 / none]
   ```

3. **Ask user** (use AskUserQuestion):
   - All archivable items
   - Specific items (by number)
   - None (cancel)

4. **Execute archiving**:
   ```bash
   # Create dated archive folder
   archive_dir="agent-docs/archives/$(date +%Y%m%d)"
   mkdir -p "$archive_dir"

   # Move items
   git mv source "$archive_dir/"
   ```

5. **Commit**:
   ```bash
   git add agent-docs/
   git commit -m "docs: archive old documentation"
   ```

6. **Report**:
   ```
   Archived 5 items to agent-docs/archives/20251229/
   ```

---

## Mode: Sync

**Triggers**: "sync docs", "update readme", "sync doc pointers"

Ensure README.md points to all documentation and check cross-references.

### Steps

1. **Scan agent-docs/** for all .md files

2. **Build document map**:
   ```
   Features: 4 features with docs
   ADRs: 12 decisions
   Lessons: 8 lessons
   Reference: 5 documents
   ```

3. **Check README.md** links:
   - Does it link to agent-docs/?
   - Are all major sections referenced?
   - Any broken links?

4. **Generate suggested README section**:
   ```markdown
   ## Documentation

   | Doc | Purpose |
   |-----|---------|
   | [Architecture](agent-docs/architecture.md) | System design |
   | [Features](agent-docs/features/) | Current work (4 features) |
   | [Decisions](agent-docs/decisions/adrs/) | ADRs (12 decisions) |
   | [Lessons](agent-docs/lessons/) | Learned (8 lessons) |

   For AI agents, see [AI.md](agent-docs/AI.md).
   ```

5. **Offer to update README**:
   ```
   README.md documentation section is outdated.
   Update with current structure? [yes/no]
   ```

---

## Frontmatter Templates

### Permanent Document
```yaml
---
title: Document Title
lifecycle: permanent
created: 2025-12-29
updated: 2025-12-29
owner: global
---
```

### Session Document
```yaml
---
title: Session Handoff - Feature Name
lifecycle: session
created: 2025-12-29
updated: 2025-12-29
owner: feature-name
session_id: session-20251229-143000
---
```

### Ephemeral Document
```yaml
---
title: Verify Report
lifecycle: ephemeral
created: 2025-12-29
expires_after_days: 7
owner: feature-name
---
```

### ADR Document
```yaml
---
title: "ADR-001: Use React for Frontend"
lifecycle: permanent
created: 2025-12-29
updated: 2025-12-29
owner: global
status: accepted
supersedes: null
superseded_by: null
---
```

### Lesson Document
```yaml
---
title: API Authentication Failures
lifecycle: permanent
created: 2025-12-29
updated: 2025-12-29
owner: global
severity: high
triggers:
  - API
  - authentication
  - 401
  - 403
---
```

---

## Pre-Commit Hook Integration

This skill works with the doc commit hook (`rustie-doc-commit-hook.sh`):

```bash
# What the hook checks:
# 1. No .md in root except allowed list
# 2. All agent-docs/*.md have frontmatter
# 3. All frontmatter has lifecycle field

# If hook blocks:
# "Run /rustie-docs fix to resolve documentation issues"
```

The hook ensures enforcement at commit time, while this skill helps fix issues interactively.

---

## Best Practices

### DO
- Add frontmatter to every doc in agent-docs/
- Use `_ephemeral/` for temporary files
- Run audit weekly or after major changes
- Archive old sessions promptly
- Keep README.md pointing to current structure

### DON'T
- Create .md files in project root (except allowed list)
- Skip lifecycle field in frontmatter
- Let verify-reports accumulate indefinitely
- Ignore audit warnings for too long
- Manually edit frontmatter dates (use script)

---

## Manual Invocation

```
/skill rustie-docs          # Prompts for mode
"check my docs"             # audit mode
"fix doc issues"            # fix mode
"create a new ADR"          # create mode
"archive old docs"          # archive mode
"sync readme"               # sync mode
```
