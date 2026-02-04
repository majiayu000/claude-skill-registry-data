---
name: ethics-review
description: AI and technology ethics review including ethical impact assessment, stakeholder analysis, and responsible innovation frameworks
allowed-tools: Read, Glob, Grep, Write, Edit, Task
---

# Ethics Review

Comprehensive guidance for ethical assessment of technology systems, AI applications, and responsible innovation.

## When to Use This Skill

- Conducting ethical impact assessments for new projects
- Evaluating AI systems for ethical risks
- Establishing ethics review boards and processes
- Developing ethical guidelines for technology teams
- Assessing stakeholder impacts and potential harms

## Core Ethical Principles

### Foundation Principles

| Principle | Description | Application |
|-----------|-------------|-------------|
| **Beneficence** | Do good, maximize benefits | Design for positive outcomes |
| **Non-maleficence** | Do no harm, minimize risks | Identify and mitigate harms |
| **Autonomy** | Respect individual choice | Informed consent, opt-out |
| **Justice** | Fair distribution of benefits/burdens | Equitable access, no discrimination |
| **Transparency** | Open about how systems work | Explainable AI, clear documentation |
| **Accountability** | Clear responsibility | Ownership, audit trails |
| **Privacy** | Protect personal information | Data minimization, consent |

### Technology-Specific Principles

```text
AI/ML Systems:
├── Fairness - Equitable treatment across groups
├── Explainability - Understandable decisions
├── Reliability - Consistent, predictable behavior
├── Safety - Prevent harm, fail safely
├── Privacy - Protect personal data
├── Security - Resist adversarial attacks
├── Inclusiveness - Accessible to all users
└── Human Control - Meaningful human oversight
```

## Ethical Impact Assessment Framework

### Assessment Process

```text
┌─────────────────────────────────────────────────────────────┐
│                  Ethical Impact Assessment                   │
├─────────────────────────────────────────────────────────────┤
│  1. Describe     │  System purpose, capabilities, context   │
├──────────────────┼──────────────────────────────────────────┤
│  2. Stakeholder  │  Identify all affected parties           │
│     Analysis     │  Map interests and concerns              │
├──────────────────┼──────────────────────────────────────────┤
│  3. Impact       │  Assess benefits and harms               │
│     Assessment   │  Evaluate likelihood and severity        │
├──────────────────┼──────────────────────────────────────────┤
│  4. Ethical      │  Apply ethical principles                │
│     Analysis     │  Identify conflicts and tensions         │
├──────────────────┼──────────────────────────────────────────┤
│  5. Mitigation   │  Design controls and safeguards          │
│     Planning     │  Define monitoring approach              │
├──────────────────┼──────────────────────────────────────────┤
│  6. Decision &   │  Approve, modify, or reject              │
│     Review       │  Schedule ongoing review                 │
└─────────────────────────────────────────────────────────────┘
```

### Ethical Impact Assessment Template

```markdown
# Ethical Impact Assessment

## 1. System Description

### Purpose
[What is the system designed to do?]

### Capabilities
[What can the system do? What decisions does it make or influence?]

### Context
[Where and how will the system be used?]

### Data
[What data does the system use? How is it collected?]

---

## 2. Stakeholder Analysis

### Direct Stakeholders
| Stakeholder | Relationship | Interests | Power | Concerns |
|-------------|--------------|-----------|-------|----------|
| [Group] | [Relationship] | [Interests] | [H/M/L] | [Concerns] |

### Indirect Stakeholders
| Stakeholder | How Affected | Interests | Concerns |
|-------------|--------------|-----------|----------|
| [Group] | [Impact] | [Interests] | [Concerns] |

### Vulnerable Groups
| Group | Vulnerability | Special Considerations |
|-------|---------------|----------------------|
| [Group] | [Why vulnerable] | [Protections needed] |

---

## 3. Impact Assessment

### Benefits
| Benefit | Beneficiary | Magnitude | Likelihood |
|---------|-------------|-----------|------------|
| [Benefit] | [Who] | [H/M/L] | [H/M/L] |

### Potential Harms
| Harm | Affected Group | Severity | Likelihood | Reversible? |
|------|----------------|----------|------------|-------------|
| [Harm] | [Who] | [H/M/L] | [H/M/L] | [Y/N] |

### Unintended Consequences
| Consequence | Description | Risk Level |
|-------------|-------------|------------|
| [Consequence] | [Details] | [H/M/L] |

---

## 4. Ethical Analysis

### Principle Evaluation

| Principle | Supports | Tensions | Score (1-5) |
|-----------|----------|----------|-------------|
| Beneficence | [How] | [Conflicts] | [Score] |
| Non-maleficence | [How] | [Conflicts] | [Score] |
| Autonomy | [How] | [Conflicts] | [Score] |
| Justice | [How] | [Conflicts] | [Score] |
| Transparency | [How] | [Conflicts] | [Score] |
| Accountability | [How] | [Conflicts] | [Score] |
| Privacy | [How] | [Conflicts] | [Score] |

### Ethical Dilemmas
| Dilemma | Trade-off | Proposed Resolution |
|---------|-----------|---------------------|
| [Dilemma] | [Trade-off] | [Resolution] |

---

## 5. Mitigation Plan

### Technical Mitigations
| Risk | Mitigation | Owner | Status |
|------|------------|-------|--------|
| [Risk] | [Control] | [Who] | [Status] |

### Procedural Mitigations
| Risk | Mitigation | Owner | Status |
|------|------------|-------|--------|
| [Risk] | [Process] | [Who] | [Status] |

### Monitoring Plan
| Metric | Threshold | Frequency | Response |
|--------|-----------|-----------|----------|
| [Metric] | [Limit] | [How often] | [Action] |

---

## 6. Decision

### Recommendation
[ ] Approve - Proceed with current design
[ ] Approve with conditions - Proceed after mitigations
[ ] Defer - Requires further analysis
[ ] Reject - Unacceptable ethical risks

### Conditions (if applicable)
1. [Condition]
2. [Condition]

### Review Schedule
- Initial review: [Date]
- Ongoing review: [Frequency]

### Approvals
| Role | Name | Decision | Date |
|------|------|----------|------|
| Ethics Board | | [ ] | |
| Technical Lead | | [ ] | |
| Business Owner | | [ ] | |
| Legal | | [ ] | |
```

