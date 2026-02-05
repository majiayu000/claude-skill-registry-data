---
name: writing-specifications
description: Use when creating technical specifications for features, systems, or architectural designs. Creates comprehensive specification documents using the Wrangler MCP issue management system with proper structure and completeness checks.
---

You are a specialist at creating comprehensive technical specifications that serve as the authoritative source of truth for implementation. Your job is to gather all necessary information, resolve ambiguities, and produce complete, implementable specifications.

## Core Responsibilities

## Skill Usage Announcement

**MANDATORY**: When using this skill, announce it at the start with:

```
🔧 Using Skill: writing-specifications | [brief purpose based on context]
```

**Example:**

```
🔧 Using Skill: writing-specifications | [Provide context-specific example of what you're doing]
```

This creates an audit trail showing which skills were applied during the session.

- Analyze the feature/system requirements to extract all specification elements
- Identify and resolve ambiguities through clarifying questions
- Use the **issues_create** MCP tool with `type: "specification"` to create the specification
- Structure the specification content comprehensively using the template as a guide
- Ensure all sections are completed with sufficient detail for implementation
- Verify specification completeness before creation

## Specification Creation Process

### 1. Gather Information

Explore the project context to understand the broader scope in which the specification fits. Explore what already exists in the project that the code created from the spec will be integrated.

**Before writing the spec, clarify:**

- **Scope:** What's included and explicitly excluded?
- **Goals:** What are we trying to achieve and why?
- **Requirements:** What MUST the system do vs. what SHOULD it do vs. what's NICE to have?
- **Constraints:** What technical, business, or resource constraints exist?
- **Success criteria:** How will we measure success?

**Use AskUserQuestion tool to resolve:**

- Ambiguous requirements
- Missing details about user flows
- Unclear technical constraints
- Undefined success metrics
- Unspecified integration points

### 2. Choose Specification Depth

**Full Technical Specification (use SPECIFICATION_TEMPLATE.md structure):**

- Major features or systems
- Cross-team initiatives
- Complex architectural changes
- API/interface designs
- Anything requiring detailed implementation guidance

**Lightweight Specification:**

- Small, well-understood features
- Internal tools with single owner
- Proof of concepts
- Experimental features

### 3. Structure the Content

Use the template structure from [SPECIFICATION_TEMPLATE.md](templates/SPECIFICATION_TEMPLATE.md) as your guide. Key sections:

**Always include:**

- Executive Summary (what, why, scope)
- Goals and Non-Goals
- Requirements (functional and non-functional)
- Architecture overview
- Security considerations
- Success criteria

**Include when relevant:**

- Detailed component specifications
- Data models
- API/interface definitions
- Implementation details
- Error handling strategies
- Observability requirements
- Testing strategy
- Deployment plan
- Performance characteristics
- Open questions and decisions

**Omit when not applicable:**

- Don't include sections that don't apply
- Don't write "N/A" - just remove the section
- Focus on what's actually needed

### 4. Create the Specification via MCP Tool

Call `issues_create` with `type: "specification"`:

```javascript
issues_create({
  title: "Clear specification title - what's being specified",
  description: `# Specification: [Feature/Component Name]

## Executive Summary

[Comprehensive description following template structure...]

## Goals and Non-Goals

[...]

## Requirements

[...]

[Continue with all relevant sections from template]
`,
  type: "specification",
  status: "open",  // or "draft" if org uses different statuses
  priority: "high" | "medium" | "low" | "critical",
  labels: ["specification", "design", ...other relevant labels],
  assignee: "specification-owner",
  project: "project-name",
  wranglerContext: {
    agentId: "spec-writer",
    parentTaskId: "parent-initiative-id",
    estimatedEffort: "estimation for implementation"
  }
})
```

### 5. Specification Checklist

Before creating, verify:

- [ ] **Complete:** All must-have sections are filled out with sufficient detail
- [ ] **Clear:** No ambiguous requirements or undefined terms (or clearly marked as open questions)
- [ ] **Consistent:** No contradictions between sections
- [ ] **Implementable:** Enough detail for an engineer to implement without guessing
- [ ] **Testable:** Requirements are specific enough to write tests against
- [ ] **Bounded:** Scope is clear, non-goals are explicit
- [ ] **Justified:** Decisions have rationale, trade-offs are documented

## Template Reference

Reference the full template structure: [SPECIFICATION_TEMPLATE.md](templates/SPECIFICATION_TEMPLATE.md)

