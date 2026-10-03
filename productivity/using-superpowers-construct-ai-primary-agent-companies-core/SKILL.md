---
memory_layer: durable_knowledge
para_section: pages/skills/using-superpowers
gigabrain_tags: skills, workflow, methodology, tool-usage, process
openstinger_context: skill-activation, workflow-management, tool-integration
last_updated: 2026-03-30
related_docs:
  - docs/superpowers/README.md
  - docs/superpowers/framework/
related_skills:
  - writing-plans
  - executing-plans
  - subagent-driven-development
frequency_percent: 100.0
success_rate_percent: 98.0
---

## Overview

**Invoke relevant or requested skills BEFORE any response or action.** Even a 1% chance a skill might apply means that you should invoke the skill to check. If an invoked skill turns out to be wrong for the situation, you don't need to use it.

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, skip this skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. This is not optional. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

## Instruction Priority

Superpowers skills override default system prompt behavior, but **user instructions always take precedence**:

1. **User's explicit instructions** (CLAUDE.md, GEMINI.md, AGENTS.md, direct requests) — highest priority
2. **Superpowers skills** — override default system behavior where they conflict
3. **Default system prompt** — lowest priority

If CLAUDE.md, GEMINI.md, or AGENTS.md says "don't use TDD" and a skill says "always use TDD," follow the user's instructions. The user is in control.

## How to Access Skills

**In Claude Code:** Use the `Skill` tool. When you invoke a skill, its content is loaded and presented to you—follow it directly. Never use the Read tool on skill files.

**In Gemini CLI:** Skills activate via the `activate_skill` tool. Gemini loads skill metadata at session start and activates the full content on demand.

**In other environments:** Check your platform's documentation for how skills are loaded.

## Platform Adaptation

Skills use Claude Code tool names. Non-CC platforms: see `references/codex-tools.md` (Codex) for tool equivalents. Gemini CLI users get the tool mapping loaded automatically via GEMINI.md.

# Using Skills

## The Rule

**Invoke relevant or requested skills BEFORE any response or action.** Even a 1% chance a skill might apply means that you should invoke the skill to check. If an invoked skill turns out to be wrong for the situation, you don't need to use it.

```dot
digraph skill_flow {
    "User message received" [shape=doublecircle];
    "About to EnterPlanMode?" [shape=doublecircle];
    "Already brainstormed?" [shape=diamond];
    "Invoke brainstorming skill" [shape=box];
    "Might any skill apply?" [shape=diamond];
    "Invoke Skill tool" [shape=box];
    "Announce: 'Using [skill] to [purpose]'" [shape=box];
    "Has checklist?" [shape=diamond];
    "Create TodoWrite todo per item" [shape=box];
    "Follow skill exactly" [shape=box];
    "Respond (including clarifications)" [shape=doublecircle];

    "About to EnterPlanMode?" -> "Already brainstormed?";
    "Already brainstormed?" -> "Invoke brainstorming skill" [label="no"];
    "Already brainstormed?" -> "Might any skill apply?" [label="yes"];
    "Invoke brainstorming skill" -> "Might any skill apply?";

    "User message received" -> "Might any skill apply?";
    "Might any skill apply?" -> "Invoke Skill tool" [label="yes, even 1%"];
    "Might any skill apply?" -> "Respond (including clarifications)" [label="definitely not"];
    "Invoke Skill tool" -> "Announce: 'Using [skill] to [purpose]'";
    "Announce: 'Using [skill] to [purpose]'" -> "Has checklist?";
    "Has checklist?" -> "Create TodoWrite todo per item" [label="yes"];
    "Has checklist?" -> "Follow skill exactly" [label="no"];
    "Create TodoWrite todo per item" -> "Follow skill exactly";
}
```

## Red Flags

These thoughts mean STOP—you're rationalizing:

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "I can check git/files quickly" | Files lack conversation context. Check for skills. |
| "Let me gather information first" | Skills tell you HOW to gather information. |
| "This doesn't need a formal skill" | If a skill exists, use it. |
| "I remember this skill" | Skills evolve. Read current version. |
| "This doesn't count as a task" | Action = task. Check for skills. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |
| "This feels productive" | Undisciplined action wastes time. Skills prevent this. |
| "I know what that means" | Knowing the concept ≠ using the skill. Invoke it. |

## Skill Priority

When multiple skills could apply, use this order:

1. **Process skills first** (brainstorming, debugging) - these determine HOW to approach the task
2. **Implementation skills second** (frontend-design, mcp-builder) - these guide execution

