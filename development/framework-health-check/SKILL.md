---
name: framework_health_check
description: Execute comprehensive framework health checks to validate core cc-sessions functionality including write-gating, state persistence, skill precedence, LCMP freshness, and handoff log structure
schema_version: 1.0
---

# framework_health_check

**Type:** ANALYSIS-ONLY
**DAIC Modes:** DISCUSS, ALIGN, IMPLEMENT, CHECK (all modes)
**Priority:** Medium

## Trigger Reference

This skill activates on:
- Keywords: "framework health", "run health check", "validate framework", "framework test", "check framework"
- Intent patterns: "(run|execute|perform).*?health.*?check", "validate.*?framework", "framework.*?health"

From: `skill-rules.json` - framework_health_check configuration

## Purpose

Execute comprehensive framework health checks to validate core cc-sessions functionality. Tests write-gating, state persistence, skill precedence, LCMP freshness, and handoff log structure. This is an ANALYSIS-ONLY skill that reports health status and suggests REPAIR tasks for failures.

## Core Behavior

In any DAIC mode, when explicitly requested or during REPAIR tasks:

1. **Write-Gating Validation**
   - Simulate write attempt in DISCUSS mode
   - Verify write is blocked with correct error message
   - Test that IMPLEMENT mode allows writes
   - Validate CC_SESSION_MODE / CC_SESSION_TASK_ID protection

2. **State Persistence Validation**
   - Check `sessions/sessions-state.json` exists
   - Validate JSON structure and required fields
   - Verify state aligns with recent work
   - Test state read/write operations

3. **Skill Precedence Validation**
   - Verify project skills override defaults
   - Test skill-rules.json syntax and structure
   - Confirm DAIC-aware skill triggers
   - Validate ANALYSIS-ONLY vs WRITE-CAPABLE enforcement

4. **LCMP Freshness Check**
   - Verify LCMP files exist (decisions.md, insights.md, gotchas.md)
   - Check last modification dates
   - Identify suspiciously old/empty files
   - Suggest compaction if appropriate

5. **Handoff Log Structure**
   - Verify `docs/ai_handoffs.md` exists (if applicable)
   - Validate YAML structure of recent entries
   - Check required fields: timestamp, from, to, issue_id, branch, completed, next, context_files
   - Report format violations

## Safety Guardrails

**ANALYSIS-ONLY RULES:**
- ✓ NEVER call write tools (Edit, Write, MultiEdit)
- ✓ NEVER auto-fix health check failures
- ✓ NEVER modify framework configuration
- ✓ Only provide analysis and recommendations
- ✓ Safe to run in any DAIC mode

**Health Check Safety:**
- Never execute destructive tests
- Only read files, never write
- Handle missing files gracefully
- Report clear pass/fail status
- Suggest REPAIR tasks for failures

## Examples

### When to Activate

✓ "Run framework health check"
✓ "Validate the framework is working correctly"
✓ "Check if write-gating is enforced"
✓ "Is the framework healthy?"
✓ During REPAIR tasks to verify fixes

### Typical Output

**Scenario: All Checks Pass**
```markdown
### Framework Health Check: ✓ HEALTHY

**Write-Gating:** ✓ PASS
- Test write blocked in DISCUSS mode with correct error
- Write-capable skills properly gated to IMPLEMENT mode

**State Persistence:** ✓ PASS
- sessions/sessions-state.json exists and valid
- Fields align with session state
- JSON structure correct

**Skill Precedence:** ✓ PASS
- Project skills in .claude/skills/ loaded
- skill-rules.json valid (v2.0.0)
- 10 skills configured with proper DAIC awareness

**LCMP Freshness:** ✓ PASS
- context/decisions.md updated 2 days ago
- context/insights.md updated 5 days ago
- context/gotchas.md updated 1 day ago
- All files active and current

**Handoff Log:** ✓ PASS (or N/A if not used)
- docs/ai_handoffs.md structure valid
- Last 3 entries follow YAML format
- Required fields present

**Overall Status:** ✓ Framework is healthy
**Recommendation:** No action needed
```

**Scenario: Failures Detected**
```markdown
### Framework Health Check: ⚠️ ISSUES FOUND

**Write-Gating:** ✗ FAIL
- Test write in DISCUSS mode was NOT blocked
- CRITICAL: Write-gating enforcement broken
- Expected: Error blocking write
- Actual: Write succeeded

**State Persistence:** ✓ PASS
- sessions/sessions-state.json valid

**Skill Precedence:** ⚠️ WARNING
- skill-rules.json has syntax error on line 45
- Some skills may not load correctly

**LCMP Freshness:** ⚠️ WARNING
- context/decisions.md last updated 90 days ago
- Suspiciously stale, may need review

**Handoff Log:** ✗ FAIL
- docs/ai_handoffs.md missing required field: `context_files`
- Entry from 2025-11-10 uses old schema

**Overall Status:** ⚠️ Framework has issues
**CRITICAL Issues:** 1 (write-gating broken)
**Warnings:** 2 (skill syntax error, stale LCMP)

**Recommended Actions:**
1. IMMEDIATE: Create REPAIR-write-gating task (critical safety issue)
2. Create REPAIR-skill-rules task (syntax error blocking skills)
3. Consider LCMP review if decisions.md content is outdated
4. Update handoff log schema or backfill missing fields
```

