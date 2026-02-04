---
name: write-to-doc
description: Automatically invoked when writing formal documentation (specs, ADRs, reviews, plans). Ensures consistent structure, appropriate detail level, and proper file location.
---

# Write to Documentation Skill

This skill activates when you need to create or update formal project documentation.

## When This Skill Activates

Automatically engage when:
- Writing feature specifications
- Creating architectural decision records (ADRs)
- Documenting review findings
- Writing implementation plans
- Creating interface definitions
- Documenting data models
- Writing knowledge base articles

## Documentation Principles

### Clarity
- Use clear, precise language
- Define technical terms
- Provide examples where helpful
- Use consistent terminology

### Structure
- Follow established templates
- Use clear headings and sections
- Organize information logically
- Include table of contents for long documents

### Completeness
- Cover all necessary aspects
- Include context and rationale
- Link to related documents
- Specify version and date

### Maintainability
- Keep documentation close to code
- Use relative links for internal references
- Include update dates
- Note document owner/maintainer

## Documentation Locations

### Feature Specifications
- **Location:** `docs/features/[feature-name].md`
- **Template:** `docs/features/_template.md`
- **Purpose:** Formal feature requirements and design

### Architectural Decisions
- **Location:** `docs/architecture/decisions.md` (or individual ADR files)
- **Template:** `docs/architecture/_decision-template.md`
- **Purpose:** Record important architectural choices

### Interface Definitions
- **Location:** `docs/architecture/interfaces/[api-name].md`
- **Template:** `docs/architecture/interfaces/_template.md`
- **Purpose:** API contracts and integration specifications

### Review Findings
- **Location:** `ai_docs/reviews/[type]-[subject]-[date].md`
- **Template:** `ai_docs/reviews/_template.md`
- **Purpose:** Expert review outputs and recommendations

### Implementation Plans
- **Location:** `ai_docs/plans/[feature-name]-plan.md`
- **Purpose:** Detailed implementation breakdown

### Data Models
- **Location:** `docs/architecture/models/[model-name].md`
- **Purpose:** Database schemas, ERDs, domain models

### Knowledge Base
- **Location:** `ai_docs/knowledge/[topic]/`
- **Template:** `ai_docs/knowledge/_template/`
- **Purpose:** Domain knowledge for agents

## Workflow

### 1. Identify Document Type
Determine what kind of documentation is needed

### 2. Load Appropriate Template
Use the template for consistency:
```
Feature Spec → docs/features/_template.md
ADR → docs/architecture/_decision-template.md
Interface → docs/architecture/interfaces/_template.md
Review → ai_docs/reviews/_template.md
```

### 3. Fill Template Sections
Complete all required sections:
- Don't skip sections - use "N/A" if truly not applicable
- Provide sufficient detail for implementation
- Include examples and code snippets where helpful
- Link to related documents

### 4. Use Proper Formatting

#### Headings
```markdown
# Document Title (H1 - once per document)
## Major Section (H2)
### Subsection (H3)
#### Detail (H4)
```

#### Code Blocks
```markdown
```language
code here
```
```

#### Lists
```markdown
- Unordered item
- Unordered item

1. Ordered item
2. Ordered item
```

