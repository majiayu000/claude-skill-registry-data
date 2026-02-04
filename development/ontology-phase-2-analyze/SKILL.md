---
name: ontology-phase-2-analyze
description: |
  Phase 2 of Ontology Builder Pipeline. AI acts as domain SME to analyze raw inputs,
  extract entities/workflows/rules, fill knowledge gaps using market expertise.
  Use after Phase 1 ingestion is complete.
---

# Phase 2: Analyze as SME

Act as domain Subject Matter Expert to analyze inputs and extract structured knowledge.

## Trigger

Execute when:
- Phase 1 ingestion-report.md is available
- Analysis refresh requested

## SME Mindset

You are a **Senior Business Analyst + Domain Expert**. Your expertise adapts to the domain specified in `project-context.md`.

Your job: Transform raw, messy inputs into clean, structured domain knowledge.

## Domain Expertise Activation

### Step 0: Identify and Immerse in Domain

1. **Read `project-context.md`** to identify:
   - Domain type (HR, Finance, Sales, Operations, Healthcare, etc.)
   - Industry vertical (if specified)
   - Region (for regulatory context)
   - Reference systems mentioned

2. **Activate SME Mode** for the identified domain:
   
   ```
   I am now acting as a Senior SME in [DOMAIN] with:
   - 10+ years hands-on experience
   - Deep knowledge of industry-leading systems
   - Understanding of best practices and standards
   - Familiarity with regional regulations
   ```

3. **If domain is unfamiliar or specialized**:
   - Use web search to research current industry standards
   - Look up major enterprise systems in that domain
   - Research regional compliance requirements
   - Find common entity patterns and workflows

### SME Knowledge Areas (Dynamic)

For ANY domain, you should be able to reason about:

| Area | What to Consider |
|------|------------------|
| **Standard Entities** | What objects typically exist in this domain? |
| **Common Workflows** | What are the standard business processes? |
| **Industry Systems** | What software systems are leaders in this space? |
| **Regulatory** | What compliance requirements apply (by region)? |
| **Best Practices** | What patterns are considered best practice? |
| **Anti-Patterns** | What mistakes should be avoided? |

### Example Domain Activation

```yaml
# If project-context says: Domain = HR, Region = Vietnam

SME Activation:
  domain: "Human Capital Management (HCM)"
  reference_systems: 
    - "Workday HCM"
    - "SAP SuccessFactors" 
    - "Oracle HCM Cloud"
  standards: 
    - "SHRM guidelines"
    - "ISO 30414 (HR metrics)"
  regulations:
    - "Vietnam Labor Code 2019"
    - "Social Insurance Law"
    - "Decree 145/2020 on labor contracts"
  key_patterns:
    - "Position-based vs Job-based staffing"
    - "Accrual-based leave management"
    - "Multi-level approval workflows"
```

```yaml
# If project-context says: Domain = Finance, Region = Vietnam

SME Activation:
  domain: "Financial Management"
  reference_systems:
    - "SAP S/4HANA FI/CO"
    - "Oracle Financials Cloud"
    - "MISA (Vietnam local)"
  standards:
    - "Vietnam Accounting Standards (VAS)"
    - "Circular 200/2014"
    - "IFRS alignment"
  regulations:
    - "E-invoice (Decree 123/2020)"
    - "VAT regulations"
    - "Transfer pricing rules"
  key_patterns:
    - "Procure-to-Pay (P2P)"
    - "Order-to-Cash (O2C)"
    - "Month-end close process"
```

### When to Use Web Search

Use web search when you need to:
- Verify current regulations or standards
- Research unfamiliar domain terminology
- Find latest best practices
- Understand specific regional requirements
- Research competitor/reference systems

**Search Strategy**:
```
1. "[Domain] enterprise software best practices"
2. "[Domain] [Region] compliance requirements 2024"
3. "[Reference System] [Entity] data model"
4. "[Industry] standard workflows"
```

## Process

### Step 1: Load Context

Read:
1. `_output/_logs/ingestion-report.md`
2. `_input/project-context.md`
3. `_input/domain-hints.md` (if exists)

Establish:
- Domain type (HR, Finance, Sales, etc.)
- Regional context (for regulations)
- Existing system landscape
- Key constraints

### Step 2: Deep Read All Sources

For each file in ingestion report, perform deep analysis:

```yaml
analysis_per_file:
  file: [path]
  
  entities_extracted:
    - name: [EntityName]
      evidence: "[quote from source]"
      confidence: [HIGH|MEDIUM|LOW]
      attributes_mentioned: [list]
      
  workflows_extracted:
    - name: [WorkflowName]
      evidence: "[quote from source]"
      confidence: [HIGH|MEDIUM|LOW]
      actors_mentioned: [list]
      steps_mentioned: [list]
      
  rules_extracted:
    - description: [rule description]
      evidence: "[quote from source]"
      confidence: [HIGH|MEDIUM|LOW]
      applies_to: [entity or workflow]
      
  questions_raised:
    - question: [what's unclear]
      context: [why it matters]
```

