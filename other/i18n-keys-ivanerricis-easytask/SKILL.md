---
name: i18n-keys
description: Add, rename, merge or remove translation keys in EasyTask (src/i18n/locales en + it) without breaking the e2e specs, the docs screenshots or the unused-keys test. Use when touching any file in src/i18n/locales, when a UI text changes, or when a spec fails with an element that "wasn't found" by its text.
---

# Translation keys (EasyTask)

Two languages, always together: `src/i18n/locales/en/*.ts` and `src/i18n/locales/it/*.ts` (files by area: `common`, `dialogs`, `settings`, `tasks`, `workspace`, `menus`, `shortcuts`, `errors`, `automations`, `audio`, `archive`, `details`, `template-editor`). Types come from `src/i18n/i18next.d.ts`: a wrong key is a `tsc` error in `src`.

## What checks keys
- `tsc -b`: keys used with `t("...")` in `src` exist (typed). Dynamic keys (template strings, `as never`) are not checked.
- `src/i18n/unused-keys.test.ts`: every key is used somewhere. Removing the last use of a key fails it; so does leaving a key that nothing uses. Keys read with a computed name are matched by prefix (the `DYNAMIC_PREFIXES` list at the top of the test, for example `settings.appearance.`, `undo.`, `trash.`): a new family of computed keys needs its prefix added there, and keys under a listed prefix are never reported as unused.
- `src/i18n/i18n.test.tsx`: both languages have the same keys.
- **Not checked by any unit test**: the keys used by the e2e (`e2e/specs/*.ts`, `e2e/helpers.ts`, `e2e/ui-tour/tour-kit.ts`, `e2e/docs-shots`). They read the text with `tr("key")`, also with computed keys such as `settings.${category}.title`. A key that disappeared makes the spec fail only in the CI (Windows or the Linux shards).

## Steps
1. Edit en and it together; same key, same placeholders (`{{count}}`, `{{name}}`), plurals as `key_one` / `key_other` in both.
2. Merge duplicates (two keys with the same text in the same area) only when they mean the same thing for the user.
3. After removing or renaming a key, search every use, **including e2e**:
   `rg -n "old\.key|old\.\$\{" src e2e`
   and the computed forms (`tr(\`settings.${...}.title\`)`).
4. Update the specs, helpers and ui-tour to the new key. Check each `tr("...")` of the specs exists: the quick way is to run the key list of the specs against `src/i18n/locales/en` (a throwaway vitest test or a script), then delete it.
5. Run `npx vitest run src/i18n`, `npx tsc -b`, `npm run e2e:typecheck`.
6. A text visible in the docs screenshots changed: tell the user that `docs/screenshots` must be regenerated with `npm run docs:screenshots` (needs tauri-driver, not available in the cloud).

## Style
Short sentences, sentence case, no final dot in buttons. Italian: "Apri a destra", not "Apri sulla destra". Shortcut names go through `src/lib/shortcuts.ts`, not in the strings.
