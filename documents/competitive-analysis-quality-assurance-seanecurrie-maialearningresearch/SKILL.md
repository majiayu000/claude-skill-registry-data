---
name: competitive-analysis-quality-assurance
description: Systematic fact-checking, source verification, and quality assurance for competitive research deliverables. This skill ONLY activates when explicitly requested - it does not auto-trigger. Use this skill when you explicitly ask to review competitive research, fact-check claims, verify sources, validate consistency, or assess quality of completed analysis documents. Example requests that activate this skill "review this competitive analysis", "fact-check these findings", "verify the sources", "quality check this report", "are these claims accurate", or "validate this analysis".
---

# Competitive Analysis Quality Assurance

This skill provides systematic fact-checking, source verification, and quality assurance methodologies for competitive research deliverables. It works as a companion to the competitive-research-brightdata skill, ensuring findings meet enterprise consulting standards before final delivery.

## When to Use This Skill

Use this skill AFTER initial research is complete, during the review and quality assurance phase. Specifically:

- **Fact-Checking:** Verify specific claims, statistics, or facts from research
- **Source Validation:** Check citations are accurate, accessible, and relevant
- **Consistency Review:** Ensure information is consistent across multiple documents
- **Gap Identification:** Find missing information or areas needing deeper research
- **Quality Assessment:** Evaluate against consulting-grade standards
- **Pre-Delivery Review:** Final QA before presenting to stakeholders

## Typical Project Structure

When working with competitive research projects, documents are typically organized as:

**Standard Template Structure (New Projects):**
```
[PROJECT]/
├── 00-PROJECT-OVERVIEW/          # Research objectives, scope
├── 01-RESEARCH-INPUTS/           # All research data
│   ├── company-profiles/         # Client company profile
│   ├── competitor-profiles/      # Individual competitor deep-dives
│   └── raw-data/                 # Search results, scraped content
├── 02-ANALYSIS-OUTPUTS/          # Analysis working files
│   ├── comparative-analysis/     # Feature matrices, pricing, positioning
│   └── strategic-insights/       # SWOT, competitive maps, recommendations
├── 03-DELIVERABLES/              # Client-ready deliverables
│   └── current/                  # Canonical versions (DOCX/HTML/PDF)
├── 04-QA-DOCUMENTATION/          # QA reports, change logs
├── 05-ITERATIONS/                # Iteration documentation
└── 06-PROJECT-MANAGEMENT/        # Task trackers, methodology notes
```

**Legacy Structure (Pre-November 2025):**
```
ProjectName/
├── 00-PROJECT-OVERVIEW/          # Research objectives, progress tracker
├── 01-COMPANY-PROFILES/          # Client/baseline company profile
├── 02-COMPETITOR-PROFILES/       # Individual competitor deep-dives
├── 03-COMPARATIVE-ANALYSIS/      # Feature matrices, pricing, positioning
├── 04-STRATEGIC-INSIGHTS/        # SWOT, competitive maps, recommendations
├── 05-FINAL-DELIVERABLES/        # Executive summaries, reports
└── 06-PROJECT-MANAGEMENT/        # Task trackers, methodology notes
```

**Path Discovery Protocol:**

Before asking user for file paths:
1. Check current directory structure using `ls` or glob patterns
2. Look for common project directory patterns (both structures above)
3. Identify which structure variant is in use
4. Note available documents for review
5. Only ask clarifying questions after understanding what exists

**When asked to review documents, check these directories first** before asking user for specific file paths. This makes QA more efficient by knowing where to look.

## Available Tools

### Research & Verification Tools

**web_search** - Search the web to verify claims and find corroborating sources
- Use to validate facts, statistics, company information
- Cross-reference with original research sources
- Find additional sources for under-supported claims

**search_engine (Bright Data)** - Professional-grade search across Google/Bing/Yandex
- Use for deeper verification when web_search insufficient
- Access same tools used in original research
- Validate hard-to-find or specialized information

**web_fetch** - Retrieve full webpage content to verify citations
- Use to check if cited sources actually contain claimed information
- Validate quote accuracy and context
- Verify publication dates and authorship

**scrape_as_markdown (Bright Data)** - Extract clean content from websites
- Use for detailed source verification
- Check if company websites still contain cited information
- Validate pricing, features, or specifications

