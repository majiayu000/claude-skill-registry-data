---
name: probate-property-finder
description: >
  Find real property owned by probate decedents when you only have the case filing (PR number,
  decedent name, executor details) but no property address. Browses county assessor/CAD sites,
  deed records, and aggregators to discover every parcel the decedent owned, then outputs a
  Sift-ready CSV with formatted addresses and property data. Works on single records or bulk
  CSV. Use whenever someone says "find the property for this probate", "what did the decedent
  own", "complete this probate list", "enrich probate records", "fill in missing property
  addresses", "probate property lookup", "property discovery", or uploads a CSV of probate
  filings missing property addresses. Also use when someone has a decedent name and county
  but no property address. Even if the user just says "I have probates but no addresses" or
  "find the properties for these" — use this skill.
---

# Probate Property Finder

When a real estate investor pulls probate filings from a county, they often get only the case
number, decedent name, date of death, and executor contact information — but no property
address. This skill bridges that gap by researching what real property the decedent actually
owned and producing a clean, upload-ready CSV for REI Sift.

This skill focuses exclusively on **property discovery and data enrichment**. It does NOT
identify decision-makers, skip trace heirs, or do deep prospecting — the `deep-prospecting`
skill handles that separately once you have an address.

## Critical Principle: Actually Browse the Sites

The single most important thing this skill does is **use browser tools to navigate county
assessor and recorder websites and execute searches**. Do not merely identify URLs or list
them as resources — you must actually open the browser, navigate to the site, type in search
terms, read the results, and extract data from the pages.

If a county assessor site is broken, unresponsive, or returns no results, immediately pivot
to the county recorder/deed search. If that fails, use aggregator sites. But always start by
actually browsing the official county data source.

Aggregator sites (Zillow, NeighborWho, Spokeo, etc.) are for cross-referencing only — never
treat them as primary sources. They often have stale or incorrect ownership data. The county
assessor is the source of truth for current ownership, and deed records are the source of
truth for ownership history.

## Input Formats

The skill accepts two input modes:

### Single Record
The user provides details about one probate case in conversation:
- Decedent name (required)
- County/state where probate was filed (required)
- Case/file number (helpful but optional)
- Executor name and address (helpful for cross-referencing)
- Date of death (helpful for narrowing searches)

### Bulk CSV
The user uploads a CSV file containing multiple probate records. The CSV may have varying
column names, but typically includes some combination of:
- File/case number
- Deceased/decedent name
- Date of death/deceased
- Executor/PR name
- Executor address (street, city, state, zip — may be separate columns or combined)

Parse the CSV flexibly — column names vary between counties and users. Map whatever columns
exist to the internal fields: `decedent_name`, `case_number`, `date_of_death`, `county`,
`state`, `executor_name`, `executor_address`, `executor_city`, `executor_state`, `executor_zip`.

If the county is not in a column, check the filename, the user's message, or ask.

## Research Workflow

For each record, execute these steps in order. Every step involves actually browsing the
web — not just identifying sites to check later.

### Step 1: Parse and Prepare the Record

