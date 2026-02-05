---
name: nci-manipulation-analysis
description: Analyzes content for manipulation techniques using the NCI (Narrative Credibility Index) Protocol. Detects emotional manipulation, suspicious timing, uniform messaging, tribal division, and missing information across 20 categories. Use when asked to analyze content for manipulation, propaganda, disinformation patterns, or when user provides a URL or text asking "is this manipulative?", "analyze this for bias", "check for propaganda", or similar requests.
---

# NCI Manipulation Analysis

Pattern-based manipulation detection that identifies **how** content tries to influence you, not whether claims are factually true. Manipulation techniques leave fingerprints regardless of underlying accuracy.

## Quick Start

### For Text Content
1. Read the content provided by user
2. Apply 20-category analysis (see [references/categories.md](references/categories.md))
3. Calculate composite factors and overall score (see [references/scoring.md](references/scoring.md))
4. **Check deep research triggers** - if score > 40 or key categories elevated, verify claims
5. Generate dual perspectives
6. Output report in requested format

### For URLs
1. Use `WebFetch` to retrieve content from URL
2. Extract main article/post text
3. Proceed with text analysis workflow
4. Note source metadata (publication, date, author)
5. **If triggers met**: Use `fact-checker` agent to verify key claims

## First Principles (Summary)

The NCI Protocol is grounded in these principles (see `agents/perspective-generator.md` for full version):

1. **Evidence over authority** - Evaluate patterns in content, not source reputation
2. **Steel-man interpretation** - Present strongest version of each perspective
3. **Atomic decomposition** - Break claims into smallest verifiable units
4. **Source agnosticism** - Apply identical standards regardless of source alignment
5. **Bidirectional beneficiary analysis** - Ask who benefits if believed AND if dismissed
6. **Pattern vs. Intent** - Focus on techniques; deep research evidence can inform motives

These principles ensure fair, consistent analysis across all content regardless of political or ideological alignment.

## Workflow

```
Progress:
- [ ] 1. Input Processing (text or URL)
- [ ] 2. Score all 20 categories (1-5 scale each)
- [ ] 3. Calculate 5 composite factors
- [ ] 4. Calculate overall score (0-100)
- [ ] 5. Check deep research triggers (see Step 5)
- [ ] 6. Generate perspectives (manipulative + legitimate)
- [ ] 7. Output report
```

### Step 1: Input Processing

**For direct text:**
```
INPUT TYPE: Text
LENGTH: [word count]
CONTEXT PROVIDED: [any user context]
```

**For URLs:**
```
INPUT TYPE: URL
URL: [url]
Fetching content with WebFetch...
EXTRACTED: [article title, publication, date if available]
```

When processing URLs, also check:
- Publication reputation
- Author credentials (if available)
- Publication date and timeliness

### Step 2: Score All 20 Categories

For each category, provide:
```
CATEGORY #[N]: [Name]
Score: [1-5]
Evidence: [Specific quotes/patterns from content]
Confidence: [LOW/MED/HIGH]
```

See [references/categories.md](references/categories.md) for detailed category definitions and scoring criteria.

**Detection signals to look for:**

| Signal Type | Examples |
|------------|----------|
| Emotional vocabulary | fear, outrage, danger, threat, shocking |
| Urgency language | immediately, urgent, now, before it's too late |
| Tribal markers | we/they asymmetry, us vs them, real patriots |
| Dehumanizing terms | animals, vermin, horde, infestation |
| Attribution asymmetry | stated/confirmed vs claimed/alleged |
| Logical fallacies | whataboutism, false equivalence, ad hominem |

### Step 3: Calculate Composite Factors

See [references/scoring.md](references/scoring.md) for weights.

```
COMPOSITE FACTORS:
─────────────────
Emotional Manipulation: [weighted avg of cat 1-5] → [1-5 scale]
Suspicious Timing:      [weighted avg of cat 6-8] → [1-5 scale]
Uniform Messaging:      [weighted avg of cat 9-11] → [1-5 scale]
Tribal Division:        [weighted avg of cat 12-14] → [1-5 scale]
Missing Information:    [weighted avg of cat 15-20] → [1-5 scale]
```

