---
name: frame-product
description: Turns a feature idea into a product decision - who, which metric, what cost, smallest sellable slice - at .workflow/idea-<slug>/frame.md. Use when a feature is proposed with no ticket or agreed scope.
---

# frame-product

```
wb <args>    # wb not on PATH: python <this skill's directory>/../../lib/wb.py <args>
```

The entry here is an **idea**, not a ticket. The output is a decision someone can
disagree with, or a ticket worth planning. Deciding to not build it is a
successful outcome.

## Steps

1. **Get the bar.** `repo profile`. On `solo-saas` and `startup` the product
   case is part of the work. On `scaleup` and `enterprise` a product owner makes
   this call — offer the framing, do not make the decision for them.

2. **Answer these, in writing.** An answer of "unknown" is legitimate and more
   useful than a guess dressed up as a fact:
   - **Who** has this problem, and how do you know? Named users, support
     tickets, or churn reasons — not a persona invented for the answer.
   - **What do they do today** instead? If the workaround is fine, that is the
     finding.
   - **Which metric moves**, and roughly how much. One metric. "Engagement" is
     not one.
   - **What does it cost** — build time, cost per user per month, and the
     support load it creates. A feature that generates recurring tickets costs
     more than the sprint that shipped it.
   - **Does it change pricing** or a plan limit? That is a different decision,
     and a slower one.
   - **What breaks** if it succeeds — the load, the edge cases, the operational
     burden. One operator cannot be on call for a queue.

3. **Cut it down.** State the **smallest slice that tests the belief**, not the
   complete feature. Manual before automated, one plan before all plans, one
   region before all regions. Then say what the full version would be, so the
   cut is visible rather than accidental.

4. **Check it against the code.** Does something similar already exist? An idea
   that is a config change is not a project.
   `../../shared/code-search.md`.

5. **Write `.workflow/idea-<slug>/frame.md`** with those answers, the chosen
   slice, and a recommendation: **build now**, **build later** (with what would
   change your mind), or **do not build** (with why).

6. **Then a ticket, if it survives.** Title, problem, the slice, the metric, and
   what "done" means. That ticket is what `plan-change` consumes.

## Rules

- **No metric, no build.** A feature nobody can tell succeeded or failed is a
  feature nobody can decide to remove.
- **Say when the answer is "do not build".** Recommending against something is
  the point of framing it.
- **Costs are stated, not implied.** Cost per user and support load, in numbers
  where numbers exist, marked as estimates where they do not.
- **Do not design the implementation here.** The slice is a product boundary;
  how to build it is `plan-change`'s question.
