---
name: dev-coding-debug
description: "Systematic debugging workflow enforcing 'The Iron Law': No fixes without root cause investigation first."
---

# Systematic Debugging (Dev Coding Debug)

## Core Principles (The Iron Law)

> **NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

If you haven't completed Phase 1 (Root Cause) and Phase 2 (Pattern Analysis), you cannot propose fixes. Symptom fixes are failure.

## 🏗️ The Four Phases

### Phase 1: Root Cause Investigation
**Goal: Understand WHAT and WHY.**
1.  **Read Errors**: sticky to the error message. Don't skip stack traces.
2.  **Reproduce**: Can you trigger it reliably? If not, gather more data.
3.  **Instrumentation**: For multi-component systems, log data flow at boundaries.
4.  **Trace**: Follow the bad value backwards to its source (`root-cause-tracing`).

### Phase 2: Pattern Analysis
**Goal: Find the standard before fixing.**
1.  **Find Working Examples**: Locate similar code that works.
2.  **Compare**: Read reference implementations completely.
3.  **Identify Differences**: List every difference, however small.

### Phase 3: Hypothesis and Testing
**Goal: Scientific Method.**
1.  **Single Hypothesis**: "I think X is the root cause because Y".
2.  **Test Minimally**: Change ONE variable at a time to test the hypothesis.
3.  **Verify**: If it didn't work, revert and form a NEW hypothesis. NO layering fixes.

### Phase 4: Implementation
**Goal: Fix the root cause, not the symptom.**
1.  **Failing Test**: Create a minimal reproduction test case (Red).
2.  **Single Fix**: Address the identified root cause (Green).
3.  **Verify**: Ensure no regressions.

## �️ Supporting Techniques

### 1. Root Cause Tracing ("Why did this happen?")
**Don't just fix the bad value. Find where it came from.**
- **Technique**: Ask "What called this with a bad value?" repeatedly until you find the source.
- **Rule**: Fix at the source, not at the symptom.

### 2. Defense-in-Depth ("Make it impossible")
**Don't just validate at one place.**
- **Layer 1 (Entry)**: Reject invalid input at IDL/API boundary.
- **Layer 2 (Logic)**: Ensure data makes sense for the operation.
- **Layer 3 (Guard)**: Environment checks (e.g., test vs prod).
- **Layer 4 (Debug)**: Logging for forensics.

### 3. Condition-Based Waiting (No `sleep`)
**Never guess how long something takes.**
- **Bad**: `sleep(50)`
- **Good**: `waitFor(() => condition)`
- **Why**: Flaky tests often come from arbitrary timeouts.

## �🚩 Red Flags (STOP immediately)
- "Quick fix for now"
- "Just try changing X"
- "One more fix attempt" (Limit: 3 attempts. Then question Architecture.)
- Proposing solutions before tracing.

## ✅ Quality Standards
- **Reproduction Script**: Must exist before fixing.
- **Log Cleanup**: All temporary instrumentation removed.
- **Safe YAML**: Frontmatter descriptions quoted.

## Checklist
- [ ] **Phase 1**: Did you identify the *exact* line/reason for failure?
- [ ] **Phase 2**: Did you compare with a working example?
- [ ] **Phase 4**: Is there a test case that failed before and passes now?
- [ ] **Cleanup**: Are all `print`/`console.log` removed?
