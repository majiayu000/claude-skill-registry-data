---
name: ftw
description: "PIV workflow orchestrator - Plan, Implement, Validate loop for systematic multi-phase software development. Use when building features phase-by-phase with PRPs, automated validation loops, or multi-agent orchestration. Supports PRD creation, PRP generation, codebase analysis, and iterative execution with validation."
user-invocable: true
disable-model-invocation: true
metadata: {"openclaw":{"emoji":"gear","homepage":"https://github.com/SmokeAlot420/ftw","requires":{"bins":["git"]},"os":["darwin","linux"]},"minis":{"originalSource":"https://clawskills.sh/skills/smokealot420-ftw","convertedAt":"2026-10-31T22:11:18.200Z","license":"Unknown"}}
---

# PIV Ralph Orchestrator

## Arguments: $ARGUMENTS

Parse arguments using this logic:

### PRD Path Mode (first argument ends with `.md`)

If the first argument ends with `.md`, it's a direct path to a PRD file:
- `PRD_PATH` - Direct path to the PRD file
- `PROJECT_PATH` - Derived by going up from PRDs/ folder
- `START_PHASE` - Second argument (default: 1)
- `END_PHASE` - Third argument (default: auto-detect from PRD)

### Project Path Mode

If the first argument does NOT end with `.md`:
- `PROJECT_PATH` - Absolute path to project (default: current working directory)
- `START_PHASE` - Second argument (default: 1)
- `END_PHASE` - Third argument (default: 4)
- `PRD_PATH` - Auto-discover from `PROJECT_PATH/PRDs/` folder

### Detection Logic

```
If $ARGUMENTS[0] ends with ".md":
  PRD_PATH = $ARGUMENTS[0]
  PROJECT_PATH = dirname(dirname(PRD_PATH))
  START_PHASE = $ARGUMENTS[1] or 1
  END_PHASE = $ARGUMENTS[2] or auto-detect from PRD
  PRD_NAME = basename without extension
Else:
  PROJECT_PATH = $ARGUMENTS[0] or current working directory
  START_PHASE = $ARGUMENTS[1] or 1
  END_PHASE = $ARGUMENTS[2] or 4
  PRD_PATH = auto-discover from PROJECT_PATH/PRDs/
  PRD_NAME = discovered PRD basename
```

### Mode Detection

After parsing arguments:
- If PRD_PATH was provided or auto-discovered → **MODE = "execute"** (normal flow)
- If no PRD found and no PRD_PATH provided → **MODE = "discovery"**

---

## Required Reading by Role

**CRITICAL: Each role MUST read their instruction files before acting.**

| Role | Instructions |
|------|-------------|
| Discovery (no PRD) | Read {baseDir}/references/piv-discovery.md |
| PRD Creation | Read {baseDir}/references/create-prd.md |
| PRP Generation | Read {baseDir}/references/generate-prp.md |
| Codebase Analysis | Read {baseDir}/references/codebase-analysis.md |
| Executor | Read {baseDir}/references/piv-executor.md + {baseDir}/references/execute-prp.md |
| Validator | Read {baseDir}/references/piv-validator.md |
| Debugger | Read {baseDir}/references/piv-debugger.md |

**Prerequisite:** A PRD must exist before entering the Phase Workflow. If no PRD exists, the orchestrator enters Discovery Mode (see below).

---

## Discovery Mode (No PRD Found)

When MODE = "discovery":

1. Read {baseDir}/references/piv-discovery.md for the discovery process
2. Present discovery questions to the user in a friendly, conversational tone (single message)
   - Target audience is vibe coders, not senior engineers — keep it approachable
   - Skip questions the user already answered in their initial message
3. Wait for user answers
4. Fill gaps with your own expertise:
   - If user doesn't know tech stack → research (web search, codebase scan) and PROPOSE one
   - If user can't define phases → propose 3-4 phases based on scope
   - Always propose-and-confirm: "Here's what I'd suggest — does this sound right?"
5. Run project setup (create PRDs/, PRPs/templates/, PRPs/planning/)
6. Generate PRD: Read {baseDir}/references/create-prd.md, use discovery answers + your proposals to write PRD to PROJECT_PATH/PRDs/PRD-{project-name}.md
7. Set PRD_PATH to the generated PRD, auto-detect phases → continue to Phase Workflow

The orchestrator handles discovery and PRD generation directly (no sub-agent needed — interactive Q&A requires staying in the same session, and answers are already in context for PRD generation).

---

## Orchestrator Philosophy

> "Context budget: ~15% orchestrator, 100% fresh per subagent"

You are the **orchestrator**. You stay lean and manage workflow. You DO NOT execute PRPs yourself - you spawn specialized sub-agents with fresh context for each task.

