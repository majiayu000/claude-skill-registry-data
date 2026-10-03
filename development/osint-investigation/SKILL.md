---
name: osint-investigation
description: "Public-records OSINT: SEC, sanctions, courts, property."
allowed-tools:
  - bash
  - web_search
  - browse_page
  - write_file
enabled: true
related-skills: [deep-research, arxiv]
license: MIT
author: Adapted from hermes-agent (Nous Research, MIT); ShinMegamiBoson/OpenPlanter
---

# OSINT Investigation — Public Records Cross-Reference

Investigative framework for public-records OSINT: government contracts,
corporate filings, lobbying, sanctions, offshore leaks, property records,
court records, web archives, knowledge bases, and global news. Resolve
entities across heterogeneous sources, build cross-links with explicit
confidence, and produce structured evidence chains.

**Python stdlib only.** Zero install. Most sources work with no API key.

## When to Use

Use when the user asks for:
- "follow the money" — government contracts, lobbying → legislation, sanctions
- Corporate due diligence — who controls company X, where incorporated, board
  members, filings
- Sanctions screening — is entity X on OFAC SDN, ICIJ offshore leaks
- Property ownership — find recorded deeds/mortgages by name or address
- Litigation history — find federal + state court opinions
- Multi-source entity resolution where naming varies (LLC suffixes, abbreviations)
- Evidence-chain construction with explicit confidence levels
- "what's been said about X" — international news + Wikipedia + Wayback Machine

## Core Sources

### Corporate & Financial

| Source | What | Access |
|--------|------|--------|
| **SEC EDGAR** | US public company filings (10-K, 10-Q, 8-K, 13F) | `curl` to `https://efts.sec.gov/LATEST/search-index?q=...` |
| **USAspending.gov** | Federal contracts and grants | `curl` to `https://api.usaspending.gov/api/v2/...` |
| **Senate Lobbying** | Lobbying Disclosure Act filings | `curl` to `https://lda.senate.gov/api/v1/...` |
| **OFAC SDN** | Sanctions list | `curl` to `https://www.treasury.gov/ofac/...` |
| **ICIJ Offshore Leaks** | Panama Papers, Paradise Papers, etc. | `browse_page` to `https://offshoreleaks.icij.org/...` |
| **OpenCorporates** | Corporate registry (optional free token) | `curl` to `https://api.opencorporates.com/...` |

### Property & Courts

| Source | What | Access |
|--------|------|--------|
| **NYC ACRIS** | NYC property records (deeds, mortgages) | `browse_page` to `https://a836-acris.nyc.gov/...` |
| **CourtListener** | Federal + state court opinions | `curl` to `https://www.courtlistener.com/api/...` |

### Archives & Knowledge

| Source | What | Access |
|--------|------|--------|
| **Wayback Machine** | Archived web pages | `browse_page` to `https://web.archive.org/web/...` |
| **Wikipedia/Wikidata** | Encyclopedia + structured data | `bash` with `curl` to Wikipedia API |
| **GDELT** | Global news monitoring | `bash` with `curl` to `https://api.gdeltproject.org/...` |

## Methodology

### 1. Entity Resolution

Before cross-referencing, resolve the entity across sources:
- Normalize names (LLC suffixes, abbreviations, DBA aliases)
- Identify unique identifiers (EIN, LEI, CIK, OpenCorporates ID)
- Build a canonical entity record with all known aliases

### 2. Source-by-Source Query

For each relevant source, query by entity name or identifier:

```bash
# SEC EDGAR — search for company filings
curl -s "https://efts.sec.gov/LATEST/search-index?q=%22Company+Name%22" | python3 -c "..."

# USAspending — federal contracts to entity
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_by_award/" -d '{"filters":{...}}'

# OFAC SDN — check sanctions list
curl -s "https://www.treasury.gov/ofac/downloads/sdn.csv" | grep -i "entity name"
```

### 3. Cross-Link Analysis

Build explicit cross-links between sources:
- Same entity appearing in multiple sources
- Timing correlation (contract award → lobbying registration → legislation)
- Shared addresses, phone numbers, officers across entities

### 4. Confidence Scoring

For each finding, assign confidence:
- **High**: Official government record, multiple corroborating sources
- **Medium**: Single official source, or multiple unofficial sources
- **Low**: Single unofficial source, unverified

### 5. Evidence Chain

Construct an evidence chain showing how findings connect:
```
[Source A: fact 1] → [Source B: fact 2] → [Inference: conclusion]
  confidence: High      confidence: Medium     confidence: Medium
```

## Output

Produce a structured investigation report:

```markdown
# OSINT Investigation: [Entity / Topic]

## Executive Summary
[2-3 paragraph overview of findings]

## Entity Profile
- **Canonical Name**: ...
- **Aliases**: ...
- **Identifiers**: EIN, LEI, CIK, etc.
- **Known Addresses**: ...

## Findings by Source

### SEC EDGAR
[Findings with dates, filing types, key data]

### USAspending
[Contract awards, amounts, dates, agencies]

### OFAC SDN
[Sanctions status: CLEAR / MATCH (with details)]

### [Other sources...]

## Cross-Link Analysis
[Explicit connections between findings across sources]

## Evidence Chain
[Step-by-step reasoning from raw data to conclusions]

## Confidence Assessment
[Summary of confidence levels for key conclusions]

## Sources
[All URLs queried, with access dates]
```

Save to `.poirot/outputs/osint-{entity}-{YYYYMMDD}.md`.

## Pitfalls

- **Name variants**: "Acme LLC", "Acme L.L.C.", "Acme" may be different
  entities. Normalize but don't assume.
- **Stale data**: Public records may lag. Note the record's date.
- **False positives**: Sanctions list partial name matches need full record
  review. Don't report a match without verifying the full entry.
- **Rate limits**: Government APIs may rate-limit. Add delays between requests.
- **Legal caution**: OSINT findings are leads, not proof. Frame as "evidence
  suggests" not "proven".
