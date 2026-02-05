---
name: SDD Orchestrator
description: >
  Orchestrate Specification-Driven Development (SDD) workflow. Use when user wants to
  create features, implement specs, check workflow status, or follow the SDD process.
  Triggers on: "create feature", "implement", "what's the SDD status", "follow SDD",
  "spec-driven", "specification", "run /feature", "run /implement", "next SDD step".
  Automatically validates prerequisites, routes to correct phase, and updates
  plans/todos after completion.
degree-of-freedom: medium
allowed-tools: Task, SlashCommand, Read, Edit, Glob, Bash(fd:*), Bash(rg:*)
---

@.claude/shared-imports/constitution.md
@.claude/shared-imports/CoD_Σ.md
@.claude/shared-imports/master-todo-utils.md

# SDD Orchestrator Skill

## Purpose

This skill orchestrates the entire Specification-Driven Development workflow by:
1. Auto-triggering on SDD-related user intents
2. Invoking `sdd-coordinator` agent for prerequisite validation
3. Routing to the correct phase command/skill
4. Updating plans/todos after phase completion
5. Integrating supporting skills based on feature type

**Announce at start:** "I'm using the SDD orchestrator skill to manage your development workflow."

---

## Quick Reference

| Phase | Command/Skill | Prerequisites | Output |
|-------|---------------|---------------|--------|
| 1 | /define-product | Repository | memory/product.md |
| 2 | /generate-constitution | product.md | memory/constitution.md |
| 3 | /feature | (optional) product.md, constitution.md | specs/$FEATURE/spec.md |
| 4 | /clarify | spec.md with [NEEDS CLARIFICATION] | Updated spec.md |
| 5 | /plan | spec.md (clarified) | plan.md, research.md, data-model.md |
| 6 | (auto) | plan.md | tasks.md |
| 7 | /audit | spec.md, plan.md, tasks.md | audit-report.md |
| 8 | /implement | tasks.md, audit PASS | Code + tests |

---

## Workflow Files

- **@.claude/skills/sdd-orchestrator/workflows/detection.md** - Intent pattern matching
- **@.claude/skills/sdd-orchestrator/workflows/prerequisite-check.md** - Task tool invocation
- **@.claude/skills/sdd-orchestrator/workflows/phase-routing.md** - Route to correct phase
- **@.claude/skills/sdd-orchestrator/workflows/post-phase-sync.md** - Update plans/todos

---

## Step 1: Detect SDD Intent

**See:** @.claude/skills/sdd-orchestrator/workflows/detection.md

**Pattern Matching:**

```
Intent_Patterns := {
  feature_creation: ["create feature", "new feature", "build", "I want to", "/feature"],
  implementation: ["implement", "code", "develop", "/implement", "start coding"],
  audit: ["audit", "verify", "check", "/audit", "validate"],
  planning: ["plan", "design", "/plan", "architecture"],
  status: ["status", "progress", "what's next", "SDD status", "where am I"],
  foundation: ["define product", "/define-product", "generate constitution", "/generate-constitution"]
}
```

**Detection Logic:**
```
IF user_message ∩ Intent_Patterns ≠ ∅:
  intent := matched_category
  PROCEED to Step 2
ELSE:
  SKIP orchestration (not an SDD action)
```

---

## Step 2: Invoke SDD Coordinator

**See:** @.claude/skills/sdd-orchestrator/workflows/prerequisite-check.md

**Task Tool Invocation:**

```
Task(
  subagent_type="sdd-coordinator",
  description="SDD prerequisite validation",
  prompt="""
    Check current SDD workflow status for this project.

    User intent: {detected_intent}
    Working directory: {cwd}

    Return JSON:
    {
      "current_phase": <1-8>,
      "prerequisites_met": <true|false>,
      "missing_artifacts": ["list of missing files"],
      "blocking_issues": ["list of blockers"],
      "recommended_action": "specific command or action",
      "reason": "explanation"
    }
  """
)
```

**Response Handling:**
```
IF prerequisites_met = true:
  PROCEED to Step 3 (routing)
ELIF missing_artifacts ≠ []:
  REPORT missing artifacts to user
  SUGGEST prerequisite steps
ELIF blocking_issues ≠ []:
  EXPLAIN blockers
  OFFER remediation options
```

---

## Step 3: Route to Correct Phase

**See:** @.claude/skills/sdd-orchestrator/workflows/phase-routing.md

**Routing Matrix:**

