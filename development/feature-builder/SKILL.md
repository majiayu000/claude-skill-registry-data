---
name: feature-builder
description: Guides feature implementation through 8 phases (Phase 0 Architecture → Phase 7 Documentation). Automatically detects when user starts coding without Phase 0 and enforces architecture-first development. Manages state across sessions, launches specialized agents, and ensures quality gates are met through paired programming approach.
---

# Feature Builder Skill

## Purpose

This skill enforces a systematic 8-phase approach to feature implementation that prevents context loss, ensures quality, and maintains architecture documentation. It enables "two-in-the-box" paired programming where both Claude and the user catch issues and suggest improvements.

**Critical Philosophy**: Architecture documentation BEFORE and AFTER implementation prevents wasted effort and enables context to survive session boundaries.

---

## Skill Activation Triggers

### Automatic Activation

This skill automatically activates when the user's message indicates feature development work.

**Intent-Based Triggers** - Look for the INTENT, not exact phrases:

**Creating/Building Intent**:
- "create a feature" / "create feature" / "create new feature"
- "build a feature" / "build feature" / "build a new"
- "add a feature" / "add feature" / "add new feature"
- "implement a feature" / "implement feature" / "implement a new feature"
- "develop a feature" / "develop feature"

**Updating/Modifying Intent**:
- "update a feature" / "update feature"
- "modify a feature" / "modify feature"
- "change a feature" / "change feature"
- "enhance a feature" / "enhance feature"

**Action Phrases**:
- "I want to create/add/implement/build/develop/update/modify [a/new] feature"
- "I want to create/add/implement/build/develop/update/modify [a/new] capability"
- "Let's create/add/implement/build/develop"
- "I'm going to create/add/implement/build/develop"
- "Can we create/add/implement/build/develop"

**Pattern Matching Guidelines**:
- Ignore articles ("a", "the", "an") when matching
- Ignore modifiers ("new", "complex", "simple") when matching
- Match on the core action verb + "feature/capability/functionality"
- If user's message contains action verb (create/add/implement/build/develop/update/modify) + feature-related noun → TRIGGER

**CRITICAL AUTO-DETECTION**: If you detect the user is about to write implementation code (editing .scala files, creating new components) and there is NO corresponding architecture document in `working/`, immediately:
1. **STOP** - Do not proceed with coding
2. **ACTIVATE** this skill
3. **INFORM** user: "I've detected you're about to implement code without Phase 0 architecture documentation. Per the feature-builder workflow, we must create architecture documentation first."
4. **INITIATE** Phase 0 process

### Explicit Invocation

User can also explicitly request: "use feature-builder skill" or "let's follow the feature workflow"

---

## Workflow Overview

```
Phase 0: Document Architecture & Plan (MANDATORY - STRICT GATE)
         ↓ [Explicit Approval Required]
Phase 1: Code Changes (Implementation)
         ↓ [Warning if compilation fails]
Phase 2: Scala Ninja Code Review (Auto-launch agent)
         ↓ [Warning if critical issues found]
Phase 3: Specifications Creation (BDD scenarios)
         ↓ [Warning if undefined steps exist]
Phase 4: Component Testing (Integration verification)
         ↓ [Warning if tests fail, allow override]
Phase 5: Unit Testing with Scala Testing Ninja (Auto-launch agent)
         ↓ [Warning if coverage < 70%, allow override]
Phase 6: Document As-Is Architecture (APPROVAL GATE)
         ↓ [Explicit Approval Required]
Phase 7: Architecture Doc Agent Finalization (Auto-launch agents)
         ↓ [Complete]
```

---

## State Management

### Progress Tracking

For EVERY feature, create and maintain: `working/{feature-name}-progress.md`

This file tracks:
- Feature name and high-level description
- Current phase (0-7) with timestamp
- Phase completion checklist (✅/⏳/❌)
- Key decisions log (date, decision, rationale)
- Files created or modified
- Agent reviews completed
- Blockers or issues encountered
- Next steps

