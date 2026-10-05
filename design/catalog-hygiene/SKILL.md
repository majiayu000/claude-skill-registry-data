---
name: catalog-hygiene
description: This skill should be used when the user mentions "translation catalog", "i18n keys", "missing translations", "unused keys", "untranslated", "locale files", "message catalog", "RTL", "right to left", "logical properties", "bidi", or auditing/cleaning translation files and preparing a UI for right-to-left languages. It provides the methodology for keeping catalogs healthy and making layouts direction-agnostic.
---

# Catalog Hygiene

## Purpose
Provide a standardized, static methodology for keeping translation catalogs correct and complete, and for making a UI ready for right-to-left languages. A catalog rots the moment code and translations drift: keys used in code but missing from a locale render raw ids to users, keys left in the catalog after a feature is deleted are paid-for cruft, and values that were copy-pasted from English *look* translated but ship the wrong language. RTL readiness is the other half, a layout full of physical `left`/`right` CSS silently breaks in Arabic and Hebrew.

## Catalog Health Checks
Cross-reference the code's translation calls against every locale file and report:

| Check | Definition | Impact |
|---|---|---|
| Missing key | used in code, absent in a locale | fallback text or a raw key shown to users |
| Unused key | in the catalog, referenced nowhere | dead weight; wasted translation spend |
| Untranslated value | target value byte-equal to the source | looks done, ships the source language |
| Placeholder drift | `{name}`/`{count}` set differs across locales | `undefined` in the string or a formatter throw |
| ICU error | malformed `plural`/`select`, unbalanced braces | renders literally or throws at runtime |
| Missing plural category | locale lacks a CLDR form its grammar needs | wrong number agreement for real inputs |

Measure **coverage per locale** = translated keys ÷ source keys, and treat the source locale (usually `en`) as the reference set.

## Key Design Principles
- Namespace keys by feature/component and derive them from **meaning**, not the English string, so re-wording copy does not churn keys.
- One key = one message = one place. Reuse before duplicating; do not fork `save`/`save_button`/`btn_save` for the same word.
- Never machine-translate to fill a gap, leave the value empty (or the framework's missing sentinel) for a human translator.

## RTL Readiness In One Line
Replace direction-baked physical CSS with logical properties (`margin-left` → `margin-inline-start`, `left` → `inset-inline-start`, `text-align: left` → `start`). Logical properties resolve to the correct physical side based on the element's `dir`, so one stylesheet serves both directions. What logical properties *cannot* fix, mirrored icons, x-axis transforms, directional shadows, and bidi text, needs human judgment. See `references/rtl-logical-properties.md`.

## Never Fabricate
"Untranslated" by value-equality has false positives (proper nouns, brand names, shared tokens like "OK"/"Email"), flag, never auto-delete. Never invent a coverage number or a key that is not in the files.

## Additional Resources
### Reference Files
- **`references/catalog-frameworks.md`**: key and file conventions plus extraction idioms for react-i18next, react-intl/FormatJS, vue-i18n, next-intl, i18next, and gettext (`.po`), including how to find every translation call for cross-referencing.
- **`references/rtl-logical-properties.md`**: the complete physical→logical CSS property map and the common RTL pitfalls (directional icons, transforms, shadows, background-position, and bidi text handling).
