---
name: bdd-workflow
description: Complete Behavior-Driven Development workflow coordinating SCENARIO → STEP DEFINITIONS → IMPLEMENT → REFACTOR cycle with Given/When/Then scenarios. Use when writing BDD tests or implementing features from user stories.
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# bdd-workflow

**Skill Type**: Orchestrator (BDD Workflow)
**Purpose**: Coordinate complete BDD cycle with Given/When/Then scenarios
**Prerequisites**:
- Work unit with REQ-* key (e.g., "Create scenario for <REQ-ID>")
- Requirement details available

---

## Agent Instructions

You are orchestrating the complete **Behavior-Driven Development (BDD)** workflow.

Your goal is to implement a requirement using **Given/When/Then scenarios** in pure business language while maintaining requirement traceability.

---

## Workflow

### Phase 0: Prerequisites Check

**Before starting BDD, verify**:
1. ✅ Requirement key exists (REQ-F-*, REQ-NFR-*, REQ-DATA-*)
2. ✅ Requirement details available (what to implement)
3. ✅ Working directory is a git repository
4. ✅ BDD framework available (Cucumber, Behave, etc.)

**If prerequisites missing**:
- No REQ-* key → Invoke `requirement-extraction` skill
- No requirement details → Ask user for clarification
- Not a git repo → Ask user if they want to initialize git
- No BDD framework → Ask user which framework to install

---

### Phase 1: SCENARIO (Write Given/When/Then)

**Invoke**: `write-scenario` skill

**Purpose**: Write behavior scenarios in business language

**What write-scenario does**:
- Creates feature file (e.g., `features/authentication.feature`)
- Writes scenarios in Gherkin format (Given/When/Then)
- Tags scenarios with REQ-* key in comments
- Uses pure business language (no technical jargon)
- Commits: "SCENARIO: Add scenarios for REQ-*"

**Success Criteria**: Scenarios written in business language

---

### Phase 2: STEP DEFINITIONS (Implement Test Code)

**Invoke**: `implement-step-definitions` skill

**Purpose**: Translate Given/When/Then into executable test code

