---
name: coderabbit-fix
description: Implement fixes for specific CodeRabbit review issues. Runs in isolated subagent context with focused task. Verifies fixes with tests before returning. Use one per issue from triage task list.
---

# Fixing Issues

## Overview

This skill implements a single, focused fix from a CodeRabbit issue. It runs in an isolated subagent context with clear constraints to prevent scope creep. Each subagent fixes exactly one issue and nothing more.

**Input**: Task object from `coderabbit-triage` (task_id, file, line, issue, instructions, constraints)

**Output**: Fixed code + detailed summary of changes and verification

**When to use**: Called once per task from the triage plan. Can run in parallel with other instances of this skill.

## Process

### Step 1: Understand the Issue

Before implementing, fully understand the problem:

1. **Read the issue description** from task input
2. **Read CodeRabbit's suggestion** carefully
3. **Open the file** and read the problematic code section (include 5 lines before and after)
4. **Ask yourself**:
   - Why is this broken?
   - What are the consequences if not fixed?
   - What does the suggested fix address?
5. **Identify the root cause**, not just the symptom

### Step 2: Evaluate Suggestion (Technical Rigor)

Don't blindly follow CodeRabbit's suggestion. Verify it:

```text
CodeRabbit suggests: "Add HMAC-SHA256 signature verification"

Questions to ask:
- Is HMAC-SHA256 the right algorithm? (Yes, industry standard for webhooks)
- Are there edge cases? (Replay attacks, timing attacks, key rotation)
- Is the suggestion complete? (Includes replay prevention? Yes, via timestamp)
- Are there better approaches? (Could use RS256? Less suitable here, HMAC is correct)
- Will this break existing behavior? (No, adds validation, doesn't change behavior)

Decision: ✅ Implement as suggested, plus timing attack protection via timingSafeEqual
```

If suggestion seems incomplete or wrong:

- Document your concern
- Propose alternative with reasoning
- Example: "CodeRabbit suggests simple cache, but recommend Redis for distributed systems"

### Step 3: Implement Fix (With Rigor)

Follow the fixer_instructions from your task exactly.

**For critical issues** (security, correctness):

