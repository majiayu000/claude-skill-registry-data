---
name: ai-disclosure-auditor
description: Use when AI contribution metadata must match the actual workflow, when model alias and dated identifiers need auditing, when verified and fabricated citation counts feed a release decision, or when a venue's AI disclosure statement needs evidence behind it.
---

# AI Disclosure Auditor

## When to use

Use this skill before release, after AI-assisted drafting, or during citation cleanup when the user needs disclosure metadata to match the actual workflow. Its citation counts come from apa-doi-verifier results, and its verdict feeds repo-release-integrity-check at release time. It is not for building an open-science release package or recording authorship contributions, those are open-science-release-packager and authorship-contribution-ledger.

## Inputs

- Booklet file or set of booklet files.
- Actual AI tools used.
- Human review state.
- Verified citation count.
- Fabricated citation count.
- Disclosure standard expected by the project or publisher.

## Workflow

1. Read the frontmatter before the body.
2. Confirm `ai_assisted` reflects actual AI use.
3. Confirm `ai_tools.name`, `vendor`, `model_alias`, `model_dated`, and `role`.
4. Classify contribution level using the project policy, not tone impression.
5. Confirm `human_review` and `human_review_date`.
6. Compare `verified_citations_count` with the reference list and in-text citation set when available.
7. Confirm `fabricated_citations_count` is zero for release material.
8. Check `disclosure_standard` against the current project policy.
9. Recommend frontmatter corrections and any body disclosure corrections.

## Output

Return:

- Disclosure verdict.
- Field-level audit table.
- Contribution level rationale.
- Human review evidence needed.
- Citation count reconciliation.
- Fabricated citation risk notes.
- Required release blockers.
- What to record at session end: the disclosure verdict per file, any fields still pending human confirmation, and a one-line summary for the release log.

## Verification

- Model alias and dated model fields are both present.
- Human review is not upgraded without evidence.
- Citation counts are not copied from older aggregate files without checking the current file.
- Release material with fabricated citations is blocked.
- Aggregate disclosure and per-file frontmatter are consistent.
- Before closing: every release blocker is documented and the verified disclosure output is ready to hand to open-science-release-packager.

## Safety

Do not expose prompts, logs, private notes, credentials, unpublished clinical data, or reviewer identities unless the user explicitly supplies publication-safe excerpts. Keep the audit at metadata and disclosure level when private context is not needed.

## Example prompt

"Audit the AI disclosure fields for all released booklets and tell me which files block v1.1.0."

Expected smoke output:

- A file-by-file table with pass, partial, or fail.
- A release-blocker list.
- A count summary for contribution levels and human review state.

## Türkçe kullanım notu

Bu beceri, yapay zekâ katkı beyanının gerçek iş akışıyla örtüşüp örtüşmediğini alan alan denetler. Model kimlikleri, insan incelemesi durumu ve atıf sayıları kanıtla karşılaştırılır, uydurma atıf içeren içerik yayına kapatılır. Atıf sayıları apa-doi-verifier doğrulamasından gelir, sonuç yayın bütünlüğü kontrolüne girdi olur. Açık bilim paketi için open-science-release-packager'a, yazarlık katkı kaydı için authorship-contribution-ledger'a devredilir. Oturum sonunda denetim kararı ve bekleyen alanlar kayda geçirilir.
