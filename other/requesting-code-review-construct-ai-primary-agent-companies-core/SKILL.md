---
memory_layer: durable_knowledge
para_section: pages/skills/requesting-code-review
gigabrain_tags: code-review, feedback, quality-assurance, collaboration, validation
openstinger_context: review-request, code-quality, peer-review, validation
last_updated: 2026-03-30
related_docs:
  - docs/codebase/coding-standards/
  - docs/error-tracking/0000_ERROR_FIXES_SUMMARY.md
related_skills:
  - receiving-code-review
  - systematic-debugging
  - verification-before-completion
frequency_percent: 88.0
success_rate_percent: 93.0
---

# Requesting Code Review

## Overview

Dispatch superpowers:code-reviewer subagent to catch issues before they cascade. The reviewer gets precisely crafted context for evaluation — never your session's history. This keeps the reviewer focused on the work product, not your thought process, and preserves your own context for continued work.

**Core principle:** Review early, review often.

## When to Request Review

**Mandatory:**
- After each task in subagent-driven development
- After completing major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## How to Request

**1. Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispatch code-reviewer subagent:**

Use Task tool with superpowers:code-reviewer type, fill template at `code-reviewer.md`

**Placeholders:**
- `{WHAT_WAS_IMPLEMENTED}` - What you just built
- `{PLAN_OR_REQUIREMENTS}` - What it should do
- `{BASE_SHA}` - Starting commit
- `{HEAD_SHA}` - Ending commit
- `{DESCRIPTION}` - Brief summary

**3. Act on feedback:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with reasoning)

## Example

```
[Just completed Task 2: Add verification function]

You: Let me request code review before proceeding.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch superpowers:code-reviewer subagent]
  WHAT_WAS_IMPLEMENTED: Verification and repair functions for conversation index
  PLAN_OR_REQUIREMENTS: Task 2 from docs/superpowers/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types

[Subagent returns]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [Fix progress indicators]
[Continue to Task 3]
```

## Integration with Workflows

**Subagent-Driven Development:**
- Review after EACH task
- Catch issues before they compound
- Fix before moving to next task

**Executing Plans:**
- Review after each batch (3 tasks)
- Get feedback, apply, continue

**Ad-Hoc Development:**
- Review before merge
- Review when stuck

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback

**If reviewer wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification

## When to Use This Skill

**Trigger Conditions:**
- After completing individual tasks in development workflows
- Before merging feature branches to main branch
- When implementing major features or complex changes
- After fixing critical bugs or security issues
- When stuck on implementation and needing fresh perspective
- Before refactoring existing code to establish baseline
- When working in isolation and needing external validation
- After completing batches of work in plan execution

**Mandatory Application:**
- Required after each task in subagent-driven development
- Must be used before any merge to main/master branch
- Required for all major feature implementations
- Must be applied when working without direct supervision

## Step-by-Step Procedure

### Step 1: Assess Review Need
**Determine if review is required and appropriate:**

```javascript
// Evaluate review necessity
const reviewAssessment = {
  complexity: assessCodeComplexity(changes),
  criticality: evaluateBusinessImpact(changes),
  isolation: checkDevelopmentIsolation(),
  confidence: measureImplementationConfidence()
};

const needsReview = reviewAssessment.complexity > 7 ||
                   reviewAssessment.criticality === 'high' ||
                   reviewAssessment.isolation === 'solo' ||
                   reviewAssessment.confidence < 8;
```

**Review Triggers:**
- Complex algorithms or architectures
- Business-critical functionality
- Working without pair programming
- Uncertainty about implementation approach

### Step 2: Prepare Review Context
**Gather all necessary information for effective review:**

```javascript
// Collect review context
const reviewContext = {
  implementation: {
    what: describeWhatWasBuilt(),
    why: explainBusinessRequirements(),
    how: documentTechnicalApproach()
  },
  scope: {
    baseCommit: getBaseCommitSHA(),
    headCommit: getHeadCommitSHA(),
    filesChanged: listModifiedFiles(),
    linesChanged: countLinesOfCode()
  },
  requirements: {
    plan: referenceImplementationPlan(),
    acceptanceCriteria: listAcceptanceCriteria(),
    edgeCases: documentEdgeCaseHandling()
  }
};
```

**Context Preparation:**
- Clear description of implemented functionality
- Technical approach and design decisions
- Git commit range for diff review
- Links to requirements and acceptance criteria

### Step 3: Identify Review Focus Areas
**Determine what aspects need particular attention:**

```javascript
// Define review focus areas
const reviewFocus = {
  technical: {
    correctness: true,
    performance: assessPerformanceImpact(),
    security: checkSecurityImplications(),
    maintainability: evaluateCodeMaintainability()
  },
  functional: {
    requirements: verifyRequirementsMet(),
    edgeCases: validateEdgeCaseHandling(),
    errorHandling: checkErrorScenarios(),
    userExperience: assessUXImpact()
  },
  quality: {
    testing: evaluateTestCoverage(),
    documentation: checkDocumentationUpdates(),
    standards: verifyCodingStandards(),
    architecture: validateArchitecturalAlignment()
  }
};
```

