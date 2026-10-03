---
name: i18n
description: "Manage translations for this Svelte SPA's custom i18n system. Use whenever the user mentions translations, i18n, langStore, t(), adding/translating keys, hardcoded strings, missing translations, language toggle, or the frontend/src/lib/i18n/{en,id}.json files. Triggers on: i18n, translation, translate, t(), langStore, hardcoded string, missing translation, language, bahasa, en.json, id.json, language key, Add [language] translation, is this string translated?"
---

# i18n for this Svelte SPA

This project uses a **custom i18n system** (NOT Paraglide — see AGENTS.md decision #6 for why). All operations should preserve this architecture: flat JSON files + `t(key, vars?)` function. Do NOT migrate to Paraglide/inlang or introduce compile-time extraction without explicit user request.

## Project conventions (DO NOT BREAK)

### File layout
- Translation files: `frontend/src/lib/i18n/{en,id}.json`
- Loader: `frontend/src/lib/i18n/index.svelte.ts`
- **Base language**: `en` (English) — reference structure for integrity/validation checks
- **Second language**: `id` (Indonesian)
- Keep both files in sync — any add/delete must update BOTH

### Key style — FLAT `snake_case`
Keys are **flat dotted strings using underscores**, grouped by prefix. Examples:
```
site_name, site_tagline
nav_home, nav_admin
hello_title, hello_subtitle, hello_description
admin_title, admin_text
login_title, login_username, login_password
```
**Never use nested objects** (`{"nav": {"home": "..."}}`) — this project uses flat keys only. When using the MCP, tools may suggest `nested` style — override to `flat` or reject nested key suggestions.

### Interpolation
Uses `{var}` placeholder syntax:
```json
"items_count": "{count} items"
```
```svelte
t('items_count', { count: 3 })
```
When adding translations with placeholders, ensure the **same `{var}` names appear in both `en` and `id`** versions. The interpolator does not validate missing vars — output will show the literal `{var}` text.

### Usage in components
```svelte
<script>
  import { t, i18n } from '$lib/i18n/index.svelte';
</script>

<h1>{t('site_name')}</h1>
<button onclick={() => i18n.toggle()}>{t('lang_toggle')}</button>
```
**Never call `t()` outside Svelte reactive context** expecting reactivity — `t()` reads `i18n.current` which is `$state`, so it only updates inside Svelte components.

## Editing translations

There's no MCP server wired up for this project's i18n (only `playwright` and `svelte` are configured in `.opencode/opencode.json`) — this is plain JSON, so read and edit the files directly rather than looking for a specialized tool.

### User asks "what's missing / is everything translated?"
1. Read both `en.json` and `id.json` and diff the key sets — a key present in one but not the other is a bug
2. Grep `frontend/src` for `t('...')` calls and confirm every key referenced in code actually exists in both files
3. Report using a markdown table: | key | status | notes |

### User asks "add a new translation key" or "translate [string]"
1. Check whether a similar key already exists first (grep for the English text or a likely key prefix)
2. Add the new key to **both** `en.json` and `id.json`, using the flat snake_case style with the appropriate prefix (`nav_`, `hero_`, `section_`, `about_`, `admin_`, `settings_`, etc.) — keep it at the same relative position in both files so they stay easy to diff by eye
3. Wire it up in the component with `t('new_key')`
4. **Remind the user**: "Restart `pnpm dev` or refresh the page — Svelte doesn't hot-reload JSON imports."

### User asks "extract hardcoded strings" / "find untranslated text in component"
1. Read the component and identify literal user-facing strings not already wrapped in `t(...)`
2. Propose keys in the snake_case style above, with EN/ID translations
3. **Do NOT auto-extract** — show the user the proposed texts → keys → EN/ID translations and ask for confirmation
4. After confirmation, add the keys to both JSON files and replace the literal strings with `t('key')` calls

### User asks "rename / delete a key"
1. Grep `frontend/src/` for every reference to the key first: pattern `\bt\(['"]old_key['"]`
2. Show the user every call site before touching anything
3. After the user confirms, rename/delete in both `en.json` and `id.json`, then update every `.svelte` file that called `t('old_key', ...)`

### User asks "show structure / stats" or "validate / organize files"
Read both JSON files directly and compare — there's no dedicated tool for this, it's just JSON. If the key sets have drifted apart, add the missing keys (ask the user for the translation text if you don't know it) rather than silently deleting the extras.

## Common pitfalls

### 1. Keys with mixed casing
The project enforces lowercase snake_case. If the MCP suggests `nav.Home` or `nav_home_page_title_v2`, **reject silently and propose the project-style** equivalent (`nav_home`, `home_title`).

### 2. Plurals / count
There is **no pluralization system**. Keys like `items_count` accept `{count}` and render as `"{count} items"`. Do not introduce ICU MessageFormat or new plural libraries.

### 3. Component rewiring after key rename
After renaming any key, ALL `.svelte` files using `t('old_key', ...)` must be updated. Use `grep`:
```
pattern: \bt\(['"]old_key['"]
include: *.svelte
```

### 4. Adding a third language (e.g., `zh`)
- Create `frontend/src/lib/i18n/zh.json` with all keys (copy from `en.json` as starting point)
- Update `index.svelte.ts`: extend `Lang` type + adding to `dictionaries`
- Update `i18n.toggle()` — currently only flips en ↔ id, won't rotate to third language
- Update MCP config if needed; MCP will auto-detect the new file
- Verify with `i18n_check_translation_integrity`

### 5. Spaces and special chars in keys
Keys must match `[a-z][a-z0-9_]*`. Indonesian text with `/`, `:`, spaces in value is fine — only keys are constrained.

## Important: do NOT touch

- `frontend/src/lib/i18n/index.svelte.ts` — Svelte store mechanics are stable. Only modify when adding a third language.
- IDs of existing translations: renaming breaks runtime silently (`t('old_key')` returns the raw literal). Always grep first.
- The `STORAGE_KEY = 'desa_wisata_lang'` constant in `index.svelte.ts` — used by existing users; changing it forgets their language preference.

## Verification after any change

Before declaring "done":
1. Confirm `en.json` and `id.json` have identical key sets (no key present in only one)
2. Grep `frontend/src` for every `t('key')` call and confirm each key exists in both files
3. If you added `{var}` interpolation, confirm the same `{var}` names appear in both language versions