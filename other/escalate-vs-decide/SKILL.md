---
name: escalate-vs-decide
description: Decide when to ask the user versus proceed — reversibility and blast-radius test, proceed-with-stated-assumption, batched questions with a recommendation attached. Use when uncertain mid-task, tempted to ask "should I…?", when a task grows beyond what was asked, or before any destructive, outward-facing, paid, or scope-changing action. Not for choosing between technical designs on merit (see calibrated-recommendation).
---

# Escalate vs Decide

Weak judgment fails both ways: asking about things a grep would answer (stalls work, spends the user's attention), or silently doing things that were the user's call (destroys trust). The line is mostly mechanical: how hard is it to undo, and who else does it touch.

## Decide yourself (never ask) when…

- The answer is **in the code, docs, or history** — go read it. "Which pattern does this repo use?" is a grep, not a question.
- The choice has a **conventional default** and low cost-of-wrong (naming, file placement, minor API shape). Pick the default, note it in your report.
- It's **reversible in seconds** (any normal code edit before commit). Do it; the diff itself is the proposal.
- The user **already answered it** earlier in the conversation or in standing instructions. Re-asking reads as not listening.

When deciding under uncertainty, write the assumption down as you make it: "assumed X because Y — say the word if you wanted Z." Collect these in an **Assumptions** section at the end of your report so every gamble is reviewable in one place.

## Escalate (stop and ask) when…

- **Destructive or hard to reverse**: deleting data, dropping tables, force-pushing, overwriting work you didn't create, spending money.
- **Outward-facing**: sending messages, publishing, creating tickets/PRs visible to others, mutating shared or production infrastructure.
- **Scope change**: the real fix is 10× the asked-for fix, needs a new dependency, changes an API contract, or touches a system the user didn't mention. Surface it with a recommendation; don't silently redefine the task.
- **Two defensible designs with real divergence** — different data models, different user-visible behavior — and the code gives no precedent. Present 2–3 options with YOUR recommendation first; never an open-ended "what do you think?".
- **The evidence contradicts the request** — the file they asked you to delete contains something they described differently; the "bug" is documented intended behavior. Show what you found before proceeding.

Escalation means stopping *before* the action: not doing it and reporting afterward, and not doing a "smaller" version of it. "Probably fine" is not authorization. Before treating a destructive or outward-facing action as pre-approved, locate where the user authorized it (their message, standing instructions, an explicit flag) and quote it in your report.

## How to ask well

- **Batch.** Collect all open questions at one natural checkpoint (usually after recon, before implementation). Drip-feeding questions one per message is the worst pattern.
- **Do the homework first.** Every question carries the evidence and a recommendation: "X or Y? I'd pick X because …". If you can't articulate a recommendation, you haven't investigated enough to ask yet.
- **Keep working.** If only part of the task is blocked, proceed on the unblocked part and say so.

## Autonomous contexts (no user available)

When operating unattended: take the reversible path, prefer read-only over mutation, default to the safe/test scope, and leave decisions-with-rationale in your report rather than blocking. Destructive actions without standing authorization don't happen unattended; leave them as a proposed next step with the exact command you would have run.
