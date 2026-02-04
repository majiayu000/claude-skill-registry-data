---
name: homework-grading-workflow
description: >-
  Process scanned homework PDFs by extracting student names via vision, matching to roster,
  creating individual PDFs per student, and updating completion spreadsheets.
  Triggers: "process homework PDF", "organize by student", "create student files from scan",
  "update homework checklist", "who submitted", "sort assignments", "grade papers",
  "split PDF by student", "track completion", "missing assignments".
  Handles: batched scanned worksheets, handwritten name recognition, fuzzy roster matching,
  session resume for large batches (99-image limit), teacher grading automation.
---

# Homework Grading Workflow

Process scanned homework: extract names from pages using vision → match to roster → create individual PDFs → update completion spreadsheets.

**Core accuracy rules:** Read EVERY page individually (no batching) | Focus on Name field at TOP | Verify EACH PDF after creation

**Required inputs:** Scanned homework PDF + Student roster spreadsheet (with period sheets) + Completion spreadsheet (optional)

## Workflow Overview

```
Phase 0: Planning (BEFORE ANYTHING ELSE)
├── Count pages in PDF (fitz.open → len(doc))
├── CREATE tracking file with batch plan
├── Calculate sessions needed: ceil(total_pages / 99)
├── Display plan to user:
│   "150 pages = 2 sessions (99 + 51)"
└── User confirms before proceeding

Phase 1: Setup
├── Load roster from xlsx skill
├── Extract PDF pages as images
└── Tracking file already exists from Phase 0

Phase 2: Page Analysis (CRITICAL)
├── Check tracking file for current_session and start_page
├── Read EACH page individually (max 99 per session)
├── Find Name field at top
├── Match to roster (fuzzy matching)
├── Save to tracking file after EACH page
└── Stop at session limit, inform user to resume

Phase 3: User Verification
├── Display uncertain pages
├── User confirms/corrects names
└── All pages must be assigned

Phase 4: Create PDFs
├── Group pages by student
├── Create individual PDFs
└── Skip Unknown pages

Phase 5: Update Spreadsheet
├── Add assignment column
├── Mark submissions with X
└── Update Total formula

Phase 6: Verification
├── Check each PDF has correct pages
├── Cross-reference spreadsheet
└── Cleanup temp files
```

## Quick Reference

| Phase | Reference File | Script/Template |
|-------|---------------|-----------------|
| Decision Flow | [workflow-flowchart.md](reference/workflow-flowchart.md) | - |
| Page Analysis | [page-analysis.md](reference/page-analysis.md) | `scripts/extract_pages.py` |
| Status Tracking | [status-tracking.md](reference/status-tracking.md) | `scripts/update_status.py`, `templates/homework-grading-status.yaml` |
| PDF Creation | [pdf-creation.md](reference/pdf-creation.md) | `scripts/create_student_pdfs.py` |
| Spreadsheet | [spreadsheet-update.md](reference/spreadsheet-update.md) | - |
| Verification | [verification.md](reference/verification.md) | - |
| Troubleshooting | [troubleshooting.md](reference/troubleshooting.md) | - |
| Multi-Model Analysis | [clink-integration.md](reference/clink-integration.md) | PAL MCP `clink` tool |

## Required Skills Integration

**Always invoke these skills:**
```
Skill: document-skills:xlsx  # For spreadsheet operations
Skill: document-skills:pdf   # For PDF manipulation
```

## Critical Rules

**Phase 0 (BEFORE ANYTHING ELSE):**
- Create tracking file FIRST → Calculate batch plan (`ceil(pages/99)`) → Display plan → Get user confirmation

**Page Analysis:**
- ONE page per Read call (never batch) | Focus on "Name:" at TOP | Save to tracking file after EACH page | Stop at 99-image limit

**Verification:**
- Open and verify EACH student PDF | User MUST resolve uncertain pages | Cross-check spreadsheet X marks

## Red Flags → STOP

| If you see... | Do this instead |
|---------------|-----------------|
| No tracking file created | Create tracking file FIRST with batch plan |
| Batching pages | Read ONE page per Read call |
| Unknown pages being processed | User MUST confirm names first |
| Skipping PDF verification | Open and check EACH PDF |
| Not saving after each page | Save to tracking file after EVERY page |

**Confidence levels:** high (exact match) → proceed | medium (fuzzy match) → proceed with note | low/unknown → flag for user review. See [page-analysis.md](reference/page-analysis.md) for details. For difficult handwriting, use `clink` to get second opinion from another model - see [clink-integration.md](reference/clink-integration.md).

## Session Resume

99-image limit per session. Tracking file (`{output_folder}/homework-grading-status.yaml`) enables automatic resume. See [status-tracking.md](reference/status-tracking.md) for schema and resume workflow.

## Output Structure

```
{output_folder}/
├── homework-grading-status.yaml
├── Student Individual Files/{Student}.pdf
└── {completion_spreadsheet} (updated)
```

## Prerequisites

```bash
pip install PyMuPDF pandas openpyxl pyyaml filelock
```
