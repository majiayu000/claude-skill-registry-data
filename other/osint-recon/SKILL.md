---
name: osint-recon
description: General OSINT investigation skill — property intelligence, person enrichment, court records, geospatial data pipeline, and passive corporate security audit methodology for comprehensive reconnaissance.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [osint, reconnaissance, investigation, property-intel, person-intel, geospatial, mcp]
    triggers: [investigate, who-lives-at, recon, osint, search, find-information, security-audit, passive-audit, corporate-recon, entity-assessment, breach-history, legal-regulatory, AG-settlement, state-attorney-general, class-action, financial-health, debt-analysis, PE-ownership, leadership-profile, CEO-background, executive-profile, threat-attractiveness]
    related_skills: [osint-business, osint-person, osint-property, osint-social, osint-threat, domain-intel]
---

# OSINT Reconnaissance

General-purpose open-source intelligence investigation skill. Covers the end-to-end pipeline from address → owner → person enrichment → court records → geospatial cross-referencing.

## Prerequisites

### Required MCP Servers
The following MCP servers should be configured in `config.yaml` for full capability:

```yaml
mcpServers:
  property-intel-mcp:
    command: npx
    args: ["-y", "@modelcontextprotocol/property-intel"]
  person-intel-mcp:
    command: npx
    args: ["-y", "@modelcontextprotocol/person-intel"]
  geospatial-mcp:
    command: npx
    args: ["-y", "@modelcontextprotocol/geospatial-mcp"]
```

If not available, use web-based alternatives (county assessor websites, PACER, Google Maps).

### Recommended Tools
- Web browser (Firefox DevTools MCP) for manual lookups
- Terminal for curl/API queries
- Custom MCP servers for specialized data sources

## Step-by-Step Reconnaissance Workflow

### 1. Define Investigation Scope

Before starting, establish:
- **Target type**: Property, person, business, event, or all?
- **Jurisdiction**: County, state, federal, international?
- **Depth**: Quick lookup vs. deep dive?
- **Legal constraints**: What data sources are permitted?

```
Scope: Residential address 123 Main St, Anytown, CA
Depth: Owner identification → background check → asset mapping
Sources: County assessor, state court records, social media
```

### 2. Address → Property Intelligence

Start with a physical address to establish the property baseline:

```python
# Using property-intel-mcp (conceptual)
tools.call("property-intel-mcp", {
    "address": "123 Main St, Anytown, CA 90210",
    "include": ["owner", "tax_history", "valuation", "parcel_map"]
})
```

**Output provides:**
- Parcel number (APN)
- Current owner name(s)
- Assessed value & market estimate
- Tax payment history (delinquency flags)
- Property type (residential/commercial/vacant)
- Sale history
- Square footage, lot size, bedrooms/bathrooms

### 3. Owner → Person Enrichment

Take the owner name from step 2 and enrich with person intelligence:

```python
tools.call("person-intel-mcp", {
    "name": "John Doe",
    "state": "CA",
    "include": ["aliases", "address_history", "relatives", "employer"]
})
```

**Output provides:**
- Known aliases and name variations
- Current and previous addresses
- Possible relatives and associates
- Employer and professional history
- Phone numbers and emails (public sources)
- Social media profiles

### 4. Person → Court Records

Search for legal history tied to the person:

```
Search sources:
- PACER (federal courts): https://pacer.uscourts.gov
- State court portals (varies by state)
- County Superior Court online search
- Case law aggregators (Google Scholar, CourtListener)
- Arrest records and incarceration databases
```

**What to look for:**
- Civil lawsuits (eviction, foreclosure, debt collection)
- Criminal records
- Family court (divorce, custody, restraining orders)
- Bankruptcy filings
- Tax liens and judgments

### 5. Cross-Reference with Geospatial Data

Use geospatial intelligence to map relationships:

```python
# Geospatial analysis (conceptual)
tools.call("geospatial-mcp", {
    "address": "123 Main St, Anytown, CA 90210",
    "radius": "0.5mi",
    "include": ["parcels", "crime_data", "demographics"]
})
```

**Analysis patterns:**
- Proximity to other owned properties
- Neighborhood demographic context
- Crime statistics near address
- Environmental hazards (flood zones, Superfund sites)
- Nearby points of interest (schools, churches, businesses)

### 6. Business Entity Association

Check if the person or address is linked to any business entities:

