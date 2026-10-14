---
name: receiving-code-review
description: Teaches how to receive review feedback properly — verify-before-implement on every comment, different skepticism levels by source, evidence-based pushback, no performative agreement. Prevents blindly implementing review suggestions without understanding them.
---

# Receiving Code Review

## Problem it solves

Agents (and humans) often handle review feedback poorly:
- Blindly agreeing with every comment without understanding it
- Implementing suggestions without verifying they're correct
- Performative agreement — saying "good point, fixed" when the fix doesn't address the issue
- Getting defensive or dismissing valid feedback
- Wasting effort on changes the reviewer didn't actually request
- Circular review loops from misunderstanding feedback

## Protocol

### 1. Understand before acting

For each review comment:
1. **Read it completely** — don't skim
2. **Paraphrase it back** to yourself: "They want me to change X because Y"
3. **Ask if unclear** — if the comment is ambiguous, ask: "Just to confirm, you want X changed to Y, correct?"

Do NOT start implementing until you understand what's being asked and why.

### 2. Verify-before-implement

Before making any change requested in review:
- **Is the suggestion correct?** Will it actually solve the stated problem?
- **Does it follow the project's patterns?** (see follow-existing-patterns)
- **Does it maintain the spec?** (see spec-driven-development)
- **Are there side effects?** What else might break?

If the answer to any of these is "no" or "I'm not sure", do not implement — investigate first or push back.

### 3. Skepticism levels by source

Not all review feedback is equal. Apply skepticism based on source:

| Source | Skepticism | Approach |
|--------|-----------|----------|
| **Author (you)** | High | Self-review before submitting. You have the most context but also the most blind spots. |
| **Domain expert** | Low | Strong signal. Understand the rationale carefully. |
| **Peer** | Medium | Good signal. Verify against spec and patterns. |
| **Non-domain expert** | Medium-High | Check if comment is about correctness vs preference. |
| **Automated tool** | Low for rules, High for suggestions | Linters/rules are ground truth. Tool suggestions need human judgment. |

### 4. Evidence-based pushback

If you disagree with a review comment:
- Don't say "I disagree" — say "I think X is better because Y"
- Provide evidence: "The spec says Z", "This follows the existing pattern in file.rs:42"
- Offer alternatives: "Would approach A work instead of suggested B?"
- Accept if you're wrong: "You're right, I missed that edge case. Fixed."

### 5. No performative agreement

Never do these:
- Saying "fixed" when you haven't actually made the change
- Saying "good point" when you don't actually agree
- Making the change without understanding why
- Marking a comment resolved without verifying the fix works

Instead:
- "I see your point about X. I've updated the code to Y."
- "Good catch on the edge case. Added handling for it."
- "I understand the concern, but I think the current approach is correct because..."

### 6. Keep a change log

When making review-driven changes:
- Track each requested change and its resolution status
- Verify each change passes tests
- Re-read the diff before submitting the next round

## Detection triggers

Activate when:
- Review feedback is received (from any source: human, AI, tool)
- Implementing changes based on someone else's suggestion
- About to respond to a review comment
- User says "fix this" and you need to evaluate if it's correct

## When NOT to use

- You are the reviewer (use code-review instead)
- Clear bug fixes with unambiguous root cause (use debugging-and-error-recovery)
- User explicitly says "just do it, trust me"

## Cross-references

- **code-review** — Use together. code-review gives reviews; receiving-code-review teaches how to respond to them.

- **code-collaborate-qa** — For conversational back-and-forth about code. receiving-code-review is for structured response to formal review.

- **anti-sycophancy** — Performative agreement is a form of sycophancy. Verify before agreeing.

- **follow-existing-patterns** — When implementing review feedback, check that the change follows existing patterns.

- **spec-driven-development** — Review suggestions must stay within spec scope. If a suggestion expands scope, push back or re-spec.

- **verify-and-cite** — Verify review claims before implementing. Don't assume the reviewer is right.

- **anti-premature-termination** — Do not declare "all review comments addressed" until each is verified and changes are tested.
