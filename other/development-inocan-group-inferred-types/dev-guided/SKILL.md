---
name: dev-guided
description: Human-in-the-loop iterative development. Use when requirements will emerge during implementation, decisions need human approval at each step, or work will span multiple sessions with frequent feedback loops. Creates problem statement, decisions log, runbook, and progress tracking.
---

# Guided Development

## Overview

Guided development is a workflow designed for iterative, human-in-the-loop software development. Unlike traditional planning approaches that create detailed upfront plans, this workflow establishes problem boundaries, captures explicit human decisions, and enables incremental implementation with continuous feedback.

**Use this skill when:**
- The problem is exploratory and not fully understood upfront
- Human input is needed for key technical decisions
- Development will proceed iteratively across multiple sessions
- The human wants to maintain control rather than delegate to autonomous execution

## Workflow Decision Tree

When the skill is invoked, determine which phase to enter:

```
Does docs/development/NNN-<name>/ exist with materials?
├─ NO  → Initial Setup Phase (create problem_statement, decisions, runbook, progress)
└─ YES → Implementation Session Phase (load context, plan, implement, update progress)
```

## Initial Setup Phase

When no materials exist, guide the human through creating foundational documents via structured Q&A.

### Process

1. **Determine folder location**
   - Check for existing development session folders: `docs/development/`
   - Determine next number: `NNN` (e.g., 001, 002, etc.)
   - Ask human for feature name
   - Create folder: `docs/development/NNN-<name>/`

2. **Create problem_statement.md**
   - Load the template from `references/template-problem_statement.md`
   - Ask questions to understand the problem:
     - "What problem are you trying to solve?"
     - "What is the scope of this work? What's explicitly out of scope?"
     - "What does success look like?"
     - "Are there any constraints or requirements?"
   - Fill in the template with responses
   - Save as `problem_statement.md`

3. **Create decisions.md**
   - Load the template from `references/template-decisions.md`
   - **CRITICAL RULE:** MUST ask about every unclear aspect. MUST NOT assume "sensible defaults" or "de facto standards"
   - Probe for decisions on:
     - Language/framework choices
     - Library/dependency choices
     - Architectural patterns
     - Data storage approaches
     - Testing strategies
     - Error handling approaches
     - Security considerations
   - For each unclear aspect:
     - Explain why a decision is needed
     - Present options if helpful (without bias)
     - Ask for the human's choice
     - Record the decision with rationale
   - Save as `decisions.md`

4. **Create runbook.md**
   - Load the template from `references/template-runbook.md`
   - Ask questions:
     - "How should this code be built/compiled?"
     - "How should this code be run/tested?"
     - "Are there any other validation steps?"
     - "At what points during implementation should I pause and ask for your feedback?"
   - Fill in build, test, run, and validation instructions
   - Create structured feedback points
   - Save as `runbook.md`

5. **Create empty progress.md**
   - Load the template from `references/template-progress.md`
   - Create empty file (will be populated after first implementation session)
   - Save as `progress.md`

6. **Complete setup**
   - Inform human that setup is complete
   - Ask if they want to start the first implementation session now or later
   - If now, proceed to Implementation Session Phase

### Reference Materials

For detailed guidance on the initial setup phase, read `references/initial-setup.md`.

## Implementation Session Phase

When materials already exist, start an implementation session to continue development work.

### Process

1. **Load context**
   - Read `problem_statement.md` to understand the problem scope
   - Read `decisions.md` to understand what choices have been made
   - Read `runbook.md` to understand validation and feedback points
   - Read `progress.md` to understand what's been done and what's outstanding
   - Check for existing `plan-N.md` files to understand previous approaches

2. **Determine session number**
   - List existing `plan-N.md` files
   - Next session number = max(N) + 1
   - If no plan files exist, this is session 1

3. **Enter plan mode**
   - Based on loaded context, create a plan for this session
   - Plan should include:
     - What will be accomplished
     - Specific steps to take
     - Dependencies between steps
     - Expected validation points from runbook
     - Outstanding questions or uncertainties
   - Present plan to human for approval

4. **Save approved plan**
   - After human approves the plan, save as `plan-N.md` where N is the session number
   - Proceed with implementation

