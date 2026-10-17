---
name: rails-active-support
description: "Use when designing, implementing, reviewing, testing, or optimizing Rails Active Support primitives, including core extensions/loading, ActiveSupport::Concern, class_attribute, CurrentAttributes, callbacks, Notifications instrumentation, time/date semantics, inflection, and reusable Active Support utilities."
license: MIT
---

# Rails Active Support Engineering

## Purpose

Treat Active Support as a reusable framework foundation, not as a miscellaneous bag of convenience methods.

Active Support provides Rails utility classes, Ruby extensions, and cross-cutting framework primitives. The current Rails guides document both selective core-extension loading and an instrumentation API; current APIs also cover Concern composition, inheritable class attributes, and request-scoped CurrentAttributes.

This skill owns:

- core extension/loading boundaries;
- ActiveSupport::Concern composition;
- reusable class/module configuration;
- class_attribute inheritance and mutation semantics;
- CurrentAttributes and request/execution context;
- generic ActiveSupport callbacks;
- ActiveSupport::Notifications event contracts;
- time/date/time-zone utility boundaries;
- inflector/reflection use at security-sensitive boundaries;
- deterministic testing of Active Support primitives.

It composes with:

- rails-observability for operational telemetry and production diagnostics;
- ruby-concurrency for thread/fiber safety;
- rails-active-model and rails-active-record for model lifecycle behavior;
- rails-zeitwerk for autoloading and constant loading;
- rails-i18n for localized rendering and translation;
- rails-test-engineering for test boundaries;
- rails-security / rails-security-engineering for dynamic constantization, context isolation, and untrusted input.

## Activate when

- adding or changing ActiveSupport::Concern modules;
- introducing class_attribute or inheritable configuration;
- adding CurrentAttributes or request-scoped global context;
- creating custom ActiveSupport callbacks;
- instrumenting application code with ActiveSupport::Notifications;
- selecting or cherry-picking Active Support core extensions;
- changing Time.zone/date/time utility behavior;
- using Active Support inflection or constantize/safe_constantize;
- reviewing monkey patches/core extensions;
- debugging framework behavior caused by Active Support utilities.

Do not activate for a generic Ruby utility that does not use Active Support semantics.

## Repository inspection

Inspect before implementation:

1. Ruby/Rails/Active Support versions;
2. existing Active Support imports and initializers;
3. current concerns and dependency relationships;
4. class_attribute/configuration conventions;
5. Current/current-user/request-context conventions;
6. callback definitions and lifecycle owners;
7. existing ActiveSupport::Notifications events/subscribers;
8. Time.zone and date/time conventions;
9. inflections and dynamic constantization;
10. rails-observability and logging conventions;
11. test helpers and isolation/reset behavior.

Search for an existing local abstraction before creating another concern, context object, instrumentation event, or configuration macro.

## Core extensions and loading

Active Support can be loaded selectively: active_support/core_ext/some_class, a specific extension file, all core extensions, or active_support/all. Rails applications normally load Active Support unless active_support.bare is configured.

Choose the narrowest loading boundary that is practical.

Prefer:

- existing Rails-provided loading in normal Rails application code;
- targeted requires in standalone Ruby libraries;
- explicit dependency declarations for gems that use Active Support outside Rails.

Avoid:

- requiring active_support/all inside a focused reusable library without a reason;
- assuming a core extension exists merely because it exists in a Rails application;
- creating duplicate monkey patches for a method already provided by Active Support.

Treat a core extension as a compatibility dependency.

## ActiveSupport::Concern

ActiveSupport::Concern provides dependency-aware module composition plus included/prepended blocks and class_methods. Rails documents it as a way to encapsulate reusable behavior and correctly resolve module dependencies.

Use a concern when:

- behavior is cohesive;
- multiple classes share the same protocol;
- the host class remains the clear owner of the domain behavior;
- the dependency is a reusable cross-cutting trait.

Prefer an explicit object/service when:

- the behavior has substantial state;
- several unrelated dependencies are injected;
- the module would need many callbacks/macros;
- inclusion changes surprising public APIs;
- the concern becomes a hidden inheritance layer.

Keep concern dependencies explicit.

Do not build "god concerns" that contain unrelated callbacks, queries, validations, authorization, serialization, and callbacks in one module.

Prefer namespaced, narrow concerns with a clear host contract.

## class_attribute and reusable configuration

Active Support's class_attribute provides inheritable class-level values that subclasses can override without mutating the parent configuration. Current Rails also provides options for instance accessors and defaults.

Use class_attribute for configuration that is intentionally inherited/overridden.

Define:

- owner;
- default;
- inheritance semantics;
- mutation API;
- whether instances may read/write;
- mutability of the value.

Beware mutable defaults.

Prefer immutable values or copy-on-write update patterns for arrays/hashes.

Do not use class_attribute as hidden mutable global application state.

When configuration varies per request/user/tenant, use explicit context rather than class_attribute.

## CurrentAttributes and execution context

CurrentAttributes exposes thread-isolated singleton-like request attributes and resets them around requests. Rails' current API also supports reset hooks for related context such as Time.zone.

