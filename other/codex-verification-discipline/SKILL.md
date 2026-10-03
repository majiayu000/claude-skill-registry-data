---
name: codex-verification-discipline
description: Use when about to claim work is complete, fixed, or passing; run verification and read the output before any success claim.
load_priority: always
---

## TL;DR
Evidence before claims. Run the command, read the output, THEN claim the result. No shortcuts. No "should work." No exceptions.

# Verification Before Completion

## Activation

1. Activate before ANY claim of completion, success, or passing status.
2. Activate on explicit `$codex-verification-discipline`, `$verify`, or `$evidence`.
3. Activate before committing, PR creation, or task sign-off.
4. Activate when about to move to the next task.
5. This skill is **always-loaded** — it runs as a constant behavioral constraint.

**Announce at start:** "I'm verifying before claiming completion."

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command **in this message**, you cannot claim it passes.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## Common Violations

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

## Red Flags — STOP

If you catch yourself thinking or writing:

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler ≠ tests |
| "Agent said success" | Verify independently |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |
| "It's trivial" | Trivial things break. Run it. |

## Evidence Patterns

**Tests:**
```
✅ [Run test command] → [See: 34/34 pass] → "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**Regression tests (TDD Red-Green):**
```
✅ Write → Run (FAIL) → Implement → Run (PASS) → "Regression test verified"
❌ "I've written a regression test" (without red-green verification)
```

**Build:**
```
✅ [Run build] → [See: exit 0] → "Build passes"
❌ "Linter passed" (linter ≠ build)
```

**Requirements:**
```
✅ Re-read plan → Create checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"
```

**Agent delegation:**
```
✅ Agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report
```

## When To Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

## Integration with Other Skills

| Skill | How Verification Integrates |
| --- | --- |
| `codex-test-driven-development` | Verify RED and GREEN steps with actual test output |
| `codex-execution-quality-gate` | Gate scripts provide the evidence; this skill ensures you actually READ the output |
| `codex-systematic-debugging` | Verify root cause fix with regression test evidence |
| `codex-subagent-execution` | Verify subagent output with VCS diff, not agent reports |
| `codex-branch-finisher` | Verify tests before presenting completion options |

## Script Invocation Discipline

1. When this workflow calls helper scripts from other skills, run `--help` first.
2. Treat helper scripts as black-box tools and execute by contract before reading source.
3. Read script source only when customization or bug-fixing is required.

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.