### When NOT to Activate

✗ User is asking about application health (not framework)
✗ Question is about performance/load testing
✗ Focus is on feature functionality (not framework integrity)
✗ General debugging (not framework-specific)

## Health Check Procedures

### 1. Write-Gating Test

```markdown
**Test Procedure:**
1. Verify current mode is NOT IMPLEMENT
2. Check if write tools are available
3. Verify hooks prevent write execution
4. Expected: Write blocked with error message
5. Actual: [Result]

**Pass Criteria:**
- Write is blocked
- Error message mentions DAIC mode / write-gating
- No file is actually written

**Fail Conditions:**
- Write succeeds in non-IMPLEMENT mode
- No error message
- Hooks not executing
```

### 2. State Persistence Test

```markdown
**Test Procedure:**
1. Check sessions/sessions-state.json exists
2. Parse JSON (should not throw)
3. Validate required fields: mode, task, flags
4. Check if task aligns with git branch (if applicable)

**Pass Criteria:**
- File exists and is valid JSON
- Required fields present
- Values make sense (e.g., mode is DISCUSS/ALIGN/IMPLEMENT/CHECK)

**Fail Conditions:**
- File missing
- Invalid JSON
- Missing required fields
- Nonsensical values
```

### 3. Skill Precedence Test

```markdown
**Test Procedure:**
1. Check .claude/skills/skill-rules.json exists
2. Parse JSON and validate schema
3. Count configured skills
4. Verify DAIC modes correctly specified
5. Check for syntax errors
6. Run `node scripts/validate-skills.js` for comprehensive validation

**Pass Criteria:**
- skill-rules.json valid
- All skills have type: ANALYSIS-ONLY or WRITE-CAPABLE
- DAIC modes properly configured
- No syntax errors
- All registered skills have corresponding files
- No orphaned skill files
- All required fields present

**Fail Conditions:**
- File missing or invalid JSON
- Skills missing required fields
- Invalid DAIC mode values
- Syntax errors
- Missing skill files
- Orphaned files detected

**Validation Script:**
- Run `node scripts/validate-skills.js` for detailed skill validation
- Checks file/registration consistency
- Validates required fields
- Detects orphaned files
- Reports errors and warnings
```

### 4. LCMP Freshness Test

```markdown
**Test Procedure:**
1. Check context/decisions.md exists
2. Check context/insights.md exists
3. Check context/gotchas.md exists
4. Get last modified dates
5. Flag if >60 days old

**Pass Criteria:**
- All three files exist
- At least one updated in last 30 days
- Files contain content (not empty)

**Warning Conditions:**
- Files exist but very stale (>60 days)
- Files empty or placeholder-only

**Fail Conditions:**
- Required LCMP files missing
```

### 5. Handoff Log Test (Optional)

```markdown
**Test Procedure:**
1. Check if docs/ai_handoffs.md exists
2. Read last 3 entries
3. Validate YAML structure
4. Check required fields present

**Pass Criteria:**
- YAML structure valid
- Required fields: timestamp, from, to, completed, next
- Recent entries (if handoffs active)

**Warning Conditions:**
- Old schema used in some entries
- Missing optional fields

**Fail Conditions:**
- Invalid YAML
- Missing required fields
- File completely malformed
```

## Health Check Report Template

```markdown
### Framework Health Check Report
**Date:** [ISO timestamp]
**Triggered By:** [User request / REPAIR task / Auto]

---

#### Write-Gating
[✓ PASS | ✗ FAIL | ⚠️ WARNING]
[Details]

#### State Persistence
[✓ PASS | ✗ FAIL | ⚠️ WARNING]
[Details]

#### Skill Precedence
[✓ PASS | ✗ FAIL | ⚠️ WARNING]
[Details]
- Run `node scripts/validate-skills.js` for comprehensive skill validation

#### LCMP Freshness
[✓ PASS | ✗ FAIL | ⚠️ WARNING]
[Details]

#### Handoff Log
[✓ PASS | ✗ FAIL | ⚠️ WARNING | N/A]
[Details]

---

**Overall Status:** [✓ HEALTHY | ⚠️ ISSUES | ✗ CRITICAL]
**Critical Issues:** [count]
**Warnings:** [count]

**Recommended Actions:**
1. [Action 1]
2. [Action 2]
...
```

## Integration with REPAIR Tasks

When running health checks during REPAIR tasks:
1. Run full health check suite
2. Compare results to pre-fix baseline
3. Verify fixes resolved targeted issues
4. Document improvements in context/gotchas.md
5. Report any new issues introduced

## Decision Logging

When health check reveals issues:

```markdown
### Framework Health Issue: [Date]
- **Check:** Write-gating validation
- **Result:** FAIL - writes not blocked in DISCUSS mode
- **Impact:** CRITICAL - framework safety compromised
- **Action:** Created REPAIR-write-gating-2025-11-15 task
- **Prevention:** Add health check to pre-release checklist
```

## Related Skills

- **framework_version_check** - For version sync validation (subset of health check)
- **framework_repair_suggester** - To create REPAIR tasks for failures
- **cc-sessions-hooks** - If hooks are causing health check failures
- **skill-developer** - If skill system issues detected

---

**Last Updated:** 2025-11-15
**Framework Version:** 2.0
