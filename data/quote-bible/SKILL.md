---
name: quote-bible
description: Fetch and display Bible verses in multiple translations when users explicitly request to quote a specific verse or passage. This skill should be used when users say "quote" followed by a Bible reference (e.g., "quote John 3:16" or "quote Matthew 5:3-10"). The skill retrieves verses using an external Python script and displays all available translations.
---

# Quote Bible

## Overview

Retrieve and display Bible verses in all available translations using an external fetch script. The skill executes a Python script that fetches verse data and presents it in a clear, formatted output.

## When to Use

Use this skill when:
- User explicitly says "quote" followed by a Bible reference
- Examples: "quote John 3:16", "quote Gen 1:1", "quote Matthew 5:3-10"

Do NOT use this skill when:
- User is asking about a Bible verse without requesting a quote
- User is performing translation work (use other specialized skills)
- User is searching for a verse by topic or content (use search tools)

## How to Use

### Step 1: Parse the Bible Reference

Extract the Bible reference from the user's request. The reference format should be compatible with the fetch script:
- **Book code**: Must use USFM 3.0 three-letter codes (e.g., "JHN" for John, "GEN" for Genesis, "MAT" for Matthew)
  - Refer to `references/book_codes.md` for the complete list of USFM codes
  - Common book names will need to be converted to USFM codes (e.g., "John" → "JHN", "Genesis" → "GEN")
- **Chapter number**: The chapter number
- **Verse number(s)**: Single verse or range (e.g., "3" or "3-10")

### Step 2: Execute the Fetch Script

Use the Bash tool to execute the verse fetcher:

```bash
python3 ~/projects/mcp/bible/fetch_verse.py "<reference>"
```

Where `<reference>` is the Bible reference using USFM 3.0 codes:
- "GEN 1:1" (Genesis 1:1)
- "JHN 3:16" (John 3:16)
- "MAT 5:3-10" (Matthew 5:3-10)

### Step 3: Display Results

Present the output from the fetch script to the user. The script returns all available translations for the requested verse(s).

Format the output clearly:
- Include the verse reference
- Show each translation with its version identifier
- Maintain proper citation format following project standards: `{lang}` → `{lang}-{version}` → `{lang}-{version}-{year}`

## Examples

### Example 1: Single Verse

**User:** "quote John 3:16"

**Action:** Convert "John" to USFM code "JHN", then execute:
```bash
python3 ~/projects/mcp/bible/fetch_verse.py "JHN 3:16"
```

**Expected behavior:** Display John 3:16 in all available translations

### Example 2: Verse Range

**User:** "quote Matthew 5:3-10"

**Action:** Convert "Matthew" to USFM code "MAT", then execute:
```bash
python3 ~/projects/mcp/bible/fetch_verse.py "MAT 5:3-10"
```

**Expected behavior:** Display Matthew 5:3 through 5:10 in all available translations

### Example 3: Using Book Codes

**User:** "quote Gen 1:1"

**Action:** Convert "Gen" to USFM code "GEN", then execute:
```bash
python3 ~/projects/mcp/bible/fetch_verse.py "GEN 1:1"
```

**Expected behavior:** Display Genesis 1:1 in all available translations

## Notes

- The script handles translation and version selection automatically
- If the script returns an error, inform the user and check:
  - The reference format is valid
  - The fetch script is accessible at the specified path
  - The requested verse exists

## Resources

### references/

- `book_codes.md` - Reference guide for Bible book abbreviations and USFM 3.0 codes used in the project

**Note:** The example `scripts/` and `assets/` directories are not needed for this skill and can be deleted.
