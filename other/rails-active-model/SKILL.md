---
name: rails-active-model
description: "Use when designing, implementing, reviewing, testing, or integrating Rails Active Model classes that need model-like behavior without Active Record persistence, including attributes, validations, conversions, naming, dirty tracking, callbacks, serialization, translation, and form/view integration."
license: MIT
---

# Rails Active Model Engineering

## Purpose

Use Active Model when a plain Ruby object needs a deliberate subset of Rails model behavior without becoming an Active Record persistence object.

Active Model is the Rails model-like layer for non-database objects. Rails documents ActiveModel::Model as a recommended entry point and describes modules for attributes, callbacks, conversion, dirty tracking, validations, naming, serialization, translation, and linting.

This skill owns:

- deciding whether Active Model is justified;
- choosing the smallest Active Model modules;
- typed/default attributes;
- validation/error contracts;
- to_model/to_key/to_param/model_name behavior;
- dirty-state semantics;
- callback lifecycle;
- serialization;
- translation;
- Active Model lint/test contracts.

Compose with:

- rails-active-record for persistence and database lifecycle;
- rails-validations for validation/invariant decisions;
- rails-action-controller for request/input boundaries;
- rails-action-view for forms and rendering;
- rails-i18n for translation/locale context;
- ruby-domain-modeling / ruby-poro for domain ownership;
- ruby-service-objects when behavior is an application workflow;
- rails-test-engineering for deterministic tests.

Core decision:

    Rails model protocol required?
      -> no: PORO/value object/service
      -> yes, persistence required: rails-active-record
      -> yes, no persistence: rails-active-model

## Activate when

- introducing ActiveModel::Model;
- adding ActiveModel::Attributes to a plain Ruby object;
- building a model-backed form/input object;
- adding Active Model validations outside Active Record;
- implementing conversion or model naming;
- using ActiveModel::Dirty on a non-persisted object;
- defining ActiveModel::Callbacks lifecycle events;
- serializing or translating a model-like object;
- adding Active Model lint tests;
- reviewing whether a PORO should become a Rails-facing model object.

Do not activate merely because a class has attributes or validation. Active Model should earn its framework contract.

## Repository inspection

Inspect before implementation:

1. Ruby/Rails versions and available Active Model APIs;
2. whether the object is persisted, transient, or both;
3. neighboring POROs, form objects, services, and Active Record models;
4. existing Active Model usage;
5. form builders, routes, partials, and controller consumers;
6. validation/error and translation conventions;
7. callback and side-effect conventions;
8. serialization/API contracts;
9. tests and lint infrastructure.

Search for an existing repository abstraction before introducing another model-like layer.

## Boundary selection

Use a plain PORO/value object when no Rails model protocol is needed.

Use Active Model when Rails consumers need model-like initialization, errors, naming, conversion, typed attributes, or form/view compatibility.

Use Active Record when persistence, querying, associations, schema lifecycle, or database callbacks are intrinsic.

Do not use Active Model as a lightweight Active Record replacement.

## Model API contract

ActiveModel::Model supports model-style initialization and Rails model integration. Define the contract explicitly:

- accepted initialization attributes;
- readable/writable attributes;
- valid? and errors;
- persisted?;
- id/to_key when relevant;
- to_param when used in URLs;
- model_name;
- partial path when object rendering is used.

Do not accept arbitrary constructor hashes merely because Active Model can initialize from attributes.

## Attributes and type semantics

ActiveModel::Attributes provides typed attributes, defaults, casting, and serialization for plain Ruby objects.

Define:

- logical type;
- default;
- nilability;
- accepted source forms;
- casting behavior;
- serialized representation.

Test nil, blank, malformed date/number/boolean input, defaults, and repeated assignment.

Keep casting separate from semantic validation. A value can cast successfully and still be invalid domain state.

Prefer built-in types over custom types unless the contract requires custom casting.

## Validation and errors

Use validation for object-state acceptance.

Keep separate:

    casting
    -> validation
    -> domain operation

Do not use validations as:

- authorization;
- database uniqueness guarantees;
- transaction coordination;
- external API success checks;
- application workflow orchestration.

