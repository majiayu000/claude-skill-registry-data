---
name: deep-prospecting
description: Deep prospect real estate leads to identify decision-makers when skip tracing fails. Use when user provides a property address, filing, probate docket, foreclosure notice, or any distress record and needs to find the correct owner/heir/executor. Executes the complete L1-L3 research flow and then skip traces the decision-maker directly at TruePeopleSearch, FastPeopleSearch, and CyberBackgroundChecks to deliver phone numbers, emails, and associates in the final output.
---

# Deep Prospecting

Deep prospecting is the manual research process for identifying and verifying decision-makers (owner/heir/executor) when standard skip tracing fails. Core philosophy: **"When everyone hits a wall, we bring a shovel."**

## When to Use This Skill

- Skip trace returned no usable phone numbers
- Called 3+ attempts with no contact
- Vacant mailing address discovered
- Return mail (bad address)
- Probate cases (often only docket number available)
- Entity/LLC ownership (need actual decision-maker)
- Conflicting owner/address information in public records

## Input Requirements

User provides any combination of:
- Property address
- Owner name (full or partial)
- Filing/docket number
- Probate case information
- Foreclosure notice details
- Any distress record data

## Workflow Overview

```
1. Auto-select research level (L1/L2/L3) based on input
2. Execute mandatory source checks for selected level
3. Build ownership/title analysis
4. Resolve identity variants (if applicable)
5. Map family tree (if deceased owner)
6. VERIFY heir alive/dead status (recursive until living heirs found)
7. Identify decision-maker(s) from VERIFIED LIVING heirs only
8. Skip trace decision-maker at TruePeopleSearch, FastPeopleSearch, and CyberBackgroundChecks
9. Compile skip trace results (phone numbers, emails, associates)
10. Deliver formatted research pack with contact info included
```

## Level Selection Logic

**L1 Initial Block** → Skip trace yielded no usable mobiles; verify with light public records
- Trigger: No phone numbers returned, but owner appears alive and reachable
- Focus: Cross-verification and simple public record lookups

**L2 Address/Name Variation** → Conflicting/incomplete owner/address/name; resolve via title/deed chain + history
- Trigger: Public records show conflicting information, multiple name variants, or incomplete data
- Focus: Title work (deeds), Google dorking, property history

**L3 Deceased Owner/Heirs** → Owner likely deceased; identify living decision-maker via obits/genealogy
- Trigger: Owner appears deceased, heir/executor contact unknown
- Focus: Obituaries, Ancestry, newspapers, family tree mapping, **heir verification loop**

## Source Checklist by Level

### L1 Baseline Sources
- [ ] County Assessor/CAD (ownership & mailing)
- [ ] Recorder/Deed image (names, middle initials, instrument type)
- [ ] Google dorking on owner/address (site:, intitle:, filetype:)
- [ ] Tax payment history (or FOIA path if not public)
- [ ] Clerk civil/criminal/dockets (owner + co-owners)
- [ ] Skip trace completed at TruePeopleSearch, FastPeopleSearch, and CyberBackgroundChecks

### L2 Sources (add to L1)
- [ ] Deed chain (last 3-5 instruments) + instrument type
- [ ] Name-variant sweep (aliases, maiden/married, initials)
- [ ] Cross-county property/recorder/docket searches from address history

### L3 Sources (add to L1 as needed)
- [ ] Obituaries: Legacy.com, Newspapers.com, FindAGrave, Ancestry
- [ ] Minimal family tree (spouse/children/siblings + current cities)
- [ ] **Heir Verification Loop** (verify alive/dead status for each heir)
- [ ] Decision-maker identification (executor/surviving spouse/oldest child) - **from verified living heirs only**
- [ ] Skip trace completed for decision-maker at TruePeopleSearch, FastPeopleSearch, and CyberBackgroundChecks

## Research Execution

### Phase 1: Initial Verification and Title Review

| Step | Action | Purpose |
|------|--------|---------|
| 1.0 | Verify Current Ownership | Confirm seller still owns property; check for recent sales |
| 1.1 | Review the Deed (Critical) | Analyze for middle initials, relationships, transaction type (arms-length, quitclaim, inherited) |
| 1.2 | Identify Title Issues | Look for installment agreements, multiple owners/heirs |
| 1.3 | Initial Google Search | Use owner name + property address with dorking operators |

### Phase 2: Genealogy & Historical Research (L3)

| Step | Action | Purpose |
|------|--------|---------|
| 2.0 | Search for Obituaries | Find survivors, spouses, relationships |
| 2.1 | Newspapers.com Deep Dive | Historical mentions, city directories, marriage announcements |
| 2.2 | Map the Family Tree | Build tree from obituaries and deeds |
| 2.3 | "Go Back to Go Forward" | Use older records to find new leads |

