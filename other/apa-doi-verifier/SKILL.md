---
name: apa-doi-verifier
description: Use when a reference list needs APA 7 cleanup, when DOIs must be confirmed real against Crossref or PubMed, when the user asks whether AI-suggested citations actually exist, or when a manuscript needs a citation hygiene pass before submission or defense.
---

# APA DOI Verifier

## When to use

Use this skill when a bibliography, reference list, manuscript section, or AI-generated citation set needs APA 7 cleanup and DOI verification before it is trusted. In the wider lifecycle it runs after social-science-literature-triage has scoped the sources and before ai-disclosure-auditor counts verified citations, and its per-source results belong in the source-passport-ledger record. It is not where you decide which sources to read, that is social-science-literature-triage, and it does not count verified citations into a disclosure statement, that is ai-disclosure-auditor; here you only prove that the references already in hand are real and correctly formatted.

## Inputs

- Reference list or citations to check.
- Manuscript discipline.
- Journal style constraints, if stricter than APA 7.
- Whether live Crossref, PubMed, publisher, or library lookup is available.

## Workflow

1. Preserve the user's original reference list as the comparison baseline.
2. Split references into journal articles, books, chapters, reports, guidelines, preprints, theses, and web sources.
3. For journal articles, check title, authors, year, journal, volume, issue, pages, and DOI.
4. Use Crossref as the first DOI lane when browsing or a Crossref tool is available.
5. Use PubMed or publisher pages as a second lane for biomedical, clinical, psychology, and health sources.
6. Flag ambiguous or non-resolving references instead of repairing them by guesswork.
7. Convert valid entries into APA 7 style.
8. Classify fabricated citation risk as low, medium, high, or confirmed fabricated.

## Output

Return:

- Cleaned APA 7 reference list.
- Verification table with status per reference.
- DOI corrections.
- Items without DOI and why that may be acceptable.
- Fabricated citation risk classification.
- Open verification tasks.
- What to record at session end: the cleaned reference file, the references still unresolved, and a one-line note for the AI-use disclosure.

## Verification

- Every DOI resolves or is explicitly marked unresolved.
- No DOI is invented from a title, author, or journal pattern.
- Author order is preserved unless a source confirms otherwise.
- Books and official reports are not forced into DOI format.
- Risk classification distinguishes missing DOI from nonexistent source.
- Every verification claim names the lane that confirmed it, Crossref, PubMed, publisher page, or library record, per reference.
- Before closing: every unresolved reference is written down where the next pass can find it, and the verified set is ready to hand to ai-disclosure-auditor for counting.

## Safety

Do not use synthetic metadata as final truth. Do not claim Crossref, PubMed, Scopus, or Web of Science verification unless it was actually performed in the current session or the user supplied exported evidence.

## Example prompt

"Verify these 12 APA references for DOI correctness and classify fabricated citation risk."

Expected smoke output:

- A table with reference number, source type, DOI status, metadata status, and risk.
- Corrected APA 7 entries only for verified or user-confirmed sources.
- A short list of unresolved items for manual lookup.

## Türkçe kullanım notu

Bu beceri, bir kaynakçayı güvenilir saymadan önce APA 7 düzenine sokar ve her DOI'nin gerçekten var olduğunu doğrular. Hakeme gitmeden önceki son kontrolde, yapay zekâ destekli taslakların kaynakçasında ya da jüri öncesi tez denetiminde kullanın. Çözülmeyen DOI tahminle onarılmaz, doğrulanmamış referans temiz sayılmaz, her doğrulama hangi kanaldan yapıldığıyla birlikte raporlanır. Bu beceri hangi kaynakların okunacağına karar vermez, o iş social-science-literature-triage'ındır, doğrulanmış kaynakları beyana saymak için ai-disclosure-auditor'a devreder. Oturum sonunda temizlenmiş dosya, çözülmemiş referanslar ve beyana eklenecek kısa not kayda geçirilir.
