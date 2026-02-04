---
name: get-source-languages
description: Fetch source language (Greek/Hebrew) word data for Bible verses. Use this when users want to study Greek or Hebrew words, understand original language meanings, or analyze source text morphology. The skill retrieves Macula source language data and merges it with Strong's dictionary entries to provide comprehensive linguistic information. Also supports direct Strong's number lookups and English word searches across all Greek/Hebrew lexicon entries.
---

# Get Source Languages

## Overview

Retrieve detailed source language (Greek/Hebrew) data for Bible verses, including original text, morphology, Strong's dictionary entries, and semantic information. This skill combines Macula linguistic datasets with Strong's dictionary to provide comprehensive word-level analysis.

**New:** Also supports direct Strong's number lookups and searching for English words to find all Greek and Hebrew variants (e.g., search "love" to find G0025, G5368, H0157).

## Data Repository Setup

This skill requires the **mybibletoolbox-data** repository for Strong's dictionary data.

### Auto-Clone Bible Data

Before using this skill, check if bible data exists. If not, auto-clone it:

```bash
# Check if bible data exists
if [ ! -d "data" ]; then
  echo "Bible data not found. Cloning mybibletoolbox-data..."
  git clone https://github.com/authenticwalk/mybibletoolbox-data data
  echo "✓ Bible data ready"
fi
```

**Expected location:** `data/bible/words/strongs/`

**What it contains:**
- 14,197 Strong's dictionary entries (Greek + Hebrew)
- Full bible data repository (2.6GB)
- Use sparse checkout for minimal footprint (see setup-sparse-checkout.sh)

**Note:** Scripts have been updated to use the new `data/bible/` location.

## When to Use

Use this skill when:
- User wants to study Greek or Hebrew words in a verse
- User asks about original language meanings or etymology
- User needs morphological analysis (tense, case, gender, etc.)
- User is doing word studies or comparative analysis
- User mentions "Greek", "Hebrew", "original language", "source text", or "Strong's"
- User asks about a Strong's number directly (e.g., "What is G0025?")
- User asks about English words and their Greek/Hebrew equivalents (e.g., "Greek words for love")

Do NOT use this skill when:
- User only wants English translations (use quote-bible skill)
- User is doing topical study without language focus
- User needs commentary rather than linguistic data

## How to Use

There are two main modes: **verse-based lookup** and **Strong's number/word lookup**.

### Mode A: Verse-Based Lookup

Use when analyzing a specific Bible verse.

#### Step 1: Parse the Bible Reference

Extract the Bible reference from the user's request. The reference must use USFM 3.0 three-letter codes:
- **Book code**: Use USFM 3.0 (e.g., "JHN", "GEN", "MAT")
- **Chapter:Verse format**: "JHN 3:16", "GEN 1:1"

#### Step 2: Execute the Source Languages Fetcher

Use the Bash tool to execute the fetcher script:

```bash
python3 /home/user/context-grounded-bible/src/lib/source_languages_fetcher.py "<reference>"
```

Where `<reference>` is the verse reference:
- "JHN 3:16" (John 3:16)
- "GEN 1:1" (Genesis 1:1)
- "ROM 8:28" (Romans 8:28)

#### Step 3: Display Results

The script returns YAML data containing:
- **verse**: Verse reference
- **language**: Source language (heb/grc)
- **text**: Original language text
- **words**: Array of word objects with:
  - `text`: Original language word
  - `lemma`: Dictionary form
  - `morphology`: Grammatical properties (pos, case, tense, gender, number, etc.)
  - `translation`: English gloss
  - `strongs_data`: Full Strong's dictionary entry merged from all sources
  - `lexical`: Strong's number references
  - `semantic`: Semantic domain information

Present the information clearly to the user, highlighting:
- Original text with transliteration
- Strong's numbers and definitions
- Morphological information relevant to their question
- English glosses for understanding

#### Options

Optional flags:
- `--output <file>`: Save results to a YAML file
- `--json`: Output as JSON instead of YAML
- `--no-generate`: Don't auto-generate Macula data if missing

### Mode B: Strong's Number/Word Lookup

Use when studying specific Strong's numbers or English words.

#### Step 1: Execute get_strongs.py

Use the Bash tool to execute:

**Lookup by Strong's numbers:**
```bash
python3 /home/user/context-grounded-bible/src/lib/get_strongs.py G0025 G5368 H0157
```

**Search by English word:**
```bash
python3 /home/user/context-grounded-bible/src/lib/get_strongs.py --word love
```

**Search multiple words:**
```bash
python3 /home/user/context-grounded-bible/src/lib/get_strongs.py --word love --word beloved
```

**Combined:**
```bash
python3 /home/user/context-grounded-bible/src/lib/get_strongs.py G0025 --word love
```

#### Step 2: Display Results

The script returns YAML data structured as:
```yaml
words:
  G0025:
    strongs_number: G0025
    language: greek
    lemma: ἀγαπάω
    transliteration: agapáō
    definition: to love (in a social or moral sense)
    kjv_usage: (be-)love(-ed)
    derivation: ...
  G5368:
    strongs_number: G5368
    ...
```

