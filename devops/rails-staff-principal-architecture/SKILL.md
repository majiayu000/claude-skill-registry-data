---
name: rails-staff-principal-architecture
description: Make senior staff/principal-level Rails architecture decisions about boundaries, dependencies, modularity, coupling, ownership, evolution, and system-wide tradeoffs without adding architecture for its own sake.
license: MIT
---
# Rails Staff and Principal Architecture

## Purpose
Use this skill for architecture decisions that span multiple Rails subsystems or materially change the dependency graph, ownership model, deployment shape, modularity, or long-term evolution of a Rails application.

## Activate when
Activate for modular monolith design, bounded contexts, dependency direction, subsystem extraction, architecture refactors, platform/domain boundaries, shared-kernel decisions, application decomposition, cross-team ownership, architectural migrations, repository-wide coupling, major framework adoption, or staff/principal architecture review.

Do not use this skill for ordinary feature placement when existing repository boundaries already solve the problem. Use the focused domain skill first for routing, persistence, jobs, security, APIs, assets, engines, or testing.

## Core contract
Architecture exists to preserve business and technical invariants under change. A staff/principal decision must identify the problem, constraints, ownership, alternatives, costs, migration path, and verification evidence.
Prefer the smallest boundary that makes ownership, change isolation, dependency direction, scaling, security, or reliability materially better.
Do not introduce layers, services, packages, engines, abstractions, or distributed systems merely because they are fashionable.

## Architecture decision sequence
1. State the actual problem and affected invariants.
2. Resolve runtime, Rails, persistence, deployment, and organizational constraints.
3. Map current dependencies and data ownership.
4. Identify the authoritative owner of each invariant.
5. Define desired dependency direction.
6. Compare alternatives, including no structural change.
7. Choose the smallest viable architecture.
8. Design an incremental migration path.
9. Define fitness checks and operational evidence.
10. Record tradeoffs and rejected alternatives.

## Repository inspection
Inspect application structure, domains/modules, routes, controllers, services, jobs, events, models, database ownership, external providers, engines, initializers, configuration, tests, deployment topology, CI, dependency graph, and runtime boundaries. Search actual call sites before declaring a dependency or subsystem boundary.

## Boundary design
A useful boundary owns a coherent capability or invariant and has explicit inputs, outputs, dependencies, persistence ownership, security context, and operational responsibility.
Keep boundaries cohesive and avoid splitting by file type alone. A `services/` directory is not an architecture by itself.

## Dependency direction
Dependencies should point toward stable policy or explicitly owned contracts. Avoid cycles between domains, bidirectional service dependencies, and infrastructure leakage into core policy.
An abstraction is useful when it changes dependency direction or protects a meaningful contract, not merely because two classes share methods.

## Modularity and modular monoliths
Prefer an in-process modular boundary when the problem is ownership and coupling rather than independent deployment. A modular monolith can enforce namespace, dependency, database, event, or public-API boundaries without prematurely introducing network failure modes.
When a modular boundary becomes an extraction candidate, make its contract explicit before moving process boundaries.

## Bounded contexts and shared kernel
Use bounded contexts when terminology, invariants, ownership, or change cadence differ materially. Keep shared kernels small and stable. Duplication can be safer than sharing a volatile abstraction across unrelated domains.

## Data ownership
For every important invariant, identify the authoritative writer and storage owner. Avoid two subsystems independently owning the same mutable truth.
Cross-boundary access should use explicit interfaces, projections, queries, events, or stable data contracts rather than arbitrary table coupling.

## Service and domain boundaries
Choose models, domain objects, application services, commands, policies, queries, and adapters according to responsibility. Do not create a service layer that simply forwards every Active Record method.
Push domain rules toward the owner of the invariant. Keep orchestration at application boundaries.

## Shared infrastructure
Shared infrastructure should be reusable because its contract is genuinely common and operationally important. Avoid a global `Utils`/`Common` layer that becomes an unowned dependency sink.
Make shared configuration, logging, telemetry, HTTP clients, caching, feature flags, and infrastructure contracts explicit.

## Cross-cutting concerns
Authentication, authorization, observability, reliability, idempotency, configuration, and security should have explicit ownership. Do not duplicate cross-cutting behavior in every domain boundary.
Use focused skills to implement each concern, then use this skill to verify composition and dependency direction.

## Dependency graph and cycle control
Treat the dependency graph as a first-class architecture artifact. Identify cycles, high-fan-out modules, unstable dependencies, and ownership ambiguity.
Break cycles through ownership clarification, interfaces, events, value objects, dependency inversion, or restructuring. Do not add an arbitrary abstraction solely to make a graph tool pass.

## Change coupling
Review how many files, teams, deploys, schemas, queues, or services must change together for a business change. High change coupling is evidence for architectural improvement when it is persistent and costly.
Do not optimize for theoretical decoupling when the real change frequency and operational cost do not justify it.

## Consistency boundaries
Choose consistency deliberately: transactionally local invariants should remain local where practical; asynchronous propagation should define stale/pending/reconciliation semantics.
Do not introduce distributed transactions or synchronous service calls when a local transaction or asynchronous projection can preserve the required invariant.

## Extraction and service decomposition
Extract a process/service only when there is a real boundary such as independent scaling, deployment cadence, failure isolation, ownership, regulatory isolation, or technology/runtime constraints.
Before extraction, establish a stable contract, data ownership, observability, failure model, deployment strategy, and migration plan. Distributed boundaries introduce latency, partial failure, compatibility, and operational burden.

