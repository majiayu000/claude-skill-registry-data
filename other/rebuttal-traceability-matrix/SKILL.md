---
name: rebuttal-traceability-matrix
description: Use when reviewer comments arrive and each one needs a tracked decision, when a revise and resubmit letter must map every comment to a manuscript change, or when contradictory reviewer demands need evidence-based, editor-facing framing.
---

# Rebuttal Traceability Matrix

## When to use

Use this skill after peer review, revise and resubmit, editorial triage, grant review, or supervisor feedback when comments must be answered systematically. Once the matrix stands, anti-ai-trace-revision keeps the response prose in the author's voice. It is not for handling confidential peer review material that must not be disclosed externally, that is peer-review-confidentiality-protocol.

## Inputs

- Reviewer comments.
- Editor letter, if available.
- Manuscript section map.
- Constraints, such as word limit, journal tone, or non-negotiable methodological boundaries.
- Revised manuscript excerpts, if already drafted.

## Workflow

1. Split comments into atomic claims.
2. Label each claim as accepted, partially accepted, rejected with rationale, clarification only, or outside scope.
3. Map each claim to manuscript sections, tables, figures, appendices, or cover letter only.
4. Identify comments that require new analysis, citation support, transparency language, or limitation framing.
5. Draft a traceability matrix.
6. Draft response text with a respectful, non-defensive tone.
7. Flag contradictions between reviewers and suggest editor-facing framing.
8. Before sharing the response letter externally, confirm with peer-review-confidentiality-protocol that no confidential reviewer identities or editorial metadata are exposed.

## Output

Return:

- Reviewer comment matrix.
- Decision category per comment.
- Manuscript change map.
- Required evidence or citation checks.
- Editor response summary.
- Reviewer-by-reviewer response draft.
- Residual risks.
- What to record at session end: the completed matrix file, any reviewer comments still without a manuscript location, and which open evidence needs require a new analysis pass.

## Verification

- Every reviewer comment is represented once.
- Partial acceptance states exactly what changed and what did not.
- Rejections are evidence-based and respectful.
- Manuscript locations are specific enough for a coauthor to verify.
- No unsupported claim is added to satisfy a reviewer.
- Before closing: every open evidence need is listed explicitly, the response letter has been checked against peer-review-confidentiality-protocol, and the matrix is saved where a coauthor can verify it independently.

## Safety

Do not invent manuscript changes. Do not claim analyses were run unless outputs are supplied or verified. Preserve reviewer anonymity and remove private editorial metadata before sharing externally.

## Example prompt

"Turn these Reviewer 1 and Reviewer 2 comments into a traceability matrix and draft a response letter outline."

Expected smoke output:

- A matrix with comment ID, reviewer, issue, decision, manuscript location, action, and response draft.
- A separate list of unresolved evidence needs.

## Türkçe kullanım notu

Bu beceri, hakem yorumlarını tek tek karara bağlar ve her kararı el yazmasındaki değişikliğe eşler. Kabul, kısmi kabul ve gerekçeli ret ayrımı netleşir, hakemler arası çelişkiler editöre dönük çerçeveyle işaretlenir. Hakemi memnun etmek için desteksiz iddia eklenmez, yapılmamış analiz yapılmış gibi yazılmaz. Matris kurulduktan sonra yanıt metninin sesi anti-ai-trace-revision ile korunur. Yanıt mektubu dışarı çıkmadan önce gizli hakem kimliği veya editoryal meta veri taşımadığı peer-review-confidentiality-protocol ile teyit edilir. Oturum sonunda matris dosyası ve açık kanıt ihtiyaçları kayda geçirilir.
