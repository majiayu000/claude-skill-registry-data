---
name: osint-property
description: Property intelligence skill — county assessor lookups, valuation analysis, parcel maps, tax delinquency detection, foreclosure flags, and chaining property data with person data.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [osint, property, market-lead, assessor, tax-records, foreclosure, parcel]
    triggers: [property, assessor, market-lead, tax-records, parcel, foreclosure, property-lookup]
    related_skills: [osint-person, osint-recon]
---

# OSINT Property Intelligence

Property intelligence from public records — county assessor databases, tax records, parcel maps, valuation trends, and foreclosure detection. Chain property data with person data to identify ownership networks.

## Prerequisites

### Recommended MCP Servers
```yaml
mcpServers:
  property-intel-mcp:
    command: npx
    args: ["-y", "@modelcontextprotocol/property-intel"]
  geospatial-mcp:
    command: npx
    args: ["-y", "@modelcontextprotocol/geospatial-mcp"]
```

### Free Public Data Sources (no MCP needed)
- **County Assessor Portals**: Each county publishes property records online (search for "[county] county assessor parcel search")
- **Zillow / Redfin / Realtor.com**: Market valuation estimates and recent sales
- **DataTree / RealQuest**: Commercial property data aggregators
- **USPS Address Validation**: https://tools.usps.com/zip-code-lookup.htm
- **FEMA Flood Maps**: https://msc.fema.gov/portal/search
- **EPA Superfund Sites**: https://www.epa.gov/superfund/search-superfund-sites

## Property Data Fundamentals

### Key Identifiers
| Field | Description | How to Find |
|-------|-------------|-------------|
| APN (Assessor Parcel Number) | Unique property ID, county-specific | County assessor portal |
| Street Address | Physical location | USPS standardize first |
| Legal Description | Lot/block/tract from deed | County recorder |
| Owner Name | Current recorded owner(s) | Assessor records |
| Property Type | Residential/commercial/vacant | Zoning + use code |

### What Property Records Reveal
- **Ownership**: Current and historical owners
- **Valuation**: Assessed value (tax basis) vs. market value
- **Taxes**: Annual amount, payment history, delinquency
- **Improvements**: Building details, square footage, year built
- **Sales History**: Previous sale dates and prices
- **Liens**: Tax liens, mechanic's liens, HOA liens
- **Mortgages**: Lender name, loan amount, recording date
- **Foreclosure**: Notice of Default, Notice of Sale, REO status
- **Exemptions**: Homestead, senior, disabled veteran (indicates occupancy)

## Step-by-Step Workflows

### 1. Standard Property Lookup

#### By Address

```bash
# Step 1: Standardize the address
# Use USPS ZIP Code lookup
curl -s "https://tools.usps.com/tools/app/ziplookup/cityByZip" \
  -d "zip5=90210" | jq .

# Step 2: Search county assessor (example — pattern varies by county)
# Navigate county assessor website
# Firefox DevTools MCP approach:
# 1. navigate_page to assessor portal
# 2. fill_by_uid with address fields
# 3. extract results
```

#### By Parcel Number (APN)

```
APN Format: Typically "123-456-789" or "1234 567 890"
County-specific: Some use map book/page/parcel (e.g., MB 12 PG 34 PAR 5)

Search strategies:
- Exact APN if known
- Partial APN with wildcard if supported
- Map-based search by neighborhood grid
```

#### By Owner Name

```
Beneficial for:
- Landlord portfolio discovery
- Property management companies
- Trust and LLC ownership unraveling
- Related party transactions

Pitfalls:
- Common names yield many results
- Trust names obscure individual owners
- LLC names may be generic
```

### 2. Valuation Analysis

```python
# Valuation data points to collect
valuation_data = {
    "assessed_value": 350000,      # Tax assessment basis
    "market_value_estimate": 525000, # Zillow/Zestimate or similar
    "last_sale_price": 480000,     # Most recent transaction
    "last_sale_date": "2020-06-15",
    "tax_rate": 1.25,              # Effective tax rate (% of assessed)
    "annual_taxes": 4375,          # Assessed * tax rate / 100
    "assessed_vs_market_ratio": 0.67  # Assessed / Market
}
```

