---
name: mvsep-i18n-validation
description: Modify or verify MVSEP interface translations, startup locale selection, language preferences, and international-facing text.
---

# MVSEP language validation

The interface supports `en`, `zh-CN`, and `ja`. Read `src/i18n/index.ts`, `src/i18n/detect.ts`, and the relevant JSON files under `src/i18n/locales/` before changing language behavior.

Reuse [testing](../testing/SKILL.md) for regression coverage and [debugging](../debugging/SKILL.md) for runtime failures. The locale expectations below are specific to MVSEP.

## Startup and preferences

A valid saved selection takes precedence over automatic detection, including migrated browser storage. Without a saved selection, `src-tauri/src/system_locale.rs` reads the first nonempty value from `LC_ALL`, `LC_MESSAGES`, and `LANG`. If none is available, the frontend uses `navigator.language`.

Chinese selects `zh-CN`, Japanese selects `ja`, and other locales select English. Preserve support for POSIX strings (`zh_CN.UTF-8`, `C`, `POSIX`) and browser tags (`zh-CN`, `ja-JP`). Do not let a Chinese WebView override an explicitly English system locale.

Check fresh-start detection separately from saved preferences. Useful cases include conflicting locale variables, empty variables, unsupported languages, invalid saved values, storage migration, and language changes followed by restart.

## Visible text

Search the affected render code, `src-tauri/tauri.conf.json`, and `index.html` for fixed text. The native startup title must be usable before translation initialization. Compare translation key coverage against English and verify interpolation placeholders remain consistent. Avoid changing task state or algorithm loading behavior merely to re-render a language switch.

`README.md` is the default English documentation; Chinese is `README.zh-CN.md`, Japanese is `README.ja.md`, and `README.en.md` preserves old links.

## Checks

```bash
npm run build
cargo test --manifest-path src-tauri/Cargo.toml locale_environment_precedence
```

For changes to visible UI or startup integration, launch the app with an isolated configuration directory and inspect the affected screens under English and Chinese locales. Ensure isolation matches the app's actual database path resolution; do not overwrite the user's saved settings. A build or mocked language test does not prove that a released AppImage starts in the intended language. Report any runtime validation that remains outstanding.
