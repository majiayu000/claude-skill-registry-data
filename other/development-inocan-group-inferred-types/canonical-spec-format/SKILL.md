---
name: canonical-spec-format
description: Canonical specification format reference. Use when understanding the canonical spec schema, field requirements, provider-agnostic specification structure, or validating specifications against the schema.
allowed-tools: Read, Glob, Grep
---

# Canonical Specification Format

Reference guide for the canonical specification format - the provider-agnostic intermediate representation defined in ADR-115.

## When to Use This Skill

**Keywords:** canonical specification, canonical spec, spec schema, specification format, provider-agnostic, spec fields, spec validation, spec structure, YAML specification, JSON schema

**Use this skill when:**

- Understanding canonical specification structure
- Validating specifications against schema
- Creating specifications manually
- Mapping between providers and canonical format
- Debugging specification transformation issues

## Quick Reference

### Minimal Valid Specification

```yaml
id: "SPEC-001"
title: "Feature Title"
type: feature

context:
  problem: "Problem description (min 20 chars)"
  motivation: "Business value"

requirements:
  - id: "REQ-001"
    text: "The system SHALL do something"
    priority: must
    ears_type: ubiquitous
    acceptance_criteria:
      - id: "AC-001"
        given: "precondition"
        when: "action"
        then: "outcome"

metadata:
  status: draft
  created: "2025-12-24"
  provider: canonical
```

### Required Fields

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Format: SPEC-{number} |
| `title` | string | Human-readable title |
| `type` | enum | feature, bug, chore, spike, tech-debt |
| `context.problem` | string | Min 20 characters |
| `context.motivation` | string | Business value |
| `requirements` | array | At least one requirement |
| `metadata.status` | enum | draft, review, approved, implemented, deprecated |
| `metadata.created` | string | ISO 8601 date |
| `metadata.provider` | string | Provider that created this spec |

## Field Reference

### Root Level

```yaml
id: "SPEC-001"           # Required: Unique identifier
title: "Feature Title"    # Required: Human-readable name
type: feature             # Required: Specification type
```

**Type Values:**

| Type | Description |
| --- | --- |
| `feature` | New functionality or capability |
| `bug` | Defect fix |
| `chore` | Maintenance task |
| `spike` | Research or investigation |
| `tech-debt` | Technical debt reduction |

### Context Section

```yaml
context:
  problem: |                    # Required: min 20 chars
    Clear description of the problem.
    What pain point does this address?
  motivation: |                 # Required
    Business value or user benefit.
    Why should we invest in this?
  background: |                 # Optional
    Additional context, history, constraints
```

### Requirements Section

```yaml
requirements:
  - id: "REQ-001"               # Required: Unique within spec
    text: "EARS requirement"    # Required: EARS-formatted
    priority: must              # Required: must/should/could/wont
    ears_type: event-driven     # Required: EARS pattern type
    acceptance_criteria:        # Required: at least one
      - id: "AC-001"
        given: "precondition"
        when: "action"
        then: "outcome"
        and:                    # Optional: additional conditions
          - "additional condition"
    notes: "Optional notes"     # Optional
```

**Priority Values (MoSCoW):**

| Priority | Description |
| --- | --- |
| `must` | Non-negotiable, system fails without it |
| `should` | Important but not critical |
| `could` | Desirable if resources permit |
| `wont` | Explicitly excluded from scope |

**EARS Type Values:**

| Type | Pattern | Example |
| --- | --- | --- |
| `ubiquitous` | The system SHALL... | "The system SHALL encrypt data" |
| `state-driven` | WHILE..., the system SHALL... | "WHILE active, the system SHALL..." |
| `event-driven` | WHEN..., the system SHALL... | "WHEN clicked, the system SHALL..." |
| `unwanted` | IF..., THEN the system SHALL... | "IF error, THEN the system SHALL..." |
| `complex` | Combinations | "WHILE active, WHEN clicked..." |
| `optional` | WHERE..., the system SHALL... | "WHERE enabled, the system SHALL..." |