**Update this file at EVERY phase transition** to enable recovery after context loss.

### TodoWrite Integration

Use TodoWrite to create todos for all 8 phases at the start:
```
[ ] Phase 0: Architecture doc created and approved
[ ] Phase 1: Code implemented and compiles
[ ] Phase 2: scala-ninja review complete
[ ] Phase 3: Feature files created
[ ] Phase 4: Component tests passing
[ ] Phase 5: Unit tests passing, coverage met
[ ] Phase 6: As-built architecture documented and approved
[ ] Phase 7: Documentation validated by agents
```

Mark each as `in_progress` when starting, `completed` when phase exits successfully.

---

## Phase 0: Document Architecture & Implementation Plan (STRICT GATE)

### Goal
Establish clear architectural vision BEFORE writing any code.

### Entry Behavior
When this phase starts:
1. **Create progress tracker**: `working/{feature-name}-progress.md` from template
2. **Create architecture doc**: `working/{feature-name}-architecture.md` from template
3. **Engage user in collaborative design**:
   - Ask clarifying questions about requirements
   - Discuss affected modules and integration points
   - Suggest architectural patterns that fit
   - Identify potential issues early
   - Propose alternatives when ambiguity exists

### Collaborative Architecture Design

**Two-in-the-Box Approach**:
- Explain your reasoning for architectural choices
- Ask: "I'm thinking we should use pattern X because Y. What do you think?"
- When user suggests something, discuss trade-offs: "That approach has advantage A but we should consider trade-off B. Which matters more for this feature?"
- Document ALL decisions with rationale in architecture doc

**Required Sections** in architecture document:
1. **Feature Summary**: 2-3 sentence description
2. **Current State**: What exists today (if modifying existing functionality)
3. **Target State**: What we're building
4. **Affected Modules**: Which Maven modules will change
5. **Interface Contracts**: APIs, actor messages, data models
6. **Data Flow**: How information moves through the system (diagram if complex)
7. **Integration Points**: External systems, other actors, services
8. **Success Criteria**: How we'll know it works
9. **Open Questions**: Anything unresolved (must be answered before proceeding)
10. **Design Decisions Log**: Key choices with rationale

### Exit Criteria (STRICT - MUST BE MET)

- ✅ Architecture document complete with all required sections
- ✅ All "Open Questions" resolved
- ✅ User has reviewed the architecture
- ✅ **EXPLICIT APPROVAL RECEIVED**: User must say "approve architecture" or "approved" or "looks good, proceed"
- ✅ Progress tracker created and updated
- ✅ Phase 0 todo marked completed

### Blocking Behavior

**CRITICAL**: Do NOT proceed to Phase 1 until explicit approval is received. If user tries to start coding without approval:
- **STOP**: "We haven't completed Phase 0 yet. The architecture document needs your explicit approval before we can start coding."
- **WAIT**: Pause and wait for approval

**If user wants to change architecture**: Update the document, mark open questions, get approval on the updated version.

---

## Phase 1: Code Changes

### Goal
Implement the code according to the approved architecture document.

### Entry Behavior
1. Mark Phase 1 todo as `in_progress`
2. Reference architecture doc frequently during implementation
3. Use TodoWrite to track individual implementation tasks

### Implementation Guidelines

**Refer to Architecture Doc**:
- Before making decisions, check if architecture doc addresses it
- If making a choice not covered in doc, discuss with user first
- Keep implementation aligned with approved design

**When Design Must Change**:
If during implementation you realize the architecture needs adjustment:
1. **STOP coding**
2. **EXPLAIN** to user: "I've discovered [issue] during implementation. The architecture doc needs updating because [reason]."
3. **PROPOSE** architectural change with rationale
4. **UPDATE** Phase 0 architecture document
5. **GET APPROVAL** on the change
6. **THEN** continue coding

### Exit Criteria (WARNING-BASED)

- ✅ All planned code changes complete
- ✅ Code compiles: `mvn compile -pl {modules} -q`
- ✅ No compilation errors