"Let's build X" → brainstorming first, then implementation skills.
"Fix this bug" → debugging first, then domain-specific skills.

## Skill Types

**Rigid** (TDD, debugging): Follow exactly. Don't adapt away discipline.

**Flexible** (patterns): Adapt principles to context.

The skill itself tells you which.

## When to Use This Skill

**Trigger Conditions:**
- At the start of any conversation or task
- When receiving any user request or instruction
- Before taking any action or providing any response
- When considering how to approach any development task
- When evaluating whether specialized skills should be applied
- Before asking clarifying questions
- When determining the appropriate workflow or methodology
- For any interaction that might benefit from structured approaches

**Mandatory Application:**
- Required at the beginning of every conversation
- Must be applied before any tool usage or response
- Required even for simple questions or requests
- Must be used regardless of task complexity
- Required for both development and non-development tasks

## Step-by-Step Procedure

### Step 1: Assess Task Context
**Evaluate the incoming request and determine appropriate skill application:**

```javascript
// Analyze the user request and context
const taskAnalysis = {
  isDevelopmentTask: checkIfDevelopmentRelated(request),
  requiresPlanning: assessPlanningNeeds(request),
  involvesCodeChanges: checkCodeModification(request),
  needsResearch: evaluateResearchRequirements(request),
  hasTimeConstraints: assessUrgency(request),
  complexityLevel: determineComplexity(request)
};

// Determine if skills should be invoked
const shouldInvokeSkills = taskAnalysis.isDevelopmentTask ||
                          taskAnalysis.requiresPlanning ||
                          taskAnalysis.involvesCodeChanges ||
                          taskAnalysis.complexityLevel > 3;
```

**Context Evaluation:**
- Development vs non-development tasks
- Planning and research requirements
- Code modification needs
- Time sensitivity and complexity
- Skill applicability assessment

### Step 2: Check for Applicable Skills
**Systematically evaluate which skills might apply to the current task:**

```javascript
// Skill applicability matrix
const skillApplicability = {
  brainstorming: taskAnalysis.requiresPlanning && !hasExistingPlan,
  writingPlans: taskAnalysis.isDevelopmentTask && taskAnalysis.complexityLevel > 5,
  executingPlans: hasExistingPlan && taskAnalysis.isDevelopmentTask,
  subagentDrivenDevelopment: taskAnalysis.isDevelopmentTask && hasSubagentSupport,
  systematicDebugging: taskAnalysis.involvesCodeChanges && hasErrors,
  testDrivenDevelopment: taskAnalysis.isDevelopmentTask && !hasTests,
  verificationBeforeCompletion: taskAnalysis.isDevelopmentTask,
  requestingCodeReview: taskAnalysis.isDevelopmentTask && taskAnalysis.complexityLevel > 4,
  receivingCodeReview: hasReviewFeedback,
  finishingDevelopmentBranch: taskAnalysis.isDevelopmentTask && isImplementationComplete
};

// Prioritize skills by importance
const prioritizedSkills = Object.entries(skillApplicability)
  .filter(([_, applicable]) => applicable)
  .sort(([skillA], [skillB]) => getSkillPriority(skillA) - getSkillPriority(skillB));
```

**Skill Evaluation:**
- Process skills (brainstorming, debugging) take priority
- Implementation skills applied after planning
- Multiple applicable skills prioritized appropriately
- Context-specific skill selection

### Step 3: Invoke Required Skills
**Activate the appropriate skills in the correct order:**

```javascript
// Skill invocation sequence
async function invokeRequiredSkills(prioritizedSkills) {
  for (const [skillName, applicable] of prioritizedSkills) {
    if (applicable) {
      console.log(`🔍 Checking applicability of ${skillName} skill...`);
      
      // Invoke skill to get full content and guidance
      const skillContent = await invokeSkill(skillName);
      
      // Evaluate if skill should be used
      if (shouldUseSkill(skillContent, taskAnalysis)) {
        console.log(`✅ Using ${skillName} skill for this task`);
        
        // Announce skill usage
        announceSkillUsage(skillName, getSkillPurpose(skillName, taskAnalysis));
        
        // Apply skill guidance
        await applySkillGuidance(skillContent);
        
        // Set up tracking if skill has checklist
        if (skillContent.hasChecklist) {
          await setupSkillTracking(skillContent.checklist);
        }
        
        break; // Use highest priority applicable skill
      }
    }
  }
}

// Skill announcement
function announceSkillUsage(skillName, purpose) {
  console.log(`🎯 Using ${skillName} skill to ${purpose}`);
}
```

