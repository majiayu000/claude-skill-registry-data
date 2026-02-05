---
name: documenting-with-audit
description: Automated documentation auditing - ensures CLAUDE.md coverage, updates stale docs, recommends structural improvements
---

# Documentation Auditing

Automated system to keep documentation complete, accurate, and current. Manages CLAUDE.md hierarchy and all project docs.

## Purpose

Documentation drifts from code. This skill:
- Ensures every meaningful directory has CLAUDE.md
- Automatically updates docs when code changes
- Tracks freshness via git commits + timestamps
- Recommends structural improvements
- Uses git for review/approval

## State File: `.docsaudit.yaml`

Tracks audit state for all docs.

**Format:**
```yaml
version: 1

ignore:
  - node_modules/**
  - .git/**
  - dist/**
  - __pycache__/**

max_age_days: 90

audits:
  README.md:
    commit: abc123
    date: 2025-11-19T10:30:00Z
    scope: ["**/*"]

  src/auth/CLAUDE.md:
    commit: def456
    date: 2025-11-15T09:00:00Z
    # No scope = directory default (src/auth/**/*)
```

**Bootstrap if missing:**
- Create file with sensible defaults
- Scan existing docs
- Initialize all with current HEAD
- Infer scopes based on location

## Scope System

**Scope = glob patterns defining which files a doc describes**

### Default Scope (Automatic)

Every doc scopes to its directory:
- `README.md` (root) → `**/*` (whole project)
- `src/auth/CLAUDE.md` → `src/auth/**/*`
- `docs/api.md` → `docs/**/*`

Predictable, consistent, no special cases.

### Explicit Override

```yaml
docs/api.md:
  scope: ["src/api/**/*"]  # Track API code, not docs dir
```

### Independent Docs

```yaml
CONTRIBUTING.md:
  scope: []  # Explicit empty = no code dependencies
```

### Staleness

Doc is stale if:
1. Files in scope changed since `commit`
2. More than `max_age_days` since `date`

Both triggers checked.

## Audit Process

### Step 1: Coverage Check

**Goal:** Every meaningful directory has CLAUDE.md

**Process:**
1. Find all directories (exclude hidden)
2. Check against ignore patterns
3. For non-ignored without CLAUDE.md:
   - Analyze contents
   - Would CLAUDE.md add value?
   - If yes: **Create CLAUDE.md**
   - If no: **Add to ignore list**

**Decision Criteria:**

Ask: "Would CLAUDE.md help understand this?"

Consider:
- Any meaningful code/content?
- Logic, utilities, modules?
- Config, data, assets needing explanation?
- Test fixtures, scripts, migrations?

If yes (even for 2-line doc) → create it.

Ignore only:
- Build artifacts (dist/, __pycache__)
- Dependencies (node_modules/)
- Git internals (.git/)

**No file extension filtering** - analyze actual content.

### Step 2: Ignore Review

**Goal:** Un-ignore directories that grew meaningful

**Process:**
1. For each ignored directory:
   - Analyze current contents
   - Has it grown complex/meaningful?
   - Still makes sense to ignore?
2. If should be documented:
   - Remove from ignore list
   - Create CLAUDE.md
   - Report: "Un-ignored X - grew to Y modules"
3. If still ignorable:
   - Keep in ignore list

**Examples of growth:**
- `tests/fixtures/` added 10 complex test scenarios
- `scripts/` now has deployment orchestration
- `utils/` grew from 1 to 8 helper modules

### Step 3: Freshness Check

**Goal:** Update stale docs automatically

**Process:**

For each doc in `audits`:

1. **Get scope** (explicit or directory default)

2. **Check staleness** via TWO triggers:
   ```bash
   # Code staleness
   git diff <last-commit>..HEAD -- <scope-patterns>

   # Time staleness
   days_since(date) > max_age_days
   ```

3. **If stale:**
   - Analyze code changes
   - Read current doc
   - Update doc to reflect changes
   - Preserve structure/style
   - Write updated doc

4. **Update audit record:**
   ```yaml
   audits:
     path/to/doc.md:
       commit: <new-HEAD>
       date: <now>
   ```

**Parallel processing:** Use Task tool for multiple docs simultaneously.

### Step 4: Sanity Check

**Goal:** Recommend structural improvements

**Process:**

Analyze overall doc structure, detect issues:

**Consolidate:**
- Compare doc scopes
- Check content similarity (>70% overlap)
- Recommend: "Merge A + B - they cover same topic"

**Move:**
- Doc location vs scope mismatch
- Example: `docs/database.md` with scope `src/db/**/*`
- Recommend: "Move to src/db/CLAUDE.md"

**Delete:**
- Scope patterns match zero files
- Doc obsolete, no code described
- Recommend: "Delete or archive X - no code in scope"

**Split:**
- Doc too large (>500 lines)
- Multiple distinct topics
- Recommend: "Split X into Y sections"

**Merge:**
- Multiple tiny docs (<50 lines each)
- Related scopes, similar topics
- Recommend: "Merge A, B, C into single guide"

**Present recommendations, don't auto-apply** - bigger decisions need human judgment.

