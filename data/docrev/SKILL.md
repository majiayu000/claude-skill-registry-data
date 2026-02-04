---
name: docrev
description: "Document revision workflow tool (CLI: `rev`). Use when working with Word documents containing reviewer comments, importing track changes to markdown, replying to reviewer comments, building PDF/DOCX outputs, generating response letters, validating citations/DOIs, or any document revision task."
---

# docrev - Document Revision Tool

`rev` is a CLI tool for document workflows with Word ↔ Markdown round-trips.

Works for any document that goes through Word-based review: scientific papers, contracts, reports, proposals, manuals.

## Content and Layout, Separated

In Markdown, you focus on content. Write text, add citations with `[@key]`, insert equations with `$...$`, reference figures with `@fig:label`. No fiddling with fonts or styles.

Layout is controlled in `rev.yaml`:

```yaml
title: "My Document"
output:
  docx:
    reference-doc: template.docx
```

Change the template, rebuild, and every document gets the new formatting.

## Core Workflow

### 1. Create or import a project

```bash
rev new my-document          # Start from scratch
rev import manuscript.docx   # Start from existing Word doc
```

### 2. Build and share

```bash
rev build docx               # Generate Word document
```

Send to reviewers. They add comments and track changes in Word.

### 3. Import feedback

```bash
rev sync reviewed.docx       # Updates markdown with annotations
rev sync                     # Auto-detect most recent .docx
```

### 4. View and address comments

```bash
rev status                   # Project overview
rev todo                     # List all pending comments
rev next                     # Show next pending comment
rev comments methods.md      # List all comments with context
```

### 5. Reply to reviewer comments

**Always use the non-interactive reply mode:**

```bash
rev reply methods.md -n 1 -m "Added clarification about sampling methodology"
rev reply results.md -n 3 -m "Updated figure to include 95% CI"
```

Replies appear as: `{>>Reviewer: Original<<} {>>User: Reply<<}`

### 6. Resolve addressed comments

```bash
rev resolve methods.md -n 1  # Mark comment #1 as resolved
```

### 7. Rebuild with comment threads

```bash
rev build docx --dual        # Produces clean + annotated versions
```

- `paper.docx` — clean, for submission
- `paper_comments.docx` — includes comment threads as Word comments

### 8. Archive reviewer files

```bash
rev archive                  # Move reviewer files to archive/
```

### 9. Generate response letter

```bash
rev response                 # Generate point-by-point response letter
```

## Annotation Syntax (CriticMarkup)

- `{++inserted text++}` - Additions
- `{--deleted text--}` - Deletions
- `{~~old~>new~~}` - Substitutions
- `{>>Author: comment<<}` - Comments
- `{>>Author: comment [RESOLVED]<<}` - Resolved comment

## Quick Commands

| Task | Command |
|------|---------|
| Create project | `rev new my-project` |
| Create LaTeX project | `rev new my-project --template latex` |
| Import Word doc | `rev import manuscript.docx` |
| Sync Word feedback | `rev sync reviewed.docx` |
| Sync PDF comments | `rev sync annotated.pdf` |
| Extract PDF comments | `rev pdf-comments annotated.pdf` |
| Extract with highlighted text | `rev pdf-comments file.pdf --with-text` |
| Append PDF comments | `rev pdf-comments annotated.pdf --append methods.md` |
| Project status | `rev status` |
| Next pending | `rev next` |
| List pending | `rev todo` |
| Filter by author | `rev comments file.md --author "Reviewer 2"` |
| Reply to all pending | `rev reply file.md --all -m "Addressed"` |
| Accept all changes | `rev accept file.md -a` |
| Build Word | `rev build docx` |
| Build PDF | `rev build pdf` |
| Build clean + annotated Word | `rev build docx --dual` |
| Build clean + annotated PDF | `rev build pdf --dual` |
| Show contributors | `rev contributors` |
| Lookup ORCID | `rev orcid 0000-0002-1825-0097` |
| Archive reviewer files | `rev archive` |
| Word count per section | `rev word-count` |
| Project dashboard | `rev stats` |
| Search all sections | `rev search "query"` |
| Pre-submission check | `rev check` |
| Validate citations | `rev citations` |
| Check grammar/style | `rev grammar` |
| Check spelling | `rev spelling` |
| Open PDF preview | `rev preview pdf` |
| Auto-rebuild on changes | `rev watch` |
| Check for updates | `rev upgrade --check` |

