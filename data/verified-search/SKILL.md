---
name: verified-search
description: Expert verified search with source validation, credibility scoring, and fact-checking
version: 1.0.0
author: USER
tags: [search, verification, fact-checking, credibility, validation]
---

# Verified Search

## Purpose
Perform web searches with built-in verification, credibility scoring, and fact-checking to ensure accurate, trustworthy information.

## Activation Keywords
- verified search, trusted search
- fact check, credibility check
- validate information, verify source
- trusted sources, reliable info
- cross-check, confirm

## Core Capabilities

### 1. Search Execution
- Multi-engine queries
- Query optimization
- Result aggregation
- Deduplication
- Ranking adjustment

### 2. Source Validation
- Domain authority check
- Author verification
- Publication date
- Citation analysis
- Bias indicators

### 3. Credibility Scoring
- Source reputation
- Content accuracy
- Cross-reference matches
- Freshness score
- Expert consensus

### 4. Fact Verification
- Claim extraction
- Evidence gathering
- Counter-evidence search
- Verdict determination
- Confidence rating

### 5. Result Presentation
- Credibility-ranked results
- Source summaries
- Verification status
- Alternative viewpoints

## Verification Process

```
1. Execute Search
   → Multiple search engines
   → Query variations
   → Collect top N results

2. Filter & Rank
   → Domain authority score
   → Content relevance
   → Source freshness
   → Remove duplicates

3. Verify Each Source
   → Check author credentials
   → Verify publication date
   → Assess domain reputation
   → Look for citations

4. Cross-Reference
   → Compare across sources
   → Identify consensus
   → Flag contradictions
   → Note unique claims

5. Score & Present
   → Credibility score (1-10)
   → Verification status
   → Key findings
   → Caveats
```

## Credibility Scoring Criteria

| Factor | Weight | Description |
|--------|--------|-------------|
| Domain Authority | 25% | Site reputation, history |
| Author Expertise | 20% | Credentials, track record |
| Source Citations | 20% | References, peer review |
| Cross-Reference | 20% | Corroboration by others |
| Recency | 15% | Publication date relevance |

## Verification Status Labels

```
✅ VERIFIED - Multiple credible sources confirm
⚠️ PARTIALLY VERIFIED - Some sources confirm, gaps exist
❓ UNVERIFIED - Single source, needs more evidence
❌ DISPUTED - Conflicting credible sources
🔄 OUTDATED - Information may no longer be current
```

## Search Result Format

```markdown
## Search Results: [Query]

### Result 1: [Title]
- **Source**: [Domain] | **Credibility**: 8/10
- **Status**: ✅ VERIFIED
- **Summary**: [Key points]
- **Cross-referenced by**: [Other sources]

### Result 2: [Title]
- **Source**: [Domain] | **Credibility**: 6/10
- **Status**: ⚠️ PARTIALLY VERIFIED
- **Summary**: [Key points]
- **Note**: [Verification gaps]

### Consensus View
[What most credible sources agree on]

### Disputed Points
[Where sources disagree]

### Verification Notes
- Total sources checked: N
- Credible sources: M
- Average credibility: X/10
```

## Example Usage

```
User: "Search for React 19 release date"

Verified Search Response:
Query: "React 19 release date official"

Results (5 sources checked):

1. React.dev Blog (Official)
   - Credibility: 10/10 ✅ VERIFIED
   - Status: Primary source
   - Finding: React 19 released December 2024

2. GitHub React Releases
   - Credibility: 10/10 ✅ VERIFIED
   - Confirms: v19.0.0 tag exists

3. Dev.to Article
   - Credibility: 6/10 ⚠️ PARTIALLY VERIFIED
   - Accurate date, secondary source

Consensus: React 19 officially released December 2024
Confidence: HIGH (confirmed by primary sources)
```
