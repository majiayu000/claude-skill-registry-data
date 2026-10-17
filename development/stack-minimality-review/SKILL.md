---
name: stack-minimality-review
description: Review a Ruby, Rails, React, TypeScript, and PostgreSQL diff for unnecessary complexity, indirection, dependencies, and speculative flexibility without changing the code.
license: MIT
---
# Stack Minimality Review

## Purpose
Perform a narrow simplicity review after correctness and security review. Identify what can be deleted, replaced, or shortened without weakening the actual contract.

## Activate when
Use for simplify-this-diff requests, over-engineering reviews, delete lists, minimal-diff reviews, or explicit simplicity checks.

Do not use this as the sole review for correctness, security, accessibility, performance, or migration safety.

## Repository inspection
Inspect the entire diff, touched-file context, nearby callers, repository conventions, installed dependencies, Rails extension points, React architecture, and PostgreSQL constraints.

## Decision rules
Use concrete finding tags:
- delete: dead code or unused flexibility;
- framework: custom behavior replaceable by Rails, React, browser, CSS, TypeScript, or PostgreSQL;
- dependency: a gem or package duplicates a native or existing capability;
- yagni: one-use abstraction, interface, configuration, or extension point;
- shrink: equivalent behavior with a smaller clear implementation;
- boundary: duplicated logic that belongs at an existing shared owner.

Apply the deletion test before tagging an abstraction `yagni` or `shrink`: inline it into its callers mentally. If complexity reappears across several callers, the module earns its keep; if it disappears, it is a pass-through. A port or strategy with a single implementation and no test adapter is a hypothetical seam, not a real one (see the deep-module reference in `ruby-api-design`).

This review covers simplicity only. Use `change-review` for the full standards-and-spec review of a diff.

Do not label security controls, accessibility behavior, required validation, integrity constraints, observability, or the minimum test proving non-trivial behavior as bloat.

## Implementation procedure
1. Read the complete diff.
2. Verify every deletion candidate against call sites and runtime behavior.
3. Produce one concrete line per finding: location, tag, removal, replacement.
4. Use measured diff changes for any reduction count.
5. Do not modify files.

## Anti-patterns / failure modes
- Calling an abstraction unnecessary without inspecting its consumers.
- Removing tests because they increase line count.
- Treating a framework convention as universal when the repository has an intentional deviation.
- Removing a database constraint because application validation also exists.
- Removing React state without proving the value is derived and has no independent semantics.

## Reference example

One line per finding, each verified against call sites before it is written. Reviewing the diff that introduced `OrderTotalCalculator`:

```text
app/services/order_total_calculator.rb:1 yagni — single caller (Order#total_cents), no variation; delete the class and inline `line_items.sum(&:amount_cents)` into Order#total_cents.
app/models/order.rb:5 shrink — `OrderTotalCalculator.new(self).call` becomes `line_items.sum(&:amount_cents)`.
```

Not reported: the `has_many :line_items` association, the existing model test, and any database constraint on `line_items.order_id`, because those carry required behaviour rather than bloat.

## Agent review checklist
- [ ] Diff and call sites inspected.
- [ ] Repository conventions checked.
- [ ] Every finding has a concrete replacement.
- [ ] Correctness/security/accessibility/data integrity remain out of scope for this narrow review.
- [ ] Any savings are based on actual repository changes.
- [ ] No files were modified.

## Verification
Findings are verified by traceable file locations and evidence from the repository. Run the normal correctness, security, performance, accessibility, and migration checks separately.

## Source foundation
- https://ponytail.dev/
- https://github.com/DietrichGebert/ponytail
- Repository-specific Ruby, Rails, React, TypeScript, and PostgreSQL conventions
