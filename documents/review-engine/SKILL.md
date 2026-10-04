---
name: review-engine
description: >
  Activate when the user provides reviewer or co-author feedback (annotated PDF,
  pasted comments, or reviewer report) and wants to implement revisions. Extracts
  review points, maps them to paper.tex locations, classifies actions, implements
  changes, recompiles, and generates a change log + latexdiff. Handles the full
  revision loop from feedback to committed changes.
---

> **Orchestration Log**: When this skill is activated, append a log entry to `outputs/orchestration_log.md`:
> ```
> ### Skill Activation: Review Engine (Round [N])
> **Timestamp:** [current date/time]
> **Actor:** AI Agent (review-engine)
> **Input:** [N] review points from [source] (annotated PDF / pasted text / reviewer report)
> **Output:** [N] changes implemented, paper recompiled, latexdiff generated
> **Human decisions:** [list of QUESTION items resolved by orchestrator]
> ```

# Review Engine

## Core Principle

Academic revision is a structured, repeatable process: **extract feedback -> interpret ->
classify -> implement -> verify**. This engine automates the entire loop. The human
orchestrator approves the change plan; the engine executes it.

This skill was derived from 4 actual co-author revision rounds on a real paper
(Blask & Funk, 2026). Every step reflects what we learned works — and what fails —
when processing human feedback on AI-generated manuscripts.

## When to Activate

- User provides an annotated PDF (co-author or reviewer comments)
- User pastes reviewer comments from a journal decision letter
- User says "implement these changes", "process this review", "revision round"
- User says "respond to reviewers", "R&R", "revise and resubmit"
- After self-review (Phase 6) produces a critique that needs implementation

## Prerequisites

- `paper.tex` exists in `latex/` and compiles successfully (this is the baseline)
- `pdflatex` and `bibtex` are available
- `latexdiff` is available (for visual change tracking)
- PyMuPDF (`fitz`) is available for PDF annotation extraction (`pip install pymupdf`)

---

## Step 1: EXTRACT Review Points

The first step is to get all review points into a structured format, regardless of
how the reviewer provided them.

### From Annotated PDF (Co-Author Review)

This is the most common case: a co-author annotates the PDF with highlights, sticky
notes, and text comments. Use `scripts/extract_annotations.py`:

```python
import sys
sys.path.insert(0, "scripts")
from extract_annotations import extract_annotations, annotations_to_markdown

annotations = extract_annotations("path/to/annotated.pdf")
print(annotations_to_markdown(annotations))
print(f"\nTotal: {len(annotations)} annotations found")
```

If `scripts/extract_annotations.py` is not available, use inline PyMuPDF:

```python
import fitz

doc = fitz.open("path/to/annotated.pdf")
annotations = []

for page_num, page in enumerate(doc, 1):
    for annot in page.annots() or []:
        entry = {
            "page": page_num,
            "type": annot.type[1],  # "Highlight", "Text", "FreeText", "StrikeOut"
            "content": annot.info.get("content", "").strip(),
            "author": annot.info.get("title", ""),
            "highlighted_text": "",
        }

        # Extract highlighted/marked text via quadpoints
        if annot.type[0] in (8, 9, 10, 11) and annot.vertices:  # Highlight, Underline, Squiggly, StrikeOut
            quad_count = len(annot.vertices) // 4
            text_parts = []
            for i in range(quad_count):
                quad = annot.vertices[i * 4:(i + 1) * 4]
                rect = fitz.Rect(
                    min(p[0] for p in quad), min(p[1] for p in quad),
                    max(p[0] for p in quad), max(p[1] for p in quad),
                )
                text_parts.append(page.get_text("text", clip=rect).strip())
            entry["highlighted_text"] = " ".join(text_parts)

        if entry["content"] or entry["highlighted_text"]:
            annotations.append(entry)

doc.close()
```

**Common pitfall:** The user may send the wrong PDF (without annotations). If
extraction returns 0 annotations, tell the user immediately and ask them to
re-send. Do NOT proceed with an empty annotation list.

### From Pasted Text (Journal R&R)

