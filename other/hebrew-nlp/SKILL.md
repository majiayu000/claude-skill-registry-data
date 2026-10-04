---
name: hebrew-nlp
description: Use when processing Hebrew text ג€” normalization, RTL handling, name extraction, intent matching, search indexing. Covers shared utilities under `src/lib/hebrew/`.
---

# Hebrew NLP skill

## When to invoke

- Normalizing customer input before storing in CRM (name, address, free text)
- Intent detection for routing (matching Hebrew trigger phrases)
- Search / dedup of customer records
- Generating embeddings of Hebrew text for retrieval

## Hard rules

1. **Always normalize before matching** ג€” Hebrew has multiple representations of the same string (with/without ׳ ׳™׳§׳•׳“, with/without geresh, final letters)
2. **Final letters**: ׳/׳/׳/׳£/׳¥ at end of word are visually distinct but semantically identical to ׳›/׳/׳ /׳₪/׳¦ ג€” normalize for search, preserve for display
3. **Bidi-safe storage** ג€” never store strings with embedded LRM/RLM control chars; strip on input
4. **Numbers**: Israeli phone numbers (`05X-XXXXXXX`), ׳×׳´׳– (9 digits with check digit), dates (DD/MM/YYYY vs YYYY-MM-DD) ג€” always parse to canonical form
5. **Mixed Hebrew/English** is the norm, not the exception ג€” never assume single-script text

## Normalization checklist

- [ ] Strip ׳ ׳™׳§׳•׳“ (vowel marks) for matching, preserve for display
- [ ] Normalize geresh (׳³) and gershayim (׳´) ג€” Unicode has both Hebrew and ASCII versions
- [ ] Final letters ג†’ base letters for matching
- [ ] Collapse whitespace, strip bidi controls
- [ ] Lowercase any embedded English
- [ ] NFC unicode normalization

## Common pitfalls

- **Sorting**: JavaScript default sort is wrong for Hebrew ג€” use `Intl.Collator('he-IL')`
- **String length**: `.length` returns code units, not grapheme clusters ג€” use `Intl.Segmenter` for visible character count
- **Regex**: `\w` and `\b` do NOT work on Hebrew ג€” use Unicode property escapes (`\p{L}`, `\p{N}`) with `u` flag

## Intent matching for routing

Store trigger phrases in `src/lib/hebrew/intents.ts` as normalized strings. Match input after applying same normalization. Never compare raw strings.

## What this skill is NOT

- Not a translator ג€” never translate Hebrewג†”English in code paths the customer sees
- Not a tokenizer for LLM input ג€” Claude handles Hebrew tokenization natively