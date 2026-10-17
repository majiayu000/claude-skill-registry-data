---
name: rails-architecture
description: Use when implementing or reviewing Rails application structure, MVC boundaries, resource flows, REST behavior, or cross-layer feature changes. Also covers maintainability review of REST design, MVC responsibilities, indexing, callbacks, and migrations.
license: MIT
---

# Rails Architecture

## Purpose

Map a Rails feature to the repository's existing request, domain, persistence, presentation, and integration boundaries.

## Activate when

- a feature crosses routes/controllers/models/views/services
- a new Rails resource is introduced
- an existing endpoint grows in scope
- application boundaries are unclear
- architecture is being refactored

## Boundary with focused Rails skills

Use this skill for cross-layer ownership and request-flow decisions. Delegate detailed route decisions to `rails-routing`, controller boundary decisions to `rails-action-controller`, persistence decisions to `rails-active-record`, and HTTP contract testing to `rails-test-engineering`. Do not duplicate detailed guidance from those skills.

## Patterns

This skill consults the following patterns from the shared `patterns/` catalog. The pattern names are load-bearing — in a single-skill install, the catalog is not present, so an agent names the pattern to load rather than linking to its path.

| Load when | Pattern | Covers |
|---|---|---|
| a change crosses routes/controllers/models/views/services and needs the cross-layer flow traced | `request-flow` | Request lifecycle; HTTP contract boundary |
| a change introduces or moves a dependency between layers | `dependency-direction-contract` | Dependency direction; inward-pointing boundaries |
| a controller and a service share authorization for one operation | `controller-service-authorization-composition` | Authorization at the execution boundary, not only the controller |
| a policy object is introduced or moved | `policy-object-boundary` | Policy object responsibility and isolation |
| a change should be audited against the Rails Way philosophy (CoC, DRY, MVC, use-Rails-first, deliberate deviation) | `the-rails-way` | 5-step decision hierarchy for AI coding assistants; where-code-belongs placement table; eight anti-patterns mapped to owning skills/patterns |

## Repository inspection



Read the smallest useful slice of the repository:

```text
routes
  -> controller
  -> authorization/authentication
  -> domain/service/query
  -> model/database
  -> serializer/view
  -> tests
```

Also inspect:

- Gemfile/lockfile
- schema/migrations
- CI
- existing conventions
- background jobs/external services when involved

## MVC responsibilities

Rails' MVC model separates request handling, presentation, and persistence/domain behavior.

A controller should coordinate the request, not become a second domain layer.

Views should present.

Persistence models should represent persistence and domain behavior that naturally belongs there.

Services/domain objects/query objects should be introduced when the workflow or query responsibility is genuinely separate from the existing object.

## Thin controller / model responsibility

The source material describes the traditional "thin controller, richer model" Rails style. Preserve the intent—controllers should not contain substantial business logic—but do not interpret "fat model" as permission to turn Active Record models into catch-alls.

Repository conventions decide whether domain behavior belongs in models, services, form objects, policies, commands, or other boundaries.

## REST/resource design

Prefer conventional resources when they accurately represent the operation.

Use custom actions when standard resource semantics do not fit, and keep them explicit.

## Cross-layer procedure

1. trace the current request flow
2. identify the required behavior contract
3. identify the owner of each responsibility
4. reuse existing boundaries
5. implement the smallest coherent change
6. update focused tests
7. verify authorization, validation, persistence, and response behavior

## Architectural anti-patterns

- fat controllers
- Active Record models used as universal service objects
- duplicated business rules across controller/model/view
- introducing a service for a trivial single-object operation
- inventing a new layer when the repository has no need for it
- mixing unrelated refactors into a feature

## Reference example

Request flow layered by responsibility: the HTTP boundary stays stateless and thin, the workflow owns the transaction, the model owns invariants.

```ruby
# app/controllers/checkouts_controller.rb - HTTP boundary only
class CheckoutsController < ApplicationController
  def create
    result = Checkout::Complete.call(user: current_user, cart: current_cart)

    if result.success?
      redirect_to result.value, notice: t(".completed")
    else
      redirect_to cart_path, alert: result.error
    end
  end
end

# app/operations/checkout/complete.rb - workflow boundary (transaction, collaborators)
# app/models/order.rb - persistence and invariants
#
# Dependencies point inward: controller -> operation -> model.
# A model that needs checkout steps is the wrong direction; re-route through the
# operation instead of reaching outward from the persistence layer.
```

## Agent review checklist

- [ ] request flow understood
- [ ] boundary ownership explicit
- [ ] existing conventions reused
- [ ] controller remains orchestration-focused
- [ ] persistence concerns are not duplicated
- [ ] cross-layer tests exist where the contract crosses layers
- [ ] architecture change is justified by actual complexity