Parse reviewer comments by detecting common patterns:

```
Reviewer 1:
Major Comments:
1. The authors should clarify...
2. The methodology section lacks...

Minor Comments:
1. On page 5, the reference to...
```

Split into individual review points by:
- Numbered items ("1.", "2.", "-", "a)")
- Reviewer sections ("Reviewer 1:", "Reviewer 2:")
- Category headers ("Major Comments:", "Minor Comments:", "Questions:")
- Page/line references ("page 5", "line 42", "Section 3")

### From Self-Review (Phase 6 Output)

Parse the structured self-critique from `self_review.md` or the Phase 6 output.
Each bullet point or numbered item becomes a review point.

### Output Format

Every extraction method produces the same structure:

```
{
  "id": 1,
  "source": "pdf_annotation" | "pasted_text" | "self_review",
  "page": 5,                    # PDF page (if applicable)
  "type": "Highlight",          # Annotation type (if PDF)
  "reviewer": "Burkhardt Funk", # Reviewer name (if known)
  "reviewer_text": "just delete, I think ref to tab 1 is also wrong here",
  "highlighted_text": "Following Hevner et al.'s guidelines, we evaluate in three steps",
  "section_ref": null            # Will be filled in Step 2
}
```

---

## Step 2: MAP to Source

For each review point, locate the corresponding position in `paper.tex`.

### Mapping Strategy

1. **Primary: Text match.** Take the `highlighted_text` (or key phrases from
   `reviewer_text`) and search `paper.tex` using grep/search. Handle:
   - LaTeX commands embedded in text (`\textit{...}`, `\citep{...}`)
   - Line breaks (the PDF renders continuous text that spans multiple LaTeX lines)
   - Ligatures and special characters (fi, fl, -- vs. --)

2. **Secondary: Page-to-section estimation.** If no text match is found, use the
   PDF page number to estimate which LaTeX section it corresponds to. Compile the
   paper, check page breaks, and narrow down the section.

3. **Tertiary: Manual flag.** If neither works, flag the review point with
   `mapping_confidence: low` and present it to the user for manual location.

### Identifying Section Context

For each matched location, also extract:
- The `\section{}` or `\subsection{}` it belongs to
- The line number in `paper.tex`
- 3 lines of surrounding context (for the change plan display)

### Output

Each review point is enriched:

```
{
  ...,
  "tex_line": 256,
  "tex_section": "\\subsection{Pipeline Implementation}",
  "tex_context": "Following Hevner et al.'s guidelines, we evaluate in three steps...",
  "mapping_confidence": "high" | "medium" | "low"
}
```

---

## Step 3: CLASSIFY Actions

For each review point, determine what the reviewer is asking for and how to respond.

### Action Types

| Type | Description | Automation | Example |
|------|-------------|-----------|---------|
| `DELETE` | Remove text entirely | Full auto | "just delete" |
| `REPLACE` | Change specific text or terminology | Full auto | "systems -> agents" |
| `MOVE` | Relocate content to different section | Guided auto | "belongs in conclusion" |
| `RESTRUCTURE` | Reorganize section flow/argument | Needs plan approval | "Better: briefly describe each agent" |
| `FIX` | Correct references, typos, formatting | Full auto | "is it 7.1?" |
| `FIGURE` | Modify or regenerate a figure | Invoke figure-engine | "extend orchestrator zone" |
| `SHORTEN` | Reduce or condense text | Guided auto | "zu kleinteilig" |
| `EXPAND` | Add more detail or explanation | Invoke writing-engine | "elaborate on methodology" |
| `APPROVE` | No action needed (positive feedback) | Log only | "fine with phases" |
| `QUESTION` | Ambiguous -- needs human decision | Block + ask | "do we do that?" |

### Priority Levels

- **CRITICAL:** Factual error, wrong reference, misattribution, missing content
- **MAJOR:** Structural change, unclear argument, missing justification
- **MINOR:** Wording improvements, terminology, formatting
- **COSMETIC:** Typos, spacing, style preferences

### Classification Process

