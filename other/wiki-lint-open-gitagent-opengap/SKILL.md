---
name: wiki-lint
description: "Health-check the wiki for contradictions, stale claims, orphan pages, missing cross-references, and knowledge gaps. Use periodically or when the user says 'lint the wiki' or 'check wiki health'."
allowed-tools: Read Glob Grep
---

# Wiki Lint

Audit the wiki for quality and consistency issues.

## Workflow

### Step 1: Read the full index
Read `memory/wiki/index.md` to get the complete page catalog.

### Step 2: Check each category

**Contradictions**
- Scan pages that reference the same entities or concepts
- Flag claims that conflict across pages
- Note which sources support each side
- Recommend resolution (usually: update the older claim with a note)

**Stale claims**
- Check page frontmatter `updated` dates
- Flag pages not updated in recent ingests that cover topics where new sources exist
- Identify claims that newer sources have superseded

**Orphan pages**
- Find pages with no inbound `[[wikilinks]]` from other pages
- These may be valid standalone pages or may indicate missing cross-references

**Missing pages**
- Scan for `[[wikilinks]]` that point to pages that don't exist yet
- Identify important concepts mentioned frequently but lacking their own page

**Missing cross-references**
- Find pages that discuss the same entities but don't link to each other
- Suggest wikilinks that should be added

**Knowledge gaps**
- Based on the topics covered, suggest:
  - Questions worth investigating
  - Sources worth finding
  - Angles not yet explored

### Step 3: Report

Produce a structured report:

```markdown
# Wiki Health Report — [date]

## Contradictions (X found)
- [page-a] vs [page-b]: [description of conflict]

## Stale Claims (X found)
- [page]: last updated [date], but [newer-source] may supersede

## Orphan Pages (X found)
- [page]: no inbound links

## Missing Pages (X found)
- [[concept-name]]: referenced in [N] pages but has no page

## Missing Cross-References (X found)
- [page-a] and [page-b] both discuss [topic] but don't link

## Suggested Investigations
- [question or source suggestion]
```

### Step 4: Log
Append to `memory/log.md`:
```
## [YYYY-MM-DD] lint | Wiki Health Check
- Contradictions: X
- Stale claims: X
- Orphan pages: X
- Missing pages: X
- Missing cross-references: X
```
