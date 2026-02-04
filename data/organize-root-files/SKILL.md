---
name: organize-root-files
description: Clean up and organize markdown files dumped at project root. Routes files to appropriate directories (memos/, docs/, devops/docs/) or deletes obsolete content. Follows project file organization guidelines from CLAUDE.md.
---

You are the root directory organization specialist. Your job is to identify markdown files that were created at the project root and route them to their appropriate locations based on content and purpose.

## Core Responsibilities

## Skill Usage Announcement

**MANDATORY**: When using this skill, announce it at the start with:

```
🔧 Using Skill: organize-root-files | [brief purpose based on context]
```

**Example:**
```
🔧 Using Skill: organize-root-files | [Provide context-specific example of what you're doing]
```

This creates an audit trail showing which skills were applied during the session.



- Scan project root for markdown files (especially ALL_CAPS.md files)
- Analyze each file's purpose and relevance
- Route files to appropriate directories or delete if obsolete
- Follow project organization guidelines from CLAUDE.md
- Report on all organizational actions taken

## Execution Strategy

### Phase 1: Discovery

**Approach:**

1. **List all markdown files in project root:**
   ```bash
   find . -maxdepth 1 -name "*.md" -type f
   ```

2. **Filter to organizational candidates:**
   - Include: Files that look like they should be organized
     - `RCA-*.md` (Root cause analyses)
     - `ANALYSIS-*.md`
     - `IMPLEMENTATION-*.md`
     - `SUMMARY-*.md`
     - `NOTES-*.md`
     - `DESIGN-*.md`
     - `INVESTIGATION-*.md`
     - Any ALL_CAPS.md files
   - Exclude: Files that should stay at root
     - `README.md`
     - `CHANGELOG.md`
     - `LICENSE.md`
     - `CONTRIBUTING.md`
     - `CODE_OF_CONDUCT.md`

3. **Read each candidate file:**
   - First 50 lines to understand purpose
   - Check metadata (dates, context references)
   - Identify topic and relevance

**Output:** List of files with preliminary categorization

---

### Phase 2: Categorization

**For each file, determine:**

#### **Category 1: Delete (Obsolete)**

**Criteria:**
- Incorrect analysis that was later discarded
- Temporary debugging notes no longer relevant
- Draft content superseded by better version
- Experimental ideas that weren't pursued

**Signs of obsolescence:**
- Contains phrases like "This didn't work", "Incorrect assumption", "Discarded approach"
- References specific debugging session that's resolved
- Duplicate content (better version exists elsewhere)
- Very old and no longer applicable

**Action:** Delete file

---

#### **Category 2: Memos (Reference Material)**

**Criteria:**
- Root cause analysis (even if old, for future reference)
- Lessons learned from technical problems
- Investigation findings
- Decision records and rationale
- Post-mortems
- Implementation summaries
- Research findings

**Signs it's a memo:**
- Documents "why" something was done
- Contains technical insights worth preserving
- Future developers might need this context
- Historical record of problem solving

**Action:** Move to `memos/` with date-prefixed name

**Naming convention:**
```
memos/YYYY-MM-DD-topic-slug.md
```

Examples:
- `RCA-AUTH-FAILURE.md` → `memos/2025-11-17-auth-failure-rca.md`
- `IMPLEMENTATION-SUMMARY-MCP.md` → `memos/2024-10-29-mcp-integration-summary.md`
- `NOTES-DEBUGGING-SESSION.md` → `memos/2025-11-15-debugging-session-notes.md`

---

#### **Category 3: User Documentation**

**Criteria:**
- Content users/customers should read
- How-to guides
- Feature explanations
- API usage examples
- Getting started guides
- FAQ content

**Signs it's user documentation:**
- Written for end users, not developers
- Explains features and usage
- Contains examples of using the product
- No internal implementation details

**Action:** Move to `docs/` with lowercase-dash-separated name

**Naming convention:**
```
docs/lowercase-with-dashes.md
```

Examples:
- `USING-WORKFLOWS.md` → `docs/using-workflows.md`
- `API-GUIDE.md` → `docs/api-guide.md`
- `GETTING-STARTED.md` → `docs/getting-started.md`

---

#### **Category 4: Developer Documentation**

**Criteria:**
- Internal developer/maintainer focused
- Architecture decisions (ADR)
- Deployment procedures
- Development setup
- CI/CD configuration
- Infrastructure details

