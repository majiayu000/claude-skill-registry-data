---
memory_layer: durable_knowledge
para_section: pages/skills/writing-plans
gigabrain_tags: planning, implementation, project-management, task-breakdown, specification
openstinger_context: project-planning, task-decomposition, implementation-strategy
last_updated: 2026-03-30
related_docs:
  - docs/superpowers/specs/
  - docs/superpowers/plans/
related_skills:
  - brainstorming
  - executing-plans
  - subagent-driven-development
frequency_percent: 90.0
success_rate_percent: 88.0
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** This should be run in a dedicated worktree (created by brainstorming skill).

**Save plans to:** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`
- (User preferences for plan location override this default)

## When to Use This Skill

**Trigger Conditions:**
- After completing brainstorming and having an approved design specification
- When implementing multi-step features requiring detailed planning
- Before any code implementation in a clean worktree environment
- When breaking down complex requirements into executable tasks
- For projects requiring systematic, testable implementation
- When working with developers who need complete context and guidance
- After design approval but before touching any code

**Prerequisites:**
- Approved design specification from brainstorming skill
- Clean worktree environment (created by using-git-worktrees skill)
- Clear understanding of requirements and acceptance criteria

## Step-by-Step Procedure

### Step 1: Validate Prerequisites
**Before writing any plan, ensure all prerequisites are met:**

```javascript
const prerequisites = {
  approvedSpec: checkSpecApproval(specPath),
  cleanWorktree: verifyWorktreeCleanliness(),
  contextAvailable: ensureZeroContextAssumption(),
  toolsVerified: validateDevelopmentTools()
};
```

**Prerequisites Check:**
- Approved design specification from brainstorming
- Clean worktree environment (no uncommitted changes)
- Zero-context assumption (detailed documentation required)
- Development tools and environment verified

### Step 2: Perform Scope Analysis
**Analyze project scope and decomposition needs:**

```javascript
// Check if project needs decomposition
const scopeAnalysis = analyzeProjectScope(specContent);
if (scopeAnalysis.multipleSubsystems) {
  suggestSubsystemDecomposition(scopeAnalysis.subsystems);
  return; // Stop and decompose first
}
```

**Scope Validation:**
- Single responsibility principle assessment
- Independent subsystem identification
- Decomposition recommendations if needed
- Complexity evaluation for planning approach

### Step 3: Design File Structure
**Map out complete file architecture before task breakdown:**

```javascript
const fileStructure = designFileArchitecture(specRequirements, existingCodebase);

fileStructure.validateResponsibilities();
fileStructure.checkBoundaries();
fileStructure.assessTestability();
```

**File Structure Design:**
- Clear responsibility assignment per file
- Well-defined interfaces between components
- Testability assessment for each unit
- Following established codebase patterns

### Step 4: Create Plan Document Framework
**Set up the standardized plan document structure:**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (\`- [ ]\`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

**Document Framework:**
- Standardized header with execution guidance
- Clear goal and architecture statements
- Technology stack identification
- Agent execution instructions

### Step 5: Break Down into Bite-Sized Tasks
**Decompose into 2-5 minute executable tasks:**

```javascript
const tasks = decomposeIntoTasks(specRequirements, fileStructure);

tasks.forEach(task => {
  task.validateGranularity(); // Each task 2-5 minutes
  task.ensureTestability();  // Must be independently testable
  task.checkDependencies();  // Clear prerequisite identification
});
```

**Task Granularity Rules:**
- Each task represents one complete, testable change
- 2-5 minute execution time per task
- Independent execution capability
- Clear success/failure criteria

### Step 6: Document Complete Implementation Details
**Provide zero-context implementation guidance:**

```javascript
for (const task of tasks) {
  // Document exact file paths
  task.files = identifyExactFilePaths(task.changes);
  
  // Provide complete code implementations
  task.implementation = writeCompleteCode(task.requirements);
  
  // Include test code and commands
  task.tests = writeFailingTests(task.requirements);
  task.commands = generateExactCommands(task.changes);
}
```

**Complete Documentation:**
- Exact file paths for all changes
- Complete code implementations (not references)
- Failing test code with exact assertions
- Precise command-line instructions with expected output

### Step 7: Execute Plan Review Loop
**Automated quality assurance through subagent review:**

```javascript
// Dispatch plan reviewer subagent
const reviewResult = await dispatchPlanReviewer(planDocument, specDocument);

let iterations = 0;
while (reviewResult.status !== 'approved' && iterations < 3) {
  // Fix identified issues
  applyReviewFixes(reviewResult.issues);
  
  // Re-dispatch for review
  reviewResult = await dispatchPlanReviewer(planDocument, specDocument);
  iterations++;
}

if (iterations >= 3) {
  await requestHumanReview(reviewResult);
}
```

**Review Process:**
- Automated plan quality assessment
- Maximum 3 fix iterations before human escalation
- Preserves original author context for fixes
- Advisory review with option to dispute

### Step 8: Present Execution Options
**Offer choice between execution approaches:**

```javascript
const executionOptions = {
  subagentDriven: {
    description: 'Fresh subagent per task with inter-task review',
    skill: 'subagent-driven-development',
    advantages: ['Parallel execution', 'Independent task validation']
  },
  inlineExecution: {
    description: 'Batch execution with checkpoints',
    skill: 'executing-plans', 
    advantages: ['Single session continuity', 'Faster for small plans']
  }
};

// Present options to user
await presentExecutionChoice(executionOptions);
```

**Execution Choice:**
- Subagent-driven for complex, multi-step plans
- Inline execution for simpler, faster implementation
- Clear guidance on when to use each approach

### Step 9: Save and Commit Plan
**Store plan in standardized location with proper versioning:**

```bash
# Generate plan filename
PLAN_FILENAME="docs/superpowers/plans/$(date +%Y-%m-%d)-${FEATURE_NAME// /-}.md"

# Save plan document
savePlanDocument(planContent, PLAN_FILENAME);

# Commit to version control
git add "$PLAN_FILENAME"
git commit -m "docs: add implementation plan for ${FEATURE_NAME}

- Based on approved spec: ${SPEC_PATH}
- ${NUM_TASKS} bite-sized tasks
- Ready for execution via ${EXECUTION_SKILL}"
```

**Plan Archival:**
- Standardized naming convention
- Git versioning for plan evolution
- Link to source specification
- Execution method documentation

### Step 10: Transition to Execution
**Hand off to appropriate execution skill:**

```javascript
// Route to selected execution approach
if (userChoice === 'subagent-driven') {
  await invokeSkill('subagent-driven-development', {
    planPath: PLAN_FILENAME,
    specPath: SPEC_PATH
  });
} else {
  await invokeSkill('executing-plans', {
    planPath: PLAN_FILENAME,
    specPath: SPEC_PATH
  });
}
```

**Clean Handoff:**
- Complete context transfer to execution skill
- Clear success criteria communication
- No implementation work in planning phase

## Cross-References

### Related Procedures
- [Brainstorming Skill](skills/brainstorming/SKILL.md) - Design phase prerequisite
- [Executing Plans Skill](skills/executing-plans/SKILL.md) - Inline execution option
- [Subagent Driven Development Skill](skills/subagent-driven-development/SKILL.md) - Recommended execution approach

### Related Skills
- `brainstorming` - Design and specification phase
- `executing-plans` - Inline plan execution
- `subagent-driven-development` - Recommended execution method
- `using-git-worktrees` - Isolated development environment

### Related Agents
- `DevForge_AI_Team` - Plan creation and validation
- `QualityForge_AI_Team` - Plan review and quality assurance
