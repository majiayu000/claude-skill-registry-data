---
name: deep-interview
description: "Ambiguity gating — detects vague feature requests and forces structured requirements gathering with scoring across scope, platform, performance, integration, and acceptance criteria. Prevents wasted cycles on underspecified tasks."
alwaysApply: true
---

# Deep Interview — Ambiguity Gating

Before executing any feature request, evaluate whether the requirements are clear enough to proceed. Vague requests waste agent cycles and produce code that needs reworking.

## When to Activate

A request is **vague** when ALL of these are true:
- No file paths or directory references mentioned
- No function, class, or component names specified
- No code blocks or snippets included
- No numbered steps or explicit instructions
- The request is more than 10 words (short requests like "add a jump" are intentionally open-ended and acceptable)

If **any one** specificity signal is present, skip the interview and proceed normally.

## Exemptions — Skip the Interview

Do NOT activate for:
- **Bug fixes** — request mentions "error", "bug", "crash", "fix", "broken", "NullReference", "exception"
- **Commands with built-in clarification** — `/unity-workflow` has its own Phase 1: Clarify, `/unity-prototype` expects open-ended prompts
- **Explicit opt-out** — user includes `--skip-interview` or says "just do it" / "don't ask"
- **Follow-up requests** — user is continuing a conversation where requirements were already established
- **Simple modifications** — "make it faster", "change the color to red", "increase the speed"

## Ambiguity Score

Rate the request across 5 dimensions. Each scores 0–2:

| Score | Meaning |
|-------|---------|
| 0 | Unspecified — no information provided |
| 1 | Partial — vague or implied |
| 2 | Clear — explicitly stated or obvious from context |

### Dimensions

1. **Scope** — What exactly is being built? What are its boundaries? What is NOT included?
2. **Platform** — Target platform, Unity version, render pipeline, input method?
3. **Performance** — FPS target, memory budget, draw call limits, target device tier?
4. **Integration** — What existing systems does this touch? Dependencies? Data flow?
5. **Acceptance Criteria** — How do we know it's done? What should we test? What does success look like?

**Threshold: total score >= 6 out of 10 to proceed.**

## Interview Protocol

When the score is below threshold:

1. **Present the current scores** — show the user which dimensions are weak
2. **Ask targeted questions** — max 3 questions per round, focused on the lowest-scoring dimensions
3. **Re-score after each round** — update scores based on answers
4. **Proceed when threshold is met** — or when the user explicitly opts out

Question style: be direct and specific, not generic. Instead of "What platform?", ask "Is this for mobile (touch input, limited GPU) or desktop (keyboard/mouse, full GPU budget)?"

## Output: Requirements Document

When the threshold is met, produce a structured summary:

```
## Requirements Summary

**Feature:** [one-line description]

**Scope:** [what's included and what's explicitly excluded]
**Platform:** [target platform, input method, render pipeline]
**Performance:** [constraints, budgets, target devices]
**Integration:** [systems touched, dependencies, data flow]
**Acceptance Criteria:**
- [criterion 1]
- [criterion 2]
- [criterion 3]
```

Ask the user to confirm the summary before proceeding to implementation.

## Scoring Examples

**Vague (score 3/10):** "Add multiplayer to my game"
- Scope: 1 (multiplayer is broad — co-op? competitive? matchmaking?)
- Platform: 0 (unspecified)
- Performance: 0 (unspecified)
- Integration: 1 (implies networking but no specifics)
- Acceptance: 1 (implied: "it works")

**Clear enough (score 7/10):** "Add 2-player local co-op split-screen for the existing PlayerController using the new Input System"
- Scope: 2 (2-player local co-op split-screen)
- Platform: 1 (implies desktop from split-screen, but not explicit)
- Performance: 1 (split-screen implies rendering budget concern)
- Integration: 2 (PlayerController, Input System explicitly named)
- Acceptance: 1 (implied: both players can play simultaneously)
