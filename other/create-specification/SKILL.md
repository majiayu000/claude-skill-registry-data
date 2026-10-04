---
name: create-specification
description: 'Create a new specification file organized by feature folders, optimized for Generative AI consumption.'
---

# Create Specification

Your goal is to create a new specification file for `${input:SpecPurpose}`.

The specification file must define the requirements, constraints, and interfaces for the solution components in a manner that is clear, unambiguous, and structured for effective use by Generative AIs. Follow established documentation standards and ensure the content is machine-readable and self-contained.

## Folder Structure

Specifications are organized by feature. Each feature gets its own folder under `specs/` at the repository root.

```
specs/
├── products/
│   ├── index.md          # Auto-generated index of all product specs
│   ├── spec-v1.md        # Initial spec
│   ├── spec-v2.md        # Iteration / revision
│   └── spec-v2.1.md      # Minor revision
├── auth/
│   ├── index.md
│   └── spec-v1.md
└── infrastructure/
    ├── index.md
    └── spec-v1.md
```

### Naming Conventions

- **Feature folders**: `specs/[a-z0-9-]+/` — lowercase, hyphen-delimited, descriptive of the feature domain (e.g., `products`, `user-auth`, `payment-processing`)
- **Spec files**: `spec-v[major].[minor].md` — versioned per iteration
  - First spec for a feature is always `spec-v1.md`
  - Major revisions (breaking changes, scope changes) increment the major version: `spec-v2.md`
  - Minor revisions (clarifications, additions, non-breaking changes) increment minor: `spec-v2.1.md`

### Index File (`index.md`)

Every feature folder must contain an `index.md` that summarizes all specs in that folder. Update or create the index file whenever a new spec is added.

```md
# [Feature Name] Specifications

Summary of all specifications for this feature domain.

| Version | Date | Description |
|---------|------|-------------|
| [v1]    | [date] | [Brief description] |
| [v2]    | [date] | [Brief description] |

## Change Log

- **v2** ([YYYY-MM-DD]): [What changed and why]
- **v1** ([YYYY-MM-DD]): [Initial spec]
```

## Best Practices for AI-Ready Specifications

- Use precise, explicit, and unambiguous language.
- Clearly distinguish between requirements, constraints, and recommendations.
- Use structured formatting (headings, lists, tables) for easy parsing.
- Avoid idioms, metaphors, or context-dependent references.
- Define all acronyms and domain-specific terms.
- Include examples and edge cases where applicable.
- Ensure the document is self-contained and does not rely on external context.
- When iterating on an existing spec, reference the previous version and clearly document what changed.

## Workflow

1. **Determine the feature folder** based on the spec purpose. Ask the user if unclear.
2. **Create the feature folder** if it does not exist under `specs/`.
3. **Check for existing specs** in the folder to determine the correct version number.
4. **Create the spec file** using the template below, saved as `specs/[feature]/spec-v[n].md`.
5. **Update or create `index.md`** in the feature folder to reflect the new spec.

## Specification Template

Each specification file must follow this template. The front matter should be structured correctly:

```md
---
title: [Concise Title Describing the Specification's Focus]
version: [e.g., v1, v2, v2.1]
date_created: [YYYY-MM-DD]
last_updated: [Optional: YYYY-MM-DD]
owner: [Optional: Team/Individual responsible for this spec]
feature: [Feature domain, e.g., products, auth, infrastructure]
tags: [Optional: List of relevant tags or categories]
previous_version: [Optional: Path to previous version, e.g., ../spec-v1.md]
---

# Introduction

[A short concise introduction to the specification and the goal it is intended to achieve.]

## 1. Purpose & Scope

[Provide a clear, concise description of the specification's purpose and the scope of its application. State the intended audience and any assumptions.]

## 2. Definitions

[List and define all acronyms, abbreviations, and domain-specific terms used in this specification.]

## 3. Requirements, Constraints & Guidelines

[Explicitly list all requirements, constraints, rules, and guidelines. Use bullet points or tables for clarity.]

- **REQ-001**: Requirement 1
- **SEC-001**: Security Requirement 1
- **[3 LETTERS]-001**: Other Requirement 1
- **CON-001**: Constraint 1
- **GUD-001**: Guideline 1
- **PAT-001**: Pattern to follow 1

## 4. Interfaces & Data Contracts

[Describe the interfaces, APIs, data contracts, or integration points. Use tables or code blocks for schemas and examples.]

## 5. Acceptance Criteria

[Define clear, testable acceptance criteria for each requirement using Given-When-Then format where appropriate.]

- **AC-001**: Given [context], When [action], Then [expected outcome]
- **AC-002**: The system shall [specific behavior] when [condition]
- **AC-003**: [Additional acceptance criteria as needed]

## 6. Test Automation Strategy

[Define the testing approach, frameworks, and automation requirements.]

- **Test Levels**: Unit, Integration, End-to-End
- **Frameworks**: [List relevant frameworks for this stack]
- **Test Data Management**: [approach for test data creation and cleanup]
- **CI/CD Integration**: [automated testing in CI pipeline]
- **Coverage Requirements**: [minimum code coverage thresholds]
- **Performance Testing**: [approach for load and performance testing]

## 7. Rationale & Context

[Explain the reasoning behind the requirements, constraints, and guidelines. Provide context for design decisions.]

## 8. Dependencies & External Integrations

[Define the external systems, services, and architectural dependencies required for this specification. Focus on **what** is needed rather than **how** it's implemented. Avoid specific package or library versions unless they represent architectural constraints.]

### External Systems
- **EXT-001**: [External system name] - [Purpose and integration type]

### Third-Party Services
- **SVC-001**: [Service name] - [Required capabilities and SLA requirements]

### Infrastructure Dependencies
- **INF-001**: [Infrastructure component] - [Requirements and constraints]

### Data Dependencies
- **DAT-001**: [External data source] - [Format, frequency, and access requirements]

### Technology Platform Dependencies
- **PLT-001**: [Platform/runtime requirement] - [Version constraints and rationale]

### Compliance Dependencies
- **COM-001**: [Regulatory or compliance requirement] - [Impact on implementation]

**Note**: This section should focus on architectural and business dependencies, not specific package implementations. For example, specify "OAuth 2.0 authentication library" rather than a specific package version.

## 9. Examples & Edge Cases

    ```code
    // Code snippet or data example demonstrating the correct application of the guidelines, including edge cases
    ```

## 10. Validation Criteria

[List the criteria or tests that must be satisfied for compliance with this specification.]

## 11. Changelog (from previous version)

[When this is an iteration, document what changed from the previous version:]

- **Added**: [New requirements, sections, or features]
- **Changed**: [Modified requirements or constraints]
- **Removed**: [Deprecated or removed items]
- **Rationale**: [Why these changes were made]

## 12. Related Specifications / Further Reading

- [Link to related specs within this feature folder, e.g., `./spec-v1.md`]
- [Link to specs in other feature folders, e.g., `../auth/spec-v1.md`]
- [Link to relevant external documentation]
```