**Analysis Questions:**
- Is assessed value significantly below market? (Potential tax advantage)
- Did last sale price deviate from market trends? (Distressed sale / premium)
- Is the tax rate consistent with neighboring properties?
- Have there been recent reassessments or appeals?

### 3. Tax Delinquency Detection

```bash
# Tax delinquency check workflow
# Step 1: Query assessor for tax status
# Step 2: Check county treasurer for delinquent tax list
# Step 3: Search for tax lien sales in the county

# Common patterns:
# - "Delinquent Tax List" + county name
# - "Tax Sale" + county + date
# - "Notice of Default" + county recorder
```

**Red Flags:**
- Late payments (even 30 days)
- Multiple missed payments
- Tax lien filed against property
- Property in tax sale/auction
- Notice of default recorded
- Foreclosure filing

**Impact:**
- Tax liens take priority over mortgages
- County can sell property to satisfy back taxes
- Redemption periods vary by state (6 months to 3 years)
- Interest and penalties accrue at high rates

### 4. Foreclosure Detection Pipeline

```python
# Foreclosure lifecycle (California example)
stages = {
    "pre-foreclosure": {
        "filing": "Notice of Default (NOD)",
        "remedy_period": "90 days to reinstate",
        "public_record": "County recorder document"
    },
    "auction": {
        "filing": "Notice of Trustee Sale (NOTS)",
        "timeline": "21+ days after NOD expires",
        "location": "County courthouse steps (typically)"
    },
    "post-foreclosure": {
        "status": "Real Estate Owned (REO) by lender",
        "listing": "MLS listing by asset manager",
        "eviction": "Tenants at risk of displacement"
    }
}
```

**Detection Sources:**
1. County recorder new filings (daily/weekly check)
2. Legal notices in local newspapers
3. Third-party foreclosure data feeds
4. MLS listing status changes ("Short Sale", "REO/Bank Owned")

### 5. Chain Property Data with Person Data

```python
# Cross-reference workflow
cross_ref = {
    "step_1": "Property lookup → identify owner(s)",
    "step_2": "Owner name search in person-intel-mcp",
    "step_3": "Check if owner is LLC or trust → beneficiary search",
    "step_4": "Address history of owner → other owned properties",
    "step_5": "Search relatives/associates for co-owned properties",
    "step_6": "Map all discovered properties geospatially",
    "step_7": "Check business entity filings → property LLCs",
    "step_8": "Cross-reference court records → property litigation"
}
```

### 6. Portfolio Discovery

Find all properties owned by a single person or entity:

```bash
# Techniques for portfolio discovery
# 1. County-wide owner name search (assessor portal)
# 2. Same mailing address on multiple parcels
# 3. Same trustee/LLC manager on multiple entities
# 4. Same phone number on multiple tax records
# 5. Same lender on multiple mortgages
# 6. Geospatial cluster analysis of owned parcels
```

## Web Browser Quick Lookup (No Special Tools Needed)

When conventional web search tools are unavailable or blocked, use the **Playwright MCP browser** to perform property OSINT directly.

### Step 1: Location Identification

If you have only a vague location name (misheard placenames, neighborhood names), verify the location first:

1. **Use OSM Nominatim search** via curl or browser:
   ```
   https://nominatim.openstreetmap.org/search?q=Shaker+Bay+Albany+County&format=json
   ```
   This returns exact street names, zip codes, and coordinates.

2. **Common placename corrections for NY:**
   - "Colony" → Colonie /kəˈloʊni/ (pronounced like "colony" by locals)
   - "Leatham" → Latham (hamlet in Colonie)
   - "Shaker Bay" → Shaker Bay Road (residential street, not a body of water)

3. **Get road geometry** from OSM API for property location context:
   ```
   https://api.openstreetmap.org/api/0.6/way/{way_id}
   ```

### Step 2: Quick Property Records (Free Aggregators)

The fastest way to get bulk property data without a per-county portal search:

**CountyOffice.org** — Aggregates 40+ property records per street into one page:
```
https://www.countyoffice.org/shaker-bay-rd-latham-ny-property-records/
```
Returns: assessed market value, tax value, sale history, acreage, bed/bath count, year built, owner count — all for free without login.

