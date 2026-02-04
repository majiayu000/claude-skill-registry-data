---
name: dutch-law-downloader
description: Downloads Dutch official legal publications including national laws (wetten, ministeriele regelingen, koninklijk besluiten), local regulations (lokale verordeningen, gemeentelijk beleid), and implementation policies (uitvoeringsbeleid) from government databases (BWB, CVDR) and converts them to YAML format with textual content only. Use when user wants to download, fetch, or import any Dutch regulation by name or type.
allowed-tools: Read, Write, WebFetch, Bash, Grep, Glob
---

# Dutch Law Downloader

Downloads official Dutch legal publications from government sources (national and local) and converts them to the regelrecht YAML format.

## What This Skill Does

1. Searches for Dutch regulations in government databases:
   - **BWB** (Basiswettenbestand) - National laws and regulations
   - **CVDR** (Centrale Voorziening Decentrale Regelgeving) - Local regulations
2. Presents search results with identifiers (BWBR, CVDR) and metadata
3. Downloads the XML from the official repository
4. Parses the XML to extract articles and metadata
5. Converts to YAML format with **text only** (no machine_readable sections)
6. Saves to `regulation/nl/{layer}/{law_id}/{date}.yaml`

## Supported Regulation Types

### National Level (BWB)
- Wetten (formal laws)
- AMvB (Algemene maatregel van bestuur)
- Ministeriele regelingen
- Koninklijk besluiten
- Beleidsregels (implementation policies)

### Local Level (CVDR)
- Gemeentelijke verordeningen (municipal ordinances)
- Provinciale verordeningen (provincial ordinances)
- Waterschapsverordeningen (water board ordinances)
- Uitvoeringsbeleid (implementation policies)

## Important Constraints

- Keep legal text EXACTLY as it appears in the source (preserve all formatting, markdown links)
- Do NOT convert monetary amounts (keep as written: "€795,47" not "79547")
- Do NOT add any machine_readable sections (leave completely empty)
- Extract ALL articles - do not skip any
- Preserve article structure and numbering exactly

## Step-by-Step Instructions

### Step 1: Determine Database to Search

Based on the regulation type, choose the appropriate database:

**For National Regulations:** Use `x-connection=BWB`
- Wetten, AMvB, ministeriele regelingen, koninklijk besluiten, beleidsregels

**For Local Regulations:** Use `x-connection=CVDR`
- Gemeentelijke verordeningen, provinciale verordeningen, uitvoeringsbeleid

**If unclear:** Search both databases and combine results

### Step 2: Search for the Regulation

**API Endpoint (BWB):**
```
http://zoekservice.overheid.nl/sru/Search?operation=searchRetrieve&version=1.2&x-connection=BWB&query={QUERY}&maximumRecords=10
```

**API Endpoint (CVDR):**
```
http://zoekservice.overheid.nl/sru/Search?operation=searchRetrieve&version=1.2&x-connection=CVDR&query={QUERY}&maximumRecords=10
```

**Query Construction:**
- For title: `dcterms.title%20any%20"{name}"`
- For BWBR ID: `dcterms.identifier=={BWBR_ID}`
- For CVDR ID: `dcterms.identifier=={CVDR_ID}`
- For municipality: `overheidcvdr.organisatietype==gemeenten AND dcterms.title%20any%20"{name}"`
- URL encode spaces as `%20`

**Examples:**
```
# Search BWB
http://zoekservice.overheid.nl/sru/Search?operation=searchRetrieve&version=1.2&x-connection=BWB&query=dcterms.title%20any%20"zorgtoeslag"&maximumRecords=10

# Search CVDR for municipal regulations
http://zoekservice.overheid.nl/sru/Search?operation=searchRetrieve&version=1.2&x-connection=CVDR&query=dcterms.title%20any%20"afvalstoffenverordening"&maximumRecords=10

# Search specific municipality
http://zoekservice.overheid.nl/sru/Search?operation=searchRetrieve&version=1.2&x-connection=CVDR&query=overheidcvdr.organisatietype==gemeenten%20AND%20dcterms.creator==Amsterdam%20AND%20dcterms.title%20any%20"afval"&maximumRecords=10
```

### Step 3: Parse Search Results

Extract from the XML response:

**For BWB results:**
- `<dcterms:title>` - Law title
- `<dcterms:identifier>` - BWBR ID (e.g., "BWBR0018451")
- `<dcterms:type>` - Type (wet, AMvB, ministeriele regeling, etc.)
- `<overheidbwb:geldigheidsdatum>` - Effective date

**For CVDR results:**
- `<dcterms:title>` - Regulation title
- `<dcterms:identifier>` - CVDR ID (e.g., "CVDR123456_1")
- `<dcterms:creator>` - Municipality/organization name
- `<overheidcvdr:organisatietype>` - Type (gemeenten, provincies, waterschappen)
- `<dcterms:issued>` - Issue date

Present results to user with format:
```
Found {N} results:

1. {Title}
   ID: {BWBR_ID or CVDR_ID}
   Type: {Type}
   Organization: {Creator} (if CVDR)
   Latest version: {Date}

2. ...
```

Ask user: "Which regulation would you like to download? (Enter number or ID)"

### Step 4: Download XML Files

Once user selects a regulation, download the appropriate XML files:

**For BWB (National) Regulations:**

A. WTI File (Metadata):
```
https://repository.officiele-overheidspublicaties.nl/bwb/{BWBR_ID}/{BWBR_ID}.WTI
```

B. Toestand File (Legal Text):
```
https://repository.officiele-overheidspublicaties.nl/bwb/{BWBR_ID}/{DATE}/xml/{BWBR_ID}_{DATE}.xml
```