**Signs it's developer documentation:**
- Technical details for maintainers only
- Deployment/operations procedures
- Architecture rationale
- Internal system design

**Action:** Move to `devops/docs/` with lowercase-dash-separated name

**Naming convention:**
```
devops/docs/lowercase-with-dashes.md
```

Examples:
- `DEPLOYMENT-GUIDE.md` → `devops/docs/deployment-guide.md`
- `ARCHITECTURE-DECISIONS.md` → `devops/docs/architecture-decisions.md`
- `CI-CD-SETUP.md` → `devops/docs/ci-cd-setup.md`

---

### Phase 3: Execution

**Approach:**

1. **Create directories if needed:**
   ```bash
   mkdir -p memos
   mkdir -p devops/docs
   # docs/ usually exists, but ensure it
   mkdir -p docs
   ```

2. **For each file, execute action:**

   **Delete:**
   ```bash
   rm FILE.md
   ```

   **Move to memos:**
   ```bash
   # Extract or infer date
   mv FILE.md memos/YYYY-MM-DD-topic.md
   ```

   **Move to docs:**
   ```bash
   # Convert to lowercase-dash format
   mv FILE.md docs/lowercase-topic.md
   ```

   **Move to devops/docs:**
   ```bash
   mv FILE.md devops/docs/lowercase-topic.md
   ```

3. **Track all actions for report**

**Output:** Organized file structure

---

### Phase 4: Reporting

**Generate organization report:**

```markdown
# Root Directory Organization Report

## Summary

Organized [N] markdown files from project root.

**Actions:**
- Deleted: [N] obsolete files
- Moved to memos/: [N] files
- Moved to docs/: [N] files
- Moved to devops/docs/: [N] files

## Detailed Actions

### Deleted (Obsolete)

- `RCA-INCORRECT-HYPOTHESIS.md` - Discarded analysis, superseded by correct RCA
- `TEMP-DEBUG-NOTES.md` - Temporary debugging session notes, issue resolved

### Moved to memos/

- `RCA-AUTH-FAILURE.md` → `memos/2025-11-17-auth-failure-rca.md`
  - Root cause analysis worth preserving for future reference

- `IMPLEMENTATION-SUMMARY-MCP.md` → `memos/2024-10-29-mcp-integration-summary.md`
  - Implementation summary documenting MCP integration decisions

- `INVESTIGATION-PERFORMANCE.md` → `memos/2025-11-10-performance-investigation.md`
  - Performance investigation findings and solutions

### Moved to docs/

- `USING-WORKFLOWS.md` → `docs/using-workflows.md`
  - User guide for workflow system

- `API-EXAMPLES.md` → `docs/api-examples.md`
  - API usage examples for end users

### Moved to devops/docs/

- `DEPLOYMENT-GUIDE.md` → `devops/docs/deployment-guide.md`
  - Deployment procedures for maintainers

- `ARCHITECTURE-DECISIONS.md` → `devops/docs/architecture-decisions.md`
  - ADR for internal design decisions

## Root Directory Status

**Before:** [N] markdown files (excluding standard files like README.md)
**After:** 0 organizational files remaining

**Preserved at root:**
- README.md
- CHANGELOG.md
- LICENSE.md
[etc.]

## Recommendations

- All analysis/documentation files now properly organized
- Root directory clean and maintainable
- Future files should follow guidelines in CLAUDE.md

---

*Generated by organize-root-files skill*
```

---

## Decision Logic

### How to Determine File Category

**Use this decision tree:**

1. **Is the file relevant anymore?**
   - No → DELETE
   - Yes → Continue

2. **Who is the audience?**
   - End users → DOCS
   - Developers/maintainers → DEVOPS/DOCS
   - Future self/team (reference) → MEMOS

3. **What's the purpose?**
   - Teaching users how to use product → DOCS
   - Explaining internal design/operations → DEVOPS/DOCS
   - Recording what happened/why → MEMOS

4. **Still unsure?**
   - Contains "RCA", "Analysis", "Investigation" → MEMOS
   - Contains "Guide", "Tutorial", "How to" → Check audience (DOCS or DEVOPS/DOCS)
   - Contains "Decision", "Design", "Architecture" → DEVOPS/DOCS
   - Default → MEMOS (safer to preserve than delete)

---

## Important Considerations

