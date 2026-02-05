---
name: debug-issues
description: Debug bugs and errors using intel-first approach with systematic root cause analysis. Use proactively when errors occur, tests fail, or unexpected behavior appears. MUST trace from symptom to root cause with CoD^Σ reasoning.
---

# Debugging Skill

## Overview

This skill performs systematic bug diagnosis using intelligence-first approach to trace from symptom to root cause with complete CoD^Σ reasoning chain.

**Core principle:** Capture symptom → Parse error → Intel trace → Root cause → Propose fix

**Announce at start:** "I'm using the debug-issues skill to diagnose this problem."

## Quick Reference

| Phase | Key Activities | Output |
|-------|---------------|--------|
| **1. Capture Symptom** | Reproduction steps, error message, environment | Symptom description |
| **2. Parse Error** | Extract error type, file:line, stack trace | Parsed error object |
| **3. Intel Trace** | project-intel.mjs queries from error to cause | Intel evidence chain |
| **4. Root Cause** | Identify specific file:line with CoD^Σ trace | Root cause |
| **5. Report** | Generate bug report with fix proposal | bug-report.md |

## Templates You Will Use

- **@.claude/templates/bug-report.md** - Complete bug report with fix (Phase 5)
- **@.claude/templates/mcp-query.md** - For verifying library behavior (Phase 4)

## Intelligence Tool Guide

- **@.claude/shared-imports/project-intel-mjs-guide.md** - For systematic intel queries

## The Process

Copy this checklist to track progress:

```
Debugging Progress:
- [ ] Phase 1: Symptom Captured (reproduction steps documented)
- [ ] Phase 2: Error Parsed (file:line extracted)
- [ ] Phase 3: Intel Trace Complete (queries executed)
- [ ] Phase 4: Root Cause Identified (specific file:line)
- [ ] Phase 5: Bug Report Generated (with fix proposal)
```

### Phase 1: Capture Symptom

Document the complete symptom:

1. **Error Message:**
   ```
   TypeError: Cannot read property 'discount' of undefined
   at calculateTotal (src/pricing/calculator.ts:67)
   at processCheckout (src/checkout/checkout.ts:123)
   ```

2. **Reproduction Steps:**
   ```
   1. Add items to cart
   2. Apply discount code "SAVE20"
   3. Click "Checkout"
   4. ERROR: 500 response
   ```

3. **Frequency & Environment:**
   ```
   - Frequency: 15% of checkout attempts
   - Environment: Production
   - User impact: High (blocks checkout)
   ```

**Enforcement:**
- [ ] Complete error message captured
- [ ] Reproduction steps documented
- [ ] Frequency and environment noted

### Phase 2: Parse Error

Extract structured information from error:

#### Parse Stack Trace

```
ERROR: TypeError: Cannot read property 'discount' of undefined
  at calculateTotal (src/pricing/calculator.ts:67)  ← ROOT ERROR
  at processCheckout (src/checkout/checkout.ts:123)
  at POST /api/checkout (src/api/routes.ts:45)

Parsed:
{
  error_type: "TypeError",
  message: "Cannot read property 'discount' of undefined",
  root_location: "src/pricing/calculator.ts:67",
  root_function: "calculateTotal",
  call_chain: [
    "src/api/routes.ts:45",
    "src/checkout/checkout.ts:123",
    "src/pricing/calculator.ts:67"
  ]
}
```

#### Identify Entry Point

```
Entry point: src/pricing/calculator.ts:67
Function: calculateTotal
Issue: Accessing .discount on undefined object
```

**Enforcement:**
- [ ] Error type identified
- [ ] Root file:line extracted
- [ ] Function name identified
- [ ] Call chain documented

### Phase 3: Intel Trace

**See:** @.claude/skills/debug-issues/workflows/intel-trace.md

**Summary:**

Systematic 4-query workflow using project-intel.mjs to trace from error to root cause.

**Query Workflow:**
1. **Locate Function**: Find file containing the error-causing function
2. **Analyze Symbols**: Get exact line numbers for functions
3. **Trace Dependencies**: Check what the function imports
4. **Check Dependency**: Analyze suspicious imports for return types

**Token Efficiency:**
- Intel queries: ~350 tokens
- Targeted reads: ~400 tokens
- **Total: ~750 tokens vs 8600 (91% savings)**

### Phase 4: Root Cause Analysis

**See:** @.claude/skills/debug-issues/workflows/root-cause-analysis.md

**Summary:**

Use targeted reads (ONLY lines identified by intel) to identify root cause with complete CoD^Σ trace.

