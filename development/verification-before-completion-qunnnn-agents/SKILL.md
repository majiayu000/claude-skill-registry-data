---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs — requires running verification commands and confirming output before making any success claims; evidence before assertions always
tags: [meta, workflow, quality, verification]
applies-to: [antigravity, cursor, copilot, gemini]
level: project
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

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

## Flutter Verification Commands

| Claim | Required Command | Not Sufficient |
|-------|-----------------|----------------|
| Tests pass | `flutter test` output: 0 failures | Previous run, "should pass" |
| Analysis clean | `flutter analyze` output: 0 issues | Partial check, extrapolation |
| Build succeeds | `flutter build apk --debug` or `flutter build ios --no-codesign`: exit 0 | Analyze passing, "looks good" |
| Code generation OK | `dart run build_runner build --delete-conflicting-outputs`: exit 0 | "Models look correct" |
| No lint issues | `dart fix --dry-run`: 0 fixes needed | "I followed the style guide" |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Requirements met | Line-by-line checklist against spec | Tests passing |

## Red Flags — STOP

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
| "Analyze passed" | Analyze ≠ tests ≠ build |
| "Agent said success" | Verify independently |
| "Partial check is enough" | Partial proves nothing |
| "The code looks correct" | Looking ≠ running |
| "build_runner will handle it" | Run it and check the output |

## Key Patterns

**Tests:**
```
✅ [Run flutter test] [See: All tests passed] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**Analysis:**
```
✅ [Run flutter analyze] [See: No issues found] "Analysis clean"
❌ "I followed the conventions"
```

**Build:**
```
✅ [Run flutter build] [See: exit 0] "Build succeeds"
❌ "Analyze passed" (analyze doesn't check compilation fully)
```

**Code Generation:**
```
✅ [Run build_runner] [See: Succeeded after X.Xs] "Code generation complete"
❌ "The annotations look correct"
```

**Requirements:**
```
✅ Re-read plan → Create checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"
```

## When To Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

**Rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion/correctness

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.