### Document Analysis Tools

**Filesystem tools** - Read and analyze research documents
- Use to review company profiles, competitive analyses, reports
- Cross-reference claims across multiple documents
- Check for internal consistency

## Workflow

### Phase 1: Scope the Review

**Locate Project Files First:**

Before asking clarifying questions, check if you can identify the project structure:
1. Look for common research project directory patterns (see "Typical Project Structure" above)
2. Check filesystem for folders like `01-COMPANY-PROFILES/`, `02-COMPETITOR-PROFILES/`, `03-COMPARATIVE-ANALYSIS/`
3. If found, note the structure and available documents
4. This allows more specific clarifying questions

**Clarify Review Objectives:**

Ask questions to understand what needs review:
- Which documents need fact-checking? (Specific profiles, analyses, or full project)
- What level of review? (Quick validation, comprehensive audit, or targeted fact-check)
- Are there specific claims flagged for verification?
- What's the timeline for review completion?
- Are there known concerns or areas of uncertainty?
- What quality standard should be met? (Internal review, client-ready, publication-grade)

**Identify Review Priority:**
- **High Priority:** Executive summaries, key findings, strategic recommendations
- **Medium Priority:** Detailed analyses, comparison matrices, company profiles  
- **Low Priority:** Background information, methodology notes, project management docs

**Determine Review Depth:**
- **Rapid Scan (30 min - 1 hour):** Check critical claims only, spot-check citations
- **Standard Review (2-4 hours):** Verify key claims, validate major sources, check consistency
- **Comprehensive Audit (1-2 days):** Verify all claims, validate all sources, full consistency check

### Phase 2: Document Analysis

**Step 1: Read and Map Documents**

Read all in-scope documents to understand:
- Document structure and organization
- Key claims and findings
- Supporting evidence and citations
- Relationships between documents
- Overall narrative flow

**Create Mental Map:**
- Major themes and findings
- Critical claims requiring verification
- Sources cited multiple times
- Areas with sparse supporting evidence
- Potential inconsistencies

**Step 2: Extract Claims for Verification**

For each document, identify:
- **Factual Claims:** Statistics, dates, company information, market share, pricing
- **Attributed Quotes:** Direct quotes from sources
- **Comparative Statements:** X is better/worse/more than Y
- **Strategic Conclusions:** Recommendations based on evidence
- **Source Citations:** URLs, publication dates, author names

See `references/verification-checklist.md` for comprehensive claim categories.

### Phase 3: Source Validation

**Step 1: Citation Verification**

For each citation, verify:
- **URL Accessibility:** Does the link work?
- **Content Accuracy:** Does the source actually say what's claimed?
- **Date Currency:** Is the publication date accurate and recent?
- **Author Credibility:** Is the source authoritative?
- **Context Accuracy:** Is the quote/claim in proper context?

**Verification Process:**
1. Use `web_fetch` to retrieve cited URL
2. Search for claimed information in fetched content
3. Verify quote accuracy (exact wording, not out of context)
4. Check publication date matches citation
5. Assess source quality and credibility

**Document Findings:**
- ✅ Verified: Source confirms claim
- ⚠️ Partially Verified: Source supports but with caveats
- ❌ Not Verified: Source doesn't support claim
- 🔗 Broken: URL inaccessible or content changed
- 📅 Outdated: Source too old or superseded by newer info

**Step 2: Cross-Reference Verification**

For major claims, seek multiple sources:
- **Single-Source Risk:** Claims with only one source need additional validation
- **Triangulation:** Find 2-3 independent sources confirming claim
- **Conflicting Sources:** Note when sources disagree
- **Source Hierarchy:** Prioritize primary over secondary sources

**Use web_search and Bright Data to:**
- Find corroborating sources for single-sourced claims
- Validate statistics from independent sources
- Check if newer information supersedes old sources
- Find authoritative primary sources (company sites, official reports)

### Phase 4: Fact-Checking

**Step 1: Factual Claim Verification**

For each factual claim, verify:

**Company Information:**
- Founded date, headquarters location, CEO name
- Ownership structure (public, private, PE-backed)
- Funding amounts, acquisition prices
- Employee count, office locations