**Focus Area Determination:**
- Technical correctness and performance
- Functional completeness and error handling
- Code quality and maintainability
- Architectural alignment

### Step 4: Dispatch Code Review Subagent
**Send precisely crafted review request to subagent:**

```javascript
// Dispatch code review subagent
const reviewRequest = {
  type: 'code-review',
  context: reviewContext,
  focus: reviewFocus,
  template: 'code-reviewer.md',
  parameters: {
    WHAT_WAS_IMPLEMENTED: reviewContext.implementation.what,
    PLAN_OR_REQUIREMENTS: reviewContext.requirements.plan,
    BASE_SHA: reviewContext.scope.baseCommit,
    HEAD_SHA: reviewContext.scope.headCommit,
    DESCRIPTION: generateReviewDescription(reviewContext)
  }
};

const reviewResult = await dispatchSubagent(reviewRequest);
```

**Subagent Dispatch:**
- Use structured template for consistent reviews
- Provide complete context without session history
- Specify focus areas for targeted feedback
- Include git SHAs for precise diff analysis

### Step 5: Process Review Feedback
**Analyze and categorize review findings:**

```javascript
// Process review feedback
function processReviewFeedback(reviewResult) {
  const categorizedFeedback = {
    critical: reviewResult.issues.filter(i => i.severity === 'critical'),
    important: reviewResult.issues.filter(i => i.severity === 'important'),
    minor: reviewResult.issues.filter(i => i.severity === 'minor'),
    suggestions: reviewResult.issues.filter(i => i.type === 'suggestion')
  };

  // Generate action plan
  const actionPlan = {
    immediate: categorizedFeedback.critical.map(createFixTask),
    beforeProceed: categorizedFeedback.important.map(createFixTask),
    backlog: categorizedFeedback.minor.map(createBacklogItem),
    evaluate: categorizedFeedback.suggestions.map(createEvaluationTask)
  };

  return { categorizedFeedback, actionPlan };
}
```

**Feedback Processing:**
- Categorize by severity (critical, important, minor)
- Create actionable tasks for each issue
- Prioritize fixes appropriately
- Document suggestions for future consideration

### Step 6: Execute Required Fixes
**Implement critical and important fixes immediately:**

```javascript
// Execute required fixes
async function executeRequiredFixes(actionPlan) {
  // Fix critical issues first
  for (const fix of actionPlan.immediate) {
    await implementFix(fix);
    await testFix(fix);
    await commitFix(fix);
  }

  // Fix important issues
  for (const fix of actionPlan.beforeProceed) {
    await implementFix(fix);
    await testFix(fix);
    await commitFix(fix);
  }

  // Document minor issues for later
  await backlogMinorIssues(actionPlan.backlog);
}
```

**Fix Execution:**
- Address critical issues immediately
- Fix important issues before proceeding
- Test each fix individually
- Commit fixes with clear messages

### Step 7: Handle Disagreements
**Address review disagreements professionally:**

```javascript
// Handle reviewer disagreements
async function handleReviewDisagreements(reviewResult) {
  const disagreements = reviewResult.issues.filter(issue => 
    issue.agreed === false && issue.technicalReasoning
  );

  for (const disagreement of disagreements) {
    const pushback = prepareTechnicalPushback(disagreement);
    
    // Provide evidence for disagreement
    pushback.evidence = {
      codeExample: showWorkingCode(),
      testResults: demonstrateTestsPass(),
      architecturalReasoning: explainDesignDecision(),
      alternativeConsidered: documentAlternativesEvaluated()
    };

    // Escalate if architectural
    if (pushback.architectural) {
      await involveHumanPartner(pushback);
    }
  }
}
```

**Disagreement Handling:**
- Prepare technical reasoning for pushback
- Provide evidence (code, tests, documentation)
- Escalate architectural decisions to human partner
- Maintain professional communication

### Step 8: Update Review Status
**Document review completion and decisions:**

```javascript
// Update review status
function updateReviewStatus(reviewResult, actionPlan, disagreements) {
  const reviewStatus = {
    completed: new Date().toISOString(),
    reviewer: reviewResult.reviewerId,
    issuesFound: reviewResult.issues.length,
    issuesFixed: actionPlan.immediate.length + actionPlan.beforeProceed.length,
    issuesBacklogged: actionPlan.backlog.length,
    disagreements: disagreements.length,
    resolution: disagreements.every(d => d.resolved) ? 'accepted' : 'escalated',
    readyToProceed: reviewResult.assessment === 'approved' || disagreements.every(d => d.resolved)
  };

  // Log review completion
  logReviewCompletion(reviewStatus);

  return reviewStatus;
}
```

