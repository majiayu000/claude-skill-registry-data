---
name: spec-builder
description: Generate comprehensive specification documents including requirements, technical design, and detailed task breakdown from any feature request. Use when the user asks to create specs, requirements docs, design docs, or needs to break down a feature into implementation tasks. Perfect for planning new features, understanding system architecture, or preparing work for AI coding agents.
allowed-tools: Write, Read
---

# Spec Generator Skill

Generate a complete specification suite that transforms ideas into actionable implementation plans.

## Purpose

This skill helps you create professional, comprehensive specification documents that include:

1. **Requirements** (requirements.md) - User stories with acceptance criteria
2. **Technical Design** (design.md) - Architecture, components, and interactions
3. **Task Breakdown** (tasks.md) - Granular, actionable implementation tasks

Perfect for product teams, developers, and AI coding agents to understand requirements, system architecture, and execution steps.

---

## 📋 Phase 1: REQUIREMENTS Generation

### Objective
Create clear, testable requirements using user stories and acceptance criteria.

### Instructions

1. **Identify the Core User Story**
   - Write in format: "As a [user], I want to [action], so that [benefit]"
   - Focus on user value, not implementation

2. **Define Acceptance Criteria using EARS Format**
   - Use WHEN/THEN structure for clarity
   - Make criteria specific and testable
   - Cover both success and failure scenarios

3. **Specify Constraints and Boundaries**
   - Input requirements and validation rules
   - Output expectations
   - Performance requirements
   - Security considerations
   - Error handling requirements

### Template Structure

```markdown
# Requirements: [Feature Name]

## Overview
Brief description of what this feature does and why it matters.

## User Stories

### Story 1: [Title]
**As a** [user type]
**I want** [action]
**So that** [benefit]

### Story 2: [Title]
...

## Acceptance Criteria

### Criterion 1: [Name]
**WHEN** [trigger condition or scenario]
**THE SYSTEM SHALL** [expected behavior]

**GIVEN** [precondition]
**WHEN** [action]
**THEN** [expected outcome]

### Criterion 2: [Name]
...

## Constraints & Requirements

### Functional Requirements
- REQ-001: [Requirement description]
- REQ-002: ...

### Non-Functional Requirements
- Performance: [specific metrics]
- Security: [security requirements]
- Scalability: [scalability needs]

### Input Requirements
- Input format: [specification]
- Validation rules: [rules]
- Data sources: [sources]

### Output Requirements
- Output format: [specification]
- Success conditions: [conditions]
- Failure conditions: [conditions]

## Edge Cases
1. [Edge case 1]
2. [Edge case 2]
...

## Out of Scope
- [What this feature explicitly does NOT include]
```

---

## 🏗️ Phase 2: DESIGN Generation

### Objective
Create a technical design that shows HOW the system will work.

### Instructions

1. **High-Level Architecture**
   - Describe the overall system structure
   - Identify major components and their roles
   - Show data flow and integration points

2. **Component Design**
   - Break down into logical modules/components
   - Define responsibilities for each component
   - Specify interfaces and contracts

3. **Interaction Design**
   - Create sequence diagrams (text format)
   - Show component interactions
   - Define API contracts and data structures

4. **Technical Decisions**
   - List key technical choices
   - Document trade-offs
   - Explain rationale for decisions

5. **Risk Analysis**
   - Identify potential risks
   - Suggest mitigation strategies

### Template Structure

```markdown
# Technical Design: [Feature Name]

## Overview
High-level summary of the technical approach.

## Architecture

### System Architecture
[Describe the overall architecture - layers, boundaries, external dependencies]

```
[Text-based architecture diagram]
┌─────────────┐
│   Frontend  │
├─────────────┤
│   API Layer │
├─────────────┤
│ Business    │
│ Logic       │
├─────────────┤
│   Data      │
│   Layer     │
└─────────────┘
```

### Component Breakdown

#### Component A: [Name]
- **Purpose**: [What it does]
- **Responsibilities**: 
  - [Responsibility 1]
  - [Responsibility 2]
- **Dependencies**: [What it depends on]
- **Interfaces**: [Public APIs/methods]

#### Component B: [Name]
...

## Data Model

### Entities
```
Entity: [Name]
Fields:
  - field1: type (description)
  - field2: type (description)
Relationships:
  - relationship description