- Add comprehensive error handling
- Add defensive checks (don't assume inputs are valid)
- Include security-focused logging
- Handle edge cases explicitly

Example: Signature verification

```typescript
// ✅ Correct: Defensive, handles all cases
function verifyWebhookSignature(request) {
  // Defensive: Check all required inputs
  if (!request.headers["x-webhook-signature"]) {
    logger.warn({ event: "signature_missing", webhook_id: request.id });
    throw new UnauthorizedError("Missing signature header");
  }

  if (!request.body) {
    logger.warn({ event: "body_empty", webhook_id: request.id });
    throw new BadRequestError("Empty webhook body");
  }

  // Compute signature with constant-time comparison
  const expectedSignature = crypto
    .createHmac("sha256", process.env.WEBHOOK_SECRET)
    .update(request.body)
    .digest("hex");

  const providedSignature = request.headers["x-webhook-signature"];

  // Use timing-safe comparison to prevent timing attacks
  if (!crypto.timingSafeEqual(Buffer.from(expectedSignature), Buffer.from(providedSignature))) {
    logger.warn({
      event: "signature_invalid",
      webhook_id: request.id,
      expected_length: expectedSignature.length,
      provided_length: providedSignature.length,
    });
    throw new UnauthorizedError("Invalid webhook signature");
  }

  return true;
}
```

**For important issues** (bugs, performance):

- Fix the immediate problem
- Add comments explaining the fix
- Verify related functionality doesn't break

**For minor issues** (style, clarity):

- Make focused change
- Don't refactor unnecessarily
- Preserve existing patterns

### Step 4: Add Safety Checks

Think about what can go wrong:

**Signature verification**:

- ✅ Empty header → return 401
- ✅ Timing attacks → use timingSafeEqual
- ✅ Signature mismatch → log + return 401
- ✅ Missing secret → throw at startup

**Idempotency handling**:

- ✅ Missing idempotency key → generate UUID
- ✅ Duplicate key → return cached result
- ✅ Cache grows unbounded → implement TTL cleanup
- ✅ Concurrent identical keys → use Promise deduplication

**Error logging**:

- ✅ Sensitive data → filter from logs
- ✅ PII in error messages → redact
- ✅ Log levels correct → info/warn/error appropriately

### Step 5: Test Locally

**Required tests**:

```bash
# 1. Run related tests first
npm test -- src/webhooks.test.ts

# 2. Check specific test cases pass
# For signature: test valid, invalid, missing, timing attack
# For idempotency: test duplicate keys, cache TTL, concurrent
# For logging: test all error types logged, no sensitive data

# 3. Run full suite
npm test

# 4. Check coverage hasn't decreased
npm test -- --coverage
```

**For critical issues**: All tests must pass. Zero tolerance.

**For important/minor issues**: All existing tests pass + new test for fix.

### Step 6: Verify with CodeRabbit (Optional)

If uncertain fix is complete, re-run CodeRabbit locally:

```bash
coderabbit --prompt-only --type diff HEAD~1
```

If CodeRabbit reports the issue still exists:

- Revisit the fix
- Check if it was actually applied
- Review if suggestion was incomplete

### Step 7: Report Back

Return summary in this format:

```jsonc
{
  "task_id": 1,
  "status": "✅ FIXED",
  "file": "src/webhooks.ts",
  "line": 42,
  "severity": "critical",
  "domain": "payment-webhook-security",

  "changes_summary": {
    "lines_added": 35,
    "lines_deleted": 2,
    "files_modified": ["src/webhooks.ts"]
  },

  "what_changed": [
    "Added HMAC-SHA256 signature verification at webhook handler entry",
    "Implemented replay attack protection via timestamp validation (5 minute window)",
    "Added timing-safe comparison to prevent timing attacks",
    "Added structured error logging for all signature failures",
    "Created verifyWebhookSignature() utility function"
  ],

  "why_this_approach": {
    "algorithm": "HMAC-SHA256 is industry standard for webhook security (see RFC 6234)",
    "timing_safe": "timingSafeEqual prevents timing attacks that could leak signature info",
    "replay_protection": "Timestamp validation (5 min window) prevents replay attacks if key is compromised",
    "error_logging": "Structured logs enable debugging in production without exposing secrets",
    "function_extraction": "Separate function makes testing and reuse possible"
  },

  "code_snippet": {
    "before": "function handleWebhook(req, res) { ... }",
    "after": "function handleWebhook(req, res) { verifyWebhookSignature(req); ... }"
  },

  "tests_passed": {
    "total": 8,
    "webhook_security_tests": "8/8 passing",
    "all_tests": "42/42 passing",
    "new_tests_added": [
      "✅ Valid signature verification succeeds",
      "✅ Invalid signature verification fails with 401",
      "✅ Missing signature verification fails with 401",
      "✅ Timing attack with modified signature fails",
      "✅ Stale timestamp (>5 min) fails with 401",
      "✅ Future timestamp fails with 401"
    ]
  },

  "quality_checklist": {
    "follows_task_instructions": true,
    "respects_constraints": true,
    "all_tests_passing": true,
    "no_new_warnings": true,
    "code_style_consistent": true,
    "error_handling_complete": true,
    "logging_appropriate": true,
    "security_hardened": true
  },

  "estimated_time": "12 minutes",
  "actual_time": "14 minutes",

  "ready_for_next_phase": true,

  "notes": "Implementation includes defense-in-depth: signature + timing attack prevention + replay protection + detailed logging. Aligns with OWASP webhook security guidelines."
}
```

## Key Principles

**Task isolation**: Fix only what's assigned. Don't improve other code.

**Technical rigor**: Understand root cause, not just symptoms. Question suggestions.

**Safety first**: Add defensive checks, error handling, comprehensive logging.

**Test evidence**: Don't claim it's fixed. Prove it with passing tests.

**Constraints matter**: Fixer_instructions and constraints are guardrails. Respect them.

## Common Patterns

**Signature verification**:

- Use crypto.timingSafeEqual
- Include replay attack prevention
- Log all failures
- Test timing attacks

**Idempotency**:

- Extract idempotency key early
- Check cache before processing
- Store result after processing
- Implement TTL-based cleanup

**Error logging**:

- Structured JSON logging
- Include request IDs for tracing
- Filter sensitive data
- Appropriate log levels

## Constraints (Universal)

- **DO**: Implement exactly as instructed
- **DO**: Add error handling and logging
- **DO**: Run all tests before returning
- **DO**: Include reasoning for technical decisions
- **DON'T**: Change unrequested code
- **DON'T**: Refactor or "improve" other functions
- **DON'T**: Remove existing error handling
- **DON'T**: Skip tests - prove it works
- **DON'T**: Ignore the constraints in your specific task

## Integration Points

```text
coderabbit-triage
         ↓
[dispatch multiple coderabbit-fix instances]
         ↓
coderabbit-fix #1 (parallel)
coderabbit-fix #2 (parallel)
coderabbit-fix #3 (parallel)
         ↓
Main agent collects summaries
         ↓
Final verification: full test suite + CodeRabbit re-check
```

## Error Handling

**If fix doesn't compile**:

- Report error immediately
- Include error message
- Ask for clarification on constraints

**If tests fail**:

- Debug systematically
- Include test output in report
- Don't return until tests pass

**If constraint violated**:

- Immediately notify
- Roll back changes
- Ask for revised instructions

Always provide evidence. Never claim success without proof.
