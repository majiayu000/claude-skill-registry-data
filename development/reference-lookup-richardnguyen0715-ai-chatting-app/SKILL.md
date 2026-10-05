---
name: reference-lookup
description: Search your references and context knowledge base for patterns relevant to a current task. Use before implementing anything non-trivial to surface prior art from your analyzed repos.
---

# Reference Lookup

## Overview

Before starting any non-trivial implementation, search your knowledge base. You may have already studied a repo that solves this exact problem — or at least has relevant patterns you can adapt.

## When to Use

- Before implementing a new feature or module
- When choosing between approaches (check what worked in references)
- When debugging a class of problem you've seen before
- When evaluating a new library or technique

## Don't Skip This Step

> "I'll figure it out from scratch" costs 2 hours.
> "Let me check my references first" costs 5 minutes and often saves the 2 hours.

---

## Lookup Workflow

### Step 1 — Define What You're Looking For

Write a one-sentence description of your task, then extract:

```
Task: "Implement incremental Delta Lake writes that avoid full overwrites"

Keywords: Delta, incremental, merge, upsert, MERGE INTO, idempotent
Domain:   databricks, patterns
Tech:     PySpark, Delta Lake
```

### Step 2 — Search Context KB

```bash
# Search by keyword across all context
grep -r "merge\|upsert\|incremental" ~/.copilot/context/ -l --include="*.md"

# Read matching files
cat ~/.copilot/context/databricks/{matching-file}.md
```

### Step 3 — Search Reference Analyses

```bash
# Search pattern sections of analysis files
grep -r "incremental\|merge\|delta" ~/references/ --include="analysis.md" -l
grep -r "incremental" ~/references/ --include="analysis.md" -n | head -20
```

### Step 4 — Browse Reference Code

If an analysis mentions a specific file:
```bash
grep -r "MERGE INTO\|delta.merge" ~/references/{repo}/ --include="*.py" -n | head -20
cat ~/references/{repo}/{path/to/file}.py
```

---

## Presenting Results

After searching, produce a structured summary:

```
## Lookup Results: "{your task}"

### ✅ Direct Match
Found in: ~/.copilot/context/databricks/delta-merge-pattern.md
---
{paste key content / snippet}
---
→ Apply by: {specific adaptation needed}

### 🔶 Related
- ~/references/delta-lake-recipes/analysis.md §6 — "MERGE pattern with SCD Type 2"
  Worth reading: covers deduplication during merge

### ❌ Not Found
No existing pattern for "{specific aspect of task}"
→ After implementing, consider adding to ~/.copilot/context/patterns/

### Recommended Approach
Based on references, use: {specific recommendation with reasoning}
```

---

## Search Cheatsheet

| Looking for | Search command |
|------------|---------------|
| All entries in a domain | `ls ~/.copilot/context/{domain}/` |
| Keyword across all KB | `grep -r "{term}" ~/.copilot/context/ -l` |
| Keyword in references | `grep -r "{term}" ~/references/ --include="*.md" -l` |
| Code snippet in refs | `grep -r "{term}" ~/references/ --include="*.py" -n` |
| What repos cover topic | `grep -r "{term}" ~/references/ --include="analysis.md" -l` |

---

## After Lookup

| Result | Action |
|--------|--------|
| Direct match found | Use it, note any adaptation needed |
| Partial match found | Build on it, document the gap |
| No match found | Implement, then run `context-extraction` to capture it |
| Relevant repo not analyzed | Run `repo-analysis` skill first |

## Tips

- **Cast a wide net** with keywords — don't just search the exact term
- **Read, don't skim** — a 2-minute read of a matching file is worth it
- **Check multiple domains** — a pattern from `auth/` might apply to `patterns/` use cases
- Use `reference-navigator` agent for an automated lookup with AI synthesis