For persisted invariants compose with rails-active-record and rails-database-engineering.

Preserve error keys/messages and translation contracts.

## Conversion and naming

Active Model conversion allows model-like objects to participate in Rails forms/routes/views. Define persisted?, to_model, to_key, to_param, and model_name deliberately.

Transient objects must not accidentally appear persisted.

Never derive authorization from to_param.

Test the actual Rails consumer, not only the conversion methods in isolation.

## Dirty tracking

ActiveModel::Dirty can track changes on non-persisted objects, but the object owns the apply/reset lifecycle.

Define:

    assignment
    -> pending changes
    -> apply/commit OR rollback/reset

Do not treat Dirty as proof of persistence.

Do not trigger irreversible effects merely because a setter changed.

Test current/previous values and reset semantics.

## Callbacks

ActiveModel::Callbacks can expose explicit lifecycle events on plain Ruby objects. The object defines events and runs the callback chain explicitly.

Use callbacks only when lifecycle hooks are intrinsic to the model protocol.

Prefer an explicit service/method when:

- external effects occur;
- sequencing matters to callers;
- the operation has significant branching;
- the callback would hide application workflow.

When callbacks are justified, define events, timing, failure behavior, ordering, and tests.

## Serialization

ActiveModel::Serialization requires an explicit string-keyed attributes contract and exposes serializable_hash. Treat serialization as a representation boundary.

Define included fields, excluded/sensitive fields, computed values, nested representation, and compatibility requirements.

Do not serialize every attribute by default.

Coordinate external API representations with rails-api-integration.

## Translation

ActiveModel::Translation integrates model-like objects with I18n and humanized attribute names.

Coordinate with rails-i18n for locale context, translation keys, fallback, and errors.

Never use translated labels as machine identifiers.

## Form/input objects

Active Model is a good fit for transient form/input models because the object can own attributes, casting, validations, errors, naming, and Rails form compatibility without pretending to be an Active Record row.

Keep multi-record persistence and transaction ownership in an explicit service/domain transaction.

Do not let a form object become a universal application service.

## Active Model versus Active Record

When converting between the two, explicitly review:

- persistence ownership;
- database constraints;
- callback semantics;
- durable keys;
- dirty lifecycle;
- serialization/API compatibility;
- form routing and parameter nesting.

Similar method names do not imply identical lifecycle semantics.

## Security and privacy

Treat model-like objects as input/output boundaries.

Review:

- mass-assignment-like construction of privileged fields;
- unsafe URL parameters;
- sensitive serialization;
- error leakage;
- callbacks doing privileged side effects;
- cross-tenant object reuse.

Never treat validation success as authorization.

Never expose secrets through serialization, errors, to_param, or debugging output.

## Testing and linting

Rails provides Active Model lint tests for validating the model protocol expected by Rails consumers. Use lint tests for reusable model-like objects.

Test at the smallest boundary:

- initialization;
- casting/defaults;
- validations/errors;
- conversion/naming;
- dirty lifecycle;
- callbacks;
- serialization;
- translation;
- form/view integration;
- lint protocol.

Use request/system tests only where actual Rails integration is part of the contract.

## Reference example

A form object with Active Model behavior but no persistence: typed attributes, validations, and a single submit entry point.

```ruby
class OnboardingForm
  include ActiveModel::Model        # validations, naming, conversion
  include ActiveModel::Attributes   # typed cast attributes

  attribute :email, :string
  attribute :plan, :string, default: "trial"
  attribute :seats, :integer

  validates :email, format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :seats, numericality: { only_integer: true, greater_than: 0 }

  def submit
    return false unless valid?

    Account.create!(email: email, plan: plan, seats: seats)
  end
end

# Controller: OnboardingForm.new(onboarding_params).submit
# The form object owns input handling; Account keeps persistence rules.
```

## Agent review checklist

