---
name: Spec and Plan Generation
description: This skill should be used when commands need to generate specifications or implementation plans, when the user asks about "how to write specs", "how to create plans", "spec structure", "plan hierarchy", or when working with track creation. Provides patterns for interactive questioning, spec structure, and hierarchical plan generation.
version: 0.1.0
---

# Spec and Plan Generation

This skill provides patterns and strategies for generating high-quality specifications and implementation plans for Conductor tracks.

## Overview

Effective specs and plans are the foundation of Context-Driven Development. This skill covers:
- Interactive questioning strategies
- Specification structure and content
- Hierarchical plan generation
- Workflow methodology integration
- Quality criteria and validation

## Interactive Questioning Strategy

### Question Types

**Additive Questions** (multiple answers allowed):
- Use for brainstorming and defining scope
- Add "(Select all that apply)" after the question
- Examples: "What features should this include?", "Who are the target users?"

**Exclusive Choice Questions** (single answer):
- Use for foundational, singular commitments
- Do NOT add "(Select all that apply)"
- Examples: "What is the primary technology?", "Which workflow methodology?"

### Questioning Guidelines

1. **Present Options**: Always provide 2-3 plausible options
2. **Include Escape Hatch**: Last option must be "Type your own answer"
3. **Sequential Flow**: Ask one question at a time, wait for response
4. **Context-Aware**: Reference project context (product.md, tech-stack.md)
5. **Confirm Understanding**: Summarize before moving to next question

### Question Count by Track Type

- **Features**: 3-5 questions to clarify requirements
- **Bugs**: 2-3 questions for reproduction and expected behavior
- **Chores**: 2-3 questions for scope and success criteria

## Specification Structure

### Essential Sections

1. **Overview**: High-level description (2-3 paragraphs)
2. **Functional Requirements**: What it must do (bulleted list)
3. **Non-Functional Requirements**: Performance, security, etc. (if applicable)
4. **Acceptance Criteria**: Definition of done (testable conditions)
5. **Out of Scope**: What this does NOT include (prevents scope creep)

### Spec Quality Criteria

- **Specific**: Clear, unambiguous requirements
- **Testable**: Can verify completion
- **Achievable**: Realistic given constraints
- **Relevant**: Aligns with product goals
- **Time-bound**: Implicitly through plan phases

For detailed spec templates and examples, see:
- **`references/spec-templates.md`** - Templates for features, bugs, chores
- **`examples/sample-specs/`** - Real-world specification examples

## Plan Generation

### Hierarchical Structure

Plans have three levels:

1. **Phases**: Major stages (3-7 per track)
   - Example: "Backend API", "Frontend UI", "Testing & Documentation"

2. **Tasks**: Specific actions (3-10 per phase)
   - Example: "Create user model", "Implement authentication"

3. **Sub-tasks**: Detailed steps (2-5 per task)
   - Example: "Add email field", "Add password hashing"

### Plan Quality Criteria

- **Atomic**: Each task is independently completable
- **Sequential**: Logical order of execution
- **Testable**: Can verify each task completion
- **Realistic**: Achievable scope per task
- **Complete**: Covers all spec requirements

### Workflow Integration

Plans must follow the methodology defined in `workflow.md`:

**TDD Workflow**:
```markdown
### [ ] Task: Add user validation
- [ ] Sub-task: Write validation tests
- [ ] Sub-task: Run tests (expect failure)
- [ ] Sub-task: Implement validation logic
- [ ] Sub-task: Run tests (expect pass)
- [ ] Sub-task: Refactor for clarity
```

**Standard Workflow**:
```markdown
### [ ] Task: Add user validation
- [ ] Sub-task: Implement validation logic
- [ ] Sub-task: Test validation manually
- [ ] Sub-task: Review code quality
```

### Phase Completion Tasks

If `workflow.md` defines a "Phase Completion Verification and Checkpointing Protocol", append to each phase:

```markdown
### [ ] Task: Conductor - User Manual Verification '<Phase Name>' (Protocol in workflow.md)
```

For detailed plan generation strategies, see:
- **`references/plan-generation-patterns.md`** - Advanced planning techniques
- **`examples/sample-plans/`** - Real-world plan examples

## Question Examples by Track Type

### Feature Questions

1. "What specific functionality should this feature provide?"
2. "Who will use this feature and in what scenarios?"
3. "What are the inputs and outputs?"
4. "How should it integrate with existing features?"
5. "What are the acceptance criteria?"

### Bug Questions

1. "What is the current (incorrect) behavior?"
2. "What is the expected (correct) behavior?"
3. "How can this bug be reproduced?"

### Chore Questions

1. "What needs to be improved or refactored?"
2. "What is the scope of changes?"
3. "What are the success criteria?"

## User Confirmation Process

### For Specifications

1. Present drafted spec in markdown format
2. Ask: "Does this accurately capture the requirements?"
3. Offer options:
   - "Yes, this is correct"
   - "No, I need to make changes"
4. If changes needed, iterate until approved

### For Plans

1. Present drafted plan in markdown format
2. Ask: "Does this plan cover all necessary work?"
3. Offer options:
   - "Yes, proceed with this plan"
   - "No, I need to adjust the plan"
4. If changes needed, iterate until approved

## Common Patterns

### Feature Spec Pattern

```markdown
# Specification: [Feature Name]

## Overview
[2-3 paragraphs describing the feature, its purpose, and context]

## Functional Requirements
- Must allow users to [action]
- Must validate [input] before [action]
- Must display [output] when [condition]

## Non-Functional Requirements
- Performance: [metric]
- Security: [requirement]
- Accessibility: [standard]

## Acceptance Criteria
- [ ] Users can [action] successfully
- [ ] System validates [input] correctly
- [ ] Error messages are clear and helpful

## Out of Scope
- [Feature X] will be addressed in a future track
- [Integration Y] is not part of this implementation
```

### Bug Spec Pattern

```markdown
# Specification: Fix [Bug Name]

## Overview
[Description of the bug and its impact]

## Current Behavior
[What currently happens - the bug]

## Expected Behavior
[What should happen - the fix]

## Reproduction Steps
1. [Step 1]
2. [Step 2]
3. [Observe incorrect behavior]

## Acceptance Criteria
- [ ] Bug no longer occurs when following reproduction steps
- [ ] Existing functionality remains intact
- [ ] Tests added to prevent regression
```

### Plan Pattern

```markdown
# Implementation Plan: [Track Title]

## Phase 1: [Phase Name]

### [ ] Task: [Task Name]
- [ ] Sub-task: [Detailed step]
- [ ] Sub-task: [Detailed step]

### [ ] Task: [Task Name]
- [ ] Sub-task: [Detailed step]

### [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: [Phase Name]

### [ ] Task: [Task Name]
- [ ] Sub-task: [Detailed step]

### [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)
```

## Tips for Commands

When generating specs and plans:
1. Load project context first (product.md, tech-stack.md, workflow.md)
2. Use AskUserQuestion for interactive gathering
3. Present options with "Type your own answer"
4. Confirm drafts before finalizing
5. Follow workflow methodology in plans
6. Include phase completion verification tasks
7. Keep tasks atomic and testable

## Additional Resources

- **`references/spec-templates.md`** - Detailed templates
- **`references/plan-generation-patterns.md`** - Advanced patterns
- **`examples/sample-specs/`** - Example specifications
- **`examples/sample-plans/`** - Example plans
