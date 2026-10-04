---
name: submission-engine
description: >
  Activate when the user wants to prepare a paper for submission to a specific
  venue. Handles venue-specific formatting validation, anonymization checks for
  double-blind review, cover letter generation, suggested reviewer identification,
  and submission checklist completion. Produces a submission-ready package.
---

> **Orchestration Log**: When this skill is activated, append a log entry to `outputs/orchestration_log.md`:
> ```
> ### Skill Activation: Submission Engine
> **Timestamp:** [current date/time]
> **Actor:** AI Agent (submission-engine)
> **Input:** Target venue: [venue], paper: [paper.tex / draft.md]
> **Output:** Submission package prepared: cover letter, anonymization report, checklist
> ```

# Submission Engine

## Core Principle

A paper is only as good as its submission package. Many strong papers receive desk
rejections because of anonymization failures, formatting errors, or missing cover
letters. This engine ensures that the transition from "paper is ready" to "paper is
submitted" is error-free and complete.

## When to Activate

- User says "prepare submission", "submit to [venue]", "submission package"
- User says "anonymize", "blind review", "double-blind check"
- User says "cover letter", "suggested reviewers", "submission checklist"
- After Phase 6 (LaTeX export) when the paper is ready for submission
- User runs `/prepare-submission`

## Prerequisites

- `latex/paper.tex` exists and compiles
- `latex/paper.pdf` exists
- Target venue is specified (or can be inferred from framing.md)

---

## Step 1: IDENTIFY Target Venue & Load Requirements

### Venue Database

For common IS/CS venues, apply known formatting requirements:

| Venue | Type | Page Limit | Format | Blind | Template |
|-------|------|-----------|--------|-------|----------|
| ICIS | Conference | 17 pages | AIS template | Double-blind | AIS Electronic Library |
| ECIS | Conference | 15 pages (research) / 12 (short) | AIS template | Double-blind | AIS Electronic Library |
| HICSS | Conference | 10 pages | IEEE format | Single-blind | IEEE |
| WI | Conference | 12 pages | Springer LNBIP | Double-blind | Springer |
| AMCIS | Conference | 10 pages | AIS template | Double-blind | AIS Electronic Library |
| MISQ | Journal | No strict limit (~40-60 pages) | MISQ style | Double-blind | MISQ website |
| ISR | Journal | No strict limit (~30-50 pages) | INFORMS style | Double-blind | PubsOnline |
| EJIS | Journal | ~8000-10000 words | Taylor & Francis | Double-blind | T&F website |
| BISE | Journal | ~8000-10000 words | Springer | Double-blind | Springer |
| JIT | Journal | ~8000-10000 words | Sage | Double-blind | Sage |

If venue is not in the database:
1. Search web for "[venue name] submission guidelines" / "author guidelines"
2. Extract: page limit, format, blind review policy, template requirements
3. Document in submission package

### Venue-Specific Checks

For the identified venue, create a checklist of formatting requirements:
- Page/word limit
- Font and spacing requirements
- Reference style (APA, IEEE, ACM, etc.)
- Abstract word limit
- Keywords required?
- Author info format
- Appendix rules
- Figure/table formatting rules

---

## Step 2: ANONYMIZATION CHECK (for Double-Blind)

### What to Check

Scan `paper.tex` for any element that could reveal author identity:

| Check | What to Find | How to Fix |
|-------|-------------|-----------|
| **Author names** | `\author{}`, author names in text | Remove or replace with "Author" |
| **Self-citations** | "we previously showed (OurName, 2023)" or "in our prior work" | Replace with "(Author, Year)" or rephrase |
| **Institutional references** | University names, lab names, company names | Anonymize: "[Anonymous University]" |
| **Acknowledgments** | `\section*{Acknowledgments}` with grant numbers, names | Remove entirely or anonymize |
| **URLs/links** | GitHub repos, project websites, personal pages | Remove or anonymize |
| **File metadata** | PDF properties (author field in LaTeX) | Check `\hypersetup{pdfauthor=...}` |
| **Track changes** | Comment markers with author names | Remove `% [R3: ... per AuthorName]` |
| **Funding info** | Grant numbers linked to specific PIs | Remove or generalize |
| **Supplementary material** | Links to identifiable repositories | Use anonymous sharing (e.g., anonymous GitHub) |

### Self-Citation Detection

Self-citations are the #1 anonymization failure. Scan for:

1. **Explicit self-refs:** Search for all author names from `\author{}` in citation keys and text
2. **Implicit self-refs:** Patterns like:
   - "In our previous work" / "In prior work, we" / "We have shown"
   - "Building on [OurPaper]" where OurPaper is by any of the authors
   - "As Author1 and Author2 (Year) demonstrated" where Author1/2 are paper authors
3. **Citation key patterns:** Check if any `\citep{}`/`\citet{}` keys contain author last names that match paper authors

