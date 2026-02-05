---
name: specification
description: Use when writing or updating spec.md files. Defines requirement format, user story structure, and scenario patterns.
---

# Specification Writing Skill

This skill defines how to write specifications that follow the project's conventions.
**CRITICAL:** Stick to the Domain Specific Language in this document. Do not add you own extra headings for example.

## Specification Location

**Specifications live close to the code** following the principle of locality of behavior:

- Spec filename: `SPEC.md` (uppercase)
- Location: In the same directory as the code it specifies, or in a feature-specific subdirectory
- Example: `src/feature/SPEC.md` or `src/feature/SPEC.md`

## Specification Format

Every SPEC.md file must follow this structure:

### 1. Feature Header
```markdown
# {Feature Name} Specification

## Feature: {Brief Feature Title}
As a {user role}
I want to {goal/capability}
Possible Solutions:
- {Solution 1}
```

**Rationale for User Goals + Possible Solutions:**
- Focus on WHAT the user wants to achieve, not a specific HOW
- Acknowledge that multiple solutions may exist to meet the user's goal
- Solutions should be considered throughout implementation
- Design the codebase to be modular enough to swap solutions without major refactoring
- Keeps options open until implementation details are needed

### 2. Requirements Section
```markdown
## Requirements
Format: `[IS-TEST-IMPLEMENTED][IS-CODE-IMPLEMENTED] IDENTIFIER: example case`
- U = implemented via unit test
- A = implemented via acceptance test
- X = implemented
- O = not yet implemented
```

### 3. Organized Requirements
Group requirements into logical sections:

**Requirement format:**
```markdown
- [O][O] REQ-XXX-001: {Specific, testable requirement}
- [O][O] REQ-XXX-002: {Another specific requirement}
```

**Requirement naming:**
- Use feature-specific prefix
- Number sequentially starting from 001
- Sequentiallity does not need to be enforced (reduce work renumbering)
  - you can skip numbers if a requirement is removed
  - add characters if add a requirement between other requirements
- Keep requirements atomic and testable
- One requirement per line

**CRITICAL - Atomic Requirements:**
- Each requirement must test ONE specific thing
- If a requirement has "and" or lists multiple attributes, split it into separate requirements
- Each requirement should map to one test (or a small set of closely related tests)

**CRITICAL - User-Facing Requirements Only:**
- Requirements must describe FEATURES from the user's perspective
- Each requirement should be stated ONLY ONCE in the spec
- DO NOT create separate requirements for implementation details

**Before adding a requirement, ask:**
1. Is this something the user directly experiences or cares about?
2. Have I already stated this requirement elsewhere in the spec or in another spec file?
3. Is this describing WHAT the system does for the user, or HOW it does it internally?

### 4. Scenarios

**IMPORTANT:** ONLY add scenarios for modules that require end to end testing with other modules. By default don't add scenarios but elicit from the human if they think Scenarios/Acceptance Testing apply to this feature.  

**Use Given/When/Then format:**
- **Given** - Setup/preconditions
- **When** - User action/trigger
- **Then** - Expected outcome/verification
- **And** - Additional clauses for any section

**Describe WHAT, not HOW:**
- Focus on user behavior and system outcomes
- Avoid implementation details (field names, status codes, internal states)
- Describe the value and intent, not the mechanics
- Keep scenarios at a high level of abstraction

**Cover end-to-end flows:**
- Start with user perspective
- Verify final state

## Integration with STDD Workflow

This spec skill is **STEP 1** of the spec-test-driven development workflow:

1. **Write Spec** ← (this skill)
2. Write Tests (based on spec requirements)
3. Implement Code (to pass tests)

After completing the spec:
1. Get user approval
2. Proceed to writing tests based on requirements using TDD
3. Follow stdd skill for remaining steps
