---
name: requirement-analyzer
description: Analyzes and documents requirements for any software project, technology-agnostic approach to requirement engineering
---

# Generic Requirement Analyzer

A technology-agnostic skill for analyzing, categorizing, and documenting software requirements for any type of project.

## Core Responsibilities

### 1. Requirement Decomposition

Break down requirements into universal categories:

```yaml
Requirement Categories:
  Functional:
    - What the system must do
    - User interactions
    - Business logic
    - Data processing

  Non-Functional:
    - Performance targets
    - Security requirements
    - Usability standards
    - Reliability metrics

  Constraints:
    - Technical limitations
    - Business rules
    - Regulatory compliance
    - Resource boundaries
```

### 2. Requirement Analysis Framework

**Universal User Story Format:**
```yaml
User Story:
  as_a: [user role/persona]
  i_want: [feature/capability]
  so_that: [business value/benefit]

Acceptance Criteria:
  given: [initial context/state]
  when: [action/trigger]
  then: [expected outcome/result]
```

**Requirement Specification Template:**
```yaml
Requirement:
  id: REQ-[number]
  title: [brief description]
  type: functional|non-functional|constraint
  priority: must|should|could|wont
  description: [detailed description]
  rationale: [why this is needed]
  source: [stakeholder/document]
  acceptance_criteria:
    - [measurable criterion 1]
    - [measurable criterion 2]
  dependencies:
    - [related requirement ids]
  risks:
    - [potential risks]
  assumptions:
    - [underlying assumptions]
```

### 3. Priority Frameworks

**MoSCoW Method:**
```yaml
Must Have:
  - Critical for launch
  - System fails without it
  - Legal/regulatory requirement

Should Have:
  - Important but not vital
  - Workaround exists
  - High value for users

Could Have:
  - Desirable but not necessary
  - Nice to have
  - Can be postponed

Won't Have (this time):
  - Out of scope
  - Future consideration
  - Explicitly excluded
```

**Kano Model:**
```yaml
Basic Needs:
  - Expected by users
  - Causes dissatisfaction if missing

Performance Needs:
  - More is better
  - Linear satisfaction

Excitement Needs:
  - Delighters
  - Unexpected features
  - Competitive advantage
```

### 4. Requirement Quality Criteria

**SMART Requirements:**
```yaml
Specific:
  - Clear and unambiguous
  - Well-defined scope

Measurable:
  - Quantifiable success criteria
  - Testable conditions

Achievable:
  - Technically feasible
  - Resource realistic

Relevant:
  - Aligns with business goals
  - Provides value

Time-bound:
  - Has deadline/milestone
  - Time constraints defined
```

**Completeness Checklist:**
```yaml
Requirement Completeness:
  - [ ] Clear description
  - [ ] Defined acceptance criteria
  - [ ] Identified stakeholder
  - [ ] Priority assigned
  - [ ] Dependencies mapped
  - [ ] Risks assessed
  - [ ] Assumptions documented
  - [ ] Traceability established
```

### 5. Stakeholder Analysis

**Stakeholder Mapping:**
```yaml
Stakeholder Analysis:
  identification:
    - End users
    - Business owners
    - Technical team
    - Regulatory bodies
    - External partners

  influence_interest_matrix:
    high_influence_high_interest:
      - Key players
      - Manage closely

    high_influence_low_interest:
      - Keep satisfied
      - Regular updates

    low_influence_high_interest:
      - Keep informed
      - Regular communication

    low_influence_low_interest:
      - Monitor
      - Minimal effort
```

### 6. Requirement Validation

**Validation Techniques:**
```yaml
Review Methods:
  walkthrough:
    - Informal review
    - Author-led
    - Educational focus

  inspection:
    - Formal review
    - Defined roles
    - Defect detection

  prototype_validation:
    - Visual representation
    - User feedback
    - Early validation
```

**Validation Criteria:**
```yaml
Quality Attributes:
  correctness:
    - Accurately represents need
    - Factually correct

  consistency:
    - No conflicts
    - Uniform terminology

  completeness:
    - All aspects covered
    - No gaps

  feasibility:
    - Technically possible
    - Resource available

  testability:
    - Verifiable criteria
    - Measurable outcomes
```

## Analysis Process

### Step 1: Requirement Gathering
```yaml
Sources:
  - Stakeholder interviews
  - Existing documentation
  - Market research
  - Competitive analysis
  - User feedback
  - Regulatory requirements
```

### Step 2: Categorization
```yaml
Classification:
  1. Parse raw requirements
  2. Identify requirement type
  3. Assign categories
  4. Group related items
  5. Identify patterns
```

### Step 3: Analysis
```yaml
Analysis Activities:
  1. Ambiguity resolution
  2. Conflict identification
  3. Gap analysis
  4. Dependency mapping
  5. Risk assessment
```

### Step 4: Documentation
```yaml
Documentation Outputs:
  - Requirement specification
  - Traceability matrix
  - Stakeholder matrix
  - Risk register
  - Assumption log
```

## Output Formats

### Requirement Specification Document
```markdown
# Requirement Specification

## Executive Summary
[High-level overview of requirements]

## Functional Requirements
### FR-001: [Title]
- **Description**: [Detail]
- **Priority**: Must Have
- **Acceptance Criteria**:
  1. [Criterion 1]
  2. [Criterion 2]

## Non-Functional Requirements
### NFR-001: [Title]
- **Category**: Performance
- **Metric**: Response time < 2 seconds
- **Validation**: Load testing

## Constraints
### CON-001: [Title]
- **Type**: Technical
- **Description**: [Limitation details]
- **Impact**: [How it affects design]

## Dependencies
[Requirement dependency diagram]

## Risks and Assumptions
### Risks
- [Risk 1]: [Mitigation strategy]

### Assumptions
- [Assumption 1]: [Validation plan]
```

### Traceability Matrix
```yaml
Traceability:
  REQ-001:
    source: "User Interview #3"
    design_element: "Component A"
    test_case: "TC-001, TC-002"
    implementation: "Module X"

  REQ-002:
    source: "Regulatory Doc Section 4.2"
    design_element: "Security Layer"
    test_case: "TC-010"
    implementation: "Auth Module"
```

## Integration Points

### With Project Configuration
```yaml
# Project-specific configuration
requirement_config:
  project_type: "web_application|mobile_app|api|system"

  priority_framework: "moscow|kano|numerical"

  requirement_categories:
    - functional
    - non-functional
    - business
    - technical

  validation_requirements:
    review_type: "formal|informal"
    approval_levels: 2

  compliance_standards:
    - "ISO 27001"
    - "GDPR"
```

### With Technology-Specific Skills
```yaml
# Technology-specific extensions
tech_specific:
  framework: "[Framework name]"

  requirement_patterns:
    - "[Framework-specific pattern]"

  validation_rules:
    - "[Technology-specific rule]"
```

## Best Practices

1. **Stakeholder Engagement**: Involve all stakeholders early
2. **Clear Communication**: Use unambiguous language
3. **Measurable Criteria**: Define quantifiable success metrics
4. **Iterative Refinement**: Requirements evolve, plan for changes
5. **Traceability**: Maintain links from requirements to implementation
6. **Risk-Based Focus**: Prioritize based on risk and value
7. **Documentation**: Keep requirements current and accessible

## Universal Application

This skill can be applied to:
- Web applications
- Mobile applications
- Desktop software
- Embedded systems
- APIs and services
- Cloud platforms
- IoT solutions
- Enterprise systems
- Machine learning projects
- Any software development project

The skill adapts to project needs through configuration rather than modification, ensuring reusability across different technology stacks and domains.