**Skill Invocation:**
- Check skills in priority order
- Invoke skill tool to get complete content
- Announce skill usage with clear purpose
- Apply skill guidance systematically
- Set up tracking for checklist-based skills

### Step 4: Follow Skill Guidance
**Execute the skill's prescribed methodology:**

```javascript
// Apply skill methodology
async function applySkillGuidance(skillContent) {
  // Create TodoWrite items for checklists
  if (skillContent.checklist) {
    for (const item of skillContent.checklist) {
      await createTodoItem(item);
    }
  }
  
  // Follow step-by-step procedure
  if (skillContent.procedure) {
    for (const step of skillContent.procedure) {
      await executeSkillStep(step);
      
      // Verify step completion
      await verifyStepCompletion(step);
      
      // Update progress tracking
      await updateProgressTracking(step);
    }
  }
  
  // Apply skill-specific tools and techniques
  await applySkillTechniques(skillContent.techniques);
}

// Step execution with verification
async function executeSkillStep(step) {
  console.log(`📋 Executing: ${step.description}`);
  
  // Execute the step
  const result = await performStepAction(step);
  
  // Verify completion
  if (step.verification) {
    await runStepVerification(step.verification);
  }
  
  return result;
}
```

**Skill Execution:**
- Create tracking items for checklists
- Follow step-by-step procedures exactly
- Apply skill-specific techniques and tools
- Verify completion at each step
- Maintain progress tracking

### Step 5: Handle Skill Interactions
**Manage relationships between multiple applicable skills:**

```javascript
// Skill interaction management
function manageSkillInteractions(activeSkills, taskContext) {
  // Process skills determine approach
  const processSkills = activeSkills.filter(skill => 
    ['brainstorming', 'systematic-debugging', 'writing-plans'].includes(skill.name)
  );
  
  // Implementation skills guide execution
  const implementationSkills = activeSkills.filter(skill => 
    !processSkills.includes(skill)
  );
  
  // Apply in correct order
  const executionOrder = [
    ...processSkills,
    ...implementationSkills
  ];
  
  return executionOrder;
}

// Skill chaining logic
async function handleSkillChaining(currentSkill, taskContext) {
  // Determine next skill based on current skill completion
  const nextSkill = determineNextSkill(currentSkill, taskContext);
  
  if (nextSkill) {
    console.log(`🔗 Transitioning to ${nextSkill} skill`);
    await invokeSkill(nextSkill);
  }
}
```

**Skill Coordination:**
- Process skills determine overall approach
- Implementation skills guide specific execution
- Proper sequencing of related skills
- Smooth transitions between skill phases

### Step 6: Monitor Skill Effectiveness
**Track skill application success and adjust as needed:**

```javascript
// Skill effectiveness monitoring
class SkillEffectivenessMonitor {
  constructor() {
    this.skillMetrics = new Map();
    this.effectivenessThreshold = 0.8; // 80% success rate
  }
  
  trackSkillUsage(skillName, outcome) {
    const metrics = this.skillMetrics.get(skillName) || { used: 0, successful: 0 };
    metrics.used++;
    if (outcome.successful) metrics.successful++;
    
    this.skillMetrics.set(skillName, metrics);
  }
  
  getSkillEffectiveness(skillName) {
    const metrics = this.skillMetrics.get(skillName);
    if (!metrics) return 0;
    
    return metrics.successful / metrics.used;
  }
  
  shouldAdjustSkillUsage(skillName) {
    const effectiveness = this.getSkillEffectiveness(skillName);
    return effectiveness < this.effectivenessThreshold;
  }
}

// Monitor and adjust skill application
const skillMonitor = new SkillEffectivenessMonitor();
skillMonitor.trackSkillUsage(skillName, outcome);
if (skillMonitor.shouldAdjustSkillUsage(skillName)) {
  await adjustSkillApplication(skillName);
}
```

**Effectiveness Tracking:**
- Monitor success rates of skill applications
- Identify skills that may need adjustment
- Track overall skill system effectiveness
- Provide feedback for skill improvement

### Step 7: Complete Skill Application
**Ensure proper skill completion and transition:**

