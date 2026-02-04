---
name: scripture-study
description: Study scripture by retrieving and merging all available commentary data for one or more verses. Supports verse ranges, depth levels (light/medium/full), and optional filtering by tool type.
---

# Scripture Study

## Overview

Retrieve and merge all available commentary data for Bible verses to enable comprehensive scripture study. This skill aggregates YAML commentary files from various Bible study tools, providing a unified view of lexical, theological, historical, and practical insights.

## Data Repository Setup

This skill requires the **mybibletoolbox-data** repository for verse commentary data.

### Auto-Clone Commentary Data

Before using this skill, check if data exists for the requested book(s). If not, auto-clone with sparse checkout:

```bash
# Function to ensure book data is available
ensure_book_data() {
  local BOOK=$1  # e.g., "MAT", "JHN", "ROM"

  # Check if data repo exists
  if [ ! -d "data" ]; then
    echo "Data not found. Cloning mybibletoolbox-data with sparse checkout..."
    git clone --filter=blob:none --sparse https://github.com/authenticwalk/mybibletoolbox-data data
    cd data
    git sparse-checkout init --cone
    git sparse-checkout set bible/${BOOK}
    cd ..
    echo "✓ Data ready for ${BOOK}"
  else
    # Check if specific book is available
    if [ ! -d "data/bible/${BOOK}" ]; then
      echo "Adding ${BOOK} to sparse checkout..."
      cd data
      git sparse-checkout add bible/${BOOK}
      cd ..
      echo "✓ ${BOOK} added"
    fi
  fi
}

# Example: For studying Matthew 5:3-10
ensure_book_data "MAT"
```

**Expected location:**
- `data/bible/{BOOK}/` - All verse data for book

**Sparse checkout strategy:**
- **Single book study**: Clone only that book
- **Multiple books**: Add books as needed with `git sparse-checkout add`
- **Sermon series**: Clone all needed books upfront

## When to Use

Use this skill when:
- User wants to study a specific verse or passage
- User asks for "all available data" or "commentary" on a verse
- User needs comprehensive verse analysis
- User mentions studying scripture, doing research, or preparing teaching materials
- User specifies a verse reference with depth or detail requirements

Do NOT use this skill when:
- User only wants to quote/display the verse text (use quote-bible skill)
- User wants to study source languages specifically (use get-source-languages skill)
- User is creating new commentary data (use appropriate tool-specific skills)

## How to Use

### Step 1: Parse the Bible Reference

Extract verse reference(s) from the user's request. References must use USFM 3.0 three-letter codes:

**Formats supported:**
- Single verse: "JHN 3:16", "GEN 1:1", "MAT 5:3"
- Verse range: "MAT 5:3-10", "JHN 1:1-5"
- Multiple verses: "JHN 3:16 JHN 3:17 JHN 3:18"
- Chapter: "MAT 5" (all verses in chapter 5)

**Book codes:** USFM 3.0 standard (MAT, JHN, GEN, ROM, PSA, etc.)

### Step 2: Determine Depth Level

Identify the depth level from the user's request or default to "medium":

**Depth levels:**
- `light`: Core files only (essential commentary, translations, key insights)
- `medium`: Core files + verse-level tools (default)
- `full`: All available data including chapter-level and book-level context

**Determining depth from user intent:**
- "Quick overview", "summary", "brief": → `light`
- "Study", "analysis", "research": → `medium`
- "Comprehensive", "everything", "all data", "deep dive": → `full`

### Step 3: Execute the Scripture Study Script

Use the Bash tool to execute:

```bash
python3 /home/user/context-grounded-bible/src/lib/scripture_study.py "BOOK CHAPTER:VERSE" --depth <level>
```

**Examples:**

Single verse with default depth:
```bash
python3 /home/user/context-grounded-bible/src/lib/scripture_study.py "JHN 3:16"
```

Verse range with full depth:
```bash
python3 /home/user/context-grounded-bible/src/lib/scripture_study.py "MAT 5:3-10" --depth full
```

Multiple verses:
```bash
python3 /home/user/context-grounded-bible/src/lib/scripture_study.py "JHN 3:16 JHN 3:17"
```

Filter by tool type:
```bash
python3 /home/user/context-grounded-bible/src/lib/scripture_study.py "JHN 3:16" --filter sermon-illustrations
```

### Step 4: Display Results

The script returns merged YAML data containing all available commentary organized by verse. Present the information clearly to the user:

**For single verse:**
- Show available commentary categories
- Highlight key insights relevant to their question
- Note data sources and citation information

**For verse ranges:**
- Present verse-by-verse breakdown
- Identify common themes across verses
- Summarize key patterns or progressions

**For comprehensive study:**
- Overview of all available data types
- Key theological, lexical, and practical insights
- Cross-references and related topics

## Options and Parameters

### Required Parameters

- `reference`: Verse reference in USFM 3.0 format (BOOK CHAPTER:VERSE)

### Optional Parameters

- `--depth <level>`: Depth level (light|medium|full) - default: medium
- `--filter <tool>`: Include only specific tool types (can specify multiple)
- `--exclude <tool>`: Exclude specific tool types (can specify multiple)
- `--output <file>`: Save results to YAML file
- `--json`: Output as JSON instead of YAML
- `--list-tools`: Show available tools for the verse(s)