## DOI Management

```bash
rev doi check references.bib         # Validate DOIs
rev doi lookup references.bib        # Find missing DOIs
rev doi add 10.1234/example          # Add citation from DOI
```

## Validation

```bash
rev validate --journal nature        # Check journal requirements
rev validate --list                  # List 21 available journal profiles
rev lint                             # Check broken refs, missing citations
```

## Cross-References

Use in markdown files:
- `@fig:label` - Figure reference (becomes "Figure 1" in Word)
- `@tbl:label` - Table reference
- `@eq:label` - Equation reference
- `{#fig:label}` - Anchor for figures

## Template Variables

Available in section files (processed during build):
- `{{date}}` - Current date (YYYY-MM-DD)
- `{{date:MMMM D, YYYY}}` - Custom format
- `{{title}}` - Document title
- `{{author}}` - First author
- `{{word_count}}` - Total word count

## Project Structure

```
my-document/
├── rev.yaml           # Project config
├── introduction.md    # Section files with annotations
├── methods.md
├── results.md
├── discussion.md
├── references.bib     # Bibliography
├── figures/           # Images
└── paper.docx         # Built output
```

## PDF Comment Workflow

For reviewers who annotate PDFs instead of Word documents:

### 1. Extract comments from PDF

```bash
rev pdf-comments annotated.pdf              # Display all comments
rev pdf-comments annotated.pdf --by-author  # Group by reviewer
rev pdf-comments annotated.pdf --json       # Output as JSON
```

### 2. Import into markdown

```bash
rev sync annotated.pdf                      # Auto-import to sections
rev pdf-comments annotated.pdf --append methods.md  # Append to specific file
```

### 3. Build PDF with margin notes

```bash
rev build pdf --dual
```

Produces:
- `paper.pdf` — clean version for submission
- `paper_comments.pdf` — comments rendered as LaTeX margin notes

**Supported PDF Annotations:**
- Sticky notes, text boxes, highlights, underlines, strikethrough, squiggly

## When Helping Users

1. **Setup**: Ensure `rev config user "Name"` is set for replies
2. **Sync phase**: Run `rev sync` to get feedback (works with both Word and PDF)
3. **Review phase**: Use `rev todo` and `rev next` to navigate comments, `rev reply` to respond
4. **Accept phase**: Use `rev accept -a` or `rev review` to handle track changes
5. **Build phase**: Run `rev build docx --dual` or `rev build pdf --dual` for annotated versions
6. **Archive phase**: Run `rev archive` to move reviewer files
7. **Validation phase**: Run `rev check` before submission
8. **Response letter**: Use `rev response` to generate point-by-point responses

## Critical: Ask Questions When Unsure

When addressing reviewer comments or editing documents:

- **Never guess methods or numbers** - If a comment asks for clarification about methodology, sample sizes, statistical parameters, dates, or any quantitative information, ASK the user rather than inventing values
- **Placeholders are acceptable** - Use `[???]` or `[TODO: specify X]` when information is missing rather than fabricating data
- **Search online for references** - When comments request citations, use web search to find appropriate references rather than guessing
- **Clarify ambiguous requests** - If a reviewer comment could be interpreted multiple ways, ask the user which interpretation they prefer
- **Verify existing values** - When editing numbers that already exist in the document, confirm changes with the user if there's any doubt

Example scenarios requiring user input:
- "Add a reference for this claim" → Search online OR ask user for specific citation
- "Clarify the sample size" → Ask user for the correct number
- "Specify the statistical test used" → Ask user which test was actually used
- "Add the date of data collection" → Ask user for the actual date

For complete command reference, see [REFERENCE.md](REFERENCE.md).