**Other free aggregators** to chain:
- **NeighborWho** — Owner & property records by street (may require free signup)
- **FastPeopleSearch** — Free occupant/owner names by address
- **FamilyTreeNow** — Free relative lookups for property occupants
- **BeenVerified** — Paid but has rich free previews
- **PropertyShark** — Paid but has free search previews

### Step 3: Extract Owner Names from Google AI Overview

Google's AI Overview is a powerful **free intelligence source** for property owner names:

```
Search in browser: "Shaker Bay Rd Latham NY owner names families"
```
AI Overview often surfaces:
- Owner names from public property records
- Trust names (e.g., "Dianne C. Hellert Revocable Living Trust")
- Developer/LLC information
- Notable families in the neighborhood
- Sale prices and dates

**Why this works:** Google aggregates data from Zillow, Redfin, Homes.com, Whitepages, Spokeo, and other property sites into its AI Overview — giving you the owner names without paying for individual reports.

### Step 4: Cross-Reference Occupants

Chain free people-search sites for each address:

| Site | What It Provides | URL Pattern |
|------|-----------------|-------------|
| FastPeopleSearch | Most recent occupant | `https://www.fastpeoplesearch.com/address/{street}-{city}-{zip}` |
| FamilyTreeNow | Residents + relatives | `https://www.familytreenow.com/records/people/address/{address}` |
| Whitepages Property | Owner name from deeds | `https://property.whitepages.com/property/...` |

### Step 5: County Clerk Online Records (Paid but Official)

The county clerk's online record system has the **actual recorded deeds** with full owner names:
```
https://www.searchiqs.com/nyalb/Login.aspx  (Albany County example)
```
Most counties use a third-party provider (SearchIQS, RealTDM, etc.) with subscription access.

### Full Workflow Example (from Shaker Bay Road OSINT)

```python
workflow = {
    "1_location": "OSM Nominatim → confirmed Shaker Bay Road, Latham, Colonie, NY 12110",
    "2_bulk_data": "CountyOffice.org → 41 property records with assessed values ($149K-$4.3M)",
    "3_owner_names": "Google AI Overview → Hellert Family, James D. Finning, Sheila Nelson",
    "4_occupants": "FastPeopleSearch + FamilyTreeNow → Shannon Older, relatives of Nelson",
    "5_developer": "Redfin listing → Shaker Bay Properties, LLC (developer), agent Arline Littman",
    "6_context": "Wikipedia → Colonie history (Shaker settlement), Latham demographics (13,680 pop)"
}
```

This workflow works for **any US street** — just substitute the location and re-run each step.

## Example Commands

### Firefox DevTools MCP — County Assessor Lookup

```
# Step 1: Open assessor portal
navigate_page(url="https://assessor.lacounty.gov/property-search/")

# Step 2: Enter address
fill_by_uid(uid="address_input", value="123 Main St")

# Step 3: Search
click_by_uid(uid="search_button")

# Step 4: Extract owner
take_snapshot(selector="#property-details .owner-name")

# Step 5: Check tax status
take_snapshot(selector="#tax-details")
```

### Terminal — Bulk CSV Processing

```bash
# If you have a CSV of addresses, process each
while IFS=, read -r address city state zip; do
  echo "=== Looking up: $address, $city, $state $zip ==="
  # Custom script to call assessor API
  python lookup_property.py "$address" "$city" "$state" "$zip"
  sleep 2  # Rate limiting
done < addresses.csv
```

## Property-Specific MCP Tools (Templates)

If building custom MCP tools for property intelligence:

```python
# Example MCP tool structure
@mcp.tool()
async def lookup_property(address: str) -> str:
    """
    Look up property records by address.
    Returns owner, assessed value, tax status, and sale history.
    """
    # 1. Standardize address
    # 2. Determine county from ZIP
    # 3. Query county assessor portal
    # 4. Parse results
    # 5. Return structured data
    pass

@mcp.tool()
async def detect_foreclosure(apn: str, county: str, state: str) -> str:
    """
    Check for foreclosure activity on a property.
    """
    # 1. Search county recorder for NOD/NOTS
    # 2. Check tax delinquency
    # 3. Check MLS status if available
    # 4. Return risk assessment
    pass
```

