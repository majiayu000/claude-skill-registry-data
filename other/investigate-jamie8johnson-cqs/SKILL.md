---
name: investigate
description: Run before starting an implementation task — scout + gather assemble relevant files, functions, tests, and notes into a brief.
argument-hint: "<task description>"
---

# Investigate

Run before starting any implementation task. Assembles all relevant context in one call.

## Arguments

- `<task_description>` — what you're about to implement (natural language)

## Process

1. Run `cqs scout "<task_description>" --json` via Bash
2. Run `cqs gather "<task_description>" --json --tokens 4000` via Bash
3. Present results as an implementation brief

## Output Format

Present this to the user (fill in from the JSON results):

```
## Investigation: <task_description>

### Relevant Files
<from scout: file groups ranked by relevance, with chunk names>

### Key Functions to Understand
<from gather: top functions with signatures, grouped by role>
- **Modify targets:** <functions that likely need changes>
- **Dependencies:** <functions called by the targets>
- **Tests:** <existing tests that cover these functions>

### Staleness
<from scout: any stale files that need reindexing>

### Notes
<from scout: any relevant project notes>

### Suggested Approach
Based on the code structure:
1. Start with <most relevant file/function>
2. Check <dependency> for the interface contract
3. Test coverage: <good/partial/none> — <recommendation>
```

## Rules

- If scout returns no results, try a broader query or different phrasing
- If gather returns no code (token budget exhausted), increase `--tokens` or narrow the query
- Always present the "Suggested Approach" — synthesize the scout+gather results into a 3-step plan
- If relevant notes mention warnings or gotchas, highlight them prominently
- If stale files are found, suggest `cqs index` before proceeding