```
Search sources:
- Secretary of State business search (state-specific)
- OpenCorporates: https://opencorporates.com
- SAM.gov entity search: https://sam.gov
- SEC EDGAR: https://sec.gov/edgar
"""

### 7. Social Media & Digital Footprint

Search for online presence:

```python
# Google dork pattern
site:linkedin.com/in "John Doe" "Anytown"

# Social media platform search
urls = [
    f"https://facebook.com/search/people/?q={name}",
    f"https://twitter.com/search?q={name}",
    f"https://instagram.com/web/search/topsearch/?query={name}"
]
```

### 8. Compile Findings

Organize results into a structured report:

```
Subject: John Doe
Primary Address: 123 Main St, Anytown, CA

PROPERTY SUMMARY:
- Parcel: 1234-567-890
- Value: $450,000 (assessed), ~$620,000 (estimated market)
- Owned since: 2015-03-15
- Status: Current on taxes, no liens

PERSON PROFILE:
- DOB: 1975-08-22 (estimated)
- Aliases: Johnathan Doe, JD
- Known employer: ABC Corp (2018-present)
- Social: linkedin.com/in/johndoe, fb.com/johndoe

LEGAL HISTORY:
- Traffic violation (2019) - paid
- Small claims case SC-2020-0042 (dismissed)

BUSINESS TIES:
- Registered agent: Anytown Properties LLC (formed 2021)

RISK ASSESSMENT:
- LOW - Clean public record, stable employment, current on obligations
```

## Example Workflows

### Quick Address Lookup
```
1. Input address
2. Query property-intel-mcp for owner
3. Query person-intel-mcp for enrichment
4. Output summary report
```

### Full Subject Investigation
```
1. Start with name or address
2. Property records → ownership chain
3. Person enrichment → aliases, relatives
4. Court records → legal history
5. Business search → entity ties
6. Social media → digital footprint
7. Geospatial → context mapping
8. Compile final intelligence report
```

### Asset Tracing
```
1. Identify known assets (property, vehicles, business)
2. Search county records for other owned properties
3. Check UCC filings for secured assets
4. Search business filings for LLC involvement
5. Cross-reference person enrichment addresses
6. Geospatial analysis for proximity patterns
```

### Corporate Security Audit (Multi-Entity)
```
1. Entity identification — resolve each named target to legal entity + domain
2. Breach & incident history — known data breaches, ransomware, threat actors
3. Legal & regulatory history — state AG actions, class actions, consent decrees
4. Technology footprint — cloud providers, subdomains, tech stack
5. Leadership profiling — CEO/board, security maturity indicators
6. Financial health — PE ownership, debt load, earnings trend
7. Attack surface — passive-only checks (crt.sh, headers, job postings)
8. Threat actor attractiveness — who would target this entity and why
9. Cross-entity comparison — risk matrix across all targets
10. Structured report — tiered findings with source attribution
```

## Advanced OSINT Tool Integrations

Tools from the investigator's arsenal — beyond basic searches to the systems used by federal investigators and intelligence communities.

### IntelTechniques (Michael Bazzell's Toolkit)

Built by Michael Bazzell, a former FBI cybercrimes investigator who runs a highly respected OSINT training operation. His site hosts a free search tool collection that aggregates dozens of lookups into one place.

- **URL:** https://inteltechniques.com/
- **Cost:** Free (web-based)
- **Capabilities:**
  - Cross-reference usernames, emails, and phone numbers instantly
  - Same methodologies taught to federal investigators
  - Aggregates dozens of OSINT lookups in one interface
  - No install needed — runs in the browser

**How to use in an investigation:**
1. Navigate to https://inteltechniques.com/
2. Choose the search type (username, email, phone, name)
3. Input your target identifier
4. Results aggregate from dozens of sources simultaneously
5. Cross-reference findings with other tools for verification

### Epieos — Email & Phone OSINT Engine

Demonstrates exactly how un-anonymous an email address is. When you input an email, it reveals which Google services are tied to it — profile photos, real names, and linked Google accounts.

- **URL:** https://epieos.com/
- **Cost:** Free (basic), paid for bulk
- **Capabilities:**
  - Email reverse lookup → reveals Google services tied to it
  - Profile photos and real names from Google's systems (~4 seconds)
  - Phone number reverse lookup
  - Checks if email registered on various platforms

**Investigation workflow:**
```bash
# Step 1: Open Epieos in browser
# navigate_page to: https://epieos.com/