### Filter Options

Use `--filter` to focus on specific commentary types:

```bash
# Only sermon illustrations
--filter sermon-illustrations

# Only source language data
--filter original-language-words

# Multiple filters
--filter sermon-illustrations --filter translations
```

Use `--exclude` to omit specific types:

```bash
# Exclude translations (often very large)
--exclude translations-ebible
```

## Examples

### Example 1: Quick Overview

**User:** "Give me a quick overview of John 3:16"

**Action:** Execute:
```bash
python3 /home/user/context-grounded-bible/src/lib/scripture_study.py "JHN 3:16" --depth light
```

**Expected behavior:** Returns core commentary with essential insights, avoiding overwhelming detail

### Example 2: Verse Range Study

**User:** "I want to study the Beatitudes in Matthew 5"

**Action:** Execute:
```bash
python3 /home/user/context-grounded-bible/src/lib/scripture_study.py "MAT 5:3-12" --depth medium
```

**Expected behavior:** Returns verse-by-verse commentary for each Beatitude with moderate detail

### Example 3: Comprehensive Analysis

**User:** "Give me everything you have on Genesis 1:1"

**Action:** Execute:
```bash
python3 /home/user/context-grounded-bible/src/lib/scripture_study.py "GEN 1:1" --depth full
```

**Expected behavior:** Returns all available commentary including chapter and book-level context

### Example 4: Sermon Preparation

**User:** "I'm preaching on Romans 8:28, show me sermon illustrations"

**Action:** Execute:
```bash
python3 /home/user/context-grounded-bible/src/lib/scripture_study.py "ROM 8:28" --filter sermon-illustrations
```

**Expected behavior:** Returns only sermon illustration data for targeted preparation

### Example 5: Multiple Verses

**User:** "Compare John 3:16, Romans 5:8, and 1 John 4:8"

**Action:** Execute:
```bash
python3 /home/user/context-grounded-bible/src/lib/scripture_study.py "JHN 3:16 ROM 5:8 1JN 4:8"
```

**Expected behavior:** Returns commentary for all three verses, enabling comparison

## Technical Details

### Data Sources

The skill aggregates data from:
- **Commentary files:** `./bible/commentary/{BOOK}/{chapter:03d}/{BOOK}.{chapter:03d}.{verse:03d}-{tool}.yaml`
- **Chapter-level files:** `./bible/commentary/{BOOK}/{chapter:03d}/{BOOK}.{chapter:03d}-{tool}.yaml`
- **Book-level files:** `./bible/commentary/{BOOK}/{BOOK}-{tool}.yaml`

### Depth Filtering

**Light depth includes:**
- Tools with scope: core
- Essential data only (~1-50 KB per verse)
- Examples: sermon-illustrations, cross-references

**Medium depth includes:**
- Tools with scope: core + standard
- Standard research depth (~50-500 KB per verse)
- Examples: core tools + word-studies, historical-context, semantic-clusters

**Full depth includes:**
- Tools with scope: core + standard + comprehensive
- Exhaustive reference data (>500 KB per verse)
- Examples: medium tools + all-translations, complete-lexicon

### Tool Registry

The script reads from `bible-study-tools/tool-registry.yaml` to determine:
- Available tool types
- Tool file suffixes
- Scope levels (core/standard/comprehensive)
- Which tools should be included at each depth level

**Scope Mapping:**
- `core`: Always included (light, medium, full queries)
- `standard`: Included in medium and full queries only
- `comprehensive`: Included in full queries only

### Data Merging

Uses `yaml_merger.py` to merge multiple YAML files:
- Nested merge preserves structure
- String values are concatenated if different
- Lists are extended
- Citations are preserved

## Error Handling

If the script fails:
1. **"No commentary found"**: No data exists for this verse yet
2. **"Invalid verse reference"**: Check reference format (BOOK CHAPTER:VERSE)
3. **"Tool not found"**: Specified filter tool doesn't exist (use --list-tools)
4. **"File not readable"**: YAML syntax error in source file (report issue)

## Integration with Tool Ecosystem

### For Tool Creators

When creating new Bible study tools with `bible-study-tool-creator`:
- Register your tool in `bible-study-tools/tool-registry.yaml`
- Specify scope level:
  - `core`: Essential data, always included (<50 KB)
  - `standard`: Standard research depth (50-500 KB) - most tools
  - `comprehensive`: Exhaustive reference (>500 KB)
- Use standard file naming: `{BOOK}_{chapter}_{verse:03d}.{tool-suffix}.yaml`

### For Tool Experimenters

When using `tool-experimenter` to improve tools:
- Consider how your tool fits into the depth hierarchy
- Test output size to determine appropriate scope level
- Update tool registry with final scope after experimentation
- Ensure YAML structure is compatible with merging

## Notes

- Verse references use USFM 3.0 book codes (MAT, JHN, GEN, etc.)
- Chapter and verse numbers are zero-padded in file paths (001, 005, 016)
- YAML format ensures both human and AI readability
- Citations are preserved through merging for full traceability
- Empty results indicate no commentary has been generated yet for that verse

## Version History

### Version 1.0.0 (2025-10-30)
- Initial creation
- Supports single verses, ranges, and multiple verses
- Three depth levels (light/medium/full)
- Filter and exclude options
- Tool registry integration