### Fix Strategy

For each finding:
- **Self-citations (critical):** Replace with "(Author, Year)" and add to a separate "self-citations" list that can be restored after acceptance
- **Author info:** Create a separate `paper_deanonymized.tex` that preserves the original author information
- **Acknowledgments:** Move to a `acknowledgments_hidden.tex` file for post-acceptance restoration

### Output

```markdown
## Anonymization Report

**Status:** [PASS / FAIL — N issues found]

### Critical Issues (must fix before submission)
- [ ] Line [N]: Self-citation detected: \citep{blask2024} — author name matches paper author
- [ ] Line [N]: "In our previous work (Blask & Funk, 2023)" — explicit self-reference

### Warnings (review recommended)
- [ ] Line [N]: Acknowledgments section contains personal names
- [ ] Line [N]: GitHub URL in footnote may be identifiable

### Passed Checks
- [x] No author names in \author{} (anonymized version)
- [x] PDF metadata clean (pdfauthor field empty)
- [x] No institutional affiliations in text body
```

---

## Step 3: GENERATE Cover Letter

### Template

```markdown
# Cover Letter

**To:** [Editor-in-Chief / Program Chairs]
**From:** [Corresponding Author]
**Date:** [Date]
**Re:** Submission of "[Paper Title]" to [Venue]

---

Dear [Editor-in-Chief / Program Chairs / Editorial Board],

We are pleased to submit our manuscript entitled "[Paper Title]" for
consideration [for publication in / at] [Venue Name].

**Summary:** [2-3 sentences summarizing the paper's contribution. What problem
does it address? What does it find? Why does it matter?]

**Relevance to [Venue]:** [2-3 sentences explaining why this paper fits the
venue's scope, mission, or current call for papers. Reference specific tracks
or special issues if applicable.]

**Contribution:** This paper makes [N] contributions to the [field] literature:
(1) [contribution 1], (2) [contribution 2], [and (3) contribution 3].

**Method:** [1 sentence on methodology and key data/evidence.]

[**Special issue / track:** If applicable: "We submit this paper for
consideration in the [special issue name / track name] because [fit]."]

**Declarations:**
- This manuscript has not been published elsewhere and is not under
  consideration at another journal or conference.
- All authors have approved the manuscript and agree to its submission.
- [If applicable: Ethics approval was obtained from [institution] (Ref: [number]).]
- [If applicable: The authors declare no conflicts of interest.]

**Suggested Reviewers:** [See Step 4 — include if venue requests/allows this.]

We look forward to your consideration.

Sincerely,
[Corresponding Author Name]
[Affiliation]
[Email]
```

### Customization

- **Journal submission:** More formal, mention special issues, discuss fit with journal scope
- **Conference submission:** Shorter, mention track, discuss timeliness of contribution
- **R&R resubmission:** Replace with revision cover letter (different structure — summarize changes, reference review-engine output)

Save as `submission/cover_letter.md` (and optionally `submission/cover_letter.pdf`).

---

## Step 4: SUGGEST Reviewers

### Strategy

Identify potential reviewers from the paper's own reference list:

1. **Extract most-cited authors** from `references.bib`:
   - Count how many times each author appears across all references
   - Rank by frequency + citation count of their papers

2. **Filter for appropriateness:**
   - Remove co-authors of any paper author (conflict of interest)
   - Remove anyone cited only once (may not be relevant enough)
   - Remove authors from the same institution as paper authors