**Market Data:**
- Market share percentages
- Customer counts (students, schools)
- Geographic presence (countries, states)
- Revenue, pricing (if publicly available)

**Product Features:**
- Feature availability (does product actually have X?)
- Integration partnerships
- Technology specifications
- Launch dates for new features

**Verification Method:**
1. Search for claim using web_search or Bright Data
2. Find 2-3 authoritative sources
3. Compare found information with document claim
4. Note any discrepancies
5. Flag claims requiring updates

See `references/fact-checking-methodology.md` for detailed verification techniques.

**Step 2: Statistical Verification**

For statistics and metrics:
- **Check Math:** Do percentages, calculations add up correctly?
- **Validate Source:** Where does statistic come from?
- **Assess Currency:** Is data recent enough to be relevant?
- **Context Check:** Is statistic used appropriately?

**Common Statistical Issues:**
- Outdated data presented as current
- Percentages that don't align with stated totals
- Selective use of favorable statistics
- Statistics from biased or unreliable sources

**Step 3: Comparative Claims**

For claims like "X is better/cheaper/more popular than Y":
- **Verify Both Sides:** Confirm data for X AND Y
- **Check Comparison Basis:** Are units/timeframes comparable?
- **Validate Currency:** Are comparisons using current data?
- **Assess Fairness:** Is comparison apples-to-apples?

### Phase 5: Consistency Analysis

**Step 1: Internal Consistency Check**

Verify information is consistent within and across documents:

**Within Document:**
- Does executive summary match detailed findings?
- Are statistics consistent throughout document?
- Do conclusions follow from evidence presented?
- Are section recommendations aligned?

**Across Documents:**
- Is company information same in profile and matrix?
- Are feature comparisons consistent with profiles?
- Does pricing analysis match profile pricing sections?
- Are strategic recommendations aligned across analyses?

**Common Inconsistencies:**
- Different dates for same event
- Different market share numbers  
- Conflicting feature availability claims
- Contradictory strategic recommendations

**Step 2: Timeline Verification**

Check date-related claims:
- Founding dates match across documents
- Acquisition dates consistent
- Product launch dates accurate
- News/developments in chronological order
- "Recent" and "latest" claims actually recent

**Step 3: Numerical Consistency**

Verify numbers across documents:
- Student counts consistent
- Market share percentages add up
- Pricing consistent across documents
- Growth rates mathematically valid

### Phase 5.5: Source Attribution Verification

**Objective:** Verify that all numeric claims and key facts have proper citations.

**Citation Format Requirements:**

All claims of the following types MUST have inline citations in the format `(Source, YYYY)`:

1. **Pricing Claims:** Any `$X` or `$X-Y` figure
   - Example: "Naviance pricing ranges from $8-12 per student (PowerSchool, 2024)"

2. **Market Share:** Any `X%` market or share claim
   - Example: "SCOIR holds approximately 12% market share (EdTech Analysis, 2024)"

3. **Customer Counts:** Any "X schools" or "X students" claim
   - Example: "serving over 2,400 schools (SCOIR, 2024)"

4. **Funding Amounts:** Any `$XM` or `$XB` funding claim
   - Example: "raised $42M in Series C (Crunchbase, 2023)"

5. **Satisfaction Ratings:** Any `X/5` or `X.X/10` rating
   - Example: "rated 4.6/5 on G2 (G2, November 2024)"

6. **Growth Rates:** Any `X% growth` claim
   - Example: "40% year-over-year growth (Company Report, 2024)"

**Verification Process:**

1. Scan document for numeric patterns (regex: `\$[\d,]+`, `\d+%`, `\d+/\d+`, etc.)
2. For each match, check if `(Source, YYYY)` appears within 100 characters
3. Flag uncited claims for review
4. Generate compliance report

**Citation Compliance Report Format:**

```
## Citation Compliance Check

**Document:** [filename]
**Date:** [review date]

### Summary
- Total numeric claims found: X
- Claims with proper citations: Y (Z%)
- Claims missing citations: N

### Uncited Claims Requiring Attention

| Line | Claim | Type | Recommendation |
|------|-------|------|----------------|
| 45 | "$4.80 per student" | Pricing | Add source citation |
| 112 | "12% market share" | Market Share | Add source citation |

### Properly Cited Examples
[List 2-3 good examples as reference]
```

