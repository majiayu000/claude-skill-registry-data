---
name: i18n
description: Use when internationalising or localising an app, preparing it for translation, extracting hardcoded strings, adding plurals, or fixing locale bugs — dates, times, time zones, DST, numbers, currency, units, first day of the week, RTL layout, or text that breaks with long translations, CJK, or emoji. Covers web/JS/TS, Apple platforms (String Catalogs, FormatStyle), and Android. Not for writing translations.
license: MIT
allowed-tools: Read Glob Grep Edit Write
model: sonnet
effort: high
compatibility: Any UI project; detects the platform — web and JS/TS first-class, Apple platforms (Swift/SwiftUI) well supported, native Android best-effort
metadata:
  short-description: Prepare apps for translation and locale-correct formatting.
---

You make an app ready for any language and region, so adding a language later is translation work, not a refactor. Use the platform's own localisation and formatting APIs as the source of truth — never a custom framework around them.

## 1. Pick the Mode

Decide from the request; do not ask.

- **Build mode** — the task creates or changes UI or formatting code. Apply the rules as constraints while writing it. Mention a rule only when it changed a decision, in one line.
- **Adopt mode** — the user asks to internationalise, prepare for translation, or fix i18n across the app. Work through Step 4.

Ship no new languages unless asked. Making strings localisable and adding translations are separate jobs.

## 2. Detect the Platform

Read the manifest as prose and load **only** the matching guide:

| Platform | Detected by | Load |
|---|---|---|
| **Web / JS / TS** | `package.json` | `references/js.md` |
| **Apple platforms** | `*.xcodeproj`, `Package.swift` with an app target | `references/apple.md` |
| **Android** | `build.gradle(.kts)` | `references/android.md` |

If the project already uses an i18n library (`next-intl`, `react-i18next`, `vue-i18n`, `FormatJS`, …), keep it and follow its conventions; the guide covers what to check, not which library to swap to. React Native/Expo uses `references/js.md` for strings and formatting. Other stacks: apply the rules using that platform's ICU/CLDR-backed APIs.

## 3. Rules

| Rule | Impact | Applies to | File |
|---|---|---|---|
| Localisable strings | CRITICAL | every user-facing string, plurals, interpolation | `rules/localisable-strings.md` |
| Time zones and timestamps | CRITICAL | stored events, history, timelines, schedules | `rules/time-zones.md` |
| Locale-aware formatting | HIGH | dates, times, numbers, percentages, currency, durations | `rules/locale-formatting.md` |
| Units and measurements | HIGH | distance, speed, weight, temperature | `rules/units.md` |
| Text and layout | HIGH | user-generated text, layout, RTL, long translations | `rules/text-and-layout.md` |
| Deterministic tests | MEDIUM | tests touching dates, numbers, or strings | `rules/deterministic-tests.md` |

## 4. Adopt Mode

1. **Inventory** — find hardcoded user-facing strings, hand-rolled date/number formats, string concatenation, fixed units, and `left`/`right` layout. Report the counts before editing
2. **Set up the resource** — one string catalog or message file in the platform's native format, English (or the project's development language) only
3. **Fix in impact order** — CRITICAL first. Change only what international correctness needs; keep the existing design and behaviour
4. **Never change persisted data semantics** (timestamp meaning, stored units) without an explicit migration the user has approved — propose it instead
5. **Test** — add the deterministic tests from `rules/deterministic-tests.md`; build and run the suite, and report real results
6. **Validate the UI** — pseudolocalisation, the longest text expansion, RTL, and the largest text size, using the tools in the platform guide

End with what changed, what is still hardcoded and why, and any migration you proposed but did not apply.

## Boundaries

- **Accessibility labels** must be localisable like any string; what they should say belongs to `accessibility`.
- **User-generated content** (names, notes, place names) is never translated, transliterated, or normalised unless the user asks.
- **Translation itself** — machine translation, translation services, and translator workflow are out of scope. Do not send app strings or user content to an external service.
