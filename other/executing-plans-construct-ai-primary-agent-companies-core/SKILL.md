---
memory_layer: durable_knowledge
para_section: pages/skills/executing-plans
gigabrain_tags: execution, implementation, project-management, task-execution, plan-following
openstinger_context: plan-execution, task-implementation, development-workflow
last_updated: 2026-03-30
related_docs:
  - docs/superpowers/plans/
  - docs/superpowers/specs/
related_skills:
  - writing-plans
  - finishing-a-development-branch
  - verification-before-completion
frequency_percent: 78.0
success_rate_percent: 89.0
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks, report when complete.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

**Note:** Tell your human partner that Superpowers works much better with access to subagents. The quality of its work will be significantly higher if run on a platform with subagent support (such as Claude Code or Codex). If subagents are available, use superpowers:subagent-driven-development instead of this skill.

## The Process

### Step 1: Load and Review Plan
1. Read plan file
2. Review critically - identify any questions or concerns about the plan
3. If concerns: Raise them with your human partner before starting
4. If no concerns: Create TodoWrite and proceed

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

### Step 3: Complete Development

After all tasks complete and verified:
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use superpowers:finishing-a-development-branch
- Follow that skill to verify tests, present options, execute choice

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Stop when blocked, don't guess
- Never start implementation on main/master branch without explicit user consent

## When to Use This Skill

**Trigger Conditions:**
- After a comprehensive implementation plan has been created using writing-plans skill
- When executing multi-step implementation in a structured, reviewable manner
- When working in an isolated development environment (git worktree)
- When plan requires systematic task execution with verification checkpoints
- When implementation involves multiple files, components, or complex logic
- When working without subagent support (use subagent-driven-development if available)
- After plan review and approval from human partner
- When following a detailed, bite-sized task breakdown

**Prerequisites:**
- Approved implementation plan from writing-plans skill
- Clean worktree environment (not main/master branch)
- Understanding of plan requirements and acceptance criteria
- Access to development environment and tools

## Step-by-Step Procedure

### Step 1: Plan Loading and Critical Review
**Load and thoroughly analyze the implementation plan:**

```javascript
// Plan loading and validation
const planDocument = loadPlanDocument(planPath);
const planValidation = validatePlanStructure(planDocument);

if (!planValidation.isValid) {
  reportPlanIssues(planValidation.issues);
  await requestPlanClarification(planValidation.issues);
  return; // Stop until plan is fixed
}

// Critical review checklist
const reviewChecklist = {
  clearObjectives: planDocument.goal !== undefined,
  biteSizedTasks: planDocument.tasks.every(task => task.estimatedTime <= 5),
  testableSteps: planDocument.tasks.every(task => task.verification !== undefined),
  completeContext: planDocument.assumptions !== undefined,
  errorHandling: planDocument.riskAssessment !== undefined
};

if (!reviewChecklist.allMet) {
  await raisePlanConcerns(reviewChecklist.failedItems);
  return; // Stop until concerns addressed
}
```

**Critical Review Points:**
- Plan objectives are clear and achievable
- Tasks are appropriately sized (2-5 minutes each)
- Each task has clear verification criteria
- All assumptions and dependencies are documented
- Risk assessment and error handling included

### Step 2: Environment Preparation
**Set up isolated development environment:**

```bash
# Verify worktree environment (REQUIRED)
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" == "main" || "$CURRENT_BRANCH" == "master" ]]; then
  echo "ERROR: Cannot execute plans on main/master branch"
  echo "Use using-git-worktrees skill to create isolated environment"
  exit 1
fi

# Verify clean working directory
if [[ -n $(git status --porcelain) ]]; then
  echo "ERROR: Working directory not clean"
  echo "Commit or stash changes before starting plan execution"
  exit 1
fi

# Set up execution tracking
EXECUTION_LOG="plan-execution-$(date +%Y%m%d-%H%M%S).log"
echo "Starting plan execution: $(date)" > "$EXECUTION_LOG"
echo "Plan: $PLAN_PATH" >> "$EXECUTION_LOG"
echo "Worktree: $CURRENT_BRANCH" >> "$EXECUTION_LOG"
```

**Environment Requirements:**
- Isolated worktree (not main/master)
- Clean working directory
- All required tools and dependencies available
- Execution tracking initialized

### Step 3: Task Execution Loop
**Execute each task systematically with verification:**