### Phase 2.5: Heir Verification Loop (L3 - CRITICAL)

**Purpose:** Verify each identified heir is alive before adding as potential decision-maker. If deceased, find THEIR heirs and repeat until living heirs are confirmed.

#### Verification Process

```
FOR EACH heir identified in Phase 2:
    1. Search for heir's obituary/death record
    2. Check FindAGrave for burial record
    3. Search "[HEIR NAME] obituary [CITY/STATE]"
    4. Check Ancestry death records if available
    
    IF heir confirmed ALIVE:
        → Mark as ✓ (verified living) in heir map
        → Add to potential decision-maker list
        
    IF heir confirmed DECEASED:
        → Mark as † (deceased) in heir map
        → Record DOD if found
        → Search for THEIR obituary to find survivors
        → Add their heirs to verification queue
        → REPEAT verification process for new heirs
        
    IF status UNCERTAIN:
        → Mark as ? (unverified) in heir map
        → Note last known activity date
        → Include in decision-maker list with LOW confidence
```

#### Verification Sources (in order of reliability)

| Source | What to Look For | Reliability |
|--------|------------------|-------------|
| FindAGrave | Burial record, DOD, family links | HIGH |
| Legacy.com | Obituary with survivors listed | HIGH |
| Newspapers.com | Death notice, obituary | HIGH |
| Ancestry Death Records | SSN death index, state records | HIGH |
| Google "[Name] obituary [City]" | News articles, funeral home posts | MEDIUM |
| TruePeopleSearch/FastPeopleSearch | No record found or "Deceased" notation | MEDIUM |
| No recent activity (10+ years) | Indirect indicator only | LOW |

#### When to Stop the Loop

- All identified heirs verified as living OR
- Found at least 2-3 verified living heirs with decision-making authority OR
- Reached 3rd generation with no living heirs found (escalate to L4/attorney)

### Phase 3: Locating the Target (Verified Living Heir/Executor)

| Step | Action | Purpose |
|------|--------|---------|
| 3.0 | Identify the Target | Select from **verified living heirs only** |
| 3.1 | Search for the Target | Use full name, city, estimated age |
| 3.2 | Cross-Reference and Validate | Use second source to validate |
| 3.3 | Document Findings | Record all valid contact numbers |

**Decision-Maker Priority (from verified living heirs):**
1. Named executor (if probate filed)
2. Surviving spouse
3. Oldest living child
4. Sibling (if no spouse/children)
5. Grandchild (if children deceased)

## Manual Skip Trace Execution (3-Site Waterfall)

After identifying the decision-maker(s), run them through all three sites in order. Each site pulls from slightly different databases, so hitting all three maximizes your chance of getting a working number. Browse each site directly using the browser tools.

### Site 1: TruePeopleSearch.com (Primary)

The "King" of free skip tracing and the first stop for every manual trace. It often surfaces a high volume of wireless numbers and landlines, plus previous addresses that help confirm absentee owners who recently moved.

**How to search:**
1. Navigate to https://www.truepeoplesearch.com
2. Search by name: `{FULL NAME}` in `{CITY, STATE}`
3. If name search is too broad, use the address search: `{PROPERTY ADDRESS}` or `{TAX MAILING ADDRESS}`
4. **Scroll past the "Sponsored Results"** (they look like buttons) — the free data lives in the plain-text "Details" section below
5. Record: all phone numbers (mobile + landline), current/previous addresses, age, associated names

**What to capture:**
- Phone numbers (label as mobile/landline where shown)
- Current and previous addresses (confirm against property/tax records)
- Associated people / relatives (cross-reference with heir map if L3)
- Age (confirm against deed/obit timeline)

### Site 2: FastPeopleSearch.com (Backup / Cross-Reference)

The strongest alternative to TruePeopleSearch. Many investors report it pulls from a slightly different database, so it can unlock leads the first site misses. Clean layout makes it easy to copy/paste into a CRM.

**How to search:**
1. Navigate to https://www.fastpeoplesearch.com
2. Search by name: `{FULL NAME}` in `{CITY, STATE}`
3. If name returns too many results, try address search with `{KNOWN ADDRESS}`
4. Record any NEW phone numbers or addresses not already found on TruePeopleSearch
5. Pay attention to "Also Known As" names — useful for L2 name-variant cases

**What to capture:**
- Any phone numbers NOT already found on TruePeopleSearch
- Email addresses (sometimes shows these more reliably)
- "Also Known As" aliases (feed back into L2 name variant sweep)
- Current address (cross-reference for validation)

### Site 3: CyberBackgroundChecks.com (Deep Data / Associates)

