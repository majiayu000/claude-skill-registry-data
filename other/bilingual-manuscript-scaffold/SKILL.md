---
name: bilingual-manuscript-scaffold
description: Use when authoring a new manuscript, thesis chapter, or abstract from scratch in Turkish and English in parallel — building the claim skeleton first, then drafting Turkish and re-authoring English — not for auditing parity between existing versions.
---

# Bilingual Manuscript Scaffold

## When to use

Use this skill when a manuscript needs to be written in Turkish and English in parallel and the risk is drift: two versions that quietly stop claiming the same things. It also applies when only the skeleton is needed, an IMRAD outline with word budgets, before any prose exists. For voice repair on finished prose use anti-ai-trace-revision, and for reference verification use apa-doi-verifier. It is not for auditing whether a concept translates cleanly across cultural contexts; that is multilingual-concept-validity-audit.

## Inputs

- Research question, hypotheses, and the main findings or planned analyses.
- Target venue and its structural rules, when known.
- Which language the author drafts in first. Turkish first is the default this scaffold assumes.
- Word limits per section, when the venue sets them.

## Workflow

1. Build the claim skeleton before either language: research question, each hypothesis or proposition, the evidence that supports it, and the limitation that bounds it, as a numbered list.
2. Lay the IMRAD scaffold over the skeleton and assign each claim to a section, with a word budget per section.
3. Draft the Turkish version first, in the author's register, section by section against the skeleton.
4. Write the English version from the skeleton and the Turkish section outlines. Re-author each section as English academic prose. Sentence-by-sentence translation produces calques and is the failure mode this workflow exists to prevent.
5. Keep one reference list. Both versions cite the same sources, and the DOI sets must match exactly.
6. Run the parity check after each section: same claim order, same evidence per claim, same heading count, same DOI set.
7. When a section's prose fights the author's voice, route it through anti-ai-trace-revision before moving on.
8. When a key term carries different theoretical weight in Turkish and English academic traditions, hand the concept list to multilingual-concept-validity-audit before the parity check closes.

## Output

Return:

- The claim skeleton.
- The IMRAD scaffold with word budgets.
- Drafted sections in both languages, marked draft until parity passes.
- A parity report per section.
- What to record at session end: the latest claim skeleton, the parity report for each completed section, any concept terms flagged for multilingual-concept-validity-audit, and a one-line note for the AI-use disclosure.

## Verification

- The DOI sets of the two versions are identical.
- Heading counts match between the versions.
- Each claim appears in both languages with the same evidence attached.
- No section was produced by sentence-level translation, checked by reading the English aloud for calque rhythm.
- Word budgets respected or the overrun is flagged with a cut plan.
- Before closing: every concept term flagged during parity has either been cleared or handed to multilingual-concept-validity-audit, and the parity report for each section is saved where the next session can find it.

## Safety

Meaning must not drift between languages. When the two versions disagree, stop and resolve the claim skeleton first instead of patching one side. Never invent content to fill a gap in one language, and never alter statistics or quotations during re-authoring.

## Example prompt

"Aile içi dijital çatışma üzerine makalemi Türkçe yazdım, İngilizce sürümünü iskeletten yeniden kurmama yardım et."

Expected smoke output:

- A claim skeleton extracted from the Turkish draft.
- An English section plan built from the skeleton, with word budgets.
- The first re-authored section and its parity report.

## Türkçe kullanım notu

Bu beceri, iki dilde yaşayacak bir el yazmasını tek iskeletten kurar. Önce iddia iskeleti çıkarılır, sonra Türkçe taslak yazılır, İngilizce sürüm cümle çevirisiyle değil iskeletten yeniden yazılır. Her bölümden sonra eşlik kontrolü yapılır. Başlık sayısı, iddia sırası ve DOI kümesi iki sürümde birebir örtüşmek zorundadır. İki dil arasında anlam kayarsa önce iskelet düzeltilir. Kavram geçerliliği kültürler arasında denetlenmek istendiğinde multilingual-concept-validity-audit becerisi devreye girer.