```

### Data Flow
1. [Step 1: data enters system]
2. [Step 2: transformation]
3. [Step 3: output]

## Sequence Diagrams

### Primary Flow: [Scenario Name]
```
User → Frontend: [action]
Frontend → API: [request]
API → Service: [call]
Service → Database: [query]
Database → Service: [result]
Service → API: [response]
API → Frontend: [data]
Frontend → User: [display]
```

### Alternative Flow: [Scenario Name]
...

## API Contracts

### Endpoint 1: [Name]
- **Method**: POST/GET/etc
- **Path**: /api/v1/resource
- **Request Body**:
```json
{
  "field1": "type",
  "field2": "type"
}
```
- **Response**:
```json
{
  "status": "success",
  "data": {}
}
```
- **Error Codes**: 400, 401, 500

### Endpoint 2: [Name]
...

## Technical Decisions

### Decision 1: [Title]
- **Context**: [Why this decision is needed]
- **Options Considered**:
  1. Option A: [pros/cons]
  2. Option B: [pros/cons]
- **Decision**: [Chosen option]
- **Rationale**: [Why this was chosen]
- **Trade-offs**: [What we're accepting]

### Decision 2: [Title]
...

## Error Handling Strategy
- [How errors are caught and handled]
- [Logging strategy]
- [User-facing error messages]

## Security Considerations
- Authentication: [approach]
- Authorization: [approach]
- Data protection: [approach]
- Input validation: [approach]

## Performance Considerations
- Expected load: [metrics]
- Optimization strategy: [approach]
- Caching strategy: [if applicable]
- Database indexing: [if applicable]

## Risks & Mitigations

### Risk 1: [Title]
- **Impact**: High/Medium/Low
- **Probability**: High/Medium/Low
- **Mitigation**: [Strategy]

### Risk 2: [Title]
...

## Future Considerations
- [What might change]
- [Extensibility points]
- [Technical debt to consider]
```

---

## ✅ Phase 3: TASK BREAKDOWN Generation

### Objective
Break down the design into granular, actionable tasks suitable for implementation.

### Instructions

1. **Create Sequential Tasks**
   - Order tasks by dependencies
   - Each task should be completable independently once dependencies are met
   - Aim for tasks that take 2-8 hours

2. **For Each Task Include**:
   - Clear description of what needs to be done
   - Expected output/deliverable
   - Input requirements
   - Dependencies on other tasks
   - Acceptance criteria for completion
   - Complexity/time estimate (optional)

3. **Organize by Categories**:
   - Data/Schema tasks
   - Backend/API tasks
   - Frontend/UI tasks
   - Integration tasks
   - Testing tasks
   - Documentation tasks

4. **Review and Organize Tasks**:
   - Ensure tasks are properly sequenced by dependencies
   - Verify each task has clear acceptance criteria
   - Confirm tasks are appropriately sized (2-8 hours each)

### Template Structure

```markdown
# Task Breakdown: [Feature Name]

## Task Overview
Total estimated tasks: [number]
Estimated total effort: [time/complexity]

## Task Dependencies Graph
```
Task 1 → Task 3 → Task 5
Task 2 → Task 4 → Task 5
```

---

## 📦 Phase 1: Foundation Tasks

### Task #1: [Task Title]

**Category**: Data/Schema

**Description**:
[Detailed description of what needs to be done]

**Expected Output**:
- [Deliverable 1: e.g., schema.json file]
- [Deliverable 2: e.g., migration script]

**Input Requirements**:
- [What you need before starting]

**Dependencies**:
- None (or list dependent tasks)

**Acceptance Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Complexity**: Low/Medium/High
**Estimated Time**: [2-4 hours]

**Implementation Notes**:
- [Any specific guidance]
- [Gotchas to watch out for]

---

### Task #2: [Task Title]
...

## 📦 Phase 2: Backend/API Tasks

### Task #3: [Task Title]
...

## 📦 Phase 3: Frontend/UI Tasks

### Task #5: [Task Title]
...

## 📦 Phase 4: Integration Tasks

### Task #7: [Task Title]
...

## 📦 Phase 5: Testing Tasks

### Task #9: [Task Title]

**Category**: Testing

**Description**:
Write unit tests for [component]

**Expected Output**:
- Test file with >80% coverage
- All edge cases covered

**Test Cases**:
1. [Test case 1]
2. [Test case 2]
...

---

## 📦 Phase 6: Documentation & Deployment

### Task #11: [Task Title]
...

---

## Summary

### Critical Path
[List the sequence of tasks that must be completed in order]

### Parallel Work Opportunities
[Tasks that can be done simultaneously]

### Risk Items
[Tasks with high uncertainty or complexity]

### Definition of Done
- [ ] All tasks completed
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Code reviewed
- [ ] Deployed to staging
```

---

## 🚀 Usage Instructions

### How to Use This Skill

1. **Provide the Feature Request**
   - Describe what you want to build
   - Include any context, constraints, or requirements
   - Mention target users and use cases

2. **Let the Skill Work**
   - The skill will guide you through all three phases
   - Ask clarifying questions if needed
   - Iterate on each document