```javascript
// Task execution loop
for (const task of planDocument.tasks) {
  console.log(`Starting Task ${task.id}: ${task.title}`);
  
  // Mark task as in progress
  updateTaskStatus(task.id, 'in_progress');
  
  try {
    // Execute each step in the task
    for (const step of task.steps) {
      console.log(`Executing: ${step.description}`);
      
      // Execute the step (follow plan instructions exactly)
      const stepResult = await executeStep(step);
      
      if (!stepResult.success) {
        throw new Error(`Step failed: ${stepResult.error}`);
      }
      
      // Run step verification if specified
      if (step.verification) {
        const verificationResult = await runVerification(step.verification);
        if (!verificationResult.success) {
          throw new Error(`Verification failed: ${verificationResult.error}`);
        }
      }
    }
    
    // Mark task as completed
    updateTaskStatus(task.id, 'completed');
    logTaskCompletion(task.id, Date.now());
    
  } catch (error) {
    // Handle task failure
    updateTaskStatus(task.id, 'failed');
    logTaskFailure(task.id, error.message);
    
    // Stop execution and seek guidance
    await reportTaskFailure(task.id, error.message);
    await requestExecutionGuidance(task.id, error.message);
    return; // Stop until guidance received
  }
}
```

**Task Execution Principles:**
- Follow plan instructions exactly (no improvisation)
- Execute one task at a time
- Run all specified verifications
- Stop immediately on any failure
- Document all execution results

### Step 4: Inter-Task Verification
**Verify work between tasks to catch issues early:**

```javascript
// Inter-task verification
function performInterTaskVerification(completedTasks, planDocument) {
  const verifications = [
    // Build verification
    { name: 'build', command: 'npm run build', required: true },
    
    // Test verification
    { name: 'tests', command: 'npm test', required: true },
    
    // Linting verification
    { name: 'lint', command: 'npm run lint', required: false },
    
    // Integration verification (if applicable)
    { name: 'integration', command: planDocument.integrationTests, required: planDocument.hasIntegrationTests }
  ];

  for (const verification of verifications) {
    if (verification.required) {
      console.log(`Running ${verification.name} verification...`);
      const result = await runCommand(verification.command);
      
      if (!result.success) {
        throw new Error(`${verification.name} verification failed: ${result.error}`);
      }
      
      logVerificationResult(verification.name, result);
    }
  }
}
```

**Verification Types:**
- Build verification (ensure code compiles)
- Test verification (ensure tests pass)
- Linting verification (code quality)
- Integration verification (end-to-end functionality)

### Step 5: Handle Execution Blockers
**Systematically address and resolve blockers:**

```javascript
// Blocker resolution protocol
async function handleExecutionBlocker(blocker) {
  const blockerAnalysis = analyzeBlocker(blocker);
  
  switch (blockerAnalysis.type) {
    case 'missing_dependency':
      await resolveMissingDependency(blockerAnalysis.details);
      break;
      
    case 'test_failure':
      await diagnoseTestFailure(blockerAnalysis.details);
      break;
      
    case 'unclear_instruction':
      await requestInstructionClarification(blockerAnalysis.details);
      break;
      
    case 'environmental_issue':
      await resolveEnvironmentIssue(blockerAnalysis.details);
      break;
      
    default:
      await escalateBlockerToHuman(blockerAnalysis);
  }
}

// Never guess or work around blockers
function analyzeBlocker(blocker) {
  return {
    type: categorizeBlocker(blocker),
    details: extractBlockerDetails(blocker),
    severity: assessBlockerSeverity(blocker),
    resolution_options: suggestResolutionOptions(blocker)
  };
}
```

**Blocker Resolution:**
- Missing dependencies: Install and verify
- Test failures: Diagnose and fix root cause
- Unclear instructions: Request clarification
- Environmental issues: Resolve setup problems

### Step 6: Progress Tracking and Reporting
**Maintain detailed execution tracking:**

```javascript
// Progress tracking system
class ExecutionTracker {
  constructor(planDocument) {
    this.plan = planDocument;
    this.startTime = Date.now();
    this.taskProgress = new Map();
    this.blockers = [];
    this.verifications = [];
  }

  updateProgress(taskId, status, details) {
    this.taskProgress.set(taskId, { status, timestamp: Date.now(), details });
    this.saveProgress();
  }

  reportProgress() {
    const completedTasks = Array.from(this.taskProgress.values()).filter(t => t.status === 'completed').length;
    const totalTasks = this.plan.tasks.length;
    const progressPercent = (completedTasks / totalTasks) * 100;
    
    return {
      completed: completedTasks,
      total: totalTasks,
      percentage: progressPercent,
      estimatedTimeRemaining: this.calculateTimeRemaining(),
      blockers: this.blockers.length,
      lastUpdate: new Date().toISOString()
    };
  }

  calculateTimeRemaining() {
    const completedTasks = Array.from(this.taskProgress.values()).filter(t => t.status === 'completed');
    const avgTaskTime = completedTasks.reduce((sum, task) => sum + task.details.duration, 0) / completedTasks.length;
    const remainingTasks = this.plan.tasks.length - completedTasks.length;
    
    return avgTaskTime * remainingTasks;
  }
}
```

**Progress Tracking:**
- Task completion status
- Time estimates and actuals
- Blocker documentation
- Verification results

### Step 7: Plan Completion and Handoff
**Complete execution and hand off to finishing skill:**