5. **Implement according to plan**
   - Follow the approved plan
   - **Respect feedback points:** When reaching a feedback point in runbook.md, MUST pause and ask for human input
   - **Document new decisions:** If new unclear aspects arise, update decisions.md and ask for human input
   - **Update runbook if needed:** If build/test/validation steps change, update runbook.md
   - **Follow existing decisions:** Use the choices recorded in decisions.md
   - Perform validation steps from runbook.md
   - Ensure all tests pass

6. **Update progress.md**
   - Add a new session entry using this format:
   ```markdown
   ## Session N (YYYY-MM-DD)

   ### Accomplished
   - [What was implemented/completed]
   - [Tests that now pass]
   - [Issues that were resolved]

   ### Outstanding
   - [What still needs to be done]
   - [Known issues or blockers]

   ### Questions
   - [New unclear aspects that need decisions]
   - [Uncertainties or concerns]
   ```

7. **Session completion**
   - Verify all changes are recorded in progress.md
   - Verify any new decisions are in decisions.md
   - Verify runbook.md is current
   - Inform human that session is complete
   - Summarize what was accomplished and what's next

### Reference Materials

For detailed guidance on implementation sessions, read `references/implementation-session.md`.

## Key Principles

### Workflow Principles

1. **No Assumptions**: Never assume "sensible defaults" or "de facto standards". Always ask for explicit human decisions.

2. **Respect Feedback Points**: Feedback points in runbook.md are mandatory pause points. Never skip them.

3. **Living Documents**: decisions.md, runbook.md, and progress.md are living documents that evolve throughout the development session.

4. **Session-Scoped Plans**: Each implementation session gets its own plan file. Plans are ephemeral and session-specific, not long-term roadmaps.

5. **Problem-Focused**: problem_statement.md defines the problem and scope, not the solution. It provides boundaries, not prescriptions.

### Engineering Principles

1. **Test Driven Development (TDD)**: For every new feature or bugfix, you MUST:
   - Write a failing test that correctly validates the desired functionality
   - Run the test to confirm it fails as expected
   - Write ONLY enough code to make the failing test pass
   - Run the test to confirm success
   - Refactor if needed while keeping tests green

2. **YAGNI (You Aren't Gonna Need It)**: The best code is no code. Don't add features we don't need right now. When it doesn't conflict with YAGNI, architect for extensibility and flexibility.

3. **DRY (Don't Repeat Yourself)**: Work hard to reduce code duplication, even if the refactoring takes extra effort.

4. **Minimal Changes**: Make the SMALLEST reasonable changes to achieve the desired outcome. Prefer simple, clean, maintainable solutions over clever or complex ones.

5. **Fix Broken Things Immediately**: All test failures are your responsibility, even if they're not your fault. Fix broken things immediately when you find them.

6. **Never Skip Tests**: Never delete a test because it's failing. Never write tests that "test" mocked behavior. Test output must be pristine to pass.

## Example Usage

**Starting new work:**
```
Human: "I want to add OAuth authentication to the app"
Agent: [Invokes dev-guided skill]
Agent: [Creates docs/development/001-oauth-auth/ folder]
Agent: [Guides through creating problem_statement, decisions, runbook, progress]
Agent: "Setup complete. Ready to start first implementation session?"
```

**Continuing existing work:**
```
Human: "Continue working on OAuth" [in directory with existing materials]
Agent: [Invokes dev-guided skill]
Agent: [Loads problem_statement, decisions, runbook, progress]
Agent: [Enters plan mode]
Agent: "Based on progress, I plan to implement token storage. Here's my plan..."
Agent: [After approval, saves as plan-2.md and implements]
Agent: [Updates progress.md with session 2 summary]
```

## Resources

This skill includes reference materials with detailed phase guidance and templates:

### references/
- `initial-setup.md` - Detailed guidance for the initial setup phase
- `implementation-session.md` - Detailed guidance for implementation sessions
- `template-problem_statement.md` - Template for problem statements
- `template-decisions.md` - Template for decisions with examples
- `template-runbook.md` - Template for runbook with feedback point examples
- `template-progress.md` - Template for progress tracking