| Intent | Prerequisites Met | Action |
|--------|-------------------|--------|
| feature_creation | Yes | Invoke `/feature` command |
| feature_creation | No (no product.md) | Suggest `/define-product` first |
| implementation | Yes (audit PASS) | Invoke `/implement plan.md` |
| implementation | No (audit FAIL) | Show audit failures, suggest fixes |
| implementation | No (no tasks.md) | Invoke `/tasks` first |
| audit | Yes | Invoke `/audit` command |
| planning | Yes | Invoke `/plan spec.md` |
| status | N/A | Report current phase and next steps |
| foundation | N/A | Invoke `/define-product` or `/generate-constitution` |

**Invocation Method:**
```
SlashCommand(command="/{phase_command} {args}")
```

---

## Step 4: Post-Phase Sync

**See:** @.claude/skills/sdd-orchestrator/workflows/post-phase-sync.md

**After EVERY phase completion:**

### 4.1 Update plans/master-plan.md
```
IF phase ∈ {feature_creation, planning}:
  Add spec reference to master plan
  Update phase status in YAML frontmatter
```

### 4.2 Update todos/master-todo.md
```
IF phase = feature_creation:
  Add new feature entry to master todo
IF phase = implementation:
  Mark completed tasks with [x]
  Update progress summary
```

### 4.3 Log to event-stream.md
```
Append: "[{timestamp}] SDD: Phase {N} ({phase_name}) complete - {artifact_created}"
```

---

## Step 5: Integrate Supporting Skills

**Based on feature type detection:**

| Feature Type | Supporting Skills | When Invoked |
|--------------|-------------------|--------------|
| Frontend/UI | shadcn, frontend-design | During spec creation, implementation |
| Backend/API | analyze-code | Pre-implementation research |
| Testing | test-driven-development | During implementation |
| Complex/Unclear | discovery-driven-planning | Before /feature |

**Integration Method:**
```
IF frontend_keywords ∈ spec.md:
  Load @.claude/skills/shadcn/SKILL.md context
  Load @.claude/skills/frontend-design/SKILL.md context

IF implementation_phase AND tests_required:
  Load test-driven-development patterns
  Ensure tests written before code
```

---

## Error Handling

### Common Errors and Recovery

| Error | Detection | Recovery |
|-------|-----------|----------|
| Missing spec.md | File not found | "Create specification first: /feature" |
| Audit FAIL | audit-report.md has CRITICAL | "Fix issues before implementation" |
| [NEEDS CLARIFICATION] | Marker in spec.md | "Run /clarify to resolve ambiguities" |
| No product.md | File not found | "Optional: /define-product for aligned features" |
| Prerequisite cycle | Coordinator returns BLOCKED | "Manual intervention required" |

---

## Example Execution

**User:** "I want to create a new authentication feature"

**Orchestrator Response:**
```
I'm using the SDD orchestrator skill to manage your development workflow.

1. [DETECT] Intent: feature_creation (authentication)

2. [VALIDATE] Invoking sdd-coordinator...
   Result: {
     "current_phase": 3,
     "prerequisites_met": true,
     "recommended_action": "/feature 'authentication with OAuth'"
   }

3. [ROUTE] Prerequisites met. Invoking /feature command...

4. [POST-SYNC] After spec creation:
   - Added specs/015-authentication/spec.md reference to plans/master-plan.md
   - Added feature entry to todos/master-todo.md
   - Logged to event-stream.md

5. [INTEGRATE] Frontend keywords detected. Loading shadcn patterns...

Ready for next phase. Run /implement when audit passes.
```

---

## Dependencies

**Agents:**
- `sdd-coordinator` - Prerequisite validation and workflow status

**Skills:**
- define-product, generate-constitution, specify-feature
- clarify-specification, create-implementation-plan, generate-tasks
- implement-and-verify, analyze-code, debug-issues
- shadcn, frontend-design, test-driven-development (supporting)

**Commands:**
- /feature, /plan, /tasks, /audit, /implement, /verify

---

## Configuration

**Activation Patterns (for skill description tuning):**
- "create feature", "new feature", "build feature"
- "implement", "start coding", "develop"
- "SDD status", "workflow status", "what's next"
- "follow SDD", "spec-driven", "specification"
- "/feature", "/implement", "/plan", "/audit"

**Reliability Target:** 80%+ auto-activation on SDD-related messages

---

**Skill Version**: 1.1.0
**Last Updated**: 2025-12-12
**Changelog**:
- v1.1.0 (2025-12-12): Added Glob to allowed-tools, foundation phases detection, auto-chain docs, status fallback
- v1.0.0 (2025-12-11): Initial version - SDD workflow orchestration
