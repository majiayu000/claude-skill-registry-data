---
name: osint-business
description: Corporate intelligence skill — business entity lookup, officer tracing, beneficial ownership, SEC EDGAR filings, SAM.gov contracts, and LLC/trust/corp entity type detection.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [osint, business, corporate, sec, edgar, beneficial-ownership, entity-search, contract, sam-gov]
    triggers: [business, company, corporate, llc, sec, edgar, beneficial-owner, secretary-of-state, entity-search, contract]
    related_skills: [osint-person, domain-intel, osint-recon]
---

# OSINT Business / Corporate Intelligence

Corporate intelligence from public records — entity formation documents, officer/director tracing, beneficial ownership chains, SEC filings, government contracts, and entity-type detection for unravelling shell companies and ownership structures.

## Prerequisites

### Recommended MCP Servers
```yaml
mcpServers:
  sec-edgar-mcp:
    command: npx
    args: ["-y", "@modelcontextprotocol/sec-edgar"]
  person-intel-mcp:
    command: npx
    args: ["-y", "@modelcontextprotocol/person-intel"]
```

### Free Public Data Sources
- **Secretary of State Business Search**: Each state has a free entity search portal
- **OpenCorporates**: https://opencorporates.com (largest open database of companies)
- **SEC EDGAR**: https://www.sec.gov/edgar (public company filings)
- **SAM.gov**: https://sam.gov (federal contractor registration)
- **USPTO**: https://www.uspto.gov (trademark assignments reveal business activity)
- **Better Business Bureau**: https://www.bbb.org (complaints and business profiles)
- **FINRA BrokerCheck**: https://brokercheck.finra.org (financial professionals)
- **State Professional Licensing Boards**: Contractor, real estate, medical licenses
- **Dun & Bradstreet**: https://www.dnb.com (business credit reports, some free)
- **Credit Reporting**: Experian Business, Equifax Business (paid)

## Entity Type Detection

### Common US Entity Types

| Type | Suffix | Ownership | Formation | Best For |
|------|--------|-----------|-----------|----------|
| Sole Proprietorship | None (DBA) | Individual | No state filing | Freelancers |
| General Partnership | GP | Partners | Optional filing | Professional groups |
| Limited Partnership | LP, Ltd. | General + Limited Partners | State filing | Real estate, investments |
| LLC | LLC, L.L.C. | Members | State filing | Small business, real estate |
| S-Corp | Inc., Corp., Ltd. | Shareholders (≤100) | State filing + IRS election | Tax-efficient small business |
| C-Corp | Inc., Corp., Ltd. | Shareholders (unlimited) | State filing | Public companies, VC-funded |
| Nonprofit | Inc. (501c3) | No owners, Board | State filing + IRS exemption | Charitable organizations |
| Trust | Trust | Trustee + Beneficiaries | Private document | Estate planning, privacy |
| Series LLC | LLC (Series) | Series members | DE/IL/NV/TX/OK/UT only | Multi-asset holding |

### Privacy Indicators by State Formation

| State | Anonymity Level | Notes |
|-------|----------------|-------|
| Delaware | Low-Medium | Officer/Director public, but registered agent can conceal |
| Wyoming | Medium-High | No member/officer disclosure (until CTA 2024) |
| Nevada | Medium | No member/officer disclosure |
| New Mexico | High | No reporting requirements (historically) |
| Texas | Medium | Managing agent names public |
| California | Low | Full officer/manager disclosure |

## Step-by-Step Workflows

### 1. Entity Lookup by Name

```bash
# Step 1: Identify likely state of formation
# - State where entity operates
# - Delaware (most common for LLCs/Corps)
# - State with favorable privacy laws (WY, NV, NM)

# Step 2: Search Secretary of State business database
# Example: California Secretary of State
# navigate_page to: https://businesssearch.sos.ca.gov/
# Enter entity name or file number

# Step 3: Extract entity details
# - Entity name and type
# - File number / Entity ID
# - Status (Active, Suspended, Dissolved, Forfeited)
# - Date of formation
# - Agent for service of process
# - Principal address
# - Officers / Managers / Members (state-dependent)
```

**Florida Sunbiz (FL DOS):** See `references/fl-sunbiz-entity-search.md` for the Sunbiz URL structure, status codes, fuzzy-matching pitfalls, and the Chrome DevTools MCP table-extraction technique for efficient batch lookups.

