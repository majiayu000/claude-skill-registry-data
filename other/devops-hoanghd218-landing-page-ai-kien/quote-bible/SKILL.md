---
name: quote-bible
description: Fetch and display Bible verses in multiple translations with optional language filtering. Use when users explicitly request to quote a specific verse (e.g., "quote John 3:16" or "quote Matthew 5:3"). The skill retrieves verses from BibleHub and eBible corpus (1000+ translations) using STANDARDIZATION.md format with language filtering support.
---

# Quote Bible

## Overview

Retrieve and display Bible verses from BibleHub and eBible corpus with optional language filtering. The skill executes a Python script that fetches verse data in standardized format and presents it in clear, formatted output. Supports 1000+ translations across hundreds of languages.

## Data Sources

This skill fetches verses from two sources:

1. **BibleHub** (https://biblehub.com): ~67 major translations (fetched via web)
2. **eBible corpus**: 1000+ translations pre-processed as YAML files in `.data/commentary`

The eBible data is already processed and stored in the `.data` git repository. If a verse is not available in your sparse checkout, add the chapter using:
```bash
cd .data && git sparse-checkout add commentary/{BOOK}/{chapter:03d}
# Example: cd .data && git sparse-checkout add commentary/NAM/001
```

## When to Use

Use this skill when:
- User explicitly says "quote" followed by a Bible reference
- Examples: "quote John 3:16", "quote Gen 1:1", "quote Matthew 5:3"
- User wants to see a verse in specific languages (e.g., "quote John 3:16 in English and Spanish")

Do NOT use this skill when:
- User is asking about a Bible verse without requesting a quote
- User is performing translation work (use other specialized skills)
- User is searching for a verse by topic or content (use search tools)
- User wants verse ranges (single verses only currently supported)

## How to Use

### Step 1: Parse the Bible Reference

Extract the Bible reference from the user's request. The reference format follows STANDARDIZATION.md:
- **Book code**: USFM 3.0 three-letter codes (e.g., "JHN" for John, "GEN" for Genesis, "MAT" for Matthew)
  - Common book names must be converted to USFM codes (e.g., "John" → "JHN", "Genesis" → "GEN")
  - See `scripts/book_codes.py` for complete mapping
- **Chapter number**: The chapter number
- **Verse number**: Single verse only (ranges not currently supported)

### Step 2: Determine Language Filter (Optional)

If user specifies languages, determine ISO-639-3 codes:
- English → `eng`
- Spanish → `spa`
- French → `fra`
- Greek (Ancient) → `grc`
- Hebrew → `heb`

See STANDARDIZATION.md for complete ISO-639-3 language code list.

### Step 3: Execute the Fetch Script

Use the script from the project root:

```bash
# All languages (1000+ translations)
python3 src/tools/fetch_verse.py "MAT-005-003"

# English only
python3 src/tools/fetch_verse.py "JHN 3:16" --lang eng

# Multiple languages
python3 src/tools/fetch_verse.py "GEN 1:1" --lang eng,spa,fra

# Original languages only
python3 src/tools/fetch_verse.py "ROM 8:28" -l grc,heb
```

**Supported formats:**
- Standardized: `MAT-005-003` (recommended, per STANDARDIZATION.md)
- Convenience: `"JHN 3:16"`, `GEN.1.1` (also accepted)

**Language filtering:**
- No flag: Returns all available translations
- `--lang` / `-l`: Filter by comma-separated ISO-639-3 codes
- `--all`: Override any filtering (fetch everything)

### Step 4: Display Results

Present the output from the fetch script. The script returns JSON with translation codes as keys and verse text as values.

Format the output clearly:
- Include the verse reference
- Show translation count (printed to stderr by script)
- Show each translation with its version identifier
- Translation codes follow STANDARDIZATION.md format: `{lang}-{version}` or `{lang}-{version}-{year}`

## Examples

### Example 1: Single Verse (All Languages)

**User:** "quote John 3:16"

**Action:** Convert "John" to USFM code "JHN", then execute:
```bash
python3 src/tools/fetch_verse.py "JHN 3:16"
```

**Expected behavior:** Display John 3:16 in 1000+ translations from all languages

### Example 2: Single Language Filter

**User:** "quote Matthew 5:3 in English"

**Action:** Convert "Matthew" to USFM code "MAT", use `eng` language code:
```bash
python3 src/tools/fetch_verse.py "MAT 5:3" --lang eng
```

**Expected behavior:** Display Matthew 5:3 in English translations only (~50 versions)

### Example 3: Multiple Languages

**User:** "quote Genesis 1:1 in English, Spanish, and French"

**Action:** Convert "Genesis" to USFM code "GEN", use multiple language codes:
```bash
python3 src/tools/fetch_verse.py "GEN 1:1" --lang eng,spa,fra
```

**Expected behavior:** Display Genesis 1:1 in English, Spanish, and French translations

### Example 4: Original Languages

**User:** "quote Romans 8:28 in the original languages"

**Action:** Convert "Romans" to USFM code "ROM", use Greek and Hebrew codes:
```bash
python3 src/tools/fetch_verse.py "ROM 8:28" -l grc,heb
```

**Expected behavior:** Display Romans 8:28 in Greek (and Hebrew if available for NT context)

### Example 5: Standardized Format

**User:** "quote Matthew 5:3"

**Action:** Convert to standardized format with zero-padding:
```bash
python3 src/tools/fetch_verse.py "MAT-005-003"
```

**Expected behavior:** Display Matthew 5:3 in all available translations (using STANDARDIZATION.md format)

## Notes

- **Data sources**: Combines BibleHub (~67 translations via web) + eBible corpus (1000+ translations from `.data/commentary`)
- **eBible data**: Pre-processed as YAML files in `.data/commentary/{BOOK}/{chapter:03d}/{verse:03d}/{BOOK}-{chapter:03d}-{verse:03d}-translations-ebible.yaml`
- **Sparse checkout**: If a verse is missing, add the chapter to sparse checkout:
  ```bash
  cd .data && git sparse-checkout add commentary/{BOOK}/{chapter:03d}
  ```
- **Performance**: Fast lookups - eBible data is read from pre-processed YAML, not raw corpus files
- **Language filtering**: Use `--lang` to filter by ISO-639-3 codes (e.g., `--lang eng,spa,fra`)
- **Format flexibility**: Script accepts multiple formats (MAT-005-003, "JHN 3:16", GEN.1.1)

If the script returns an error, check:
- The reference format is valid (USFM 3.0 book codes)
- The verse exists in the Bible
- Network access is available (for first-time BibleHub fetch)
- Language codes are valid ISO-639-3 codes

## Resources

### scripts/

- `fetch_verse.py` - Main verse fetcher with language filtering
- `book_codes.py` - USFM 3.0 book code mappings and reference parser
- `biblehub_fetcher.py` - BibleHub integration

### Project Documentation

- `STANDARDIZATION.md` - Verse reference format, language codes, and citation standards
- `SCHEMA.md` - Data structure and citation requirements
- `ATTRIBUTION.md` - Source credits and citation codes