### Date Inference

When moving to `memos/`, try to determine the date:

1. **Check git history:**
   ```bash
   git log --follow --format=%aI -- FILE.md | tail -1
   ```

2. **Check file modification time:**
   ```bash
   stat -f %Sm -t %Y-%m-%d FILE.md  # macOS
   stat -c %y FILE.md | cut -d' ' -f1  # Linux
   ```

3. **Check content for date references:**
   - Look for dates in headers
   - Check for "Created:", "Date:", etc.

4. **Use today's date if unknown:**
   - Last resort: use current date

### Content Preservation

**Never modify file content** - only move and rename.

The goal is organization, not editing.

### Ambiguous Cases

If truly ambiguous:
- **Default to memos/** (safer to preserve)
- **Add note in report** about uncertainty
- **User can manually relocate** if needed

### Standard Root Files

**Always preserve these at root:**
- README.md
- CHANGELOG.md
- LICENSE.md / LICENSE
- CONTRIBUTING.md
- CODE_OF_CONDUCT.md
- SECURITY.md
- .gitignore, .gitattributes
- package.json, pyproject.toml (language manifests)

---

## Examples

### Example 1: Old RCA Worth Keeping

**File:** `RCA-DATABASE-DEADLOCK.md`

**Content preview:**
```markdown
# Root Cause Analysis: Database Deadlock

## Issue
Production experienced deadlocks on 2024-08-15...

## Investigation
...detailed analysis...

## Solution
Implemented row-level locking instead of table locks...

## Lessons Learned
- Always use row-level locking for high-concurrency tables
- Monitor lock wait times
```

**Decision:** MEMOS
- Valuable historical record
- Lessons learned worth preserving
- Future devs might encounter similar issue

**Action:** Move to `memos/2024-08-15-database-deadlock-rca.md`

---

### Example 2: Temporary Debug Notes

**File:** `DEBUG-NOTES-TEMP.md`

**Content preview:**
```markdown
# Debug notes

Trying different approaches to fix auth bug...

Approach 1: didn't work
Approach 2: didn't work
Approach 3: FIXED IT! (moved to proper implementation)

Delete this file after confirming fix deployed.
```

**Decision:** DELETE
- Explicitly marked as temporary
- Problem solved
- No lasting value

**Action:** Delete file

---

### Example 3: User Guide

**File:** `WORKFLOW-USAGE.md`

**Content preview:**
```markdown
# Using Wrangler Workflows

This guide shows you how to use workflows in your projects.

## Running Housekeeping

To clean up your project:
```bash
/wrangler:housekeeping
```
...
```

**Decision:** DOCS
- Teaching users how to use feature
- No internal details
- End-user focused

**Action:** Move to `docs/workflow-usage.md`

---

### Example 4: Deployment Procedure

**File:** `DEPLOY-PROCESS.md`

**Content preview:**
```markdown
# Deployment Process

Internal guide for deploying Wrangler updates.

## Prerequisites
- Access to npm registry
- GitHub deploy permissions

## Steps
1. Run tests: `npm test`
2. Build MCP server: `npm run build:mcp`
...
```

**Decision:** DEVOPS/DOCS
- Internal operations guide
- Maintainer-only content
- Deployment procedures

**Action:** Move to `devops/docs/deploy-process.md`

---

## Integration with Housekeeping Workflow

This skill is designed to be called as a subagent from the `housekeeping` workflow:

**In housekeeping Phase 2, add as Agent D:**

```
Agent D: Root Directory Organization
- Task: Clean up markdown files at project root
- Skill: organize-root-files
- Independence: Operates on root .md files only
```

This keeps root clean automatically during routine housekeeping.

---

## Success Criteria

✅ All organizational candidate files identified
✅ Each file correctly categorized
✅ Files moved to appropriate directories with correct naming
✅ Obsolete files deleted
✅ Root directory clean (only standard files remain)
✅ Report generated documenting all actions

---

## Future Enhancements

### Automatic Date Detection

Improve date inference with:
- Parse file content for explicit dates
- Use git blame to find creation date
- Store creation metadata

### Content Analysis

Use more sophisticated analysis:
- Keyword extraction
- Topic modeling
- Similarity to existing organized files

### Interactive Mode

For ambiguous files:
- Show user the file
- Ask which category
- Learn from user choices

---

*Organize Root Files Skill v1.0*
