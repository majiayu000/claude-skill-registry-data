---
name: self-healing
description: >
  Automatically diagnose and fix broken workflows, failing scripts, errors, and bugs
  without giving up. Trigger when a script fails, a workflow breaks, there's an error
  message, code isn't working as expected, or the user says "it's broken", "this isn't
  working", "I'm getting an error", "fix this", or pastes a stack trace. Also trigger
  proactively when Claude encounters an error mid-task. When to trigger: any time a
  bash command exits non-zero; when a build step fails (npm install, pip, cargo, etc.);
  when a runtime error appears in logs or the terminal; when the user reports unexpected
  behavior ("the button doesn't work", "it returns empty"); and proactively whenever an
  internal error occurs during task execution. Key capabilities: a structured diagnostic
  loop (error → triage → attempt 1 → attempt 2 → escalate if unresolved), categorized
  fix strategies for dep/import errors, permission/path errors, type/runtime errors,
  network/API errors, and logic/output errors. Never applies patches without root-cause
  investigation. Escalates to superpowers-systematic-debugging after two failed attempts.
  Ideal for any developer who encounters errors mid-session and wants resolution without
  manual debugging. Also useful for automated CI pipelines, pre-deploy smoke tests, and
  as a first-response layer before filing a bug report.
---

# Self-Healing Workflow Skill

## Core Philosophy

Quick wins for superficial issues (missing deps, typos, wrong paths).
If the issue persists after 2 attempts, escalate to `superpowers-systematic-debugging`.
Never apply patches without investigating root cause — triage first, then escalate.

## Diagnostic Loop
```
Error encountered
      ↓
1. Read full error message carefully
2. Identify error type (see categories below)
3. Attempt 1 fix strategy
4. Re-run / re-test
5. If still failing → try one more strategy (attempt 2)
6. After 2 failed attempts → invoke `superpowers-systematic-debugging`
   - Summarize what was tried and what happened
   - Pass the root cause hypothesis forward
```

## Error Categories & Fix Strategies

### Dependency / Import Errors
1. Check if package is installed (`pip list`, `npm list`)
2. Install missing package with correct version
3. Check for name conflicts or deprecated packages

### Permission / Path Errors
1. Verify file/directory exists
2. Check read/write permissions
3. Use absolute paths instead of relative

### Type / Runtime Errors
1. Add defensive type checks
2. Log intermediate values to trace the issue
3. Add null/undefined guards

### Network / API Errors
1. Check if service is reachable
2. Verify credentials and headers
3. Add retry logic with exponential backoff
4. Check rate limits

### Logic / Output Errors
1. Add debug logging at each step
2. Test with minimal input to isolate the issue
3. Compare actual vs expected output explicitly

## Self-Repair Rules
- Always show what the error was and what fix was attempted
- Explain *why* the fix should work
- After fixing, verify the fix didn't break anything else
- If using workarounds, flag them as technical debt

## Escalation to Systematic Debugging

If 2 attempts don't resolve the issue, stop self-healing and invoke:
- `superpowers-systematic-debugging` — for bugs, test failures, technical issues

When escalating, provide:
1. What was tried and why it failed
2. Root cause hypothesis (if any)
3. The original error message

Do NOT continue guessing — escalate after 2 attempts.