# Step 2: Enter target email address
# Step 3: Review Google service associations:
#   - Google Account profile photo
#   - Google Maps reviews written
#   - YouTube channel (if linked)
#   - Google Play app reviews
#   - Google Calendar (if exposed)

# Step 4: Cross-reference with Holehe holehe target@email.com --only-used
# Epieos shows Google-specific results
# Holehe shows 100+ platform registrations
```

### Hunchly — Browser Evidence Capture & Chain of Custody

A browser extension built specifically for online investigators. As you browse, it automatically captures and timestamps every single page you visit. This builds a fully documented, admissible, and reconstructible evidence trail.

- **URL:** https://www.hunch.ly/
- **Cost:** Paid ($139/year, free trial available)
- **Platform:** Chrome/Chromium extension
- **Capabilities:**
  - Auto-captures every page visited with full-page screenshots
  - Timestamps every capture for chain of custody
  - Full HTML source saved (not just screenshots)
  - Search across all captured pages
  - Export case files for legal proceedings
  - Nothing lost if a webpage is later taken down

**Investigation workflow:**
```
1. Install Hunchly extension in Chrome/Chromium
2. Create a new case for each investigation
3. Browse normally — Hunchly captures everything in the background
4. Notes and tags can be added to each capture
5. Export case file when investigation is complete
6. Captures include: full page screenshot, HTML source, HTTP headers, timestamp
```

**When to use Hunchly:**
- Documenting evidence that may be taken down later
- Building admissible evidence for legal proceedings
- Multi-session investigations where you need continuity
- Collaborative investigations with team case sharing

### Overpass Turbo — Advanced Geolocation via OpenStreetMap

Used for advanced geolocation that goes far beyond simple reverse image searches. By combining this tool with OpenStreetMap data, investigators can cross-reference specific visual landmarks from a photo against geographic databases to pin down locations with shocking precision.

- **URL:** https://overpass-turbo.eu/
- **Cost:** Free
- **Data Source:** OpenStreetMap (community-maintained global map database)
- **Capabilities:**
  - Query geographic features (buildings, roads, landmarks, power lines, streetlights)
  - Cross-reference visual landmarks against spatial databases
  - Filter by feature type, size, color, material
  - Visualize results on an interactive map
  - Export results as GeoJSON, GPX, KML
  - Same technique used by Bellingcat to locate conflict footage

**Basic geolocation workflow:**
```
1. Extract visual landmarks from photo/video:
   - Unusual building shapes or rooflines
   - Streetlight/power pole designs
   - Road markings and signage styles
   - Geographic features (hills, water bodies, vegetation)
   - Radio towers, antennas, or distinctive structures

2. Build Overpass Turbo query to find matching features:
```

```cpp
// Example: Find all McDonald's restaurants within 1km of a known point
// This is Overpass QL (Query Language)
[out:json];
(
  node["amenity"="fast_food"]["name"="McDonald's"](around:1000,40.7128,-74.0060);
  way["amenity"="fast_food"]["name"="McDonald's"](around:1000,40.7128,-74.0060);
);
out center;

// Example: Find distinctive streetlight types in a region
[out:json];
(
  node["highway"="street_lamp"]({{bbox}});
);
out body;
```

```
3. Narrow down by comparing visual features:
   - Country-specific road markings (yellow vs white lines)
   - Regional building architecture styles
   - Unique landmarks visible in the background
   - Power grid infrastructure (pole shapes, transformer boxes)
   - Vegetation types (palm trees, pine forests, desert plants)

4. Cross-reference with Google Street View to confirm
5. Document coordinate evidence with timestamps
```

**Real-world use case (Bellingcat method):**
```
1. Photo shows a distinctive yellow building with a curved roof
2. Extract: building shape, color, nearby landmarks, vegetation
3. Query Overpass Turbo for buildings with those attributes
4. Cross-reference results with satellite imagery
5. Verify via Street View or other sources
6. Pinpoint exact location with high confidence
```

### Cross-Reference Workflow Using All Tools

```bash
# 1. START with email or username
holehe target@email.com --only-used -NP          # Check email registrations
sherlock targetusername --print-found              # Find username accounts

# 2. ENRICH with Google service data
# Navigate to: https://epieos.com/ → enter email → check Google associations

# 3. DEEP DIVE on findings
# IntelTechniques: cross-reference all identifiers
# Overpass Turbo: geolocate any location clues

