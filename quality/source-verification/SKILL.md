---
name: source-verification
description: >
  Use when incorporating information from research, references, or external sources.
  This skill provides verification procedures to ensure information used in deliverables
  is accurate, current, and from authoritative sources, preventing hallucination and
  misinformation.
---

# Source Verification

## Overview
This skill defines how to verify information before using it in any deliverable. Agent hallucination and outdated information can cause serious downstream problems. Use this skill whenever incorporating facts, citations, specifications, or claims from any source other than direct knowledge.

## When to Use
- When citing statistics, figures, or factual claims
- When referencing standards, regulations, or compliance requirements
- When quoting or paraphrasing from external sources
- When making technical claims about systems, tools, or capabilities
- When recommending approaches based on market or competitive intelligence
- **Don't use when:** Expressing opinion, creative content, or common knowledge within your domain expertise

## Core Procedures

### Step 1: Identify Claims Requiring Verification
Flag any statement that:
- Includes specific numbers, dates, or measurements
- References external standards, laws, or regulations
- Makes factual claims (not analysis or opinion)
- Cites another person, organization, or source
- Uses words like "according to," "research shows," "studies prove"

### Step 2: Assess Source Credibility
Rate source on these dimensions:

| Dimension | High Credibility | Low Credibility |
|-----------|-----------------|-----------------|
| Authority | Subject matter expert, official source | Anonymous, unattributed |
| Currency | Published within last year | Published 3+ years ago |
| Methodology | Peer-reviewed, tested, validated | Opinion, anecdote, unverified |
| Bias | Independent, multiple viewpoints | Single interest, advocacy |
| Corroboration | Confirmed by multiple independent sources | Only source makes this claim |

### Step 3: Verification Actions
Based on claim type, perform appropriate verification:

**STATISTICAL/EVIDENCE CLAIMS:**
- [ ] Find original source of the data (not secondary citation)
- [ ] Check sample size, methodology, and margins of error
- [ ] Compare with at least one other source for corroboration
- [ ] Note any limitations or caveats from original source

**REGULATORY/COMPLIANCE CLAIMS:**
- [ ] Verify against official regulatory body publication
- [ ] Check effective date and any pending changes
- [ ] Confirm applicability to current context (jurisdiction, industry)
- [ ] Note any pending challenges or interpretations

**TECHNICAL/PRODUCT CLAIMS:**
- [ ] Check official documentation or release notes
- [ ] Verify version number and applicability
- [ ] If possible, test or confirm with direct observation
- [ ] Note any known issues or limitations

**MARKET/COMPETITIVE CLAIMS:**
- [ ] Cross-reference with multiple market research sources
- [ ] Check date of information (markets change rapidly)
- [ ] Note source's potential bias (vendor reports favor vendors)
- [ ] Distinguish between fact and analyst opinion

### Step 4: Document Verification
For each verified claim, record:
```
Claim: [what was stated]
Source: [where it came from, with URL/citation]
Verification: [what was done to confirm it]
Confidence: [HIGH / MEDIUM / LOW with reasoning]
Status: [VERIFIED / UNVERIFIED / DISPUTED]
```

### Step 5: Act on Verification Results
- **VERIFIED (HIGH confidence):** Use freely in deliverables
- **VERIFIED (MEDIUM confidence):** Use with appropriate caveats
- **UNVERIFIED:** Either find alternative source or explicitly label as unconfirmed
- **DISPUTED:** Present competing evidence, recommend further research

## Quality Checklist
- [ ] All factual claims identified and verified
- [ ] Sources are authoritative, current, and credible
- [ ] Independent corroboration obtained where possible
- [ ] Unverifiable claims clearly labeled as such
- [ ] Confidence level documented for each claim
- [ ] Disputed claims include both sides of evidence

## Error Handling
- **Error:** Source is unavailable or behind paywall
  **Response:** Find alternative credible source, note original is unavailable
- **Error:** Sources contradict each other
  **Response:** Present contradiction, escalate to research specialist (Scholar, Explorer, Alex) for resolution
- **Error:** Original source is primary data requiring expertise to evaluate
  **Response:** Flag expertise gap, escalate to domain specialist agent
- **Error:** Time pressure doesn't allow full verification
  **Response:** Deliver with explicit confidence levels, schedule follow-up verification

## Cross-Team Integration
**Related Skills:** knowledge-retrieval, competitive-analysis, research-methodology, conflict-resolution
**Used By:** Researchers (Scholar, Explorer, Alex, Analyst, Oracle), ALL agents when citing external information