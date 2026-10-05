---
name: synthesizing-pillars
description: Use when evidence collection is complete for a pillar and need to extract actionable insights. Transforms raw evidence into structured synthesis with patterns and contradictions identified.
context: fork
agent: general-purpose
---

# Pillar Synthesis

This skill transforms raw evidence objects into structured insights for a single research pillar.

## Prerequisites

- Evidence gate passed (≥5 evidence objects for this pillar)
- Evidence objects in `02-evidence/<pillar>/`

## Workflow

Use TodoWrite to track these mandatory steps:

<required>
1. Load all evidence objects for the pillar
2. Identify patterns and themes
3. Resolve or document contradictions
4. Extract key insights
5. Generate synthesis document
6. Link insights to evidence IDs
</required>

### Step 1: Load Evidence

Read all `EV-<pillar>-*.yaml` files from `02-evidence/<pillar>/`.

For each evidence object, extract:
- Claim
- Confidence
- Assumptions
- Tags

Build a working set of all claims.

### Step 2: Identify Patterns

Group evidence by theme:
- What claims cluster together?
- What topics have multiple evidence points?
- What themes emerge across sources?

**Pattern identification:**
```
Theme: Pricing
├── EV-market-pricing-smb-wtp (0.75) - SMB WTP $29
├── EV-market-pricing-enterprise-wtp (0.80) - Enterprise WTP $99
└── EV-competitors-pricing-benchmark (0.70) - Market avg $45

Insight: Pricing flexibility needed for multi-segment
```

### Step 3: Handle Contradictions

For contradictory evidence:

1. **Note the contradiction explicitly**
2. **Assess confidence delta** - Higher confidence wins if large gap
3. **Check recency** - More recent may supersede older
4. **Check authority** - More authoritative source wins
5. **If unresolved** - Document both, flag for decision-making

```markdown
### Contradiction: User Segment Priority

**EV-users-segment-power-users** (0.70): Power users drive retention
**EV-users-segment-casual** (0.65): Casual users drive growth

**Resolution:** Unresolved. Both valid for different goals.
**Recommendation:** Requires explicit decision (DEC-*)
```

### Step 4: Extract Key Insights

For each theme, formulate 1-3 key insights:

**Insight structure:**
- **Observation:** What the evidence shows
- **Implication:** What this means for the product
- **Confidence:** How confident we are (based on evidence)
- **Evidence:** Which EV-* IDs support this

<good-example>
```yaml
insight: "SMB segment has price sensitivity ceiling at $30/mo"
observation: "Multiple sources confirm $29-30 WTP peak"
implication: "Pricing above $30 requires enterprise features"
confidence: 0.75
evidence:
  - EV-market-pricing-smb-wtp
  - EV-competitors-pricing-benchmark
```
- Specific, falsifiable insight
- Clear observation and implication
- Evidence IDs cited
- Appropriate confidence based on evidence
</good-example>

<bad-example>
```yaml
insight: "Users like low prices"
observation: "People prefer cheaper things"
implication: "We should be cheap"
confidence: 0.9
evidence: []
```
- Vague, non-actionable insight
- Obvious observation with no research backing
- No evidence citations
- Overconfident without evidence
</bad-example>

### Step 5: Generate Synthesis Document

Write `03-synthesis/SYN-<pillar>.md` using template from [references/synthesis-template.md](references/synthesis-template.md).

**Required sections:**
1. Executive Summary (3-5 bullet points)
2. Key Insights (with evidence citations)
3. Contradictions and Resolutions
4. Gaps and Uncertainties
5. Recommended Decisions (what needs explicit DEC-*)

### Step 6: Link to Evidence

Every insight must cite evidence:

```markdown
## Key Insight: Price Ceiling

SMB segment shows consistent willingness-to-pay ceiling around $30/month.
(EV-market-pricing-smb-wtp, EV-competitors-pricing-benchmark)

This suggests pricing above $30 requires additional value justification
or enterprise-focused features.
```

## User Interaction

Use the **AskUserQuestion tool** when:

### Contradiction resolution needed
```
Question: "Evidence conflicts on [topic]. How should I resolve?"
Options:
- "Favor higher confidence source"
- "Favor more recent source"
- "Document both, defer to decision phase"
- "Help me assess the sources"
```

### Insight interpretation unclear
```
Question: "Evidence suggests [X]. Is this interpretation correct?"
Options:
- "Yes, that interpretation is correct"
- "No, the implication is different"
- "Need more context to interpret"
```

### Gap identification
```
Question: "Synthesis reveals gap in [area]. How to handle?"
Options:
- "Note gap, proceed with available evidence"
- "Request additional research"
- "Critical gap - block until resolved"
```

## Output

After synthesis:

```markdown
## Synthesis Complete: [pillar]

**Evidence Analyzed:** [N] objects
**Key Insights:** [M]
**Contradictions:** [X] ([Y] resolved, [Z] pending)

### Top Insights
1. [Insight with evidence citation]
2. [Insight with evidence citation]
3. [Insight with evidence citation]

### Decisions Needed
- [Topic requiring DEC-*]
- [Another decision point]

### Document Location
`03-synthesis/SYN-<pillar>.md`
```

## References

- [references/synthesis-template.md](references/synthesis-template.md) - Document template
