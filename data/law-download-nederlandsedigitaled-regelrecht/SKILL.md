---
name: law-download
description: >
  Downloads Dutch official legal publications including national laws, local
  regulations, and implementation policies from government sources (wetten.overheid.nl,
  lokaleregelgeving.overheid.nl). Use this skill proactively when: user mentions
  downloading, fetching, or importing a Dutch law by name or BWB/CVDR identifier,
  when a source.regulation reference points to a law not in the corpus, or when
  user provides a wetten.overheid.nl URL. Activate automatically when user mentions
  a specific Dutch law name, BWB identifier (BWBR...), or CVDR identifier.
allowed-tools: Read, Write, WebFetch, Bash, Grep, Glob
user-invocable: true
---

# Law Download

Downloads official Dutch legal publications from government sources (national
and local) and converts them to the regelrecht YAML format.

**Pipeline:** `/law-download` (this skill) → `/law-interpret` (adds machine_readable logic)

Use this skill first to create a text-only YAML file, then use `/law-interpret`
to add machine-readable execution logic to it.

## What This Skill Does

1. Searches for Dutch regulations in government databases:
   - **BWB** (Basiswettenbestand) - National laws and regulations
   - **CVDR** (Centrale Voorziening Decentrale Regelgeving) - Local regulations
2. Presents search results with identifiers (BWBR, CVDR) and metadata
3. Downloads the XML from the official repository
4. Parses the XML to extract articles and metadata
5. Converts to YAML format with **text only** (no machine_readable sections)
6. Saves to `corpus/regulation/nl/{layer}/{law_id}/{date}.yaml`

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
https://zoekservice.overheid.nl/sru/Search?operation=searchRetrieve&version=1.2&x-connection=BWB&query={QUERY}&maximumRecords=10
```

**API Endpoint (CVDR):**
```
https://zoekservice.overheid.nl/sru/Search?operation=searchRetrieve&version=1.2&x-connection=CVDR&query={QUERY}&maximumRecords=10
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
https://zoekservice.overheid.nl/sru/Search?operation=searchRetrieve&version=1.2&x-connection=BWB&query=dcterms.title%20any%20"zorgtoeslag"&maximumRecords=10

# Search CVDR for municipal regulations
https://zoekservice.overheid.nl/sru/Search?operation=searchRetrieve&version=1.2&x-connection=CVDR&query=dcterms.title%20any%20"afvalstoffenverordening"&maximumRecords=10

# Search specific municipality
https://zoekservice.overheid.nl/sru/Search?operation=searchRetrieve&version=1.2&x-connection=CVDR&query=overheidcvdr.organisatietype==gemeenten%20AND%20dcterms.creator==Amsterdam%20AND%20dcterms.title%20any%20"afval"&maximumRecords=10
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
- `<bwb-dl:bwb-id>` → `bwb_id` (top-level field)
- `<bwb-dl:soort>` → Map to `regulatory_layer`:
  - "wet" → "WET"
  - "AMvB" → "AMVB"
  - "ministeriele regeling" → "MINISTERIELE_REGELING"
  - "beleidsregel" → "BELEIDSREGEL"
  - "koninklijk besluit" → "KONINKLIJK_BESLUIT"
  - See schema for full enum list
- `<bwb-dl:citeertitel>` or `<bwb-dl:officiele-titel>` → `name` (and slugified for directory name)
- First `<bwb-dl:intrekking datum="...">` → `valid_from`
- `<bwb-dl:publicatiedatum>` → `publication_date`

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
$schema: https://raw.githubusercontent.com/MinBZK/regelrecht/refs/tags/schema-v0.7.1/schema/v0.7.1/schema.json
$id: "{LAW_SLUG}"
name: "{LAW_TITLE}"
regulatory_layer: "{MAPPED_LAYER}"
publication_date: "{YYYY-MM-DD}"
valid_from: "{YYYY-MM-DD}"
url: "https://wetten.overheid.nl/{BWBR_ID}/{DATE}"
bwb_id: "{BWBR_ID}"

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
- All identifiers (`bwb_id`, `url`) are top-level, not nested

### Step 8: Save File

**Directory Structure:**
```
corpus/regulation/nl/{regulatory_layer_lowercase}/{law_id}/{valid_from}.yaml
```

**Example:**
```
corpus/regulation/nl/wet/wet_op_de_zorgtoeslag/2025-01-01.yaml
corpus/regulation/nl/ministeriele_regeling/regeling_standaardpremie/2025-01-01.yaml
```

Create directories if they don't exist.

### Step 9: Validate YAML Against Schema (with repair loop)

The generated YAML has to pass `just validate`. The schema is the single
source of truth.

```bash
just validate {FILE_PATH}
```

**If validation fails** — repair (up to 3 rounds):
1. Read the error output carefully, identify broken fields/structure
2. Fix the YAML with the Edit tool
3. Re-run `just validate`
4. If still failing after 3 rounds, stop and report the errors to the user

**Common validation issues:**
- Missing required fields (`regulatory_layer`, `publication_date`, `url`, `articles`)
- Missing `bwb_id` for national laws (WET, AMVB, MINISTERIELE_REGELING, GRONDWET)
- Incorrect `regulatory_layer` enum value
- Malformed YAML syntax (bad indentation, unescaped special characters in text)
- Invalid date formats (must be `YYYY-MM-DD`)
- Articles missing `number`, `text`, or `url` fields

**Do NOT proceed to Step 10 with invalid YAML.** A file that fails validation
cannot be used by `/law-interpret` in the next step.

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
To add machine-readable execution logic, run /law-interpret on this file.
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
- Generate human-readable directory name slugs (lowercase, underscores — e.g., `wet_op_de_zorgtoeslag`)
- Double-check all articles are included (count them)
- Validate YAML syntax before saving
