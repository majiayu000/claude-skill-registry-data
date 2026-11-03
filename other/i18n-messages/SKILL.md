---
name: i18n-messages
description: How to add or change user-facing copy in this repo (EN + PL catalogue). Use whenever adding, editing or removing any string a user will see, or when the i18n parity test goes red.
---

The product ships in two locales, `en` (the source and the schema) and `pl`. The full contract is
docs/SPEC.md §9, owned by docs/I18N.md - this is the working procedure.

## Adding or changing a string

1. Never hardcode user-facing copy in a component. Add a dotted key to `src/lib/i18n/messages/en.ts`
   in the group its surface belongs to, and render it through `t()`. The groups are a reading aid,
   not a namespace: moving a key between them touches nothing else.
2. **The same key lands in `pl.ts` in the same change.** English is the schema, so the compiler
   catches a missing key; it cannot catch the four things that make copy look finished and read
   wrong, and `src/lib/i18n/__tests__/parity.test.ts` does: a renamed placeholder, a plural branch
   Polish needs and English does not, an empty value, and an English sentence sitting in the Polish
   catalogue. Run `pnpm test` - red output names the exact key.
3. Author a real translation. A word that is genuinely identical in both languages goes in the
   `PROPER_NOUNS` list in the parity test, where adding it is a visible decision rather than a quiet
   weakening of the untranslated check.
4. Removing a key removes it from both files.

## Traps that pass a naive check

- **Polish has four CLDR plural categories** (`one`, `few`, `many`, `other`) where English has two.
  A message with a count goes through the plural machinery; an `if (n === 1)` in a component is a
  defect (SPEC §9).
- **Placeholders are part of the key's contract**: `{count}` must survive translation under the same
  name. `as const` in `en.ts` is what makes the literal type carry them.
- **Numbers, dates and money inside messages** are formatted by the message formatter with the active
  locale, never concatenated in pre-formatted.
- **`Intl.DisplayNames` and `Intl.Locale.prototype.textInfo` are banned** in `src/lib/i18n`, and
  `source-rules.test.ts` enforces it: their output differs between workerd and WebKit, which is a
  hydration mismatch rather than a tolerance. Both facts live in the frozen table in `locales.ts`.
- **Stored rows carry keys and parameters, never sentences** - a notification row or an email
  envelope written as prose is unreadable to someone who later switches language.

## Verification

`pnpm test` (parity + source rules) is the law here.
