---
name: chinese-zotero-import
description: Import Chinese language works into Zotero with proper pinyin transliteration and translations following Chicago style guidelines
---

# Chinese to Zotero Import Skill

This skill helps you create properly formatted Zotero entries for Chinese language sources, following Chicago Manual of Style guidelines for Chinese, Japanese, and Korean languages (Sections 11.89-99).

## When to Use This Skill

Use this skill when the user provides:
- A Chinese bibliography reference that needs to be imported into Zotero
- A PDF of a Chinese document (government document, journal article, book, web resource)
- Chinese metadata that needs proper transliteration and formatting

## Chicago Style Requirements for Chinese Sources

According to Chicago style, citations should include:
1. **Transliteration** (REQUIRED): Pinyin transliteration using Library of Congress Romanization practices
2. **Original Chinese characters** (OPTIONAL): Included after the transliteration
3. **English translation** (RECOMMENDED): In square brackets after the Chinese characters

### Example Chicago Citation Format

```
Hua Linfu 華林甫. "Qingdai yilai Sanxia diqu shuihan zaihai de chubu yanjiu" 清代以來三峽地區水旱災害的初步硏究 [A preliminary study of floods and droughts in the Three Gorges region since the Qing dynasty]. Zhongguo shehui kexue 中國社會科學 1 (1999): 168–79.
```

## Field Format Convention

For RIS entries, combine transliteration, Chinese characters, and translation in each field:

- **Author**: `[Transliteration] [Chinese characters]`
  - Example: `Hua, Linfu 華林甫`

- **Title**: `[Transliteration] [Chinese characters] [English translation in brackets]`
  - Example: `Qingdai yilai Sanxia diqu shuihan zaihai de chubu yanjiu 清代以來三峽地區水旱災害的初步硏究 [A preliminary study of floods and droughts in the Three Gorges region since the Qing dynasty]`

- **Journal/Publisher**: `[Transliteration] [Chinese characters]`
  - Example: `Zhongguo shehui kexue 中國社會科學`

## Workflow

### Step 1: Extract Metadata

When the user provides a Chinese reference or PDF:

1. Extract or request the following metadata:
   - **Author(s)** (Chinese characters)
   - **Title** (Chinese characters)
   - **Publication type** (journal article, book, government document, web resource, etc.)
   - **Journal/Publisher name** (if applicable, in Chinese)
   - **Date/Year**
   - **Volume, Issue, Pages** (for articles)
   - **URL** (for web resources)
   - **DOI** (if available)

2. If reading a PDF, extract text and identify key metadata fields

### Step 2: Generate Pinyin Transliterations

For each Chinese text field (author, title, journal name):

1. Generate pinyin transliteration following these rules:
   - Use proper pinyin romanization with tone marks or numbers removed
   - Capitalize proper nouns and first word of titles
   - Use spaces appropriately between words/syllables
   - Follow Library of Congress Romanization practices

2. Present transliterations to the user for verification

### Step 3: Request English Translations

For titles and other important fields:

1. Either generate or request English translations
2. Translations should be concise and descriptive
3. Present to user for confirmation

### Step 4: Create RIS File

Generate a properly formatted RIS file with the following structure:

#### For Journal Articles:

```
TY  - JOUR
AU  - [Last, First (transliteration)] [Chinese characters]
TI  - [Title (transliteration)] [Chinese characters] [English translation in brackets]
T2  - [Journal name (transliteration)] [Chinese characters]
PY  - [Year]
VL  - [Volume]
IS  - [Issue]
SP  - [Start page]
EP  - [End page]
UR  - [URL if available]
DO  - [DOI if available]
ER  -
```

#### For Books:

```
TY  - BOOK
AU  - [Last, First (transliteration)] [Chinese characters]
TI  - [Title (transliteration)] [Chinese characters] [English translation in brackets]
PB  - [Publisher (transliteration)] [Chinese characters]
CY  - [City]
PY  - [Year]
UR  - [URL if available]
ER  -
```

#### For Government Documents:

```
TY  - RPRT
AU  - [Author/Agency (transliteration)] [Chinese characters]
TI  - [Title (transliteration)] [Chinese characters] [English translation in brackets]
PB  - [Publisher/Agency (transliteration)] [Chinese characters]
CY  - [City]
PY  - [Year]
UR  - [URL if available]
ER  -
```

#### For Web Resources:

```
TY  - ELEC
AU  - [Author (transliteration)] [Chinese characters] (if available)
TI  - [Title (transliteration)] [Chinese characters] [English translation in brackets]
PB  - [Website name (transliteration)] [Chinese characters]
PY  - [Year]
UR  - [URL]
DA  - [Access date, format: YYYY/MM/DD]
ER  -
```

### Step 5: Save and Present

1. Save the RIS file with a descriptive filename based on the author/title
2. Present the RIS content to the user for review
3. Offer to open the file in BBEdit for editing
4. Provide instructions for importing into Zotero

## RIS Field Reference

Common RIS fields used for Chinese sources:

- `TY` - Type of reference (JOUR=journal, BOOK=book, RPRT=report, ELEC=electronic/web)
- `AU` - Author (Last, First format with transliteration + Chinese characters)
- `TI` - Title (transliteration + Chinese characters + [English translation])
- `T2` - Secondary title/Journal name (transliteration + Chinese characters)
- `PB` - Publisher (transliteration + Chinese characters)
- `CY` - City of publication
- `PY` - Publication year
- `VL` - Volume
- `IS` - Issue
- `SP` - Start page
- `EP` - End page
- `UR` - URL
- `DO` - DOI
- `DA` - Access date (for web resources)
- `ER` - End of reference (required)

## Pinyin Transliteration Guidelines

Follow Library of Congress Romanization for Chinese:

1. **Capitalization:**
   - Capitalize the first word of titles
   - Capitalize proper nouns (names, places)
   - Keep other words lowercase

2. **Spacing:**
   - Separate words logically
   - Personal names: Given name and surname as separate words
   - Compound words: Use judgment for readability

3. **Tone marks:**
   - Generally omit tone marks in bibliographic references
   - Use plain vowels without diacritics

4. **Special cases:**
   - Place names: Use official romanizations when available
   - Personal names: Verify preferred romanization if known

## Example Workflow

**User provides:**
```
華林甫, "清代以來三峽地區水旱災害的初步硏究", 中國社會科學, 1999年第1期, 第168-179頁
```

**Skill generates:**

1. **Extract metadata:**
   - Author: 華林甫
   - Title: 清代以來三峽地區水旱災害的初步硏究
   - Journal: 中國社會科學
   - Year: 1999
   - Issue: 1
   - Pages: 168-179

2. **Generate transliterations:**
   - Author: Hua Linfu
   - Title: Qingdai yilai Sanxia diqu shuihan zaihai de chubu yanjiu
   - Journal: Zhongguo shehui kexue

3. **Request translation:**
   - "A preliminary study of floods and droughts in the Three Gorges region since the Qing dynasty"

4. **Create RIS file:**

```
TY  - JOUR
AU  - Hua, Linfu 華林甫
TI  - Qingdai yilai Sanxia diqu shuihan zaihai de chubu yanjiu 清代以來三峽地區水旱災害的初步硏究 [A preliminary study of floods and droughts in the Three Gorges region since the Qing dynasty]
T2  - Zhongguo shehui kexue 中國社會科學
PY  - 1999
IS  - 1
SP  - 168
EP  - 179
ER  -
```

## Important Notes

- **Always verify transliterations** with the user, especially for proper names
- **Ask for English translations** if you cannot confidently generate them
- **Include Chinese characters** directly in the main fields (AU, TI, T2, PB) alongside transliterations
- **Check for existing metadata** - some Chinese publications include English abstracts or keywords
- **Use URL and DOI** when available to ensure citability
- **For government documents**, identify the issuing agency correctly
- **For web resources**, include access date as these may change or disappear

## Importing into Zotero

After creating the RIS file:

1. Open Zotero
2. Go to File > Import
3. Select the RIS file
4. Choose "Import to Zotero" and select destination collection
5. Review the imported entry and verify all fields are correct

The RIS format ensures that:
- Transliterated names appear in the author field with Chinese characters
- English translations are included with titles
- Original Chinese text is preserved in the same fields
- All bibliographic information is captured correctly
- Chicago style formatting is maintained

## Common Document Types

### Government Documents
- Often lack individual authors; use agency name
- May have complex hierarchical authorship
- URLs are critical as print copies may be rare
- Format: `[Agency transliteration] [Chinese characters]`

### Web Resources
- Always include URL and access date
- Website/publisher name may be important
- Author may be corporate or absent
- Format all fields consistently with transliteration + Chinese

### Journal Articles
- Usually have the most complete metadata
- May already include English title/abstract
- Check for DOI in Chinese databases
- Journal names should include both pinyin and Chinese

### Books
- May have translators or editors
- Publisher location (city) is important
- Edition information may be relevant
- Publisher names need transliteration + Chinese