# 4. DOCUMENT everything
# Hunchly: auto-capture all browsed pages with timestamps

# 5. VERIFY across multiple independent sources
```

## Common Pitfalls

### Data Freshness
- **PITFALL**: Assessor data may be 6-18 months old.
- **SOLUTION**: Always note data date; cross-check with recent sales data.
- **WORKAROUND**: County recorder's office may have more current records than assessor.

### Name Commonality
- **PITFALL**: "John Smith" produces too many false positives.
- **SOLUTION**: Narrow by middle name, DOB, address, or SSN last-4.
- **WORKAROUND**: Add date of birth or middle initial to filter results.

### Jurisdiction Gaps
- **PITFALL**: Federal court records (PACER) don't cover state cases.
- **SOLUTION**: Search both federal AND state court systems.
- **WORKAROUND**: Use CourtListener for aggregated federal + some state.

### Address Standardization
- **PITFALL**: "123 Main St" vs "123 Main Street" — different results.
- **SOLUTION**: Use USPS standardized address format.
- **WORKAROUND**: Always try 2-3 address variants.

### False Assumptions
- **PITFALL**: Assuming the person listed on the deed still lives there.
- **SOLUTION**: Cross-check with utility records, voter registration, vehicle registration.
- **WORKAROUND**: Even when property is occupied, the owner may be a landlord.

## Legal & Ethical Notes

> **⚠️ WARNING**: OSINT must comply with all applicable laws. This skill describes **publicly available information** techniques only. Never:
> - Access protected/private systems without authorization (CFAA violation)
> - Use credentials obtained through deception
> - Scrape websites that prohibit automated access in their ToS
> - Harass, dox, or intimidate subjects
> - Violate state-specific privacy laws (e.g., CA CPRA, GDPR for EU subjects)
> - Use information for unlawful purposes (stalking, fraud, discrimination)

### Permissible Uses
- Investigative journalism
- Background checks with subject consent
- Fraud investigation
- Security research
- Legal discovery (with attorney supervision)
- Personal safety research

### Recommended Practices
- Document all sources and timestamps
- Verify findings from at least 2 independent sources
- Do not share raw intelligence with unauthorized parties
- Respect data retention and deletion policies of sources
- Consider whether subject has a reasonable expectation of privacy

## Reference Files

- `references/data-sources.md` — Full catalog of 65+ FOSS data sources organized by domain, with API status and coverage notes
- `references/js-site-data-extraction.md` — Web OSINT techniques for extracting data from JS-heavy sites (Wix, job boards), OSM Nominatim geocoding, and Facebook embed profiling. Workarounds when search engines are CAPTCHA-blocked.
- `references/passive-security-audit.md` — Ten-stage passive legal security audit methodology for named entities: entity identification, breach/incident history, legal & regulatory history, tech stack mapping, leadership & org profiling, financial health & ownership analysis, attack surface assessment, threat actor attractiveness, cross-entity comparison, and structured reporting

## Cross-References

- `references/data-sources.md` — Full catalog of 65+ FOSS data sources organized by domain, with API status and coverage notes
- `references/passive-security-audit.md` — Ten-stage passive legal security audit methodology for named entities: entity identification, breach/incident history, legal & regulatory history, tech stack mapping, leadership & org profiling, financial health & ownership analysis, attack surface assessment, threat actor attractiveness, cross-entity comparison, and structured reporting
- `security/osint-property` — Deep dive into property intelligence workflows
- `security/osint-person` — Person investigation enrichment techniques
- `security/osint-business` — Corporate entity and beneficial ownership tracing
- `security/osint-social` — Social media reconnaissance and identity resolution
- `security/osint-threat` — Threat intelligence (Shodan, VirusTotal, SpiderFoot)
- `security/osint-redteam` — Red team operations and attack surface mapping
- `security/osint-facial` — FOSS facial recognition for identity verification
- `software-development/systematic-debugging` — Apply systematic methodology patterns to investigation

## Verification Checklist

- [ ] Property intelligence returns assessor data with parcel number
- [ ] Person enrichment resolves name to at least address history and aliases
- [ ] Court records search returns results (even if empty)
- [ ] Geospatial analysis provides proximity context
- [ ] Business entity search finds registered entities
- [ ] Findings cross-verified from 2+ sources
- [ ] Legal constraints documented before investigation began
- [ ] Report compiled with source attribution and timestamps