**If exit criteria NOT met**:
- **WARN**: "Phase 1 exit criteria not met: [specific issues]. This may cause problems in later phases."
- **OFFER OPTIONS**:
  1. "Fix the issues before proceeding (recommended)"
  2. "Proceed anyway with unmet criteria (not recommended - explain risks)"
- **REQUIRE CONFIRMATION**: User must explicitly choose option 2 to proceed with failures

---

## Phase 2: Scala Ninja Code Review

### Goal
Expert-level code review for patterns, idioms, and quality.

### Entry Behavior
1. Mark Phase 2 todo as `in_progress`
2. **AUTO-LAUNCH scala-ninja agent**:
   ```
   Use Task tool with subagent_type=scala-ninja
   Prompt: "Review the following code changes for this feature: [list files]
           Focus on: functional programming patterns, type safety, Scala 3 idioms,
           immutability, composition, error handling, visibility pattern compliance"
   ```

### Review Process

**After scala-ninja completes**:
1. **SUMMARIZE** findings for user: "scala-ninja found X issues: [categorize by severity]"
2. **DISCUSS** recommendations: "The most important suggestion is [X] because [Y]. Do you agree we should apply this?"
3. **APPLY** feedback collaboratively
4. **RE-COMPILE** after changes: `mvn compile -pl {modules} -q`

### Exit Criteria (WARNING-BASED)

- ✅ scala-ninja review complete
- ✅ Critical issues addressed (user may defer non-critical)
- ✅ Code follows Scala best practices
- ✅ Code compiles after fixes

**If exit criteria NOT met**:
- **WARN**: "scala-ninja identified [N] critical issues that weren't addressed: [list]. Proceeding may result in technical debt."
- **ASK**: "Should we address these issues now or proceed anyway?"
- **REQUIRE CONFIRMATION** to proceed with unaddressed critical issues

---

## Phase 3: Specifications Creation

### Goal
Create BDD specifications for the new functionality.

### Entry Behavior
1. Mark Phase 3 todo as `in_progress`
2. Identify test scenarios based on architecture doc and implementation

### Collaborative Scenario Design

**Two-in-the-Box Approach**:
- Propose scenarios: "I think we need scenarios for [X, Y, Z]. Am I missing any edge cases?"
- Ask about priorities: "Should we focus more on error scenarios or happy path for this feature?"
- Discuss coverage: "This covers [percentage] of the new code. Is that sufficient for your risk tolerance?"

**Required Scenarios**:
1. Happy path scenarios
2. Error scenarios (what happens when things go wrong)
3. Edge cases (boundary conditions, empty inputs, etc.)
4. State transitions (for actors/FSMs)

**Feature File Location**: `test-probe-core/src/test/resources/features/component/{actor-name}.feature`

**Step Pattern Naming**: Follow actor-specific patterns from `.claude/styles/bdd-testing-standards.md`

### Exit Criteria (WARNING-BASED)

- ✅ Feature files created
- ✅ Scenarios cover happy path and error cases
- ✅ Step patterns follow actor-specific naming conventions

**If exit criteria NOT met**:
- **WARN**: "Feature files are incomplete: [specific gaps]. Tests may not catch issues."
- **ASK**: "Should we add coverage for [missing scenarios] or proceed?"
- **REQUIRE CONFIRMATION** to proceed with gaps

---

## Phase 4: Component Testing

### Goal
Verify integration behavior through BDD component tests.

### Entry Behavior
1. Mark Phase 4 todo as `in_progress`
2. Implement step definitions if needed
3. Run component tests: `mvn test -Pcomponent-only -pl test-probe-core`

### Test Execution

