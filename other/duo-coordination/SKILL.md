---
name: duo-coordination
description: >
  DM coordination protocol optimized for 2-agent duo teams. The main worker
  drives the analysis while the auditor reviews, challenges, and fills gaps.
  With only one recipient per DM, sharing is cheap. Load this skill to
  understand the duo communication model.
---

# Duo Coordination Skill

You are part of a **two-agent duo** — one main worker and one auditor.
The main worker drives the primary analysis; the auditor reviews the
worker's findings, challenges assumptions, and explores angles the worker
may have missed. With only one teammate, every DM has exactly one
recipient, so **sharing is cheap**.

## Completing Your Role

The two roles finish their work with different tools:

- **Auditor**: call `complete_task` with your review summary when you have
  confirmed or corrected the main worker's findings.
- **Main worker**: do NOT call `complete_task`. After reconciliation, call
  `prepare_report` to unlock `send_user_markdown_report`, then
  `send_user_markdown_report` to deliver the final report to the user.

## Share Results When Ready

When you have results to share, DM your partner with:
1. Key findings and your interpretation
2. Any assumptions, parameters, or scope decisions you made

Share when your analysis is complete or when you need partner input.
Do NOT send gratuitous "thanks" or "looks good" messages without data.

## Trust-But-Verify (Do NOT Duplicate Partner's Work)

When you receive your partner's results, **do NOT re-run the same
analysis** or a trivial variation of it. Instead:

1. **Review the methodology**: check the logic, assumptions, parameters,
   and reasoning for correctness.
2. **Spot-check assumptions**: are the right constraints applied? Are
   edge cases handled?
3. **Only re-investigate if you find a concrete issue** — e.g., "Your
   calculation assumes X, but the problem states Y. Let me check with
   the corrected assumption."
4. **Confirm agreement explicitly**: "Your reasoning and results look
   correct — the approach and assumptions are sound. I agree."

Re-running the same work wastes time and adds no information.
Focus your effort on **complementary angles** your partner hasn't
explored yet.

## Reconcile Differences

If your results differ from your partner's:
1. DM them with **both results** and the reasoning for each
2. Identify the root cause (different assumptions, parameters, scope,
   or interpretation)
3. Agree on the correct methodology

Common discrepancy causes:
- Different assumptions or interpretation of the problem
- Different parameter choices or boundary conditions
- Missing edge cases or constraints
- Scope mismatches (partial vs complete analysis)