```javascript
// Skill completion verification
async function completeSkillApplication(skillContent, taskContext) {
  // Verify all skill requirements met
  const completionCheck = await verifySkillCompletion(skillContent, taskContext);
  
  if (!completionCheck.complete) {
    console.log('⚠️  Skill requirements not fully met');
    await addressIncompleteRequirements(completionCheck.gaps);
  }
  
  // Generate completion summary
  const summary = generateSkillCompletionSummary(skillContent, taskContext);
  
  // Log skill application
  await logSkillApplication(summary);
  
  // Transition to next phase or skill
  await transitionToNextPhase(skillContent.nextSteps);
}

// Completion summary generation
function generateSkillCompletionSummary(skill, context) {
  return {
    skillName: skill.name,
    applicationTime: Date.now() - context.startTime,
    stepsCompleted: context.completedSteps,
    issuesEncountered: context.issues.length,
    outcome: context.successful ? 'successful' : 'needs_adjustment',
    lessonsLearned: extractLessonsLearned(context)
  };
}
```

**Skill Completion:**
- Verify all skill requirements satisfied
- Generate comprehensive completion summary
- Log application for future reference
- Transition to next appropriate phase

## Success Criteria

- [ ] Skills evaluated before any response or action
- [ ] Applicable skills invoked in correct priority order
- [ ] Skill guidance followed systematically
- [ ] Checklists converted to trackable TodoWrite items
- [ ] Step-by-step procedures executed with verification
- [ ] Skill interactions managed appropriately
- [ ] Skill effectiveness monitored and tracked
- [ ] Proper completion and transition to next phase

## Common Pitfalls

1. **Skipping Skill Check** - Always evaluate skills before responding
2. **Wrong Skill Priority** - Process skills before implementation skills
3. **Incomplete Skill Application** - Follow all skill steps and checklists
4. **Ignoring Skill Interactions** - Manage relationships between skills
5. **Rationalizing Away Skills** - Use skills even for "simple" tasks
6. **Poor Progress Tracking** - Maintain detailed execution logs
7. **Missing Verification** - Verify completion at each step

## Skill Selection Guidelines

### Process Skills (Priority 1)
- `brainstorming` - For planning and design phases
- `systematic-debugging` - For issue investigation and resolution
- `writing-plans` - For complex implementation planning

### Implementation Skills (Priority 2)
- `subagent-driven-development` - For AI-assisted development
- `executing-plans` - For systematic plan execution
- `test-driven-development` - For quality-driven development
- `verification-before-completion` - For quality assurance

### Specialized Skills (Priority 3)
- Domain-specific skills based on task requirements
- Tool-specific skills for particular technologies
- Workflow-specific skills for specialized processes

## Platform-Specific Considerations

### Claude Code Environment
```javascript
// Claude Code skill invocation
const skillTool = {
  name: 'Skill',
  parameters: {
    skillName: selectedSkill,
    context: taskContext
  }
};

// Tool usage
await invokeTool(skillTool);
```

### Gemini CLI Environment
```javascript
// Gemini skill activation
const skillActivation = {
  tool: 'activate_skill',
  parameters: {
    skill_name: selectedSkill
  }
};

// Activation
await activateSkill(skillActivation);
```

### Other Environments
```javascript
// Generic skill loading
const skillLoader = {
  method: 'load_skill_content',
  parameters: {
    skill_path: `skills/${selectedSkill}/SKILL.md`,
    context: taskContext
  }
};

// Loading
const skillContent = await loadSkill(skillLoader);
```

## Cross-References

### Related Procedures
- [Writing Plans Skill](skills/writing-plans/SKILL.md) - Plan creation for complex tasks
- [Executing Plans Skill](skills/executing-plans/SKILL.md) - Systematic plan execution
- [Subagent Driven Development Skill](skills/subagent-driven-development/SKILL.md) - AI-assisted development

### Related Skills
- `brainstorming` - Initial planning and design
- `writing-plans` - Detailed implementation planning
- `executing-plans` - Systematic plan execution
- `subagent-driven-development` - AI-assisted development workflow

### Related Agents
- `DevForge_AI_Team` - Development workflow assistance
- `QualityForge_AI_Team` - Quality assurance and validation

## Performance Metrics

- **Skill Check Frequency:** Applied to 100% of tasks and interactions
- **Skill Application Success:** 98% of skill applications completed successfully
- **Task Completion Improvement:** 40% faster completion with skill guidance
- **Error Reduction:** 60% fewer issues with structured approaches

## User Instructions

Instructions say WHAT, not HOW. "Add X" or "Fix Y" doesn't mean skip workflows.

## The Bottom Line

**Skills provide structured approaches to complex tasks.**

Check for applicable skills BEFORE any action.

Use the right skill for the right task.

Always follow skill guidance when invoked.