Use CurrentAttributes only for narrow request/execution context that would otherwise have to be threaded through a large number of layers.

Good candidates include:

- current authenticated account/user;
- request ID/correlation data;
- request-local tenant;
- request-local locale/context.

Keep the context small.

Do not put business state, arbitrary caches, domain aggregates, or long-lived configuration in CurrentAttributes.

Explicitly define:

- who sets each attribute;
- reset boundary;
- job handoff behavior;
- thread/fiber/concurrency behavior;
- test reset behavior;
- whether nested execution needs copied context.

Never assume CurrentAttributes automatically propagates into every background job, thread, or external process boundary.

Prefer explicit job arguments for durable work.

## ActiveSupport::Callbacks

ActiveSupport::Callbacks provides generic lifecycle callback infrastructure used by Rails components.

Use generic callbacks when:

- a class owns a clear lifecycle protocol;
- callbacks are part of a reusable framework contract;
- before/around/after semantics are genuinely useful.

Prefer explicit method orchestration when the lifecycle becomes business workflow.

Define:

- callback event names;
- ordering;
- halting/abort behavior;
- around callback nesting;
- failure semantics;
- instrumentation;
- test isolation.

Do not use callbacks to hide network calls, transactions, authorization, or unrelated business workflows.

## ActiveSupport::Notifications

ActiveSupport::Notifications provides instrumentation for Ruby/Rails code. Events have names and arbitrary payloads; subscribers can observe duration, allocations, payloads, and exceptions. Rails recommends a library-oriented event naming convention such as event.library.

For custom events define:

- stable event name;
- owner/library namespace;
- payload schema;
- units and meanings;
- low-cardinality identifiers;
- sensitive-data filtering;
- exception semantics;
- subscriber lifecycle.

Prefer:

    domain.operation
    component.action

over opaque or user-derived event names.

Use monotonic subscriptions when elapsed duration accuracy matters.

Do not use instrumentation as the business event bus.

Do not make subscribers mutate authoritative domain state.

Do not place secrets, raw request bodies, credentials, or high-cardinality user data into every payload.

Compose with rails-observability for metrics/logging/tracing export.

## Time and date semantics

Active Support extends Ruby date/time behavior and supplies time-zone aware Rails APIs.

Before using time helpers decide:

- wall-clock versus elapsed/monotonic time;
- UTC persistence versus local presentation;
- Time.zone versus system timezone;
- date versus timestamp semantics;
- daylight-saving behavior;
- beginning/end-of-period semantics.

Prefer Time.zone-aware application logic where Rails local time matters.

Persist durable timestamps in the repository's authoritative timezone convention.

Do not use local wall-clock time for duration measurement; use monotonic timing where elapsed accuracy matters, including Notifications monotonic subscriptions.

Never convert a timezone choice into authorization or tenant identity.

## Inflection and dynamic constantization

Active Support inflections provide Rails naming conventions and utilities such as singularize/pluralize and constantization helpers.

Treat dynamic constantization as a security-sensitive boundary.

Rules:

- prefer an explicit allowlisted mapping for external/user-controlled values;
- use safe_constantize only when missing constants are genuinely expected;
- do not constantize arbitrary request parameters into executable classes;
- keep autoloading/constant-loading concerns with rails-zeitwerk;
- test irregular inflections that affect routes, serializers, or persistence names.

Inflection configuration is global application behavior; change it narrowly and test the affected names.

## Reusable Active Support utilities

Use Active Support utilities when they make an existing Rails contract clearer.

Examples include:

- HashWithIndifferentAccess where mixed symbol/string-key APIs are intentional;
- with_options for grouped option construction;
- class_attribute for inherited configuration;
- concern utilities for reusable module composition;
- inflection helpers for framework naming;
- core extensions such as blank?/present?/presence where the repository already expects Rails semantics.

Do not introduce Active Support extensions merely to shorten code.

Keep utility semantics visible at important domain/security boundaries.

## Security and concurrency

Active Support primitives can hide global or shared state.

Review:

- class-level configuration mutation;
- CurrentAttributes leakage;
- thread/fiber isolation;
- callback side effects;
- notification payload exposure;
- dynamic constantization;
- global inflection changes;
- monkey patches.

When state is mutable, define the owner and lifecycle.

For any request-local state, prove reset/isolation behavior.

For concurrent code, compose with ruby-concurrency and test race-sensitive behavior explicitly.

## Testing

Test at the smallest owning boundary:

- targeted core-extension availability;
- Concern dependency and included/prepended behavior;
- class_attribute inheritance and mutation isolation;
- CurrentAttributes set/reset/isolation behavior;
- callback order/halting/around semantics;
- notification name/payload/duration/error contracts;
- time-zone and DST boundaries;
- inflection and constantization allowlists;
- test isolation across examples.

Use temporary Notifications subscriptions sparingly; the Rails API notes that temporary subscription can affect internal caches and performance, so long-lived subscribers are preferred for normal instrumentation.

Do not rely on global state left behind by another test.

## Reference example

A Concern with a class_attribute default, and a notification subscriber kept free of application work.

