---
name: translation-workflow
description: Manage i18n translation workflows for this codebase, including locale diffing, batching, applying translated JSON entries with translation-helper commands, syncing, validating, and avoiding unsafe JSON edits.
---

# Translation Workflow

**CRITICAL: NEVER use the Edit tool on JSON locale files.** Multi-byte UTF-8 characters (Japanese, etc.) cause crashes. ALWAYS use `apply-inline` command to update translations.

## Overview

This project uses `scripts/translation-helper.ts` for i18n management. English (`locales/en/`) is the source of truth. All translations are stored as JSON files in `locales/{locale}/`.

## Translation Helper Commands

### Check Translation Status

```bash
# Show statistics for a locale
yarn i18n:stats de
yarn i18n:stats es

# See what needs translation (human-readable)
yarn i18n:diff de

# Machine-readable diff for programmatic use
yarn i18n:helper diff-json de
```

### Get Work Batches

```bash
# Get 20 entries needing translation
yarn i18n:batch de interactive-tools.json 20

# Get next batch (with offset)
yarn i18n:batch de interactive-tools.json 20 20
```

Returns JSON with:

- `entries[]` - Array of `{key, english}` pairs
- `totalRemaining` - How many entries still need translation
- `batchNumber` / `totalBatches` - Progress tracking

### Apply Translations

```bash
# Apply from inline JSON (preferred for LLM workflow)
yarn i18n:helper apply-inline de interactive-tools.json '[{"key":"pages[0].title","value":"Translated title"}]'

# Apply from batch file
yarn i18n:helper apply de ./translations.json
```

### Maintenance Commands

```bash
# Add missing keys from English (syncs structure)
yarn i18n:helper sync de

# Validate JSON structure
yarn i18n:helper validate de

# List all translation files
yarn i18n:helper list-files de
```

## LLM Translation Workflow

1. **Get a batch**: `yarn i18n:batch de {file} 20 {offset}`
2. **Translate entries**: Provide the English text and request translations
3. **Apply immediately**: `yarn i18n:helper apply-inline de {file} '{json}'`
4. **Repeat**: Increase offset by batch size until complete

Example batch output:

```json
{
  "locale": "de",
  "file": "interactive-tools.json",
  "batchNumber": 1,
  "totalBatches": 58,
  "totalRemaining": 1159,
  "entries": [
    { "key": "category", "english": "Tools" },
    { "key": "pages[0].slug", "english": "image-resizer" }
  ],
  "responseFormat": {
    "description": "Return a JSON array of objects with \"key\" and \"value\" fields"
  }
}
```

## File Structure

```
locales/
├── en/                    # Source of truth
│   ├── interactive-tools.json
│   ├── formats.json
│   └── ...
├── de/                    # German
├── es/                    # Spanish
├── fr/                    # French
├── it/                    # Italian
├── ja/                    # Japanese
└── pt/                    # Portuguese
```

## Key Notation

Nested keys use dot/bracket notation:

- `category` → Top-level key
- `pages[0].title` → First array element, then `title` property
- `pages[0].features[0].title` → Nested array access

## Translation Quality Guidelines

1. **Preserve meaning over literal translation** - Localize appropriately
2. **Keep placeholders intact** - `{variable}`, `%s`, etc.
3. **Maintain tone** - Marketing copy vs. UI text vs. technical docs
4. **Handle technical terms** - Keep brand names, product names, URLs unchanged
5. **Array consistency** - If English has 5 items, translation should too

## Common Issues

### JSON Parse Errors

```bash
# Validate files to find syntax errors
yarn i18n:helper validate de
```

### Missing Keys After English Update

```bash
# Sync adds new keys from English to target locale
yarn i18n:helper sync de
```

### Untranslated Entries (Same as English)

The script treats values identical to English as "untranslated" - review these to ensure they're correctly localized.

## Package Scripts

| Script             | Command                             |
| ------------------ | ----------------------------------- |
| `yarn i18n:stats`  | Show translation statistics         |
| `yarn i18n:diff`   | Show missing/untranslated entries   |
| `yarn i18n:batch`  | Get a batch of entries to translate |
| `yarn i18n:helper` | Direct access to all commands       |
| `yarn i18n:check`  | Run translation validation checks   |