For each review point:
1. Read the `reviewer_text` in context of `highlighted_text`
2. Determine intent (what does the reviewer want changed?)
3. Assign `action_type` and `priority`
4. For actionable items, draft a `proposed_change` (1-sentence description)
5. Determine `automation_level`: can this be done automatically, or does it need
   human input or another engine (figure-engine, writing-engine)?

### Handling Multilingual Comments

Reviewers may comment in any language (German is common in DACH academia).
Interpret the comment in its original language; do not require translation.
Common German review phrases:
- "streichen" / "löschen" = DELETE
- "umformulieren" = REPLACE/RESTRUCTURE
- "verschieben nach" = MOVE
- "zu lang" / "kürzen" = SHORTEN
- "passt" / "ok" / "einverstanden" = APPROVE
- "unklar" / "verstehe ich nicht" = needs EXPAND or RESTRUCTURE

### Output

Each review point is enriched:

```
{
  ...,
  "action_type": "DELETE",
  "priority": "MAJOR",
  "automation_level": "full_auto" | "guided" | "needs_approval" | "needs_engine" | "needs_human",
  "proposed_change": "Remove the three-step evaluation paragraph at line 256",
  "depends_on": []  // IDs of other changes this depends on
}
```

---

## Step 4: PLAN -- Present Change Plan

**This is the QUALITY GATE. Do NOT proceed without user approval.**

### Change Plan Format

Present a structured overview of all review points and proposed changes:

```
📋 REVISION PLAN -- Round [N]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Source: [annotated PDF from Burkhardt Funk / Reviewer 1 report / ...]
Extracted: [N] review points
Actionable: [N] changes | Approved: [N] (no action) | Questions: [N] for you

 #  | Type        | Priority | Section | Reviewer Said               | Proposed Change
----|-------------|----------|---------|-----------------------------|--------------------------
 1  | REPLACE     | MINOR    | global  | "systems -> agents"         | Global replace in 8 locations
 2  | DELETE      | MAJOR    | S4.1    | "just delete"               | Remove eval paragraph (L256)
 3  | MOVE        | MAJOR    | S4.2    | "belongs in conclusion"     | Move scope para to S8
 4  | RESTRUCTURE | MAJOR    | S4.2    | "briefly describe each agent"| Rewrite with phase summaries
 5  | FIX         | MINOR    | S7.3    | "is it 7.1?"               | Fix cross-reference
 6  | FIGURE      | MAJOR    | Fig 1   | "extend orchestrator zone"  | Regenerate via PaperBanana
 7  | APPROVE     | --       | S2.5    | "fine with phases"          | No action -- logged
 8  | QUESTION    | MAJOR    | S4.2    | "do we do that?"            | ⚠️  Need your decision

⚠️  QUESTIONS requiring your input:
  Q1 (#8): Burkhardt asks "do we do that? delete?" about Phase 5/6 descriptions.
           -> Delete entirely, or shorten to one sentence each?

Execution order (respecting dependencies):
  1 -> 2 -> 3 -> 4 -> 5 -> 6

🔄 Approve plan to proceed with implementation.
   -> Override: modify any proposed change before I execute.
```

### Handling Questions

For items classified as `QUESTION`:
- Present the reviewer's comment with full context
- Offer 2-3 concrete options (not open-ended)
- Wait for user's decision
- Update the change plan with the decision
- Re-present if needed

### Dependencies

Some changes depend on others:
- Terminology replacement should happen BEFORE restructuring (so the new text
  already uses correct terms)
- Moves should happen BEFORE expansions (so new text goes to the right place)
- Fixes should happen AFTER structural changes (cross-references may shift)

Build a dependency graph and present the execution order.

---

## Step 5: IMPLEMENT Changes

After the user approves the plan, execute changes in dependency order.

### Execution Order

1. **Global terminology changes** (`REPLACE` with `replace_all: true`)
   - These affect the entire file and should be done first
   - Example: replace "research systems" with "research agents" globally

2. **Deletions** (`DELETE`)
   - Remove content cleanly, leaving a comment marker
   - Format: `% [R{round}: {brief description} -- deleted per {reviewer}]`

