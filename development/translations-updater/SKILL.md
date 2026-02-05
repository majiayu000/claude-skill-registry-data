---
name: translations-updater
description: Update and complete JournalOS translation JSON files by running composer journalos:locale and fixing missing or empty translations in lang/*.json. Use when UI copy changes, new keys are added, or locale files are out of sync.
---

# Translations Updater

This Skill keeps JournalOS translation files consistent and complete. It regenerates locale keys using the project command and then fixes missing, empty, or invalid entries inside lang/*.json files.

## When to use this Skill

Use this Skill when:
- New UI text or translation keys were introduced
- Modules, pages, or components added new strings
- Translation JSON files contain empty or missing values
- Locale files are out of sync with the codebase

## Instructions

### Step 1: Regenerate locale files

1. Run the locale generation command:
   ```bash
   composer journalos:locale
   ```
2. Confirm the command completes successfully before making any edits.

### Step 2: Scan for missing or incomplete translations

1. Review all translation files:
   - `lang/*.json`

2. Identify any entries that are:
   - Missing keys (present in one locale but absent in another)
   - Empty strings (e.g. `"some.key": ""`)
   - Whitespace-only values
   - Null values
   - Invalid JSON

### Step 3: Fix translations

Apply the following rules:

1. Do not remove translation keys unless they are confirmed unused.

2. For missing keys:
   - Add the key to the relevant locale file(s).

3. For empty or invalid values:
   - Replace them with an appropriate human-readable translation.

4. Ensure consistency:
   - Same meaning across languages
   - Same tense and tone
   - Same terminology as used elsewhere in the app

5. Preserve formatting and placeholders exactly:
   - Do not modify tokens such as `:name`, `:count`, `{value}`
   - Do not alter embedded HTML or Markdown

### Step 4: Validate JSON correctness

Ensure all `lang/*.json` files:
- Are valid JSON
- Use consistent indentation
- Contain no duplicate keys

### Step 5: Quality checks

1. Confirm there are no:
   - Empty strings
   - Null values
   - Placeholder values like TODO

2. If a translation is uncertain, prefer literal and conservative wording.

3. Maintain existing key order unless the project explicitly requires sorting.

### Step 6: Run tests

1. Run the test suite:
   ```bash
   composer test
   ```
2. Resolve any failures related to translations or locale loading.

## Best practices

- Never rename translation keys without corresponding code changes
- Never translate or alter placeholders
- Favor consistency over stylistic variation
- Avoid informal language unless the UI already uses it

## Validation checklist

- [ ] `composer journalos:locale` executed successfully
- [ ] All `lang/*.json` files are valid JSON
- [ ] No missing keys remain
- [ ] No empty or null translation values remain
- [ ] Placeholders are preserved exactly
- [ ] All tests pass

## Output expectation

All translation files in `lang/*.json` are regenerated, complete, valid, and contain no missing or empty translations.
