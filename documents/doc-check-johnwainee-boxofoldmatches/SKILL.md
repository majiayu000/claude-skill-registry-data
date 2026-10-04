---
name: doc-check
description: Run the deterministic markdown conformance workflow on a document or directory and explain the findings. Use when the user asks to validate/check a doc or says /doc-check.
---

# /doc-check — run document conformance

1. Run it:
   - Governance baseline (with known-findings baseline):
     `make doc-check`
   - A specific file or directory:
     `uv run python -m koa.workflows.doc_check <path>`
     (add `--baseline architecture/evidence/doc-check-known-findings.json` when
     checking `architecture/governance/`)
2. Explain each failing finding in plain language and what would fix it. The checks:
   `title_present` (level-1 heading first), `status_present` (`**Status:**` marker),
   `date_present` (`**Date:**`/`**Prepared:**`), `heading_step` (no level jumps),
   `links_resolve` (relative links exist).
3. Rules:
   - Documents under `architecture/governance/` are committed **verbatim** — never
     edit them to silence findings. If a finding is accepted as-is, add it to
     `architecture/evidence/doc-check-known-findings.json` with a one-line rationale
     in the commit message.
   - For any other document, prefer fixing the document.
4. Remember this workflow is a placeholder (ADR-KOA-DEV-001), not Kūkulu — don't grow
   it new check types without an ADR.