3. **Moves** (`MOVE`)
   - Cut content from source location (leave comment marker)
   - Paste at target location with transition sentences
   - Fix any cross-references that pointed to the moved content

4. **Restructures** (`RESTRUCTURE`)
   - These are the most complex changes -- rewrite section flow
   - Invoke writing-engine if new text needs to be drafted
   - Preserve citation keys and cross-references

5. **Shortenings** (`SHORTEN`)
   - Condense text while preserving key information and citations
   - Leave comment marker noting what was shortened

6. **Fixes** (`FIX`)
   - Cross-reference corrections: scan all `\label{}`, fix `\ref{}`
   - Typo corrections
   - Formatting fixes

7. **Figure changes** (`FIGURE`)
   - Invoke figure-engine skill
   - Use PaperBanana direct Python API via `paperbanana_direct.py`
   - Copy generated figure to `latex/figures/`
   - Update `\includegraphics` path if needed

8. **Expansions** (`EXPAND`)
   - Invoke writing-engine skill for new text
   - Place at correct location
   - Integrate with surrounding text

### Comment Markers

Every change gets a LaTeX comment marker for traceability:

```latex
% [R3: Moved scope paragraph to conclusion per Burkhardt]
% [R3-05: Fixed cross-reference Section 6.1 -> \ref{sec:task_redistribution}]
% [R4: Three-step evaluation paragraph deleted per Burkhardt]
```

Format: `% [R{round}: {brief description}]`
Or with ID: `% [R{round}-{change_number}: {description}]`

---

## Step 6: VERIFY

After all changes are implemented, verify the paper still compiles and looks correct.

### Compilation

Run the full LaTeX compilation cycle:

```bash
cd latex/
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex -interaction=nonstopmode paper.tex
pdflatex -interaction=nonstopmode paper.tex
```

**Target:** 0 errors, 0 undefined references, 0 undefined citations.

If compilation fails:
1. Check the `.log` file for the error
2. Fix the issue (usually a mismatched brace, missing `\end{}`, or bad `\ref{}`)
3. Recompile (up to 3 fix-recompile attempts)
4. If still failing after 3 attempts, present the error to the user

### Latexdiff

Generate a visual diff against the baseline:

```bash
latexdiff <(git show BASELINE_COMMIT:latex/paper.tex) latex/paper.tex > latex/paper_diff.tex
pdflatex -interaction=nonstopmode latex/paper_diff.tex
bibtex paper_diff
pdflatex -interaction=nonstopmode latex/paper_diff.tex
pdflatex -interaction=nonstopmode latex/paper_diff.tex
```

The baseline commit should be:
- The commit just before the first revision round started
- Or a user-specified commit hash

### Sanity Checks

1. **Page count:** Should be within +/-2 pages of the original. Major deviations
   indicate something went wrong (content accidentally deleted or duplicated).
2. **References:** `grep "undefined" paper.log` should return 0 matches.
3. **Orphans:** All figures referenced in text should exist in `figures/`.
4. **Bibliography:** All `\citep` / `\citet` keys should resolve.

### Verification Report

```
✅ REVISION ROUND [N] COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 paper.pdf -- [N] pages, 0 errors
📊 Changes implemented: [N] of [N] planned
📝 paper_diff.pdf generated against baseline [commit hash]

Compilation:  ✅ Clean (0 errors, 0 warnings)
References:   ✅ All \ref{} and \citep{} resolved
Page count:   [N] pages (was [N] before revision)
Figures:      ✅ All [N] figures present

Review points:
  ✅ Implemented:  [N]
  ℹ️  Approved:    [N] (no action needed)
  ❓ Deferred:    [N] (marked for next round)
```

---

## Step 7: DOCUMENT

### Change Log

Save a detailed change log for each round:

**File:** `outputs/revision_log_r{N}.md`