A newer favorite in REI communities for its depth on email addresses and associates. The "Possible Associates" and "Relatives" lists are especially valuable for probate leads and elusive landlords — calling a relative is often the best route.

**How to search:**
1. Navigate to https://www.cyberbackgroundchecks.com
2. Search by name: `{FULL NAME}` in `{CITY, STATE}`
3. Focus on the "Possible Associates" and "Relatives" sections
4. Record any NEW contacts, email addresses, and associate names not found on the first two sites

**What to capture:**
- Email addresses (this site is often the best source for these)
- "Possible Associates" list (business partners, neighbors, co-signers)
- "Relatives" list (cross-reference with heir map; may reveal heirs you missed)
- Any additional phone numbers

### Skip Trace Validation

After running all three sites, cross-reference the results to build confidence:

**High-Confidence Match (ready to dial):**
- Same phone number appears on 2+ sites
- Associated addresses include subject property or tax mailing address
- Relatives/associates match names from deeds, obits, or heir map
- Age band fits deed history and obit dates

**Medium-Confidence Match (dial but verify):**
- Phone number appears on only 1 site
- Address matches but no relative/associate confirmation
- Name variant matches but slightly different city

**Low-Confidence Match (verify before investing time):**
- Only partial name match
- No address overlap with known records
- No relative/associate cross-reference

## Heir Map Template (L3)

When deceased owner identified, create visual heir map with **verification status**:

```
Decedent: † {DECEDENT FULL} (DOD {YYYY-MM-DD}) [{CITY, ST}]
│
├─ Spouse/Partner:
│  └─ {STATUS} {SPOUSE FULL} [{CITY, ST}] {DOD if deceased}
│
├─ Children:
│  ├─ {STATUS} {CHILD 1} [{CITY, ST}] {DOD if deceased}
│  │   └─ Grandchildren (if Child 1 deceased):
│  │       ├─ {STATUS} {GRANDCHILD 1A} [{CITY, ST}]
│  │       └─ {STATUS} {GRANDCHILD 1B} [{CITY, ST}]
│  │
│  ├─ {STATUS} {CHILD 2} [{CITY, ST}] {DOD if deceased}
│  │   └─ Grandchildren (if Child 2 deceased):
│  │       └─ {STATUS} {GRANDCHILD 2A} [{CITY, ST}]
│  │
│  └─ {STATUS} {CHILD 3} [{CITY, ST}]
│
└─ Siblings:
   ├─ {STATUS} {SIBLING 1} [{CITY, ST}]
   └─ {STATUS} {SIBLING 2} [{CITY, ST}]

STATUS MARKERS:
  †  = Verified DECEASED (with DOD if known)
  ✓  = Verified LIVING (confirmed no death record)
  ?  = UNVERIFIED (status unknown, needs confirmation)
  ★  = Executor (confirmed via probate filing)
  ▸  = Recommended decision-maker (verified living + authority)
  ●  = Current living owner (confirmed on title/deed)
```

### Heir Map Example (with verification)

```
Decedent: † John Robert Smith (DOD 2019-03-15) [Dallas, TX]
│
├─ Spouse:
│  └─ † Mary Jane Smith (DOD 2022-08-20) [Dallas, TX]
│
├─ Children:
│  ├─ † Robert John Smith Jr. (DOD 2021-01-10) [Fort Worth, TX]
│  │   └─ Grandchildren:
│  │       ├─ ✓ ▸ Michael Robert Smith [Austin, TX] ← DECISION-MAKER
│  │       └─ ✓ Jennifer Smith-Lopez [Houston, TX]
│  │
│  ├─ ✓ Susan Smith-Williams [Plano, TX]
│  │
│  └─ ? David Allen Smith [Last known: Arlington, TX, 2015]
│
└─ Siblings:
   └─ † William Smith (DOD 2018-05-22) [Oklahoma City, OK]

VERIFICATION SUMMARY:
- Verified Living: Michael R. Smith, Jennifer Smith-Lopez, Susan Smith-Williams
- Verified Deceased: Mary Jane Smith, Robert John Smith Jr., William Smith
- Unverified: David Allen Smith (no recent records, possible deceased)
- Recommended Decision-Maker: Michael Robert Smith (oldest grandchild, verified living)
```

## Deliverable Format

Output a research pack with these sections (headings + bullets only, no JSON):

