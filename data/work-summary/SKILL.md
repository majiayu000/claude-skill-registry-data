---
name: work-summary
description: Create factual working journal entries in Notes/WorkingJournal/ after completing analysis work. Use when user asks to "summarize work", "document results", or "create working journal entry". Ensures code is committed, copies figures to attachments, and creates objective summaries with citations.
---

# Work Summary Skill

Create factual working journal entries that document completed analysis work without interpretation or recommendations.

## When to Use

Activate when user requests:
- "Summarize the work"
- "Document the results"
- "Create a working journal entry"
- "Write up the analysis"

## Instructions

### Step 1: Verify Git Commit

Check if code has been committed:

```bash
git status
```

**If uncommitted changes exist:**
1. Inform user: "I see uncommitted changes. Should I run the code-quality-reviewer agent and commit the code first?"
2. Wait for user confirmation
3. If confirmed, use Task tool with `subagent_type="code-quality-reviewer"` then assist with git commit
4. Get commit info: `git log -1 --pretty=format:"%H%n%s"`

**If clean:** Get latest commit: `git log -1 --pretty=format:"%H%n%s"`

### Step 2: Confirm Understanding

**If you have context from recent work:**
- Summarize your understanding of objective, code location, output location
- Use AskUserQuestion tool to confirm with user

**If you don't have context:**
- Ask user for: objective, code location, output location

Then read code files, output files, and documentation to gather information.

### Step 3: Handle Figures

If figures exist in output folder:

```bash
mkdir -p Notes/WorkingJournal/attachments
cp Output/[subfolder]/figure.png Notes/WorkingJournal/attachments/YYYY-MM-DD-description.png
```

In markdown:
```markdown
![Descriptive caption](./attachments/YYYY-MM-DD-description.png)

Source: [Original](../../Output/[subfolder]/figure.png)
```

### Step 4: Create Working Journal Entry

**Filename:** `Notes/WorkingJournal/YYYY-MM-DD-[Author]-[Description].md`

**Front Matter:**
```yaml
---
author: "[[Author]]"
date: YYYY-MM-DD
project: "[[IntermediaryDemand]]"
git_commit: [full hash if available]
git_message: "[message if available]"
permalink: working-journal/YYYY-MM-DD-author-description
---
```

### Step 5: Write Summary

**Structure can be flexible**, but typically include:
- Objective section
- Summary of what was done
- Data description
- Methodology description
- Results with tables/figures
- Technical implementation details (code and outputs)

**Use relative paths from Notes/WorkingJournal/:**
- Code: `../../Code/`
- Output: `../../Output/`
- Data: `../../Data/`

## Critical Rules - MUST FOLLOW

### 1. Be Factual and Objective

**✓ DO:**
- State what was done and what was found
- Report numerical results precisely
- Describe methods used
- Link every claim to source (code, output, documentation)

**✗ DO NOT:**
- Interpret economic meaning without user request
- Speculate on causes or implications
- Make recommendations or suggest next steps
- Use subjective assessments ("excellent", "poor", "successful")

### 2. Examples

**Good (Factual):**
- "Processed 4.7M holdings from 11,857 submissions"
- "Difference of -30% (-$243B)"
- "Front-end tenors within 7% of benchmark"
- "Classification success rate: 70% (3,988 of 5,699)"

**Bad (Speculative/Interpretive):**
- "This suggests the classification is insufficient"
- "The results indicate strong performance"
- "This likely means we should use BKMS data"
- "The excellent match validates our approach"

### 3. Cite Everything

Every claim must link to supporting evidence:
- `[descriptive text](../../path/to/file)`
- Code files for methodology
- Output files for results
- Documentation for data sources

### 4. Figures

- Copy to attachments/ with descriptive filename
- Cite original source location
- Use descriptive captions

### Step 6: Verify Report Quality

After creating the report, use the report-checker agent to verify quality:

```
Use Task tool with subagent_type="report-checker"
Pass: report path, code location, output location, objective
```

The agent will check:
- All claims are cited and accurate
- No speculation or unsupported interpretation
- Numbers match source files
- No subjective language

If issues found, revise the report before finalizing.

## After Creating

1. Tell user the file path
2. List what was documented
3. Report any issues found by report-checker
4. Ask: "Would you like me to add any specific information?"
5. Do NOT suggest interpretations or next steps unless asked
