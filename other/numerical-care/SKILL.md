---
name: numerical-care
description: Handle numbers like they bite — float equality, currency arithmetic, rounding, allocations that must sum exactly, division by zero, overflow, unit mismatches. Use when writing or reviewing any arithmetic beyond a counter — money, tax, discounts, splits, percentages, averages, rates, coordinates, durations, unit conversion, aggregations, or comparisons of computed values.
---

# numerical-care

Numeric bugs pass every casual test and then misprice an order. Weak numerical work writes the formula and tests it with 10 and 20. Strong numerical work names the hazard on every arithmetic line and tests with the value that would expose it.

## Standing hazards

1. **Never compare floats with `==`.** `0.1 + 0.2 != 0.3`. Compare within an epsilon scaled to the magnitude, or restructure to avoid the comparison. Tests assert almost-equal, not equal.
2. **Money is integer minor units or Decimal — never binary floats.** Match what the codebase already uses (find its existing money type before adding one); if it uses floats for money, flag that in the report rather than extending it.
3. **Rounding is a policy, not a default.** Half-up, banker's, floor for "never overcharge" — pick deliberately, name it in a comment, and round once at the boundary (display or storage), not mid-calculation where errors compound.
4. **Allocations must sum exactly.** Splitting a total across N parts, tax across line items, percentages that should total 100: compute the parts, then assign the remainder deliberately to a named part. Assert `sum(parts) == total` in a test.
5. **Every `/` needs a zero plan.** Average of an empty list, percentage of a zero total, rate over a zero-length window: state what the result is (0, null, error) and handle it. Check integer vs true division where the language distinguishes them.
6. **Representation limits:** silent 32-bit wrap, IDs and timestamps beyond 2^53 in a double (keep big IDs as strings), precision loss on casts between types.
7. **Units travel with the value.** ms vs s, cents vs dollars, bytes vs MB, degrees vs radians, percent vs fraction (`0.15` or `15`?), percentage points vs percent change. Name variables with their unit (`timeout_ms`, `rate_pct`) wherever ambiguity is possible; convert at the boundary, never mid-formula.
8. **Aggregations over floats depend on order and method.** Summing many floats naively drifts; use the platform's compensated sum when it matters, and don't compare results produced by different aggregation orders.
9. **Time arithmetic is not integer arithmetic.** A day is not 86400 s across DST; months vary; use the platform's date library for calendar math and monotonic durations for elapsed time.

## Procedure

- Grep the diff for `/`, `*`, `-`, `+`, `==`, `<=`, `>=`, `round`, `floor`, `ceil`, `parseFloat`, `toFixed` and check each hit against the list above.
- For each arithmetic line ask: what value makes this wrong — zero, negative, huge, 0.1, or parts that sum to 100.01? Run that value, in a test or a one-off call, and compare against an expected value computed independently (by hand or by a different method), not against the code's own output.
- Report the rounding policy and units chosen, and any float-money or unit ambiguity found in existing code that you did not fix.