Extract all available fields from the input. Note:
- The executor's address is NOT the subject property — it's where the executor lives (often
  a different city or state entirely). However, it may sometimes BE a property the decedent
  owned (e.g., the executor is a family member living in the decedent's house). You MUST
  verify this on the county assessor, not assume.
- The county where probate was filed is the most likely location for the decedent's property,
  but not guaranteed — search all mentioned geographies.
- Clean up name formatting: "LAST, FIRST MIDDLE" should become "First Middle Last" for
  search purposes. Handle suffixes (Jr., Sr., II, III) gracefully.

### Step 2: County Assessor / CAD Search (Primary)

This is the highest-value lookup because county assessors index properties by owner name.
You must actually navigate to the site and execute the search using browser tools.

**How to find the right assessor site:**
1. Google: `{County Name} county {State} property tax search` or
   `{County Name} county {State} assessor property search by owner name`
2. Look for the official county website — NOT third-party aggregators
3. Many counties use common platforms:
   - DevNet/Wedge (e.g., `champaignil.devnetwedge.com`) — often address/parcel search only
   - Tyler Technologies / iasWorld
   - Esri-based GIS portals
   - State-specific systems (e.g., Texas uses county appraisal districts like `brazoscad.org`)

**Important: Some county sites only search by address or parcel number, NOT by owner name.**
If the main assessor site doesn't have owner-name search, look for alternative portals:
- Community data sites (e.g., `cu-citizenaccess.org` for Champaign County IL)
- Tax year databases that allow owner name lookup
- GIS portals with owner-name search capability
- The county may have separate "property search" and "tax inquiry" sites — try both

**Search strategy:**
1. Try the decedent's full name: "Last, First Middle" and "Last, First"
2. If too many results, add middle initial
3. If no results, try maiden name if known (e.g., "Tomlinson" for "Tomlinson Howell")
4. Try name variants: with/without suffix, middle name vs initial, hyphenated vs not
5. Record ALL parcels returned — decedents often own multiple properties

**For each parcel found, capture:**
- Property address (full street address)
- City, State, Zip
- Parcel ID / APN / PIN
- Assessed value (land + improvements if available)
- Property type (residential, commercial, vacant land, farm land, etc.)
- Square footage, lot size, year built, bedrooms, bathrooms (if shown)
- Acreage (especially for rural/farm parcels)

**If the county assessor site is broken, not loading, or returns no results**, do NOT give
up — proceed IMMEDIATELY to Step 3 (Deed Records). County websites go down often; this is
not an excuse to stop searching.

### Step 3: Deed / Recorder Search (Critical Fallback)

This step is ESSENTIAL when the assessor site fails or returns nothing. County recorder
offices maintain deed records that show every property transfer. Navigate to the recorder's
site and search.

**How to find the recorder site:**
- Google: `{County Name} county {State} deed records search` or
  `{County Name} county {State} official records search`
- Texas: Many counties use `{county}.tx.publicsearch.us` (e.g., `brazos.tx.publicsearch.us`)
- Illinois: Check `{county}countyclerk.com` or the county clerk's website
- Other states: Search for the county recorder of deeds or county clerk website

**Search strategy:**
1. Navigate to the recorder/clerk's online search portal
2. Search by the decedent's last name: "Howell, Irene" or "Weber, Virginia"
3. Look for documents where the decedent is the **GRANTEE** (they received the property)
   — these are the properties they owned
4. Also check where they are the **GRANTOR** — if there's a deed transferring property
   AFTER the date of death, the property has already been moved out of the estate
5. Look for document types: WARRANTY DEED, QUIT CLAIM DEED, GRANT DEED, DEED OF TRUST
6. Extract the legal description from the deed (e.g., "WOODBROOK 00003 000T 00583 0156")
7. Cross-reference the legal description with the assessor to get a street address

**Analyzing deed results:**
- If the most recent deed shows the decedent as grantee (received property) with no
  subsequent transfer, the property is likely still in the estate
- If a TRUSTEE'S DEED or SUBSTITUTE TRUSTEE'S DEED shows the property going FROM the
  decedent TO a bank/savings institution, the property was likely foreclosed
- If a WARRANTY DEED shows the decedent transferring the property to someone else before
  death, they no longer owned it
- Note the dates of all transactions — this tells the story of ownership

### Step 4: Executor Address Verification

Before moving to aggregators, check whether the executor's address is actually owned by
the decedent. This is extremely common in probate — the surviving spouse or adult child
(now executor) often lives in the decedent's house.

1. Navigate to the county assessor site for the executor's county
2. Search by the executor's street address (or parcel search if available)
3. Check the owner name on file:
   - If it shows the DECEDENT's name → the executor's address IS the estate property
   - If it shows the EXECUTOR's name → it's the executor's own home, NOT estate property
   - If it shows BOTH names (joint ownership) → it's likely an estate property
4. Record the parcel data if it's the decedent's property

This verification must be done on the actual county assessor, not aggregator sites.
Aggregators often show outdated or inaccurate ownership data and will lead to wrong
conclusions (e.g., showing someone as "resident" when they're actually not the owner).

### Step 5: Aggregator Cross-Reference (Supplemental Only)

Use aggregator sites ONLY to supplement or cross-reference data already found in Steps 2-4.
Never use these as the sole basis for a property finding.

1. **Zillow**: Search the decedent's name + city/state for sold/off-market listings
2. **Redfin**: Similar search
3. **County GIS Portal**: Separate mapping portal with parcel data

If aggregators show a property NOT found in assessor/deed searches, note it as LOW
confidence and flag for manual verification.

### Step 6: Google Dorking (Fallback Discovery)

When assessor and recorder searches come up empty, use targeted Google searches:

```
"{Decedent Full Name}" property {County} {State}
"{Decedent Full Name}" deed {County}
"{Decedent Full Name}" obituary (obituaries often say "of [address]" or "[Name], [age], of [City]")
"{Decedent Full Name}" "property tax" {County}
site:{county-assessor-domain} "{Decedent Last Name}"
```

Also try:
- Searching obituary sites (Legacy.com, local newspaper obits) — they frequently include
  the decedent's city of residence or street
- Searching the decedent's name in neighboring counties
- Searching name variants (maiden name, middle name, with/without suffix)

### Step 7: Multi-County Sweep

Search for properties in ALL geographies mentioned in the record:
- The county where probate was filed (primary)
- The county/state where the executor lives (if different)
- Any other counties/states mentioned in the record or discovered during research

This is not optional. Even when the executor lives out of state, they may be managing
property in a completely different location. A probate filed in County A with an executor
in State B means you search BOTH County A and the executor's county in State B.

### Step 8: Compile and Validate

For each property discovered:
1. Verify the owner name on title matches the decedent (accounting for name variants,
   middle initials, suffixes)
2. Confirm the property has NOT been transferred after the date of death (check for
   recent deeds or sales)
3. Note if property was foreclosed or sold before death (still include in output with note)
4. Flag any properties where ownership is uncertain (partial name match, common name, etc.)
5. If the decedent died recently and the property appears in prior-year tax records but
   not the current year, it may have been transferred to the executor/estate — check the
   prior year's assessor data too

## Handling Edge Cases

### No Property Found
If no property can be found after ALL steps (assessor, recorder/deeds, executor address
check, aggregators, Google dorking):
- Mark the record as "NO PROPERTY FOUND" in the output
- Note which sources were actually checked (not just identified)
- Common reasons: decedent was a renter, property was sold before death, property is in
  a trust or LLC name, property is in a different state entirely, property was foreclosed

### Multiple Properties Found
Include ALL properties as separate rows in the output CSV, each linked back to the same
case number so the user knows they came from the same probate filing. This is very common
with rural/farm properties — one decedent may own multiple parcels.

### Common Names
When a name is very common (e.g., "John Smith"), use these disambiguation strategies:
- Cross-reference with the executor's address or the probate county
- Use the date of death to eliminate active owners
- Check if middle names or initials narrow the results
- Flag the result as LOW confidence if ambiguity remains

### Executor Address IS the Property
Sometimes the executor lives at the decedent's property (common with surviving spouses
or adult children). You MUST verify this by checking the county assessor for the owner
name on the executor's address. Do NOT assume the executor's address is the property
just because the executor lives there — verify that the DECEDENT is listed as owner on
the assessor. If the assessor shows the EXECUTOR as owner (not the decedent), then it
is the executor's property, not the estate's.

### Deceased Owners Disappearing from Current Tax Year
When a property owner dies, their name may be removed from the CURRENT tax year's
assessor records and replaced with the executor or estate name. If searching the current
year returns nothing, check the PRIOR tax year's records. Many assessor sites let you
toggle between tax years.

### Trust / LLC Ownership
The decedent may have held property in a trust or LLC. If the direct name search returns
nothing:
- Try searching for "[Decedent Last Name] Trust" or "[Decedent Last Name] Living Trust"
- Try "[Decedent Last Name] LLC" or "[Decedent Last Name] Properties"
- Check if the obituary or any court records mention a trust

### Foreclosed / Previously Transferred Property
If deed records show the property was foreclosed (trustee's deed to a bank) or transferred
before death, the decedent no longer owns it. Still include it in the output but note:
"Property foreclosed [DATE] — no longer in estate" or "Transferred to [GRANTEE] on [DATE]"

### Minor / Invalid Records
Some rows in the CSV may not be valid probate cases (e.g., "Minor - Didn't log"). Skip
these records and note them in the output as "SKIPPED - [reason]".

## Output Format

### Primary Output: Sift-Ready CSV

The CSV must have these columns in this order:

```
Case Number, Decedent Name, Property Address, City, State, Zip, Parcel ID, Assessed Value, Property Type, Bedrooms, Bathrooms, Sq Ft, Lot Size, Year Built, Executor Name, Executor Address, Executor City, Executor State, Executor Zip, Confidence, Notes
```

**Column definitions:**
- `Case Number`: Original case/file number from input
- `Decedent Name`: Cleaned decedent name (First Middle Last format)
- `Property Address`: Street address ONLY (no city/state/zip) — properly formatted with
  standard abbreviations (St, Ave, Blvd, Dr, Ln, Ct, etc.)
- `City`: City name
- `State`: Two-letter state abbreviation
- `Zip`: 5-digit zip code
- `Parcel ID`: County parcel/APN number (blank if not found)
- `Assessed Value`: Total assessed value in dollars (blank if not found)
- `Property Type`: SFR, Multi-Family, Condo, Townhouse, Vacant Land, Farm Land, Commercial
- `Bedrooms`: Number (blank if not found)
- `Bathrooms`: Number (blank if not found)
- `Sq Ft`: Living area square footage (blank if not found)
- `Lot Size`: Lot size in sq ft or acres (blank if not found)
- `Year Built`: 4-digit year (blank if not found)
- `Executor Name`: From input record
- `Executor Address`: From input record
- `Executor City`: From input record
- `Executor State`: From input record
- `Executor Zip`: From input record
- `Confidence`: HIGH / MEDIUM / LOW
  - HIGH = Owner name matches exactly, verified on county assessor
  - MEDIUM = Found on deed records or single-source confirmation
  - LOW = Common name, ambiguous match, aggregator-only, or unverified
- `Notes`: Brief note on research outcome (e.g., "Verified on Champaign Co. assessor -
  2 parcels, 80 acres farm land", "Foreclosed 1987 - no longer in estate",
  "Executor address verified as executor's own property, not decedent's")

**Address Formatting Rules:**
- Capitalize first letter of each word (123 Main St, not 123 MAIN ST or 123 main st)
- Use standard USPS abbreviations: St, Ave, Blvd, Dr, Ln, Ct, Cir, Pl, Rd, Way, Ter
- No periods in abbreviations (St not St.)
- Include unit/apt numbers where applicable (123 Main St Apt 4B)
- No trailing commas or extra whitespace
- For farm/rural parcels without a street address, use the legal description or parcel
  location (e.g., "Section 9, Township 20N, Range 9E" or just note "Rural parcel - no
  street address" and include the Parcel ID)

### Summary Report (Markdown)

After the CSV, also produce a brief markdown summary:

```
## Probate Property Finder — Results Summary

- **Records processed**: X
- **Properties found**: X (across Y parcels)
- **No property found**: X
- **Skipped**: X
- **Multi-property records**: X
- **Foreclosed/transferred**: X

### Records Needing Attention
[List any LOW confidence matches or records where the user should verify manually]
```

## Processing Strategy for Bulk CSVs

When processing a CSV with many records:

1. **Parse the entire CSV first** — understand the column mapping and total record count
2. **Group records by county** — batch lookups by county to minimize site navigation
3. **Process county by county** — for each county:
   a. Navigate to the assessor/CAD site once
   b. Search each decedent name from that county
   c. Record all findings
   d. Move to the next county
4. **Check executor addresses** on the assessor for possible estate properties
5. **Search deed/recorder records** for any records that came up empty on the assessor
6. **Google dorking** as final fallback for stubborn records
7. **Compile the full output CSV** with all records

This county-batching approach is much faster than processing record-by-record because
you only have to figure out each county's assessor site once.

## Important Reminders

- The executor's mailing address is NOT the subject property in most cases. Verify on the
  assessor before assuming. The assessor's owner field is the source of truth.
- Always search by the DECEDENT's name, not the executor's name, when looking for property
  ownership.
- Properties may have been sold or transferred before death — check deed history.
- Some decedents may not own any real property at all (they rented). This is a valid finding.
- Accuracy matters more than speed. A wrong address wastes the investor's marketing dollars.
  When in doubt, flag it as LOW confidence rather than guessing.
- Save the output CSV to the workspace/Desktop folder so the user can download it.
- When a county assessor site is down or broken, pivot to deed records immediately — do
  not stop searching.
- Always check prior tax year records when a recently deceased owner doesn't appear in
  the current year.
