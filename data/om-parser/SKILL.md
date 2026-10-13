---
name: om-parser
description: "Parse CRE Offering Memorandums. Extract NOI, cap rate, occupancy, rent roll, property details, financial projections from OMs. Maps extracted data to structured schemas and flags extraction gaps."
---

# /om-parser -- CRE Offering Memorandum Parser

Extract structured financial and property data from Commercial Real Estate Offering Memorandums (OMs). Handles PDF, DOCX, and text formats. Maps extracted data to structured property schemas and flags inconsistencies or missing fields.

> Before executing, read `_shared/plugin-context.md` for Nexus domain vocabulary, MCP tool references, and quality standards.

## Prerequisites

**Required**: An OM document -- uploaded PDF, DOCX, pasted text, or a link to a document in a data room.

**Optional MCP Connections** (enhance automation):
- **Nexus MCP** (`nexus.syntari-ai.com/api/mcp`) -- `nexus_get_cre_asset`, `nexus_list_cre_assets` for cross-referencing extracted data against existing portfolio
- **Box MCP** -- `ai_extract_freeform`, `get_file_content` for parsing OMs stored in Box data rooms
- **BigData.com MCP** (via `financial-analysis` plugin) -- market data for validation of extracted metrics
- **Egnyte MCP** -- data room document access

**Graceful Degradation**: If MCP tools are not connected, paste OM text directly into the conversation, upload the PDF/DOCX file, or provide key data points manually. The extraction framework and validation logic work identically with manual input.

## When to Use
- Ingesting a new CRE deal from a broker-provided OM document
- Populating a deal pipeline from source marketing materials
- Extracting financial metrics for quick screening before full underwriting
- Building a comparable transaction database from OM packages received over time
- Automating bulk OM ingestion from email attachments or data room uploads
- Validating OM-stated metrics against third-party data sources

## OM Section Taxonomy

Standard OMs follow this section structure. Extract from each in sequence:

| Section | Key Fields | Extraction Method |
|---------|-----------|-------------------|
| **Executive Summary / Investment Highlights** | Deal headline, asking price, summary cap rate, investment thesis | First 2-3 pages, bullet points |
| **Property Description** | Name, address, type, year built, total SF/units, lot size, stories, parking | Property header block |
| **Location / Market Overview** | Submarket, MSA, proximity to demand drivers, market vacancy, rent trends | Map section, narrative paragraphs |
| **T12 Operating Statement** | GPR, vacancy loss, EGI, OpEx line items, NOI, cap rate | Financial tables |
| **Pro Forma / Projections** | Year 1-5 projections, rent growth rate, expense growth, exit cap rate, IRR | Forward-looking tables |
| **Rent Roll** | Unit mix, unit count by type, current rent, market rent, lease start/end, tenant names | Rent roll table |
| **Comparable Sales** | Recent sales, address, date, price, price/SF, cap rate | Comps table |
| **Debt / Financing** | Existing loan balance, rate, maturity, assumability, suggested LTV | Financing section |

## Property Detail Fields (Full Extract List)

**Physical**
- Property name, street address, city, state, zip, county, MSA
- Property type (Multifamily / Office / Retail / Industrial / Mixed-Use / Hospitality)
- Total square footage (gross, net rentable), total units (multifamily), lot size (acres)
- Year built, year renovated, number of stories, number of buildings, parking spaces

**Financial**
- Asking price, price per SF, price per unit (multifamily)
- Current NOI, pro forma NOI, T12 NOI
- In-place cap rate, pro forma cap rate, market cap rate
- Gross potential rent, vacancy loss, effective gross income
- Operating expense ratio, management fee %, taxes, insurance, maintenance
- Net operating income, DSCR, debt service amount, debt yield

**Income**
- Average current rent per SF / per unit
- Average market rent per SF / per unit
- Occupancy rate (physical), occupancy rate (economic)
- Rent-to-market gap (upside potential)

**Projections**
- Annual rent growth assumption (Years 1-5)
- Exit cap rate assumption, hold period
- Projected levered IRR, equity multiple, cash-on-cash return

## Data Shapes

### OM Extracted Data

```typescript
interface OMExtractedData {
  // Property
  propertyName: string | null
  address: string | null
  city: string | null
  state: string | null
  propertyType: 'Multifamily' | 'Office' | 'Retail' | 'Industrial' | 'Mixed-Use' | null
  yearBuilt: number | null
  totalUnits: number | null
  totalSqft: number | null

  // Financial
  askingPrice: number | null
  currentNoi: number | null
  capRate: number | null
  occupancy: number | null
  grossPotentialRent: number | null
  vacancyLoss: number | null
  operatingExpenseRatio: number | null

  // Projections
  projectedIrr: number | null
  exitCapRate: number | null
  holdPeriod: number | null
  rentGrowthAssumption: number | null

  // Rent Roll
  rentRoll: Array<{
    unitType: string
    unitCount: number
    sqftPerUnit: number
    currentRent: number
    marketRent: number
    leaseExpiry: string | null
  }>

  // Extraction Quality
  extractionGaps: string[]       // Fields that could not be populated
  consistencyFlags: string[]     // Internal consistency issues found
  sourceDocument: string         // Document name or reference
}
```

## Workflow