#### Tables
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data     | Data     | Data     |
```

#### Links
```markdown
[Link Text](relative/path/to/doc.md)
[External Link](https://example.com)
```

#### Emphasis
```markdown
**bold** for strong emphasis
*italic* for emphasis
`code` for inline code
```

### 5. Include Metadata
Add document metadata at the top:
```markdown
**Version:** 1.0.0
**Last Updated:** 2024-01-15
**Status:** Draft | In Review | Approved | Deprecated
**Owner:** Team/Person
```

### 6. Cross-Reference Related Docs
Link to:
- Related feature specs
- Relevant ADRs
- Interface definitions
- Architecture documentation
- Previous decisions

### 7. Save to Correct Location
Follow the location guidelines above

## Document Quality Checklist

Before finalizing documentation:

- [ ] Uses appropriate template
- [ ] All required sections completed
- [ ] Clear and concise language
- [ ] Technical terms defined
- [ ] Examples provided where helpful
- [ ] Code snippets included where relevant
- [ ] Related documents linked
- [ ] Metadata included (version, date, status)
- [ ] Saved to correct location
- [ ] File naming follows convention
- [ ] Formatting consistent
- [ ] Spelling and grammar checked

## Writing Style

### Active Voice
**Good:** "The system validates user input"
**Avoid:** "User input is validated by the system"

### Present Tense
**Good:** "The function returns a Promise"
**Avoid:** "The function will return a Promise"

### Specific Language
**Good:** "Response time must be less than 200ms"
**Avoid:** "Response should be fast"

### Concise Sentences
**Good:** "Use JWT tokens for authentication."
**Avoid:** "In order to provide authentication capabilities, the system should utilize JWT tokens."

## Common Document Types

### Feature Specification
**Purpose:** Define what to build
**Key Sections:** Overview, requirements, user flows, acceptance criteria, technical considerations

### ADR (Architectural Decision Record)
**Purpose:** Record important decisions
**Key Sections:** Context, decision drivers, options considered, decision, consequences

### Interface Definition
**Purpose:** Define API contract
**Key Sections:** Endpoints, request/response formats, error handling, examples

### Review Report
**Purpose:** Document review findings
**Key Sections:** Summary, findings by area, issues by severity, recommendations

### Implementation Plan
**Purpose:** Break down implementation
**Key Sections:** Steps, considerations, risks, success criteria

## Examples

### Good Feature Spec Section
```markdown
## User Flow

### Happy Path: User Registration

1. User navigates to `/signup`
2. User fills registration form:
   - Email (validated: must contain @, max 254 chars)
   - Password (min 10 chars, must include uppercase, lowercase, number)
   - Name (min 2 chars, max 100 chars)
3. User clicks "Sign Up"
4. System validates input (client-side)
5. System submits to `POST /api/auth/register`
6. System sends verification email
7. System displays "Check your email" message
8. User clicks verification link in email
9. System activates account
10. System redirects to dashboard

### Error Path: Invalid Email

1-3. [Same as happy path]
4. System detects invalid email format
5. System displays error: "Please enter a valid email address"
6. Focus returns to email field
7. User corrects and resubmits
```

### Good ADR
```markdown
# ADR 003: Use JWT for Authentication

**Date:** 2024-01-15
**Status:** Accepted

## Context

We need to authenticate users across our web app and mobile apps. We require:
- Stateless authentication
- Support for multiple clients
- Token expiration and refresh
- Scalability to millions of users

## Decision Drivers

- Horizontal scalability (no server-side session storage)
- Mobile app support
- API-first architecture
- Security requirements

## Decision

Use JWT (JSON Web Tokens) for authentication with:
- 15-minute access token expiration
- 7-day refresh token expiration
- RS256 signing algorithm
- Tokens stored in httpOnly cookies for web, secure storage for mobile

## Consequences

### Positive
- Stateless - easy to scale horizontally
- Works across all clients
- Industry standard with good library support
- Self-contained - no database lookup per request

### Negative
- Cannot revoke tokens before expiration
- Token size larger than session IDs
- Need to implement refresh token rotation
- More complex than session-based auth

## Implementation Notes

- Store refresh tokens in database for revocation capability
- Implement token rotation on refresh
- Use short access token expiration for security
- Add token to request header: `Authorization: Bearer {token}`
```

## References

- [Markdown Guide](https://www.markdownguide.org/)
- [GitHub Flavored Markdown](https://github.github.com/gfm/)
- [CommonMark Specification](https://commonmark.org/)

## Constraints

- Keep documents focused and purposeful
- Don't document everything - only what adds value
- Update documentation when implementation changes
- Archive outdated documentation rather than deleting
- Link between related documents to avoid duplication