### Step 4: Calculate Overall Score

```
OVERALL SCORE = Σ(composite_factor × weight × confidence)

Weights:
- Emotional Manipulation: 25%
- Suspicious Timing: 20%
- Uniform Messaging: 20%
- Tribal Division: 15%
- Missing Information: 20%

Scale 1-5 → 0-100: overall_score = (weighted_avg - 1) × 25
```

### Step 5: Check Deep Research Triggers

After calculating scores, check if deep research is needed for claim verification.

**Trigger Conditions** (if ANY are met, proceed to verification):

```
DEEP RESEARCH CHECK:
─────────────────────
Overall NCI Score > 40?        [ ] Yes → Verify key claims
Suspicious Timing > 3?         [ ] Yes → Correlate events, timeline
Authority Issues (Cat 16) > 3? [ ] Yes → Verify credentials
Cherry-Picking (Cat 18) > 3?   [ ] Yes → Find omitted context
Historical Parallels > 2?      [ ] Yes → Research precedent campaigns

TRIGGERS MET: [N] → If > 0, proceed to verification
```

**If Triggers Met:**

1. **Extract Key Claims**: Identify 3-5 most impactful factual assertions
2. **Invoke Claim Verifier**: Use `fact-checker` agent or `/decipon:verify`
3. **Apply Deep Research**: Use `../deep-research/SKILL.md` methodology
4. **Track Results**:
   ```
   CLAIM: [Statement]
   STATUS: [VERIFIED / PARTIALLY VERIFIED / UNVERIFIED / CONTRADICTED]
   SOURCE: [URL]
   CONFIDENCE: [1-100]
   NCI IMPACT: [How this affects scores]
   ```

5. **Adjust Scores If Needed**:
   - Verified claims → May reduce Authority Issues, Cherry-Picking scores
   - Contradicted claims → Increase relevant category scores
   - Document adjustments in final report

**If No Triggers Met:**
Proceed directly to Step 6 (Perspective Generation).

### Step 6: Generate Dual Perspectives

**CRITICAL**: Always generate BOTH interpretations.

```
MANIPULATIVE INTERPRETATION:
This content appears designed to [specific manipulation goal].
Key manipulation techniques detected:
- [Technique 1 with evidence]
- [Technique 2 with evidence]
- [Technique 3 with evidence]
Confidence: [X]%

LEGITIMATE INTERPRETATION:
This content may reflect [genuine intent/concern].
Supporting factors:
- [Factor 1]
- [Factor 2]
- [Factor 3]
Confidence: [Y]%
```

For perspective generation guidance, leverage the critique framework from the deep-research skill if available.

### Step 7: Output Report

**Standard Format (Markdown):**

```markdown
# NCI Analysis Report

## Content Summary
[Brief description of analyzed content]

## Overall Score: [0-100] [severity indicator]
Confidence: [X]%

## Composite Factors
| Factor | Score | Confidence |
|--------|-------|------------|
| Emotional Manipulation | [X.X]/5 | [%] |
| Suspicious Timing | [X.X]/5 | [%] |
| Uniform Messaging | [X.X]/5 | [%] |
| Tribal Division | [X.X]/5 | [%] |
| Missing Information | [X.X]/5 | [%] |

## Key Findings
[Top 3-5 manipulation indicators with evidence]

## Claim Verification (if deep research triggered)
| Claim | Status | Confidence | Source |
|-------|--------|------------|--------|
| [Claim 1] | [VERIFIED/etc] | [%] | [URL] |
| [Claim 2] | [Status] | [%] | [URL] |

**Score Adjustment**: [Original] → [Adjusted] ([+/-N] due to verification)

## Perspectives
### If Manipulative
[Manipulative interpretation]

### If Legitimate
[Legitimate interpretation]

## Category Details
[Expandable section with all 20 category scores]

## Methodology
NCI Protocol v1.0 - Pattern-based manipulation detection
Deep Research: [Yes/No] - [N] claims verified
```