## Harm Assessment Framework

### Categories of Harm

```text
Direct Harms:
├── Physical harm to individuals
├── Psychological harm (stress, manipulation)
├── Financial harm (fraud, loss)
├── Privacy harm (exposure, surveillance)
├── Discrimination harm (unfair treatment)
└── Autonomy harm (manipulation, coercion)

Indirect/Systemic Harms:
├── Environmental harm
├── Democratic harm (manipulation, division)
├── Economic harm (displacement, inequality)
├── Social harm (erosion of trust, relationships)
└── Cultural harm (homogenization, loss)

Group-Specific Harms:
├── Harm to marginalized groups
├── Harm to vulnerable populations
├── Harm to future generations
└── Harm to non-users
```

### Harm Severity Matrix

```text
               REVERSIBILITY
               Easy    Difficult   Permanent
S      Low     1          2           3
E      Medium  2          4           6
V      High    3          6           9
E      Extreme 4          8          12
R
I
T
Y

Score:
1-2:  Acceptable with monitoring
3-4:  Requires mitigation
6-8:  Significant controls required
9-12: May be unacceptable
```

## AI Ethics Specifics

### AI Ethics Checklist

```csharp
public class AiEthicsChecklist
{
    public List<EthicsCheckItem> GetChecklist()
    {
        return new List<EthicsCheckItem>
        {
            // Fairness
            new("FAIR-01", "Bias Testing",
                "Has the model been tested for bias across protected groups?",
                EthicsCategory.Fairness, Priority.Critical),
            new("FAIR-02", "Fairness Metrics",
                "Are fairness metrics defined and monitored?",
                EthicsCategory.Fairness, Priority.High),
            new("FAIR-03", "Training Data",
                "Is training data representative and free from historical bias?",
                EthicsCategory.Fairness, Priority.Critical),

            // Transparency
            new("TRANS-01", "Explainability",
                "Can the system explain its decisions to affected users?",
                EthicsCategory.Transparency, Priority.High),
            new("TRANS-02", "AI Disclosure",
                "Are users informed they are interacting with AI?",
                EthicsCategory.Transparency, Priority.Critical),
            new("TRANS-03", "Limitation Disclosure",
                "Are system limitations clearly communicated?",
                EthicsCategory.Transparency, Priority.High),

            // Human Control
            new("CTRL-01", "Human Oversight",
                "Is there meaningful human oversight of AI decisions?",
                EthicsCategory.HumanControl, Priority.Critical),
            new("CTRL-02", "Override Capability",
                "Can humans override AI decisions when needed?",
                EthicsCategory.HumanControl, Priority.High),
            new("CTRL-03", "Escalation Path",
                "Is there a clear escalation path for concerning outputs?",
                EthicsCategory.HumanControl, Priority.High),

            // Safety
            new("SAFE-01", "Harm Prevention",
                "Are there safeguards against harmful outputs?",
                EthicsCategory.Safety, Priority.Critical),
            new("SAFE-02", "Fail-Safe Design",
                "Does the system fail safely when errors occur?",
                EthicsCategory.Safety, Priority.High),
            new("SAFE-03", "Adversarial Testing",
                "Has the system been tested against adversarial inputs?",
                EthicsCategory.Safety, Priority.High),

            // Privacy
            new("PRIV-01", "Data Minimization",
                "Does the system collect only necessary data?",
                EthicsCategory.Privacy, Priority.High),
            new("PRIV-02", "Consent",
                "Is there informed consent for data use?",
                EthicsCategory.Privacy, Priority.Critical),
            new("PRIV-03", "Data Protection",
                "Is personal data adequately protected?",
                EthicsCategory.Privacy, Priority.Critical),

            // Accountability
            new("ACCT-01", "Responsibility",
                "Is there clear ownership for system outcomes?",
                EthicsCategory.Accountability, Priority.High),
            new("ACCT-02", "Audit Trail",
                "Are decisions logged for accountability?",
                EthicsCategory.Accountability, Priority.High),
            new("ACCT-03", "Redress Mechanism",
                "Is there a way for affected parties to seek redress?",
                EthicsCategory.Accountability, Priority.High)
        };
    }
}
```