### Design Section (Optional)

```yaml
design:
  approach: |                   # Optional: implementation approach
    High-level description of how to implement
  components:                   # Optional: affected components
    - "Component 1"
    - "Component 2"
  dependencies:                 # Optional: prerequisites
    - "External dependency"
  alternatives:                 # Optional: considered alternatives
    - name: "Alternative approach"
      reason_rejected: "Why not chosen"
```

### Traceability Section (Optional)

```yaml
traceability:
  adr_refs:                     # Optional: related ADRs
    - "ADR-115"
  requirement_refs:             # Optional: related requirements
    - "FR-001"
    - "NFR-001"
  epic_ref: "EPIC-1118"         # Optional: parent EPIC
  user_story_refs:              # Optional: related user stories
    - "US-001"
```

### Metadata Section

```yaml
metadata:
  status: draft                 # Required
  created: "2025-12-24"         # Required: ISO 8601
  provider: canonical           # Required
  version: "1.0.0"              # Optional: semantic version
  bounded_context: "WorkManagement"  # Optional: from ADR-024
```

**Status Values:**

| Status | Description |
| --- | --- |
| `draft` | Initial creation, not reviewed |
| `review` | Under review/refinement |
| `approved` | Approved for implementation |
| `implemented` | Implementation complete |
| `deprecated` | No longer valid |

**Bounded Context Values (ADR-024):**

- WorkManagement
- Orchestration
- Workflows
- Expertise
- ExecutionControl
- TriggerManagement
- Integrations

## Validation Rules

### ID Formats

| Field | Format | Example |
| --- | --- | --- |
| Specification ID | SPEC-{number} | SPEC-042 |
| Requirement ID | REQ-{number} | REQ-001 |
| Acceptance Criterion ID | AC-{number} | AC-001 |
| ADR Reference | ADR-{number} | ADR-115 |
| EPIC Reference | EPIC-{number} | EPIC-1118 |
| User Story Reference | US-{number} | US-001 |

### Content Constraints

| Field | Constraint |
| --- | --- |
| `context.problem` | Minimum 20 characters |
| `requirements` | At least one requirement |
| `acceptance_criteria` | At least one criterion per requirement |
| `metadata.created` | Valid ISO 8601 date |

### EARS Pattern Validation

Each requirement's `text` field must match its declared `ears_type`:

| ears_type | Required Pattern |
| --- | --- |
| `ubiquitous` | Starts with "The" + entity + "SHALL" |
| `state-driven` | Starts with "WHILE" |
| `event-driven` | Starts with "WHEN" |
| `unwanted` | Contains "IF" and "THEN" |
| `optional` | Starts with "WHERE" |
| `complex` | Multiple pattern keywords |

## JSON Schema Location

```text
schemas/canonical-spec.schema.json
```

## Provider Transformation

The canonical format serves as the hub for all provider transformations:

```text
                    ┌─────────────┐
                    │  Canonical  │
                    │    Spec     │
                    └──────┬──────┘
           ┌───────────────┼───────────────┐
           │       │       │       │       │
           ▼       ▼       ▼       ▼       ▼
        ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐
        │EARS │ │Ghrkn│ │Kiro │ │SpKit│ │ ADR │
        └─────┘ └─────┘ └─────┘ └─────┘ └─────┘
```

All providers implement `ISpecificationProvider`:

```csharp
interface ISpecificationProvider
{
    string ProviderName { get; }
    Task<Result<CanonicalSpec>> ParseAsync(string input);
    Task<Result<string>> GenerateAsync(CanonicalSpec spec);
    Task<ValidationResult> ValidateAsync(CanonicalSpec spec);
    bool CanParse(string input);
}
```

## References

**Detailed Documentation:**

- [Schema Reference](references/schema-reference.md)
- [Validation Rules](references/validation-rules.md)

**Repository Resources:**

- `schemas/canonical-spec.schema.json` - JSON Schema
- `docs/adr/ADR-115-specification-provider-abstraction.md` - Architecture decision

---

**Last Updated:** 2025-12-26
