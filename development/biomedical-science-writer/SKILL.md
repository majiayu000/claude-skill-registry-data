---
name: biomedical-science-writer
description: Draft biomedical research manuscripts from research data. Use when user wants to write a research paper, has a project folder with papers, data, figures, and a GitHub repository link. Orchestrates context-ingestion, scoping, literature-review, code-analyzer, results-interpreter, synthesis, and assembler sub-skills.
---

# Biomedical Science Writer

Orchestrates the creation of scientific manuscript drafts through a structured, note-generating workflow.

## Core Principle: No Silent Assumptions

**This skill NEVER makes assumptions about user data without explicit confirmation.**

When encountering ambiguity in data, code, or figures:
1. **STOP** and ask the user for clarification
2. **DOCUMENT** all clarifications received
3. **VERIFY** interpretations before drafting

It is better to ask too many questions than to misinterpret the user's research. Every clarification is logged in the relevant notes files for transparency.

## Specialist Agents

This skill employs specialist agents for domain expertise:

| Agent | Role | Invoked During |
|-------|------|----------------|
| **Biostatistician** | Statistical accuracy review | Methods, Results |
| **Academic Reviewer** | Publication readiness review | Before Assembly |

### Biostatistician Agent

The biostatistician (`skills/biostatistician/SKILL.md`) ensures:
- Appropriate statistical test selection
- Assumption checking and validation
- Correct statistical reporting format
- Effect sizes with confidence intervals
- Multiple comparison handling

**No statistical claims are published without biostatistician sign-off.**

### Academic Reviewer Agent

The academic reviewer (`skills/academic-reviewer/SKILL.md`) acts as a skeptical peer reviewer:
- Verifies every claim is supported by its cited reference
- Validates the hypothesis is clinically meaningful and testable
- Confirms methods actually test the stated hypothesis
- **Independently interprets results** before reading Discussion
- Identifies discrepancies between evidence and author conclusions
- Flags overstatements and unsupported claims
- Routes issues to other agents or user for resolution

**No manuscript proceeds to final assembly without academic reviewer approval.**

## Expected Project Structure

User must organize their project folder as follows:

```
project/
├── papers/              # PDF files of relevant literature
│   ├── smith-2023.pdf
│   ├── jones-2022.pdf
│   └── ...
├── data/                # Raw data outputs (CSV, Excel)
│   ├── results.csv
│   ├── demographics.csv
│   └── ...
├── figures/             # Generated figures (PNG, JPG, SVG)
│   ├── figure1.png
│   ├── figure2.png
│   └── ...
├── irb/                 # OPTIONAL - IRB protocol documents (.pdf, .docx, .md)
│   ├── protocol.pdf     # IRB-approved protocol
│   └── amendments/      # Optional protocol amendments
└── config.md            # Project configuration (see template below)
```

### IRB Documents (Optional)

If provided, IRB documents enable:
- **Auto-populated ethics statement** in final manuscript
- **Scope comparison checkpoint** during scoping (catches discrepancies early)
- **Cross-reference validation** in Methods and Results (ensures consistency)

Supported formats: PDF, Word (.docx), Markdown (.md)

### config.md Template

```markdown
# Project Configuration

## GitHub Repository
url: https://github.com/username/repo-name
branch: main
access: private  # or public

## Constraints
word_limit: 3500
target_journal: Radiology: Artificial Intelligence
citation_style: AMA

## Additional Notes
[Any other context for the manuscript]
```

## Output Structure

The skill generates intermediate notes and drafts:

```
project/
├── notes/
│   ├── papers/              # Condensed notes per PDF (via subagent)
│   │   ├── smith-2023.md
│   │   └── jones-2022.md
│   ├── papers-library/      # ALL PDFs stored centrally
│   │   ├── smith-2023.pdf
│   │   └── jones-2022.pdf
│   ├── bibliography.md      # Master bibliography with citations/links
│   ├── literature-synthesis.md  # Aggregated themes and findings
│   ├── code-analysis.md     # GitHub repo analysis
│   ├── data-analysis.md     # Data/figures interpretation
│   ├── irb-summary.md       # IRB document extraction (if irb/ provided)
│   ├── irb-scope-comparison.md  # IRB vs actual scope (if irb/ provided)
│   ├── statistical-review.md    # Biostatistician sign-off report
│   └── reviewer-feedback.md     # Academic reviewer feedback
├── drafts/
│   ├── introduction.md
│   ├── methods.md
│   ├── results.md
│   ├── discussion.md
│   └── abstract.md
├── inventory.md             # What's available in project
├── scope.md                 # Research question, findings, constraints
└── manuscript.md            # Final assembled draft
```

## Workflow

