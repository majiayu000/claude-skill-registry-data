---
name: fermi-estimation
description: >
  Use for Fermi estimation, or when a rough number is needed fast: "roughly how many...", "ballpark the cost", "estimate capacity or market size", "is this even feasible?". Decomposes, uses ranges and sanity-checks. Skip when exact data is available or a precise calculation is wanted.
license: MIT
metadata:
  author: ysskrishna
  version: "2026.10.5"
---

# Fermi Estimation

Get a defensible order-of-magnitude answer from factors you can reason about. The goal is the right power of ten and a clear view of what drives it, not a precise number.

## When to use

- Capacity, load, storage, cost, headcount, market size or time estimates with little data.
- "Roughly how many", "ballpark", "back of the envelope", "is it even feasible".
- Checking whether a plan's numbers are plausible before investing in measurement.

Skip: when exact data exists (query it instead), or the user needs a precise calculation.

## Before you start

1. State in one block: **Quantity** (with units and period), **Purpose** (what decision depends on it), **Needed accuracy** (a power of ten, or within a factor of 2), and **Pass** (Decompose, Estimate, Combine, Cross-check, Sensitivity).
2. **Gather first.** Look for real anchors before guessing: logs, dashboards, billing, docs, prior numbers. Replace any guess with data you can find. Ask up to 3 questions only for anchors tools cannot supply.
3. **Light path.** Small ask: 3-4 factors, one range each, a result line and one cross-check.

## Steps

### 1. Decompose
Break the quantity into factors you can estimate, usually a product: population x frequency x size, or rate x time. Write the formula first.

### 2. Estimate
For each factor give a **low** and **high** and a one-line basis. Mark guesses `[ESTIMATED]`; mark found data with its source.

| Factor | Low | High | Basis |
|--------|-----|------|-------|

### 3. Combine
Multiply lows and highs for bounds. For a single central value, take the geometric midpoint (the square root of low x high), which suits ranges that span powers of ten. Report the result as a range and an order of magnitude.

### 4. Cross-check
Estimate the same quantity a second way (top-down vs bottom-up, or compare to a known similar system). If the two differ by more than about 3x, find which factor is off.

### 5. Sensitivity
Name the one or two factors that move the answer most, and what measurement would narrow them.

## Pitfalls

- False precision: "47,312 requests per second" from guessed inputs. Round to one significant figure.
- Unit mismatches (per day vs per second, bytes vs bits). Write units in every row.
- Double counting a factor that appears in two inputs.
- Anchoring on the first number you thought of. Estimate the low and high first, then the middle.
- Skipping the cross-check, which is what separates an estimate from a guess.
- Forgetting peaks: averages hide the busiest hour. State average and peak when sizing capacity.

Worked example: [references/example.md](references/example.md).

## Checklist

- [ ] Quantity, units, purpose and needed accuracy stated
- [ ] Formula written before numbers
- [ ] Each factor has low, high, basis; guesses marked `[ESTIMATED]`
- [ ] Result as a range and order of magnitude
- [ ] Cross-checked a second way
- [ ] Dominant factor named, with the measurement that would narrow it
