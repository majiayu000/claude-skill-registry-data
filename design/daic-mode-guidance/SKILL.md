---
name: daic_mode_guidance
description: Explain the DAIC (Discuss-Align-Implement-Check) workflow, help users understand current mode, what's allowed in each mode, and how to transition between modes - ANALYSIS-ONLY skill
schema_version: 1.0
---

# daic_mode_guidance

**Type:** ANALYSIS-ONLY
**DAIC Modes:** DISCUSS, ALIGN, IMPLEMENT, CHECK (all modes)
**Priority:** Medium

## Trigger Reference

This skill activates on:
- Keywords: "what mode", "DAIC", "can I write", "implement mode", "current mode", "DISCUSS mode", "ALIGN mode", "CHECK mode"
- Intent patterns: "what.*(mode|DAIC)", "can.*?(write|edit|modify)", "(current|which).*?mode"

From: `skill-rules.json` - daic_mode_guidance configuration

## Purpose

Explain the DAIC (Discuss-Align-Implement-Check) workflow, help users understand the current mode, what's allowed in each mode, and how to transition between modes. This is an ANALYSIS-ONLY skill that provides guidance but never modifies mode or writes files.

## Core Behavior

In any DAIC mode:

1. **Mode Explanation**
   - Explain what DAIC means and why it exists
   - Describe the current mode
   - List what is and isn't allowed in current mode
   - Show how to transition to other modes

2. **Write-Gating Clarification**
   - Explain why writes are blocked in DISCUSS/ALIGN/CHECK
   - Clarify that only IMPLEMENT mode allows writes
   - Describe the safety benefits of write-gating
   - Provide transition phrases for IMPLEMENT mode

3. **Workflow Guidance**
   - Suggest appropriate mode for current task
   - Explain typical DAIC flow (DISCUSS → ALIGN → IMPLEMENT → CHECK)
   - Guide iterative refinement (CHECK → DISCUSS → ALIGN → IMPLEMENT)
   - Help troubleshoot mode confusion

4. **Transition Assistance**
   - List trigger phrases for each mode
   - Explain when to use each mode
   - Show how to return to DISCUSS from any mode
   - Guide emergency transitions (if blocked)

## Safety Guardrails

**ANALYSIS-ONLY RULES:**
- ✓ NEVER call write tools (Edit, Write, MultiEdit)
- ✓ NEVER change CC_SESSION_MODE directly
- ✓ NEVER bypass mode transition protocols
- ✓ Only provide analysis and guidance
- ✓ Safe to run in any DAIC mode

**Mode Guidance Quality:**
- Provide clear, actionable instructions
- Include specific transition phrases
- Explain rationale behind mode restrictions
- Show examples of appropriate work for each mode
- Never confuse user about current mode

## DAIC Mode Reference

### DISCUSS Mode
**Purpose:** Clarify intent, constraints, and relevant SoT
**Allowed:**
- Ask questions and gather requirements
- Review existing code and documentation
- Discuss approach and tradeoffs
- Reference SoT (Tier-1, Tier-2 docs)
- Use read-only tools (Read, Grep, Glob, Bash for reads)

**Not Allowed:**
- Write, Edit, or MultiEdit tools
- Creating or modifying files
- Running commands that modify state

**Transition to IMPLEMENT:**
- User says: "go ahead", "do it", "implement", "yert", or any configured trigger phrase
- Or: Explicitly use API: `sessions state mode IMPLEMENT`

---

### ALIGN Mode
**Purpose:** Design plan + task manifest (Tier-2)
**Allowed:**
- Create task manifests and RFCs
- Design architecture and approach
- Define success criteria and todos
- Plan file structure and API contracts
- Use read-only tools

**Not Allowed:**
- Write, Edit, or MultiEdit tools
- Implementing the actual code
- Modifying application files

**Transition to IMPLEMENT:**
- Same triggers as DISCUSS mode
- User approves the plan

---

### IMPLEMENT Mode
**Purpose:** Execute the manifest; write tools allowed
**Allowed:**
- Write, Edit, MultiEdit tools
- Create and modify files
- Run tests and builds
- Execute approved todos from manifest
- Follow the approved plan

**Not Allowed:**
- Deviating from approved manifest without discussion
- Modifying Tier-1 docs without explicit approval
- Bypassing success criteria

**Transition to CHECK:**
- Automatically transitions when all todos complete
- Or: Explicitly use API: `sessions state mode CHECK`

---

### CHECK Mode
**Purpose:** Test, verify, summarize outcomes
**Allowed:**
- Run tests and validation
- Review implemented changes
- Summarize what was accomplished
- Suggest next steps
- Minimal updates to Tier-2/LCMP (only when clearly valuable)

**Not Allowed:**
- Major new implementations
- Creating new features
- Extensive file modifications

**Transition to DISCUSS:**
- Automatically returns after CHECK completes
- Or: User starts new discussion
- Or: Explicitly use API: `sessions state mode DISCUSS`

## Examples

### When to Activate

✓ "What mode am I in?"
✓ "Can I edit files now?"
✓ "How do I switch to implement mode?"
✓ "Why can't I write?"
✓ "What's DAIC?"

### Typical Output

