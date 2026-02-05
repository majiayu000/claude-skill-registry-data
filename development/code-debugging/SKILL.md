---
name: code-debugging
description: Systematic 5-step debugging ladder for broken story implementations. Use when a story is at implementing (broken) stage.
---

# Code Debugging

Fix broken story implementations using a systematic 5-step debugging ladder. Each step applies a specific debugging technique with increasing sophistication.

## When to Use

Use this skill when:
- A story is at `implementing (broken)` stage
- Implementation failed with `status: partial` or `status: failed`
- Tests are failing after an implementation attempt

## The 5-Step Debug Ladder

```
Step 1: code-sentinel       → Known anti-patterns
Step 2: root-cause-tracing  → Trace backward to source
Step 3: librarian agent     → Research outdated APIs
Step 4: Opus 4.5            → Fresh analysis
Step 5: systematic-debugging → Full 4-phase framework
   ↓
Escalate → implementing (escalated)
```

Each step is attempted in order. If a step fixes the issue, implementation is retried. If all 5 steps fail, the story is escalated for human review.

---

## Step 1: Code Sentinel

**Tool:** `Skill(skill="code-sentinel")`

Check for known anti-patterns that cause test failures:

1. Run `pytest tests/test_code_patterns.py -v`
2. If tests fail, read the anti-pattern file for each failure
3. Apply the documented fix
4. Verify tests pass

| Common Anti-Patterns |
|----------------------|
| Heredocs in GitHub Actions |
| Grep exit code handling |
| Git operations without staging |
| Non-deterministic file selection |
| Absolute imports for siblings |

**Exit condition:** All pattern tests pass → retry implementation

---

## Step 2: Root Cause Tracing

**Tool:** `Skill(skill="superpowers:root-cause-tracing")`

Trace the error backward to find its source:

1. **Capture the error** — Get full stack trace and error message
2. **Trace data flow** — Follow variables backward from error point
3. **Identify mutation** — Find where data changed unexpectedly
4. **Fix at source** — Correct the root cause, not symptoms

**Key Questions:**
- What value was expected vs. actual?
- Where did this value come from?
- What transformed it along the way?

**Exit condition:** Root cause fixed → retry implementation

---

## Step 3: Librarian Agent

**Tool:** `Task(subagent_type="general-purpose")` with web search

Research outdated APIs, version mismatches, or deprecated patterns:

1. **Identify the API/library** — What external dependency is involved?
2. **Check version** — Is the installed version current?
3. **Search for changes** — Look for breaking changes, deprecations
4. **Update code** — Apply modern patterns from current docs

**Prompt template:**
```
Research the error: "[ERROR MESSAGE]"

Check if this relates to:
1. Deprecated API patterns
2. Version mismatches
3. Breaking changes in recent releases

Search the official documentation and provide:
1. The correct modern pattern
2. Migration steps if needed
```

**Exit condition:** API updated to current pattern → retry implementation

---

## Step 4: Opus 4.5 Fresh Analysis

**Tool:** Claude Opus 4.5 with optimized handover prompt

Get a fresh perspective with the most capable model:

1. **Prepare handover** — Key context only, not full chat history
2. **Include specifics:**
   - Exact error message and stack trace
   - What has been tried (steps 1-3)
   - Relevant code snippets
   - Test file and line numbers
3. **Request targeted fix** — Ask for specific code changes

**Handover format:**
```markdown
## Context
Story [ID] implementation failed at [stage].

## Error
[Exact error message and stack trace]

## Previous Attempts
1. code-sentinel: [result]
2. root-cause-tracing: [result]
3. librarian agent: [result]

## Relevant Code
[Key snippets only]

## Request
Analyze the error and provide specific code fixes.
```

**Exit condition:** Opus fix applied → retry implementation

---

## Step 5: Systematic Debugging

**Tool:** `Skill(skill="superpowers:systematic-debugging")`

Full 4-phase debugging framework as final attempt:

### Phase 1: Reproduce
- Isolate the minimal failing case
- Ensure consistent reproduction

### Phase 2: Diagnose
- Add logging at key points
- Use debugger/breakpoints
- Binary search for error location

### Phase 3: Fix
- Apply minimal targeted fix
- Don't refactor unrelated code
- Document why fix works

### Phase 4: Verify
- Confirm original test passes
- Run related tests
- Check for regressions

**Exit condition:** Fix verified → retry implementation

---

## Step 6: Escalate

If all 5 steps fail:

1. **Update story status:**
   ```sql
   UPDATE story_nodes
   SET hold_reason = 'escalated',
       debug_attempts = 5
   WHERE id = '[story_id]';
   ```

2. **Create escalation summary:**
   ```markdown
   ## Escalation: Story [ID]

   ### Error
   [Final error state]

   ### Debug Attempts
   1. code-sentinel: [result]
   2. root-cause-tracing: [result]
   3. librarian agent: [result]
   4. Opus 4.5: [result]
   5. systematic-debugging: [result]

   ### Recommendation
   [What human should investigate]
   ```

3. **Notify** — Post to story's GitHub issue

---

## Workflow Integration

The debug orchestrator is invoked by `new-0rchestrator.yml` when:

```yaml
# Query for broken stories
SELECT id, title, debug_attempts
FROM story_nodes
WHERE stage = 'implementing'
  AND hold_reason = 'broken'
  AND debug_attempts < 5
ORDER BY updated_at ASC
LIMIT 1;
```

After each debug attempt:

```yaml
# Update attempt counter
UPDATE story_nodes
SET debug_attempts = debug_attempts + 1,
    updated_at = datetime('now')
WHERE id = '[story_id]';
```

---

## Database Fields

| Field | Type | Description |
|-------|------|-------------|
| `debug_attempts` | INTEGER | Count of debug ladder steps tried (0-5) |
| `hold_reason` | TEXT | `'broken'` during debugging, `'escalated'` after 5 failures |
| `notes` | TEXT | Append debug attempt results for history |

---

## Example Usage

```python
# Pseudo-code for debug orchestrator invocation

story = get_broken_story()
attempt = story.debug_attempts + 1

if attempt == 1:
    result = run_code_sentinel(story)
elif attempt == 2:
    result = run_root_cause_tracing(story)
elif attempt == 3:
    result = run_librarian_agent(story)
elif attempt == 4:
    result = run_opus_analysis(story)
elif attempt == 5:
    result = run_systematic_debugging(story)
else:
    escalate(story)
    return

if result.success:
    story.hold_reason = None  # Clear broken hold
    story.debug_attempts = 0   # Reset counter
    retry_implementation(story)
else:
    story.debug_attempts = attempt
    save(story)
```
