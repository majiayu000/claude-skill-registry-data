---
name: framework_repair_suggester
description: Detect framework and tooling issues then suggest creating REPAIR- tasks to address them systematically - ANALYSIS-ONLY skill that identifies problems and proposes structured fixes
schema_version: 1.0
---

# framework_repair_suggester

**Type:** ANALYSIS-ONLY
**DAIC Modes:** DISCUSS, ALIGN, IMPLEMENT, CHECK (all modes)
**Priority:** High

## Trigger Reference

This skill activates on:
- Keywords: "REPAIR task", "framework issue", "broken gating", "framework bug", "framework broken"
- Intent patterns: "create.*?REPAIR.*?task", "framework.*(issue|bug|broken|problem)", "REPAIR-"

From: `skill-rules.json` - framework_repair_suggester configuration

## Purpose

Detect framework and tooling issues, then suggest creating REPAIR- tasks to address them systematically. This is an ANALYSIS-ONLY skill that identifies problems and proposes structured fixes, but never modifies framework files directly.

## Core Behavior

In any DAIC mode:

1. **Issue Detection**
   - Monitor for framework misbehavior (hooks not firing, write-gating bypassed, state corruption)
   - Identify when framework docs are out of sync
   - Detect when skills aren't working as configured
   - Recognize when prompts are inconsistent or outdated
   - Notice when gating rules are being violated

2. **Root Cause Analysis**
   - Investigate why the issue occurred
   - Check related framework components
   - Review recent changes that might have caused it
   - Identify systemic vs. one-off problems
   - Assess impact and urgency

3. **REPAIR Task Proposal**
   - Generate REPAIR- task ID with date (e.g., `REPAIR-write-gating-2025-11-15`)
   - Define problem clearly and specifically
   - Propose solution approach
   - List files that need investigation/modification
   - Provide success criteria
   - Include prevention strategy

4. **Context Gathering**
   - Collect error messages, logs, and symptoms
   - Identify affected components
   - Note when issue first appeared
   - Gather recent changes for correlation
   - Provide all context needed for repair

## Safety Guardrails

**ANALYSIS-ONLY RULES:**
- ✓ NEVER call write tools (Edit, Write, MultiEdit)
- ✓ NEVER auto-create REPAIR task files
- ✓ NEVER modify framework directly
- ✓ Only provide analysis and task proposals
- ✓ Safe to run in any DAIC mode

**Issue Detection Safety:**
- Don't false-alarm on expected behavior
- Distinguish framework bugs from user errors
- Verify issue is reproducible before suggesting REPAIR
- Assess urgency accurately (CRITICAL vs. low priority)
- Suggest workarounds when available

## Examples

### When to Activate

✓ "Write-gating isn't blocking writes in DISCUSS mode"
✓ "The sessions_enforce hook seems broken"
✓ "Framework version drift detected"
✓ "Skills aren't triggering when they should"
✓ "Create a REPAIR task for X"

### Typical Output

**Scenario: Write-Gating Failure**
```markdown
### REPAIR Task Suggestion: Write-Gating Broken

**Issue Detected:** Write tools are not being blocked in DISCUSS mode

**Symptoms:**
- Write tool succeeded in DISCUSS mode (expected: blocked)
- No error message from sessions_enforce hook
- sessions-state.json shows mode=DISCUSS but write completed

**Impact:** CRITICAL
- Framework safety compromised
- Users can bypass DAIC discipline
- Risk of unintended file modifications

**Root Cause (Suspected):**
- sessions/hooks/sessions_enforce.js may not be loaded
- Hook might have syntax error preventing execution
- PreToolUse hook registration may have failed

**Proposed REPAIR Task:**

**Task ID:** `REPAIR-write-gating-2025-11-15`

**Problem:**
Write-gating enforcement is broken. Write tools (Edit, Write, MultiEdit) are not being blocked when mode is DISCUSS/ALIGN/CHECK. This is a critical safety issue that undermines the framework's core discipline.

**Investigation Steps:**
1. Check if sessions/hooks/sessions_enforce.js exists and loads
2. Review hook for syntax errors or logic bugs
3. Verify PreToolUse hook registration in Claude Code
4. Test write-gating in each DAIC mode
5. Check if hook execution order matters

**Files to Review:**
- sessions/hooks/sessions_enforce.js
- sessions/hooks/README.md (if exists)
- Hook loading mechanism
- sessions/sessions-config.json (hook configuration)

**Proposed Fix:**
1. Fix syntax errors if present
2. Add defensive logging to hook
3. Ensure hook returns { success: false } correctly
4. Test in all modes before deploying

**Success Criteria:**
- Write tools blocked in DISCUSS/ALIGN/CHECK modes
- Clear error message shown to user
- Write tools allowed in IMPLEMENT mode
- Health check passes for write-gating

**Prevention:**
- Add write-gating test to framework health check
- Run health check before committing hook changes
- Document hook testing procedure
- Add to pre-release checklist

**Would you like me to create this REPAIR task file?**
(Note: This requires IMPLEMENT mode and user approval)
```