```javascript
// Plan completion verification
async function completePlanExecution(planDocument, executionTracker) {
  // Final comprehensive verification
  const finalVerification = await performFinalVerification(planDocument);
  
  if (!finalVerification.success) {
    throw new Error(`Final verification failed: ${finalVerification.error}`);
  }

  // Generate completion report
  const completionReport = {
    planPath: planDocument.path,
    totalTasks: planDocument.tasks.length,
    completedTasks: executionTracker.reportProgress().completed,
    executionTime: Date.now() - executionTracker.startTime,
    blockersEncountered: executionTracker.blockers.length,
    finalVerification: finalVerification,
    readyForIntegration: true
  };

  // Log completion
  logPlanCompletion(completionReport);

  // Announce completion and handoff
  console.log("🎉 Plan execution complete!");
  console.log("Using finishing-a-development-branch skill to complete work...");
  
  // REQUIRED: Hand off to finishing skill
  await invokeSkill('finishing-a-development-branch', {
    planPath: planDocument.path,
    completionReport: completionReport
  });
}
```

**Completion Requirements:**
- All tasks completed successfully
- Final verification passed
- Comprehensive completion report
- Clean handoff to finishing skill

### Step 8: Execution Review and Lessons Learned
**Document execution insights for future improvement:**

```javascript
// Execution review and documentation
function performExecutionReview(planDocument, executionTracker) {
  const review = {
    planQuality: assessPlanQuality(planDocument, executionTracker),
    executionEfficiency: calculateExecutionEfficiency(executionTracker),
    blockerAnalysis: analyzeBlockers(executionTracker.blockers),
    improvementSuggestions: generateImprovementSuggestions(planDocument, executionTracker),
    skillEffectiveness: evaluateSkillUsage(planDocument)
  };

  // Store review for future plan improvement
  saveExecutionReview(review);
  
  return review;
}

// Key metrics for review
function assessPlanQuality(plan, tracker) {
  return {
    taskGranularity: calculateAverageTaskTime(tracker),
    verificationCompleteness: calculateVerificationCoverage(plan, tracker),
    blockerPrevention: assessBlockerPrevention(plan, tracker),
    clarityOfInstructions: evaluateInstructionClarity(plan, tracker)
  };
}
```

**Review Categories:**
- Plan quality assessment
- Execution efficiency metrics
- Blocker analysis and prevention
- Skill effectiveness evaluation
- Future improvement suggestions

## Success Criteria

- [ ] Plan loaded and critically reviewed before execution
- [ ] Isolated worktree environment verified
- [ ] All tasks executed in specified order
- [ ] Each task verified according to plan specifications
- [ ] Inter-task verifications completed successfully
- [ ] All blockers resolved with proper escalation
- [ ] Progress tracked and reported throughout execution
- [ ] Final verification passed before completion
- [ ] Clean handoff to finishing-a-development-branch skill
- [ ] Execution review completed and documented

## Common Pitfalls

1. **Starting Without Plan Review** - Always review plan critically first
2. **Working on Main Branch** - Never execute plans on main/master
3. **Skipping Verifications** - Run all specified verifications
4. **Guessing Around Blockers** - Stop and seek clarification
5. **Incomplete Task Execution** - Follow each step exactly
6. **Poor Progress Tracking** - Maintain detailed execution logs
7. **Premature Completion Claims** - Use finishing skill for final verification

## Execution Environment Requirements

### Git Worktree Setup
```bash
# Create isolated worktree (REQUIRED)
git worktree add ../worktree-name feature-branch-name
cd ../worktree-name

# Verify isolation
git branch --show-current  # Should not be main/master
git status  # Should be clean
```

### Development Environment
```bash
# Verify all required tools
node --version
npm --version
git --version

# Install dependencies
npm install

# Verify setup
npm run build
npm test
```

### Execution Tracking
```bash
# Initialize execution log
EXECUTION_LOG="execution-$(date +%Y%m%d-%H%M%S).log"
echo "Plan Execution Started: $(date)" > "$EXECUTION_LOG"
echo "Plan: $PLAN_PATH" >> "$EXECUTION_LOG"
echo "Environment: $(pwd)" >> "$EXECUTION_LOG"
```

## Cross-References

### Related Procedures
- [Writing Plans Skill](skills/writing-plans/SKILL.md) - Creates plans for execution
- [Finishing Development Branch Skill](skills/finishing-a-development-branch/SKILL.md) - Completes work after execution
- [Using Git Worktrees Skill](skills/using-git-worktrees/SKILL.md) - Sets up isolated environment

### Related Skills
- `writing-plans` - Plan creation prerequisite
- `finishing-a-development-branch` - Required completion skill
- `verification-before-completion` - Quality assurance integration
- `subagent-driven-development` - Preferred alternative with subagent support

### Related Agents
- `DevForge_AI_Team` - Implementation assistance during execution
- `QualityForge_AI_Team` - Verification and quality assurance
