---
name: ontology-phase-3-synthesize
description: |
  Phase 3 of Ontology Builder Pipeline. Synthesizes analysis results into 
  complete Domain Requirement Document (DRD). Use after Phase 2 analysis 
  is complete to generate structured DRD.
---

# Phase 3: Synthesize DRD

Transform analysis results into a complete, well-structured Domain Requirement Document.

## Trigger

Execute when:
- Phase 2 analysis-report.md is available
- DRD regeneration requested

## Process

### Step 1: Load Analysis Results

Read:
1. `_output/_logs/analysis-report.md`
2. `_input/project-context.md` (for header info)

### Step 2: Generate DRD Structure

Create: `_output/00-drd/DRD-[module].md`

Follow the template below exactly.

### Step 3: Write Each Section

#### Section 1: Context
- Copy from project-context.md
- Add scope from analysis

#### Section 2: Domain Concepts
- Transform consolidated entities into concept descriptions
- Write in natural language, not YAML
- Include "key characteristics" for each
- Mark confidence inline

#### Section 3: Business Rules
- Organize rules by category
- Use consistent ID format
- Include conditions and actions

#### Section 4: Workflows
- Write full workflow descriptions
- Include main flow and alternates
- Reference entities by name

#### Section 5: Data Examples
- Generate realistic examples
- Show different scenarios
- Use YAML format for clarity

#### Section 6: Integration Points
- List external system integrations
- Specify data direction and purpose

### Step 4: Add Metadata

- Confidence markers throughout
- Source attributions
- Assumptions section
- Open questions section

### Step 5: Self-Review

Before finalizing:
- [ ] All analysis entities covered?
- [ ] All workflows included?
- [ ] Business rules linked to entities/workflows?
- [ ] Examples are realistic?
- [ ] No TODO placeholders?

## DRD Template

```markdown
# Domain Requirement Document: [Module Name]

**Module**: [MODULE-CODE]  
**Version**: 1.0  
**Generated**: [timestamp]  
**Generator**: AI Ontology Builder Pipeline  
**Status**: Draft - Pending Review

---

## Document Information

| Field | Value |
|-------|-------|
| Project | [Project name] |
| Domain | [Domain type] |
| Region | [Region/Country] |
| Confidence Level | [Overall: HIGH/MEDIUM/LOW] |
| Assumptions Made | [Count] |
| Open Questions | [Count] |

---

## 1. Context

### 1.1 Business Background

[2-3 paragraphs describing business context, synthesized from inputs]

[CONFIDENCE: HIGH/MEDIUM/LOW] (Source: [sources])

### 1.2 Scope

**In Scope**:
- [Feature 1] [CONFIDENCE]
- [Feature 2] [CONFIDENCE]
- [Feature 3] [CONFIDENCE]

**Out of Scope**:
- [Item 1] → [Reason/Where handled]
- [Item 2] → [Reason]

### 1.3 Users & Roles

| Role | Description | Key Actions | Source |
|------|-------------|-------------|--------|
| [Role 1] | [Desc] | [Actions] | [Source] |
| [Role 2] | [Desc] | [Actions] | [Source] |

---

## 2. Domain Concepts

> These concepts form the foundation of the [Module] domain model.

### 2.1 Core Concepts

#### [Concept Name 1] [CONFIDENCE]

[2-3 sentence description in natural language]

**Key Characteristics**:
- [Characteristic 1]
- [Characteristic 2]
- [Characteristic 3]

**Attributes** (for reference):
- `[attribute_1]`: [type] - [description]
- `[attribute_2]`: [type] - [description]

**Related To**: [Entity1], [Entity2]

(Source: [source files] | [If ASSUMED: "Market knowledge: [reference]"])

---

#### [Concept Name 2] [CONFIDENCE]

[Description]

**Key Characteristics**:
- [Characteristic 1]
- [Characteristic 2]

...

### 2.2 Supporting Concepts

#### [Supporting Concept 1] [CONFIDENCE]

[Description]

---

## 3. Business Rules

### 3.1 [Category] Rules

| ID | Rule | Condition | Action | Source |
|----|------|-----------|--------|--------|
| BR-[MOD]-001 | [Short name] | [When condition] | [Then action] | [Source] |
| BR-[MOD]-002 | [Short name] | [When condition] | [Then action] | [Source] |

### 3.2 [Category] Rules

| ID | Rule | Condition | Action | Source |
|----|------|-----------|--------|--------|
| BR-[MOD]-010 | [Short name] | [When condition] | [Then action] | [Source] |

### 3.3 Assumed Rules (Market Standard)

> These rules are assumed based on industry standards and market knowledge.

| ID | Rule | Condition | Action | Reference |
|----|------|-----------|--------|-----------|
| BR-[MOD]-A01 | [Short name] | [When condition] | [Then action] | [Market reference] |

---

## 4. Workflows

### 4.1 WF-[MOD]-001: [Workflow Name] [CONFIDENCE]

**Classification**: [CORE | SUPPORT | INTEGRATION]  
**Trigger**: [What initiates this workflow]  
**Actors**: [Actor 1], [Actor 2], [System]  
**Result**: [What is achieved when workflow completes]

**Main Flow**:

1. [Actor] [action description]
2. System [validation/processing description]
3. [Actor] [next action]
4. System [updates/notifications]
5. [Continue as needed...]

**Alternate Flows**:

- **[Step]a. [Condition]**: [What happens instead]
- **[Step]b. [Condition]**: [What happens instead]

**Exception Handling**:

| Exception | Trigger | System Response |
|-----------|---------|-----------------|
| [Exception 1] | [Condition] | [Response] |
| [Exception 2] | [Condition] | [Response] |

**Business Rules Applied**: BR-[MOD]-001, BR-[MOD]-002

**Related Entities**: [Entity1], [Entity2]

(Source: [sources])

---

### 4.2 WF-[MOD]-002: [Workflow Name] [CONFIDENCE]

[Same structure as above]

---

## 5. Data Examples

### 5.1 [Concept] Examples

```yaml
Example 1: [Scenario name]
  [concept_name]:
    [attribute_1]: [value]
    [attribute_2]: [value]
    [attribute_3]: [value]

