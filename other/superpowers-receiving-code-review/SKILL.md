---
name: superpowers-receiving-code-review
description: "Use when receiving code review feedback \u2014 respond with technical rigor using a 6-step pattern: read without reacting, understand by restating, verify against actual codebase reality, evaluate technical soundness, respond with acknowledgment or reasoned pushback, and implement one item at a time with per-item testing. Purpose: Ensure every review suggestion is correct before implementing \u2014 avoid following orders from reviewers who lack full context, and avoid implementing what was requested without verifying it actually solves the problem. Key capabilities: Stop-on-unclear guardrail \u2014 if any item is unclear, stop completely until clarified; YAGNI check via grep for actual usage before adding features; per-source handling (human partner trusted after understanding, external reviewers evaluated not followed); technical pushback with evidence from working tests or code; GitHub inline comment thread replies to keep context with the code. When to trigger: after requesting-code-review and receiving feedback; when a human partner revises a PR with follow-up comments; when an external contributor or AI tool suggests changes; when reviewer opinions conflict with each other or the implementation plan; after any review round in a multi-reviewer PR; before implementing any suggestion that touches architecture, changes an API contract, or adds a new dependency. Also for: evaluating AI-generated review suggestions; handling staff engineer suggestions."
---




# Receiving Code Review

**Core principle:** "Verify before implementing. Ask before assuming. Technical correctness over social comfort."

## The 6-Step Response Pattern

1. **Read** — absorb complete feedback without reacting
2. **Understand** — restate in own words or ask for clarification
3. **Verify** — check against actual codebase reality
4. **Evaluate** — is it technically sound for *this* codebase?
5. **Respond** — technical acknowledgment or reasoned pushback
6. **Implement** — one item at a time, test each

## Handling Unclear Feedback

**Stop completely** if any item is unclear. Items may be related — partial understanding leads to wrong implementation.

If you understand items 1,2,3 but not 4,5 — state exactly that and ask for clarification before proceeding on anything.

## Source-Specific Handling

**From your human partner:** trusted after understanding; still ask if scope unclear; skip performative agreement; go straight to action.

**From external reviewers:** evaluate suggestions, don't follow orders. Before implementing:
1. Check if technically correct for *this* codebase
2. Check if it breaks existing functionality
3. Check the reason for the current implementation
4. Check if it works on all platforms/versions
5. Check if the reviewer understands the full context

If suggestion seems wrong: push back with technical reasoning.

## YAGNI Check

When a reviewer suggests adding features: grep the codebase for actual usage. If unused, propose removing it instead.

## Implementation Order for Multi-Item Feedback

1. Clarify unclear items **first**
2. Then implement: blocking issues → simple fixes → complex fixes
3. Test each fix individually
4. Verify no regressions

## When to Push Back

- Suggestion breaks existing functionality
- Reviewer lacks full context
- Violates YAGNI
- Technically incorrect for this stack
- Conflicts with architectural decisions

Use technical reasoning (not defensiveness), reference working tests/code.

## Acknowledging Correct Feedback

- ✅ "Fixed. [Brief description]"
- ✅ "Good catch — [specific issue]. Fixed in [location]."
- ❌ Any gratitude expression ("Thanks", "You're right", etc.)

Actions speak louder than words.

## Gracefully Correcting Wrong Pushback

State the correction factually and move on:
- "You were right — I checked [X] and it does [Y]. Implementing now."
- No long apology, no defending why you pushed back.

## GitHub Thread Replies

Reply in the inline comment thread, not as a top-level PR comment.

## Forbidden Responses

Avoid performative agreement:
- "You're absolutely right!"
- "Great point!" / "Excellent feedback!"
- "Let me implement that now" (before verification)
