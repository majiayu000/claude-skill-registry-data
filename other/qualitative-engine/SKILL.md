---
name: qualitative-engine
description: >
  Activate when the user needs to analyze qualitative data — interview transcripts,
  field notes, or open-ended survey responses. Handles structured summarization,
  thematic coding, cross-case analysis, theme matrices, and evidence retrieval.
  Designed to solve the context-window problem: generates compact summaries first,
  then works from summaries instead of full transcripts. Only loads full text
  when specific quotes are needed. Supports Gioia, Mayring, Grounded Theory,
  and general thematic analysis workflows.
---

> **Orchestration Log**: When this skill is activated, append a log entry to `outputs/orchestration_log.md`:
> ```
> ### Skill Activation: Qualitative Engine
> **Timestamp:** [current date/time]
> **Actor:** AI Agent (qualitative-engine)
> **Input:** [brief description of the analysis request]
> **Output:** [brief description — e.g., "23 interviews summarized, 14 first-order codes identified"]
> ```

# Qualitative Engine

## Core Principle: Summary-First, Full-Text-on-Demand

**CRITICAL:** Qualitative data (interview transcripts) can easily overflow the context window.
Follow this strict protocol:

1. **NEVER load all transcripts into context simultaneously**
2. **ALWAYS generate structured summaries first** (Phase 1)
3. **Work from summaries** for coding and analysis (Phases 2-4)
4. **Load full transcripts ONLY** when extracting specific verbatim quotes (Phase 5)
5. **Load at most 2-3 full transcripts at a time** when quote-hunting

## Utility Script

The `scripts/process_interviews.py` script provides:

```python
from scripts.process_interviews import (
    load_interviews,      # Read all .md files from interviews/
    build_index,          # Generate INDEX.md with metadata
    chunk_interview,      # Split long transcripts into chunks
    search_interviews,    # Keyword search across all interviews
    save_index,           # Save index file
    save_summary,         # Save individual summaries
)
```

---

## Phase 1: Structured Summarization

### Purpose
Transform each full transcript into a compact structured summary (~300 words)
that preserves analytical value while reducing context consumption by 80-90%.

### Step 1: Build Interview Index

```python
interviews = load_interviews("interviews/")
index = build_index(interviews)
save_index(index, "interviews/INDEX.md")
```

### Step 2: Generate Summaries

For EACH interview, read the full transcript and produce a summary in this exact format:

```markdown
# Summary: [Interviewee Name / Title]
**Date:** [date]  |  **Role:** [professional role]  |  **Organization:** [org]  |  **Duration:** [if available]

## Context
[1-2 sentences: Who is this person? Why were they interviewed? What is their relevance?]

## Key Statements (verbatim quotes)
1. "[Direct quote — max 2 sentences]" — on [topic]
2. "[Direct quote — max 2 sentences]" — on [topic]
3. "[Direct quote — max 2 sentences]" — on [topic]
[3-5 quotes that capture the most analytically valuable statements]

## Core Themes Discussed
- **[Theme A]:** [2-3 sentence summary of their position/experience]
- **[Theme B]:** [2-3 sentence summary]
- **[Theme C]:** [2-3 sentence summary]

## Unique Insights
[1-2 sentences: What does this interviewee say that NO other interviewee says?
What is their unique contribution to the data set?]

## Relevance to Research Questions
- **RQ1:** [How does this interview inform RQ1? One sentence.]
- **RQ2:** [How does this interview inform RQ2? One sentence.]
- **RQ3:** [How does this interview inform RQ3? One sentence.]
[Adapt RQs from framing.md]
```

### Step 3: Save Summaries

```python
save_summary(summary_text, "interviews/summaries/[filename]_summary.md")
```

### Context Budget Rule
- Process interviews **one at a time**: read transcript → generate summary → save → move to next
- After all summaries are generated, the summaries/ directory becomes the primary data source
- Total summary corpus: ~23 interviews × 300 words = ~7,000 words (fits easily in context)