**Integration with Workflow:**
- Run citation check BEFORE comprehensive fact-checking
- Use findings to prioritize which claims need source verification
- Include citation compliance score in final QA report

### Phase 5.6: Marketing Language Detection

**Objective:** Identify and flag promotional language that should be replaced with factual statements.

**Why This Matters:**
Enterprise-grade competitive analysis must be objective and fact-based. Marketing language undermines credibility and can lead to biased decision-making.

**Marketing Language Patterns to Flag:**

1. **Superlatives Without Evidence:**
   - "best-in-class", "industry-leading", "world-class"
   - "premier", "top-tier", "cutting-edge"
   - "unmatched", "unparalleled", "superior"
   - **Fix:** Replace with specific, measurable claims or remove

2. **Vague Promotional Claims:**
   - "revolutionary", "game-changing", "transformative"
   - "seamless", "robust", "powerful"
   - "comprehensive", "holistic", "end-to-end" (without specifics)
   - **Fix:** Define specifically what is meant or cite user reviews

3. **Unsubstantiated Comparisons:**
   - "better than competitors", "outperforms alternatives"
   - "more intuitive", "easier to use", "faster"
   - **Fix:** Cite comparative studies, user ratings, or specific metrics

4. **Emotional Appeals:**
   - "trusted by thousands", "loved by students"
   - "empowering", "inspiring", "delighting"
   - **Fix:** Replace with factual satisfaction data (ratings, NPS)

5. **Future-Tense Marketing:**
   - "will revolutionize", "poised to dominate"
   - "expected to lead", "set to transform"
   - **Fix:** Focus on current capabilities, note roadmap items separately

**Detection Process:**

1. Scan document for marketing language patterns (use word list above)
2. For each match, evaluate context:
   - Is it a direct quote from source? (acceptable if attributed)
   - Is it author's own characterization? (flag for review)
   - Is it supported by evidence? (acceptable if cited)
3. Generate marketing language report

**Marketing Language Report Format:**

```
## Marketing Language Review

**Document:** [filename]
**Date:** [review date]

### Summary
- Marketing phrases detected: X
- Requiring revision: Y
- Acceptable (quoted/supported): Z

### Phrases Requiring Revision

| Line | Phrase | Issue | Suggested Fix |
|------|--------|-------|---------------|
| 23 | "industry-leading platform" | Superlative without evidence | "platform serving X schools" |
| 89 | "seamless integration" | Vague claim | "integrates with X, Y, Z systems (Source, YYYY)" |

### Acceptable Usages
[List cases where marketing language is properly attributed or supported]
```

**Acceptable Exceptions:**
- Direct quotes from company marketing (clearly attributed)
- User review quotes (with source citation)
- Industry analyst characterizations (with citation)
- Historical statements about company positioning (with context)

**Integration with Workflow:**
- Run marketing language check during initial document scan
- Flag issues alongside citation problems
- Include marketing language score in final QA report (target: <5 unattributed promotional phrases)

### Phase 5.7: Cross-Document Consistency Check

**Objective:** Ensure key data points are consistent across all related documents.

**Why This Matters:**
Competitive analysis projects often have the same data (pricing, market share, customer counts) appearing in multiple documents. Inconsistencies undermine credibility and confuse stakeholders.

**High-Risk Data Categories:**

These data types commonly appear in multiple documents and require consistency verification:

1. **Pricing Data:**
   - Per-student pricing
   - Enterprise pricing tiers
   - Implementation fees
   - Check: Executive summary, pricing analysis, competitor profiles

2. **Market Metrics:**
   - Market share percentages
   - Customer counts (schools, students)
   - Geographic coverage
   - Check: All analyses, executive summary, profiles

3. **Company Information:**
   - Founding dates
   - Headquarters locations
   - Employee counts
   - Funding amounts
   - Check: Company profiles, comparative analyses

4. **Product Capabilities:**
   - Feature availability (Yes/No/Partial)
   - Integration partnerships
   - Technology specifications
   - Check: Feature matrices, profiles, recommendations

**Consistency Check Process:**