- [ ] Active Model justified over PORO/value object
- [ ] persistence boundary explicit
- [ ] Rails/API availability resolved
- [ ] public attributes explicit
- [ ] casting/default semantics defined
- [ ] validation boundary explicit
- [ ] database invariants remain database-owned
- [ ] conversion/naming semantics explicit
- [ ] dirty lifecycle explicit when used
- [ ] callbacks justified and bounded
- [ ] serialized fields explicit
- [ ] translation contract reviewed
- [ ] authorization outside validation
- [ ] sensitive output excluded
- [ ] lint tests considered
- [ ] deterministic tests exist

## Anti-patterns / failure modes

- using Active Model when a PORO is sufficient;
- treating Active Model as a lightweight Active Record;
- assuming validation is database integrity;
- using callbacks as hidden service orchestration;
- treating Dirty as persistence;
- serializing every attribute;
- deriving authorization from to_param;
- allowing constructor hashes to mutate privileged state;
- duplicating rules across form objects and persisted models without a clear boundary;
- coupling transient models to database concerns;
- remote calls from validators;
- skipping lint tests for Rails-facing model objects.

## Verification

For an Active Model change:

    framework/version evidence
    -> boundary decision
    -> attributes/type semantics
    -> validation/error contract
    -> conversion/naming
    -> dirty lifecycle when applicable
    -> callbacks when justified
    -> serialization/translation
    -> Rails consumer integration
    -> security review
    -> Active Model lint tests
    -> focused regression tests

Never claim Rails model compatibility because valid? works alone. Verify the protocol actually required by consumers.

## Source foundation

Primary Rails source:

- https://guides.rubyonrails.org/active_model_basics.html
- https://api.rubyonrails.org/classes/ActiveModel/Model.html
- https://api.rubyonrails.org/classes/ActiveModel/Attributes.html
- https://api.rubyonrails.org/classes/ActiveModel/Dirty.html
- https://api.rubyonrails.org/classes/ActiveModel/Callbacks.html
- https://api.rubyonrails.org/classes/ActiveModel/Serialization.html
- https://api.rubyonrails.org/classes/ActiveModel/Validations.html

Rails documents Active Model as the model-like layer for non-persisted Ruby objects and describes its attributes, callbacks, conversion, dirty tracking, serialization, translation, validations, and linting facilities.

Composed repository skills:

- `ruby-poro` skill
- `ruby-domain-modeling` skill
- `ruby-service-objects` skill
- `rails-active-record` skill
- `rails-validations` skill
- `rails-action-controller` skill
- `rails-action-view` skill
- `rails-i18n` skill
- `rails-api-integration` skill
- `rails-test-engineering` skill
- `rails-test-engineering` skill

## Rails Active Model changes

For Active Model and Rails-facing non-persisted model changes:
- treat ActiveModel::Model as an explicit Rails-facing model protocol, not a generic base class;
- inspect the Rails/Ruby version, current Active Model usage, neighboring POROs/form objects/services, Active Record boundaries, form/view consumers, routes, validations, translations, serialization, callbacks, and tests before implementing;
- decide explicitly whether the object should remain a PORO, use Active Model, or become Active Record; do not add Active Model merely because the class has attributes or validations;
- choose the smallest Active Model modules required by actual consumers;
- keep persistence, database constraints, querying, and database lifecycle in Active Record/database boundaries when persistence is intrinsic;
- define typed/default attribute behavior separately from semantic validation; casting success is not domain validity;
- keep validation separate from authorization, transaction orchestration, external API success, and database integrity;
- validation is authorization-independent and is never an authorization mechanism;
- never treat validation as authorization;
- treat to_model, to_key, to_param, and model_name as Rails-facing conversion contracts and never derive authorization from URL parameters;
- treat ActiveModel::Dirty as change tracking rather than persistence and define apply/reset/rollback semantics explicitly;
- use ActiveModel::Callbacks only for intrinsic lifecycle hooks; prefer explicit methods/services for significant workflows and external side effects;
- define serialization fields explicitly and exclude secrets/private state from serializable representations;
- compose ActiveModel::Translation with rails-i18n and preserve stable error/attribute translation contracts;
- use Active Model lint/protocol tests for reusable Rails-facing model objects and test actual form/view/route consumers at focused integration boundaries;
- never claim Rails model compatibility from valid? alone; verify the specific protocol required by the consumer.
