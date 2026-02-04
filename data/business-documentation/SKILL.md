---
name: business-documentation
description: Master business documentation including BRD, FRD, specifications, and technical documentation for clear communication and requirements management.
---

# Business Documentation

Create comprehensive business documentation including BRDs, FRDs, and specifications that clearly communicate requirements and enable successful project delivery.

## When to Use This Skill

- Documenting project requirements
- Creating specifications
- Communicating with stakeholders
- Supporting development teams
- Facilitating testing
- Ensuring traceability
- Obtaining approvals
- Providing reference materials

## Core Documents

### 1. Business Requirements Document (BRD)

**Structure:**
```markdown
## 1. Executive Summary
- Project overview
- Business objectives
- Expected benefits

## 2. Business Context
- Current situation
- Problems/opportunities
- Strategic alignment

## 3. Scope
- In scope
- Out of scope
- Assumptions
- Constraints

## 4. Business Requirements
- Functional requirements (high-level)
- Non-functional requirements
- Business rules
- Compliance requirements

## 5. Stakeholders
- Key stakeholders
- Roles and responsibilities
- Communication plan

## 6. Success Criteria
- Metrics and KPIs
- Acceptance criteria
- Definition of done

## 7. Risks and Dependencies
- Key risks
- Mitigation strategies
- Dependencies

## 8. Timeline and Budget
- High-level schedule
- Budget estimate
- Resource requirements
```

### 2. Functional Requirements Document (FRD)

**Structure:**
```markdown
## 1. Introduction
- Purpose
- Scope
- Definitions

## 2. System Overview
- Architecture diagram
- System components
- Integration points

## 3. Functional Requirements
**FR-001: User Authentication**
- **Description:** System shall authenticate users
- **Priority:** High
- **Inputs:** Username, password
- **Processing:** Validate credentials, create session
- **Outputs:** Authentication token, user profile
- **Business Rules:** BR-001, BR-002
- **Acceptance Criteria:**
  - Valid credentials grant access
  - Invalid credentials show error
  - Account locks after 3 failed attempts

## 4. Non-Functional Requirements
**NFR-001: Performance**
- Response time < 2 seconds
- Support 1000 concurrent users

## 5. Data Requirements
- Data models
- Data dictionary
- Data validation rules

## 6. Interface Requirements
- User interfaces
- API specifications
- Integration interfaces

## 7. Appendices
- Glossary
- References
- Traceability matrix
```

## Best Practices

1. **Clear structure** - Organized, easy to navigate
2. **Consistent format** - Templates and standards
3. **Plain language** - Avoid jargon, be precise
4. **Visual aids** - Diagrams, tables, examples
5. **Unique IDs** - Requirements traceability
6. **Version control** - Track changes
7. **Stakeholder review** - Validate accuracy
8. **Living document** - Update as needed

## Resources

- **BABOK Guide**: Documentation standards
- **IEEE 830**: Software requirements specification