```
[1. Context Ingestion] ─── skills/context-ingestion/SKILL.md
│   - Scan project folder structure
│   - Validate required folders exist
│   - Clone/analyze GitHub repository
│   - Extract IRB content → notes/irb-summary.md (if irb/ exists)
│   - Generate inventory.md
│
▼
[2. Scoping] ─── skills/scoping/SKILL.md
│   - Ask: research question
│   - Ask: key findings (cross-check with inventory)
│   - Ask: constraints (word limit, journal)
│   - ★ IRB SCOPE COMPARISON → Confirm discrepancies with user (if IRB exists)
│   - Generate scope.md, notes/irb-scope-comparison.md
│
▼
[3. Literature Review] ─── skills/literature-review/SKILL.md
│   - ★ SUBAGENT PER PAPER → Prevents context overflow
│   - Process each PDF via isolated subagent → notes/papers/*.md
│   - Synthesize from condensed notes → notes/literature-synthesis.md
│   - Draft Introduction → drafts/introduction.md
│
▼
[4. Code Analysis] ─── skills/code-analyzer/SKILL.md
│   - Analyze GitHub repository
│   - Extract methodology → notes/code-analysis.md
│   - ★ BIOSTATISTICIAN REVIEW → Validate methods
│   - Draft Methods → drafts/methods.md
│
▼
[5. Results Interpretation] ─── skills/results-interpreter/SKILL.md
│   - Analyze CSV data files
│   - Interpret figures
│   - Generate → notes/data-analysis.md
│   - ★ BIOSTATISTICIAN REVIEW → Validate statistics
│   - Draft Results → drafts/results.md
│
▼
[6. Synthesis] ─── skills/synthesis/SKILL.md
│   - Read all notes/*.md
│   - Read drafts/introduction.md, methods.md, results.md
│   - Draft Discussion → drafts/discussion.md
│   - Draft Abstract → drafts/abstract.md
│
▼
[7. Academic Review] ─── skills/academic-reviewer/SKILL.md
│   - Verify claims against citations
│   - Validate hypothesis and methods alignment
│   - ★ INDEPENDENTLY interpret results
│   - Compare to Discussion conclusions
│   - Generate → notes/reviewer-feedback.md
│   - Route issues to agents or user
│
▼
[8. Assembly] ─── skills/assembler/SKILL.md
    - Confirm reviewer approval
    - Combine all drafts
    - Populate ethics statement from IRB (if available)
    - Apply formatting constraints
    - Generate → manuscript.md
```

## Entry Points

The workflow supports multiple entry points:

| Command | Starts At | Use When |
|---------|-----------|----------|
| `/biomedical-science-writer:draft` | Step 1 | Full workflow from scratch |
| `/biomedical-science-writer:literature` | Step 3 | Scope exists, need lit review |
| `/biomedical-science-writer:methods` | Step 4 | Need to analyze code only |
| `/biomedical-science-writer:results` | Step 5 | Need to interpret data only |
| `/biomedical-science-writer:synthesize` | Step 6 | All drafts exist, need Discussion |
| `/biomedical-science-writer:assemble` | Step 7 | All sections drafted, need final doc |

## Executing the Workflow

### Step 1: Context Ingestion

Read `skills/context-ingestion/SKILL.md` and follow it to:
- Validate project folder structure
- Parse config.md for GitHub URL and constraints
- Clone or fetch GitHub repository
- Inventory all available materials
- Output: `inventory.md`

### Step 2: Scoping

Read `skills/scoping/SKILL.md` and follow it to:
- Review inventory.md
- Ask user for research question
- Ask user for key findings (validate against data)
- Confirm constraints from config.md
- Output: `scope.md`

### Step 3: Literature Review

Read `skills/literature-review/SKILL.md` and follow it to discover papers from three sources:
- **Source 1**: Process user-provided PDFs in `papers/` → `notes/papers/*.md`
- **Source 2**: Web search (PubMed, Google Scholar) for gaps → `notes/search/*.md`
- **Source 3**: Reference chaining from papers found above → `notes/references/*.md`
- **Save ALL PDFs** to central library → `notes/papers-library/*.pdf`
- **Validate** all papers have citations and links → `notes/bibliography.md`
- Synthesize findings across all sources → `notes/literature-synthesis.md`
- Draft Introduction using synthesis → `drafts/introduction.md`

### Step 4: Code Analysis

Read `skills/code-analyzer/SKILL.md` and follow it to:
- Analyze cloned GitHub repository
- Extract methodology, statistical approaches, tools
- Output: `notes/code-analysis.md`, `drafts/methods.md`

### Step 5: Results Interpretation

Read `skills/results-interpreter/SKILL.md` and follow it to:
- Analyze CSV files in `data/`
- Interpret figures in `figures/`
- Output: `notes/data-analysis.md`, `drafts/results.md`

### Step 6: Synthesis

Read `skills/synthesis/SKILL.md` and follow it to:
- Read all accumulated notes
- Integrate findings with literature context
- Output: `drafts/discussion.md`, `drafts/abstract.md`

### Step 7: Assembly

Read `skills/assembler/SKILL.md` and follow it to:
- Combine all draft sections
- Apply word limit and formatting
- Generate reference list
- Output: `manuscript.md`

## References

- `references/section-guidelines.md` - Writing conventions per section
- `references/citation-format.md` - Citation formatting styles
- `references/source-note-template.md` - Template for paper notes
