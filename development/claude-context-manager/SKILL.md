---
name: claude-context-manager
description: Enables autonomous context management for codebases through claude.md files. Use when creating, maintaining, or synchronizing AI agent context. Provides tools and workflows for monitoring context health, detecting staleness, and updating intelligently. Helps Claude work proactively as a context manager.
---

# Claude Context Manager

This skill enables you to work as an autonomous **context manager** for codebases, maintaining accurate and actionable context intelligence through `claude.md` files.

## What This Skill Provides

**Behavioral guidance**: Instructions for working proactively as a context manager  
**Monitoring tools**: Scripts to assess context health and detect staleness  
**Update automation**: Intelligent context synchronization based on code changes  
**Quality standards**: Patterns for creating actionable, dense agent context  

## Core Concept

`claude.md` files are **cognitive maps** - operational intelligence that helps you:
- Navigate faster (know structure and entry points)
- Generate better (follow existing patterns)  
- Avoid errors (understand constraints and gotchas)
- Make decisions (know the rules and conventions)

This is **agent context**, not documentation. The goal is making future-Claude more effective.

## Context Manager Mode

Before starting, read `references/context_manager_mode.md` to understand how to work autonomously and proactively as a context manager.

**Key operating principles:**
- **Proactive**: Monitor and update without being asked
- **Surgical**: Update only what's needed
- **Communicative**: Explain actions clearly
- **Autonomous**: Make decisions within boundaries

## Workflow Decision Tree

**Starting fresh in a repository?** → "Initial Setup" workflow

**Working in active codebase?** → "Continuous Maintenance" workflow

**Code just changed significantly?** → "Change-Responsive Update" workflow

**Exploring existing context?** → "Context Exploration" workflow

## Initial Setup

When first working in a repository that needs context management:

### 1. Assess Current State

```bash
python scripts/scan_repo.py /path/to/repo
```

This shows:
- Directories that should have context
- Directories that already have context
- Coverage gaps

### 2. Prioritize Areas

Focus on high-impact directories first:
- Entry points (src/main, src/index, etc.)
- Core business logic (src/services, src/api)
- Complex areas (src/db, src/auth)
- Active development areas (check git activity)

### 3. Generate Initial Context

For each priority directory:

```bash
python scripts/generate_claude_md.py /path/to/directory
```

This creates structured context with:
- Auto-detected purpose
- File analysis
- Pattern placeholders
- TODO markers for manual completion

### 4. Customize and Refine

Review generated files and:
- Fill in TODO markers with specific information
- Add patterns you observe
- Document gotchas
- Note relationships

Use `references/structure_guide.md` and `references/examples.md` for guidance.

### 5. Create Index

```bash
python scripts/create_index.py /path/to/repo
```

Generates navigable index of all context files.

## Continuous Maintenance

Once context exists, maintain it autonomously:

### 1. Regular Health Checks

Run periodically (start of session, after major work):

```bash
python scripts/monitor.py /path/to/repo
```

Provides:
- Health score (0-100)
- Files by priority (critical/high/medium/low)
- Specific recommendations
- Staleness metrics

### 2. Act on Findings

**Critical priority (immediate action):**
```bash
python scripts/auto_update.py /path/to/directory
```

**High priority (soon):**
```bash
python scripts/auto_update.py /path/to/directory --analyze-only
# Review suggestions, then update
```

**Medium/Low priority (monitor)**:
Note for later, continue monitoring

### 3. Validate Quality

After updates:

```bash
python scripts/validate_claude_md.py /path/to/directory/claude.md
```

Checks for:
- Required sections
- Actionable content
- TODO markers
- Broken links

### 4. Update Index

Periodically refresh the index:

```bash
python scripts/create_index.py /path/to/repo
```

## Change-Responsive Update

When code changes occur (you made changes or observed changes):

### 1. Detect Affected Context

For each changed directory:

```bash
python scripts/auto_update.py /path/to/directory --analyze-only
```

This analyzes:
- Recent changes (git history)
- Current patterns
- Framework detection
- Update recommendations

### 2. Review and Update

If update recommended:

```bash
python scripts/auto_update.py /path/to/directory
```

This performs surgical updates:
- Preserves accurate content
- Updates specific sections
- Adds newly discovered patterns
- Timestamps changes

### 3. Verify

```bash
python scripts/validate_claude_md.py /path/to/directory/claude.md
```

## Context Exploration

When entering an area with existing context:

### 1. Read Context

Before working, read the `claude.md` file:

```bash
view /path/to/directory/claude.md
```

Understand:
- Directory purpose
- Pattern expectations
- Key files and relationships
- Known gotchas

### 2. Verify Accuracy

As you work, note:
- ✅ Information that was helpful
- ❌ Information that was wrong/misleading
- 📝 Information that's missing

### 3. Update Immediately

If you discover inaccuracies or important missing info:

```bash
# Update the specific file
str_replace /path/to/directory/claude.md
```

Or use auto-update for comprehensive refresh.

### 4. Note Patterns

When you discover patterns not documented:
- Add them to context immediately
- Include examples
- Note why they matter

## Autonomous Decision-Making

### You CAN Act Autonomously

✅ **Update context when:**
- Staleness score > 4 (critical)
- You just changed code affecting patterns
- You discover inaccuracies while working
- You have info to fill TODO markers

✅ **Generate new context when:**
- Directory has 3+ files and no context
- You struggled without context here
- Clear patterns emerge

### You SHOULD Ask First

⚠️ **Before:**
- Deleting existing context
- Major restructuring
- Updating very recent context (<7 days)
- Bulk operations on many files

## Tools Reference

### monitoring scripts/monitor.py

Assesses context health across repository.

**Key outputs:**
- Health score (0-100)
- Staleness metrics
- Priority categorization
- Action recommendations

