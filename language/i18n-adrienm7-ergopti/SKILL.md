---
name: i18n
description: Add or change localized user-facing text across every locale. Use for UI labels, dialogs, menus, tooltips, onboarding, or messages.
---

# User-facing text

`AGENTS.md` makes developer text English and routes user-facing French through
this skill. French is not hardcoded: every user-facing string goes through the
i18n system in **all 21 languages**. This includes WebView UIs (metrics,
download window, onboarding), not just native menus.

Never hardcode a UI string anywhere. There is exactly one narrow exception, and
it is documented in code where it applies: a fatal pre-boot error modal that
fires before i18n can be loaded.

## Where the strings live

```
static/ergopti_plus/_shared/data/locales/
├── en.json    ← canonical key set (tracked)
├── fr.json … zh.json   (20 more, tracked)
└── *.tsv      ← gitignored self-healing fast-parse cache — never edit, never commit
```

21 locales: `ar cs da de en es fr he hi it ja ko nl no pl pt ru sv tr uk zh`.

The `.tsv` files are a regenerated parse cache (`project-locale-fast-cache`).
Only the `.json` is the source. Editing a `.tsv` does nothing durable.

## Procedure

1. Add the key to **`en.json` first** — it is the canonical key set that every
   other locale is diffed against.
2. Propagate to the other 20. `python tools/locale/check_locales.py --fix` is the
   backfill tool; review what it writes rather than trusting it blindly.
3. Reference the key from code via the i18n accessor — never inline the text.
4. Run the gate. `npm run test:js` carries the translations audit, and
   `tests/meta/test_locale_json_valid.ahk` enforces key parity in the AHK suite.

A missing key in one locale fails CI. Adding an English string "temporarily"
with the intent to translate later does not survive the gate — do it in the same
commit.

## Reviewing

When reviewing a diff that adds UI, check for the string literal, not the key:
a hardcoded French label reads naturally and slips through review precisely
because it looks correct to a French speaker.
