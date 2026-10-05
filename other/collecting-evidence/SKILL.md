---
name: collecting-evidence
description: Use when researching a specific pillar and need to create traceable evidence objects. Guides creation of YAML evidence files with semantic IDs, confidence scores, and assumptions.
context: fork
agent: general-purpose
---

# Evidence Collection

This skill guides the creation of structured Evidence Objects for a single research pillar.

## Prerequisites

- Ledger workspace initialized (`/ledger-init` completed)
- Pillar assignment (which pillar to research)
- Research scope from `01-pillars/PILLARS.md`

## Workflow

Use TodoWrite to track these mandatory steps:

<required>
1. Load pillar scope and research questions
2. Identify evidence sources
3. Collect raw evidence
4. Create Evidence Objects with semantic IDs
5. Validate evidence quality
6. Check evidence gate (minimum 5 per pillar)
</required>

### Step 1: Load Pillar Scope

Read `01-pillars/PILLARS.md` to understand:
- Pillar priority level
- Specific research questions for this pillar
- Any scope restrictions

See [references/research-protocols.md](references/research-protocols.md) for pillar-specific protocols.

### Step 2: Identify Evidence Sources

For each research question, identify potential sources:

| Source Type | Examples | Typical Confidence |
|-------------|----------|-------------------|
| `url` | Research reports, documentation | 60-90 |
| `pdf` | Academic papers, whitepapers | 70-95 |
| `interview` | User interviews, expert calls | 50-80 |
| `internal-doc` | Company data, prior research | 60-85 |
| `experiment` | A/B tests, prototypes | 70-95 |
| `dataset` | Analytics, survey results | 65-90 |

### Step 3: Collect Raw Evidence

For each source:
1. Extract the key claim(s)
2. Note supporting quotes/data
3. Assess confidence level
4. List assumptions

**Web research protocol:**
- Use WebSearch for discovery
- Use WebFetch to retrieve and analyze content
- Track source URLs and retrieval dates
- Note if sources agree or contradict

### Step 4: Create Evidence Objects

Write YAML files to `02-evidence/<pillar>/`.

**Naming:** Use semantic IDs per [references/id-generation-rules.md](references/id-generation-rules.md).

**Schema:** See [references/evidence-object-schema.md](references/evidence-object-schema.md).

<good-example>
```yaml
id: EV-market-pricing-smb-wtp
pillar: market
source:
  type: url
  ref: "https://example.com/pricing-research"
  retrieved_at: 2026-01-21
claim: "SMB segment willingness-to-pay peaks at $29/mo for productivity tools."
quote: "Our survey of 500 SMBs found median WTP of $29/month..."
confidence: 0.75
assumptions:
  - "Survey sample representative of target market"
  - "WTP for 'productivity tools' applies to our specific category"
notes: "Sample skewed toward US companies. May need regional validation."
tags:
  - pricing
  - smb
  - wtp
```
- Semantic ID describes content (market-pricing-smb-wtp)
- Falsifiable claim with specific number ($29/mo)
- Honest confidence (0.75, not inflated)
- Explicit assumptions documented
- Source fully traceable
</good-example>

<bad-example>
```yaml
id: EV-001
pillar: market
source:
  type: url
  ref: "some website"
claim: "People like our product"
confidence: 0.95
assumptions: []
```
- Non-semantic ID (EV-001 tells nothing about content)
- Vague, unfalsifiable claim ("people like")
- Overconfident (0.95) without strong source
- No assumptions documented
- Untraceable source reference
</bad-example>

### Step 5: Validate Evidence Quality

Each Evidence Object must pass:

| Check | Requirement |
|-------|-------------|
| Falsifiable claim | Claim can be proven wrong |
| Confidence assigned | 0.0-1.0 value present |
| Assumptions listed | At least 1 assumption |
| Source traceable | Can revisit the source |
| ID is semantic | Follows ID scheme |

**Quality warnings:**
- Confidence > 0.9 without peer-reviewed source
- Multiple evidence objects with identical claims
- Assumptions that can't be tested

### Step 6: Check Evidence Gate

Before synthesis, verify **minimum 5 Evidence Objects** per pillar.

```
Evidence Gate Check: market
├── EV-market-tam-b2b-saas ✓
├── EV-market-pricing-smb-wtp ✓
├── EV-market-growth-remote-tools ✓
├── EV-market-segment-priorities ✓
└── EV-market-competitive-density ✓
Total: 5/5 minimum ✓ GATE PASSED
```

If gate fails, continue research until threshold met.

## User Interaction

Use the **AskUserQuestion tool** when:

### Source prioritization needed
```
Question: "Multiple sources available for [topic]. Which to prioritize?"
Options:
- "Academic/peer-reviewed sources (higher confidence)"
- "Recent industry reports (more current)"
- "Direct user research (more specific)"
- "Research all and compare"
```

### Confidence assessment uncertain
```
Question: "How confident should I rate this claim: '[claim]'?"
Options:
- "High (0.8-0.9) - Strong source, well-supported"
- "Medium (0.5-0.7) - Reasonable source, some uncertainty"
- "Low (0.3-0.5) - Weak source or significant assumptions"
- "Help me assess the source quality"
```

### Contradictory evidence found
```
Question: "Sources disagree on [topic]. Source A says X, Source B says Y."
Options:
- "Create evidence for both, note contradiction"
- "Prioritize more recent source"
- "Prioritize more authoritative source"
- "Research further for resolution"
```

### Evidence gate failing
```
Question: "Only [N] evidence objects for [pillar]. Need [5-N] more to pass gate."
Options:
- "Continue researching this pillar"
- "Accept partial evidence (will affect synthesis quality)"
- "Deprioritize this pillar for MVP"
- "Help me identify additional research areas"
```

## Output

After evidence collection:

```markdown
## Evidence Collection Complete: [pillar]

**Evidence Objects Created:** [N]
**Gate Status:** [PASSED/FAILED]

### Evidence Summary
| ID | Claim Summary | Confidence |
|----|---------------|------------|
| EV-market-tam-b2b-saas | TAM is $X billion | 0.80 |
| EV-market-pricing-smb-wtp | SMB WTP peaks at $29/mo | 0.75 |
| ... | ... | ... |

### Key Findings
- [Top 3 findings from this pillar]

### Contradictions Noted
- [Any conflicting evidence]

### Gaps Remaining
- [Research questions not fully answered]
```

## References

- [references/evidence-object-schema.md](references/evidence-object-schema.md) - YAML schema
- [references/research-protocols.md](references/research-protocols.md) - Pillar-specific research guidance
- [references/id-generation-rules.md](references/id-generation-rules.md) - Semantic ID creation
