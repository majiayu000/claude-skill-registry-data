---
name: settings-row
description: End-to-end recipe to add a new setting (user preference) to the EasyTask Settings dialog - stored pref with default and validation, context exposure, row in the right panel, it+en translations, reset behaviour, tests. Use when the user wants a new option/preference/setting, or to change the Settings dialog.
---

# Add a setting (EasyTask)

Paths are under `src/`. Use the name of an existing similar pref as a template: `showGroupSeparators` (boolean), `sidebarItemSize` (segmented), `colorIntensity` (slider with row reset), `audioPlayerOpacity` (slider).

## 1. Stored preference: `lib/store/preferences.ts`
- Add the type / constants if needed (`DEFAULT_X`, `X_OPTIONS`, a `clampX` or `isValidX` helper) next to similar ones (`ANIMATION_SPEEDS`, `clampBackupKeep`, `UNDO_LIMIT_OPTIONS`).
- Add an entry to `UI_PREFS` with `def<T>({ key, default, normalize })`. The field name is the name exposed by `usePreferences()`.
  - Boolean default false: `normalize: value => value === true`. Boolean default true: `normalize: value => value !== false`.
  - Enums / numbers: `normalize` must map any garbage to a valid value (`ANIMATION_SPEEDS.includes(...)`, `clampColorIntensity`).
- `key` is the name on disk: never rename it later.
- Pref only used outside React (not in `usePreferences()`): put it in `APP_PREFS` instead (e.g. `autoBackup`) and, if useful, add a thin `getX` / `saveX` wrapper at the bottom. Read/write with `getPref(name)` / `savePref(name, value)`.

## 2. Context: nothing to write for `UI_PREFS`
`contexts/preferences-context.tsx` builds state and one setter per `UI_PREFS` entry (`set` + capitalized name, via `setterName`; types in `contexts/preferences-context-object.ts`, `PrefSetterName`). So `const { x, setX } = usePreferences()` (`contexts/use-preferences.ts`) works right away. Only touch the provider if the pref has a side effect (see `language`, `animationSpeed`, `audioPlayerScale`) or belongs to `resetAudioSettings`.

## 3. The row: `components/dialogs/settings/`
Pick the category panel: `AppearanceSettings.tsx`, `NotesSettings.tsx`, `AudioSettings.tsx`, `DataSettings.tsx`, `ShortcutsSettings.tsx` (`categories.tsx` lists them; "about" stays last). A new category needs a `Panel`, an entry in `SETTINGS_CATEGORIES`, an icon and a `settings.categories.<id>` key (extend the `labelKey` union).
- Switch: `<SettingsSwitchRow label description checked onCheckedChange />` (from `SettingsRow.tsx`).
- Few exclusive values: `<SegmentedSetting label description value options onChange />` (ToggleGroup); see `SidebarItemSizeSetting.tsx`.
- Anything else (Slider, Select, Input): `<SettingsRow label description>{({ id, labelId, descriptionId }) => control}</SettingsRow>`. Tie the control to the row: `id`, `aria-describedby={descriptionId}`, and `aria-labelledby={labelId}` for groups/sliders. See `ColorIntensitySetting.tsx`, `AudioSettings.tsx` (`PercentRange`: draft while dragging, `deferChange`, `onValueDrag`/`onValueChange`/`onValueCommit`).
- Use shadcn controls from `@/components/ui/*` (Switch, Select, Slider, ToggleGroup); never raw inputs where shadcn has one.
- Non-trivial rows go in their own `XSetting.tsx` component (like `AnimationSpeedSetting.tsx`), read `usePreferences()` there.
- Layout rules:
  - Panel = `SettingsPanel title action?` containing a `SettingsCard` (flat list) or several `SettingsSubsection title` (titled card). Never put rows bare in the panel.
  - Every direct child of a card is one padded, divided row. Whatever belongs to a row (warning, error, preview, hint) goes in the SAME child: `<div className="flex flex-col gap-3"><SettingsRow .../>{extra}</div>` (see `AccentContrastHint` in `AppearanceSettings.tsx`).
- Row reset: pass `reset={value === DEFAULT ? undefined : <RowResetButton label={t("...reset")} onClick={() => setX(DEFAULT)} />}` to `SettingsRow` (the slot is reserved so controls line up).

## 4. Section "reset all"
- Appearance: `ResetAppearanceSetting.tsx`: add the pref to the destructuring, to the `isDefault` chain and to `handleReset`. Update its confirm texts (`settings.appearance.reset.*`) if they list the items.
- Audio: add the setter call to `resetAudioSettings` in `preferences-context.tsx` (and the default constant). `AudioSettings.tsx` already has the `SectionResetButton`.
- Other panels have no reset-all; if you add one, use `SectionResetButton` as the `SettingsPanel` `action`, `disabled` when all default.

## 5. Translations (both, same keys)
`i18n/locales/it/settings.ts` is the source of truth (it defines the type); `i18n/locales/en/settings.ts` is typed as `Translation["settings"]`, so a missing key fails `tsc`.
- Layout: `settings.<category>.<name>.label` / `.description` (+ `.reset`, option labels like `settings.appearance.sidebarSize.compact`). Simple rows may be a plain string (`settings.notes.sectionCount`). Subsection titles: `settings.notes.sections.<x>`.
- Italian is the primary language; no empty strings, same `{{placeholders}}` in both (`i18n/i18n.test.tsx` checks keys, empties, placeholders).

## 6. Tests
- `lib/store/preferences.test.ts`: add the key to the sorted "keeps the keys saved on disk" list; add default / garbage / clamp cases like the "audio file count and section separators preferences" block. The generic `it.each` over the table covers default and garbage already.
- `contexts/preferences-context.test.tsx`: assert the default and that the setter calls `savePref(name, value)`.
- `components/dialogs/dialog-settings.test.tsx`: its `vi.mock("@/contexts/use-preferences")` returns an explicit object: add `x` and `setX` there or the panel crashes. Add a test that changes the control and checks the setter.
- Appearance reset: update `settings/ResetAppearanceSetting.test.tsx` (`state`, mock, `it.each` of enabled cases, reset expectations).
- Texts in tests are Italian (default language). Use `userEvent` and role/name queries.
- If the pref changes app behaviour, test the consumer, mocking `usePreferences` as `GroupContainer.test.tsx` does.

## 7. Verify (from the repo root)
```
npx tsc -b
npx eslint src
npx vitest run src/lib/store/preferences.test.ts src/contexts/preferences-context.test.tsx src/components/dialogs src/i18n
```
Add the test files of the consumer you touched. Also grep for other mocks of `usePreferences` that may now lack the new field (`grep -rn "use-preferences\"" src --include=*.test.tsx`).