**Sub-agent spawning:** Use the `sessions_spawn` tool to create fresh sub-agent sessions. Each spawn is non-blocking — you'll receive results via an announce step. Wait for each agent's results before proceeding to the next step.

---

## Project Setup (piv-init)

If the project doesn't have PIV directories, create them:
```bash
mkdir -p PROJECT_PATH/PRDs PROJECT_PATH/PRPs/templates PROJECT_PATH/PRPs/planning
```
Copy `{baseDir}/assets/prp_base.md` to `PROJECT_PATH/PRPs/templates/prp_base.md` if it doesn't exist.
Create `PROJECT_PATH/WORKFLOW.md` from `{baseDir}/assets/workflow-template.md` if it doesn't exist.

---

## Phase Workflow

For each phase from START_PHASE to END_PHASE:

### Step 1: Check/Generate PRP

Check for existing PRP:
```bash
ls -la PROJECT_PATH/PRPs/ 2>/dev/null | grep -i "phase.*N\|pN\|p-N"
```

If no PRP exists, spawn a **fresh sub-agent** using `sessions_spawn` to do both codebase analysis and PRP generation in sequence:

```
RESEARCH & PRP GENERATION MISSION - Phase {N}
==============================================

Project root: {PROJECT_PATH}
PRD Path: {PRD_PATH}

## Phase {N} Scope (from PRD)
{paste phase scope}

## Step 1: Codebase Analysis
Read {baseDir}/references/codebase-analysis.md for the process.
Save to: {PROJECT_PATH}/PRPs/planning/{PRD_NAME}-phase-{N}-analysis.md

## Step 2: Generate PRP (analysis context still loaded)
Read {baseDir}/references/generate-prp.md for the process.
Use template: PRPs/templates/prp_base.md
Output to: {PROJECT_PATH}/PRPs/PRP-{PRD_NAME}-phase-{N}.md

Do BOTH steps yourself. DO NOT spawn sub-agents.
```

### Step 2: Spawn EXECUTOR

Spawn a fresh sub-agent using `sessions_spawn`:

```
EXECUTOR MISSION - Phase {N}
============================

Read {baseDir}/references/piv-executor.md for your role definition.
Read {baseDir}/references/execute-prp.md for the execution process.

PRP Path: {PRP_PATH}
Project: {PROJECT_PATH}

Follow: Load PRP → Plan Thoroughly → Execute → Validate → Verify
Output EXECUTION SUMMARY with Status, Files, Tests, Issues.
```

### Step 3: Spawn VALIDATOR

Spawn a fresh sub-agent using `sessions_spawn`:

```
VALIDATOR MISSION - Phase {N}
=============================

Read {baseDir}/references/piv-validator.md for your validation process.

PRP Path: {PRP_PATH}
Project: {PROJECT_PATH}
Executor Summary: {SUMMARY}

Verify ALL requirements independently.
Output VERIFICATION REPORT with Grade, Checks, Gaps.
```

**Process result:** PASS → commit | GAPS_FOUND → debugger | HUMAN_NEEDED → ask user

### Step 4: Debug Loop (Max 3 iterations)

Spawn a fresh sub-agent using `sessions_spawn`:

```
DEBUGGER MISSION - Phase {N} - Iteration {I}
============================================

Read {baseDir}/references/piv-debugger.md for your debugging methodology.

Project: {PROJECT_PATH}
PRP Path: {PRP_PATH}
Gaps: {GAPS}
Errors: {ERRORS}

Fix root causes, not symptoms. Run tests after each fix.
Output FIX REPORT with Status, Fixes Applied, Test Results.
```

After debugger: re-validate → PASS (commit) or loop (max 3) or escalate.

### Step 5: Smart Commit

```bash
cd PROJECT_PATH && git status && git diff --stat
```

Create semantic commit with `Built with FTW (First Try Works) - https://github.com/SmokeAlot420/ftw`.

### Step 6: Update WORKFLOW.md

Mark phase complete, note validation results.

### Step 7: Next Phase

Loop back to Step 1 for next phase.

---

## Error Handling

- **No PRD**: Enter Discovery Mode (see Discovery Mode section above)
- **Executor BLOCKED**: Ask user for guidance
- **Validator HUMAN_NEEDED**: Ask user for guidance
- **3 debug cycles exhausted**: Escalate to user

### Sub-Agent Timeout/Failure
When a sub-agent times out or fails:
1. Check for partial work (files created, tests written)
2. Retry once with a simplified, shorter prompt
3. If retry fails, escalate to user with what was accomplished

---

## Completion

```
## PIV RALPH COMPLETE

Phases Completed: START to END
Total Commits: N
Validation Cycles: M

### Phase Summary:
- Phase 1: [feature] - validated in N cycles
...

All phases successfully implemented and validated.
```
