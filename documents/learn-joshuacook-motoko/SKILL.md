---
name: learn
description: Process inbox summaries and update system knowledge. Curates role "Right Now" sections, appends "Recent Context", updates central docs. Intelligent curation, not just appending.
allowed-tools: Read, Edit, Bash, Write
---

# Learn (System Learning)

Intelligently update roles and docs based on session summaries.

## When to Activate

- User says: "learn", "update roles"
- After compressing sessions
- When inbox has session summaries

## Approach

**OLD:** Append bullets to logs
**NEW:** Intelligent curation

**Role structure:**
- What This Role Does (rarely changes)
- **Right Now** ← CURATE (what's currently relevant)
- **Recent Context** ← APPEND (timestamped, last 30 days)
- How This Role Operates (rarely changes)

## Process

### 1. Read Inbox

```bash
ls inbox/session-summaries/
cat inbox/session-summaries/*.md
```

### 2. Analyze Changes

**Extract from summaries:**
- Decisions made
- Tools/workflows built
- Role activity
- Context changes

**Categorize:**
- **Right Now:** What's newly relevant for ongoing work
- **Recent Context:** Timestamped decisions (auto-prune > 30 days)

### 3. Create Branch

```bash
git checkout -b learning-$(date +%Y-%m-%d)
```

### 4. Update Roles

**For each affected role:**

#### A. Read Current Role
```bash
cat roles/[role-file].md
```

#### B. Curate "Right Now"

This is CURATION, not appending:
1. Read existing "Right Now"
2. Add newly relevant context
3. Remove stale/no-longer-relevant items
4. Keep tight (5-10 bullets max)

#### C. Append "Recent Context"

Add timestamped entry at top:
```markdown
## Recent Context (Last 30 Days)

**YYYY-MM-DD:** [Summary]
- Key point 1
- Key point 2

[...existing entries...]
```

Auto-prune if > 10 entries.

#### D. Update "Last Updated"

### 5. Commit and PR

```bash
git add roles/*.md
git commit -m "System learning: [summary]"
git push -u origin learning-$(date +%Y-%m-%d)
gh pr create --title "System Learning $(date +%Y-%m-%d)" --body "..."
git checkout main
```

### 6. Report

```
System learning complete.

Processed: [N] session summaries
Roles updated: [list]
Branch: learning-YYYY-MM-DD
PR: #[number]

Next: Review and merge PR.
```

## Curation Guidelines

**"Right Now" = what's relevant:**
- Shapes how role operates TODAY
- Would need to know this to do role's job
- NOT just recent - could be weeks old but still relevant

**"Recent Context" = what happened:**
- Timestamped decisions
- Links to details if needed
- Auto-prune oldest when > 10 entries
