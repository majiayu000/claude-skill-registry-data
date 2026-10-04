---
name: anti-ai-trace-revision
description: Use when a draft in Turkish, English, or both reads as AI-generated and needs revision that removes machine writing patterns and translation calques while preserving meaning, citations, statistics, and the author's voice.
---

# Anti AI Trace Revision

## When to use

Use this skill when a manuscript, revision letter, website text, or report sounds machine-written and the goal is to restore a human author's voice without changing what the text claims. Typical moments: a supervisor or reviewer says the text feels AI-generated, a bilingual document reads as translated rather than written, or an AI-assisted draft is approaching submission and needs a final pass. For reviewer-response structure use rebuttal-traceability-matrix first, then bring the prose here. It is not for verifying whether citations in the revised text are real and correctly formatted, that is apa-doi-verifier.

## Inputs

- The draft, with its language or languages identified.
- The register: empathic essay, technical guide, scientific manuscript, or public-facing copy. The correct fix differs by register, and a move that is warm in an essay is a machine tell in a methods section.
- The frozen list: citations, DOIs, statistics, direct quotations, names, identifiers, code blocks, and legal wording that must survive byte for byte.
- A personal voice sample or style guide, when the author has one.

## Workflow

1. Read the whole text once without editing and write a tell inventory with line references. Diagnosis precedes repair.
2. Work the structural layer first: count-announcing headings and mechanical three-part parallels come out. Thin contrast tails of the "not X but Y" kind to at most one per document. Vary sentence length until short statements interrupt the uniform mid-length rhythm, and delete arc cliches such as "from first principles to peer review".
3. Then work the naturalness layer, sentence by sentence, asking whether a person writing in this language would put it this way. Replace metaphors that do not survive translation with native concepts. Replace borrowed jargon when the language already has a working term. Rebuild stiff calque constructions from scratch instead of swapping single words inside them.
4. In English academic prose keep em dashes rare rather than forbidden, and cut decorative adjective stacks such as rigorous, robust, comprehensive, seamless. Forcing zero em dashes into a journal manuscript creates a new artificial signature.
5. Keep the two layers as separate passes. A vocabulary pass cannot repair architecture, and an architecture pass leaves calques standing.
6. After rewriting, compare the frozen list against the original. Citations, numbers, quotations, and code must match exactly.
7. Hand the result to a reader or session that did not produce the rewrite, with the single instruction to hunt for surviving tells. The writer of a pass is the least reliable judge of it.

## Output

Return:

- The revised text.
- The tell inventory, with one before and after example per removed pattern.
- A frozen-list check confirming citations, statistics, quotations, and identifiers are unchanged.
- Residual risks that need a human read-aloud or a second human reader.
- What to record at session end: the tell inventory, the pattern counts before and after, and a note that ai-disclosure-auditor still governs the disclosure obligation regardless of how natural the revised prose reads.

## Verification

- Count-announcing headings in the revised text: zero, unless the user chose to keep a numbered structure.
- Sentences repeated verbatim across sections or sibling documents: zero.
- Contrast tails of the "not X but Y" kind: at most one per document.
- Every frozen item byte-identical to the original.
- Turkish output carries full diacritics and uses em dashes and semicolons only where they serve the sentence rather than as a reflex, since forcing either to zero leaves its own artificial signature. APA exceptions for multi-source parentheses and bibliographic page ranges stay intact.
- A reviewer who did not write the revision confirms the rewrite introduced no new tells.
- Before closing: if any citation, statistic, or identifier was touched during revision, hand the frozen list to apa-doi-verifier before the document is submitted; the revision and the citation check are separate passes.

## Safety

Never let de-patterning touch quotations, citations, statistics, or legal wording. Do not use this skill to disguise unreviewed AI text as human work. Where a journal, funder, or institution requires AI-use disclosure, the disclosure obligation stands regardless of how natural the prose reads, and ai-disclosure-auditor remains the place to check it.

## Example prompt

"Bu makale revizyonu yapay zekâ yazmış gibi okunuyor, Türkçesini ve İngilizcesini doğallaştır ama kaynakçaya dokunma."

Expected smoke output:

- A tell inventory listing structural and naturalness findings with line references.
- A revised bilingual draft with the reference list untouched.
- A frozen-list verification note and a short residual-risk list.

## Türkçe kullanım notu

Bu beceri, yapay zekâ yazmış gibi okunan bir metni anlamı ve atıfları koruyarak insan sesine döndürür. Düzeltme iki ayrı geçişle ilerler. Önce retorik iskelet ele alınır, başlıklar ve cümle ritmi makine imzasından arındırılır. Sonra her cümle doğallık testinden geçer, çeviri kokan kuruluşlar ve eğreti metaforlar yeniden yazılır. Dondurulmuş liste, yani atıflar, sayılar, alıntılar ve kod, yeniden yazımdan sonra orijinaliyle birebir karşılaştırılır. Beceri beyan yükümlülüğünü gizlemek için kullanılmaz, amaç yazım kalitesi ve yazar sesidir. Türkçe çıktıda tam diakritik korunur, tire ve noktalı virgül refleks olarak değil ancak cümleye hizmet ettiği yerde kalır.
