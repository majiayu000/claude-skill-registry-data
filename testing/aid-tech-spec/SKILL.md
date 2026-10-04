---
name: aid-tech-spec
description: AID Phase 2 - Technical Specification. Use for system architecture, API contracts, data models, security architecture, transitioning from PRD to implementation.
---

# Tech Spec Phase Skill

Purpose: design the technical solution - a blueprint developers follow without ambiguity.

Entry: PRD approved, requirements clear, dependencies identified.
Exit: tech spec complete, architecture documented, API contracts defined, data models specified.

## Deliverables

1. Tech Spec Document - Implementation-ready design
2. Architecture Diagram - Components and interactions
3. API Contracts - Endpoints, schemas, errors
4. Data Models - Schemas, types, constraints

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Over-engineering | Design for current needs |
| Missing error handling | Define errors upfront |
| Tight coupling | Design for testability |
| Ignoring non-functionals | Address performance, security |
| Unclear contracts | APIs unambiguous with examples |

## Phase Gate Checklist

- [ ] Tech spec complete
- [ ] Architecture diagram created
- [ ] All API contracts defined
- [ ] Data models specified
- [ ] Error handling strategy defined
- [ ] Security considerations addressed
- [ ] Performance requirements addressed
- [ ] Tech lead approved

## Tech Spec Template

Emit these 8 sections, in this order, with these exact headings:

````markdown
# [Feature] Technical Specification

## 1. Overview
### Problem Summary
### Proposed Solution
### Key Decisions
| Decision | Choice | Rationale |

## 2. Architecture
### System Diagram
[Mermaid or image]

### Component Breakdown
| Component | Responsibility | Dependencies |

### Data Flow

## 3. API Design
### POST /api/[resource]
**Request:**
```json
{ "field": "type" }
```

**Response (200):**
```json
{ "id": "string" }
```

**Errors:**
| Code | Error | Description |

## 4. Data Model
### Entity: [Name]
| Field | Type | Constraints | Description |

## 5. Security
### Authentication
### Authorization
### Data Protection

## 6. Error Handling
| Scenario | Response | Recovery |

## 7. Non-Functional Requirements
| Requirement | Target | Measurement |

## 8. Risks & Mitigations
| Risk | Impact | Mitigation |
````

## Role Guidance

| Role | Focus |
|---|---|
| PM | Validate approach addresses requirements |
| Dev | Own spec, design for testability |
| QA | Review testability, integration points |
| Tech Lead | Review architecture, approve direction |

## Handoff to Implementation

- Approved tech spec
- API contracts
- Data models
- Architecture decisions with rationale
- Spike/POC results (if any)

Save to: `docs/tech-spec/YYYY-MM-DD-[feature].md`