## Common Pitfalls

### Web Search Tools Unavailable
- **PITFALL**: The `web_search` tool may not exist or be unavailable in your environment. All web search engines (Google, DuckDuckGo, Bing) aggressively block curl/requests with CAPTCHAs.
- **SOLUTION**: Use the **Playwright MCP browser** instead — it renders JavaScript and bypasses most captchas. Navigate directly to Bing or Google, or use specialized property sites.
- **WORKAROUND**: When the browser is also blocked (Zillow/Redfin 403), use aggregator sites like CountyOffice.org and exploit Google's AI Overview which displays owner names from aggregated public records without requiring login.

### Data Inconsistency
- **PITFALL**: Assessor data differs from county recorder data.
- **SOLUTION**: Assessor handles valuation; Recorder handles title/deeds. Both are authoritative for their domain.
- **WORKAROUND**: Check both systems and note any discrepancies.

### Deed of Trust vs. Mortgage
- **PITFALL**: Some states use Deeds of Trust (3-party: borrower, lender, trustee); others use Mortgages (2-party).
- **SOLUTION**: Know your state's system. Foreclosure process differs.
- **WORKAROUND**: For Deed of Trust states, non-judicial foreclosure is common (faster, no court).

### LLC & Trust Ownership
- **PITFALL**: Property owned by "Smith Family Trust" or "123 Main LLC" — individual ownership is hidden.
- **SOLUTION**: Search trust name or LLC name in business records and person enrichment.
- **WORKAROUND**: Check trustee/officer names from business filings. Some trusts name the trustee in the deed.

### Timeshare / Condo Complexity
- **PITFALL**: Condo/timeshare ownership records are more complex.
- **SOLUTION**: Condo docs show unit number, HOA status. Timeshare records may be held by developer.
- **WORKAROUND**: Check HOA websites for owner info; timeshare may require title search.

### Vacation / Second Home
- **PITFALL**: Owner may live in a different state/county.
- **SOLUTION**: Check mailing address on tax records — often different from property address.
- **WORKAROUND**: The mailing address IS the owner's tax mailing address (often their home).

## Legal & Ethical Notes

> **⚠️ WARNING**: Property records are generally public information by law, but use must comply with:
> - **Fair Housing Act**: Do not discriminate based on race, color, religion, sex, familial status, national origin, disability
> - **FDCPA**: If collecting debts, property intelligence must comply with debt collection laws
> - **State-specific privacy**: Some states limit bulk downloading of assessor data
> - **Terms of Service**: County assessor websites may prohibit automated scraping
> - **GLBA**: Financial institutions have restrictions on using property data
> - **Data Broker Regulations**: Some states (VT, CA, OR) regulate data broker activities

### Best Practices
- Verify property occupancy before taking any action
- Do not use property data for predatory lending or tenant screening without consent
- Property tax delinquency is public information but may have legitimate explanations (dispute, error)
- Document your methodology for reproducibility
- Note that "owner" on tax records may not reflect current ownership if deed hasn't been recorded

## Cross-References

- `security/osint-recon` — Full investigation pipeline starting from property
- `security/osint-person` — Enrich owner information with person intelligence
- `security/osint-business` — Trace LLC/trust property ownership to beneficial owners
- `security/osint-threat` — Check if property is associated with known fraud or illegal activity
- `security/osint-redteam` — Property intelligence for physical penetration testing context
- `software-development/systematic-debugging` — Systematic methodology for complex property chains

## Verification Checklist

- [ ] Address standardized via USPS before lookup
- [ ] Parcel number (APN) obtained from assessor
- [ ] Owner name(s) recorded with source date
- [ ] Tax status verified (current / delinquent)
- [ ] Valuation data collected (assessed + estimated market)
- [ ] Sale history with dates and prices
- [ ] Lien and encumbrance check performed
- [ ] Cross-reference with person enrichment completed
- [ ] Business entity search for LLC/trust ownership
- [ ] Legal constraints documented