```markdown
# Revision Log -- Round [N]

**Date:** [ISO 8601]
**Reviewer:** [name]
**Source:** [annotated PDF / pasted comments / reviewer report]
**Review points:** [N] total ([N] implemented, [N] approved, [N] deferred)

## Changes Implemented

### Change 1: [brief title]
- **Type:** REPLACE
- **Reviewer said:** "[exact quote]"
- **Action:** Global replacement of "research systems" with "research agents" (8 occurrences)
- **Files affected:** paper.tex (lines 118, 235, 255, ...)

### Change 2: [brief title]
...

## No Action Required

### Approval 1: [brief title]
- **Reviewer said:** "[exact quote]"
- **Reason:** Positive feedback, no change needed

## Deferred to Next Round (if any)

### Deferred 1: [brief title]
- **Reviewer said:** "[exact quote]"
- **Reason:** Needs empirical data / needs further discussion
```

### Revision Letter (for Journal R&R)

If the review came from a journal, generate a formal revision letter:

**File:** `outputs/revision_letter.md`

```markdown
# Response to Reviewers

Dear Editor,

Thank you for the opportunity to revise our manuscript "[title]" (MS-XXXX).
We have carefully addressed all reviewer comments as detailed below.

---

## Reviewer 1

### Comment 1.1
> [Exact quote of reviewer comment]

**Response:** [How we addressed it]
**Change:** [Specific change made, with section/page reference]

### Comment 1.2
> [Exact quote]

**Response:** ...

---

## Reviewer 2
...
```

### Orchestration Log

Append to `outputs/orchestration_log.md`:

```markdown
## Phase 8: Revision (Round [N])
**Timestamp:** [ISO 8601]
**Actor:** AI Agent (review-engine)
**Action:** Processed [N] review points from [reviewer], implemented [N] changes
**Key metrics:** [N] review points, [N] changes, [N] approvals, [N] questions resolved
**Output artifacts:** paper.pdf, paper_diff.pdf, revision_log_r[N].md

**Quality Gate Decision:** [Approved / Redirected]
**Orchestrator Feedback:** "[user's response to change plan]"
**Scope Changes:** [any modifications to proposed changes]
```

### Git Commit

If the user approves:

```bash
git add latex/paper.tex latex/paper.pdf latex/paper_diff.pdf outputs/revision_log_r*.md
git commit -m "Round [N]: implement [reviewer] review ([N] changes)

Changes: [1-line summary of each change]

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Error Recovery

- **PDF has no annotations:** Tell the user immediately. Ask if they sent the
  correct file. Do NOT proceed with empty annotations.
- **Text not found in paper.tex:** Flag the review point with low confidence.
  Present to user with the reviewer's comment and ask them to locate it manually.
- **Compilation fails after changes:** Revert the last change, try again.
  If persistent, present the error and the problematic change to the user.
- **Conflicting reviewer instructions:** Present both to the user with options.
  Do not make the decision autonomously.
- **Figure generation fails:** Note it in the change plan, continue with other
  changes. Flag the figure change as "deferred" in the change log.

---

## Integration with Other Engines

The review engine orchestrates other skills when needed:

| Change Type | Engine Invoked | Purpose |
|-------------|---------------|---------|
| FIGURE | figure-engine | Regenerate diagrams via PaperBanana |
| EXPAND | writing-engine | Draft new text following academic templates |
| RESTRUCTURE | writing-engine | Rewrite sections following paragraph formulas |
| FIX (citations) | verification-engine | Verify corrected citations are accurate |
| COMPILE | latex-engine | LaTeX compilation and PDF generation |

---

## Iteration

This phase is designed to repeat:

```
Round 1: Major structural feedback  -> implement -> send back
Round 2: Terminology and flow       -> implement -> send back
Round 3: Minor corrections          -> implement -> send back
Round 4: Final approval + cosmetics -> implement -> done
```

Each round:
- Uses the SAME baseline commit for latexdiff (cumulative changes visible)
- Increments the round number in comment markers (`R1`, `R2`, `R3`, `R4`)
- Produces its own revision log (`revision_log_r1.md`, `revision_log_r2.md`, ...)
- Can handle feedback from multiple reviewers simultaneously (group by reviewer)
