---
name: lien-discovery-skill
description: Discover and analyze lien positions from AcclaimWeb and RealTDM to detect HOA foreclosures and senior mortgage survival
---

# Lien Discovery Skill

Analyzes recorded liens to determine priority positions and detect critical scenarios like HOA foreclosures.

## When to Use This Skill

- Stage 4 of Everest Ascent pipeline
- Determining what buyer inherits at auction
- Detecting HOA foreclosure scenarios
- Building lien satisfaction calculations

## Critical Concept: Lien Priority

**First Position Lien:** Foreclosure wipes out junior liens
**HOA Foreclosure:** Senior mortgage SURVIVES (buyer inherits it)

This is THE most critical determination in auction analysis.

## Data Sources

### AcclaimWeb (Brevard County Official Records)
- Search by: Case number, parcel ID, address
- Returns: Mortgages, liens, satisfactions, assignments
- Anti-detection: Randomized delays, user-agent rotation
- Parse: PDF documents for amounts, dates, parties

### RealTDM (Tax Certificates)
- Search by: Parcel ID
- Returns: Outstanding tax certificates, amounts, holders
- Priority: Tax liens are senior to ALL other liens

## 12 Regex Patterns (BECA Scraper V2.0)

1. **Mortgage Amount:** `\$([0-9,]+\.\d{2})`
2. **Recording Date:** `(\d{1,2}/\d{1,2}/\d{4})`
3. **Book/Page:** `Book (\d+) Page (\d+)`
4. **Instrument Number:** `Instrument# (\d+)`
5. **Mortgagor/Mortgagee:** Named entity extraction
6. **Satisfaction:** "Satisfied", "Released", "Paid in Full"
7. **Assignment:** "Assigned to", "Transferred to"
8. **HOA Lien:** "Homeowners Association", "HOA", "Condominium Association"
9. **Tax Lien:** "Tax Certificate", "Tax Deed"
10. **Judgment Lien:** "Judgment", "Lis Pendens"
11. **Mechanic's Lien:** "Construction", "Contractor"
12. **IRS Lien:** "Internal Revenue Service", "Federal Tax Lien"

## Lien Priority Rules (Florida)

**Priority Order:**
1. Tax liens (always senior)
2. Special assessment liens
3. First recorded mortgage
4. Second recorded mortgage
5. HOA liens (SUBORDINATE to mortgages in most cases)
6. Judgment liens
7. Mechanic's liens

**Exception:** HOA foreclosure on assessment lien

## HOA Foreclosure Detection

**Red Flags:**
- Plaintiff is "Homeowners Association" or "Condominium Association"
- Lien is for assessments/dues (not mortgage)
- Senior mortgage exists and was NOT joined in suit

**Action:**
```
if (plaintiff_is_hoa AND senior_mortgage_exists):
    decision = "DO_NOT_BID"
    reason = "HOA foreclosure - senior mortgage survives"
```

## Output Format

```json
{
  "lien_analysis": {
    "total_liens": 3,
    "liens": [
      {
        "position": "1st",
        "type": "mortgage",
        "amount": 250000,
        "holder": "Wells Fargo Bank",
        "recording_date": "2018-03-15",
        "instrument": "2018012345",
        "status": "active"
      },
      {
        "position": "2nd", 
        "type": "hoa_assessment",
        "amount": 15000,
        "holder": "Satellite Beach HOA",
        "recording_date": "2023-06-01",
        "status": "foreclosing"
      },
      {
        "position": "tax",
        "type": "tax_certificate",
        "amount": 8500,
        "holder": "Brevard County Tax Collector",
        "status": "active"
      }
    ],
    "foreclosure_type": "hoa",
    "senior_mortgage_survives": true,
    "buyer_inherits": [
      "Wells Fargo 1st mortgage ($250K)",
      "Tax certificate ($8.5K)"
    ],
    "recommendation": "DO_NOT_BID"
  }
}
```

## Search Process

### Step 1: AcclaimWeb Search
```
Search by case number: 2024-CA-001234
→ Returns: Lis pendens, mortgages, liens
→ Parse each PDF document
→ Extract amounts, dates, parties
```

### Step 2: Cross-Reference Parcel
```
Get parcel ID from BCPAO
Search AcclaimWeb by parcel
→ Find ALL recorded instruments on property
→ Build complete lien chain
```

### Step 3: RealTDM Tax Search
```
Search tax certificates by parcel
→ Any outstanding certificates?
→ Add to lien analysis
```

### Step 4: Priority Analysis
```
Order liens by recording date
Apply Florida priority rules
Identify which liens survive foreclosure
Calculate satisfaction amounts
```

## Example Scenarios

### Scenario 1: Clean First Mortgage Foreclosure
```
Plaintiff: Wells Fargo Bank
Lien Position: 1st mortgage
Junior Liens: 2nd mortgage ($50K), HOA lien ($5K)
→ Result: Junior liens wiped out, buyer gets clean title
→ Decision: Proceed with normal analysis
```

### Scenario 2: HOA Foreclosure (DANGER)
```
Plaintiff: Palm Bay Homeowners Association  
Lien Position: Assessment lien (subordinate)
Senior Liens: 1st mortgage Wells Fargo ($300K)
→ Result: Buyer inherits $300K mortgage
→ Decision: DO_NOT_BID
```

### Scenario 3: Tax Certificate Foreclosure
```
Plaintiff: Brevard County Tax Collector
Lien Position: Tax lien (senior to all)
Other Liens: 1st mortgage ($200K), 2nd mortgage ($50K)
→ Result: ALL liens wiped out, clean title
→ Decision: Strong opportunity
```

## Anti-Detection Measures

**BECA Scraper V2.0 Features:**
- Randomized delays (2-8 seconds between requests)
- User-agent rotation (5 different browsers)
- Session management (new session per search)
- Headless browser mode (Selenium)
- PDF parsing with pdfplumber
- OCR fallback for scanned documents

## Integration with Foreclosure Analysis

```python
# Stage 4: Lien Priority Analysis
lien_data = lien_discovery_skill.analyze(case_number, parcel_id)

if lien_data['senior_mortgage_survives']:
    decision = "DO_NOT_BID"
    max_bid = 0
else:
    # Proceed to Stage 5
    continue_pipeline()
```

## Example Usage

```
"Use lien-discovery-skill to analyze liens for case 2024-CA-001234"

"Search AcclaimWeb and RealTDM for property at 123 Main St Melbourne"
```

## Critical Reminders

1. **NO GUESSWORK:** Use actual recorded documents only
2. **Verify Dates:** Recording date determines priority
3. **Check Satisfactions:** Lien may show but be satisfied
4. **HOA = DANGER:** Always check if senior mortgage survives
5. **Tax Liens Win:** Tax certificates are senior to everything
