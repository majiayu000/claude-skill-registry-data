---
name: peer-review-confidentiality-protocol
description: Use when serving as a peer reviewer and deciding whether and how AI may assist, when a manuscript under review must never be pasted into an external tool, or when a confidentiality-preserving review and disclosure are needed.
---

# Peer Review Confidentiality Protocol

## When to use

Use this skill when serving as a peer reviewer and the question is whether AI assistance is permissible, how to structure the review without breaching confidentiality, or how to produce an AI-use disclosure alongside the submitted report. It applies at any point in the reviewing process: checking journal policy before starting, organising the reviewer's own notes into a structured draft, generating methodological questions from those notes alone, and composing the final reviewer-signed disclosure. It is not for summarising the manuscript text directly in an external tool when journal policy prohibits it, and it never substitutes the reviewer's scientific judgment for the model's output.

## Inputs

- The journal's AI-use and peer-review confidentiality policy, or a description of what the policy says.
- The reviewer's own notes on the manuscript, written before invoking the skill.
- The journal's structured review form, if one exists.
- Any methodological or reporting checklists the journal specifies.
- Editor-specific concerns or decision categories the reviewer must address.

## Workflow

1. Check the journal policy first: determine whether the policy prohibits pasting manuscript text into any third-party tool, requires disclosure, or is silent, and record that determination before proceeding.
2. If the policy prohibits sharing the manuscript text, work exclusively from the reviewer's own notes; the manuscript itself never enters the tool.
3. Classify the reviewer's notes into four categories: strengths, major concerns, minor corrections, and a note to the editor.
4. Draft the review skeleton with those categories, drawing only on the reviewer's observations, not on model inference about the manuscript's content.
5. Generate a methodological question list from the reviewer's notes, flagging gaps in design, analysis, reporting, or ethics transparency.
6. Draft the editor note if the reviewer needs to flag a concern outside the public review.
7. Compose the AI-use disclosure statement, naming the stage at which AI assisted, the model used, the contribution level, and the fact that the reviewer exercised final judgment.
8. Return the full package to the reviewer for a final human read before submission. Hand off any residual AI-disclosure questions to ai-disclosure-auditor, ethics board implications to ethics-irb-ai-protocol, anonymisation needs to sensitive-data-anonymization-gate, and the submitted report's traceability to rebuttal-traceability-matrix.

## Output

Return:

- A confidentiality compliance check recording the journal policy and the working mode it requires.
- A structured review skeleton with strengths, major concerns, minor corrections, and editor note.
- A methodological question list drawn from the reviewer's notes.
- A draft AI-use disclosure statement ready for inclusion with the submission.
- What to record at session end: the working mode used (notes-only or policy-permitted full-text), the output file path, any decisions left to the reviewer's judgment, and the handoff to ai-disclosure-auditor for final disclosure parity.

## Verification

- The confidentiality check was performed before any manuscript text was considered for input.
- If notes-only mode was applied, no manuscript passage appears in any model input or output.
- Every major concern and strength is attributed to the reviewer's own notes, not to model inference.
- The AI-use disclosure names the stage, model, contribution level, and human review step.
- Before closing: the reviewer has read and signed the report as their own scientific judgment, and the disclosure accurately represents what the model contributed and what the human decided.

## Safety

Peer review handles unpublished ideas and data that belong to the authors until publication. Pasting a confidential manuscript into an external AI tool without explicit journal permission is a breach of that trust, regardless of what the model does with the text. This skill therefore defaults to notes-only mode and escalates to ai-disclosure-auditor whenever disclosure adequacy is uncertain. The reviewer's scientific decision — accept, major revision, reject — is never delegated to the model. If the manuscript contains participant-level data, clinical material, or identifying information, sensitive-data-anonymization-gate must run before any text enters a tool.

## Example prompt

"Hakem olarak kendi notlarımı kullanarak güvenli bir değerlendirme raporu hazırlamak istiyorum. Dergi politikasını kontrol ettim, makale metnini araca veremiyorum. Notlarımdan yapı, yöntemsel sorular ve editöre not taslağı oluştur, beyan cümlesi de ekle."

Expected smoke output:

- A confidentiality check confirming notes-only mode based on the reported journal policy.
- A review skeleton structured as strengths, major concerns, minor corrections, and editor note, sourced entirely from the reviewer's notes.
- A methodological question list flagging gaps the reviewer identified.
- A draft AI-use disclosure sentence naming the structuring stage, the model, and the reviewer's retained judgment.

## Türkçe kullanım notu

Bu beceri, hakemlik sürecinde yapay zekânın neyi yapıp neyi yapamayacağını belirler ve bu sınırı gizlilik yükümlülüğünü çiğnemeden tutar. Başlangıç noktası her zaman derginin politikasıdır: metin paylaşıma kapalıysa beceri yalnızca hakemin kendi notlarıyla çalışır, makale metnini araca vermez. Notlar güçlü yönler, ana kaygılar, küçük düzeltmeler ve editöre özel not olarak sınıflandırılır. Bilimsel karar hakem olarak sizindir. Rapor tamamlanmadan önce yapay zekâ katkı beyanı hazırlanır ve ai-disclosure-auditor'a devredilir. Etik kurul gerektiren bir durum fark edilirse ethics-irb-ai-protocol devreye girer. Kimlik içeren ya da klinik veri söz konusuysa sensitive-data-anonymization-gate önce çalışır. Rapora giren her karar sizin bilimsel hükmünüzdür, yapay zekânın değil.