### Step 5: Update State

Write final `.docsaudit.yaml` with:
- New audit records
- Updated ignore list
- Current timestamp

All changes staged for git review.

## CLAUDE.md Generation

**When:** Creating new CLAUDE.md file

**Analysis:**
1. Read directory structure
2. List all files
3. Sample code files:
   - Imports/exports
   - Class/function names
   - Module patterns
4. Check existing README/comments
5. Understand purpose and relationships

**Template:**
```markdown
# [Module Name]

## Purpose
[1-2 sentences: what this does]

## Key Components
- [file/class]: [purpose]
- [file/class]: [purpose]

## Dependencies
- Uses: [other modules]
- Used by: [other modules]

## Notes
[Important context, conventions, gotchas]
```

**Keep concise:**
- 2-line CLAUDE.md better than none
- Add value, avoid obvious
- Focus on non-obvious context
- Explain "why" not "what"

**Examples:**

```markdown
# tests/fixtures/auth

JWT tokens and auth payloads for testing.
Tokens are expired but have valid structure.
```

```markdown
# scripts/deployment

Production deployment utilities.
Run via `just deploy <env>` - never manually.
Handles DB migrations, health checks, rollback.
```

## Doc Updates

**When:** Doc is stale (code or time)

**Process:**

1. **Get changes:**
   ```bash
   git diff <last-commit>..HEAD -- <scope>
   ```

2. **Summarize:**
   - Files added/removed/modified
   - Key code changes (new functions, refactored modules)
   - Significant diffs

3. **Read current doc:**
   - Understand structure
   - Identify sections
   - Note style

4. **Determine updates:**
   - Which sections affected by changes?
   - What needs adding/removing/updating?
   - Preserve unaffected sections

5. **Rewrite:**
   - Update affected sections
   - Maintain doc structure
   - Match existing style
   - Keep concise

6. **Write updated doc**

**Preserve:**
- Overall structure
- Heading hierarchy
- Writing style
- Unaffected content

**Update:**
- Obsolete information
- New features/modules
- Changed behavior
- Refactored code

## Output Format

**Structure:**
```
Documentation Audit Report

Coverage (CLAUDE.md files):
  Created (N):
    + path/to/new.md (reason)

  Un-ignored (N):
    + path/to/unignored.md (reason)

Freshness (content updates):
  Updated (N):
    ~ path/to/updated.md (summary)

  Already current (N):
    ✓ path/to/current.md

Recommendations:
  ⚠ Issue: description
  ⚠ Issue: description

Files changed: N
Review: git diff
Commit: git commit -am "docs: automated audit"
```

**Symbols:**
- `+` Created/added
- `~` Updated/modified
- `✓` Already current
- `⚠` Recommendation

## Ignore Patterns

**System defaults:**
```yaml
ignore:
  - node_modules/**
  - .git/**
  - dist/**
  - build/**
  - __pycache__/**
  - "*.pyc"
  - .pytest_cache/**
  - .mypy_cache/**
  - coverage/**
  - htmlcov/**
```

**Add project-specific:**
- Generated code directories
- Vendor dependencies
- Build outputs
- IDE files

**Review regularly** - directories grow, become meaningful.

## Error Handling

**Git errors:**
- `git diff` fails → report error, continue others
- File locked → skip, report
- Merge conflict → manual resolution needed

**Analysis errors:**
- Can't parse code → create basic CLAUDE.md
- Unclear structure → ask for manual review
- Missing scope files → flag as potential delete

**Fail gracefully, report clearly.**

## Workflow

**Standard:**
```bash
/docsaudit
# Reviews output
git diff
# If good:
git commit -am "docs: automated audit updates"
# If not:
git restore .
```

**First time (bootstrap):**
```bash
/docsaudit --init
# Creates .docsaudit.yaml
# Initializes all existing docs
git add .docsaudit.yaml
git commit -m "docs: initialize audit tracking"

# Then regular audits
/docsaudit
```

**Specific directory:**
```bash
/docsaudit src/auth
# Audits only src/auth and below
```

**Dry run:**
```bash
/docsaudit --dry-run
# Reports what would change
# Doesn't modify anything
```

## Performance

**Parallel processing:**
- Use Task tool for multiple doc updates
- Each doc update independent
- Faster for projects with many docs

**Git efficiency:**
- `git diff` is cheap, recalculate always
- No caching needed
- Incremental by design (only stale docs updated)

## Success Criteria

System working if:
1. Every meaningful directory has CLAUDE.md
2. Docs update when code changes
3. Structural issues flagged
4. Workflow: audit → review → commit
5. Zero manual tracking needed

## Philosophy

**Comprehensive coverage:**
- CLAUDE.md everywhere it adds value
- Even 2-line docs beat nothing
- Context is cheap, confusion is expensive

**Automated maintenance:**
- System does the work
- Git provides review
- Commit or revert

**Continuous improvement:**
- Regular audits catch drift
- Sanity checks improve structure
- Documentation evolves with code

**Trust but verify:**
- Automation creates/updates
- Human reviews via git
- Best of both worlds