3. **Review and Refine**
   - Review generated documents
   - Request modifications or additions
   - Ensure all stakeholders understand

4. **Track Implementation Progress**
   - Use the generated tasks as a checklist
   - Mark tasks as completed as you implement them
   - Update task status and notes as needed

### Example Invocation

```
Use spec-builder to generate a full spec for:
"Implement user authentication with 2FA, email verification, 
and session expiry handling in our web app."
```

### What You'll Get

After running this skill, you'll have three comprehensive documents:

1. **requirements.md** - Clear user stories and acceptance criteria
2. **design.md** - Technical architecture and component design
3. **tasks.md** - Detailed implementation tasks ready for developers

These documents are optimized for:
- Human developers to understand the system
- AI coding agents (Cursor, Copilot) to implement tasks
- Product teams to validate requirements
- Stakeholders to review scope and approach

---

## 💡 Best Practices

### When Creating Requirements
- Focus on WHAT, not HOW
- Make acceptance criteria testable
- Include both positive and negative cases
- Consider accessibility and internationalization

### When Creating Design
- Start high-level, then drill down
- Document WHY decisions were made
- Consider scalability from the start
- Think about error cases and edge conditions

### When Creating Tasks
- Keep tasks small and focused
- Make dependencies explicit
- Include clear acceptance criteria
- Provide enough context for independent work

### Quality Checklist
- ✅ Can a developer implement this without asking questions?
- ✅ Can QA create test cases from the requirements?
- ✅ Can an AI agent understand the task breakdown?
- ✅ Are trade-offs and risks documented?
- ✅ Is the scope clear (what's included and excluded)?

---

## 📝 Output File Organization

After running this skill, organize output files as:

```
project-root/
├── .claude/
│   └── specs/
│       └── [feature-name]/
│           ├── requirements.md
│           ├── design.md
│           └── tasks.md
```

Or place them in a dedicated specs directory:

```
project-root/
├── docs/
│   └── specs/
│       └── [feature-name]/
│           ├── requirements.md
│           ├── design.md
│           └── tasks.md
```

---

## � Iteratrion and Updates

This skill can also help you:

- **Refine existing specs**: Provide an existing spec document and ask to improve it
- **Update for changes**: When requirements change, update all three documents
- **Generate partial specs**: Only generate requirements or design if that's what you need
- **Compare approaches**: Generate multiple design options for evaluation

---

## 🎯 Success Metrics

A good spec generated by this skill should:

1. **Be Complete**: Cover all aspects from requirements to implementation
2. **Be Clear**: Anyone can understand without additional context
3. **Be Actionable**: Tasks can be implemented immediately
4. **Be Testable**: Acceptance criteria are specific and measurable
5. **Be Maintainable**: Easy to update as requirements evolve

---

## Example Output Snippets

### Requirements Example
```markdown
## User Story
**As a** registered user
**I want** to enable 2FA for my account
**So that** my account is more secure

## Acceptance Criteria
**WHEN** a user enables 2FA
**THE SYSTEM SHALL** generate a QR code with TOTP secret

**GIVEN** 2FA is enabled
**WHEN** user logs in with correct password
**THEN** system prompts for 6-digit code
**AND** code must be entered within 30 seconds
```

### Design Example
```markdown
## Component: AuthenticationService
**Purpose**: Handle user authentication flows

**Responsibilities**:
- Verify user credentials
- Manage 2FA enrollment and verification
- Handle session creation and expiry

**Interface**:
- `login(username, password): SessionToken`
- `verify2FA(userId, code): boolean`
- `enrollIn2FA(userId): QRCode`
```

### Task Example
```markdown
### Task #3: Implement 2FA Enrollment API

**Description**: Create API endpoint for users to enroll in 2FA

**Expected Output**:
- POST /api/v1/auth/2fa/enroll endpoint
- Returns QR code and backup codes
- Stores TOTP secret securely

**Acceptance Criteria**:
- [ ] Endpoint returns 200 with QR code data
- [ ] Secret is encrypted before storage
- [ ] 10 backup codes generated
- [ ] Rate limiting applied (5 requests/hour)
```

---

## 🆘 Troubleshooting

**Q: The generated spec is too detailed**
A: Ask to generate a "lightweight" or "minimal" version

**Q: Need more technical depth**
A: Request "detailed technical design with code examples"

**Q: Tasks are too large**
A: Ask to "break down tasks into smaller sub-tasks of 2-4 hours each"

**Q: Need specific format**
A: Specify your organization's format: "Use our company's standard template"

---

## Version History

- **v1.0.0** (2025-12-20): Initial release with three-phase spec generation

