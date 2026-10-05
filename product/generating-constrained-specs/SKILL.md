---
name: generating-constrained-specs
description: Use when generating PRD and architecture documents that must trace back to explicit decisions. Enforces citation requirements so no spec content exists without DEC-* references.
context: fork
agent: general-purpose
---

# Constrained Spec Generation

This skill generates PRD and architecture documents that are constrained by the decision ledger.

## Core Principle

**No spec section without a DEC-* reference.**

Every requirement, every architecture choice, must trace back to an explicit decision. This prevents:
- Ungrounded requirements
- Hidden assumptions
- Scope creep
- Orphaned features

## Prerequisites

- Decisions complete (`/ledger-decide`)
- `04-decisions/DECISIONS.yaml` exists
- `05-risks/RISKS.yaml` exists

## Workflow

Use TodoWrite to track these mandatory steps:

<required>
1. Load decisions and risks
2. Generate PRD with decision citations
3. Validate PRD constraint gate
4. Generate architecture with decision citations
5. Validate architecture constraint gate
6. Cross-reference risks in both documents
</required>

### Step 1: Load Decisions and Risks

Read:
- `04-decisions/DECISIONS.yaml` - All decisions
- `05-risks/RISKS.yaml` - All risks
- `03-synthesis/CROSS-SYNTHESIS.md` - Context

Build decision index for quick lookup.

### Step 2: Generate PRD

Write `06-prd/PRD.md` using template from [references/prd-template.md](references/prd-template.md).

**Constraint enforcement:**
Every section heading must include decision reference:
```markdown
## 2. Target Users (DEC-scope-power-users-first)
```

Every requirement must cite decisions:
```markdown
### 2.1 Primary Users
Power users within SMB organizations who manage complex workflows.
(DEC-scope-power-users-first, DEC-scope-smb-segment)
```

### Step 3: Validate PRD Constraint Gate

Check every PRD section:
- [ ] Section heading has DEC-* reference
- [ ] Requirements cite supporting decisions
- [ ] Risks are cross-referenced where relevant

**Gate failure:** If any section lacks DEC-* reference, cannot proceed.

### Step 4: Generate Architecture

Write `07-architecture/ARCHITECTURE.md` using template from [references/architecture-template.md](references/architecture-template.md).

**Constraint enforcement:**
```markdown
## 3. Data Model (DEC-tech-postgres-primary, DEC-scope-power-users-first)

### 3.1 Core Entities
Based on power user workflow requirements (DEC-scope-power-users-first),
the data model supports complex nested structures.
```

### Step 5: Validate Architecture Constraint Gate

Check every architecture section:
- [ ] Section heading has DEC-* reference
- [ ] Technical choices cite supporting decisions
- [ ] Risks are cross-referenced where relevant

### Step 6: Cross-Reference Risks

In both documents, note relevant risks:
```markdown
### Risk Note
This approach carries RISK-tech-cold-start. See risk register for mitigations.
```

## Constraint Rules

See [references/constraint-rules.md](references/constraint-rules.md) for detailed rules.

### Citation Format

**Section headings:**
```markdown
## 2. MVP Scope (DEC-scope-power-users-first, DEC-scope-web-only)
```

**Inline citations:**
```markdown
Users will access the application via web browser only. (DEC-scope-web-only)
```

**Evidence when needed:**
```markdown
Based on user research showing 78% onboarding drop-off at team invitation
(EV-users-onboarding-dropoff), we will simplify the invitation flow.
(DEC-ux-simplified-onboarding)
```

<good-example>
```markdown
## 2. Target Users (DEC-scope-power-users-first)

Based on DEC-scope-power-users-first, the MVP targets power users within
organizations who manage complex workflows. This decision was supported by
evidence showing 3x higher retention among power users (EV-users-retention-power-users).

### 2.1 User Needs
- Complex workflow management (DEC-scope-power-users-first)
- Keyboard-first interaction (DEC-ux-keyboard-shortcuts-priority)

**Risk:** RISK-retention-expert-churn mitigated by advanced feature set.
```
- Section heading cites DEC-* reference
- Every requirement traces to a decision
- Evidence cited where relevant
- Risks cross-referenced
</good-example>

<bad-example>
```markdown
## 2. Target Users

We will target power users because they are important. Power users need
features like advanced workflows and keyboard shortcuts.

### 2.1 User Needs
- Complex workflow management
- Keyboard-first interaction
```
- No DEC-* citation in heading
- No evidence supporting claims
- No traceability to decisions
- No risk acknowledgment
</bad-example>

### What Cannot Be Spec'd

- Features not supported by any decision
- Requirements contradicting decisions
- Architecture choices without technical decisions
- Scope outside decision boundaries

## User Interaction

Use the **AskUserQuestion tool** when:

### Missing decision for section
```
Question: "PRD section '[X]' has no supporting decision. How to proceed?"
Options:
- "Skip this section (out of scope)"
- "Make a new decision for this"
- "It relates to existing decision [DEC-Y]"
```

### Decision conflict
```
Question: "Requirement '[X]' seems to conflict with [DEC-Y]. How to resolve?"
Options:
- "Revise requirement to align with decision"
- "The decision should be revisited"
- "They don't actually conflict - explain how"
```

### Risk acknowledgment
```
Question: "This section relates to [RISK-X]. Include risk note?"
Options:
- "Yes, note the risk"
- "No, not relevant here"
- "Yes, and add mitigation detail"
```

## Output

After spec generation:

```markdown
## Spec Generation Complete

**PRD Sections:** [N] (all constrained)
**Architecture Sections:** [M] (all constrained)
**Decisions Referenced:** [X] unique DEC-* IDs
**Risks Cross-Referenced:** [Y] RISK-* IDs

### Constraint Gate Status
- PRD gate: ✓ All sections cite decisions
- Architecture gate: ✓ All sections cite decisions

### Documents Generated
- `06-prd/PRD.md`
- `07-architecture/ARCHITECTURE.md`

### Decision Coverage
| Decision | PRD Sections | Arch Sections |
|----------|--------------|---------------|
| DEC-scope-power-users-first | 1, 2, 4 | 2, 3 |
| DEC-pricing-freemium | 3, 5 | 4 |
| DEC-tech-serverless | - | 1, 3, 5 |
| ... | ... | ... |

### Next Step
Run `/ledger-plan` to generate implementation backlog.
```

## References

- [references/prd-template.md](references/prd-template.md) - PRD template
- [references/architecture-template.md](references/architecture-template.md) - Architecture template
- [references/constraint-rules.md](references/constraint-rules.md) - Detailed constraint rules
