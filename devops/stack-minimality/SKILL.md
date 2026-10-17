---
name: stack-minimality
description: Apply a Ponytail-inspired minimality discipline to Ruby, Rails, React, TypeScript, and PostgreSQL projects without sacrificing correctness, security, accessibility, data integrity, observability, or explicit requirements.
license: MIT
---
# Stack Minimality

## Purpose
Reduce unnecessary code, dependencies, indirection, and operational surface area while preserving the guarantees the product actually needs.

This is a cross-cutting modifier for a Ruby + Rails + React + TypeScript + PostgreSQL codebase. It does not replace the domain skill that owns the actual contract.

The rule is: apply YAGNI, understand the system first, then stop at the first solution that completely satisfies the contract.

## Activate when
Use for implementation, refactoring, bug fixing, architecture changes, dependency selection, performance work, database changes, frontend changes, and code review.

Do not use it to simplify away security, accessibility, validation at trust boundaries, transactional integrity, data-loss protection, required observability, or tests needed to prove changed behavior.

## Repository inspection
Before editing:
- inspect the real execution path and affected call sites;
- inspect existing Rails models, controllers, services, policies, queries, serializers, and conventions;
- inspect React feature boundaries, hooks, state ownership, API clients, and installed packages;
- inspect PostgreSQL schema, constraints, indexes, query patterns, and migration conventions;
- inspect Gemfile/Gemfile.lock, package manifests and lockfiles, runtime versions, CI, and test commands.

For bugs, trace all relevant callers before patching the reported symptom.

## Decision rules
Use the first rung that genuinely satisfies the contract:

1. No change — remove speculative work or unnecessary configuration.
2. Existing code — reuse an existing helper, component, query, service, hook, type, or boundary.
3. Framework or platform primitive — prefer Rails conventions, Active Record, browser APIs, React primitives, CSS, and PostgreSQL features over custom infrastructure.
4. Language or runtime primitive — prefer Ruby and TypeScript capabilities before another abstraction.
5. Existing dependency — use an installed gem or package when it already solves the problem adequately.
6. Direct implementation — write the smallest clear method, component, query, migration, or workflow.
7. New abstraction or dependency — introduce it only when a concrete responsibility boundary, second real implementation, repeated variation, scaling requirement, or operational constraint earns it.

### Ruby
Prefer direct Ruby, Enumerable, keyword arguments, small objects, and explicit composition. Avoid service, strategy, factory, repository, or generic utility objects for one trivial behavior.

### Rails
Prefer conventional routing, controllers, Active Record, existing application boundaries, and narrowly owned lifecycle hooks. Do not wrap Active Record merely to hide Active Record. A service object should own a real workflow, not forward one model call.

### PostgreSQL
Use database constraints for durable invariants when PostgreSQL is the authoritative writer. Add indexes from actual query shape and workload evidence. Prefer fixing query/data-model problems before introducing cache state. Treat migrations as rolling-deployment contracts.

### React and TypeScript
Keep state at the smallest legitimate owner. Derive values instead of storing duplicate state. Prefer React, browser, CSS, and TypeScript primitives before new packages or wrappers. Validate untrusted runtime data at API and browser boundaries.

### Cross-stack
Reuse existing request clients, API contracts, serializers, error contracts, and test helpers before adding adapters or duplicate infrastructure. Prefer an in-process modular boundary before a network service unless independent deployment, scaling, ownership, regulatory isolation, or failure isolation is a real requirement.

## Implementation procedure
1. State the behavior or invariant that must remain true.
2. Trace the end-to-end path and inspect existing implementations.
3. Identify the lowest adequate ladder rung.
4. Implement the smallest coherent change.
5. Preserve security, accessibility, validation, data integrity, observability, and explicit requirements.
6. Add the smallest test that proves changed behavior.
7. Review the diff for unnecessary files, dependencies, indirection, and speculative flexibility.
8. Run the repository's focused checks and relevant full suite.
9. Report only observed evidence.

When deliberately choosing a simple solution with a known ceiling, record:
- Ruby/Rails: # stack-minimality: ceiling; revisit when trigger
- TypeScript/React/CSS: // stack-minimality: ceiling; revisit when trigger
- SQL/migrations: -- stack-minimality: ceiling; revisit when trigger

## Anti-patterns / failure modes
- Removing security checks, authorization, validation, accessibility, error handling, observability, or database constraints just to reduce lines.
- Adding a wrapper around a wrapper because a pattern catalogue contains it.
- Creating a service, repository, factory, strategy, or interface for one caller and one implementation without a real boundary.
- Moving local React state into global context or a state library for convenience.
- Storing a value that can be derived from current state or props.
- Replacing a PostgreSQL invariant with an application convention.
- Adding a cache before understanding the underlying query or workload.
- Adding a dependency for functionality already provided by the stack.
- Fixing one caller when multiple callers share the same broken owner.
- Treating a smaller textual diff as automatically safer.

## Reference example

A single-use calculator object forwarding one expression is removed in favour of the model method it served (ladder rung 2: existing code). The deliberate ceiling is recorded where the shortcut lives.

```ruby
# Before: an abstraction with one caller and no variation.
class OrderTotalCalculator
  def initialize(order)
    @order = order
  end

  def call
    @order.line_items.sum(&:amount_cents)
  end
end

class Order < ApplicationRecord
  has_many :line_items

  def total_cents
    OrderTotalCalculator.new(self).call
  end
end

# After: the behaviour stays on the record that owns it.
class Order < ApplicationRecord
  has_many :line_items

  # stack-minimality: summed in Ruby over loaded line items; revisit when orders exceed ~500 line items or the total is needed in SQL reports
  def total_cents
    line_items.sum(&:amount_cents)
  end
end
```

The model test that already covered `total_cents` still proves the behaviour; no new abstraction or test double is needed.

## Agent review checklist
- [ ] Full execution path inspected.
- [ ] Existing helpers, components, services, queries, and dependencies searched.
- [ ] Lowest adequate ladder rung identified.
- [ ] Rails, React, browser, TypeScript, and PostgreSQL primitives considered.
- [ ] New dependency explicitly justified.
- [ ] New abstraction has a real responsibility or variation boundary.
- [ ] Database invariants remain enforced by the authoritative store.
- [ ] Runtime data is validated at trust boundaries.
- [ ] Security and accessibility guarantees remain intact.
- [ ] Changed behavior has focused verification.
- [ ] Deliberate simplifications have a ceiling and revisit trigger.
- [ ] No speculative work remains in the final diff.

## Verification
Verify the owning contract with focused tests, then run the repository's relevant full suite and static checks. Require real query-plan evidence for database performance claims. Require browser/runtime verification for material frontend behavior when the repository supports it. Never present hypothetical savings as measured results.

## Source foundation
- https://ponytail.dev/
- https://github.com/DietrichGebert/ponytail
- https://guides.rubyonrails.org/
- https://www.postgresql.org/docs/
- https://react.dev/
- https://www.typescriptlang.org/docs/
