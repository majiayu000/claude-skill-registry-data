---
name: Five Whys Root Cause Analysis
description: This skill should be used when the user reports "error", "bug", "problem", needs to "fix" something, mentions "debug", "failing", "broken", "issue", "not working", "crash", or any problem-solving scenario. Enforces systematic root cause identification using five whys methodology before attempting solutions.
version: 0.1.0
---

# Five Whys Root Cause Analysis

## Purpose

This skill enforces systematic root cause identification before solution attempts. Apply the five whys methodology to prevent speculation-driven debugging that wastes effort, creates harmful changes, and results in never-ending fix loops.

## Core Problem

Claude Code's default behavior when encountering problems:
1. Observe symptom
2. Speculate about cause
3. Implement speculative fix
4. Fix doesn't work or creates new problems
5. Repeat indefinitely

**Result:** Wasted effort, potentially harmful changes, user frustration.

## Five Whys Methodology

### The Process

Start with the observed symptom and iteratively ask "why?" until reaching an actionable root cause.

**Example progression:**
1. **Symptom:** Login returns 500 error
2. **Why #1:** Why does login return 500? → Database connection timeout
3. **Why #2:** Why does database timeout? → Connection pool exhausted
4. **Why #3:** Why is pool exhausted? → Connections not being released
5. **Why #4:** Why aren't connections released? → Missing connection.release() call in session handler

**Root cause identified:** Missing connection.release() call - this is actionable.

### Iteration Guidelines

**Continue asking "why" until:**
- The cause is **actionable** (can be fixed with code/config changes)
- The cause **directly explains** the observed symptom
- Next "why" would be **outside our control** (external system, architectural decision)

**Don't stop at:**
- Symptom restatements ("it's broken because it doesn't work")
- Vague causes ("there's a configuration issue")
- First plausible explanation without verification
- Standard iteration counts (five is just a name - continue until root cause found)

### Evidence-Based Investigation

**For each "why", gather evidence:**

1. **Read relevant code:**
   - Files mentioned in error messages
   - Call stack locations
   - Related modules and dependencies

2. **Examine outputs:**
   - Error messages and stack traces
   - Log files
   - Console output
   - Test results

3. **Check configurations:**
   - Environment variables
   - Config files
   - Build settings
   - Dependency versions

4. **Verify assumptions:**
   - Don't assume - check actual behavior
   - Read the code that's actually running
   - Check what values are actually present

**Base each "why" answer on concrete evidence, not speculation.**

## Root Cause Determination

### Criteria for Root Cause

A root cause is identified when ALL these conditions are met:

1. **Actionable:**
   - Can be fixed with code, configuration, or environment changes
   - Within our control to modify
   - Clear fix approach exists

2. **Directly Explanatory:**
   - Cause fully explains the observed symptom
   - No gaps in the causal chain
   - Removing this cause would eliminate the symptom

3. **Terminal:**
   - Next "why" would go outside our control (system architecture, external dependencies, business requirements)
   - OR: Next "why" would not lead to a more actionable fix
   - OR: This is the deepest layer we can address

### Example: Root Cause vs Symptom

**Symptom:** "Tests are failing"
- ❌ NOT root cause: "The test expectations are wrong" (what made them wrong?)
- ❌ NOT root cause: "The code doesn't match tests" (why doesn't it match?)
- ✅ ROOT CAUSE: "Function returns null when user.profile is undefined, but tests expect empty object"

**Symptom:** "API returns 404"
- ❌ NOT root cause: "Route doesn't exist" (why doesn't it exist?)
- ❌ NOT root cause: "Router not configured" (what's the actual misconfiguration?)
- ✅ ROOT CAUSE: "Route path is '/api/v1/users' but code defines '/api/users' - missing '/v1' prefix"

### When to Stop

**Stop investigating when:**
- Identified an actionable fix with clear implementation
- Cause is a concrete code/config/data issue
- Evidence confirms this cause produces the symptom

**Continue investigating when:**
- Cause is vague or speculative
- No clear fix path exists
- Haven't verified the cause with evidence
- Fixing this wouldn't fully resolve symptom

## Anti-Patterns to Avoid

### Speculation Without Evidence

❌ **Bad:**
```
Why is login failing?
→ "Probably a timeout issue" [no evidence]
→ "Let me increase the timeout" [speculative fix]
```

✅ **Good:**
```
Why is login failing?
→ [Read error logs] → Database connection timeout after 5 seconds
→ [Read database config] → Connection pool size is 5
→ [Read application metrics] → 50 concurrent requests
→ Root cause: Connection pool too small for request volume
```

### Stopping Too Early

❌ **Bad:**
```
Why are tests failing?
→ "Tests are outdated"
→ [Starts rewriting tests without understanding why they're outdated]
```

✅ **Good:**
```
Why are tests failing?
→ Tests expect user.email, code returns user.emailAddress
Why the field name difference?
→ API v2 migration changed field names
Why weren't tests updated?
→ Tests live in separate repo, not updated in migration PR
Root cause: Migration process doesn't include cross-repo test updates
```

### Treating Symptoms

❌ **Bad:**
```
Error: "Cannot read property 'name' of undefined"
→ "Let me add null check" [treats symptom]
```

✅ **Good:**
```
Why is object undefined?
→ API call returns undefined when user not found
Why is API call made for non-existent user?
→ User ID comes from URL parameter without validation
Why no validation?
→ Route handler assumes ID is always valid
Root cause: Missing user ID validation in route handler
```

## Progressive Output Format

Show each investigation level as it completes:

```markdown
## Root Cause Analysis

### Investigation Level 1
**Observation:** [What was observed]
**Evidence:** [What was checked - files, logs, outputs]
**Finding:** [What this reveals]
**Next Question:** Why [finding]?

### Investigation Level 2
**Observation:** [Deeper observation]
**Evidence:** [More specific evidence]
**Finding:** [What this reveals]
**Next Question:** Why [finding]?

[Continue until root cause identified]

### Root Cause Identified
**Cause:** [Specific, actionable cause]
**Evidence:** [Concrete evidence supporting this]
**Fix Approach:** [How this can be addressed]
**Why This is Root:** [Meets actionability, explanatory, and terminal criteria]
```

## Integration with Problem Solving

### When Skill Activates

This skill triggers automatically when:
- User message contains problem keywords (error, bug, fix, debug, etc.)
- Tool output contains errors or exceptions
- User is clearly trying to solve a problem

### Agent Invocation

When this skill triggers, it should invoke the root-cause-analyzer agent:
- Agent runs autonomously through five whys
- Shows progressive output for each iteration
- Determines when root cause is reached
- Completes automatically

### User Override

User can bypass analysis by:
- Interrupting the agent manually
- Explicitly stating "skip root cause analysis"
- Requesting immediate fix attempts

**But default behavior is always root cause first.**

## Workflow

1. **Detect problem:** Skill triggers on keywords or errors
2. **Launch analysis:** Invoke root-cause-analyzer agent
3. **Autonomous iteration:** Agent works through whys without user prompts
4. **Progressive display:** Show each iteration as investigation proceeds
5. **Root cause identified:** Agent determines when criteria met
6. **Proceed to solution:** Now fix the identified root cause

## Success Criteria

Root cause analysis is complete when:
- ✅ Specific, actionable cause identified
- ✅ Evidence gathered confirms the cause
- ✅ Cause directly explains observed symptom
- ✅ Clear fix approach exists
- ✅ Fixing this cause will resolve the problem

**Output statement:**
"Root cause identified: [specific cause]. This is actionable and directly explains [symptom]. Proceeding to solution..."