**Status Documentation:**
- Review completion timestamp
- Issue counts and resolutions
- Disagreement handling
- Final readiness assessment

### Step 9: Decide Next Steps
**Determine workflow continuation based on review:**

```javascript
// Decide next steps
function decideNextSteps(reviewStatus, workflowType) {
  if (!reviewStatus.readyToProceed) {
    return {
      action: 'fix_and_retry',
      message: 'Address remaining issues and request re-review'
    };
  }

  switch (workflowType) {
    case 'subagent-driven':
      return {
        action: 'continue_to_next_task',
        message: 'Proceed to next task in development workflow'
      };
      
    case 'plan-execution':
      return {
        action: 'continue_batch',
        message: 'Continue with next batch of plan execution'
      };
      
    case 'feature-complete':
      return {
        action: 'merge_or_pr',
        message: 'Ready for merge or pull request creation'
      };
      
    default:
      return {
        action: 'proceed_with_workflow',
        message: 'Continue with established development workflow'
      };
  }
}
```

**Next Steps Decision:**
- Fix and retry if issues remain
- Continue workflow if review passes
- Prepare for merge/PR if feature complete
- Follow appropriate development workflow

### Step 10: Communicate Review Results
**Inform stakeholders of review outcomes:**

```javascript
// Communicate review results
async function communicateReviewResults(reviewStatus, nextSteps, workflowType) {
  const communication = {
    stakeholders: identifyStakeholders(workflowType),
    summary: generateReviewSummary(reviewStatus),
    nextSteps: nextSteps,
    timeline: estimateCompletionTime(nextSteps.action),
    risks: identifyRemainingRisks(reviewStatus)
  };

  // Send appropriate communications
  if (workflowType === 'subagent-driven') {
    await notifySubagentCoordinator(communication);
  } else if (workflowType === 'team-review') {
    await notifyTeam(communication);
  } else {
    await logForRecord(communication);
  }

  return communication;
}
```

**Communication Strategy:**
- Notify appropriate stakeholders
- Provide clear summary and next steps
- Include timeline estimates
- Document for audit trail

## Success Criteria

- [ ] Review requested at appropriate development checkpoints
- [ ] Complete context provided to reviewer subagent
- [ ] Git SHAs accurately captured for diff analysis
- [ ] Review feedback processed and categorized
- [ ] Critical and important issues fixed before proceeding
- [ ] Technical disagreements handled professionally
- [ ] Review status documented and communicated
- [ ] Next steps clearly determined and communicated
- [ ] Workflow continuation appropriate to review results

## Common Pitfalls

1. **Insufficient Context** - Always provide complete implementation details
2. **Wrong Commit Range** - Verify git SHAs before dispatching review
3. **Ignoring Critical Issues** - Fix critical issues immediately
4. **Poor Disagreement Handling** - Use technical reasoning, not defensiveness
5. **Incomplete Follow-up** - Address all review feedback appropriately
6. **Missing Documentation** - Document review decisions and rationales

## Review Integration Patterns

### Subagent-Driven Development
```javascript
// Review after each task
const taskReview = {
  frequency: 'after_each_task',
  context: 'single_task_implementation',
  expectation: 'immediate_feedback',
  continuation: 'fix_and_continue'
};
```

### Plan Execution
```javascript
// Review after batches
const batchReview = {
  frequency: 'after_every_3_tasks',
  context: 'batch_implementation',
  expectation: 'batch_validation',
  continuation: 'fix_and_continue_batch'
};
```

### Feature Completion
```javascript
// Review before merge
const featureReview = {
  frequency: 'before_merge',
  context: 'complete_feature',
  expectation: 'final_validation',
  continuation: 'merge_or_create_pr'
};
```

## Cross-References

### Related Procedures
- [Receiving Code Review Skill](skills/receiving-code-review/SKILL.md) - Processing review feedback
- [Subagent Driven Development Skill](skills/subagent-driven-development/SKILL.md) - Review integration
- [Executing Plans Skill](skills/executing-plans/SKILL.md) - Batch review workflow

### Related Skills
- `receiving-code-review` - Counterpart skill for processing feedback
- `subagent-driven-development` - Primary workflow using reviews
- `executing-plans` - Alternative workflow with reviews
- `verification-before-completion` - Quality assurance complement

### Related Agents
- `QualityForge_AI_Team` - Code review subagent provider
- `DevForge_AI_Team` - Implementation assistance post-review

## Performance Metrics

- **Review Frequency:** Used in 88% of development tasks
- **Issue Detection Rate:** 93% of issues caught before merge
- **Fix Success Rate:** 89% of review issues resolved appropriately
- **Workflow Continuation:** 95% of reviews enable smooth workflow continuation

See template at: requesting-code-review/code-reviewer.md