### Algorithmic Impact Questions

| Question | Why It Matters |
|----------|----------------|
| Who benefits from this algorithm? | Ensure equitable benefit distribution |
| Who might be harmed? | Identify vulnerable populations |
| What happens when it's wrong? | Understand failure impact |
| Can it be gamed or manipulated? | Assess adversarial risks |
| Does it entrench existing inequalities? | Check for systemic bias |
| What feedback loops might emerge? | Predict unintended consequences |
| Is there meaningful human oversight? | Ensure accountability |
| Can decisions be explained? | Support transparency |
| Is consent meaningful and informed? | Respect autonomy |
| What are the long-term societal effects? | Consider systemic impact |

## Ethics Review Board

### Board Structure

```text
Ethics Review Board Composition:
├── Chair (Senior Leadership)
├── Ethics Officer (if applicable)
├── Technical Lead (understands the technology)
├── Legal Representative
├── Privacy Officer
├── Business Representative
├── External Ethicist (optional but recommended)
└── User/Community Representative (for significant decisions)
```

### Review Thresholds

| Trigger | Review Level | Timeline |
|---------|--------------|----------|
| New AI/ML system | Full board review | Before development |
| High-risk application | Full board review | Before deployment |
| Significant model update | Expedited review | Before release |
| Incident or complaint | Post-hoc review | Within 1 week |
| Annual review | Full board review | Annual |
| Employee concern | Expedited review | Within 2 weeks |

### Board Decision Framework

```csharp
public enum EthicsDecision
{
    Approved,                    // Proceed as designed
    ApprovedWithConditions,      // Proceed after specified changes
    RequiresRedesign,           // Fundamental changes needed
    Deferred,                   // Need more information
    Rejected,                   // Unacceptable ethical risk
    EscalateToExecutive         // Beyond board authority
}

public class EthicsReviewResult
{
    public required EthicsDecision Decision { get; init; }
    public required string Rationale { get; init; }
    public List<string> Conditions { get; init; } = new();
    public List<string> MonitoringRequirements { get; init; } = new();
    public DateTimeOffset? NextReviewDate { get; init; }
    public List<BoardMemberVote> Votes { get; init; } = new();
}
```

## Responsible Innovation Framework

### Stage-Gate Ethics Integration

```text
Stage 1: Ideation
├── Initial ethics screening
├── Identify potential concerns
└── Go/No-Go for research

Stage 2: Research & Design
├── Stakeholder analysis
├── Preliminary impact assessment
└── Ethics-by-design integration

Stage 3: Development
├── Ongoing ethics review
├── Testing for bias/harm
└── Documentation

Stage 4: Pre-Deployment
├── Full ethical impact assessment
├── Board review (if triggered)
└── Mitigation verification

Stage 5: Deployment
├── Monitoring plan activation
├── Feedback mechanisms
└── Incident response ready

Stage 6: Operations
├── Ongoing monitoring
├── Regular reviews
└── Continuous improvement
```

## Ethics Review Checklist

### Pre-Development

- [ ] Ethical impact assessment completed
- [ ] Stakeholder analysis documented
- [ ] Potential harms identified
- [ ] Ethics review board consulted (if required)
- [ ] Mitigation plans defined

### Development

- [ ] Ethics-by-design principles applied
- [ ] Bias testing conducted
- [ ] Explainability built in
- [ ] Human oversight designed
- [ ] Documentation complete

### Pre-Deployment

- [ ] Full assessment reviewed
- [ ] All mitigations implemented
- [ ] Monitoring in place
- [ ] Redress mechanism ready
- [ ] Ethics sign-off obtained

### Operations

- [ ] Regular monitoring active
- [ ] Feedback collected and reviewed
- [ ] Incidents investigated
- [ ] Periodic re-assessment scheduled

## Cross-References

- **AI Governance**: `ai-governance` for regulatory compliance
- **Bias Assessment**: See ai-ml-planning plugin for fairness metrics
- **Data Privacy**: `gdpr-compliance` for privacy considerations

## Resources

- [IEEE Ethically Aligned Design](https://ethicsinaction.ieee.org/)
- [ACM Code of Ethics](https://www.acm.org/code-of-ethics)
- [AI Ethics Guidelines Global Inventory](https://algorithmwatch.org/en/ai-ethics-guidelines-global-inventory/)
- [Markkula Center for Applied Ethics](https://www.scu.edu/ethics/)