## Verification

Trace the final feature end-to-end and run the appropriate request/model/system tests. Inspect the diff for responsibility leakage and accidental architectural expansion.

## Source foundation

Grounded in the MVC, Rails application anatomy, REST/CRUD, and Rails philosophy material in *The Ruby Workshop*, including DRY and convention-over-configuration. The boundary discipline is strengthened using *Clean Ruby*'s responsibility and refactoring guidance.

## Book integration: request lifecycle

For a cross-layer change, reason through the complete path:

route -> authentication -> authorization -> params -> application/domain operation -> persistence -> representation -> HTTP response.

REST resources should use conventional resource routes when the semantics fit. Custom actions are justified by actual domain operations, not by controller convenience.

The traditional thin-controller/richer-domain guidance is useful, but do not turn Active Record models into universal workflow containers. Existing repository boundaries still decide where behavior belongs.

## Rails code-quality review

_Merged from the retired `rails-architecture` skill._

### Repository inspection

Inspect:
- Rails/Ruby versions
- config/routes.rb
- controllers, models, views/helpers
- migrations/schema
- associations/scopes
- tests
- services/jobs where relevant
- config/rails_best_practices.yml if used
- repository conventions

Do not apply a check mechanically without understanding the application's contract.

### Review domains

### Model and persistence
Review missing database indexes, risky default_scope, misplaced finder/query logic, duplicated relationship traversal, query attributes, duplicated model logic, unnecessary model methods, and input-protection concerns appropriate to the Rails version.

### RESTful routes
Review excessive custom actions, needless deep nesting, default/catch-all routes, and unrestricted auto-generated routes. Prefer conventional resources when they accurately represent the operation.

### Controllers
Review business logic leakage, repetitive setup, render complexity, and unused actions. Do not move business logic merely to satisfy a metric.

### Views and helpers
Review business/data-access logic in templates, presentation logic that belongs in helpers/presenters, unnecessary instance-variable exposure, complex rendering, and empty/unused helpers.

### Migrations and seed data
Review indexes, seed/application data separation, migration safety, and production impact. Historical rules must be adapted to the current Rails/database environment.

### Error handling
Do not rescue Exception broadly. Catch the narrowest recoverable exception at the appropriate boundary.

### Mailers
Review multipart representation when the application's mail contract requires multiple content alternatives.

### Dead code
Treat unused methods as review signals. Search callers, reflection, routes, callbacks, jobs, and external consumers before removal.

### Pattern-selection guidance

Treat analyzer findings as signals:
detect -> inspect context -> identify risk -> choose smallest justified fix -> test -> verify

Do not turn historical rules into absolute laws. In particular, do not interpret 'move to model' as permission for fat models, 'use before filter' as permission for business workflows in callbacks, or 'use association/scope/factory' as a mandate to introduce those abstractions everywhere.

### Modern Rails compatibility

Some original checks reflect older Rails conventions such as before_filter, legacy mass-assignment APIs, and Turbo Sprockets-era asset behavior. Translate the underlying intent to the application's actual Rails version. Never introduce deprecated APIs to satisfy a historical rule.

### Reference example

The controller/contributor split the linter generation expects: assignment and response in the controller, the workflow in a callable object.

```ruby
class OrdersController < ApplicationController
  def create
    result = PlaceOrder.call(user: current_user, cart: current_cart)

    if result.success?
      redirect_to result.value, notice: t(".created")
    else
      flash.now[:alert] = result.error
      render :checkout, status: :unprocessable_entity
    end
  end
end

class PlaceOrder
  def self.call(user:, cart:) = new(user: user, cart: cart).call

  def initialize(user:, cart:)
    @user = user
    @cart = cart
  end

  def call
    order = @user.orders.create!(line_items_attributes: @cart.line_item_attributes)
    Result.success(order)
  rescue ActiveRecord::RecordInvalid => e
    Result.failure(e.record.errors.full_messages.to_sentence)
  end
end
```

### Agent review checklist

- [ ] Rails/Ruby version resolved
- [ ] relevant checks considered
- [ ] findings interpreted in repository context
- [ ] indexes/constraints considered
- [ ] REST route surface reviewed
- [ ] controller/model/view/helper ownership checked
- [ ] callbacks justified
- [ ] migrations reviewed for production safety
- [ ] exception handling is narrow
- [ ] unused-code claims verified
- [ ] historical rules translated to modern Rails
- [ ] no pattern introduced solely to satisfy a metric

### Verification

Run the repository's configured RailsBestPractices command when installed and compatible. Also run focused tests and relevant CI checks. Treat analyzer output as review input: resolve, suppress with documented justification, or intentionally accept findings according to repository policy. Never claim a clean run unless it was actually executed.