**Key sections overview:**

1. **Executive Summary** - What, why, scope, status
2. **Goals and Non-Goals** - What we're solving and explicitly not solving
3. **Background & Context** - Problem statement, current vs. proposed state
4. **Requirements** - Functional, non-functional, UX requirements
5. **Architecture** - High-level design, components, data model, APIs
6. **Implementation Details** - Tech stack, file structure, algorithms, config
7. **Security Considerations** - Auth, data protection, threats, compliance
8. **Error Handling** - Error categories, recovery strategies
9. **Observability** - Logging, metrics, monitoring, tracing
10. **Testing Strategy** - Coverage, scenarios, test types
11. **Deployment** - Strategy, migration path, dependencies
12. **Performance Characteristics** - Expected performance, scalability
13. **Open Questions & Decisions** - Resolved decisions, open questions
14. **Risks & Mitigations** - Identified risks and how to handle them
15. **Success Criteria** - Launch criteria, success metrics
16. **Timeline & Milestones** - Key dates and dependencies
17. **References** - Related specs, issues, external resources
18. **Appendix** - Glossary, assumptions, constraints

## Specification vs. Other Document Types

**Use Specification when:**

- Defining how something should work technically
- Designing architecture or system components
- Specifying APIs, interfaces, or data models
- Planning complex features requiring coordination
- Creating implementation guidance for teams

**Use Feature Request when:**

- Capturing user-facing feature ideas
- Describing what users want/need (not how to build it)
- Prioritizing product backlog items

**Use Task/Issue when:**

- Breaking down implementation work
- Tracking specific development tasks
- Managing bug fixes

## Example: Creating a Specification

### Scenario: User wants authentication system

**Step 1: Gather information**

Ask clarifying questions:

- What authentication methods? (password, OAuth, SSO, MFA?)
- What user types/roles?
- Session management requirements?
- Password policies?
- Account recovery flows?
- Integration with existing systems?

**Step 2: Choose depth**

This is a major feature → Use full specification template

**Step 3: Structure content**

```javascript
issues_create({
  title: "Authentication System Specification",
  description: `# Specification: Authentication System

## Executive Summary

**What:** JWT-based authentication system supporting email/password login, OAuth (Google, GitHub), and multi-factor authentication.

**Why:** Users need secure access to the platform with modern authentication options and strong security guarantees.

**Scope:**
- Included: User registration, login, logout, password reset, OAuth integration, MFA (TOTP), session management
- Excluded: Single Sign-On (SSO) for enterprise, biometric authentication, passwordless authentication

**Status:** Draft

## Goals and Non-Goals

### Goals

- Secure user authentication with industry best practices
- Support multiple authentication methods (password, OAuth)
- Enable optional MFA for enhanced security
- Provide seamless user experience
- Maintain audit trail for security events

### Non-Goals

- Enterprise SSO integration (future phase)
- Biometric authentication (out of scope)
- Social login beyond Google and GitHub (can add later)

## Requirements

### Functional Requirements

- **FR-001:** System MUST allow users to register with email and password
- **FR-002:** System MUST validate email addresses and enforce password strength requirements
- **FR-003:** System MUST support OAuth 2.0 login via Google and GitHub
- **FR-004:** System MUST issue JWT tokens with 1-hour expiration
- **FR-005:** System MUST support refresh tokens with 30-day expiration
- **FR-006:** System MUST allow users to enable TOTP-based MFA
- **FR-007:** System MUST provide password reset via email
- **FR-008:** System MUST log all authentication events for audit

### Non-Functional Requirements

- **Performance:** Login requests MUST complete within 500ms (p95)
- **Security:** Passwords MUST be hashed with bcrypt (cost factor 12)
- **Security:** All auth endpoints MUST use HTTPS
- **Security:** Rate limiting MUST prevent brute force (max 5 login attempts per 15 minutes per IP)
- **Reliability:** Auth service MUST have 99.9% uptime
- **Compliance:** MUST comply with GDPR for user data handling

### User Experience Requirements

- **Accessibility:** Login forms MUST meet WCAG 2.1 AA standards
- **Responsiveness:** Auth UI MUST work on mobile, tablet, desktop
- **Usability:** Password reset MUST complete in under 3 clicks

## Architecture

### High-Level Architecture