### 1b. Dealing with Down/Migrated State Databases

Many state SOS/DOS websites have migrated to new platforms. Old direct URLs (often `.asp` or legacy systems) return "page unavailable" or redirect to migration notices. OpenCorporates and data aggregators also block automated searches with CAPTCHAs.

**When direct state SOS access is unavailable:**

```bash
# Step 1: Check the state's main business portal
# NY DOS example: https://www.dos.ny.gov/corporation-and-business-entity-database
# Old NY direct search: appext20.dos.ny.gov/corp_public/CORPSEARCH.INPUT (SHUT DOWN)

# Step 2: Try the UCC e-filing portal (separate system, may still work)
# NY UCC: https://ucc-efiling.dos.ny.gov — for UCC filings/debtor searches
# This reveals secured transactions, equipment loans, supplier agreements
# Search by debtor name to find the legal entity associated with a business

# Step 3: Check the Wayback Machine for cached SOS search results
# Search for cached versions of state SOS search pages
curl -s "https://web.archive.org/cdx/search/cdx?url=appext20.dos.ny.gov/*Omega*&output=text&limit=10"
# Note: Most state DOS search pages use POST forms, which Wayback doesn't capture well

# Step 4: Use alternative aggregators (note: most block automation)
# - OpenCorporates: Requires API key for automated access
# - CorporationWiki: Web form only, blocks curl
# - Bizapedia: Shows search form but rarely returns results via curl
# - Better Business Bureau: www.bbb.org — business profiles with years in operation

# Step 5: Go direct to local county clerk for assumed name/business certificates
# Business certificates (DBAs) are filed at the county level, not just state
# Search the county clerk's online records for the operating county
```

**UCC Portal Search (when state DOS is down):**

The UCC (Uniform Commercial Code) e-filing system is a different system from the corporation database, maintained separately. Even when the DOS corporation search is offline, the UCC portal may be operational:

```
URL: https://ucc-efiling.dos.ny.gov/ (NY example)
Search Type: By debtor name
What it reveals: 
  - Secured party (lender) identities
  - Equipment loans and leases
  - The exact legal entity name (used in filing)
  - Business addresses
Limitations:
  - Only shows entities with active UCC filings (liens/loans)
  - Won't show entities that never had secured debt
  - Portal may use a separate login/registration system
```

**Known NY DOS Issue (as of mid-2026):**

The NY Department of State has migrated UCC filings to a new system at `ucc-efiling.dos.ny.gov`. The old `appext20.dos.ny.gov` corporation search has been shut down with a redirect to the main DOS website. Corporation and business entity database search availability varies. If the direct search page returns "page unavailable," the system is likely still in migration. Check back or use county-level records instead.

### 2. Officer & Director Tracing

```python
# Entity → Officer discovery
officer_discovery = {
    "entity": "Acme Holdings LLC",
    "state": "DE",
    "file_number": "1234567",
    "officers_found": [
        {
            "name": "Jane Smith",
            "title": "Managing Member",
            "address": "123 Main St, Wilmington, DE"  # Often registered agent
        }
    ]
}

# Officer → Cross-Reference
cross_ref = [
    "Search officer name in other entity filings",
    "Check if officer address is registered agent mailbox",
    "Search officer in person-intel-mcp for other associations",
    "Check officer for property ownership in state",
    "Search officer for court records and litigation history"
]
```

**Patterns to Detect:**
```
- Same person → many LLCs → professional registered agent or serial entrepreneur
- Same address → multiple entities → shared office or shell address
- Registered agent address ≠ business address → intentional concealment
- Out-of-state officers → tax optimization, not necessarily concealment
- Recent officer changes → restructuring or avoidance behavior
```

### 3. Beneficial Ownership Tracing (Corporate Veil)

```python
# Methodology for identifying beneficial owners
layers = {
    "layer_0": "Target entity (The Target LLC)",
    "layer_1": "If owned by another entity → search that entity",
    "layer_2": "If owned by trust → identify trustee and beneficiaries",
    "layer_3": "If owned by foreign entity → check FEIN, registered agent",
    "final": "Track until you reach: natural person(s) or foreign entity"
}
```

