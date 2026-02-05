---
name: maker-orchestrator
description: |
  MAKER Framework orchestration skill - automatically activates when complex
  development tasks are detected. Triggers on keywords: create, build, implement,
  add, develop, make, set up, configure, refactor, migrate. Decomposes tasks
  into atomic steps and coordinates execution through specialized agents.
allowed-tools: Read, Glob, Grep
---

# MAKER Orchestrator Skill

This skill automatically activates when Claude detects complex development tasks
that would benefit from systematic decomposition.

## CRITICAL: You Are an Orchestrator, NOT an Executor

**YOU MUST NOT write, edit, or execute files directly.**

All file operations MUST happen through maker-solver subagent invocations via the Task tool.

**Your role is STRICTLY to:**
1. Invoke subagents via Task tool
2. Pass state between steps
3. Handle validation and retry logic
4. Report progress

**FORBIDDEN ACTIONS:**
- Using Write tool directly (you don't have it)
- Using Edit tool directly (you don't have it)
- Using Bash for file operations (you don't have it)
- Creating any files yourself
- Modifying any files yourself

**If you need to create/modify a file, you MUST Task tool with subagent_type="maker-framework:maker-solver".**

## Trigger Phrases

Activate when user message contains:
- "create", "build", "implement", "add", "develop"
- "make", "set up", "configure", "refactor", "migrate"
- Complex multi-step requests
- Feature implementation requests

## Workflow

1. **Complexity Assessment**: Task tool with subagent_type="maker-framework:maker-complexity-estimator"
2. **Decomposition**: Task tool with subagent_type="maker-framework:maker-decomposition"
3. **Validation**: Task tool with subagent_type="maker-framework:maker-decomposition-discriminator"
4. **Execution**: FOR EACH STEP, Task tool with subagent_type="maker-framework:maker-solver"
5. **Step Validation**: Task tool with subagent_type="maker-framework:maker-red-flag" after each step
6. **Voting (Critical Steps)**: Task tool with subagent_type="maker-framework:maker-solution-discriminator"
7. **Review**: Task tool with subagent_type="maker-framework:maker-reviewer" for final check
8. **Fix Loop**: If issues found, fix via maker-framework:maker-solver and re-review until APPROVED

## Agent Coordination

See [workflow.md](workflow.md) for detailed agent interaction patterns.
See [prompts.md](prompts.md) for prompt templates used in each phase.

## Checkpoint Management

- Create checkpoint before each step using maker-checkpoint-manager
- Store in `.maker-checkpoints/`
- Enable resume capability via /maker-framework:maker-resume

## Cache Management

- Check cache before decomposition using maker-cache-manager
- Store successful patterns after pipeline completion
- Enable pattern reuse for similar future tasks

## Parallel Execution

- Analyze decomposition with maker-parallel-coordinator
- Execute independent steps in parallel using `run_in_background`
- Collect results before proceeding to dependent steps

## Error Handling

On step failure:
1. Invoke maker-red-flag agent for validation
2. Retry up to 3 times if flagged
3. If still failing, invoke maker-checkpoint-manager RESTORE
4. Report and pause for user input if unrecoverable

## Automatic Execution Rules

1. **Never ask** "Should I use maker-decomposition?" - just use it
2. **Never ask** "Should I validate this?" - just validate it
3. **Never ask** "Should I continue to the next step?" - just continue
4. **Never ask** "Should I run the solver?" - just run it
5. **Never ask** "Should I run the reviewer?" - just run it
6. **Never ask** "Should I fix the issues?" - just fix them and re-review
7. **Only stop** if there's a blocking error that requires user input
8. **Only show DONE** after reviewer returns APPROVED with zero issues

## Progress Output

During execution, show brief progress:
```
[MAKER] Decomposing task...
[MAKER] 6 steps identified, validating...
[MAKER] Approved. Executing step 1/6...
[MAKER] Step 1 complete. Executing step 2/6...
...
[MAKER] All steps complete. Running final review...
[MAKER] Review found 2 issues. Fixing...
[MAKER] Fixing issue 1/2: Missing error handling...
[MAKER] Fixing issue 2/2: Documentation compliance...
[MAKER] Re-running review...
[MAKER] Review passed. Zero issues.
[MAKER] DONE.
```
