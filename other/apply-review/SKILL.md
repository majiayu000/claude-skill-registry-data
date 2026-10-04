---
name: apply-review
description: Act on a code review that came back from any reviewer — another agent, the Oracle, a human PR comment. Triages each finding against the actual implementation, applies what holds up, and defends what doesn't, with rejections required to cite a concrete fact rather than a preference. Explicit invocation only.
disable-model-invocation: true
---

# Apply Review

A review has come back on code you (or another agent) wrote. Your job is **not** to implement it. Your job is to judge it, finding by finding, and then act.

The reviewer read the diff. You have the implementation context: the constraints you hit, the callers you checked, the approaches you tried and abandoned, the decisions you made deliberately. A suggestion can be perfectly reasonable from outside and still wrong from inside. That asymmetry is the entire reason this skill exists.

But the asymmetry cuts both ways, and the second edge is sharper: **"I had my reasons" is cheaper than editing.** An agent told it has superior context will rationalize away legitimate findings, confidently, at no cost. Guard against that harder than against over-compliance.

## Scope

Works with any reviewer — another agent, the Oracle, Codex, a human PR comment, a pasted list. Source doesn't matter; the method is the same.

Reviewer credibility does **not** factor into triage. A finding from a senior human and a finding from a subagent get the same test. Judge the claim, not the claimant.

What matters for triage is not whether you typed the code but whether you can reach the context behind it:

- **You wrote it, or you orchestrated it** (delegated to subagents but held the plan and made the design calls) — you own the *reasons*, which is exactly what the rejection rule tests. Judge at full weight. If a rejection turns on a detail you delegated away and don't hold, recover it: re-query the subagent that wrote it, or read the code. Don't reflexively `defer` just because your own hands didn't touch the keys — an orchestrator often holds more context than the reviewer, not less.
- **You're coming in cold** — someone else's code, no memory of why the decisions were made, no subagent to ask. Then your rejections carry little weight; say so up front and lean toward `apply` or `defer`.

Do not let "a subagent did the implementation" collapse you into the cold case. That is the most common way this skill quietly reverts to compliance.

## Method

### 1. Decompose

Split the review into discrete, individually-decidable findings. Do not work from prose. Reviews arrive as paragraphs that bundle three claims into one sentence; a bundled finding gets accepted or rejected as a unit, which is how bad suggestions ride in on good ones.

Number them. If the review is vague ("consider tightening the error handling"), turn it into the concrete change it implies, or mark it `unclear` and ask.

### 2. Verify before judging

For each finding: **go look.** Read the actual code, the callers, the tests. Do not triage from memory of what you wrote — that memory is exactly what the reviewer is challenging.

Reviewers hallucinate. A finding that references a function, prop, or file that doesn't exist, or describes behavior the code doesn't have, is `invalid` — not `reject`. Distinguish the two: `invalid` means the reviewer was factually wrong, `reject` means they were factually right and you still disagree.

### 3. Triage

Assign every finding exactly one verdict:

| Verdict | Meaning |
| --- | --- |
| `apply` | Correct and the fix fits. Do it. |
| `reframe` | The problem is real, the proposed fix isn't right. Fix the problem your way. |
| `reject` | Wrong, or right in the abstract but wrong for this code. |
| `defer` | Real, but out of scope for this change — bigger refactor, separate concern, product decision. |
| `invalid` | Reviewer is factually mistaken about the code. |
| `unclear` | Can't tell what's being asked. Ask the user. |

**The rejection rule — this is the load-bearing part:**

