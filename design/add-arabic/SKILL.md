---
name: add-arabic
description: Add Arabic translations for new strings, following the project's Arabic-first conventions and IBM Plex Sans Arabic. Use when introducing user-facing text or when the user says a label "should be in Arabic".
---

# add-arabic

This is an **Arabic-first** application. Every user-visible string must be in Arabic. English is allowed only in code identifiers, comments, and admin-only labels (which are still preferably Arabic).

## Conventions

- **Font**: IBM Plex Sans Arabic (already loaded globally)
- **Direction**: RTL — `dir="rtl"` is set on `<html>`
- **Logical CSS classes**: `ms-`/`me-` not `ml-`/`mr-`, `ps-`/`pe-` not `pl-`/`pr-`, `text-start`/`text-end` not `text-left`/`text-right`
- **Numerals**: use Western Arabic numerals (`1, 2, 3`) not Eastern (`١، ٢، ٣`) — matches what Saudi users see in apps
- **Currency**: `ر.س` (riyal symbol) appended after the number with a non-breaking space
- **Dates**: Gregorian dates in DD/MM/YYYY format
- **Plurals**: Arabic has dual + plural — for now use plural form (no library, just consistent strings)

## Steps

1. **Locate the strings** to translate (page, component, validation message, toast).
2. **Translate naturally** — don't transliterate technical terms unnecessarily. Common mappings:
   - Lead → عميل محتمل
   - Customer → عميل
   - Property → عقار
   - Listing → إعلان
   - Deal → صفقة
   - Pipeline → خط الصفقات
   - Pool → الطلبات العقارية (project-specific naming — **not** "بركة")
   - Save → حفظ
   - Cancel → إلغاء
   - Delete → حذف
   - Edit → تعديل
   - More terms in [[02 - Glossary]]
3. **Place** the strings inline in the JSX (the project doesn't currently use an i18n library — it's Arabic-only). If a future English variant is added, that's a separate refactor.
4. **Verify RTL rendering** — check that the strings flow naturally with surrounding UI, and icons/spacing don't break.
5. **Run `/audit-rtl`** to catch any LTR-only classes that crept in.

## Verification checklist

- [ ] No English user-facing text remains
- [ ] All padding/margin uses logical (`ms-`/`me-`) classes
- [ ] Numbers display in Western digits
- [ ] Currency uses `ر.س`
- [ ] `/audit-rtl` clean

## Anti-patterns

- Don't transliterate technical terms — use Arabic equivalents (مفاوضة not "نيغوشيشن")
- Don't mix Arabic + English in one button label (e.g. "حفظ Save")
- Don't use Eastern Arabic numerals — Saudis read Western digits faster in apps