**CoD^Σ Trace Pattern:**
```
Step 1: → ParseError (from Phase 2)
Step 2: ⇄ IntelQuery (locate function)
Step 3: ⇄ IntelQuery (analyze symbols)
Step 4: → TargetedRead (error location)
Step 5: ⇄ IntelQuery (check dependency)
Step 6: → TargetedRead (dependency function)
Step 7: ⊕ MCPVerify (best practices)
Step 8: ∘ Conclusion (root cause + fix)
```

**Requirements:**
- Specific file:line for root cause
- Complete evidence chain
- MCP verification for library behavior
- Token efficiency analysis

### Phase 5: Bug Report Generation

**See:** @.claude/skills/debug-issues/workflows/bug-report-generation.md

**Summary:**

Generate comprehensive bug report using @.claude/templates/bug-report.md with:

**Required Sections:**
1. **Symptom** - From Phase 1
2. **CoD^Σ Trace** - From Phase 4
3. **Root Cause** - Specific file:line + explanation
4. **Fix Specification** - Exact code changes (before/after)
5. **Verification** - Test plan + acceptance criteria

**File Naming:** `YYYYMMDD-HHMM-bug-<id>.md`

## Common Error Patterns

**See:** @.claude/skills/debug-issues/examples/error-patterns.md

**Summary:**

Three frequently encountered patterns with systematic debugging approaches:

1. **React Infinite Re-render** - useEffect dependency on mutated value
2. **N+1 Query Problem** - Database queries inside loops
3. **Memory Leak** - Missing cleanup in useEffect

Each pattern includes:
- Symptom identification
- Step-by-step debugging process
- Common root causes
- Fix approaches with code examples
- Verification steps

## Enforcement Rules

**See:** @.claude/skills/debug-issues/references/debugging-rules.md

**Summary:**

Three mandatory rules for all bug diagnosis:

**Rule 1: Complete CoD^Σ Trace**
- Every step must have evidence source
- File:line references required
- MCP queries documented
- Conclusion follows logically

**Rule 2: Intel Before Reading**
- ALWAYS query project-intel.mjs first
- Use targeted reads (sed -n 'X,Yp')
- Document token savings
- Never read full files

**Rule 3: Fix with Verification**
- Propose specific code changes
- Include test plan
- Define acceptance criteria
- Verify fix addresses root cause

**Common Pitfalls:**
- Assumptions without MCP verification
- Skipping intel queries (91% token waste)
- Incomplete reproduction steps
- No fix proposal

## When to Use This Skill

**Use debug-issues when:**
- User reports an error or bug
- Tests are failing
- Unexpected behavior occurs
- Performance is degraded
- Memory issues detected

**Don't use when:**
- User wants general code analysis (use analyze-code skill)
- User wants to plan implementation (use create-plan skill)
- No specific error (use analyze-code for investigation)

## Related Skills & Commands

- **Analyze-code skill** - For general code analysis (not bug-specific)
- **Implement-and-verify skill** - For implementing the fix after debugging
- **/bug command** - User-invoked debugging (can invoke this skill)

## Success Metrics

**Accuracy:**
- Root cause identified: 95%+
- Fix proposal validated: 100%

**Efficiency:**
- Token usage: 80%+ savings vs direct reading
- Time to diagnosis: 5-15 minutes

**Completeness:**
- CoD^Σ trace: 100% complete
- MCP verification: 100% for library issues

## Prerequisites

Before using this skill:
- ✅ Error or bug has been reported/detected
- ✅ Error message, logs, or reproduction steps available
- ✅ project-intel.mjs exists and is executable
- ✅ PROJECT_INDEX.json exists (run `/index` if missing)
- ⚠️ Optional: MCP tools configured (Ref for library behavior verification)
- ⚠️ Optional: Test framework set up (for verification tests)

## Dependencies

**Depends On**:
- None (this skill is standalone and can be used at any point)

**Integrates With**:
- **analyze-code skill** - Use before this skill for general code understanding
- **implement-and-verify skill** - Use after this skill to implement the fix
- **create-implementation-plan skill** - Use after this skill if fix requires multiple changes

**Tool Dependencies**:
- project-intel.mjs (intelligence queries)
- MCP Ref tool (library documentation, optional)
- Read, Grep tools (targeted code reading)
- Bash tool (running sed for targeted reads, running tests)

## Next Steps

After debugging completes, typical progression:

**For simple fixes (1 file, <10 lines)**:
```
debug-issues (identifies root cause + proposes fix)
    ↓
User approves fix OR implement-and-verify skill implements it
    ↓
Run tests to verify fix works
```

**For complex fixes (multiple files, refactoring needed)**:
```
debug-issues (identifies root cause)
    ↓
create-implementation-plan (plan multi-file fix)
    ↓
generate-tasks (break down fix tasks)
    ↓
implement-and-verify (implement fix with TDD)
```