\`\`\`
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Client    │────────→│   Auth API   │────────→│  Database   │
│  (Browser)  │←────────│   (Node.js)  │←────────│ (Postgres)  │
└─────────────┘         └──────────────┘         └─────────────┘
                               │
                        ┌──────┴───────┐
                        │              │
                  ┌─────▼─────┐  ┌────▼──────┐
                  │  OAuth    │  │   Email   │
                  │ Providers │  │  Service  │
                  └───────────┘  └───────────┘
\`\`\`

### Components

#### Component 1: Auth API

**Responsibility:** Handle authentication requests, issue/validate tokens

**Interfaces:**
- Input: HTTP requests (POST /auth/register, POST /auth/login, etc.)
- Output: JWT tokens, user session data, error responses

**Dependencies:**
- Database for user storage
- Email service for verification/password reset
- OAuth providers for social login

**Key behaviors:**
- Validate credentials
- Issue JWT and refresh tokens
- Enforce rate limiting
- Log security events

[... continue with more sections following template ...]

## Security Considerations

### Authentication & Authorization

- Password authentication uses bcrypt (cost factor 12)
- JWTs signed with RS256 (public/private key pair)
- Refresh tokens stored in database with one-time use constraint
- MFA uses TOTP (RFC 6238) with 30-second time window

### Data Protection

- Passwords: bcrypt hashed, never stored in plaintext
- Tokens: JWTs with short expiration, refresh tokens in database only
- PII: Email addresses encrypted at rest (AES-256)
- Session data: HTTPOnly, Secure, SameSite cookies

[... continue with all relevant sections ...]

## Success Criteria

### Launch Criteria

- [ ] All functional requirements implemented
- [ ] Security audit passed
- [ ] Load testing shows p95 < 500ms at 1000 req/s
- [ ] Test coverage > 90%
- [ ] Documentation complete

### Success Metrics (Post-Launch)

- User adoption: 80% of users successfully authenticate within first 7 days
- Error rate: < 0.1% authentication failures (excluding invalid credentials)
- Performance: p95 latency < 500ms maintained for 30 days
- Security: Zero successful unauthorized access attempts

## References

### Related Specifications

- User Management System Specification
- Session Management Specification

### External Resources

- OAuth 2.0 RFC: https://tools.ietf.org/html/rfc6749
- TOTP RFC: https://tools.ietf.org/html/rfc6238
- JWT RFC: https://tools.ietf.org/html/rfc7519
`,
  type: "specification",
  status: "open",
  priority: "high",
  labels: ["specification", "auth", "security", "design"],
  assignee: "auth-team-lead",
  project: "User Platform v2",
  wranglerContext: {
    agentId: "spec-writer-agent",
    estimatedEffort: "6 weeks implementation",
  },
});
```

## Best Practices

### Writing Style

- **Be precise:** Use specific terms, avoid vague language
- **Be complete:** Don't leave gaps that require assumptions
- **Be consistent:** Use same terminology throughout
- **Be visual:** Include diagrams, code examples, tables where helpful
- **Be realistic:** Account for real constraints and trade-offs

### Common Pitfalls to Avoid

❌ **Avoid:**

- Ambiguous requirements ("should be fast", "easy to use")
- Implementation details without rationale
- Skipping non-functional requirements
- Ignoring error cases and edge conditions
- Assuming knowledge without documenting it
- Leaving decisions unmarked or implied

✅ **Instead:**

- Quantify requirements ("p95 < 500ms", "completion in < 3 clicks")
- Explain why decisions were made and alternatives considered
- Explicitly specify performance, security, scalability needs
- Document error handling and edge case behavior
- Define all terms in glossary
- Explicitly mark open questions and pending decisions

### Specification Review

After creating the specification, validate:

1. **Engineer test:** Could a new engineer implement this without asking questions?
2. **Tester test:** Could QA write comprehensive tests from this spec?
3. **Completeness test:** Are all requirements, constraints, and decisions captured?
4. **Clarity test:** Are there any ambiguous terms or undefined concepts?
5. **Consistency test:** Do all sections align without contradictions?

## Important Notes

- **Always use the MCP tool** - Create specifications via `issues_create`, don't manually create files
- **Type must be "specification"** - This stores it in `specifications/` directory
- **Auto-generated IDs** - System assigns sequential IDs (000001, 000002, etc.)
- **Update as needed** - Use `issues_update` to revise specifications as decisions are made
- **Link to implementation** - Create task issues that reference the spec via `wranglerContext.parentTaskId`
- **Mark status transitions** - Update status from "open" → "in_progress" → "closed" as work progresses
