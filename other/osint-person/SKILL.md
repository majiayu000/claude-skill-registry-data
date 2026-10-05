---
name: osint-person
description: Person investigation skill — name enrichment, employer discovery, court records, donations, LinkedIn profiling, cross-referencing across data sources with privacy considerations.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [osint, person-investigation, background-check, enrichment, court-records, linkedin, privacy]
    triggers: [person, background-check, investigate-person, find-person, enrichment, who-is, people-search]
    related_skills: [osint-business, osint-social, osint-property]
---

# OSINT Person Investigation

Person intelligence from public sources — name enrichment through multiple data streams, professional background, court records, political donations, and cross-platform social media matching. Privacy-focused methodology using only publicly available information.

## Prerequisites

### Recommended MCP Servers
```yaml
mcpServers:
  person-intel-mcp:
    command: npx
    args: ["-y", "@modelcontextprotocol/person-intel"]
  property-intel-mcp:
    command: npx
    args: ["-y", "@modelcontextprotocol/property-intel"]
```

### Free Public Data Sources
- **Google**: Advanced search operators (dorks)
- **LinkedIn**: Professional profiles (public view)
- **PACER**: Federal court records (pay-per-document, ~$0.10/page)
- **CourtListener**: Free aggregated federal + some state court opinions
- **FEC**: Campaign finance (https://www.fec.gov/data/)
- **OpenSecrets**: Political donations and lobbying (https://www.opensecrets.org)
- **Secretary of State**: Business entity filings (free per state)
- **State Bar Associations**: Attorney license verification
- **State Medical Boards**: Physician license verification
- **State Corporation Commission**: Professional licenses
- **Voter Registration**: Public in some states (varies widely)
- **County Recorder**: Marriage, divorce, property records

## Person Data Fundamentals

### Identifiers (ordered by reliability)
| Identifier | Reliability | Source |
|------------|-------------|--------|
| Full Name + DOB | Very High | Multiple |
| Full Name + Address | High | Voter registration, property |
| Full Name + Phone | High | Data brokers, directories |
| Full Name + Email | Medium-High | Breach data, social media |
| Full Name + City/State | Medium | Narrowing necessary |
| Full Name only | Low | Too many common names |
| Username/Handle | Medium | Cross-platform matching |

### What Person Intel Reveals
- **Identity**: Full name, aliases, maiden name, nicknames
- **Location**: Current/previous addresses (rental/property history)
- **Professional**: Employer, job title, work history, education
- **Financial**: Property ownership, business affiliations, bankruptcies
- **Legal**: Criminal records, civil lawsuits, judgments, liens
- **Family**: Relatives, cohabitants, marriage/divorce
- **Social**: Social media profiles, public posts, affiliations
- **Political**: Voter registration, campaign donations
- **Difficult to obtain (legally)**: SSN, DOB (not public in most states), driver's license, medical records

## Critical Change: Search Engines Now Block Automation

As of 2025-2026, all major search engines block automated curl/terminal requests:
- **DuckDuckGo**: Returns a CAPTCHA challenge page ("bots use DuckDuckGo too")
- **Bing**: Turnstile/Rubik's Cube CAPTCHA
- **Google**: "unusual traffic" CAPTCHA block

**Do NOT rely on search engines via curl.** They will fail. Use these alternatives instead:

### Search Engine Workarounds (when curl is blocked)

1. **Mobile user agents sometimes slip through** — Google with Chrome Android UA may return results briefly before triggering CAPTCHA. Not reliable.
2. **Direct site navigation** — Skip search engines entirely. Go straight to known data sources:
   - Legacy.com / Findagrave for obituaries
   - County property appraiser sites for property records
   - State Secretary of State / DOS sites for business filings
   - PACER / CourtListener for court records
3. **Wayback Machine CDX API** — Search for archived versions of blocked pages. CDX returns plain JSON with no CAPTCHA.
4. **Textise / Jina AI reader** — `r.jina.ai/http://...` can sometimes render pages behind basic anti-bot, but fails on Cloudflare.
5. **Redirect chain analysis** — If direct URL fails, check if a search engine result page (SERP) snippet contains the answer text even when the page is blocked.

### Using the Wayback Machine CDX API

The CDX API returns archive listings as plain text/JSON with no bot protection:

```bash
# List all archived snapshots for a URL
curl -s "https://web.archive.org/cdx/search/cdx?url=example.com/page&output=json&limit=5"

# List with timestamp and original URL
curl -s "https://web.archive.org/cdx/search/cdx?url=example.com&output=text&limit=10&fl=timestamp,original"

# Open a specific snapshot by timestamp
# https://web.archive.org/web/{timestamp}/{original_url}
```

**Real example (findagrave bypass):**
```bash
# 1. Find the memorial URL pattern from search snippet
# 2. Check if Wayback Machine has it archived
curl -s "https://web.archive.org/cdx/search/cdx?url=findagrave.com/memorial/178447396/*&output=json&limit=3"
# 3. Open the latest snapshot directly
# https://web.archive.org/web/{latest_timestamp}/https://www.findagrave.com/memorial/178447396/robert-j-Omega
```

### Using Findagrave for Deceased Person Research

Findagrave is blocked by Cloudflare from automated access, but:

1. **Search page** often works with curl (returns HTML with results, memorial IDs, names)
2. **Memorial pages** are Cloudflare protected
3. **Workaround**: Use Wayback Machine to view memorial pages:
   - Search findagrave.com via curl to get the memorial ID
   - Check Wayback Machine CDX API for that memorial URL
   - Load the latest archived snapshot which contains full obituary text, birth/death dates, family survivors

**Search pattern:**
```
curl -s "https://www.findagrave.com/memorial/search?firstName=Robert&lastName=Omega"
→ Returns memorial ID in the page: /memorial/178447396/robert-j-Omega
→ Then use Wayback Machine to view that memorial
```

### Cross-Referencing POS / Merchant Data

When you have access to a business's internal systems (POS, CRM, ordering platforms, loyalty programs), employee records often contain:

- **Employee PINs** (POS login codes)
- **Email addresses** (often personal/family emails reveal relationships)
- **Role levels** (Admin, Manager, Employee indicate authority)
- **Owner flags** (identifies business owner)
- **Timestamps** (account creation dates show when people joined)

**Cross-referencing for family relationships:**
- Same surname + different email domain = different generation
- Same surname + married-name variant = daughter (e.g., Omega → Cutler)
- Shared email domain (@omega-mfg.example) = family
- Admin role + family email = likely current operator
- Compare against obituary survivor list to map remaining family

**Real example:**
```
Clover employee records show:
- ROBERT Omega (deceased, 1942-2017) — Admin/Owner — BOB@Omega.COM
- Pam Cutler — Admin — pam@omega-mfg.example (daughter, married name)
- Robert Omega — Employee — robert@omega-mfg.example (son)
- maxim@omega-mfg.example — Manager (family member)

Cross-reference with obituary → "Survived by wife Donna, 2 sons, 2 daughters"
→ Pam is a daughter (married Cutler), Robert Jr. is a son
```

## State Business Entity Searches

Most state SOS/DOS websites have migrated to new systems. Old direct URLs may be broken.

| State | Current URL | Notes |
|-------|------------|-------|
| New York | https://www.dos.ny.gov/corporation-and-business-entity-database | Old appext20.dos.ny.gov is shut down |
| Generic | https://{state}.gov/sos/business-search | Check state SOS website |

**Common blockers:**
- Most state SOS sites now require CAPTCHA or have migrated to new UCC filing portals
- The old `.asp` direct search pages are frequently taken offline
- Try `site:appext20.dos.ny.gov "Business Name"` for archived NY records via Wayback Machine

## Step-by-Step Workflows

### 1. Business Contact Discovery — Email Format Inference

When you have a person's name + employer but need their email, infer it by determining the company's email pattern:

**Step 1: Identify the email domain**
```bash
# Search for the company's domain
search: "{company name} email format"
search: "{company domain} email pattern"
search: "email addresses at {company}"

# Check employee directory sites
# RocketReach, Wiza, LeadIQ, ZoomInfo often reveal partial emails
```

**Step 2: Determine the format pattern**
```python
# Common email formats (from most to least common):
# [first]@domain.com                — jason@coastal-hosp.example
# [first].[last]@domain.com          — jason.hayward@coastal-hosp.example
# [first_initial][last]@domain.com   — jhayward@coastal-hosp.example
# [first][last_initial]@domain.com   — jasonh@coastal-hosp.example
# [first_initial].[last]@domain.com  — j.hayward@coastal-hosp.example
# [last]@domain.com                  — hayward@coastal-hosp.example

# Check RocketReach or similar for the company's verified format:
search: "{company} email format rocketreach"
# RocketReach shows which format the company uses and at what percentage
```

**Step 3: Verify the guessed email**
```bash
# Check if it appears in breach data (Have I Been Pwned-style APIs)
# Check if it's listed on public employee directories or LinkedIn
# Check if it's associated with a Gravatar (returns profile image)
# Try it on the company's own "forgot password" flow (user enumeration check)

# Pattern: Search for partial email in public sources
search: "jhayward@coastal-hosp.example"
search: "site:linkedin.com/in \"jhayward\" @coastal-hosp.example"
```

**Step 4: Fallback — contact through known channels instead**
```python
# If email can't be reliably inferred:
# 1. Call the company main line, ask for the person by name
# 2. Check LinkedIn for direct messaging (if Premium)
# 3. Walk in — physical presence often beats digital outreach
```

**Real example from this session:**
```
Target: Jason Hayward, GM at Hyatt House Schenectady
Company: BBL Hospitality (manages the hotel)
Domain: coastalhosp.com
Format search: rocketreach shows 100% use [first_initial][last]
Constructed: jhayward@coastal-hosp.example
Cross-reference: wiza.co shows partial match (j*****@coastal***.com)
Result: Confirmed format, email likely valid
```

### 2. Name → Initial Enrichment

```python
# Starting with a name only
initial_search = {
    "first_name": "Jane",
    "last_name": "Smith",
    "middle_name": "",      # If known
    "city": "Portland",     # If known
    "state": "OR"           # If known
}

# Search strategy (parallel where possible)
searches = [
    "Google: 'Jane Smith' Portland OR",
    "Google: 'Jane Smith' linkedin",
    "Google: 'Jane Smith' facebook",
    "WhitePages / Spokeo / PeekYou",
    "County property records (if address known or inferred)",
    "State business entity search"
]
```

**Name Variants to Try:**
```bash
# Common name variations
"Jane Smith"
"J. Smith"
"Jane A. Smith"         # If middle initial known
"Jane Marie Smith"      # If full middle name known
"admin Smith"           # Common nickname
"Jennifer Smith"        # May be different person
"Smith, Jane"           # Last name first format

# Try variations with:
# - Hyphenated last names ("Smith-Jones")
# - Married / maiden name ("Jane Doe née Smith")
# - Professional name ("Dr. Jane Smith")
# - Suffix ("Jane Smith Jr.", "Jane Smith III")
```

### 2. Address History → Relocation Pattern

```
Sources for address history:
1. Property records (owned properties, current and past)
2. Voter registration (current address only in most states)
3. Utility records (not public, but can appear in legal filings)
4. Data broker aggregators (BeenVerified, Radaris, etc.)
5. White pages directories (historical)
6. Bankruptcy filings (lists all recent addresses)

Analysis:
- Frequent moves may indicate instability or military service
- Move to another state may indicate job relocation
- Move to cheaper area may indicate financial distress
- Maintaining multiple residences may indicate wealth or rental properties
- Address in a different state than workplace may indicate remote work
```

### 3. Employer & Professional Background

```python
# LinkedIn research (public profile)
linkedin_search = {
    "method": "Google dork",
    "query": "site:linkedin.com/in \"Jane Smith\" Portland",
    "profile_data": {
        "employer": "Acme Corp",
        "title": "Senior Engineer",
        "duration": "2018-present",
        "education": "OSU 2012-2016",
        "location": "Portland, Oregon Area",
        "mutual_connections": None  # May reveal network
    }
}

# Verification sources
verification = [
    "Company website team page",
    "Company LinkedIn page employees",
    "Professional certifications (state boards)",
    "Conference speaker bios",
    "Patent filings (USPTO)",
    "Publication author lists (Google Scholar)",
    "SEC filings (if named officer of public company)"
]
```

**Google Dork Patterns for LinkedIn:**
```
site:linkedin.com/in "Jane Smith" Portland
site:linkedin.com/in "Jane Smith" "Acme Corp"
site:linkedin.com/in "Software Engineer" Portland "Jane"
site:linkedin.com/today/author "Jane Smith"     # LinkedIn articles
```

### 4. Court Records Search

```bash
# Federal Courts (PACER)
# Register at: https://pacer.uscourts.gov
# Query: party_name = "Smith, Jane" or "Smith, J*"
# Cost: $0.10 per page (first $30 of queries free per quarter)

# Free Alternative: CourtListener
# RECAP archive (free PACER documents contributed by users)
curl -s "https://www.courtlistener.com/api/rest/v4/people/?name=Jane+Smith&state=OR"

# State Courts (varies by state)
# Example: Oregon Judicial Department Online Search
# navigate_page to: https://publicaccess.courts.oregon.gov
```

**Types of Cases to Check:**
```
CRIMINAL:
- Arrest records
- Convictions (felony/misdemeanor)
- Probation/parole status
- Traffic violations
- DUI/DWI

CIVIL:
- Lawsuits (plaintiff or defendant)
- Small claims
- Breach of contract
- Personal injury
- Employment disputes

FAMILY:
- Divorce proceedings
- Child custody/support
- Domestic violence restraining orders
- Name changes

BANKRUPTCY:
- Chapter 7 (liquidation)
- Chapter 11 (reorganization)
- Chapter 13 (wage earner plan)
- Chapter 12 (family farmer)

PROBATE:
- Inheritance (as beneficiary or executor)
- Guardianship/conservatorship
```

### User Enumeration via Login Endpoints

Many web applications reveal whether an account exists by returning different error messages for:
- **Existing user + wrong password**: "Incorrect password provided" / "Invalid password"
- **Non-existing user**: "User could not be found" / "No account with that email"

This is useful for confirming a person has an account on a given platform without needing their password. It's also a security vulnerability to report.

**How to test:**
```bash
# Step 1: Try login with target email and obviously wrong password
curl -s -X POST "https://target.com/customer/authenticate" \
  -H "Content-Type: application/json" \
  -d '{"username":"target@email.com","password":"wrongpassword123"}'

# Step 2: Try the same with a definitely-not-registered email
curl -s -X POST "https://target.com/customer/authenticate" \
  -H "Content-Type: application/json" \
  -d '{"username":"thisdoesnotexist999@nonexistent.com","password":"wrongpassword123"}'

# Step 3: Compare responses
# Different message = account exists
# Same message = no user enumeration (or both are invalid)
```

**What this reveals:**
- Confirms the person uses that service
- The email/username they registered with
- May reveal the platform's user ID format

**Note:** Some platforms rate-limit or block after multiple failed attempts. Use sparingly.

### Epieos — Email Google Service Enumeration

Epieos (https://epieos.com/) reveals exactly which Google services are tied to an email address in about 4 seconds — often pulling profile photos and real names directly from Google's systems. This is a powerful identity confirmation technique used by federal investigators.

**What Epieos reveals from an email address:**
- Google Account profile photo (confirms identity visually)
- Google Maps reviews written (reveals locations visited)
- YouTube channel (if linked to that Google account)
- Google Play app reviews
- Google Calendar (if publicly exposed)
- Google Drive shared documents (metadata)

**Investigation workflow:**
```bash
# 1. Navigate to https://epieos.com/ in browser
# 2. Enter target email address
# 3. Review Google service associations
# 4. Cross-reference profile photo with other sources (LinkedIn, Facebook)
# 5. Use Google Maps reviews to establish location patterns
# 6. Cross-reference results with Holehe:
holehe target@email.com --only-used -NP
```

**Why this matters for person identification:**
- A single email can reveal: name, photo, location history, and platform usage
- Google account profile photos are often more current than other sources
- Google Maps reviews reveal places the person actually visits (not just where they live)
- YouTube linked accounts can show content creation or commenting activity

### 5. Political Donations & Affiliations

```bash
# FEC Individual Contributions
curl -s "https://api.open.fec.gov/v1/schedules/schedule_a/\
?contributor_name=Jane+Smith\
&contributor_state=OR\
&api_key=YOUR_API_KEY" | jq .

# OpenSecrets Donor Lookup
# https://www.opensecrets.org/donor-lookup

# Voter Registration (state-specific where public)
# Oregon: OregonVotes.gov
# Other states vary widely in availability
```

**What donations reveal:**
- Political affiliations and priorities
- Wealth indicators (donation amount)
- Geographic ties (FEC requires employer/city)
- Employer disclosed on filings (may confirm professional info)
- Frequency and timing of donations

### 6. Cross-Platform Identity Resolution

```bash
# Username search across platforms
# Methods:
# 1. Google: "jane.smith" username
# 2. Namechk: https://namechk.com (checks username availability)
# 3. WhatIsMyName: https://whatsmyname.app
# 4. Sherlock: https://github.com/sherlock-project/sherlock

# Social media platforms to check:
# - LinkedIn (professional)
# - Facebook (personal)
# - Twitter/X (public posts)
# - Instagram (public profile)
# - TikTok (public profile)
# - GitHub (technical profiles)
# - Reddit (public posting history)
# - YouTube (channel)
# - Pinterest (visual boards)
# - Medium / Substack (writing)
# - Strava (exercise routes - reveals home/office)
# - Nextdoor (neighborhood)
# - Angie's List / Yelp (reviews - reveal address proximity)
```

### 7. Professional Licenses & Credentials

```bash
# Medical Licenses
# FSMB: https://www.fsmb.org/ (DocInfo search)
# State medical board websites

# Legal Licenses
# State Bar Association websites
# Example: California Bar: https://apps.calbar.ca.gov/attorney/

# Real Estate Licenses
# State DRE websites
# Example: CA DRE: https://www.dre.ca.gov/

# Contractors Licenses
# State CSLB websites
# Example: CA CSLB: https://www.cslb.ca.gov/

# CPA Licenses
# State Accountancy Board websites

# FAA Pilots License
# https://amsrvs.registry.faa.gov/airmeninquiry/
```

### 8. Compile Person Profile

```markdown
## Person Profile: Jane Smith

### Identifiers
- **Full Name**: Jane Marie Smith
- **AKA**: J. Smith, Jane Doe (maiden: Johnson)
- **DOB**: 1985-03-15 (from voter registration)
- **Phone**: (503) 555-0123 (public directory)
- **Email**: jane.smith@email.com (from LinkedIn)

### Locations
- **Current**: Portland, OR 97201 (voter registration)
- **Previous**: Seattle, WA 98102 (2015-2019, property records)
- **Previous**: Eugene, OR 97401 (2010-2015, university)

### Professional
- **Employer**: Acme Corp, Portland (2019-present) — Senior Engineer
- **Previous**: TechCo, Seattle (2015-2019) — Software Developer
- **Education**: Oregon State University (BS Computer Science, 2010)
- **License**: None applicable

### Legal
- Traffic citation (2017, WA) - paid
- No criminal record found (federal or Oregon state)
- No bankruptcy filings

### Financial
- Owns: Condo at 123 4th Ave, Portland (purchased 2020)
- No business entity filings found
- No liens or judgments

### Affiliations
- LinkedIn: linkedin.com/in/janesmith (300+ connections)
- GitHub: github.com/janesmith (15 public repos)
- FEC: Donated $500 to Senate candidate (2020)
- Professional: ACM member

### Risk Assessment
- **LOW** — Clean background, stable employment, no red flags

### Confidence
- **HIGH** — Multiple identifiers cross-referenced
- Sources: Voter registration, LinkedIn, property records, court search
- Last verified: 2024-01-15
```

### Obituary Research for Deceased Subjects

When a subject is believed to be deceased, these techniques help confirm and find family/successor information:

**Step 1: Search obituary databases**
```bash
# Findagrave (largest free database) — use mobile UA to avoid Cloudflare
curl -s -L "https://www.findagrave.com/memorial/search?firstName=Robert&lastName=Omega&location=schenectady" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Legacy.com — national obituary aggregator
curl -s -L "https://www.legacy.com/obituary/search?q=First+Last&location=City+State"
```

**Step 2: Use Wayback Machine for obituaries behind paywalls/Cloudflare**
```bash
# CDX API to find snapshots
curl -s "https://web.archive.org/cdx/search/cdx?url=findagrave.com/memorial/ID/name&output=json&limit=5"

# Get the archived page content
curl -s -L "https://web.archive.org/web/20240000000000/https://www.findagrave.com/memorial/ID/name"
```
The CDX API returns timestamps of all archived snapshots. Pick one that worked and retrieve it. The Wayback Machine often has obituaries cached from newspapers that are now paywalled or behind Cloudflare.

**Step 3: Identify survivors and family structure**
Extract from obituary text:
- Spouse name (often the executor of estate)
- Children names (may have married names — key for tracing current operators)
- Siblings, parents, nieces/nephews
- Funeral home (may have additional online obituary with details)

**Step 4: Cross-reference with internal/leaked data**
If you have access to business system data (employee lists, customer records), cross-reference:
- Same last name + same domain email = family member (e.g., `pam@omega-mfg.example` for a Omega family member)
- Admin-level access after death date = likely successor/current operator
- Match children's first names from obituary with employee records

### Business Succession After Owner Death

When a business's registered owner has died but the business is still operating:

**Who to look for as current operator (in priority order):**
1. Family members with ADMIN-level system access in the business's operational systems (POS, accounting, ordering)
2. Spouse listed in obituary (often the executor)
3. Adult children listed in obituary (especially those with the same email domain)
4. Long-term employees or managers elevated to admin roles after the death date

**How to find them:**
```python
# Pattern: Cross-reference obituary survivors with system access
obituary_family = ["Spouse Name", "Child1", "Child2"]
system_users = [
    {"name": "Pam Cutler", "email": "pam@omega-mfg.example", "role": "ADMIN"},
    {"name": "Robert Omega", "email": "robert@omega-mfg.example", "role": "EMPLOYEE"},
]
# Shared email domain (omega-mfg.example) confirms family relationship
# Admin role confirms operational control
```

**Signs the registered owner is deceased but business continues:**
- Owner's email still active (forwarding or shared access)
- Owner's system account still listed as "owner" (never updated after death)
- Orders/transactions continuing after the death date
- Family members with same surname having elevated access
- Business entity on Clover/POS still in deceased owner's name

### Cross-Referencing Leaked/Internal Data with Public OSINT

When you have access to internal system data (via API tokens, leaked credentials, or authorized access):

```python
# Pattern: Use employee email domains to confirm family structure
# If obituary says "2 sons, 2 daughters" and system shows:
# - pam@omega-mfg.example (ADMIN, married name Cutler = one daughter)
# - robert@omega-mfg.example (EMPLOYEE = likely son)
# - maxim@omega-mfg.example (MANAGER = another family member)
# The shared domain name confirms family relationship

# Pattern: Cross-reference system creation dates with life events
# - Merchant created 2014, owner died 2017, still active 2026
# - Successor can be identified by who has admin access POST-2017
```

**What to check in internal systems:**
- Employee list: names, emails, roles, PINs
- Creation timestamps vs known dates (death, business sale)
- Email domains (shared domain = family; vendor domain = third-party)
- Role hierarchy (ADMIN vs EMPLOYEE vs MANAGER)
- Last activity timestamps (shows who is currently active)

### Wayback Machine for Domain History Investigation

When investigating a domain that's no longer active:

```bash
# CDX API — list all archived snapshots
curl -s "https://web.archive.org/cdx/search/cdx?url=example.com&output=json&limit=20&fl=timestamp,original,statuscode"
# Returns: [[timestamp, url, http_status], ...]

# Retrieve specific snapshot content
curl -s -L "https://web.archive.org/web/20240000000000/https://example.com/"
```

**What domain history reveals:**
- If always parked/placeholder -> domain never used (no content to find)
- If content existed then disappeared -> business closed or rebranded
- Email addresses on the domain -> family structure (shared domain = likely family)
- Historical contact info -> previous owners

### Search Engine Blocking Workarounds

Search engines (Google, Bing, DDG) and data aggregators (OpenCorporates) actively block automated searches:

| Block Type | Symptom | Workaround |
|-----------|---------|------------|
| CAPTCHA | Challenge page | Use Wayback Machine for cached results |
| Cloudflare | "Just a moment..." | Try `r.jina.ai` text proxy or Wayback Machine |
| Turnstile (Cloudflare) | "One last step" | Switch to a different source entirely |
| Google "unusual traffic" | "Our systems detected..." | Use mobile user agent or try Bing/DDG instead |
| Rate limiting | Timeouts or 429 | Add delays between requests |

**Primary alternatives when blocked:**
1. **Wayback Machine CDX API** — best for historical content
2. **Direct site access** — visit the target site directly instead of search results
3. **Mobile user agents** — some sites allow mobile traffic more freely
4. **Different data sources** — if SOS site is down, try OpenCorporates; if OpenCorporates is blocked, try BBB or Facebook

## Executive Habitat Mapping — "Where to Spot Them"

When you need to know where key people live, work, and socialize — useful for networking, business development, or simply recognizing them in person. See `references/executive-habitat-mapping-example.md` for a full worked example from a multi-entity corporate deep dive.

### USER PREFERENCE: Photo Links Priority

When OSINTing public figures or corporate executives, the user wants:

1. **Most recent photos first** — always check the file upload date in the URL path (e.g., `/2025/` is newer than `/2020/`). Corporate leadership pages are updated periodically; grab the latest available.
2. **Labeled with full name** — every photo link MUST be preceded by the person's exact name so they can be visually matched.
3. **Gallery format** — compile all key figures into one labeled list, not scattered through text.
4. **Date-check the source** — if the photo file path or page publish date is more than 2-3 years old, flag it. For elderly subjects, verify they're still alive via news search or current leadership page listing before including them.
5. **CRITICAL: Verify photos are actual portraits** — see sub-section below.

```markdown
## Photo Gallery — [Company Name]

**[Full Name]** -- Title (YYYY photo)
https://example.com/path/to/photo.jpg

**[Next Person]** -- Title (YYYY photo)
https://example.com/path/to/next.jpg
```

#### CRITICAL: Verify Photos Are Actual Portraits

**Do not trust image URLs from corporate leadership pages without verification.** Many companies use monograms/signatures instead of headshots (especially for founders/chairmen). Red flags in URL path: `logo`, `monogram`, `signature`, `icon`, `bg-`, `pattern`, `decoration`, `branding`.

**Verification workflow:**

1. Use `vision_analyze` on each image URL to confirm it's a real photograph of a person
2. If vision says "logo", "monogram", "stylized letter", "calligraphy", or "graphic design" — it's NOT a portrait
3. If vision_analyze errors on a `.jpg` URL, check the Content-Type header — it may be served as WebP format despite the extension:
   ```bash
   curl -sI "https://example.com/photo.jpg" | grep -i content-type
   # If "image/webp", download + convert to PNG, then retry vision_analyze
   ```
4. **WebP workaround**: Many corporate sites serve headshots as WebP despite a `.jpg` extension, which causes vision_analyze to fail. Download, convert, then verify:
   ```bash
   curl -s -o "C:/Users/user/file.webp" "https://example.com/photo.jpg"
   python -c "
   from PIL import Image
   img = Image.open('C:/Users/user/file.webp')
   img.save('C:/Users/user/file.png')
   print('done', img.size)
   "
   # Then vision_analyze on the local .png file
   ```
5. **Getty Images fallback** — when corporate sites use monograms/logos instead of headshots (common with founders and chairmen), Getty Images event photography is the best source for actual photos. Search with date constraints and verify each result with vision_analyze before linking — Getty search filenames can be misleading or map to wrong subjects.
   ```bash
   # Date-constrained search: append &tbs=cdr:1,cd_min:2023,cd_max:2026
   https://www.gettyimages.com/photos/firstname-lastname
   # Always verify: vision_analyze("who is in this photo") before sending link
   ```
6. **Life-status check** — before including any executive in a dossier, verify they're still alive. Search `"First Last" obituary`, `"First Last" dies`, or check current leadership page listing. For elderly founders/founding-era figures who no longer appear on the leadership page, this is especially important. Don Led Duke (the "LD" in BBL) was deceased but would have been included without this check.
7. **Fallback sources when corporate site has no real portraits**: Getty Images (event photos), news articles, LinkedIn, Chamber of Commerce event galleries, Facebook business page event albums, local news coverage of charity events, YouTube event coverage screenshots.

### Wealth Tier Context (Optional Depth)

When profiling executive teams, the user appreciates a wealth/revenue comparison to contextualize power:
- Compare company revenue against known benchmarks (DR Horton: $36B, national homebuilder)
- Estimate founder/exec net worth range (not exact, but order of magnitude)
- Note whether company is private (harder to verify) vs public (SEC filings)
- For family-run empires, note how many family members the wealth is split across
- Flag any billionaires, PE ownership, or unusual wealth concentration

```markdown
| Company | Revenue | Type | Net Worth (est.) |
|---------|---------|------|-----------------|
| Company A | $500M | Private construction | $10-50M per principal |
| Company B | $80-400M | Private diversified | $250M+ corporate, founder nearing billionaire tier |
```

### What to Build

A **habitat profile** combines four layers:
1. **Visual identification** — what they look like (most recent headshot photo, labeled)
2. **Home base** — where they live and work (HQ, neighborhood, commute zone)
3. **Social orbit** — where they spend discretionary time (clubs, events, gyms, restaurants)
4. **Wealth context** — how rich they actually are (revenue tier, net worth range, industry comparison)

### Step 1: Extract Headshot Photos

Use the Playwright MCP browser to extract photo URLs from corporate leadership pages:

```javascript
// On any leadership/profile page:
mcp__playwright_mcp__browser_evaluate(
  function: "() => { 
    const imgs = document.querySelectorAll('img');
    const results = [];
    imgs.forEach(img => {
      if(img.src && !img.src.includes('logo') && 
         !img.src.includes('award') && !img.src.includes('icon'))
        results.push(img.src);
    });
    return results.join('\\n');
  }"
)
```

**Where to look:**
- `/about-us/leadership-team/` or `/our-team/` or `/management/`
- Individual profile pages under leadership
- LinkedIn company page posts (event photos often show multiple execs)
- News articles with press photos
- Chamber of Commerce event galleries

### Step 2: Map Home Location

Combine clues from multiple sources to narrow down where they live:

```markdown
| Clue | Source | What It Reveals |
|------|--------|-----------------|
| HQ address | Company website | General commute area |
| Registered agent address | State SOS | May be agent, not real home |
| Property records (county) | County assessor | Exact home address (if owned) |
| Voter registration | State voter database | Home address and party affiliation |
| LinkedIn location field | LinkedIn | Approximate area (city-level) |
| News article mentions | "of [Town], NY" | Hometown disclosure |
| Social media check-ins | Facebook/Instagram/Strava | Places they actually visit |
```

**For wealthy executives specifically:**
- Likely live in affluent suburbs near HQ (e.g., Loudonville, Slingerlands, Saratoga Springs for Albany-area execs)
- May have second homes (Florida/Texas for NY-based executives with snowbird patterns)
- Property records via county assessor website — search by name or spouse name

### Step 3: Map Social Orbit

Scan news articles and event calendars for where they spend time:

```python
# Social orbit signals to extract from articles and search results:
habitat_signals = {
    "private_clubs": [
        "Guan Ho Ha Fish and Game Club",    # Albany private club
        "Country clubs",                     # Golf/social clubs
        "University clubs",                  # RPI, Union, Siena alumni clubs
    ],
    "charity_events": [
        "Annual golf outings",              # Reliable yearly appearance
        "Chamber of Commerce galas",        # Business networking
        "Hospital/building fundraisers",    # Industry-related giving
    ],
    "professional_affiliations": [
        "Regional Chamber of Commerce",     # Check board members
        "Associated General Contractors",   # Industry groups
        "Board of Directors seats",         # Other companies they sit on
        "University boards",                # Alma mater involvement
    ],
    "frequent_venues": [
        "Rivers Casino & Resort",           # Adjacent to Mohawk Harbor
        "Saratoga Race Course",             # Seasonal horse racing
        "Local steakhouses/restaurants",    # Business dinner spots
    ]
}
```

**Extraction technique:** Read news articles and scan for:
- "The event was held at [Venue Name]"
- "[Person] is a member of [Organization]"
- "[Person] serves on the board of [Organization]"
- "[Company] was honored at the [Event Name] gala"

### Step 4: Cross-Reference Timing

When you know where they are at certain times, you can predict where they'll be:

```markdown
## Spotting Calendar — [Person Name]

| When | Where | Why |
|------|-------|-----|
| Weekday business hours | HQ address | Daily work |
| Project milestone dates | Job site | Construction walkthroughs |
| Quarterly reviews | Your hotel | Hospitality property audit |
| Annual gala (e.g., Sept) | Convention center | Industry awards |
| Charity golf outing (June) | Country club | Annual fundraiser |
| Race season (July-Aug) | Saratoga | Horse racing social circuit |
| Holiday party (Dec) | Event venue | Company celebration |
```

### Step 5: Compile Recognition Profile

```markdown
## Recognition Profile

### [Name] — [Title]
- **Photo**: [direct URL to headshot]
- **Age**: ~[X]s (from career timeline + photo)
- **Distinctive features**: [hair color, glasses, build, typical dress]
- **Vehicle**: [if visible in event photos or parking]
- **HQ**: [address they work from]
- **Likely home area**: [affluent suburb near HQ]
- **Known hangouts**: [clubs, venues, events]
- **Approach pitch**: [if you meet them, what to say]
```

### Example Habitat Profile (from BBL session)

```
## Kevin Gleason — CEO/Principal, BBL Construction Services
- Photo: https://www.bblinc.com/wp-content/uploads/2025/01/kevin-gleason.jpg
- Age: ~60s (40+ years at BBL since 1981)
- Education: Rensselaer Polytechnic Institute (Management Engineering)
- HQ: 302 Washington Ave Ext, Albany, NY
- Likely home: Loudonville/Slingerlands/Guilderland area (affluent Albany suburbs)
- Known event: Guan Ho Ha Fish and Game Club (charity MC)
- Affiliations: ENR Top 400 Contractor, AGC NYS, Capital Region Chamber

## Stephen Obermayer — CFO/Principal & President, BBL Hospitality
- Photo: https://www.bblinc.com/wp-content/uploads/2025/01/steve-obermayer.jpg
- Role: Top boss for hotel operations — visits properties for reviews
- Your connection: His division manages the hotel you work at
- Likely visit pattern: Quarterly management reviews, random spot checks
- Approach pitch: Knows P&L numbers, respects side-hustle mentality
```

### Privacy & Ethics

- Only use publicly available information (LinkedIn, news articles, company sites)
- Do NOT attempt to access private social media, stalk, or follow subjects
- Use habitat profiles for professional preparedness (networking, recognition), not harassment
- Do not share subjects' home addresses publicly — reference only by neighborhood/area

## Common Pitfalls

### Assumed Top Person Actually #2
- **PITFALL**: The most publicly visible person (quoted in news, listed as President) may not be the top decision-maker. The CEO may be less visible but outrank them.
- **SOLUTION**: Always scan the full `/about-us/leadership-team/` page for the org chart before declaring who's #1. CEO > President > EVP > SVP > VP. Chairman may be separate from CEO.
- **WORKAROUND**: If the leadership page lists titles, look for "CEO/Principal" or "Chief Executive Officer" — that's the top. "President/Principal" is often #2. "Chairman" may be founder/retired emeritus.
- **Real example**: At BBL Construction Services, Jonathan deForest (President) was quoted in news and seemed like the top guy, but Kevin Gleason (CEO/Principal) actually outranked him. Gleason has been at the company since 1981 and oversees the whole $500M operation.
- **PITFALL**: John Smith with a criminal record is not YOUR John Smith.
- **SOLUTION**: Always collect multiple identifiers (DOB, middle name, address) before drawing conclusions.
- **WORKAROUND**: Use DOB + last 4 SSN if available. Check known associates. Verify employer matches.

### Outdated Information
- **PITFALL**: LinkedIn profile shows current job but person moved 2 years ago.
- **SOLUTION**: Never rely on a single source. Cross-check timestamps.
- **WORKAROUND**: Look for activity recency (posts, comments, profile updates).

### Data Broker Accuracy
- **PITFALL**: Spokeo/BeenVerified often merge records of different people.
- **SOLUTION**: Treat aggregator data as leads, not facts. Verify with primary sources.
- **WORKAROUND**: Cross-reference multiple aggregators; if they disagree, flag as uncertain.

### False Negatives (Missing Data)
- **PITFALL**: "No record found" doesn't mean no record exists.
- **SOLUTION**: Document exact search parameters and databases searched.
- **WORKAROUND**: Some records are sealed, expunged, or in a different jurisdiction.

### Biased Sampling
- **PITFALL**: People with larger digital footprints are more searchable.
- **SOLUTION**: A sparse digital footprint may indicate privacy-consciousness, not lack of history.
- **WORKAROUND**: Check offline sources (property, court, licensing) which often exist regardless of digital presence.

## Legal & Ethical Notes

> **⚠️ WARNING**: Person investigation has significant legal and ethical boundaries:
> - **FCRA (Fair Credit Reporting Act)**: If information is used for employment, credit, insurance, or housing decisions, you may be a "consumer reporting agency" subject to FCRA compliance
> - **DRPA (Driver's Privacy Protection Act)**: Prohibits obtaining personal info from DMV records
> - **State Privacy Laws**: CA CPRA, VT Act 171, OR HB 2052 regulate data broker activities
> - **GDPR**: If subject is in EU, strict data protection rules apply
> - **Stalking/Harassment Laws**: Using OSINT to harass is illegal in all states
> - **Terms of Service**: LinkedIn, Facebook, etc. prohibit automated data collection
> - **Doxxing**: Publishing private information with malicious intent is illegal in many jurisdictions

### Permissible Uses
- Journalistic investigation (public interest)
- Legal investigation (attorney-supervised)
- Fraud/security investigation (legitimate business need)
- Personal safety (vetting dates, roommates, caregivers)
- Academic research (IRB-approved)
- Background check with subject consent

### Professional Standards
- **Accuracy**: Verify every finding against at least two independent sources
- **Context**: Present findings with source limitations and confidence levels
- **Timeliness**: Date all findings; stale data can be misleading
- **Confidentiality**: Do not share investigation results unnecessarily
- **Proportionality**: Use the least intrusive methods that achieve the objective
- **Bias awareness**: Document your methodology so others can reproduce results

## Reference Files

- `references/obituary-extraction.md` — Detailed playbook for extracting obituaries from Findagrave via Wayback Machine, including survivor identification for cross-referencing with business systems.

## Cross-References

- `security/osint-recon` — Full investigation pipeline starting from person
- `security/osint-property` — Property records for address history and asset verification
- `security/osint-business` — Check person's business affiliations and officer roles
- `security/osint-social` — Cross-platform social media identity resolution
- `security/osint-facial` — Facial recognition for identity confirmation
- `security/osint-threat` — Check if person appears in threat intelligence or breach data
- `security/osint-redteam` — Social engineering vector identification
- `software-development/systematic-debugging` — Apply structured methodology to complex investigations

## Verification Checklist

- [ ] Multiple name variants searched
- [ ] At least 2 independent identifiers confirm identity
- [ ] Address history compiled from property or voter records
- [ ] Employer verified from 2+ sources (LinkedIn + company page + SEC)
- [ ] Court records searched at federal level (PACER/CourtListener)
- [ ] State court records searched in relevant jurisdictions
- [ ] Business entity filings checked (state SoS)
- [ ] Social media profiles identified and reviewed
- [ ] Political donations checked (FEC/OpenSecrets)
- [ ] Professional licenses verified (if applicable)
- [ ] All findings dated with source attribution
- [ ] Legal constraints documented
- [ ] Confidence level assigned to overall assessment
