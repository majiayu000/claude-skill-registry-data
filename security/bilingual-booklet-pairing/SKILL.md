---
name: bilingual-booklet-pairing
description: Use when paired tr.md and en.md files need a parity verdict, when titles, frontmatter, headings, or DOI sets may have drifted between languages, or when a bilingual document is approaching release and its translation coverage needs an audit.
---

# Bilingual Booklet Pairing

## When to use

Use this skill whenever a booklet exists or is planned in both Turkish and English and the user needs parity rather than a loose translation. For manuscripts rather than booklets, bilingual-manuscript-scaffold builds the pair that this skill audits. It is not for validating that concepts translate equivalently across languages at a terminological level, that is multilingual-concept-validity-audit.

## Inputs

- Paths or text for `tr.md` and `en.md`.
- Booklet identifier.
- Target release status.
- Any known culturally specific examples that should not be translated literally.

## Workflow

1. Confirm both language files exist.
2. Compare frontmatter fields, especially `booklet_id`, `version`, `date_published`, `date_last_revised`, `human_review`, citation counts, fabricated citation counts, disclosure standard, license, and status.
3. Check that `language` differs correctly and titles are semantically aligned.
4. Compare heading structure and section order.
5. Identify missing paragraphs, unmatched tables, unmatched diagrams, or unmatched reference items.
6. Mark cultural adaptation points where exact translation would weaken the text.
7. Check that examples, local institutions, and legal references are appropriate for the language version.
8. Return a parity verdict.
9. When the parity verdict is pass, hand release preparation to open-science-release-packager and flag any authorship field discrepancies for authorship-contribution-ledger.

## Output

Return:

- Pair identity.
- Frontmatter parity table.
- Heading parity table.
- Content gaps.
- Cultural adaptation notes.
- Citation and disclosure parity.
- Verdict, pass, partial, or fail.
- Required fixes before release.
- What to record at session end: the parity verdict, any fields still mismatched, and which fixes were delegated versus left for human resolution.

## Verification

- Both files share the same `booklet_id`.
- Both files carry the same citation counts and fabricated citation counts.
- Heading order is either matched or intentionally adapted.
- Legal, clinical, and regional terms are not flattened into misleading literal translations.
- Release status is not recommended until both files pass parity.
- Before closing: any concept-level translation doubts are flagged for multilingual-concept-validity-audit, and the parity result is ready to hand to open-science-release-packager.

## Safety

Do not insert private examples, identifiable clinical material, or institutional secrets to make a translation feel realistic. Use anonymized or generic examples unless the user supplies publication-safe text.

## Example prompt

"Check parity between booklets/009-ethics-irb/009-01-0001/tr.md and en.md before release."

Expected smoke output:

- Frontmatter parity, pass or specific field mismatches.
- Heading parity, pass or named missing headings.
- Cultural adaptation notes for KVKK, GDPR, IRB, and ethics committee terminology.

## Türkçe kullanım notu

Bu beceri, aynı kitapçığın Türkçe ve İngilizce dosyalarının gerçekten eş olup olmadığını denetler. Başlık sayısı, frontmatter alanları, atıf sayıları ve DOI kümeleri karşılaştırılır, kültürel uyarlama gereken yerler birebir çeviriden ayrılır. Eşlik geçmeden yayın önerilmez. El yazmaları için aynı işin kurucusu bilingual-manuscript-scaffold becerisidir. Kavram düzeyinde çeviri belirsizlikleri multilingual-concept-validity-audit'e devredilir. Eşlik onaylandıktan sonra yayın hazırlığı open-science-release-packager'a taşınır.