**Techniques:**
```bash
# 1. Follow the registered agent — often connects multiple shell companies
# Search agent name at State SOS to find all entities they represent

# 2. Follow the address — shared address = shared ownership or management
# Check property records for the address

# 3. Look for SEC Schedule 13D/13G filings (5%+ ownership disclosures)
# https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany

# 4. Check UCC filings (secured transactions reveal lenders + asset ownership)
# Search by debtor name: https://www.secstates.com/UCC-Search

# 5. Look for IRS Form 990 (nonprofits disclose donors/board)
# https://projects.propublica.org/nonprofits/

# 6. CTA (Corporate Transparency Act) — as of 2024, many new entities must
#    report beneficial owners to FinCEN (law enforcement access only)
```

### 4. SEC EDGAR Filings (Public Companies)

```bash
# Search by company name
curl -s "https://www.sec.gov/cgi-bin/browse-edgar?\
action=getcompany&\
company=Apple&\
owner=exclude&\
count=10" | grep -E "href.*/Archives/"

# Common filing types:
# - 10-K: Annual report (business overview, risks, financials)
# - 10-Q: Quarterly report (financial updates)
# - 8-K: Current report (material events - acquisitions, exec changes)
# - DEF 14A: Proxy statement (executive compensation, board nominees)
# - Form 4: Insider trading (officer/director stock transactions)
# - Form 13F: Institutional investment managers (quarterly holdings)
# - S-1: Initial registration (IPO, new security offering)
# - Schedule 13D/13G: 5%+ beneficial ownership
```

**Key EDGAR Extraction Patterns:**
```python
# Proxy Statement (DEF 14A) reveals:
# - Executive compensation (salary, bonus, stock awards)
# - Board of directors (names, bios, other boards)
# - Related party transactions
# - Auditor and audit committee

# Form 4 reveals:
# - Insider buying/selling patterns
# - Option exercises
# - Date of transactions (proximity to news events)
```

### 5. Government Contracts (SAM.gov)

```bash
# Search for federal contractors
# navigate_page to: https://sam.gov/content/opportunities

# API-based search (requires SAM.gov account)
curl -s "https://api.sam.gov/prod/opportunities/v1/search\
?api_key=YOUR_API_KEY\
&limit=10\
&q=technology+services" | jq .

# Entity registration search (replaces CCR)
# https://sam.gov/search?index=entity
```

**What SAM.gov reveals:**
```
- Entity registration status and expiration
- Business type (small business, woman-owned, HUBZone, etc.)
- NAICS codes (type of business)
- Points of contact (names, phone, email)
- Past performance references
- Exclusions (suspensions, debarments) — critical red flag
- CAGE code (unique identifier for federal contractors)
```

### 6. Trademark & Intellectual Property

```bash
# USPTO trademark search
# https://www.uspto.gov/trademarks/search
# Or use TSDR API

curl -s "https://tsdr.uspto.gov/tsdr/api/v1/status/\
?requestId=TEST" 2>&1

# What trademarks reveal:
# - Business activities and product lines
# - Ownership changes (trademark assignments)
# - Geographic scope of business
# - Dates of first use (trading history)
```

### 7. Company Leadership & Management Discovery (via Search Engines)

When state SOS databases are unavailable and you need to identify who runs a company.

**Technique:** Multi-engine search + Chrome DevTools MCP evaluate_script

```
# When all search engines block automated requests with captcha/Cloudflare:
# The challenge overlay is visual-only — the underlying DOM still has the data.
# Use evaluate_script to extract rendered text that the snapshot misses:
evaluate_script(function: "() => { return document.body.innerText.substring(0, 10000); }")
```

**Step-by-step:**
1. **Identify correct company name** — the user's recollection may be imprecise. Try `"Michaels Group Homes"` vs `"Michael's Group Builders"`. Search without quotes, try related terms (`homes`, `builders`, `construction`), add geography.
2. **Navigate to company website** — look for `/about-us`, `/our-team`, `/team-detail/`, `/leadership`, `/management` for bios and contact info.
3. **Search engine discovery** — try DuckDuckGo (least blocked), then Bing, then Google. Extract rendered text with `evaluate_script` when captcha'd.
4. **Cross-reference directories** — RocketReach (org chart), Blue Book (key contacts), BuildZoom (license info), BBB (profile), LinkedIn (titles/tenure), Yelp (ownership).
5. **Verify across multiple sources** — a single source may be outdated. Cross-reference 2-3 sources to confirm.

See `references/company-leadership-research.md` for the full workflow with source-specific details, captcha bypass techniques, team-page URL pattern discovery, Instagram OSINT for small businesses, employee-by-first-name search techniques, and common pitfalls including name collision with national brands and LinkedIn authwall workarounds.