3. **Research each candidate:**
   - Current affiliation (via OpenAlex author search)
   - Recent publications (to confirm they're active in the field)
   - Email (from recent publications if available)

4. **Select 3-5 suggested reviewers** with justification

### Output

```markdown
## Suggested Reviewers

| # | Name | Affiliation | Expertise | Why Suitable | Papers Cited |
|---|------|-------------|-----------|-------------|-------------|
| 1 | [Name] | [University] | [Area] | [1-sentence] | [N] papers cited in our manuscript |
| 2 | [Name] | [University] | [Area] | [1-sentence] | [N] papers cited |
| 3 | [Name] | [University] | [Area] | [1-sentence] | [N] papers cited |

### Excluded (Conflicts of Interest)
- [Name] — co-author of [paper author] on [paper]
- [Name] — same institution as [paper author]
```

Save as `submission/suggested_reviewers.md`.

---

## Step 5: FORMATTING VALIDATION

### Automated Checks

Run these checks on `paper.tex` / `paper.pdf`:

| Check | Target | How |
|-------|--------|-----|
| Page count | Within venue limit | Count pages in PDF |
| Word count | Within venue limit (if applicable) | `texcount paper.tex` or approximate |
| Abstract length | Within venue limit (typically 150-250 words) | Count words in abstract |
| Reference style | Matches venue requirements | Check citation format (APA, IEEE, etc.) |
| Figure quality | Minimum 300 DPI, readable at print size | Check figure files |
| Table formatting | Consistent style, no vertical lines (booktabs) | Scan for `\hline` vs `\toprule` |
| Section numbering | Correct and complete | Parse `\section{}` hierarchy |
| Keywords | Present if required | Check for `\keywords{}` or equivalent |
| Running head | Present if required | Check `\pagestyle` configuration |
| Line numbers | Present if required for review | Check `\linenumbers` |

### Output

```markdown
## Formatting Validation Report

**Target venue:** [Venue]
**Status:** [PASS / N issues found]

| Check | Required | Actual | Status |
|-------|----------|--------|--------|
| Pages | max 17 | 15 | PASS |
| Abstract | 150-250 words | 218 words | PASS |
| References | APA 7 | APA 7 | PASS |
| Keywords | Required | 5 keywords present | PASS |
| Anonymized | Yes (double-blind) | Yes | PASS |
| Figure resolution | 300 DPI | fig1: 300, fig2: 150 | WARN — fig2 low res |
```

---

## Step 6: SUBMISSION CHECKLIST

### Final Checklist

Generate a comprehensive submission checklist tailored to the venue:

```markdown
## Submission Checklist — [Venue]

### Manuscript
- [ ] Paper compiles without errors (0 errors, 0 undefined references)
- [ ] Within page/word limit ([N] pages / [N] words — limit: [N])
- [ ] Abstract within word limit ([N] words — limit: [N])
- [ ] Abstract passes agent-readability check (domain named, RQ explicit, method + data source named, ≥1 concrete finding, no deferred meaning — see writing-engine Agent-Readability Rules)
- [ ] Keywords included (if required)
- [ ] All [CITE], [DATA], [TODO] placeholders resolved
- [ ] All figures referenced in text and present in figures/
- [ ] All tables referenced in text
- [ ] Bibliography complete (all \citep/\citet resolved)
- [ ] Consistent formatting throughout

### Anonymization (Double-Blind)
- [ ] Author names removed from manuscript
- [ ] Self-citations anonymized
- [ ] Institutional references removed
- [ ] Acknowledgments removed or anonymized
- [ ] PDF metadata cleaned (no author in properties)
- [ ] URLs/links to identifiable resources removed

### Submission Files
- [ ] Manuscript PDF (anonymized)
- [ ] Source files (.tex, .bib, .sty, figures/) if required
- [ ] Cover letter
- [ ] Supplementary materials (if any)
- [ ] Author information form (if required, separate from manuscript)
- [ ] Suggested reviewers list (if requested)
- [ ] Copyright/originality declaration (if required)
- [ ] Ethics statement (if applicable)

### Final Verification
- [ ] All co-authors have reviewed and approved the manuscript
- [ ] Not under review at another venue
- [ ] Submission deadline confirmed: [date]
- [ ] Submission portal accessed: [URL]
```

Save as `submission/submission_checklist.md`.

---

## Step 7: COMPILE Submission Package

### Output Directory Structure

```
submission/
├── paper_anonymous.tex     ← anonymized LaTeX source
├── paper_anonymous.pdf     ← anonymized compiled PDF
├── paper_deanonymized.tex  ← full version (for records)
├── cover_letter.md         ← cover letter
├── suggested_reviewers.md  ← reviewer suggestions
├── anonymization_report.md ← anonymization check results
├── formatting_report.md    ← formatting validation results
├── submission_checklist.md ← final checklist
└── self_citations.md       ← list of anonymized self-citations (for post-acceptance)
```

### Checkpoint

```
📦 SUBMISSION PACKAGE READY
━━━━━━━━━━━━━━━━━━━━━━━━━━
Target venue: [Venue Name]
Paper: "[Title]" — [N] pages, [N] words

Anonymization: [PASS / N issues to fix]
Formatting:    [PASS / N issues to fix]
Cover letter:  Generated
Reviewers:     [N] suggested

📁 Saved: submission/

✅ Checklist: [N]/[N] items completed
⚠️  Open items: [list any remaining items]

→ Review the checklist, then submit at [venue submission URL].
```

---

## Error Recovery

- **Venue not recognized:** Ask the user for submission guidelines URL, then extract requirements via WebFetch
- **Anonymization FAIL:** Present all issues. Do NOT auto-fix without user approval (some self-citations may be intentional)
- **Over page limit:** Report by how many pages. Suggest specific sections to shorten. Do NOT auto-cut
- **LaTeX compilation fails after anonymization:** Diff the anonymized version against the original to find the break

---

## Integration

| Scenario | Integration |
|----------|-------------|
| After Phase 6 | Natural next step — prepare for submission |
| After /review-paper + /respond-reviewers | Submit the revised version |
| R&R resubmission | Different cover letter template (revision letter) |
| Writing-engine | Shorten sections if over page limit |
| Verification-engine | Verify citations before submission |