---

## Phase 2: Initial Coding (First-Order Codes)

### Purpose
Identify empirical codes grounded in the data — what interviewees actually say.

### Input
Load ALL summary files (not full transcripts):
```
interviews/summaries/*.md
```

### Coding Process

1. **Read all summaries** in sequence
2. **Identify recurring patterns** across interviews:
   - What topics come up repeatedly?
   - What language do interviewees use?
   - What problems, solutions, or experiences are described?
3. **Generate first-order codes** — stay close to the data:
   - Use informant-centric language (in-vivo codes where possible)
   - Each code = a specific empirical observation, not an abstract concept
   - Target: 20-40 first-order codes

### Output Format: Codebook v1

```markdown
# Codebook v1 — First-Order Codes

**Date:** [date]
**Interviews coded:** [N]
**Total codes:** [N]

| Code ID | Code Label | Description | Example Quote | Frequency |
|---------|-----------|-------------|---------------|-----------|
| C01 | [label] | [what this code captures] | "[short quote]" — [interviewee] | [N interviews] |
| C02 | [label] | [what this code captures] | "[short quote]" — [interviewee] | [N interviews] |
| ... | | | | |
```

Save to: `outputs/codebook_v1.md`

### Code-to-Interview Matrix

```markdown
| Code | Interview 1 | Interview 2 | Interview 3 | ... | Total |
|------|------------|------------|------------|-----|-------|
| C01  | ✓          | ✓          |            | ... | N     |
| C02  |            | ✓          | ✓          | ... | N     |
```

Save to: `outputs/code_matrix.md`

---

## Phase 3: Thematic Grouping (Second-Order Themes)

### Purpose
Group first-order codes into higher-level analytical themes.

### Process

1. **Review the codebook** — look for clusters of related codes
2. **Group codes into themes** — each theme aggregates 2-5 first-order codes
3. **Name themes analytically** — researcher language, not informant language
4. **Target: 5-10 second-order themes**

### For Gioia Method

If using the Gioia methodology, produce the three-level data structure:

```markdown
# Gioia Data Structure

| First-Order Codes (Informant) | Second-Order Themes (Researcher) | Aggregate Dimensions |
|------------------------------|----------------------------------|---------------------|
| "We just got the tool and figured it out" | Ad-hoc AI adoption | **Unstructured Implementation** |
| "Nobody trained us on how to use it" | Missing capability building | |
| "We spent 2 hours on what used to take 2 days" | Efficiency gains from AI | **Process Transformation** |
| "The routine work basically disappeared" | Routine task elimination | |
| ... | | |
```

Save to: `outputs/gioia_data_structure.md`

### For Thematic Analysis (Braun & Clarke)

```markdown
# Theme Map

## Theme 1: [Name]
**Definition:** [What this theme captures]
**Codes included:** C01, C05, C12
**Prevalence:** [N] of [N] interviews
**Key insight:** [1 sentence]

## Theme 2: [Name]
...
```

Save to: `outputs/theme_map.md`

### For Mayring Content Analysis

```markdown
# Category System

## Main Category 1: [Name]
### Sub-Category 1.1: [Name]
**Definition:** [precise definition]
**Anchor example:** "[quote]" — [interviewee]
**Coding rule:** [when to apply this code]

### Sub-Category 1.2: [Name]
...
```

Save to: `outputs/category_system.md`

---

## Phase 4: Cross-Case Analysis

### Purpose
Systematic comparison across interviews to identify patterns and outliers.

### Cross-Case Theme Matrix