**Scenario: Skill Configuration Issue**
```markdown
### REPAIR Task Suggestion: Skill Triggers Not Firing

**Issue Detected:** Skills defined in skill-rules.json are not activating

**Symptoms:**
- User mentions "error tracking" keywords but error-tracking skill doesn't activate
- skill-rules.json appears valid
- No obvious syntax errors

**Impact:** MEDIUM
- Skills not providing value
- User experience degraded
- Wasted skill development effort

**Root Cause (Suspected):**
- Skill trigger patterns may be too narrow
- Auto-trigger logic may not be implemented
- Skill loading may have failed silently

**Proposed REPAIR Task:**

**Task ID:** `REPAIR-skill-triggers-2025-11-15`

**Problem:**
Skills are configured in skill-rules.json but not activating when expected. This suggests either trigger patterns are incorrect, or the skill activation system isn't working properly.

**Investigation Steps:**
1. Verify .claude/skills/*/SKILL.md files exist for all configured skills
2. Test skill loading with simple trigger phrases
3. Review auto-trigger implementation (if any)
4. Check Claude Code skill loading mechanism
5. Validate trigger pattern regex syntax

**Files to Review:**
- .claude/skills/skill-rules.json
- .claude/skills/*/SKILL.md (all skill prompt files)
- Skill activation logs (if available)

**Proposed Fix:**
1. Broaden trigger patterns if too narrow
2. Verify skill prompt files exist and match skill-rules.json names
3. Add manual activation examples if auto-trigger not working
4. Document current skill activation mechanism

**Success Criteria:**
- Skills activate on appropriate keywords
- Manual skill invocation works reliably
- Skill activation logged for debugging
- User can easily trigger relevant skills

**Prevention:**
- Test skill triggers during skill development
- Document trigger phrases clearly
- Provide manual activation fallback
- Add skill activation to health check

**Would you like me to create this REPAIR task file?**
```

### When NOT to Activate

✗ User is debugging application code (not framework)
✗ Issue is expected behavior (not a bug)
✗ Problem is user error (not framework malfunction)
✗ Issue can be resolved without REPAIR task

## REPAIR Task Template

Standard structure for REPAIR task proposals:

```markdown
## Task: REPAIR-[component]-[YYYY-MM-DD]

### Problem
[Clear, specific description of what's broken]

### Symptoms
- [Observable symptom 1]
- [Observable symptom 2]
- [Observable symptom 3]

### Impact
[CRITICAL | HIGH | MEDIUM | LOW]
[Explanation of impact]

### Root Cause (Suspected)
[Hypothesis about what's causing the issue]

### Investigation Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Files to Review
- [file path 1]
- [file path 2]

### Proposed Fix
[Approach to fixing the issue]

### Success Criteria
- [Measurable outcome 1]
- [Measurable outcome 2]
- [Health check passes]

### Prevention
[How to prevent this from happening again]

### Context Files
- [Relevant Tier-1 doc 1]
- [Relevant Tier-2 doc 1]
```

## Common Framework Issues

### 1. Write-Gating Failures
**Symptoms:** Writes succeed in non-IMPLEMENT modes
**Urgency:** CRITICAL
**Component:** sessions/hooks/sessions_enforce.js

### 2. Hook Not Executing
**Symptoms:** Hook logic bypassed, no errors
**Urgency:** HIGH
**Component:** Hook registration, hook syntax

### 3. State Corruption
**Symptoms:** Invalid state values, JSON parse errors
**Urgency:** HIGH
**Component:** State read/write logic

### 4. Skill Loading Failures
**Symptoms:** Skills don't trigger, missing skill errors
**Urgency:** MEDIUM
**Component:** skill-rules.json, skill .md files

### 5. Framework Doc Drift
**Symptoms:** Version mismatch, inconsistent guidance
**Urgency:** MEDIUM
**Component:** claude.md, claude-reference.md

### 6. LCMP Staleness
**Symptoms:** Old/empty LCMP files, no compaction
**Urgency:** LOW
**Component:** context/*.md files

## Urgency Assessment

**CRITICAL** - Framework safety compromised, immediate fix needed
- Write-gating bypassed
- State corruption causing crashes
- Security vulnerability

**HIGH** - Core functionality broken, fix soon
- Hooks not executing
- Task startup failing
- DAIC transitions broken

**MEDIUM** - Features degraded, fix when convenient
- Skills not triggering
- Documentation drift
- Non-critical commands failing

**LOW** - Minor issues, address eventually
- LCMP staleness
- Minor inconsistencies
- Nice-to-have improvements

## Decision Logging

When proposing REPAIR tasks:

```markdown
### REPAIR Task Proposed: [Date]
- **Task ID:** REPAIR-write-gating-2025-11-15
- **Issue:** Write-gating enforcement broken
- **Urgency:** CRITICAL
- **User Response:** [Approved / Deferred / Rejected]
- **Action Taken:** [Created task file / Added to backlog / Noted in gotchas.md]
```

## Related Skills

- **framework_health_check** - For detecting issues that need REPAIR
- **framework_version_check** - For detecting version drift requiring REPAIR
- **cc-sessions-hooks** - For implementing hook fixes during REPAIR
- **cc-sessions-core** - For implementing framework fixes during REPAIR
- **skill-developer** - For implementing skill fixes during REPAIR

---

**Last Updated:** 2025-11-15
**Framework Version:** 2.0