### 7b. Cross-Referencing Merchant/POS Data with Entity Records

When you have access to a business's internal systems (POS, payment processing, ordering platforms, loyalty programs) through a security assessment or authorized audit:

**Data available in POS systems (e.g., Clover, Toast, Square):**
- Merchant legal name and DBA
- Owner name, email, phone
- Employee list with roles, PINs, emails
- Business address and service address
- Payment processor and gateway config
- Tax ID / EIN (sometimes)
- Creation date of merchant account
- Reseller/sales partner information

**Cross-referencing POS data with public records:**
```
# 1. Merchant name → Search state SOS
# Use the exact legal name from the POS merchant record

# 2. Owner email domain → Check for related domains
# bob@omega-mfg.example → check omega-mfg.example

# 3. Employee email domains → Confirm family/business relationships
# pam@omega-mfg.example, robert@omega-mfg.example = same family/org

# 4. Owner name → Cross-reference with obituary if suspected deceased
# Check death date against merchant activity dates

# 5. Reseller ID → May identify the sales partner who has the signed application
```

```bash
# START: ABC Properties LLC (owns 123 Main St)
# ↓
# Step 1: Search state SOS for ABC Properties LLC
# → Managed by: ABC Management Inc.
# → Registered Agent: CorpServ Inc. (commercial registered agent)
# ↓
# Step 2: Search ABC Management Inc.
# → Officers: John Smith (President), Jane Smith (Secretary)
# → Both addresses: 456 CorpServ Lane, Wilmington, DE
#   (registered agent address — not real)
# ↓
# Step 3: Search John Smith + Jane Smith across ALL entities
# → Also officers of: Smith Family Trust (formed 2018)
# → Also officers of: J&J Holdings LLC (formed 2020)
# ↓
# Step 4: Search Smith Family Trust
# → Trustee: John Smith
# → Principal address: 789 Oak Ave, Portland, OR (real address!)
# ↓
# Step 5: Geocode 789 Oak Ave
# → This is the beneficial owner's actual residence
# ↓
# RESULT: John and Jane Smith are the beneficial owners of
# ABC Properties LLC, through ABC Management Inc. as manager,
# using CorpServ as registered agent for privacy.
```

## Example Commands

### Firefox DevTools — State SOS Search

```
# Search Delaware (most common for LLCs)
navigate_page("https://icis.corp.delaware.gov/Ecorp/EntitySearch/NameSearch.aspx")
fill_by_uid(uid="entity_name_input", value="ABC Properties")
click_by_uid(uid="search_button")
take_snapshot(selector="#resultsTable")
```

### OpenCorporates API

```bash
# Search by company name
curl -s "https://api.opencorporates.com/v0.4/companies/search\
?q=acme+holdings&jurisdiction_code=us_de" | jq '.results[] | {name, incorporation_date, company_type, status}'
```

### Bulk Entity Search Script

```bash
# Search multiple entities across states
for entity in "Entity1 LLC" "Entity2 Inc" "Entity3 LP"; do
  echo "=== $entity ==="
  # Call state SOS API or scraping logic
  python search_entity.py "$entity" --state de
  sleep 1  # Rate limiting
done
```

## Common Pitfalls

### Registered Agent Address Confusion
- **PITFALL**: The address on the entity filing is often the registered agent's address, not the business address.
- **SOLUTION**: Look for "Principal Address" or "Business Address" separately from "Registered Agent" address.
- **WORKAROUND**: Check property records for the entity name — that reveals real property addresses.

### Stale Entity Data
- **PITFALL**: Entity may be dissolved, suspended, or merged.
- **SOLUTION**: Always check entity status (Active/Suspended/Dissolved) on the SOS site.
- **WORKAROUND**: Look for "Statement of Information" or "Annual Report" filing dates to check recency.

### Name Similarity
- **PITFALL**: "ABC Holdings LLC" and "ABC Holding LLC" may be different entities.
- **SOLUTION**: Entity file number is the unique identifier, not the name.
- **WORKAROUND**: If file number is unknown, try exact name match, then partial search.

### Foreign Entity Complications
- **PITFALL**: Entity formed in Delaware but operating in California — needs registration in both states.
- **SOLUTION**: Search both "state of formation" and "qualification to do business" (foreign entity registration).
- **WORKAROUND**: Check "Foreign" entity filings in the operating state.