```
## 1) Level Selected & Why
[State L1/L2/L3 and the specific reason]

## 2) Source Checklist
[Mark [x]/[ ] with 1-line notes for each source checked]

## 3) Title & Ownership
- Current owner(s)
- Instrument type summary
- Red flags (QCD, installment/contract, etc.)

## 4) Identity Resolution (if variants exist)
- Which variant won & why (1-2 lines)

## 5) Genealogy/Heir Findings (if family/estate elements)
- Obit links found
- Survivors identified
- Relationship notes

## 6) Heir Verification Summary (L3 required)
- Total heirs identified: [#]
- Verified living: [# and names]
- Verified deceased: [# and names with DODs]
- Unverified: [# and names with notes]
- Generations searched: [1st/2nd/3rd]

## 7) Heir Map (L3 required; L1/L2 if relationships relevant)
[ASCII tree per template above WITH verification status markers]

## 8) Decision-Maker Identified
- Name: {FULL NAME}
- Relationship: {owner/heir/executor/spouse}
- Verification Status: {✓ Verified Living / ? Unverified}
- Current Address: {best known mailing address}
- Estimated Age: {age range based on records}
- Confidence: {HIGH/MEDIUM/LOW with reasoning}

## 9) Skip Trace Results
[Include the formatted results card - see template below]
```

## Skip Trace Results Output

At the end of research, after browsing all three skip trace sites, compile findings into a **Skip Trace Results Card**:

```
═══════════════════════════════════════════════════════════
                  SKIP TRACE RESULTS
═══════════════════════════════════════════════════════════

DECISION-MAKER: {FULL NAME}
  Relationship: {owner/heir/executor/spouse}
  Status:       {✓ Verified Living}
  Est. Age:     {AGE RANGE}

─── PHONE NUMBERS ────────────────────────────────────────
  #  | Number          | Type     | Source(s)       | Confidence
  1  | (xxx) xxx-xxxx  | Mobile   | TPS, FPS        | HIGH
  2  | (xxx) xxx-xxxx  | Landline | TPS             | MEDIUM
  3  | (xxx) xxx-xxxx  | Mobile   | CBC             | MEDIUM

─── EMAIL ADDRESSES ──────────────────────────────────────
  1  | xxxx@xxxxx.com  | CBC, FPS
  2  | xxxx@xxxxx.com  | CBC

─── ADDRESSES ────────────────────────────────────────────
  Current:  {ADDRESS} (confirmed on TPS + FPS)
  Previous: {ADDRESS} (matches tax mailing)

─── ASSOCIATES & RELATIVES ──────────────────────────────
  • {NAME} - {RELATIONSHIP} - {CITY, ST} (from CBC)
  • {NAME} - {RELATIONSHIP} - {CITY, ST} (from CBC)

─── VALIDATION ───────────────────────────────────────────
  ☑ Phone on 2+ sites    ☑ Address matches records
  ☑ Relatives match       ☑ Age fits timeline

BACKUP DECISION-MAKERS (also traced):
  • {NAME 2} · {CITY, STATE} · {RELATIONSHIP} · {PHONE}
  • {NAME 3} · {CITY, STATE} · {RELATIONSHIP} · {PHONE}

SOURCE KEY: TPS = TruePeopleSearch | FPS = FastPeopleSearch | CBC = CyberBackgroundChecks
═══════════════════════════════════════════════════════════
```

The user can dial directly from these results — no additional lookup step needed.

## Key Tools Reference

| Tool | Primary Use | Notes |
|------|-------------|-------|
| County Deed Records | Title analysis, ownership verification | Look for middle initials, transaction types |
| Google Dorking | Narrowing search results | Use site:, intitle:, filetype: operators |
| Ancestry.com | Family trees, obituaries, death records | Essential for L3 cases |
| Newspapers.com | Historical mentions, directories, obituaries | Useful for pre-2000 records |
| FindAGrave | **Heir verification**, burial records, family links | Primary source for death confirmation |
| Legacy.com | Obituaries with survivor lists | Key for heir identification AND verification |
| TruePeopleSearch.com | Phone numbers, addresses, associates | Primary skip trace site; scroll past sponsored results |
| FastPeopleSearch.com | Phone numbers, emails, aliases | Backup skip trace; pulls from different database |
| CyberBackgroundChecks.com | Emails, associates, relatives | Best for deep associate/relative data; great for probate |
| Social Media/LinkedIn | Professional/personal contact info | Last resort for living heirs |

## Error Handling

If information cannot be found:
- Mark as [MISSING] in deliverable
- State the next action to resolve
- Suggest alternative search strategies
- Note if title attorney consultation recommended (L4 scenario)

**Heir Verification Failures:**
- If heir status cannot be verified after checking all sources, mark as "?" (unverified)
- Include unverified heirs in decision-maker list with LOW confidence
- Note: "Status unverified - recommend confirming before extensive skip trace investment"
- If ALL heirs are deceased or unverified through 3 generations, escalate to L4 (title attorney)
