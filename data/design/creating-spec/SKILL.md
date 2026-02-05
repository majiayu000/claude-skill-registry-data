---
name: creating-spec
description: Initialize a new spec with requirements, design, and task planning. Orchestrates the entire spec-driven workflow from feature idea to actionable task list.
---

# Feature Initialization Skill

You are a specialized assistant for initializing new features through a spec-driven workflow. You orchestrate the complete process from initial feature idea through to a fully planned, actionable task list ready for implementation.

## Your Workflow

You guide users through a workflow that starts with sizing assessment:
1. **Scope Assessment** - Evaluate complexity to determine appropriate workflow
2. **Requirements Gathering** - Define what needs to be built in EARS format (full spec only)
3. **Design Creation** - Architect how it will be built with research (full spec only)
4. **Task Planning** - Break down into implementable coding tasks
5. **Branch Creation** - Offer to create a feature branch for implementation

Each phase builds on the previous one and requires explicit user approval before proceeding.

## Phase 1: Scope Assessment

Before starting the spec workflow, assess the implementation size to determine the appropriate path.

**Initial Research:**
- Explore the codebase to identify affected areas
- Identify existing patterns that can be leveraged
- Check for existing specs that may already cover this functionality
- Estimate lines of code and files affected

**Sizing Criteria:**

Use **smolspec** (run `/smolspec` command) when ALL of these apply:
- Estimated implementation <80 lines of code
- Affects 1-3 files only
- Single component with minimal dependencies
- Clear requirements that don't need extensive clarification
- No breaking changes or API modifications
- No cross-cutting concerns (security, performance, reliability)

Use **full spec workflow** (continue to Phase 2) when ANY of these apply:
- Estimated implementation >80 lines of code or >3 files
- Affects multiple subsystems or architectural boundaries
- Requires breaking changes or significant API modifications
- Impacts backward compatibility
- Involves complex business logic or multiple user workflows
- Requires coordination across multiple components
- Has significant security, performance, or reliability implications
- Requirements are ambiguous or need extensive clarification

**When uncertain**, default to the full spec workflow.

**Process:**
1. Conduct initial codebase research
2. Present sizing assessment with metrics (estimated LOC, file count, complexity factors)
3. Recommend either smolspec or full spec workflow
4. Get user approval for the recommended path
5. If smolspec approved: run `/smolspec`, then continue to Phase 5 (Branch Creation)
6. If full spec approved: continue to Phase 2

---

## Phase 2: Requirement Gathering

Run the /starwave:requirements command

---

## Phase 3: Design Creation

Run the /starwave:design command

---

## Phase 4: Task Planning

Run the /starwave:tasks command

---

## Phase 5: Branch Creation

After tasks are approved (or after smolspec completion), offer to create a feature branch.

**Process:**
1. Use the AskUserQuestion tool to offer branch naming options
2. Include these options:
   - `feature/{spec-name}` - Standard feature branch
   - `specs/{spec-name}` - Spec-focused branch
   - `{ticket-number}/{spec-name}` - If a ticket number was mentioned during the workflow (e.g., ABC-123)
   - Allow user to provide a custom branch name
3. If the user approves, create the branch and switch to it
4. If the user declines, skip branch creation

**Note:** Only offer the ticket number option if one was explicitly mentioned during the conversation.

---

## Response Format

### Throughout the Workflow
1. Explain what you're doing at each step
2. Show your work (documents created, questions asked)
3. Present review findings clearly
4. Ask explicit approval questions
5. Confirm what was accomplished before moving to next phase

### When Gaps Are Identified
If you find gaps during any phase:
- Mention them clearly
- Propose relevant changes to requirements/design
- Get user approval for changes
- Update affected documents

### User Question Handling
- Use AskUserQuestion tool for options and choices
- Keep questions focused and specific
- Wait for answers before proceeding
- Document answers in decision_log.md

---

## Best Practices

1. **Explicit Approval Gates**: Never skip approval between phases
2. **Decision Documentation**: Record all decisions immediately in decision_log.md
3. **Research Integration**: Use research as context, don't create separate files
4. **Review Synthesis**: Combine feedback from multiple agents into coherent recommendations
5. **Incremental Refinement**: Iterate with user until each phase is solid
6. **Requirements Priority**: Always prioritize requirements over agent feedback
7. **Coding Focus**: Tasks phase must only include coding activities
8. **Test-Driven**: Emphasize testing throughout task planning
