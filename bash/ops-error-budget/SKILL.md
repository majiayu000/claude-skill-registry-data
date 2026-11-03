---
name: ops-error-budget
description: Calculate an error budget from an SLO target and window — the budget in time and in requests, the burn-rate threshold for each alert window, the budget consumed when each alert fires, and the time to exhaustion at a given burn rate. Use when a team needs the numbers behind an SLO or an alert threshold. Not for choosing the SLOs themselves; see /ops-slos.
metadata:
  argument-hint: "<target> <window> [burn rate]"
---

# Error budget

Work out the numbers for the SLO in "$ARGUMENTS", as `references/slos-and-alerting.md` describes.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

The SLO target (for example 99.9%) and window (for example 30 days); optionally the request volume, a current burn rate, and how much of the budget is already consumed in this window (default: none, a full budget). Ask once for any that are missing.

## Process

1. **Compute with a script,** shown in full: the budget as 1 − target; the budget in minutes over the window; the budget in failed requests when a volume is given.

2. **The alert thresholds:** for each standard window pair (14.4× over 1 hour and 5 minutes, page; 6× over 6 hours and 30 minutes, page; 1× over 3 days and 6 hours, ticket), the error-rate threshold (burn rate × (1 − target)) and the budget consumed when it fires (burn rate × long window ÷ window).

3. **Time to exhaustion** at the current burn rate when given: remaining budget × window ÷ burn rate, where the remaining budget is 1 minus the share already consumed; when no consumption was given, say the figure is "from a full budget".

4. **Thresholds that can never fire:** if burn rate × (1 − target) is 100% or more, that alert can never fire (the error rate cannot exceed 100%); say so, and use a lower burn rate or a longer window for it.

5. **Without a way to run code,** give the formulas with the user's values substituted, and label the results `not computed`.

## Output

In chat: the budget, a table of the alert thresholds and budget consumed, the time to exhaustion, and the script. This skill writes no file.
