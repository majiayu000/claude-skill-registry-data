---
name: debug-protocol
description: "Use when encountering any bug, error, test failure, or unexpected behavior — before proposing any fix. Triggers on: seeing an error message, a failing test, 'it's broken', 'not working', 'weird behavior'. Works alongside the /debug command."
---

# Debug Protocol Skill

Random fixes create new bugs. This skill enforces root-cause investigation before fixes.

**Relationship with /debug command:** `/debug` creates a structured debug document and
runs multi-phase investigation. This skill is the lightweight auto-trigger version —
it fires before you touch any code and ensures the four phases are followed.
For complex bugs, use `/debug` to create the full document.

## The Rule

```
NO FIX WITHOUT A WRITTEN ROOT CAUSE AND FALSIFICATION TEST.
```

If you cannot write a falsification test, you don't have a hypothesis — you have a guess.

## When to use this skill

- Any error message appears in output
- A test fails
- Behaviour doesn't match expectation
- Previous fix didn't work
- You're about to edit a file to "try something"

## The Four Phases

### Phase 1 — Reproduce and locate (before any fix)

```bash
# 1. What does git say changed recently?
git log --oneline -5

# 2. Can you reproduce the error consistently?
# Run the failing command again — show the exact error

# 3. Where in the code does it fail?
# Read the stack trace. Note the file:line.
```

Write down:
- Exact error message (copy-paste, not paraphrase)
- File and line where it breaks
- What changed recently that could cause this

### Phase 2 — Form a hypothesis

Write ONE hypothesis:
```
"I think [specific thing] is wrong because [evidence].
Falsification test: if I [run this command/check this value], I should see [X] if wrong."
```

Do not propose a fix yet.

### Phase 3 — Test the hypothesis (smallest possible change)

Run the falsification test. Show the output.

- If output confirms hypothesis → proceed to Phase 4
- If output contradicts → form a new hypothesis, return to Phase 2
- After 3 failed hypotheses → stop and ask the human. Do not guess #4.

### Phase 4 — Fix and verify

Only after root cause is confirmed:

1. Describe the fix in one sentence before coding it
2. Make the smallest possible change
3. Run the failing test again — show it passes
4. Run the full test suite — show no regression

## Constraints

- Never edit code in Phase 1 or 2.
- Never skip to "let me try X" — write the hypothesis first.
- One change at a time. No bundled fixes.
- If 3+ fixes have failed: stop. The architecture may be wrong. Ask the human.