1. **Extract Key Data Points:**
   - Read all in-scope documents
   - Create data point inventory (what data appears where)
   - Note exact values and their locations

2. **Compare Across Documents:**
   - For each data point appearing 2+ times
   - Compare exact values
   - Flag any discrepancies

3. **Resolve Discrepancies:**
   - Determine correct value (check sources)
   - Update incorrect instances
   - Document resolution

**Cross-Document Consistency Report Format:**

```
## Cross-Document Consistency Check

**Documents Reviewed:** [list of files]
**Date:** [review date]

### Summary
- Key data points tracked: X
- Consistent across all documents: Y (Z%)
- Discrepancies found: N

### Discrepancies Requiring Resolution

| Data Point | Doc 1 Value | Doc 2 Value | Correct Value | Action Needed |
|------------|-------------|-------------|---------------|---------------|
| SCOIR pricing | $4.80/student | $4.50/student | $4.80 (Source, 2024) | Update Doc 2 |
| Naviance schools | 10,000+ | 13,000+ | 13,000+ (Source, 2024) | Update Doc 1 |

### Verified Consistent Data
[List key data points that were verified as consistent]
```

**Automated Consistency Checks:**

Where possible, use grep/search to find all instances of key terms:
- `grep -r "SCOIR.*\$" documents/` - Find all SCOIR pricing mentions
- `grep -r "market share" documents/` - Find all market share claims
- Compare results programmatically

**Integration with Workflow:**
- Run consistency check after all documents are drafted
- Prioritize high-visibility data (executive summary must match details)
- Include consistency score in final QA report (target: 100% consistency)

### Phase 6: Gap Identification

**Step 1: Coverage Assessment**

Identify areas with insufficient evidence:
- **Sparse Citations:** Major claims with only 1-2 sources
- **No Sources:** Assertions without any supporting evidence
- **Vague Claims:** Statements like "many" or "most" without data
- **Outdated Info:** Old sources when recent data available

**Step 2: Missing Information**

Flag important missing information:
- **Product Features:** Key features not mentioned
- **Pricing:** Incomplete pricing information
- **Recent Developments:** Major news not included
- **Competitive Context:** Missing competitor comparisons

**Step 3: Conflicting Information**

Note unresolved conflicts:
- Sources disagree on facts
- Different sources cite different numbers
- Contradictory claims across documents
- Uncertainty not acknowledged

### Phase 7: Quality Assessment

**Step 1: Evaluate Against Standards**

Assess research against quality criteria from `references/quality-standards.md`:

**Evidence Quality:**
- Are primary sources used appropriately?
- Are secondary sources credible?
- Is evidence recent and relevant?
- Are claims properly supported?

**Analysis Quality:**
- Are conclusions logical from evidence?
- Is analysis sufficiently deep?
- Are frameworks applied correctly?
- Are limitations acknowledged?

**Presentation Quality:**
- Is writing clear and professional?
- Is formatting consistent?
- Are tables/charts accurate and helpful?
- Is document suitable for stated audience?

**Step 2: Compare to Benchmarks**

Evaluate against consulting industry standards:
- McKinsey, BCG, Bain quality levels
- Academic research standards
- Industry analyst report standards (Gartner, Forrester)

**Step 3: Identify Improvements**

Suggest specific improvements:
- Add missing sources
- Update outdated information
- Resolve inconsistencies
- Strengthen weak claims
- Enhance analysis depth
- Improve presentation quality

### Phase 8: Generate QA Report

**Step 1: Structure Findings**

Organize findings into clear report:

**Executive Summary:**
- Overall assessment (Pass / Pass with Minor Issues / Needs Revision)
- Critical issues requiring immediate attention
- Number of claims verified vs. unverified
- Key recommendations

**Detailed Findings by Document:**
For each reviewed document:
- Document name and review date
- Claims verified (with confidence level)
- Source issues found
- Consistency problems identified
- Gaps or missing information
- Quality assessment
- Specific recommendations

**Critical Issues List:**
- Claims that need correction
- Broken or inaccessible sources
- Major inconsistencies
- Misleading or unsupported statements

**Recommendations:**
- Priority 1 (Must Fix): Critical corrections
- Priority 2 (Should Fix): Important improvements
- Priority 3 (Nice to Have): Minor enhancements

