---
name: making-decisions
description: Use when transforming synthesis insights into explicit decisions with documented trade-offs. Guides interactive decision-making and risk identification.
context: fork
agent: general-purpose
---

# Decision Ledger

This skill guides the creation of explicit decisions with full trade-off documentation.

## Prerequisites

- Synthesis complete (`/ledger-synthesize`)
- `03-synthesis/CROSS-SYNTHESIS.md` exists with decision candidates
- Per-pillar syntheses in `03-synthesis/SYN-*.md`

## Workflow

Use TodoWrite to track these mandatory steps:

<required>
1. Load decision candidates from cross-synthesis
2. For each candidate, gather evidence and options
3. Present trade-offs for user decision
4. Create decision entry with semantic ID
5. Identify risks created by each decision
6. Generate DECISIONS.yaml and RISKS.yaml
7. Validate decision quality gates
</required>

### Step 1: Load Decision Candidates

Read `03-synthesis/CROSS-SYNTHESIS.md` to extract:
- Decision topics needing resolution
- Supporting evidence from each pillar
- Identified options

### Step 2: Gather Evidence per Decision

For each decision candidate:
- Collect all relevant EV-* IDs
- Summarize what evidence supports each option
- Note confidence levels

```yaml
decision_candidate:
  topic: target-segment-priority
  options:
    - name: SMB-first
      evidence:
        - EV-users-smb-pain-points (0.80)
        - EV-economics-smb-unit-economics (0.75)
    - name: Enterprise-first
      evidence:
        - EV-market-enterprise-tam (0.85)
        - EV-competitors-enterprise-gap (0.70)
```

### Step 3: Present Trade-offs

For each decision, present:
- Options with evidence support
- What you win with each option
- What you lose with each option
- Risks created by each option

Use **AskUserQuestion** to get user's decision.

### Step 4: Create Decision Entry

Write entry to `04-decisions/DECISIONS.yaml` using schema from [references/decision-ledger-schema.md](references/decision-ledger-schema.md).

<good-example>
```yaml
- id: DEC-scope-smb-first
  decision: "Target SMB segment before enterprise"
  status: accepted
  owner: user
  created_at: 2026-01-21
  alternatives:
    - Enterprise-first
    - Multi-segment simultaneous
  evidence:
    - EV-users-smb-pain-points
    - EV-economics-smb-unit-economics
    - EV-market-enterprise-tam
  tradeoffs:
    wins:
      - "Faster iteration cycles with smaller customers"
      - "Lower sales friction (self-serve possible)"
      - "Better unit economics at start"
    loses:
      - "Smaller initial contract values"
      - "May need significant pivot for enterprise later"
  risks:
    - RISK-market-smb-churn-rate
  implications:
    - "MVP UX must optimize for self-serve onboarding"
    - "Pricing must fit SMB budget constraints"
```
- Semantic ID (DEC-scope-smb-first)
- Explicit alternatives documented
- Multiple evidence citations (3+)
- Both wins AND loses documented
- Linked risks and implications
</good-example>

<bad-example>
```yaml
- id: DEC-001
  decision: "Do the thing"
  status: accepted
  alternatives: []
  evidence: []
  tradeoffs:
    wins:
      - "It will be good"
    loses: []
```
- Non-semantic ID (DEC-001)
- Vague decision statement
- No alternatives considered
- No evidence cited
- No loses documented (unrealistic)
</bad-example>

### Step 5: Identify Created Risks

Each decision may create risks. For each identified risk:
- Create entry in `05-risks/RISKS.yaml`
- Link back to creating decision
- Document triggers and mitigations

See [references/risk-ledger-schema.md](references/risk-ledger-schema.md) for schema.

### Step 6: Generate Ledger Files

Write complete files:
- `04-decisions/DECISIONS.yaml`
- `05-risks/RISKS.yaml`

### Step 7: Validate Quality Gates

**Decision quality gate:**
- Every decision cites ≥2 evidence IDs
- Every decision lists ≥1 alternative considered
- Every decision documents wins AND loses

**Risk quality gate:**
- Every risk links to creating decision
- Every risk has severity and likelihood
- Every risk has ≥1 mitigation

## User Interaction

Use the **AskUserQuestion tool** for every decision:

### Decision prompt
```
Question: "Decision needed: [topic]"
Options:
- "[Option A] - supported by [evidence summary]"
- "[Option B] - supported by [evidence summary]"
- "[Option C] - supported by [evidence summary]"
- "Need more information before deciding"
```

### Trade-off confirmation
```
Question: "You chose [option]. Confirming trade-offs:"
Options:
- "Yes, I accept these trade-offs"
- "Wait, I want to reconsider"
- "Explain the trade-offs more"
```

### Decision status
```
Question: "Should this decision be marked as:"
Options:
- "Accepted (committed)"
- "Provisional (may revisit)"
- "Need more research first"
```

### Risk severity
```
Question: "This decision creates risk: [risk]. How severe?"
Options:
- "High - requires immediate mitigation"
- "Medium - should have mitigation plan"
- "Low - acceptable risk"
```

## Output

After decision-making:

```markdown
## Decisions Complete

**Decisions Made:** [N]
**Status:** [X] accepted, [Y] provisional
**Risks Identified:** [Z]

### Decisions Summary
| ID | Decision | Status | Evidence Count |
|----|----------|--------|----------------|
| DEC-scope-smb-first | Target SMB first | accepted | 4 |
| DEC-pricing-freemium | Use freemium model | provisional | 3 |
| ... | ... | ... | ... |

### Risks Created
| ID | Risk | Severity | Linked Decision |
|----|------|----------|-----------------|
| RISK-market-smb-churn | SMB churn rate | medium | DEC-scope-smb-first |
| ... | ... | ... | ... |

### Quality Gate Status
- Decision gate: ✓ All decisions cite ≥2 evidence
- Risk gate: ✓ All risks have mitigations

### Next Step
Run `/ledger-spec` to generate constrained PRD and architecture.
```

## References

- [references/decision-ledger-schema.md](references/decision-ledger-schema.md) - DECISIONS.yaml schema
- [references/risk-ledger-schema.md](references/risk-ledger-schema.md) - RISKS.yaml schema