**Monitor for**:
- Undefined steps (feature file doesn't match step definition)
- Test failures (scenarios failing)
- Errors (exceptions, actor timeouts)

**Fix Issues**:
- Undefined steps → Update feature file or add step definitions
- Failures → Fix implementation or test logic
- Errors → Debug and resolve exceptions

### Exit Criteria (WARNING-BASED)

- ✅ Component tests run successfully
- ✅ All scenarios pass (0 failures, 0 errors, 0 undefined steps)
- ✅ Output shows `BUILD SUCCESS`

**If exit criteria NOT met**:
- **WARN**: "Component tests have [N] failures and [M] undefined steps. Proceeding means integration behavior isn't verified."
- **DETAIL**: List specific failing scenarios
- **ASK**: "Should we fix these issues or proceed anyway? (Proceeding risks undetected integration bugs)"
- **REQUIRE CONFIRMATION** to proceed with failures

---

## Phase 5: Unit Testing with Scala Testing Ninja

### Goal
Achieve comprehensive unit test coverage using testing best practices.

### Entry Behavior
1. Mark Phase 5 todo as `in_progress`
2. **AUTO-LAUNCH scala-testing-ninja agent**:
   ```
   Use Task tool with subagent_type=scala-testing-ninja
   Prompt: "Create comprehensive unit test coverage for: [list files/classes]
           Target coverage: 70% minimum, 85% for actors/FSMs, 80% for business logic
           Focus on: all public methods, edge cases, error handling, state machines,
           fixture-based tests to minimize code duplication"
   ```

### Review Process

**After scala-testing-ninja completes**:
1. **SUMMARIZE** test suite created
2. **RUN** unit tests: `mvn test -Punit-only -pl test-probe-core`
3. **CHECK** coverage if scoverage available
4. **DISCUSS** with user: "Coverage is [X]%. Target was [Y]%. The gap is in [areas]. Should we add more tests?"

### Exit Criteria (WARNING-BASED)

- ✅ Unit tests run: `mvn test -Punit-only -pl test-probe-core`
- ✅ All tests pass (0 failures, 0 errors)
- ✅ Coverage targets met: 70% min, 85% actors/FSMs, 80% business logic
- ✅ Output shows `BUILD SUCCESS`

**If exit criteria NOT met**:
- **WARN**: "Unit test coverage is [X]%, below target of [Y]%. Gaps: [list areas]. This means [Z] code paths aren't regression-protected."
- **ASK**: "Should we add tests to meet coverage targets or proceed?"
- **REQUIRE CONFIRMATION** to proceed below coverage targets

---

## Phase 6: Document As-Is Architecture (APPROVAL GATE)

### Goal
Update architecture documentation to reflect actual implementation, including any changes made during development.

### Entry Behavior
1. Mark Phase 6 todo as `in_progress`
2. Review original Phase 0 architecture document
3. Identify deviations between planned and actual implementation

### As-Built Documentation

**Update Architecture Document With**:
1. **What Changed**: List differences from original plan
2. **Why Changes Were Made**: Rationale for each deviation
3. **Design Decisions During Implementation**: Choices made while coding
4. **Lessons Learned**: What we'd do differently next time
5. **Updated Diagrams**: Reflect actual implementation
6. **Integration Details**: Actual flow, message patterns, data structures

**Two-in-the-Box Approach**:
- Walk through changes: "During implementation, we changed [X] to [Y] because [Z]. Does that accurately capture the decision?"
- Verify completeness: "Are there any other design decisions we made that should be documented?"
- Ensure clarity: "Will this architecture doc make sense to someone picking up this feature in 6 months?"

### Exit Criteria (STRICT - MUST BE MET)

- ✅ Architecture document updated with as-built reality
- ✅ All deviations from Phase 0 plan documented with rationale
- ✅ Design decisions made during coding documented
- ✅ Diagrams updated to match actual implementation
- ✅ User has reviewed as-built documentation
- ✅ **EXPLICIT APPROVAL RECEIVED**: User must say "approve as-built docs" or "approved" or "documentation looks good"

### Blocking Behavior

**CRITICAL**: Do NOT proceed to Phase 7 until explicit approval is received. If user tries to skip:
- **STOP**: "Phase 6 requires your approval of the as-built architecture documentation before we proceed to final validation."
- **EXPLAIN**: "This documentation is critical for the next Claude Code session to have accurate context."
- **WAIT**: Pause and wait for approval

---

## Phase 7: Architecture Doc Agent Finalization

### Goal
Validate architecture documentation accuracy and completeness through specialized agents.

### Entry Behavior
1. Mark Phase 7 todo as `in_progress`
2. **AUTO-LAUNCH architecture-doc-keeper agent**:
   ```
   Use Task tool with subagent_type=architecture-doc-keeper
   Prompt: "Validate architecture documentation for feature [name]:
           - Verify docs match actual code implementation
           - Check for inconsistencies between description and reality
           - Validate all diagrams are current and accurate
           - Ensure all components are properly documented
           Files to check: working/{feature-name}-architecture.md and related code"
   ```
3. **AUTO-LAUNCH documentation-product-engineer agent**:
   ```
   Use Task tool with subagent_type=documentation-product-engineer
   Prompt: "Review architecture documentation for quality and clarity:
           - Is it clear for new engineers?
           - Are examples complete?
           - Are technical details accurate?
           - Does it follow documentation standards?
           File: working/{feature-name}-architecture.md"
   ```

### Review and Finalization

**After agents complete**:
1. **SUMMARIZE** findings from both agents
2. **DISCUSS** with user: "The agents found [X] issues. Most important: [Y]. Should we address all of them?"
3. **APPLY** feedback collaboratively
4. **UPDATE** documentation based on agent recommendations

### Exit Criteria (STRICT - MUST BE MET)

- ✅ architecture-doc-keeper validation passed
- ✅ documentation-product-engineer review passed
- ✅ All critical feedback addressed
- ✅ Documentation complete, accurate, and ready for next session
- ✅ Phase 7 todo marked completed
- ✅ Progress tracker updated with "COMPLETE" status

### Completion

Once Phase 7 exits successfully:
1. **CONGRATULATE** user: "Feature [name] is complete and fully documented! All 8 phases finished."
2. **SUMMARIZE** deliverables:
   - Code implemented and tested
   - Architecture documented (before and after)
   - [X]% test coverage achieved
   - All quality gates passed
3. **UPDATE** progress tracker with final summary
4. **SUGGEST** next steps: "Would you like to commit this work, or is there anything else to refine?"

---

## Context Loss Recovery

### If Session Resumes Mid-Feature

**When you detect an incomplete feature** (progress tracker exists but feature not complete):

1. **READ** `working/{feature-name}-progress.md`
2. **IDENTIFY** current phase from progress tracker
3. **INFORM** user: "I've detected we're in the middle of feature [name], currently at Phase [N]: [description]. Progress tracker shows: [summary]."
4. **ASK**: "Should we resume where we left off, or restart from a different phase?"
5. **RESUME** from indicated phase using this skill

### If Architecture Doc is Missing

**If you detect coding activity but no architecture doc**:
1. **STOP** immediately
2. **ACTIVATE** this skill
3. **INFORM**: "No Phase 0 architecture document found for this work. We need to create one before proceeding."
4. **OFFER OPTIONS**:
   - "Create Phase 0 architecture doc retroactively based on existing code (then proceed to testing)"
   - "Start fresh with proper Phase 0 documentation"
5. **PROCEED** based on user choice

---

## Paired Programming Guidelines

### Two-in-the-Box Collaboration

Throughout all phases, engage in collaborative development:

**Ask Questions**:
- "I'm considering approach [X]. What do you think?"
- "Should we prioritize [A] or [B] for this feature?"
- "Does this design align with your vision?"

**Explain Reasoning**:
- "I'm suggesting [X] because [Y and Z]"
- "This pattern has trade-off [A] vs [B]"
- "Based on the codebase, approach [X] seems consistent with existing patterns"

**Invite Feedback**:
- "Do you see any issues with this approach?"
- "Am I missing any edge cases?"
- "Is there a simpler way to accomplish this?"

**Document Decisions**:
- Capture discussion outcomes in progress tracker
- Record rationale in architecture doc
- Note alternatives considered and why they were rejected

**Catch Issues Together**:
- "I notice [potential issue]. Should we address this now?"
- "This might be a problem if [scenario]. Have you considered that?"
- "The architecture doc says [X] but we're implementing [Y]. Which is correct?"

---

## Integration with Existing Guides

This skill references and coordinates with:

- **`.claude/guides/IMPLEMENTATION-WORKFLOW.md`**: Detailed phase descriptions (this skill is the executable form)
- **`.claude/guides/TESTING.md`**: Testing standards for Phases 3-5
- **`.claude/guides/ACTORS.md`**: Actor patterns for Phase 1 implementation
- **`.claude/guides/BUILD.md`**: Build commands for compilation and test execution
- **`.claude/guides/ARCHITECTURE.md`**: Architecture patterns for Phase 0
- **`.claude/styles/*.md`**: Code standards referenced during implementation

---

## Quick Reference: Phase Checklist

```
[ ] Phase 0: Architecture doc → User approval → Proceed
[ ] Phase 1: Code → Compiles → Proceed (warn if fails)
[ ] Phase 2: scala-ninja review → Apply feedback → Proceed (warn if critical issues)
[ ] Phase 3: Feature files → Scenarios complete → Proceed (warn if gaps)
[ ] Phase 4: Component tests → All pass → Proceed (warn if failures)
[ ] Phase 5: Unit tests → Coverage met → Proceed (warn if below target)
[ ] Phase 6: As-built docs → User approval → Proceed
[ ] Phase 7: Doc validation → Agents approve → Complete
```

---

## Common Scenarios

### Scenario: User Wants to Skip Testing

User: "Let's skip the tests for now and come back to them later"

**Response**:
- **ACKNOWLEDGE**: "I understand wanting to move quickly"
- **WARN**: "Skipping tests means [specific risks for this feature]"
- **SUGGEST**: "Can we at least create the feature files (Phase 3) so we know what scenarios we'll need? That takes 10 minutes and prevents us from forgetting edge cases."
- **RESPECT CHOICE**: If user insists, document in progress tracker: "Tests deferred - user decision on [date]"
- **REMIND LATER**: "We deferred tests earlier. Should we address that now or continue deferring?"

### Scenario: Implementation Reveals Architecture is Wrong

During Phase 1, you realize the architecture won't work.

**Response**:
- **STOP CODING**
- **EXPLAIN**: "I've discovered [issue]. The approved architecture assumes [X], but actually [Y]."
- **PROPOSE FIX**: "We need to change [Z] in the architecture. Specifically: [details]"
- **GO BACK**: Return to Phase 0, update architecture doc
- **GET RE-APPROVAL**: "Here's the updated architecture accounting for [discovery]. Does this look better?"
- **RESUME**: After approval, continue Phase 1

### Scenario: Tests Fail But User Wants to Proceed

Component tests fail in Phase 4, user says "proceed anyway"

**Response**:
- **CONFIRM UNDERSTANDING**: "Just to confirm: we're proceeding with [N] failing tests. This means [specific risks]."
- **DOCUMENT**: Update progress tracker: "Phase 4 completed with [N] known failures: [list]. User decision to proceed on [date]."
- **PLAN RETURN**: "Should we create a todo to fix these failures later, or consider them non-critical?"
- **PROCEED**: Move to Phase 5 as requested

---

## Success Metrics

This skill is successful when:
- ✅ No features are implemented without Phase 0 architecture documentation
- ✅ Architecture documentation survives context loss and enables session recovery
- ✅ Quality gates catch issues before they compound
- ✅ Both user and Claude contribute to better solutions through collaboration
- ✅ All 8 phases are followed for every feature
- ✅ Documentation accurately reflects as-built reality

---

## Version History

- **v1.0** (2025-10-21): Initial creation with 8-phase workflow, auto-detection, paired programming approach