### Step 3: Consolidate Findings

Merge extractions from all files:

#### 3.1 Entity Consolidation

For each potential entity:
1. Merge mentions from different sources
2. Resolve naming conflicts (use most common or clearest name)
3. Combine attributes from all sources
4. Assign confidence score

```yaml
consolidated_entity:
  name: [EntityName]
  aliases: [other names used in sources]
  sources: [list of files mentioning this]
  confidence: [HIGH|MEDIUM|LOW]
  classification: [CORE|VALUE_OBJECT|REFERENCE|TRANSACTION]
  description: [synthesized from sources]
  attributes:
    - name: [attr]
      type: [inferred type]
      source: [which file mentioned it]
  relationships:
    - target: [OtherEntity]
      type: [relationship type]
      evidence: [quote]
```

#### 3.2 Workflow Consolidation

For each potential workflow:
1. Merge related actions into coherent workflows
2. Identify actors and triggers
3. Map to related entities
4. Assign confidence score

#### 3.3 Business Rule Consolidation

For each rule:
1. Link to entity or workflow
2. Determine rule type (validation, constraint, calculation)
3. Assign ID and confidence

### Step 4: Gap Analysis

Identify what's missing based on domain expertise:

#### 4.1 Entity Gaps

As SME, I expect these entities in [domain] but don't see them:
- [Expected entity 1] - [why expected]
- [Expected entity 2] - [why expected]

#### 4.2 Workflow Gaps

Standard workflows I expect but aren't documented:
- [Expected workflow 1] - [why expected]
- [Expected workflow 2] - [why expected]

#### 4.3 Attribute Gaps

Common attributes missing from entities:
- [Entity] missing [attribute] - standard in [reference system]

#### 4.4 Rule Gaps

Standard business rules not mentioned:
- [Rule description] - common in [domain]

### Step 5: Fill Gaps with Domain Expertise

For each gap identified, apply your SME expertise:

```yaml
gap_resolution:
  gap: [what's missing]
  resolution: [how I'm filling it]
  reasoning: "As SME in [domain], this is standard because [reason]"
  reference: "[Industry system] pattern" or "[Standard/Regulation]"
  confidence: ASSUMED
  assumption: [explicit assumption being made]
  needs_validation: [true|false]
```

#### SME Gap-Filling Strategies

**Strategy 1: Industry Pattern Recognition**
```
"In [domain], the standard approach for [problem] is [solution].
This is how [Reference System 1] and [Reference System 2] handle it."
```

**Strategy 2: Regulatory Inference**
```
"Based on [Region] [Regulation], this entity must include [attribute]
to comply with [requirement]."
```

**Strategy 3: Best Practice Application**
```
"Industry best practice for [scenario] is [pattern].
This avoids common issues like [anti-pattern]."
```

**Strategy 4: Web Research (when needed)**
```
If unfamiliar with domain-specific pattern:
1. Search for "[domain] [entity/workflow] best practices"
2. Search for "[reference system] [feature] documentation"
3. Synthesize findings into gap resolution
```

#### Gap-Filling Examples

**Example 1: Missing Entity Attributes**
```yaml
gap: "LeaveRequest entity missing approval tracking"
resolution: "Add approver_id, approved_at, approval_comments"
reasoning: "Standard workflow pattern - all approval-based entities 
           need to track who approved, when, and why"
reference: "Workday Absence Management pattern"
```

**Example 2: Missing Business Rule**
```yaml
gap: "No rule for leave balance validation"
resolution: "Add rule: Available balance >= Requested days"
reasoning: "Fundamental constraint in all leave management systems
           to prevent negative balances"
reference: "Universal pattern across SAP, Workday, Oracle"
```

**Example 3: Missing Workflow Step**
```yaml
gap: "Approval workflow missing escalation"
resolution: "Add auto-escalation after [configurable] days"
reasoning: "Prevents requests from being stuck indefinitely.
           Standard in enterprise approval workflows."
reference: "ServiceNow, Workday approval patterns"
```

**Example 4: Regional Compliance**
```yaml
gap: "Missing mandatory fields for Vietnam labor compliance"
resolution: "Add social_insurance_number, tax_code to Employee"
reasoning: "Required by Vietnam Labor Code for employment records"
reference: "Vietnam Labor Code 2019, Decree 145/2020"
# If uncertain, verify with web search
```

### Step 6: Resolve Conflicts

When sources conflict:

1. **Date conflict**: Use most recent source
2. **Stakeholder conflict**: Flag for human review
3. **Detail conflict**: Use most detailed version
4. **Terminology conflict**: Create alias mapping

### Step 7: Ask Clarifying Questions (If Needed)

If critical information is genuinely missing and cannot be assumed:

```markdown
## Questions for Stakeholder

Before proceeding, please clarify:

1. **[Question]**
   - Context: [why this matters]
   - My assumption if no answer: [what I'll assume]

2. **[Question]**
   - Context: [why this matters]
   - My assumption if no answer: [what I'll assume]
```

**Important**: Only ask questions that are:
- Critical for correctness
- Cannot be reasonably assumed
- Would significantly change the output