> A `reject` must be justified by a **concrete, checkable fact about this codebase**: a constraint, a specific caller, a test, a performance measurement, a documented decision, an approach you tried that failed, a requirement from the task.
>
> Not sufficient: "this is intentional", "I prefer it this way", "the current approach is fine", "it's more readable", "consistent with the existing style" (unless you name the existing code).
>
> **"The plan says so" is not a fact by itself.** A plan decision made during this same run counts only if you can also name what the plan derived it from — the requirement, the caller, the test, the measurement beneath it. The plan is your own artifact; citing it against a reviewer is circular. If the reviewer's suggestion is genuinely better than the plan's decision, the plan is what's wrong: verdict is `apply` or `reframe`, and update the plan text to match.
>
> **If you cannot name the fact, you don't have context the reviewer lacks — you have a preference. Apply the fix.**

`reframe` is the most common honest outcome and is underused. Reviewers are much better at spotting problems than prescribing fixes. Reaching for `reject` when the reviewer correctly identified a real problem is the most damaging failure mode of this skill — it discards a true finding on a technicality about the proposed solution.

### 4. Report the triage

Print the table **before making any edits**:

```
| # | Finding | Verdict | Reason |
```

Keep reasons to one line. Then:

- **All `apply` (and nothing else)** — proceed straight to step 5. No confirmation needed; there's nothing to disagree with.
- **Any `reject`, `defer`, `invalid`, or `unclear`** — stop. Wait for the user. Those are the calls where you're claiming knowledge the user can't verify from the table alone, and they're cheap to correct now and expensive to correct after edits.
- **Any `apply` that touches something risky** — auth, payments, migrations, data deletion, public API shape — stop regardless.

#### Orchestrated mode

When you are an orchestrator running this skill mid-workflow (e.g. Phase 5 of Orchestrate (TDD)), the user is not at the gate and idling the run to wait for them wastes the pipeline. The gate moves from *before edits* to *the final rollup*:

- Print the table, then **proceed immediately** with `apply` and `reframe` items — nothing is committed yet, so a wrong call is cheap to revert.
- **Hold** `reject`, `defer`, and `invalid` — report them in the rollup with one-line reasons so the user can overturn any of them.
- `unclear` findings go back to the **reviewer** first (steer its session with a specific question); only escalate to the user if the reviewer can't resolve it.
- The risky-`apply` stop (auth, payments, migrations, data deletion, public API shape) **still applies** — surface those to the user before touching them, orchestrated or not.

Everything else in this skill is unchanged: the rejection rule, verify-before-judging, and the close-out report all run at full strength.

### 5. Apply

Make the accepted changes. Then verify: run the tests, typecheck, build — whatever the project uses. A review-driven fix that breaks the build is worse than the original finding.

If applying a change reveals the reviewer was right about more than they knew, say so. If it reveals they were wrong, revert it and move that finding to `reject` with the new evidence — you now have the concrete fact the rejection rule wants.

### 6. Close out

Report:

- **Applied** — what changed, per finding.
- **Held** — rejected/deferred, one line each, so the user can push back.
- **Verification** — what you ran and the result.
- **New** — anything the review surfaced indirectly that nobody flagged.
- **Ledger** — a compact table of every finding with its final verdict and one-line reason. This is the artifact a repeat review consumes: if the same change goes back for another review round (e.g. via `aa-second-opinion`), pass this ledger to the reviewer with the instruction not to reopen adjudicated findings without new source evidence. Without it, each re-review relitigates settled calls and the loop never converges.

Do not commit unless asked.

## Anti-patterns

- **Blanket agreement.** A triage table of all-`apply` on a substantive review usually means you didn't judge, you complied. Check whether you actually opened the files.
- **Blanket defense.** All-`reject` means you're protecting your work. Re-read the rejection rule and test each reason against it.
- **Silent scope creep.** Applying a finding, noticing something adjacent, and fixing that too. Note it under **New**; don't fold it in.
- **Deferring to avoid work.** `defer` means genuinely out of scope, not "annoying to do".
- **Triaging from memory.** See step 2.

## When this is the wrong fit

- Getting a review in the first place → `aa-second-opinion`
- Cutting over-engineering → `aa-simplify`
- Review findings that amount to a redesign → stop and consult Oracle in `plan` mode; this skill applies changes, it doesn't re-architect
