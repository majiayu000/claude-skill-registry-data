---
name: receiving-code-review
description: Use when receiving code review feedback, before implementing any of it — especially if feedback seems unclear, technically questionable, or conflicts with a prior decision.
---

# Receiving Code Review

## Overview

Code review requires technical evaluation, not emotional performance.

**Core principle:** Verify before implementing. Ask before assuming. Technical correctness over
social comfort.

## The Response Pattern

1. **READ** the complete feedback without reacting.
2. **UNDERSTAND** — restate each requirement in your own words (or ask).
3. **VERIFY** each item against the actual codebase.
4. **EVALUATE** — is it technically sound for *this* codebase?
5. **RESPOND** with a technical acknowledgment or reasoned pushback.
6. **IMPLEMENT** one item at a time, testing each.

## No Performative Agreement

**Never:** "You're absolutely right!" · "Great point!" · "Excellent feedback!" · "Thanks for
catching that!" · any gratitude expression · "Let me implement that now" (before verifying).

**Instead:** restate the technical requirement, ask a clarifying question, push back with
reasoning if it's wrong, or just start working. **Actions speak — the fix in the code is the
acknowledgment.** If you catch yourself about to write "Thanks," delete it and state the fix.

## Handle Unclear Feedback First

If any item is unclear, STOP — don't implement anything yet. Ask about the unclear items
before starting, because items may be related and partial understanding produces the wrong
implementation. ("I understand items 1, 2, 3, 6. Need clarification on 4 and 5 before
proceeding.")

## Verify Before Implementing

Before acting on a finding, check:
1. Is it technically correct for THIS codebase?
2. Would it break existing functionality or a call site?
3. Is there a reason the current implementation is the way it is?
4. Does the reviewer have the full context?

If a suggestion seems wrong, push back with technical reasoning. If you can't verify it, say
so: "I can't verify this without [X] — should I investigate, ask, or proceed?" If it conflicts
with a decision the user already made (or with what `plan.md` mandates), stop and discuss
rather than silently overriding.

## YAGNI Check

If a reviewer suggests "implementing this properly," grep for actual usage first. Unused?
"Nothing calls this — remove it (YAGNI)?" Used? Then implement properly.

## Implementation Order

1. Clarify everything unclear first.
2. Then: blocking issues (breaks, security) → simple fixes (typos, imports) → complex fixes
   (refactoring, logic).
3. Test each fix individually (TDD where it adds behavior); verify no regressions.

## When to Push Back

When a suggestion breaks existing functionality, the reviewer lacks context, it violates YAGNI,
it's wrong for this stack, legacy/compat reasons exist, or it conflicts with a prior
architectural decision. Push back with technical reasoning and references — not defensiveness.
If you're uncomfortable pushing back, name that tension and tell the user what you've seen.

## Acknowledging Correct Feedback

State the fix, not gratitude: "Fixed — [what changed]." / "Good catch, [specific issue] — fixed
in [location]." Not "You're absolutely right!" or any thanks.

## Gracefully Correcting Your Pushback

If you pushed back and were wrong, state it factually and move on: "You were right — I checked
[X], it does [Y]. Fixing now." No long apology, no defending why you pushed back.

## The Bottom Line

External feedback = suggestions to evaluate, not orders to follow. Verify. Question. Then
implement. No performative agreement. Technical rigor always.