Prefer making documented assumptions over blocking progress.

### Step 8: Generate Analysis Report

Output: `_output/_logs/analysis-report.md`

```markdown
# Analysis Report

**Generated**: [timestamp]
**Analyst**: AI SME Agent
**Domain Expertise Applied**: [domain type]

## Executive Summary

- **Entities identified**: [N] ([confidence breakdown])
- **Workflows identified**: [N] ([confidence breakdown])
- **Business rules identified**: [N]
- **Gaps filled with market knowledge**: [N]
- **Assumptions made**: [N]

## Consolidated Entities

### [EntityName] [CONFIDENCE]

**Classification**: [type]
**Sources**: [list]
**Description**: [description]

**Attributes**:
| Attribute | Type | Required | Source |
|-----------|------|----------|--------|
| [attr] | [type] | [Y/N] | [source] |

**Relationships**:
| Target | Cardinality | Description |
|--------|-------------|-------------|
| [entity] | [card] | [desc] |

**Business Rules**:
- BR-XXX: [rule]

---

[Repeat for each entity]

## Consolidated Workflows

### [WorkflowName] [CONFIDENCE]

**Classification**: [CORE|SUPPORT|INTEGRATION]
**Trigger**: [trigger]
**Actors**: [list]
**Related Entities**: [list]

**High-Level Steps**:
1. [step]
2. [step]
3. [step]

**Business Rules Applied**: [list]

---

[Repeat for each workflow]

## Business Rules Catalog

| ID | Description | Applies To | Source | Confidence |
|----|-------------|------------|--------|------------|
| BR-001 | [desc] | [entity/workflow] | [source] | [conf] |

## Gap Analysis

### Gaps Filled with Market Knowledge

| Gap | Resolution | Source | Assumption |
|-----|------------|--------|------------|
| [gap] | [resolution] | [market ref] | [assumption] |

### Remaining Gaps (Need Human Input)

| Gap | Impact | Suggested Resolution |
|-----|--------|---------------------|
| [gap] | [impact] | [suggestion] |

## Assumptions Made

| # | Assumption | Rationale | Risk if Wrong |
|---|------------|-----------|---------------|
| 1 | [assumption] | [rationale] | [risk] |

## Questions for Stakeholder (Optional)

[Only if critical questions exist]

## Confidence Summary

| Category | HIGH | MEDIUM | LOW | ASSUMED |
|----------|------|--------|-----|---------|
| Entities | [N] | [N] | [N] | [N] |
| Workflows | [N] | [N] | [N] | [N] |
| Rules | [N] | [N] | [N] | [N] |

## Ready for Phase 3

Analysis complete. Proceed to DRD synthesis.
```

## Output

- `_output/_logs/analysis-report.md`
- `_output/_logs/gate-2-manifest.yaml` (verification manifest)
- Ready for Phase 3: Synthesize

## Gate 2: Self-Verification

Before completing Phase 2, generate verification manifest:

```yaml
# _output/_logs/gate-2-manifest.yaml
gate: 2
name: "Post-Analysis Verification"
timestamp: "[ISO timestamp]"

structural_checks:
  - check: "analysis-report.md exists"
    status: PASS
  - check: "Entities section present"
    status: PASS | FAIL
    entity_count: [N]
  - check: "Workflows section present"
    status: PASS | FAIL
    workflow_count: [N]
  - check: "Business rules section present"
    status: PASS | FAIL
    rule_count: [N]

consistency_checks:
  - check: "All entities have classification"
    status: PASS | FAIL
    unclassified: []
  - check: "All entities have confidence level"
    status: PASS | FAIL
  - check: "Confidence values valid"
    status: PASS | FAIL
    invalid_values: []

traceability_checks:
  - check: "Every entity has source reference"
    status: PASS | FAIL
    entities_without_source: []
  - check: "Every workflow has source reference"
    status: PASS | FAIL
    workflows_without_source: []
  - check: "Assumed items documented in assumptions section"
    status: PASS | FAIL
    undocumented_assumptions: []

coverage_metrics:
  input_files_processed: "[N]/[Total]"
  entities_from_input: [N]
  entities_assumed: [N]
  assumption_ratio: "[%]"

result:
  status: PASS | FAIL | WARN
  blocking_failures: []
  warnings: []
  proceed_to_next_phase: true | false
```

**Verification Rules**:
- FAIL if any entity has no source AND is not marked ASSUMED
- WARN if assumption_ratio > 30%
- Only proceed if `status: PASS` or `status: WARN`

## Key Behaviors

### DO:
- Make reasonable assumptions based on domain expertise
- Document every assumption explicitly
- Use market knowledge to fill gaps
- Prefer progress over perfection
- Be specific about confidence levels

### DON'T:
- Block on minor missing details
- Invent arbitrary numbers without flagging
- Ignore conflicting information
- Make assumptions without documenting them

## Next Phase

After completing analysis:
→ Load `phase-3-synthesize/SKILL.md`
→ Pass analysis-report.md as input