Example 2: [Different scenario]
  [concept_name]:
    [attribute_1]: [different value]
    [attribute_2]: [different value]
```

### 5.2 [Workflow] Scenario

```yaml
Scenario: [Scenario description]

Initial State:
  [entity]: 
    [attr]: [value]
    status: [initial status]

Action: [What happens]

Final State:
  [entity]:
    [attr]: [new value]
    status: [final status]

Side Effects:
  - [Side effect 1]
  - [Side effect 2]
```

---

## 6. Integration Points

| System | Direction | Data | Purpose | Priority |
|--------|-----------|------|---------|----------|
| [System 1] | Inbound | [Data type] | [Purpose] | [HIGH/MED/LOW] |
| [System 2] | Outbound | [Data type] | [Purpose] | [Priority] |
| [System 3] | Bidirectional | [Data type] | [Purpose] | [Priority] |

---

## 7. Non-Functional Requirements

### 7.1 Performance
- [Requirement 1]
- [Requirement 2]

### 7.2 Security
- [Requirement 1]
- [Requirement 2]

### 7.3 Audit
- [Requirement 1]

---

## 8. Assumptions

> These assumptions were made during analysis. Please validate.

| # | Assumption | Rationale | Impact if Wrong |
|---|------------|-----------|-----------------|
| A1 | [Assumption] | [Why assumed] | [Impact] |
| A2 | [Assumption] | [Why assumed] | [Impact] |
| A3 | [Assumption] | [Why assumed] | [Impact] |

---

## 9. Open Questions

> These questions need stakeholder input for complete accuracy.

| # | Question | Context | Default if No Answer |
|---|----------|---------|---------------------|
| Q1 | [Question] | [Why important] | [What we'll assume] |
| Q2 | [Question] | [Why important] | [What we'll assume] |

---

## 10. Confidence Summary

### By Section

| Section | Confidence | Notes |
|---------|------------|-------|
| Context | [HIGH/MED/LOW] | [Notes] |
| Domain Concepts | [%H/%M/%L] | [Notes] |
| Business Rules | [%H/%M/%L] | [Notes] |
| Workflows | [%H/%M/%L] | [Notes] |

### By Source

| Source Type | Items | Confidence |
|-------------|-------|------------|
| User Stories | [N] | HIGH |
| Interviews | [N] | HIGH |
| Existing Docs | [N] | MEDIUM |
| Market Knowledge | [N] | ASSUMED |

---

## 11. References

### Input Sources
- [List all input files used]

### Market References
- [List industry standards/systems referenced]

---

## Next Steps

1. [ ] Review assumptions (Section 8)
2. [ ] Answer open questions (Section 9)
3. [ ] Validate business rules (Section 3)
4. [ ] Approve for Ontology generation

---

**Document History**

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | [date] | Initial generation by AI Pipeline |
```

## Output

- `_output/00-drd/DRD-[module].md`
- `_output/_logs/gate-3-manifest.yaml` (verification manifest)
- Ready for Phase 4: Generate Ontology

## Gate 3: Self-Verification

Before completing Phase 3, generate verification manifest:

```yaml
# _output/_logs/gate-3-manifest.yaml
gate: 3
name: "Post-DRD Verification"
timestamp: "[ISO timestamp]"

structural_checks:
  - check: "DRD document exists"
    status: PASS
  - check: "All required sections present"
    status: PASS | FAIL
    sections:
      context: true | false
      domain_concepts: true | false
      business_rules: true | false
      workflows: true | false
      examples: true | false
      assumptions: true | false
  - check: "No TODO/TBD placeholders"
    status: PASS | FAIL
    placeholders_found: []

consistency_checks:
  - check: "All analysis entities in DRD"
    status: PASS | FAIL
    analysis_count: [N]
    drd_count: [N]
    missing: []
  - check: "All analysis workflows in DRD"
    status: PASS | FAIL
    missing: []
  - check: "Business rule IDs unique"
    status: PASS | FAIL
    duplicates: []
  - check: "Workflow IDs unique"
    status: PASS | FAIL
    duplicates: []

traceability_checks:
  - check: "Concepts trace to analysis"
    status: PASS | FAIL
  - check: "Confidence markers present"
    status: PASS | FAIL
    sections_without_confidence: []

quality_checks:
  - check: "Business rules have condition and action"
    status: PASS | FAIL
    vague_rules: []
  - check: "Workflows have complete main flow"
    status: PASS | FAIL
    incomplete_workflows: []
  - check: "Examples are realistic"
    status: PASS | FAIL

result:
  status: PASS | FAIL | WARN
  blocking_failures: []
  warnings: []
  proceed_to_next_phase: true | false
```

**Verification Rules**:
- FAIL if missing required sections
- FAIL if TODO/TBD placeholders remain
- WARN if any analysis entity missing from DRD

## Quality Checklist

Before proceeding to Phase 4:
- [ ] All consolidated entities from analysis appear in Section 2
- [ ] All workflows from analysis appear in Section 4
- [ ] All business rules have IDs and are linked
- [ ] Examples are realistic and consistent
- [ ] Assumptions clearly documented
- [ ] Confidence markers throughout

## Next Phase

After completing DRD:
→ Load `phase-4-generate/SKILL.md`
→ Pass DRD as input