### Shell Company Detection Limits
- **PITFALL**: CTA (Corporate Transparency Act) beneficial ownership data is NOT public — law enforcement only.
- **SOLUTION**: Use indirect methods (address chains, agent connections, asset tracing).
- **WORKAROUND**: Cannot definitively identify all beneficial owners from public data alone.

### Trademark Conflicts
- **PITFALL**: Entity name and trademark owner may differ.
- **SOLUTION**: Trademarks are registered by brand name, not legal entity name necessarily.
- **WORKAROUND**: Search both entity name AND brand/trade name.

## Legal & Ethical Notes

> **⚠️ WARNING**: Business intelligence raises specific legal concerns:
> - **Insider Trading**: SEC rules prohibit trading on material non-public information discovered through business intelligence
> - **Corporate Transparency Act**: New beneficial ownership reporting (2024) is NOT public — do not attempt to access FinCEN data
> - **Trade Secrets**: Business intelligence does NOT authorize access to trade secrets or proprietary information
> - **Competitive Intelligence**: Legal when using public sources; illegal when using deception, theft, or unauthorized access
> - **NDA Violations**: Information about a company may be covered by a non-disclosure agreement you've signed
> - **State Data Restrictions**: Some states restrict bulk downloading of business filings
> - **Web Scraping**: SEC.gov and OpenCorporates allow reasonable API access; SAM.gov requires API key

### Permissible Uses
- Due diligence before investment or acquisition
- Vendor risk assessment
- Litigation support (attorney-supervised)
- Journalistic investigation
- Fraud detection
- Compliance (AML/KYC screening)
- Competitive analysis (public sources only)

### Red Flag Indicators
- Frequent entity formation and dissolution
- Incomplete or inconsistent filings
- Rapid officer/director changes
- Using commercial registered agent + PO Box as only address
- Series of similarly-named entities (potential shell farm)
- Entity status problems (suspended, forfeited)
- Federal exclusion (SAM.gov debarment)
- Negative press or regulatory actions

## Reference Files

- `references/ny-business-entity-search.md` — New York State business entity search methodology covering DOS database, UCC portal, NY Open Data, and county clerk alternatives when state systems are down.
- `references/fl-sunbiz-entity-search.md` — Florida Sunbiz entity search methodology covering direct URL search, status code meanings, fuzzy matching pitfalls, and the Chrome DevTools MCP evaluate_script technique for efficient batch lookups.
- `references/company-leadership-research.md` — Multi-engine search strategy for finding company leadership/management when state SOS databases are down. Covers company name disambiguation, captcha/Cloudflare bypass via Chrome DevTools MCP evaluate_script, cross-referencing directories (RocketReach, Blue Book, LinkedIn, BBB, BuildZoom), parallel search across DuckDuckGo/Bing/Google, trade association member directories (CRBRA) for local builder/contractor research, employee-by-first-name search, and phonetic name matching for business names from spoken input.
- `references/corporate-family-tree-mapping.md` — Multi-entity corporate deep dive pattern for mapping parent companies, subsidiaries, sister entities, and umbrella holdings. Covers Playwright MCP multi-tab browser navigation, AI Overview orientation, family tree construction from About/Footer/Portfolio pages, founder lineage profiling, and same-name disambiguation across separate entities (worked example: BBL Companies family tree).

## Cross-References

- `security/osint-recon` — Full investigation pipeline including business intelligence
- `security/osint-person` — Tracing officers/directors back to natural persons
- `security/osint-property` — Connecting business entities to property ownership
- `security/osint-threat` — Checking entities against sanctions lists and threat databases
- `security/osint-redteam` — Entity reconnaissance for social engineering vectors
- `software-development/systematic-debugging` — Structured approach to complex ownership chains

## Verification Checklist

- [ ] Entity identified with file number and state of formation
- [ ] Entity status confirmed (Active/Suspended/Dissolved)
- [ ] Officers/directors/members extracted
- [ ] Registered agent identified (commercial or individual)
- [ ] Principal business address obtained (not registered agent address)
- [ ] Cross-reference search of officers across other entities performed
- [ ] SEC EDGAR searched (if public company)
- [ ] SAM.gov searched (if government contractor)
- [ ] USPTO trademark search performed
- [ ] Beneficial ownership traced as far as publicly possible
- [ ] UCC filings checked for secured assets
- [ ] Legal constraints documented
- [ ] Confidence level assigned to ownership chain