**For CVDR (Local) Regulations:**

Download the CVDR XML directly:
```
https://repository.overheid.nl/{CVDR_PATH}/xml/{CVDR_ID}.xml
```

Where CVDR_PATH is extracted from the search results `<gzd:resourceIdentifier>`.

If date not specified by user, use the latest version from search results.

Use WebFetch or Bash with curl to download these files.

### Step 5: Parse Metadata XML

Extract the following from the WTI XML:

**XML Namespaces:**
```xml
xmlns:bwb-dl="http://www.geonovum.nl/bwb-dl/1.0"
```

**Fields to Extract:**
- `<bwb-dl:bwb-id>` → `identifiers.bwb_id`
- `<bwb-dl:soort>` → Map to `regulatory_layer`:
  - "wet" → "WET"
  - "AMvB" → "AMVB"
  - "ministeriele regeling" → "MINISTERIELE_REGELING"
  - "koninklijk besluit" → "KONINKLIJK_BESLUIT"
  - etc.
- `<bwb-dl:citeertitel>` or `<bwb-dl:officiele-titel>` → Use to generate `$id` (slugified)
- First `<bwb-dl:intrekking datum="...">` → `effective_date`
- `<bwb-dl:publicatiedatum>` → `publication_date`

**Generate UUID:**
Use Python uuid4 to generate a new UUID for the `uuid` field.

### Step 6: Parse Legal Text XML for Articles

**XML Namespaces:**
```xml
xmlns:bwb="http://www.overheid.nl/2011/BWB"
```

**Article Structure in XML:**
```xml
<artikel eId="chp_X__art_Y" wId="BWBR..." status="goed">
  <kop>
    <label>Artikel</label>
    <nr status="officieel">Y</nr>
  </kop>
  <lid eId="..." status="goed">
    <lidnr status="officieel">1</lidnr>
    <al>Legal text here...</al>
  </lid>
  <lid>
    <lidnr>2</lidnr>
    <al>More text...</al>
  </lid>
</artikel>
```

**Extraction Logic:**
1. Find all `<artikel>` elements
2. For each article:
   - Extract `<nr>` as article number
   - Collect ALL `<lid>` (paragraphs) and `<al>` (text blocks)
   - Convert to markdown format:
     - Keep paragraph structure
     - Convert `<nadruk>` to **bold** or *italic*
     - Convert `<extref>` to markdown links `[text](url)`
   - Preserve exact formatting and line breaks
3. Generate article URL:
   ```
   https://wetten.overheid.nl/{BWBR_ID}/{DATE}#Artikel{NUMBER}
   ```

### Step 7: Generate YAML File

**Target Structure:**
```yaml
$schema: https://raw.githubusercontent.com/MinBZK/poc-machine-law/refs/heads/main/schema/v0.2.0/schema.json
$id: "{slugified_title}"
uuid: {generated_uuid}
regulatory_layer: "{MAPPED_LAYER}"
publication_date: "{YYYY-MM-DD}"
effective_date: "{YYYY-MM-DD}"

identifiers:
  bwb_id: "{BWBR_ID}"
  url: "https://wetten.overheid.nl/{BWBR_ID}/{DATE}"

articles:
  - number: "{ARTICLE_NUMBER}"
    text: |
      {MARKDOWN_TEXT}
    url: "https://wetten.overheid.nl/{BWBR_ID}/{DATE}#Artikel{NUMBER}"
  - number: "{NEXT_ARTICLE}"
    text: |
      {MORE_TEXT}
    url: "..."
```

**Important:**
- Do NOT include `machine_readable` sections
- Keep text as-is (no eurocent conversion)
- Include ALL articles from the law
- Use proper YAML multiline string format (`|`) for text

### Step 8: Save File

**Directory Structure:**
```
regulation/nl/{regulatory_layer_lowercase}/{law_id}/{effective_date}.yaml
```

**Example:**
```
regulation/nl/wet/wet_op_de_zorgtoeslag/2025-01-01.yaml
regulation/nl/ministeriele_regeling/regeling_standaardpremie/2025-01-01.yaml
```

Create directories if they don't exist.

### Step 9: Validate YAML Against Schema

Before confirming, validate the generated YAML:

```bash
uv run python script/validate.py {FILE_PATH}
```

**If validation fails:**
- Review error messages
- Fix the YAML structure
- Re-validate until it passes

**Common validation issues:**
- Missing required fields (bwb_id, uuid, etc.)
- Incorrect type for regulatory_layer
- Malformed YAML syntax
- Invalid date formats

### Step 10: Confirm with User

Report:
```
✓ Downloaded and converted {REGULATION_TITLE}
  ID: {BWBR_ID or CVDR_ID}
  Type: {Type}
  Articles: {COUNT}
  Saved to: {FILE_PATH}
  ✅ Schema validation: PASSED

The YAML file contains the legal text only.
To add machine-readable execution logic, use the law-machine-readable-interpreter skill.
```

## Error Handling

**If search returns no results:**
- Suggest alternative search terms
- Ask user if they have the BWBR ID directly

**If XML download fails:**
- Check if date exists (try other dates from manifest)
- Verify BWBR ID is correct
- Provide direct URL for user to check in browser

**If XML parsing fails:**
- Report which XML element caused the issue
- Save raw XML to temp file for manual inspection
- Ask user if they want to continue with partial data

## Tips for Success

- Always download BOTH WTI and Toestand files
- Handle XML namespaces correctly
- Preserve exact text formatting (spaces, line breaks)
- Generate human-readable `$id` slugs (lowercase, hyphens)
- Double-check all articles are included (count them)
- Validate YAML syntax before saving