**Severity Indicators (NCI Protocol v1.0):**
- 0-25: `[·]` Low manipulation risk
- 26-50: `[!]` Moderate - some concerning patterns
- 51-75: `[!!]` High - strong manipulation patterns
- 76-100: `[!!!]` Severe - overwhelming manipulation signs

## Integration with Deep Research

This plugin includes the deep-research skill for fact-checking and claim verification. Reference: `../deep-research/SKILL.md`

### Automatic Triggers

Deep research is recommended when NCI analysis shows:

| Trigger | Threshold | Verification Focus |
|---------|-----------|-------------------|
| Overall NCI Score | > 40 (upper Moderate) | Verify key claims |
| Suspicious Timing | > 3 | Correlate events, check timeline |
| Authority Issues | > 3 | Verify credentials, expertise claims |
| Cherry-Picking | > 3 | Find omitted context, full data |
| Historical Parallels | > 2 | Research precedent campaigns |

### Workflow Integration

```
NCI + DEEP RESEARCH WORKFLOW:
─────────────────────────────
1. Complete NCI analysis (Steps 1-6)
2. Check trigger conditions
3. If triggered:
   - Extract key factual claims
   - Apply claim-verifier agent
   - Use deep research methodology
   - Update scores based on findings
4. Generate final report with verification status
```

### Using the Claim Verifier

After NCI analysis, invoke the claim-verifier agent:
- See `../agents/claim-verifier.md` for verification workflow
- Uses source evaluation from `../deep-research/references/source-evaluation.md`
- Applies critique framework from `../deep-research/references/critique-framework.md`

### Verification Commands

| Command | Purpose |
|---------|---------|
| `/decipon:analyze` | Pattern analysis (this skill) |
| `/decipon:verify` | Fact-check claims with deep research |
| `/decipon:report` | Combined analysis + verification report |

### Source Evaluation Integration

When assessing sources during NCI analysis, apply confidence scoring:

| Source Type | Confidence | NCI Consideration |
|-------------|------------|-------------------|
| Official documentation | 85-95 | Reduces Authority Issues if verified |
| Government/institutional | 75-90 | Check for political context |
| Major news (AP, Reuters) | 70-85 | Generally reliable baseline |
| Partisan outlets | 40-60 | Note bias, affects Tribal Division |
| Anonymous/undated | 10-30 | Increases Missing Information |

See `../deep-research/references/source-evaluation.md` for detailed scoring.

### Contradiction Handling

When sources disagree during verification:
1. Note the contradiction explicitly
2. Apply confidence scoring to each source
3. Research additional sources to resolve
4. If unresolved, present both perspectives in report

See `../deep-research/references/critique-framework.md` for resolution protocol.

## Examples

See [references/examples.md](references/examples.md) for historical case studies including:
- Nayirah Testimony (1990) - Score: 88
- Tobacco Industry Campaign - Score: 82
- Modern examples with full category breakdowns

## When to Use

**Use NCI Analysis:**
- Content claiming urgent action needed
- Viral stories with strong emotional triggers
- Content creating clear us-vs-them dynamics
- Stories suspiciously timed with political events
- Content from unknown or questionable sources

**Don't Use:**
- Simple factual lookups (use fact-checking)
- Opinion pieces clearly labeled as such
- Personal correspondence
- Fiction/entertainment

## References

- [references/categories.md](references/categories.md) - All 20 category definitions with detection signals
- [references/scoring.md](references/scoring.md) - Scoring methodology, weights, and quantitative formulas
- [references/examples.md](references/examples.md) - Historical case studies for calibration
- [references/vocabulary.md](references/vocabulary.md) - Detection vocabulary lists
- [references/guidance.md](references/guidance.md) - Actionable tips per factor