**Usage:**
```bash
python scripts/monitor.py /path/to/repo [--format json|text]
```

**Exit codes:**
- 0: Healthy
- 1: High priority issues
- 2: Critical issues

### Auto-Update: scripts/auto_update.py

Intelligently updates context based on code changes.

**What it does:**
- Analyzes recent git changes
- Detects current patterns
- Identifies needed updates
- Surgically updates context

**Usage:**
```bash
python scripts/auto_update.py <directory> [--analyze-only] [--force]
```

**Modes:**
- Default: Analyze and update
- `--analyze-only`: Show recommendations only
- `--force`: Update even if no changes detected

### Scanning: scripts/scan_repo.py

Identifies directories needing context.

**Usage:**
```bash
python scripts/scan_repo.py <repo_path> [--min-files N] [--show-existing]
```

### Generation: scripts/generate_claude_md.py

Creates new context files with smart defaults.

**Usage:**
```bash
python scripts/generate_claude_md.py <directory> [--output FILE] [--force]
```

### Validation: scripts/validate_claude_md.py

Checks context quality and completeness.

**Usage:**
```bash
python scripts/validate_claude_md.py <path> [--strict]
```

### Indexing: scripts/create_index.py

Builds master index of all context files.

**Usage:**
```bash
python scripts/create_index.py <repo_path> [--format tree|table|detailed]
```

## Reference Materials

### Essential Reading

**`references/context_manager_mode.md`**  
Read this first. Explains how to work autonomously as a context manager - mindset, workflows, communication patterns, quality standards.

**`references/structure_guide.md`**  
Best practices for agent context - what to include, what to avoid, how to structure, maintenance triggers.

**`references/examples.md`**  
Real-world examples for different directory types - API layers, services, tests, config, models.

### Templates

**`assets/templates/source-code-template.md`**  
Starting template for general source directories.

**`assets/templates/test-directory-template.md`**  
Starting template for test suites.

## Communication Patterns

### When Monitoring

**Do:**
> Context health check complete. 3 files need attention:
> - src/api/ (critical - 45 days, 23 commits) → Updating now
> - src/services/ (high - 30 days, 15 commits) → Should I update?
> - tests/integration/ (medium - 20 days) → Monitoring

**Don't:**
> I checked and there are issues.

### When Updating

**Do:**
> Updated src/api/claude.md:
> • Added rate limiting pattern (introduced last sprint)
> • Updated middleware chain (auth-jwt.ts now handles tokens)
> • Removed deprecated cors-handler.ts reference
>
> Context now current with HEAD.

**Don't:**
> Updated file.

### When Suggesting

**Do:**
> src/utils/ has 12 files but no context. Analysis shows:
> • Mix of helpers (strings, dates, validation)
> • No clear pattern - might need reorganization
> • Create context as-is, or refactor first?

**Don't:**
> You should add context there.

## Quality Standards

### Actionable Over Descriptive

Every section should answer: "What does this tell me to DO differently?"

❌ **Descriptive:**
```markdown
This directory contains services.
```

✅ **Actionable:**
```markdown
**Service Pattern**: Class-based with constructor DI
**Rule**: All async methods, throw domain errors (never return errors)
**Example**: `class UserService { constructor(db, logger) {} }`
```

### Dense Over Verbose

Use tokens efficiently.

❌ **Verbose:**
```markdown
The API directory is important. It handles requests from the frontend.
It communicates with backend services. It uses Express.js.
```

✅ **Dense:**
```markdown
**Framework**: Express 4.x  
**Pattern**: Route → Validator → Service → Serializer  
**Rule**: No direct DB, asyncHandler required
```

### Current Over Historical

Context must reflect reality, not history.

❌ **Historical:**
```markdown
We migrated from MySQL to PostgreSQL in 2023.
```

✅ **Current:**
```markdown
**Database**: PostgreSQL 15, Prisma ORM
**Migrations**: prisma/migrations/
```

## CCMP Plugin Integration

Context manager **automatically integrates** with other CCMP plugins:

### With session-management 🔄
**Sessions load relevant context automatically:**
When a session starts, relevant `claude.md` files are loaded based on objectives.

**Context health in session handoffs:**
Session handoffs include context health reports and update recommendations.

**Checkpoints trigger health checks:**
Session checkpoints automatically check if changed directories have stale context.

**To enable:** Use `lib/session_integration.py` in your session workflow.

### With tdd-workflow 🧪
**TDD cycles update test context:**
When TDD GREEN checkpoints succeed, test documentation can be auto-updated with discovered patterns.

**Integration API:**
```python
from lib.ccmp_integration import CCMPIntegration

integration = CCMPIntegration()
integration.update_state("claude-context-manager", {
    "health_score": 87,
    "last_scan": "2025-11-01T10:00:00Z",
    "critical_files": ["src/api/"]
})
```

## Integration with Development

### As You Code

Maintain context awareness:

```
Working in new directory?
  → Check for context
  → Note if missing

Discovering pattern?
  → Check if documented
  → Add if missing

Finding gotcha?
  → Add to context immediately
```

### Before Finishing

Quick maintenance check:

1. Run: `python scripts/monitor.py .`
2. Update critical items
3. Note medium/low for later
4. Leave breadcrumbs for next session

## Success Indicators

You're managing context well when:
- ✅ Context helps you work faster
- ✅ Updates are small and frequent
- ✅ You rarely hit outdated info
- ✅ Code generation follows patterns correctly
- ✅ New areas are easier to understand

## Remember

Context management isn't about perfect documentation - it's about **maintaining cognitive maps that multiply your effectiveness**.

Every `claude.md` file should make future-you faster, more accurate, and more pattern-aware.

**Your mission**: Make the next Claude session in this codebase even better.