**Step 2: Provide Evidence**

For each finding, provide:
- **What:** Specific claim or issue
- **Where:** Document location (file, section, line)
- **Issue:** What's wrong or uncertain
- **Evidence:** What verification found
- **Recommendation:** How to fix

**Example:**
```
❌ ISSUE: Market Share Claim Unverified
WHERE: competitor-profile.md, Executive Summary, Line 12
CLAIM: "SCOIR has 12% market share"
ISSUE: Only one source cited, no date, percentage conflicts with other doc
EVIDENCE: Web search found conflicting numbers (10-15% range)
RECOMMENDATION: Add 2+ recent sources, use range if exact number unknown
```

**Step 3: Deliver Report**

Create professional QA report:
- Clear, actionable findings
- Specific locations for all issues
- Evidence for all claims of problems
- Prioritized recommendations
- Estimated time to address issues

See `references/quality-standards.md` for report format examples.

## Review Types

### Quick Validation (30-60 minutes)

**Scope:**
- Critical claims only (exec summary, key findings)
- Spot-check 5-10 major sources
- Basic consistency check
- No comprehensive audit

**Deliverable:**
- Brief bullet-point findings
- Critical issues flagged
- Pass/Needs Work assessment

**When to Use:**
- Time-constrained review
- Pre-meeting sanity check
- Initial quality assessment

### Standard Review (2-4 hours)

**Scope:**
- Verify key claims (20-30 claims)
- Validate major sources (10-15 sources)
- Cross-document consistency
- Gap identification

**Deliverable:**
- Structured QA report
- Verified/unverified claims list
- Prioritized recommendations
- Quality score

**When to Use:**
- Pre-client delivery
- Important internal review
- Peer review process

### Comprehensive Audit (1-2 days)

**Scope:**
- Verify ALL claims
- Validate ALL sources
- Full consistency analysis
- Deep gap assessment
- Detailed quality evaluation

**Deliverable:**
- Comprehensive QA report
- Claim-by-claim verification
- Full source audit
- Detailed improvement plan
- Executive summary

**When to Use:**
- High-stakes deliverables
- Client-facing reports
- Publication submissions
- Formal audits

### Targeted Fact-Check (Variable)

**Scope:**
- Specific claims flagged by requester
- Particular document section
- Single competitor profile
- Specific type of claim (e.g., all pricing data)

**Deliverable:**
- Focused findings on requested scope
- Verification results
- Targeted recommendations

**When to Use:**
- Specific concerns raised
- Dispute resolution
- Spot verification
- Follow-up on previous issues

## Best Practices

### Verification Excellence

1. **Multi-Source Validation:** Never trust single source for major claims
2. **Primary Source Priority:** Company websites, official reports, SEC filings best
3. **Date Awareness:** Note when information was gathered, flag if outdated
4. **Context Preservation:** Don't take quotes or stats out of context
5. **Bias Recognition:** Note when sources may be biased or have conflicts of interest

### Efficiency Practices

1. **Batch Verification:** Group similar claims, verify together
2. **Use Original Tools:** Bright Data tools used in research often fastest for verification
3. **Document As You Go:** Note findings immediately, don't rely on memory
4. **Focus High-Risk:** Verify critical claims thoroughly, spot-check less critical
5. **Know When to Stop:** Perfect is enemy of good, time-box verification

### Communication Practices