**For blocked/requires research**:
```
debug-issues (unable to identify root cause)
    ↓
analyze-code skill (deeper investigation)
    ↓
MCP queries (verify library behavior)
    ↓
debug-issues skill (re-run with additional context)
```

**User Action Required**:
- Provide reproduction steps if not already known
- Approve fix proposal before implementation
- Run verification tests after fix applied

**Outputs Created**:
- `YYYYMMDD-HHMM-bug-<id>.md` - Complete bug report with CoD^Σ trace and fix
- Updated code (if implementing fix immediately)
- Test files (if verification tests created)

**Commands**:
- **/implement plan.md** - If fix requires planned implementation
- **/verify plan.md** - If fix needs formal verification

## Failure Modes

### Common Failures & Solutions

**1. PROJECT_INDEX.json missing or stale**
- **Symptom**: Intel queries fail or return outdated results
- **Solution**: Run `/index` command to regenerate index
- **Prevention**: Hook auto-generates index on file changes

**2. Incomplete error information**
- **Symptom**: No stack trace, vague error message, can't reproduce
- **Solution**: Ask user for complete error log, reproduction steps, environment details
- **Requirement**: Need at least error message + approximate location to start

**3. Reading full files instead of intel-first**
- **Symptom**: Token usage high (>5K for simple bug), slow diagnosis
- **Solution**: ALWAYS query project-intel.mjs before reading any files
- **Pattern**: Search → Symbols → Dependencies → Targeted Read (never full file read)

**4. No CoD^Σ trace documented**
- **Symptom**: Bug report lacks reasoning chain, can't verify logic
- **Solution**: Document every step from symptom to root cause
- **Enforcement**: Phase 4 requires complete CoD^Σ trace in bug report

**5. Proposing fix without verification plan**
- **Symptom**: Fix suggested but no way to test it
- **Solution**: Always include test plan with acceptance criteria
- **Pattern**: "Test with X (should Y), Test with Z (should not error)"

**6. Assumptions without MCP verification**
- **Symptom**: Assuming library behavior, fix doesn't work
- **Solution**: Use Ref MCP to verify library behavior before proposing fix
- **Example**: "React useEffect cleanup" → verify in React docs before proposing solution

**7. Jumping to conclusions without intel trace**
- **Symptom**: Guessing root cause, diagnosis wrong
- **Solution**: Systematically trace from error location through dependencies
- **Enforcement**: Phases 2-3 must execute before identifying root cause

**8. Symptom captured incompletely**
- **Symptom**: Missing frequency, environment, user impact details
- **Solution**: Phase 1 checklist enforces complete symptom capture
- **Components**: Error + Reproduction Steps + Frequency + Environment + Impact

**9. Not using sed for targeted reads**
- **Symptom**: Reading entire files when only need specific lines
- **Solution**: Use `sed -n 'X,Yp' file` after intel identifies line range
- **Benefit**: Read 10-20 lines instead of 1000+ lines (99% token savings)

**10. Parallel investigation instead of systematic**
- **Symptom**: Trying multiple approaches simultaneously, getting confused
- **Solution**: Follow phase order: Symptom → Parse → Intel → Root Cause → Report
- **Enforcement**: Copy progress checklist and mark phases sequentially

## Related Skills & Commands

**Direct Integration**:
- **analyze-code skill** - Use before this skill for general understanding, or when debugging blocks
- **implement-and-verify skill** - Use after this skill to implement fix with TDD
- **create-implementation-plan skill** - Use after this skill if fix is complex
- **/bug command** - User-facing command that invokes this skill
- **code-analyzer subagent** - Subagent that can route to this skill

**Workflow Context**:
- Position: **Troubleshooting** (parallel to main workflow, invoked when errors occur)
- Triggers: Error reports, test failures, unexpected behavior
- Output: bug-report.md with root cause, CoD^Σ trace, and fix proposal

**Quality Gates**:
- **Intel-First**: MUST query project-intel.mjs before reading files (Article I)
- **Evidence-Based**: Complete CoD^Σ trace required (Article II)
- **Verification Plan**: Fix must have testable acceptance criteria (Article III)

**Common Entry Points**:
1. User reports bug → debug-issues skill
2. Tests fail during /implement → implement-and-verify invokes debug-issues skill
3. analyze-code identifies issue → routes to debug-issues for diagnosis

**Common Exit Points**:
1. Simple fix → Implement immediately
2. Complex fix → create-implementation-plan skill
3. Cannot reproduce → Request more info from user
4. Requires research → analyze-code skill for deeper investigation

## Version

**Version:** 1.1.0
**Last Updated:** 2025-10-23
**Owner:** Claude Code Intelligence Toolkit

**Change Log**:
- v1.1.0 (2025-10-23): Refactored to progressive disclosure pattern (<500 lines)
- v1.0.0 (2025-10-22): Initial version with systematic debugging workflow
