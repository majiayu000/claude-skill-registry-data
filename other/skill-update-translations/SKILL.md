---
name: Update Translations
description: "Add new i18n keys to translation files following naming conventions, detect missing locales, and flag untranslated strings. Triggers on phrases like 'add translation', 'update i18n', 'missing translation key', or when JSX strings are added under `frontend/src/`. Reports drift across locales and emits a structured patch with file:line citations."
model: inherit
---

## Purpose

Keep `frontend/src/i18n/messages/<locale>/*.json` files complete and consistent. Simpler-grants-gov ships English and Spanish today; new keys must be added to every locale file (with explicit `TODO_TRANSLATE` markers) so deploys never silently miss strings.

## When to Invoke

- A developer adds a hard-coded string in JSX/TSX under `frontend/src/`.
- A developer asks to "add a translation key" or "update i18n".
- A reviewer asks for "missing translation" coverage.
- Before tagging a release, to sweep for drift.

## When NOT to Invoke

- For backend strings — the API does not localize user-facing copy in this repo.
- For non-displayed strings (logs, error keys consumed only programmatically).
- As a substitute for human translation review — emits placeholders only.

## Inputs

- **target**: an active file, an explicit path, or `git diff` range.
- **mode** (optional): `add` (default — add proposed keys), `audit` (only report drift), or `prune` (report unused keys).

## Procedure

1. Resolve target. If a file, scan for JSX text nodes and `t('...')` calls.
2. Locate locale files: `frontend/src/i18n/messages/<locale>/*.json`. Treat the English file as the source of truth.
3. Build the key universe:
   - Keys referenced in code (`t('feature.subkey')` calls).
   - Keys present in each locale file.
4. Compute three sets:
   - **MISSING_IN_LOCALE** — present in English, missing in another locale.
   - **MISSING_IN_CODE** — present in code, missing in English.
   - **UNUSED** — present in any locale, not referenced in code.
5. For new strings detected in JSX text nodes (literal text not wrapped in `t()`), propose a key following the convention:
   - Namespace: file's component name in camelCase
   - Subkey: kebab-case slug of the string, max 4 words
   - Example: `searchBar.clearButton` for "Clear" inside `SearchBar.tsx`
6. Generate the patch:
   - English: real string
   - Other locales: `"TODO_TRANSLATE: <english>"`
7. Cross-reference `documentation/rules/frontend-*.md` for namespace conventions.
8. Emit the Output Format. In `add` mode, also emit a unified diff. Do not write files.

## Outputs

```
Update Translations — frontend/src/components/search/SearchBar.tsx
Locales: en, es
Mode: add

Findings:
  MISSING_IN_LOCALE (2):
    feature.search.placeholder        es
    feature.search.clearButton        es
  MISSING_IN_CODE (0)
  UNUSED (1):
    feature.legacy.deprecatedTip      en, es

Proposed new keys (1):
  searchBar.helperText  "Press Enter to search"  (L42)

Patch:
  --- frontend/src/i18n/messages/en/search.json
  +++ frontend/src/i18n/messages/en/search.json
  @@
  +  "searchBar.helperText": "Press Enter to search",

  --- frontend/src/i18n/messages/es/search.json
  +++ frontend/src/i18n/messages/es/search.json
  @@
  +  "searchBar.helperText": "TODO_TRANSLATE: Press Enter to search",

Block merge: yes (untranslated key in `es`)
```

## Safety

- Never writes files — emits a unified diff only.
- Never invents translations — non-English locales receive `TODO_TRANSLATE` markers.
- Never deletes keys in `add` mode; pruning requires explicit `mode=prune`.
- FedRAMP / accessibility: alt text and aria-labels are first-class i18n strings and must be wrapped in `t()`.

## Examples

**Example 1 — Add a button label**
Developer types "Clear" inside `SearchBar.tsx`. Skill proposes `searchBar.clearButton`, generates the patch for both locales.

**Example 2 — Audit drift**
`mode=audit` over the whole `frontend/src/` returns 12 keys missing from `es` and 3 unused keys in `en`.

**Example 3 — Prune unused**
`mode=prune` lists removable keys; developer reviews and applies manually.

## Related

- `.cursor/skills/skill-accessibility-check/` — flags missing aria-labels that should also be translated.
- `documentation/rules/frontend-styles.mdc` — namespace and key conventions.
