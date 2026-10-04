---
name: latex-pdf-final-review
description: Review final LaTeX thesis or paper submissions by compiling, extracting PDF text, rendering key pages, checking references, terminology, metrics, figure/table consistency, layout warnings, and manual-confirmation gaps. Use before submission, advisor review, blind review, or defense delivery.
---

# LaTeX PDF Final Review

Use this skill when the deliverable is the compiled PDF, not only the `.tex` source.

## Workflow

1. Identify the root `.tex`, output PDF, bibliography, figure directory, and current commit.
2. Compile using the project’s normal command.
3. Inspect logs for:
   - errors;
   - undefined references;
   - missing citations;
   - severe overfull/underfull boxes;
   - missing figures or fonts.
4. Extract PDF text and run targeted searches for old terms, placeholder text, stale metrics, and inconsistent model names.
5. Render key pages:
   - cover and abstract;
   - table of contents;
   - architecture/overview figures;
   - main experiment figures and tables;
   - conclusion and limitations.
6. Record findings in a review report and separate automatic checks from human-only confirmations.

## Guardrails

- Do not mark check-rate, advisor approval, signature pages, or institutional submission status as passed without user-provided evidence.
- Do not trust source inspection when the final PDF shows a layout problem.
- Do not suppress LaTeX warnings without understanding whether they affect the delivered PDF.
- Keep review artifacts out of the source tree unless the project already has a temporary output convention.

## Useful Resources

- Read `references/final-review-checklist.html` for the compact checklist.
- Use `assets/pdf-review-report.html` for review reports.
