---
name: arabic-dialect-lord
description: Lord skill for Arabic dialect-aware AI coding governance. Bridges Modern Standard Arabic (MSA) with Gulf, Egyptian, and Levantine dialects to deliver contextually-appropriate Arabic output for MENA developers.
triggers:
  - arabic dialect lord
  - arabic dialect
  - لهجة
  - خليجي
  - مصري
  - شامي
  - مغربي
  - عربي
  - arabic
  - mena
  - localization
  - تعريب
  - ترجمة عربية
personas:
  - UX
  - DOC
  - PRODUCT
  - DEVX
  - FREELANCE
tech_stack: []
lord: true

---

# Arabic Dialect Lord

[OBJ] Arabic dialect-aware governance for AI coding assistants targeting MENA developers.

## Problem

50% AI adoption in MENA, yet 28% of users who tried Arabic responses switched back to English permanently. MSA-only platforms score 24 percentage points lower on Gulf/Egyptian dialect intent detection. Code-switched Gulf/English drops to 51% accuracy on MSA-only models. This is a competitive gap no AI governance tool addresses.

## Rules

1. [REQ] **Dialect detection first.** Before generating Arabic output, detect target dialect from: explicit user request, project locale (`ar-SA`, `ar-EG`, `ar-AE`, `ar-PS`, `ar-MA`), or user profile. Default to MSA only when no signal.
2. [REQ] **Dialect registry.** Support five dialect families:
   - `gulf` (ar-SA, ar-AE, ar-QA, ar-BH, ar-KW, ar-OM) — خليجي
   - `egyptian` (ar-EG) — مصري
   - `levantine` (ar-PS, ar-JO, ar-LB, ar-SY) — شامي
   - `maghrebi` (ar-MA, ar-DZ, ar-TN) — مغربي
   - `msa` (ar) — فصحى
3. [REQ] **No dialect mixing.** A single response must stay in ONE dialect. Mixing Gulf vocabulary with Egyptian grammar = reject. Flag as `DIALECT_MIX`.
4. [REQ] **Code-switching rules.** When Arabic+English code-switching is detected (common in MENA dev workflows), preserve technical terms in English (e.g., "API", "deploy", "commit") and wrap in Arabic grammar. Never translate established technical terms to invented Arabic equivalents.
5. [REQ] **Cultural context.** Gulf dialect expects formal business register for client-facing content; Egyptian allows casual register for internal docs. Match register to audience.
6. [REQ] **RTL layout.** Any UI text in Arabic must use RTL (`dir="rtl"`). Mixed Arabic/English UI must use `dir="auto"` per element. Never force LTR on Arabic content.
7. [REQ] **Number formatting.** Arabic-Indic digits (٠١٢٣) only when locale explicitly requests; default to Western Arabic numerals (0123) for technical/code content. Currency in SAR/AED uses Western numerals per regional convention.
8. [REQ] **Date/time.** Use Hijri calendar only when explicitly requested (`calendar=islamic`); default Gregorian with Arabic month names for dialect output.
9. [REQ] **Tone calibration.** Gulf: respectful, indirect, honorific (حضرتك/فضلتك). Egyptian: direct, warm, colloquial (يا باشا/بعد إذنك). Levantine: balanced, polite. MSA: formal, neutral.
10. [REQ] **Error messages.** User-facing error messages must be in the detected dialect. Stack traces/logs stay in English (technical convention). Never translate stack traces.
11. [REQ] **Documentation.** README/CHANGELOG bilingual: Arabic dialect section + English section. Never machine-translate — dialect requires native phrasing.
12. [REQ] **AI slop detection for Arabic.** Reject: unnatural MSA in dialect context, literal translations of English idioms (e.g., "hit the ground running" → "ضرب الأرض وهو يجري" = reject), dialect-inappropriate formality.
13. [REQ] **Testing.** Arabic output must be tested with dialect-native speakers or a dialect classifier. MSA-only QA = insufficient for dialect-tagged output.
14. [REQ] **Fallback.** If dialect confidence < 0.7, fall back to MSA and inform user. Never guess a dialect silently.
15. [REQ] **Privacy.** Dialect preference is PII-adjacent (reveals region/origin). Never log dialect in audit trail without redaction. Store preference as opaque locale code only.
16. [PROHIBIT] Generating Arabic in a dialect the user did not request or the system did not detect.
17. [PROHIBIT] Mixing dialects within a single response or file.
18. [PROHIBIT] Translating established technical terms to invented Arabic equivalents (e.g., "framework" → "إطار عمل" is accepted; "framework" → "هيكلية برمجية تفاعلية" = reject as invented).
19. [PROHIBIT] Using Arabic-Indic digits in code samples or technical configuration.
20. [PROHIBIT] Machine-translating dialect content. Dialect requires native or fine-tuned generation.

## Dialect Quick Reference

| Dialect | Locale | Greeting | Thanks | Register |
|---|---|---|---|---|
| Gulf | ar-SA/ar-AE | هلا/السلام عليكم | مشكور/يعطيك العافية | Formal-respectful |
| Egyptian | ar-EG | أهلا/إزيك | شكراً/تسلم | Casual-warm |
| Levantine | ar-PS/ar-JO | أهلا وسهلا | تسلم/شكراً | Balanced |
| Maghrebi | ar-MA | أهلا | بارك الله فيك | Mixed FR/AR |
| MSA | ar | السلام عليكم | شكراً جزيلاً | Formal-neutral |

## Integration Points

- **UX persona**: RTL layout, dialect-aware UI text.
- **DOC persona**: bilingual README with dialect sections.
- **PRODUCT persona**: MENA market positioning, dialect as competitive moat.
- **DEVX persona**: locale-aware scaffolding, dialect in error messages.
- **FREELANCE persona**: Arabic proposals in client's dialect (Gulf clients = Gulf dialect).

## References

- UserQ MENA AI survey 2026: 50% adoption, 28% Arabic churn, 24-point dialect gap.
- Eshal CX Benchmark 2026: MSA vs dialect-native intent detection (91% vs 64-88%).
- IntlPull State of i18n 2026: 73% LLM-based translation adoption.