```ruby
module Billable
  extend ActiveSupport::Concern

  included do
    class_attribute :billing_currency, default: :usd
  end

  def billed_this_month?(at: Time.current)
    last_billed_at.present? && last_billed_at >= at.beginning_of_month
  end
end

# Subscribers must stay trivial; enqueue when real work is needed:
ActiveSupport::Notifications.subscribe("charge.completed") do |event|
  ChargeMetricJob.perform_later(event.payload[:charge_id])
end
```

## Agent review checklist

- [ ] Rails/Active Support version resolved
- [ ] loading/import boundary inspected
- [ ] Concern host contract explicit
- [ ] Concern dependencies explicit
- [ ] class_attribute inheritance/mutability reviewed
- [ ] CurrentAttributes scope/reset behavior explicit
- [ ] background-job context propagation explicit
- [ ] callbacks justified and bounded
- [ ] notification event schema explicit
- [ ] notification payload privacy reviewed
- [ ] monotonic timing considered for elapsed durations
- [ ] Time.zone/date semantics explicit
- [ ] inflection scope reviewed
- [ ] dynamic constantization allowlisted
- [ ] concurrency/isolation tested
- [ ] global state reset in tests

## Anti-patterns / failure modes

- requiring active_support/all inside a focused reusable library without need;
- god concerns;
- hidden dependencies between concerns;
- mutable class_attribute configuration shared across subclasses;
- using class_attribute for request/tenant state;
- putting business state into CurrentAttributes;
- assuming CurrentAttributes propagates into background jobs automatically;
- using callbacks as hidden application workflows;
- notification subscribers mutating authoritative state;
- high-cardinality or sensitive notification payloads;
- using wall-clock time to measure durations;
- constantizing untrusted strings;
- changing global inflections to fix one local naming bug;
- relying on global Active Support state in tests without reset.

## Verification

For an Active Support change:

    runtime/version evidence
    -> loading boundary
    -> composition/configuration primitive
    -> state/concurrency semantics
    -> lifecycle/callback semantics
    -> instrumentation contract
    -> time/inflection semantics
    -> security review
    -> focused tests
    -> regression verification

Never claim a CurrentAttributes value is request-safe, a notification is production-safe, or a concern is reusable merely because the code compiles. Verify lifecycle, isolation, payload, and consumer contracts.

## Source foundation

Primary Rails sources:

- https://guides.rubyonrails.org/active_support_core_extensions.html
- https://guides.rubyonrails.org/active_support_instrumentation.html
- https://api.rubyonrails.org/classes/ActiveSupport/Concern.html
- https://api.rubyonrails.org/classes/ActiveSupport/CurrentAttributes.html
- https://api.rubyonrails.org/classes/ActiveSupport/Notifications.html
- https://api.rubyonrails.org/classes/Class.html

These sources document Active Support loading/core extensions, Concern composition, CurrentAttributes, instrumentation/subscriptions, and class_attribute behavior.

Composed repository skills:

- `rails-observability` skill
- `rails-zeitwerk` skill
- `ruby-concurrency` skill
- `rails-active-model` skill
- `rails-active-record` skill
- `rails-i18n` skill
- `rails-security` skill
- `rails-security-engineering` skill
- `rails-test-engineering` skill
- `rails-test-engineering` skill

## Rails Active Support changes

For Active Support and cross-cutting Rails utility changes:
- inspect the Rails/Ruby/Active Support version, existing requires, concerns, class configuration, CurrentAttributes, callback definitions, Notifications events/subscribers, Time.zone conventions, inflections, dynamic constantization, observability, and tests before implementing;
- classify the boundary as loading, concern composition, inherited configuration, request/execution context, callbacks, instrumentation, time semantics, inflection, or framework testing;
- choose the narrowest Active Support API that satisfies the contract; do not use active_support/all inside focused reusable libraries without justification;
- keep ActiveSupport::Concern modules cohesive, document host contracts, and make dependencies explicit; do not create god concerns;
- treat class_attribute as inherited configuration, not mutable request/tenant state; control mutable defaults and test parent/subclass isolation;
- keep CurrentAttributes small and request/execution scoped; define setters, reset behavior, concurrency semantics, and explicit background-job propagation;
- never assume CurrentAttributes automatically propagates across background jobs, threads, or process boundaries;
- use ActiveSupport::Callbacks only for explicit lifecycle protocols; prefer explicit methods/services for significant business workflows and external side effects;
- define ActiveSupport::Notifications event names, payload schemas, cardinality, units, privacy, and subscriber ownership; notification payload is observational telemetry, not the business event bus;
- use monotonic timing when elapsed-duration accuracy matters and keep Time.zone/timezone choices separate from authorization or tenant identity;
- review Active Support inflection and constantization as compatibility/security boundaries; external type names require explicit allowlists;
- keep autoloading/constant ownership in rails-zeitwerk rather than hiding structural loading problems with dynamic constantization;
- isolate global/context state in tests and restore CurrentAttributes, timezone, inherited configuration, and subscriptions;
- never claim framework-state isolation, instrumentation correctness, or context propagation without tests proving the relevant lifecycle boundary.
