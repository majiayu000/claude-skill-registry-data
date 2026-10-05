---
name: hotfix
description: Fast iteration workflow with mandatory subagent plan review. Use when implementing small-to-medium changes quickly. Trigger on "quick fix", "small change", "just update X", or any change where full superpowers ceremony is overkill but accuracy still matters. Enforces brief-plan + subagent-review gates before any implementation.
---

# Hotfix

Fast, accurate iteration. Not cowboy coding. Not full superpowers ceremony.

**Use this when:** Small-to-medium changes where brainstorm → spec → plan → review is overkill.
**Use pocket-grinding instead when:** New system, architectural decision, unclear/contested requirements, or work spanning many files/phases. (A small, clearly-specified feature addition — e.g. a zoom button or CSV export — stays here in `hotfix`; "it's a feature" alone is not a reason to escalate.)

---

## The 5-Step Flow

**Step 1: Capture intent**
Restate the goal in 1-2 sentences. Surface ambiguity now, not after coding.
If the requirement is unclear after 1 clarifying question, escalate to superpowers/brainstorming.

**Step 2: Write brief plan**
3-5 bullets covering: what changes, where, how, and test approach.
Load `references/plan-format.md` to know what a valid plan looks like.
Takes 30 seconds. Not a spec. Not a doc. Just bullets.

**Step 3: Dispatch subagent reviewer**
Dispatch a general-purpose subagent to review the brief plan using validate-plan.
Load `references/reviewer-dispatch.md` for the exact dispatch template.
This is the anti-self-confidence gate. You do not review your own plan.

**Step 4: Fix issues from review**
- CRITICAL → fix before implementing. Non-negotiable.
- WARNING → fix unless you have explicit reason not to.
- INFO → apply if easy.
- Max 3 review iterations → if still CRITICAL after 3 passes, surface to user.

**Step 5: Implement**
Execute the reviewed plan. Nothing beyond what the plan says.

---

## Hard Gates

<HARD-GATE>
Do NOT write a single line of implementation code until:
1. The brief plan (3-5 bullets) is written in this conversation
2. The subagent reviewer has returned NO CRITICAL issues

This applies to EVERY task regardless of size, urgency, or who asked.
"Simple" changes skip the gate most often and cause the most silent bugs.
</HARD-GATE>

---

## Why the Subagent — Not You

You wrote the plan. You are confident in it. That confidence is the problem.

The subagent reviewer has no sunk cost in your approach. It reads the plan fresh
and catches: scope drift, DRY violations, YAGNI creep, missing edge cases.
These are exactly the failures that feel "obvious in hindsight" after implementing.

The review takes 60 seconds. Fixing a wrong assumption post-implementation
takes 30+ minutes and often requires touching more files.

---

## Red Flags — You Are Rationalizing

Stop when you think any of these:

| Thought | Counter |
|---------|---------|
| "This is a one-liner, no plan needed" | One-liners break things just like 100-liners. 30 seconds. Write the bullets. |
| "I already know exactly what to do" | So did every agent before it shipped a silent bug. The reviewer confirms it, not you. |
| "The user said skip the overhead" | User wants it fast AND correct. Plan + review IS fast. Cowboy coding is not. |
| "I've already started coding" | Stop. Write the plan retrospectively. Dispatch the review. Then continue. |
| "This is too trivial to review" | Trivial changes are where silent assumptions live. 60 seconds. Dispatch it. |
| "My tech lead / user said skip planning" | They meant skip the ceremony. 3 bullets is not ceremony. It's the thinking. |
| "I named the pressure tactic, so I'm immune" | Naming pressure does not cancel it. The gates still apply. |

---

## Scale to Task Size

The brief plan scales in depth. The gates do not scale — they are always on.

| Change size | Plan depth | Escalate? |
|-------------|------------|-----------|
| Typo / string fix | 2 bullets acceptable | No |
| Small UI change | 3-4 bullets | No |
| Logic / behavior change | 4-5 bullets + edge cases | No |
| New endpoint / component | 5 bullets minimum | Consider superpowers |
| Architectural / multi-system | Brief plan is insufficient | Yes → superpowers/brainstorming |

---

## Reference Files

- `references/plan-format.md` — Valid brief plan structure with examples
- `references/reviewer-dispatch.md` — Subagent dispatch template with validate-plan integration
