---
name: d2r-ui-feature
description: Playbook for adding or changing UI in the Diablo II Ultra Utility loot-filter/tweaks editor (React + antd + Tailwind, backed by SettingsContext and the read/apply worker hooks). Use when creating or editing a page/component under src/pages or src/shared/components, wiring a new per-profile setting, adding UI strings or game locales, or changing how game JSON files are read/written.
---

# Working on the loot-filter / tweaks UI

Applies when editing anything under `src/pages/<domain>`, `src/shared/components`,
`src/widgets`, or wiring new settings into the editor.

## 1. State lives in SettingsContext — not local state
- Read settings via `useSettings()` getters (`getItemSettings`, `getCommonSettings`,
  `getGemSettings`, `getRuneSettings`, `getTweaksSettings`…); write via the `update*` setters.
- A new per-profile setting means: extend the `AppSettings` shape, add a `getDefault*`
  helper, AND add a migration (in the style of `migrateItemsSettings` / `cleanSettings`)
  so old localStorage/profile JSON keeps loading.
- `tweaks` are stored separately (`STORAGE_KEYS.TWEAKS`) and stripped from profile
  export — never fold tweaks into profile settings.

## 2. Two different "locale" systems — do not conflate (most common bug)
- **App UI strings** (i18next): `src/shared/i18n/locales/*.json` → `de, en, es, fr, pl, ru, uk`.
  Add the key to `en.json` (source of truth), then run `node scripts/sync-locales.cjs`.
  Use in components via `useTranslation()` / `t()`.
- **Game locales** (`SUPPORTED_LOCALES`, 13: `enUS…zhCN`): columns written into the game's
  JSON, mirrored by the `Locales` interface. Adding one means updating every
  `getDefault*` / `createFilledLocales` helper in `SettingsContext`.

## 3. Game file I/O goes through the worker hooks
- Reads/writes use the `use*Worker` hooks (`readFromFiles` / `applyChanges`). Reuse them;
  don't call `readTextFile`/`writeTextFile` directly from components.
- Writes are retry-with-backoff with a fallback to the Rust `ensure_writable` command
  (game files are often read-only/locked).
- Preserve game color codes (`ÿc0`, `ÿc9`…) verbatim on write — never strip them;
  `removeColorCodes()` is display/search only.

## 4. Styling
- antd components themed via `src/shared/assets/antd-theme.css`; layout with Tailwind.
- Dark mode = the `dark` class on `<html>` (`getIsDarkTheme()`); support both themes.
- Basic vs advanced mode resizes the window (`WorkSpace.tsx`): keep layouts working at
  600×790 (basic, fixed) and 1200×790 (advanced, resizable).

## 5. Before you finish
- Run `npm run tcheck` — the ONLY correctness gate (no test runner, no linter). Fix type errors.
- If you added UI strings, confirm `sync-locales.cjs` ran and all 7 locale files have the key.
