---
name: resume-proof
description: Evidence-first governance and QA for AI-assisted resumes, covering JD matching, claim tracing, mandatory full-text approval, bilingual tailoring, formatted output coordination, PDF checks, and versioned delivery. Use when a user asks to optimize a resume for a job description, create Chinese or English variants, review resume content or layout, maintain an evidence-backed resume library, or package final resume files. Always show the complete text draft and obtain explicit approval before generating formatted files.
---

# ResumeProof

Build job-specific resumes from verified evidence while keeping claims truthful, readable, and easy to audit. Treat ResumeProof as the governance layer around the host agent's document-generation tools, not as a bundled resume-template engine.

## Non-negotiable gate

Never generate or overwrite HTML, DOCX, or PDF output before the user explicitly approves the complete text draft. Approval of an outline, one section, or a previous version does not count.

## Workflow

1. Discover the user's sources: base resume, target JD, evidence files, preferred language, template, and output location.
2. Read `references/configuration.md` when setting up a new workspace or resolving file locations.
3. Read `references/workflow.md` before tailoring or generating a resume.
4. Create the application workspace with `python scripts/resume_proof.py new`. Record supported claims in `evidence-ledger.json`.
5. Compare the resume with the JD. Prioritize role-critical capabilities, measurable outcomes, and relevant keywords without copying the JD mechanically.
6. Draft the full resume in plain text. Keep full-time roles and internships separate when mixing them could imply instability.
7. Present the complete text draft and wait for explicit approval.
8. Only after approval, record the approved-text hash with `python scripts/resume_proof.py approve`, then use available document tools to generate the requested files without changing the approved meaning.
9. Run factual, language, pagination, extraction, and visual QA. Use the CLI's `validate` and `qa` commands to record results.
10. Deliver with the CLI's `deliver` command. It must block delivery when approval is missing, approved text has changed, QA is incomplete, or a destination collision lacks explicit `--force` authorization.

## Writing rules

- Keep every claim traceable to a supplied source or explicit user confirmation.
- Do not invent metrics, tools, ownership, dates, employers, clients, markets, or outcomes.
- Prefer specific actions and results over generic capability claims.
- State partial ownership accurately with verbs such as supported, coordinated, analyzed, or contributed.
- Use natural language appropriate to the resume's language. If a humanizer skill is available, apply it only after factual content is settled.
- Keep the final resume within the user's requested length; default to no more than two A4 pages.
- Optimize for human scanning first and ATS extraction second. Avoid dense columns, decorative charts, and text embedded in images.

## Output contract

For each application, retain:

- `text-review.md`: the exact draft approved by the user
- editable source, usually HTML or DOCX
- final PDF
- `evidence-ledger.json`: claim-to-source mappings
- `manifest.json` based on `assets/manifest-template.json`
- validation notes or command output

Use `scripts/resume_proof.py` as the single cross-platform entry point. Do not bypass its approval and delivery checks with direct copies unless the user explicitly requests a manual recovery.

## QA checklist

- All dates, names, metrics, and tools match approved evidence.
- No placeholders, comments, hidden text, or stale content remain.
- Contact details and links are correct.
- The PDF text can be extracted in a sensible reading order.
- Required keywords appear naturally; forbidden or legacy terms are absent.
- Page count meets the requested limit.
- Page breaks, spacing, bullets, and alignment are visually clean.
- Delivered files match the approved files by checksum.