Present the information clearly, highlighting:
- All Greek and Hebrew variants found
- Differences in meaning between similar words
- KJV usage patterns
- Etymological relationships

#### Options

Optional flags:
- `--output <file>`: Save results to a YAML file
- `--json`: Output as JSON instead of YAML
- `--case-sensitive`: Make word search case-sensitive

## Examples

### Verse-Based Examples

#### Example 1: Study Greek Words in John 3:16

**User:** "What are the Greek words in John 3:16?"

**Action:** Execute:
```bash
python3 /home/user/context-grounded-bible/src/lib/source_languages_fetcher.py "JHN 3:16"
```

**Expected behavior:** Display each Greek word with lemma, morphology, and Strong's definition

#### Example 2: Hebrew Word Study

**User:** "I want to study the Hebrew words in Genesis 1:1"

**Action:** Execute:
```bash
python3 /home/user/context-grounded-bible/src/lib/source_languages_fetcher.py "GEN 1:1"
```

**Expected behavior:** Display Hebrew text with transliteration, morphology, and Strong's entries

#### Example 3: Verse Analysis

**User:** "What does the Greek word in Romans 8:28 mean?"

**Action:** Execute:
```bash
python3 /home/user/context-grounded-bible/src/lib/source_languages_fetcher.py "ROM 8:28"
```

**Expected behavior:** Display all Greek words with Strong's definitions and usage information

### Strong's Lookup Examples

#### Example 4: Look Up Specific Strong's Numbers

**User:** "What is G0025?"

**Action:** Execute:
```bash
python3 /home/user/context-grounded-bible/src/lib/get_strongs.py G0025
```

**Expected behavior:** Display full Strong's entry for G0025 (ἀγαπάω - agape love)

#### Example 5: Compare Greek Words for Love

**User:** "What are the different Greek words for love?"

**Action:** Execute:
```bash
python3 /home/user/context-grounded-bible/src/lib/get_strongs.py --word love
```

**Expected behavior:** Display all Greek and Hebrew Strong's entries containing "love", showing G0025 (ἀγαπάω), G5368 (φιλέω), H0157 (אָהַב), etc. with their distinct meanings

#### Example 6: Study Word Family

**User:** "Show me the Greek words for believe and faith"

**Action:** Execute:
```bash
python3 /home/user/context-grounded-bible/src/lib/get_strongs.py --word believe --word faith
```

**Expected behavior:** Display entries like G4100 (πιστεύω - believe), G4102 (πίστις - faith), showing etymological relationships

#### Example 7: Combined Lookup

**User:** "I want to study agape love specifically, plus see all love words"

**Action:** Execute:
```bash
python3 /home/user/context-grounded-bible/src/lib/get_strongs.py G0025 --word love
```

**Expected behavior:** Display G0025 and all other love-related entries from both Greek and Hebrew

## Technical Details

### Data Sources

The skill combines data from:
1. **Macula Project**: Morphologically analyzed Hebrew (WLC) and Greek (Nestle 1904) texts
   - Location: `./bible/commentaries/{BOOK}/{chapter}/{verse}/{BOOK}-{chapter}-{verse}-macula.yaml`
   - Contains: Original text, lemmas, morphology, syntax, semantic domains

2. **Strong's Dictionary**: Hebrew and Greek lexicon entries
   - Location: `./bible/words/strongs/{STRONG_NUMBER}/`
   - Contains: Lemma, definition, KJV usage, derivation, transliteration

### Auto-Generation

If Macula data doesn't exist for a verse, the script automatically:
1. Calls `macula_processor.py --verse "<reference>"`
2. Generates the macula.yaml file from cached XML datasets
3. Returns the newly generated data

This requires that Macula datasets have been downloaded via `macula_fetcher.py`.

### Data Merging

The skill uses `yaml_merger.py` to merge multiple YAML files:
- All files in a Strong's number directory are merged
- Nested merge preserves structure
- String values are concatenated if different
- Lists are extended

## Error Handling

If the script fails:
1. **"Macula data not found"**: Run `python3 src/lib/macula/macula_fetcher.py` first to download datasets
2. **"Strong's entry not found"**: Run `python3 strongs-fetcher.py` to download Strong's dictionary
3. **"Invalid verse reference"**: Check reference format (BOOK CHAPTER:VERSE)

## Integration with Tool Ecosystem

When the `tool-experimenter` skill is improving Bible study tools, it should consider this skill as an option if the tool:
- Deals with source language data
- Needs Strong's definitions
- Requires morphological analysis
- Works with Hebrew or Greek text

## Notes

- Greek text uses Unicode (polytonic Greek)
- Hebrew text uses Unicode (Hebrew with vowel points)
- Strong's numbers follow format: G0001-G5624 (Greek), H0001-H8674 (Hebrew)
- Morphology codes follow standard linguistic conventions (see Macula documentation)