### Step 1: Identify Document Format
Determine the OM format and select the appropriate extraction path:
- **PDF with text layer**: Extract text content directly (use Box MCP `get_file_content` if in data room)
- **Scanned PDF (image-only)**: Route to OCR pipeline before extraction
- **DOCX**: Extract via document parsing
- **Already structured text/JSON**: Parse directly
- **Pasted text**: Work with provided content

### Step 2: Locate and Extract Sections
Work through the OM Section Taxonomy sequentially:
- Use regex patterns to identify section headers (case-insensitive)
- For each section, apply the appropriate extraction strategy (table vs narrative vs key-value pairs)
- Financial tables: extract all rows as structured arrays, identify header rows
- Narrative sections: apply NLP extraction for key metrics embedded in prose

### Step 3: Parse Financial Tables
Extract T12, Pro Forma, and Rent Roll tables:
- Identify column headers (categories) and row labels (line items)
- Normalize line item names to canonical field names (e.g., "Gross Scheduled Income" -> `grossPotentialRent`)
- Handle multi-column tables (T12 vs Pro Forma side by side)
- Extract rent roll: one row per unit type, columns for count, SF, current rent, market rent, lease expiry

### Step 4: Map to Structured Output
Translate extracted data to the `OMExtractedData` schema:
- Property fields -> top-level fields
- Financial metrics -> financial fields
- Rent roll -> `rentRoll` array
- Projections -> projection fields

### Step 5: Flag Extraction Gaps and Inconsistencies
Before returning, validate the extracted data:
- List all fields from the full extract list that could not be populated
- Check for internal consistency: does (GPR - Vacancy) approximately equal EGI? Does (EGI - OpEx) approximately equal NOI?
- Flag any metrics that seem out of range for the property type and market (e.g., cap rate < 3% for industrial)
- Note any OCR-quality issues (garbled numbers, broken table formatting)

### Step 6: Store or Export Results
- **With Nexus MCP**: Use `nexus_underwrite_cre` to feed extracted data into the underwriting pipeline
- **Without Nexus MCP**: Output the structured `OMExtractedData` as formatted JSON or markdown tables for the user to consume directly

## Sample Output

```
OM PARSE COMPLETE -- 123 Main Street Multifamily, Austin TX

PROPERTY DETAILS
  Name:          123 Main Street Multifamily
  Address:       123 Main Street, Austin, TX 78701
  Type:          Multifamily
  Year Built:    2019
  Units:         142
  Total SF:      127,800 SF (900 SF avg)

FINANCIAL SUMMARY
  Asking Price:  $28,500,000   ($200,704/unit)
  Current NOI:   $1,396,500
  Cap Rate:      4.90%
  Occupancy:     83.2% (physical)  78.1% (economic)
  GPR:           $2,421,600
  Vacancy Loss:  ($411,672)   (17.0%)
  Op Expenses:   ($613,428)   (35% of EGI)

RENT ROLL (4 unit types extracted)
  Unit Type  Count  SF   Current Rent  Market Rent  Upside
  Studio       22   550     $1,450        $1,650      +$200
  1BR/1BA      68   800     $1,850        $2,100      +$250
  2BR/2BA      44   1,100   $2,400        $2,700      +$300
  3BR/2BA       8   1,400   $3,200        $3,600      +$400

EXTRACTION GAPS (3)
  - Existing debt terms not found (no financing section in this OM)
  - Comparable sales table missing (referenced but not included)
  - Year-5 exit cap rate assumption not stated (assumed 5.00% -- flag for underwriter)

CONSISTENCY CHECK
  GPR - Vacancy = $2,009,928 vs stated EGI $2,009,928  [OK]
  EGI - OpEx = $1,396,500 vs stated NOI $1,396,500  [OK]
  NOI / Price = 4.90% vs stated cap rate 4.90%  [OK]
```

## Workflow Chain

**Position**: Step 1 of 4 in the CRE deal chain
**Next**: `/cre-underwriter` -- passes extracted property details, T12 data, and rent roll for full underwriting analysis

## Related Skills
- `/cre-underwriter` -- Full CRE underwriting model built from the structured data extracted by this skill
- `/deal-screener` -- Screen and score the extracted deal against investment criteria
- `/deal-memo-writer` -- Write the CRE investment memo using extracted OM data
- `/financial-modeling` -- Financial model support for extracted deal metrics
- `/competitive-analysis` -- Market and submarket analysis to validate OM claims

## Confidence Calibration

Every OM parse must include a calibrated confidence assessment:

```
## Confidence Assessment
- **Score**: 0.XX (0.0 = no confidence, 1.0 = full confidence)
- **Calibration**: conservative | neutral | optimistic
- **Confidence Drivers**: [what supports the score -- e.g., "clean text-layer PDF", "all 8 sections present", "financial tables well-formatted"]
- **Data Gaps**: [what's missing that would improve confidence -- e.g., "rent roll missing lease expiry dates", "T12 has no line-item detail"]
```

Typical confidence ranges:
- **0.85+**: Clean PDF with all 8 sections, well-formatted tables, consistent financial data
- **0.65-0.84**: Most sections present, some tables require interpretation, minor gaps
- **0.40-0.64**: Partial OM (missing key sections), OCR quality issues, significant gaps
- **Below 0.40**: Heavily redacted, image-only without OCR, or summary-only document -- flag for manual review