```markdown
# Cross-Case Analysis

| Interviewee | Role | Theme 1 | Theme 2 | Theme 3 | Theme 4 | Theme 5 |
|------------|------|---------|---------|---------|---------|---------|
| [Name 1] | [Role] | Strong | Moderate | Absent | Strong | Weak |
| [Name 2] | [Role] | Weak | Strong | Strong | Absent | Moderate |
| ... | | | | | | |

## Pattern Analysis
- **Universal themes** (present in >80% of interviews): [list]
- **Majority themes** (50-80%): [list]
- **Minority/emerging themes** (20-50%): [list]
- **Outlier insights** (<20%, but analytically important): [list]

## Role-Based Patterns
- **Analysts** tend to emphasize: [themes]
- **Senior management** tends to emphasize: [themes]
- **Technology roles** tend to emphasize: [themes]

## Contradictions and Tensions
- [Theme X] vs. [Theme Y]: [describe the tension and which interviewees represent each side]
```

Save to: `outputs/cross_case_analysis.md`

---

## Phase 5: Evidence Retrieval (Quote Mining)

### Purpose
Go back to FULL transcripts to extract verbatim quotes for specific themes.

### CRITICAL: Context Management
- **Identify which quotes you need** from the summaries and code matrix FIRST
- **Then load ONLY the specific transcripts** that contain those quotes (max 2-3 at a time)
- **Use the search utility** to find relevant passages:

```python
results = search_interviews(interviews, ["AI transformation", "copilot", "tool adoption"])
for r in results[:10]:
    print(f"[{r['interview']}]: ...{r['context']}...")
```

### Quote Selection Criteria
For each theme, select 2-3 quotes that are:
- **Representative** (captures what most interviewees said)
- **Vivid** (well-articulated, memorable)
- **Analytically rich** (connects to theoretical concepts)

### Output: Evidence Table

```markdown
# Evidence Table

## Theme 1: [Name]

| Quote | Interviewee | Role | Relevance |
|-------|------------|------|-----------|
| "[Verbatim quote]" | [Name] | [Role] | Representative — captures majority view on [topic] |
| "[Verbatim quote]" | [Name] | [Role] | Contrasting — shows alternative perspective |
| "[Verbatim quote]" | [Name] | [Role] | Rich — connects to [theoretical concept] |

## Theme 2: [Name]
...
```

Save to: `outputs/evidence_table.md`

---

## Phase 6: Integration with Writing Engine

### Passing Results to Writing Engine

When the writing-engine needs qualitative findings, provide:

1. **Theme map** (from Phase 3) — for structuring the findings section
2. **Cross-case matrix** (from Phase 4) — for comparative analysis
3. **Evidence table** (from Phase 5) — for inline quotes

### Findings Section Template

```markdown
## Findings

### [Theme 1 Name]

[Interpretive paragraph linking theme to research question. 2-3 sentences.]

Interviewees consistently described [pattern]. As [Interviewee Name], a [role], explained:

> "[Verbatim quote — 1-3 sentences]"

This pattern was echoed across [N] of [N] interviews, particularly among [role group].
[Additional interpretation, 2-3 sentences.]

### [Theme 2 Name]
...
```

---

## Quality Assurance Checklist

Before presenting qualitative analysis to the user, verify:

- [ ] **Summaries exist** for all interviews (`interviews/summaries/`)
- [ ] **Codebook** has clear definitions and anchor examples
- [ ] **Each code** appears in at least 2 interviews (drop singletons unless analytically crucial)
- [ ] **Themes** are analytically distinct (no significant overlap)
- [ ] **Quotes** are verbatim (verified against full transcript)
- [ ] **Negative cases** are acknowledged (interviewees who contradict the dominant pattern)
- [ ] **Context budget** was respected (no full-corpus loading)

---

## Activation Triggers

Activate this engine when the user:
- Asks to "analyze interviews" or "code transcripts"
- Mentions "thematic analysis", "Gioia", "Mayring", "grounded theory"
- Asks to "summarize interviews" or "create interview summaries"
- Needs to "find quotes" or "evidence for [theme]"
- Wants a "cross-case analysis" or "theme matrix"
- Has qualitative data (transcripts, field notes) and needs to process it