1. **Be Specific:** Always cite document, section, line for issues
2. **Provide Evidence:** Show what verification found
3. **Be Constructive:** Frame as opportunities to strengthen, not criticism
4. **Prioritize:** Critical vs. nice-to-have improvements
5. **Acknowledge Uncertainty:** Some claims may be unverifiable (that's okay)

### Quality Mindset

1. **Professional Skepticism:** Verify but don't assume error
2. **Evidence-Based:** Every finding needs evidence
3. **Fair Assessment:** Compare to realistic standards, not perfection
4. **Collaborative Spirit:** Goal is better deliverable, not finding fault
5. **Client Focus:** Would client be satisfied with this quality?

## Common Issues & Solutions

### Issue: Broken Citation Links

**Problem:** URL in citation is inaccessible or returns 404

**Solution:**
1. Use web_search to find updated URL or archived version
2. Search for content using title/author
3. Note if content has changed or been removed
4. Recommend updating citation or finding alternative source

### Issue: Claim Without Source

**Problem:** Important claim has no supporting citation

**Solution:**
1. Use web_search or Bright Data to find supporting sources
2. If found, recommend adding citation
3. If not found, flag claim for removal or qualification
4. Consider if claim is common knowledge (citation may not be needed)

### Issue: Inconsistent Information

**Problem:** Different numbers or facts across documents

**Solution:**
1. Verify which version is correct using sources
2. If both correct (different timeframes), clarify dates
3. If one incorrect, recommend correction
4. If uncertainty, recommend noting range or caveat

### Issue: Outdated Information

**Problem:** Source is old, newer information likely available

**Solution:**
1. Search for recent sources using web_search
2. If newer info found, recommend update
3. If no newer info, note last-updated date
4. Accept that some info (history, founding dates) won't have recent sources

### Issue: Conflicting Sources

**Problem:** Multiple sources provide different facts

**Solution:**
1. Seek third-party authoritative source (tiebreaker)
2. Use most recent and authoritative source
3. If unresolved, recommend noting range or uncertainty
4. Consider if discrepancy is material (does it matter?)

### Issue: Vague or Subjective Claim

**Problem:** Claim is opinion or subjective without qualification

**Solution:**
1. Identify as opinion, not fact
2. If supported by evidence, recommend clarifying ("according to X sources" or "reviews suggest")
3. If unsupported, recommend softening or removing
4. Distinguish between analysis (supported opinion) and speculation

## References

- **verification-checklist.md** - Comprehensive checklist of what to verify by category (company info, market data, features, pricing, claims, sources, consistency)
- **quality-standards.md** - Consulting-grade quality standards, common quality issues, report format examples, benchmark comparisons
- **fact-checking-methodology.md** - Detailed techniques for verifying different types of claims, source evaluation criteria, triangulation strategies, handling uncertainty

Load these references as needed based on review scope and specific verification challenges.

## Integration with Competitive Research Skill

This skill works as an optional companion to the competitive-research-brightdata skill. **You control when/if QA happens** by explicitly requesting review.

**Optional Workflow (You Decide Each Step):**

**Step 1: Do Research** (competitive-research-brightdata)
- You conduct research using Bright Data tools
- You create company profiles, analyses, reports
- You cite sources, document findings

**Step 2: Request QA Review (ONLY When You Want It)** (research-quality-assurance)
- **You explicitly ask:** "Review the Naviance profile" or "Fact-check the pricing analysis"
- **Then this skill activates** to verify claims, check consistency, validate sources
- **Generates QA report** with findings

**Step 3: Fix Issues (If Needed)** (competitive-research-brightdata)
- **You decide:** Address critical issues, make improvements
- **You update:** Documents based on QA findings

**Step 4: Request Final Check (ONLY If You Want It)** (research-quality-assurance)
- **Optional:** "Quick validation that I fixed the issues"
- **Or skip:** Deliver without final QA if you're confident

**Step 5: Deliver When YOU Decide It's Ready**
- You determine when deliverable meets your standards
- You decide when to present to client

**Key Point:** Nothing happens automatically. You explicitly request each QA step only when you want quality review.

## Success Metrics

**Quality Indicators:**
- % of claims verified from multiple sources
- % of citations validated as accurate
- Critical issues identified and resolved
- Document consistency score
- Client satisfaction with deliverable quality

**Efficiency Metrics:**
- Review time per document
- Issues found per hour of review
- False positive rate (non-issues flagged)
- Turnaround time for QA reports

**Impact Metrics:**
- Errors caught before client delivery
- Client questions/disputes after delivery
- Repeat business (client trust)
- Reputation for quality research

---

**When to Use This Skill:**

✅ Review completed research before client delivery  
✅ Fact-check specific claims that seem uncertain  
✅ Validate sources and citations  
✅ Check consistency across multiple documents  
✅ Assess quality against consulting standards  
✅ Pre-delivery QA audit  

❌ Not for initial research (use competitive-research-brightdata)  
❌ Not for generating new findings (use research skill)  
❌ Not for strategic recommendations (that's analysis phase)