**What implement-step-definitions does**:
- Creates step definition file (e.g., `steps/authentication_steps.py`)
- Implements step definitions for each Given/When/Then
- Tags steps with REQ-* key in comments
- Runs scenarios → expects FAILURE (implementation doesn't exist)
- Commits: "STEP DEF: Add step definitions for REQ-*"

**Success Criteria**: Step definitions exist, scenarios fail

---

### Phase 3: IMPLEMENT (Make Scenarios Pass)

**Invoke**: `implement-feature` skill

**Purpose**: Implement feature to make scenarios pass

**What implement-feature does**:
- Creates implementation file (e.g., `src/auth/authentication.py`)
- Implements feature code to pass scenarios
- Tags code with REQ-* key in comments
- Runs scenarios → expects SUCCESS (scenarios pass)
- Commits: "IMPLEMENT: Implement REQ-*"

**Success Criteria**: Scenarios PASS

---

### Phase 4: REFACTOR (Improve Quality + Eliminate Tech Debt)

**Invoke**: `refactor-bdd` skill

**Purpose**: Improve code quality and eliminate technical debt

**What refactor-bdd does**:
- Refactors feature implementation
- Refactors step definitions
- Eliminates tech debt (Principle #6)
- Runs scenarios → expects STILL PASSING
- Commits: "REFACTOR: Clean up REQ-*"

**Success Criteria**: Scenarios still PASS, tech debt = 0

---

## Output Format

When you complete the BDD workflow, show:

```
[BDD Workflow: <REQ-ID>]

✅ Phase 0: Prerequisites
  ✓ Requirement: <REQ-ID> (User login)
  ✓ BDD Framework: behave (Python)
  ✓ Git repository: initialized
  ✓ Working tree: clean

✅ Phase 1: SCENARIO (Write Given/When/Then)
  ✓ Created: features/authentication.feature (3 scenarios)
  ✓ Business language ✓ (no technical jargon)
  ✓ Commit: SCENARIO: Add scenarios for <REQ-ID>

✅ Phase 2: STEP DEFINITIONS (Implement Test Code)
  ✓ Created: steps/authentication_steps.py (12 step definitions)
  ✓ Scenarios running... FAILED ✓ (expected - no implementation)
  ✓ Commit: STEP DEF: Add step definitions for <REQ-ID>

✅ Phase 3: IMPLEMENT (Make Scenarios Pass)
  ✓ Created: src/auth/authentication.py
  ✓ Implemented: login() function
  ✓ Scenarios running... PASSED ✓
  ✓ Commit: IMPLEMENT: Implement <REQ-ID>

✅ Phase 4: REFACTOR (Improve Quality)
  Code Quality Improvements:
    ✓ Added type hints
    ✓ Improved step definition reusability

  Tech Debt Pruning:
    ✓ Deleted 1 unused import
    ✓ Simplified step definition logic

  ✓ Scenarios still PASSING ✓
  ✓ Commit: REFACTOR: Clean up <REQ-ID>

🎉 BDD Workflow Complete!
  Files: 3 files (authentication.feature, authentication_steps.py, authentication.py)
  Scenarios: 3 scenarios, all passing
  Step Definitions: 12 steps
  Traceability: <REQ-ID> → commit xyz789
```

---

## Homeostasis Behavior

**If prerequisites not met**:
1. **Detect**: Missing REQ-* key
2. **Signal**: "Need requirement extraction first"
3. **Claude invokes**: `requirement-extraction` skill
4. **Retry**: bdd-workflow with new REQ-*

**If scenarios fail in IMPLEMENT phase**:
1. **Detect**: Scenarios still failing after implementation
2. **Signal**: "Implementation incomplete"
3. **Claude**: Fix implementation and retry
4. **Do NOT proceed to REFACTOR** until scenarios pass

**If tech debt detected in REFACTOR phase**:
1. **Detect**: Unused code, complexity > 10, etc.
2. **Signal**: "Tech debt detected"
3. **Claude invokes**: `prune-unused-code`, `simplify-complex-code`
4. **Verify**: Tech debt eliminated before commit

---

## Prerequisites Check

Before invoking this skill, ensure:
1. ✅ Requirement key (REQ-*) exists
2. ✅ Requirement details available
3. ✅ Git repository initialized
4. ✅ BDD framework available (or can install)

If prerequisites not met:
- Missing REQ-* → Invoke `requirement-extraction` skill
- No BDD framework → Ask user which to install (Cucumber, Behave, etc.)

---

## Skills Used

This orchestrator skill invokes:
1. `write-scenario` - Write Given/When/Then scenarios
2. `implement-step-definitions` - Implement step definitions
3. `implement-feature` - Implement feature code
4. `refactor-bdd` - Refactor and eliminate tech debt
5. `detect-unused-code` - (via refactor-bdd) Detect tech debt
6. `prune-unused-code` - (via refactor-bdd) Eliminate tech debt

---

## Configuration

This skill respects configuration in `.claude/plugins.yml`:

```yaml
plugins:
  - name: "@aisdlc/code-skills"
    config:
      bdd:
        gherkin_style: "cucumber"     # cucumber | behave
        require_scenarios_for_requirements: true
        scenario_language: "en"       # Gherkin language
        include_backgrounds: true     # Use Background sections
```

---

## BDD vs TDD

**When to use BDD**:
- ✅ Requirements written as user stories
- ✅ Stakeholders want readable tests
- ✅ Integration/acceptance testing
- ✅ Business validation focus

**When to use TDD**:
- ✅ Unit testing focus
- ✅ Low-level implementation
- ✅ Technical requirements
- ✅ Developer-focused testing

**Both can coexist**: Use BDD for acceptance tests, TDD for unit tests.

---

## Next Steps

After BDD workflow completes:
1. Review scenarios with stakeholders
2. Run scenarios as part of CI/CD
3. Move to next requirement (invoke `bdd-workflow` for next REQ-*)

---

## Notes

**Why BDD workflow?**
- Business language = stakeholders can read tests
- Given/When/Then = clear specification of behavior
- Scenarios = living documentation of requirements
- Executable specs = tests ARE the specification

**BDD complements TDD**:
```
BDD: High-level behavior (user perspective)
  ↓ validates
TDD: Low-level implementation (developer perspective)
```

**Homeostasis Goal**:
```yaml
desired_state:
  scenarios_in_business_language: true
  scenarios_passing: true
  tech_debt: 0
  requirement_traceability: complete
```

**"Excellence or nothing"** 🔥