## Architectural migration
Prefer strangler-style incremental migration: introduce target boundary, route a bounded capability through it, compare behavior, migrate data/ownership, remove old path, and enforce the new boundary.
Define rollback or recovery for every migration stage and preserve old/new compatibility during rolling deployment.

## Architecture decision records
For consequential decisions record: context, problem, constraints, options, decision, rejected alternatives, consequences, migration plan, validation, and review conditions.
Architecture documentation should explain why a boundary exists and what may depend on it; it should not become a duplicate of source code.

## Architecture fitness and enforcement
Turn important architecture rules into executable checks where possible: dependency direction, forbidden edges, namespace ownership, public API contracts, schema ownership, event contracts, test boundaries, and build/deployment constraints.
Use static checks as guards, not substitutes for architectural reasoning.

## Performance, reliability, and security tradeoffs
Architecture decisions must account for latency, throughput, connection pools, background capacity, failure domains, recovery, authorization, secrets, and data exposure.
Do not claim a boundary improves performance, resilience, or security without either measured evidence or a clearly demonstrated structural property.

## Team ownership and operational responsibility
A boundary without an owner becomes a dependency sink. Define who owns behavior, schema, operations, incidents, documentation, and compatibility.
Align technical ownership with realistic team responsibilities without making team topology the only architecture driver.

## Testing strategy
Test architecture at multiple levels: focused boundary tests, dependency/contract checks, integration tests, migration tests, failure tests, and representative end-to-end paths.
Prefer executable architecture checks for stable invariants and system tests for actual cross-boundary behavior.

## Anti-patterns / failure modes
Avoid distributed monoliths, service-for-everything designs, generic shared modules, premature microservices, dual ownership of mutable data, dependency cycles, hidden global state, architecture by folder naming alone, one giant domain layer, synchronized cross-service transactions, and documentation-only architecture rules.

## Reference example

Architecture rules that are executable: a dependency-direction check the staff review can point at, instead of a diagram nobody re-verifies.

```ruby
# One fitness function: the domain layer must not reference the HTTP layer.
# In a real repository, scan app/models (or app/domain) instead of the fixture below.
FORBIDDEN_IN_DOMAIN = %w[ActionController ActionDispatch ActionView].freeze

require "tmpdir"
Dir.mktmpdir do |domain|
  File.write(File.join(domain, "invoice.rb"), <<~RUBY)
    class Invoice
      def total_cents = 100
    end
  RUBY
  File.write(File.join(domain, "report.rb"), <<~RUBY)
    class Report
      include ActionController::Live # wrong direction: domain -> HTTP layer
    end
  RUBY

  violations = Dir[File.join(domain, "*.rb")].flat_map do |path|
    File.readlines(path).each_with_index.filter_map do |line, index|
      token = FORBIDDEN_IN_DOMAIN.find { |t| line.include?(t) }
      "#{File.basename(path)}:#{index + 1} references #{token}" if token
    end
  end

  raise "checker must find exactly one violation" unless violations.length == 1
  puts violations.first
  puts "dependency rule check: violation detected and reported (exit 1 in CI)"
end
```

## Agent review checklist
- [ ] actual problem and invariants stated
- [ ] current dependency graph inspected
- [ ] ownership boundaries explicit
- [ ] authoritative data owner identified
- [ ] dependency direction reviewed
- [ ] alternatives including no change considered
- [ ] coupling and change frequency assessed
- [ ] operational/security/reliability tradeoffs reviewed
- [ ] migration is incremental and recoverable
- [ ] architecture rules have executable checks where practical
- [ ] team/operational ownership is clear
- [ ] rejected alternatives and consequences documented

## Verification
State problem -> inspect current graph -> identify invariant/data owners -> compare alternatives -> choose smallest effective boundary -> define migration/recovery -> add architecture fitness checks -> run representative behavior tests -> review operational/security/performance effects -> inspect CI evidence.

## Source foundation
- https://guides.rubyonrails.org/application.html
- https://guides.rubyonrails.org/engines.html
- https://guides.rubyonrails.org/autoloading_and_reloading_constants.html
- https://guides.rubyonrails.org/active_job_basics.html
- https://guides.rubyonrails.org/security.html

## Rails staff/principal architecture changes

For material architecture changes:
- state the concrete problem, affected invariants, constraints, and evidence before selecting a boundary;
- inspect the current dependency graph, call graph, data ownership, deployment topology, and change coupling rather than designing from folder names;
- identify the authoritative owner of each important invariant and mutable source of truth;
- make dependency direction explicit and break cycles by clarifying ownership or stable interfaces, not arbitrary abstraction;
- consider the smallest effective in-process/module boundary before introducing Engines or independent processes;
- use bounded contexts when terminology, invariants, ownership, or change cadence materially differ;
- keep shared kernels small and stable; duplicate volatile concepts when sharing would create tighter coupling;
- do not allow multiple subsystems to independently mutate the same authoritative data without an explicit consistency/reconciliation contract;
- assess performance, reliability, security, migration, deployment, and operational ownership as first-class tradeoffs;
- require a stable contract, data owner, failure model, rollout, and recovery plan before process/service extraction;
- prefer incremental architectural migration with compatibility stages and explicit cleanup conditions;
- record consequential decisions, rejected alternatives, consequences, and review triggers;
- encode stable architecture rules as executable checks where practical;
- distinguish measured evidence from architectural hypotheses and do not claim structural improvements without verification.
