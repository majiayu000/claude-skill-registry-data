---
name: resume-i18n-translate
description: Extract i18n keys and translate the resume app locales using the existing OpenRouter-based scripts. Use when updating translation keys, adding languages, or re-running translations for dev/apps/resume and its i18next locale files.
---

# Resume I18n Translate

## Overview
Extract i18next keys and regenerate locale files for the resume app using the repository translation prompt and scripts.

## Workflow
1. Review the translation prompt and locale layout in `dev/apps/resume/scripts/translation/prompt.md` and `dev/apps/resume/src/i18n/locales`.
2. Extract keys: `cd dev/apps/resume && pnpm i18n:extract`.
3. Translate: `OPENROUTER_API_KEY=... pnpm i18n:translate`.
4. Inspect updated locale files for accuracy and avoid introducing new facts beyond the source content.
