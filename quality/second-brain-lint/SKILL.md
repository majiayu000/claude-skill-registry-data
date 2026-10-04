---
name: second-brain-lint
description: >
  Health-check the wiki for contradictions, orphan pages, stale claims,
  and missing cross-references. Use when the user says "audit",
  "health check", "lint", "find problems", or wants to improve wiki quality.
allowed-tools: Bash Read Write Edit Glob Grep
---

# Second Brain — Lint

Health-check the wiki and report issues with actionable fixes.

## Audit Steps

Run all checks below, then present a consolidated report.

### 1. Broken wikilinks

Scan all wiki pages for `[[wikilink]]` references. For each link, verify the target page exists. Report any broken links.

```bash
# Find all wikilinks across wiki pages
grep -roh '\[\[[^]]*\]\]' wiki/ | sort -u
```

Cross-reference against actual files in `wiki/`.

### 2. Orphan pages

Find pages with no inbound links — no other page references them via `[[wikilink]]`.

For each `.md` file in `wiki/sources/`, `wiki/entities/`, `wiki/concepts/`, `wiki/synthesis/`:
- Extract the page name (filename without extension)
- Search all other wiki pages for `[[Page Name]]`
- If no other page links to it, it's an orphan

### 3. Contradictions

Read pages that share entities or concepts and look for conflicting claims. Flag when:
- Two source summaries make opposing claims about the same topic
- An entity page contains information that conflicts with a source summary
- Dates, figures, or factual claims differ between pages

### 4. Stale claims

Cross-reference source dates with wiki content. Flag when:
- A concept page cites only old sources and newer sources exist on the same topic
- Entity information hasn't been updated despite newer sources mentioning that entity

### 5. Missing pages

Scan for `[[wikilinks]]` that point to pages that don't exist yet. These are topics the wiki mentions but hasn't given their own page. Assess whether they warrant a page.

### 6. Missing cross-references

Find pages that discuss the same topics but don't link to each other. Look for:
- Entity pages that mention concepts without linking them
- Concept pages that mention entities without linking them
- Source summaries that cover the same topic but don't reference each other

### 7. Index consistency

Verify `wiki/index.md` is complete and accurate:
- Every page in `wiki/sources/`, `wiki/entities/`, `wiki/concepts/`, `wiki/synthesis/` has an index entry
- No index entries point to deleted pages
- Entries are under the correct category header

### 8. Data gaps

Based on the wiki's current coverage, suggest:
- Topics mentioned frequently but lacking depth
- Questions the wiki can't answer well
- Areas where a web search could fill in missing information

## Report Format

Present findings grouped by severity:

### Errors (must fix)
- Broken wikilinks
- Contradictions between pages
- Index entries pointing to missing pages

### Warnings (should fix)
- Orphan pages with no inbound links
- Stale claims from outdated sources
- Missing pages for frequently referenced topics

### Info (nice to fix)
- Potential cross-references to add
- Data gaps that could be filled
- Index entries that could be more descriptive

For each finding, include:
- **What:** description of the issue
- **Where:** the specific file(s) and line(s)
- **Fix:** what to do about it

## After the Report

Ask the user:
> "Found N errors, N warnings, and N info items. Want me to fix any of these?"

If the user agrees, fix issues and report what changed.

## Log the lint pass

Append to `wiki/log.md`:

    ## [YYYY-MM-DD] lint | Health check
    Found N errors, N warnings, N info items. Fixed: [list of fixes applied].

## When to Lint

- **After every 10 ingests** — catches cross-reference gaps while they're fresh
- **Monthly at minimum** — catches stale claims and orphan pages over time
- **Before major queries** — ensures the wiki is healthy before you rely on it for analysis

## Related Skills

- `/second-brain-ingest` — process new sources into wiki pages
- `/second-brain-query` — ask questions against the wiki