**Scenario: User Confused About Write Blocking**
```markdown
### DAIC Mode Guidance

**Current Mode:** DISCUSS

**Why Writes Are Blocked:**
You're currently in DISCUSS mode, which is for gathering requirements and understanding the problem. Write tools (Edit, Write, MultiEdit) are only allowed in IMPLEMENT mode to ensure changes are intentional and aligned with an approved plan.

**What You Can Do in DISCUSS:**
- ✓ Ask questions and clarify requirements
- ✓ Review existing code (Read, Grep, Glob)
- ✓ Discuss approach and tradeoffs
- ✓ Reference documentation

**What You Cannot Do in DISCUSS:**
- ✗ Create or modify files
- ✗ Use Write, Edit, or MultiEdit tools

**To Enable Writes:**

1. **First, approve a plan** (I can propose one if needed)
2. **Then transition to IMPLEMENT mode** by saying any of:
   - "go ahead"
   - "do it"
   - "implement"
   - "yert"
   - Or use: `sessions state mode IMPLEMENT`

**Full DAIC Workflow:**
```
DISCUSS (you are here)
  ↓ [gather context, clarify requirements]
ALIGN
  ↓ [design plan, get approval]
IMPLEMENT
  ↓ [execute plan with write tools]
CHECK
  ↓ [verify, test, summarize]
DISCUSS (loop back for next work)
```

**Would you like me to propose a plan so we can move to IMPLEMENT?**
```

**Scenario: User in IMPLEMENT, Wants to Discuss**
```markdown
### DAIC Mode Guidance

**Current Mode:** IMPLEMENT

**You're in Implementation Mode:**
This means write tools are enabled and you're executing an approved plan.

**To Return to Discussion:**

Option 1: Let the current implementation complete
- Finish all todos in the current task
- System will auto-transition to CHECK, then DISCUSS

Option 2: Manually transition now
- Use API: `sessions state mode DISCUSS`
- Note: This will end the current implementation session

**Recommendation:**
If you want to discuss something while implementation is in progress, you can:
1. Ask questions now (I can answer without changing mode)
2. If you need to revise the plan, we should return to DISCUSS
3. If you just want to check status, that's fine in IMPLEMENT too

**What would you like to do?**
```

**Scenario: Explaining DAIC Workflow**
```markdown
### DAIC Workflow Explained

DAIC stands for: **Discuss → Align → Implement → Check**

It's a disciplined workflow that ensures code changes are intentional and aligned with clear goals.

---

#### 1. DISCUSS Mode
**Goal:** Understand the problem
**Activities:**
- Gather requirements
- Review existing code
- Ask clarifying questions
- Understand constraints

**Output:** Clear understanding of what needs to be done
**Writes:** ✗ No

---

#### 2. ALIGN Mode
**Goal:** Design the solution
**Activities:**
- Create task manifest
- Define success criteria
- List todos/acceptance criteria
- Get user approval

**Output:** Approved plan with specific todos
**Writes:** ✗ No

---

#### 3. IMPLEMENT Mode
**Goal:** Execute the plan
**Activities:**
- Write code per approved todos
- Create/modify files
- Run tests
- Follow the manifest

**Output:** Implemented changes
**Writes:** ✓ Yes (only mode where writes allowed)

---

#### 4. CHECK Mode
**Goal:** Verify quality
**Activities:**
- Run tests
- Verify success criteria met
- Summarize what was accomplished
- Suggest next steps

**Output:** Verified, tested changes
**Writes:** Limited (minimal updates only)

---

**Then Loop Back to DISCUSS for Next Work**

**Why This Matters:**
- Prevents accidental file modifications
- Ensures changes match user intent
- Provides clear checkpoints for review
- Makes collaboration predictable

**Current Mode:** [Shows current mode]
```

### When NOT to Activate

✗ User is asking about application modes (e.g., "production mode")
✗ Question is about git modes/states
✗ Focus is on other tools/frameworks (not DAIC)
✗ User just wants to know technical details (not mode guidance)

## Mode Transition Phrases

### To IMPLEMENT Mode
- "go ahead"
- "do it"
- "implement"
- "yert"
- "make it so"
- "execute"
- "proceed"

### To DISCUSS Mode
- "wait"
- "hold on"
- "let's discuss"
- "stop"
- "nevermind"

### To CHECK Mode
- Happens automatically after todos complete
- Can explicitly set: `sessions state mode CHECK`

### To ALIGN Mode
- Not typically triggered by phrases
- Happens during planning phase
- Can explicitly set: `sessions state mode ALIGN`

## Common Mode Issues

### Issue: "I can't write files"
**Cause:** Not in IMPLEMENT mode
**Solution:** Approve a plan and transition to IMPLEMENT

### Issue: "Why did implementation stop?"
**Cause:** All todos completed (auto-transition to CHECK)
**Solution:** If more work needed, return to DISCUSS and propose new todos

### Issue: "Accidentally in wrong mode"
**Cause:** User or system set mode incorrectly
**Solution:** Use API to set correct mode: `sessions state mode <MODE>`

### Issue: "DAIC feels restrictive"
**Cause:** Misunderstanding purpose of write-gating
**Solution:** Explain safety benefits, show efficient workflow

## Emergency Mode Changes

If hooks or automation cause mode problems:

```bash
# Force mode change via API
sessions state mode DISCUSS

# Check current mode
sessions state show

# Clear corrupted state (careful!)
sessions state task clear
```

## Decision Logging

When providing significant mode guidance:

```markdown
### DAIC Mode Guidance Provided: [Date]
- **User Question:** "Why can't I write files?"
- **Current Mode:** DISCUSS
- **Guidance:** Explained write-gating, provided transition phrases
- **Outcome:** User approved plan, transitioned to IMPLEMENT
- **Note:** User initially confused by auto-transition to CHECK
```

## Related Skills

- **cc-sessions-core** - For understanding core framework (including DAIC)
- **framework_health_check** - To verify DAIC enforcement is working
- **framework_repair_suggester** - If DAIC mode transitions are broken
- **cc-sessions-hooks** - If hooks are preventing mode transitions

---

**Last Updated:** 2025-11-15
**Framework Version:** 2.0
