---
name: paper-edit
description: Paper editing with built-in style constraints for academic writing quality, including anti-AI detection, LaTeX validation, and figure standards
tags: [Writing, LaTeX, Academic, Paper]
---

# Paper Edit

Edit academic papers with enforced style constraints to ensure human-quality writing and clean presentation.

## When to Use

- Editing or revising LaTeX paper sections
- Polishing paper drafts before submission
- Converting between conference templates
- Shortening paper to meet page limits
- Cleaning up figures and captions

## Style Rules (ALWAYS Enforced)

### Writing Style

**Banned patterns --- never use these:**
- Em-dashes (`---` or `--`) --- replace with commas, periods, or parentheses
- AI-style phrases: 'notably', 'leveraging', 'comprehensive', 'crucial', 'landscape', 'delve', 'furthermore', 'utilize', 'facilitate', 'underscore', 'in the realm of'
- Passive voice overuse --- prefer active voice
- Overly long sentences (>40 words) --- split them
- Redundant hedging: 'it is worth noting that', 'it should be noted that'

**Required style:**
- Natural, human academic tone
- Direct and concise
- Logical flow between sentences and paragraphs
- Consistent terminology throughout

### LaTeX Conventions

- `\cite{a,b,c}` --- no spaces after commas
- Use `\cref` or `\Cref` for cross-references when available
- Table/figure labels: `\label{tab:xxx}`, `\label{fig:xxx}`
- No orphan `\item` or `\\` at end of paragraphs
- Compile with `pdflatex` after each edit to verify

### Figure Standards

- **Clean and minimal** --- no decorative elements
- No unnecessary arrows, crowded labels, or extra legends
- Simple color schemes (colorblind-friendly preferred)
- Clear axis labels with readable font sizes (minimum 8pt)
- Captions: under 2 lines, factual, no interpretation
- Use vector formats (PDF) when possible

### Caption Standards

- Short and factual: describe what the figure shows
- No interpretation or analysis in captions
- Format: "[Description of what is shown]. [Key observation if needed]."
- Under 2 lines for figures, under 3 lines for tables

## Workflow

### Step 0: Stage Plan (for restructures or 3+ edits)

Before touching any file, if the request involves restructuring, multiple sections, or more than 3 separate edits:

1. List every file and section you will touch.
2. Group edits into 3-5 stages with a compilation checkpoint after each.
3. Present the plan and **wait for user approval** before executing stage 1.
4. Do not bundle stages. Re-confirm between stages if scope changes.

For single targeted edits (e.g., "fix typo in §2.1"), skip Step 0 and apply directly.

### Scope Discipline (always)

- When the user names specific items (reviewer comment numbers, flagged locations, bullets), edit ONLY those items.
- Never wholesale-replace an abstract, section, or formatting unless explicitly asked.
- During venue rebrands (e.g., CCS→NDSS), preserve all citations; only update template/formatting.

### Step 1: Read the Target Section

Read the full section to understand context and flow. Do not read sibling sections unless explicitly part of the requested scope.

### Step 2: Scan for Violations

Check for all style rule violations:
1. Grep for em-dashes: `---` and `--` (outside of LaTeX comments)
2. Grep for banned phrases
3. Check caption lengths
4. Verify `\cite` formatting

### Step 3: Apply Fixes

Fix violations while preserving the author's intent and argument structure. Do not rewrite content unnecessarily --- only fix what violates the rules.

### Step 4: Verify Compilation

```bash
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
```

Report any compilation errors and fix them.

### Step 5: Summary Report

After editing, report:
- Number of em-dashes removed
- Number of AI phrases replaced
- Captions shortened (if any)
- Compilation status
- Any remaining issues

## Page Reduction Tips

When asked to shorten a paper:
1. **Captions first** --- shorten verbose captions
2. **Redundant text** --- remove sentences that repeat prior content
3. **Tighten figures** --- reduce whitespace, combine subfigures
4. **Compress related work** --- cite and move on, don't summarize extensively
5. **LaTeX tricks last** --- `\vspace{-Xpt}`, `\setlength` adjustments

## Integration

- `latex-check.js` PostToolUse hook auto-validates compilation after .tex edits
- `writing-anti-ai` skill provides deeper anti-AI writing analysis
- `ml-paper-writing` skill provides venue-specific writing guidance
