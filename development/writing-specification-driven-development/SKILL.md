---
name: writing-specification-driven-development
description: Write specification documents for features using specification-driven development practices, including requirements with user stories, architecture design documents with correctness properties, and implementation plans with task breakdowns. Use when planning a new feature, designing system architecture, creating implementation roadmaps, or documenting technical specifications.
---


# Overview
This skill guides you through writing comprehensive specification documents using specification-driven development (SDD) methodology. The workflow creates three interconnected documents:

1) Requirements Document - What to build (user stories, acceptance criteria)

2) Design Document - How to build it (architecture, properties, data models)

3) Tasks Document - Implementation roadmap (task breakdown, dependencies)

Each document follows a proven pattern that ensures:
- Clear traceability from requirements → design → implementation

- Formal correctness properties that guide testing

- Maintainable, reference-able structure

## When to Use This Skill

Use this skill when:
- Designing architecture before implementation
- Planning a new feature or enhancement
- Designing system architecture or components
- Creating implementation roadmaps
- Documenting technical specifications
- Conducting technical reviews
- Creating specification documents for stakeholders
- Defining correctness properties for validation
- Breaking down large features into actionable tasks

## Workflow

The specification-driven development workflow follows these phases:

### Phase 1: Requirements Gathering
**Goal:** Understand what needs to be built and why

See detailed guide: [reference/requirements.md](reference/requirements.md)

**Key Activities:**
- Initial discovery and clarifying questions
- User stories creation
- Acceptance criteria definition
- Requirements review and approval

**Output:** `requirements.md` - Approved requirements document

**⚠️ CRITICAL:** Do NOT proceed to Phase 2 until user explicitly approves the requirements document.

---

### Phase 2: Architecture & Design
**Goal:** Define how the system will be built

**Prerequisites:** ✅ Phase 1 requirements.md must be approved by user

See detailed guide: [reference/design.md](reference/design.md)

**Key Activities:**
- System architecture design
- Correctness properties definition
- API & interface design
- Design review and approval

**Output:** `design.md` - Approved design document with correctness properties

**⚠️ CRITICAL:** Do NOT proceed to Phase 3 until user explicitly approves the design document.

---

### Phase 3: Implementation Planning
**Goal:** Break down work into actionable tasks

**Prerequisites:** ✅ Phase 2 design.md must be approved by user

See detailed guide: [reference/tasks.md](reference/tasks.md)

**Key Activities:**
- Task breakdown and hierarchical structure
- Dependency mapping
- Property-based test planning
- Tasks review and approval

**Output:** `tasks.md` - Approved implementation task list

**⚠️ CRITICAL:** Do NOT proceed to implementation until user explicitly approves the tasks document.

---

## Key Principles

1. **User as Ground Truth:** Always validate with user before moving to next phase. NEVER proceed without explicit approval.
2. **Sequential Approval:** Requirements → Design → Tasks. Each phase requires user approval before proceeding.
3. **Traceability:** Maintain clear links between requirements → design → tasks
4. **Formal Correctness:** Define testable properties, not just descriptions
5. **Iterative:** Expect to refine specs as understanding deepens
6. **Documentation:** Keep specs updated as single source of truth

---

## Approval Gates

### Gate 1: Requirements Approval
**Before creating design.md:**
- Present requirements.md to user
- Ask: "Do you approve these requirements? Can I proceed to design?"
- Wait for explicit approval
- Only proceed to Phase 2 after approval

### Gate 2: Design Approval
**Before creating tasks.md:**
- Present design.md to user
- Ask: "Do you approve this design? Can I proceed to create tasks?"
- Wait for explicit approval
- Only proceed to Phase 3 after approval

### Gate 3: Tasks Approval
**Before starting implementation:**
- Present tasks.md to user
- Ask: "Do you approve this task breakdown? Can I start implementation?"
- Wait for explicit approval
- Only proceed to implementation after approval

---

## Quick Reference

### Document Templates
- Requirements template: See [reference/requirements.md](reference/requirements.md#document-template)
- Design template: See [reference/design.md](reference/design.md#document-template)
- Tasks template: See [reference/tasks.md](reference/tasks.md#document-template)

### Handling Incomplete Information
See [reference/requirements.md](reference/requirements.md#handling-incomplete-information) for strategies on:
- Asking structured questions
- Making reasonable assumptions
- Using placeholders
- Iterative refinement

---

## Best Practices

1. **Start Simple:** Begin with minimal viable spec, expand as needed
2. **Be Specific:** Use concrete examples, avoid vague descriptions
3. **Link Everything:** Connect requirements → design → tasks explicitly
4. **Test Early:** Define properties before implementation
5. **Iterate Often:** Refine specs based on implementation learnings
6. **Document Decisions:** Capture "why" not just "what"
7. **Keep Updated:** Specs are living documents, not one-time artifacts

---

## Common Pitfalls to Avoid

- ❌ Writing specs without user validation
- ❌ Proceeding to next phase without explicit user approval
- ❌ Creating design.md before requirements.md is approved
- ❌ Creating tasks.md before design.md is approved
- ❌ Skipping correctness properties
- ❌ Creating tasks before design is clear
- ❌ Making specs too detailed upfront
- ❌ Not updating specs during implementation
- ❌ Treating specs as write-once documents
- ❌ Ignoring non-functional requirements

---

## Example Usage

**User Request:** "I need an API to manage user authentication"

**Phase 1 - Requirements:**
- Ask: What auth methods? (email/password, OAuth, etc.)
- Ask: What security requirements? (2FA, password rules, etc.)
- Write user stories and acceptance criteria
- Present requirements.md to user
- **WAIT for user approval** ⏸️
- ✅ User approves → Proceed to Phase 2

**Phase 2 - Design:**
- Design auth flow and JWT structure
- Define correctness properties (e.g., "tokens expire after N minutes")
- Design API endpoints (/login, /logout, /refresh)
- Present design.md to user
- **WAIT for user approval** ⏸️
- ✅ User approves → Proceed to Phase 3

**Phase 3 - Tasks:**
- Break down: Setup, Auth logic, Token management, Testing
- Create PBT tasks for each property
- Order by dependencies
- Present tasks.md to user
- **WAIT for user approval** ⏸️
- ✅ User approves → Proceed to Phase 4

---

## Success Criteria

A well-written specification should:
-  Be understandable by both technical and non-technical stakeholders
-  Have clear traceability from requirements to implementation
-  Include testable correctness properties
-  Provide actionable implementation guidance
-  Be maintainable and updatable
-  Serve as single source of truth for the feature
