---
name: observe-plan-act-reflect
description: Use for any complex, multi-step task - iterative agentic loop that observes current state, plans an action, executes it, and reflects on the result before looping again
---

# Observe → Plan → Act → Reflect

## Overview

Undisciplined action wastes time and introduces regressions. Random changes without observation lead to thrashing. Working without reflection means problems compound.

**Core principle:** NEVER act without first observing. NEVER claim completion without reflecting.

**Violating the letter of this process is violating its spirit.**

## The Iron Law

```
OBSERVE → PLAN → ACT → REFLECT → (loop or done)
```

You MUST complete each phase before entering the next. You MUST reflect after every action before deciding whether to loop or stop.

## When to Use

Use for ANY complex or multi-step task:
- Creating content (adventures, NPCs, stat blocks, XML)
- Fixing bugs or resolving issues
- Refactoring or restructuring files
- Running multi-step workflows
- Tasks involving 3+ file changes
- Tasks where the current state is unknown

**Use this ESPECIALLY when:**
- You don't fully understand the current state
- A previous attempt didn't work
- The task spans multiple files
- Requirements may conflict with existing content
- You are about to make irreversible changes

## The Four Phases

You MUST complete each phase before moving to the next. The loop continues until the goal is achieved or you stop and escalate.

---

### Phase 1: OBSERVE

**Before doing anything, understand the current state.**

1. **Read relevant files** — Don't act on assumptions about file contents
   - Read every file you plan to modify (in full, not just the sections you expect to change)
   - Read related files that may be affected
   - Note file structure, patterns, and existing conventions

2. **Examine current behavior**
   - What does it do now? What should it do?
   - Is there existing functionality that addresses this?
   - What constraints does the existing code/content impose?

3. **Check canon and constraints** (campaign content)
   - Verify location names against canonical geography
   - Check NPC roster for name conflicts
   - Confirm tone and design principles apply

4. **Gather evidence**
   - Run commands to see current state (build output, test results, XML validation)
   - Identify what's working and what's broken
   - Note which files are recent vs. stable

**Exit criteria:** You can accurately describe the current state — what exists, what's missing, and what constraints apply.

---

### Phase 2: PLAN

**Think before acting. Commit a plan before touching files.**

1. **Define the goal clearly**
   - What specifically needs to change?
   - What is "done"? How will you verify it?

2. **Break into discrete steps**
   - Each step should be one verifiable action (one file, one change)
   - Order matters — identify dependencies between steps
   - If more than 5 steps, reconsider scope

3. **Identify risks**
   - What could go wrong?
   - What existing content could this break?
   - Are there canon or format constraints to check?

4. **State your plan explicitly**
   - Write it out: "I will do X, then Y, then Z"
   - If you can't state the plan clearly, you don't understand the problem well enough
   - Return to Observe if the plan has gaps

**Exit criteria:** You have a clear, ordered list of specific actions with defined success criteria for each.

---

### Phase 3: ACT

**Execute one step at a time. No bundling. No "while I'm here" changes.**

1. **Execute the smallest meaningful change**
   - One file change at a time when practical
   - Preserve existing formatting and style
   - Don't fix unrelated issues

2. **Document what you're doing**
   - Note which step of your plan you're executing
   - If you deviate from the plan, note why

3. **Stop at complexity**
   - If a step turns out harder than expected, STOP
   - Return to Observe with new information
   - Do NOT add improvised fixes on top

**Exit criteria:** The planned step is executed. You have not made additional changes beyond the plan.

---

### Phase 4: REFLECT

**Verify before claiming progress. Assess before looping.**

1. **Verify the step worked**
   - Run validation commands: build, lint, XML check, etc.
   - Read the changed file — does it match your intent?
   - Check for unintended side effects

2. **Assess against goal**
   - Is the overall goal complete?
   - What remains to be done?
   - Did this step reveal new information that changes the plan?

3. **Decide: loop or done**
   - **Goal achieved:** Confirm with evidence, report completion
   - **Goal not yet achieved:** Return to Observe with updated understanding
   - **Unexpected problem found:** Return to Plan with new constraints
   - **3+ loops with no progress:** STOP — escalate or rethink approach

**Exit criteria:** You have concrete evidence of what happened and a clear next action.

---

## Loop Decision Logic

```
After Reflect:
  ├─ Goal achieved AND verified → DONE (report with evidence)
  ├─ Goal partially achieved, clear next step → OBSERVE (with new context)
  ├─ Unexpected problem found → PLAN (reformulate with new info)
  ├─ Step failed → OBSERVE (gather more evidence)
  └─ 3+ failed loops → STOP and escalate
```

## For This Campaign

### Content Creation (Adventures, NPCs, XML)

| Phase | Key Activities |
|-------|---------------|
| **Observe** | Read `DM Guild Roster.md`, existing XML UIDs, adventure templates, canonical location list |
| **Plan** | Draft structure, check for name/UID conflicts, verify tone aligns with design principles |
| **Act** | Write one file at a time; XML first, then markdown, then register in TOC |
| **Reflect** | Validate XML structure, run `./build.sh --dms`, check Homebrewery rendering |

### Debugging Build Issues

| Phase | Key Activities |
|-------|---------------|
| **Observe** | Run `./build.sh`, read full error output, identify which file triggers it |
| **Plan** | Identify the single most likely cause; do not make multiple changes |
| **Act** | One change to address the identified cause |
| **Reflect** | Run build again; check that output matches expected |

### Canon Review

| Phase | Key Activities |
|-------|---------------|
| **Observe** | Read the file being reviewed; read `canon.instructions.md`, `DM Guild Roster.md` |
| **Plan** | List specific issues: location, NPC name, tone, player-facing link violations |
| **Act** | Fix one issue at a time; note each change |
| **Reflect** | Re-read the file; verify each fix is correct and nothing new was introduced |

## Red Flags — Return to Observe

If you catch yourself thinking any of these, STOP and return to Phase 1:

- "It's probably fine"
- "I'll fix this other thing while I'm here"
- "Let me just try this and see what happens"
- "I already know what the problem is"
- "This should work"
- "Just one more change"
- "I'll verify it after I make a few more changes"

## Quick Reference

| Phase | Question to Answer | Evidence Required |
|-------|-------------------|-------------------|
| **Observe** | What is the current state? | File contents, command output |
| **Plan** | What exactly will I change, and in what order? | Written step list |
| **Act** | Did I make exactly the change I planned? | Diff or summary of changes |
| **Reflect** | Did the change work? Is the goal complete? | Verification command output |

## Integration with Other Skills

- Use **observe-plan-act-reflect** as the outer loop for any multi-step task
- Use **systematic-debugging** inside the Observe phase when diagnosing failures
- Use **verification-before-completion** inside the Reflect phase before claiming done
- Use **writing-plans** to formalize the Plan phase for large tasks
- Use **canon-check** inside the Reflect phase for campaign content
