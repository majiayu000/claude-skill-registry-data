---
name: rails-serialization-globalid-engineering
description: Design and review Rails serialization, JSON representation, Active Job argument serialization, Global ID, Signed Global ID, object identity, payload versioning, and safe deserialization boundaries.
license: MIT
---
# Rails Serialization and Global IDs Engineering

## Purpose
Use this skill when a Rails codebase serializes models or domain objects, exposes JSON representations, passes objects through Active Job, introduces Global IDs or Signed Global IDs, or changes any persistent/inter-process representation contract.

## Activate when
Activate for ActiveModel::Serialization, ActiveModel::Serializers::JSON, serializable_hash, as_json, to_json, nested include/only/except/methods, API response representations, serializer objects, sensitive-field serialization, payload versioning, GlobalID, SignedGlobalID, to_global_id, to_signed_global_id, to_sgid, GlobalID::Locator, Active Job arguments, custom serializers, and deserialization failures.

## Core contract
Treat serialization as an explicit boundary with an owned schema, compatibility policy, and security model. Keep domain objects, serialized representations, JSON encoding, Global ID identity, authorization, and Active Job argument serialization separate. Global ID is an identity reference, not object state and not authorization.

## Repository inspection
Resolve Ruby, Rails, Active Model, Active Record, Active Job, and GlobalID versions. Identify whether the representation is internal, browser-facing, API-facing, queued, persisted, or cross-application. Inspect serializers, as_json/serializable_hash, presenters, response tests, nested associations, sensitive fields, job arguments, custom serializers, GlobalID locator configuration, Signed Global ID purpose/expiry, payload fixtures, and authorization after identity resolution.

## Serialization boundary
Every externally meaningful representation should have an explicit owner, schema, required/optional fields, null semantics, nested resources, sensitive-field policy, and compatibility policy. Prefer explicit allowlists over exposing an entire model attribute hash. Do not make database schema equal to API schema accidentally.

## ActiveModel serialization
ActiveModel::Serialization requires an attributes hash using string keys. serializable_hash supports only, except, methods, and include options. Use those controls deliberately and keep serialization methods side-effect free.

## JSON representation
Use as_json as a Ruby representation contract and JSON encoding at the transport edge. Use to_json when a JSON string is actually required. For versioned public APIs, prefer a dedicated serializer or response object when representation policy is meaningful.

## Nested serialization and performance
Review association cardinality, preloading, recursion, payload size, and query count before adding nested serialization. Correct output without query and payload verification is incomplete.

## Sensitive data serialization
Sensitive attributes must be excluded from externally consumed representations unless an explicit and justified contract requires them. Review credentials, authentication material, encrypted attributes, private metadata, authorization-only fields, and internal identifiers.

## Payload versioning and compatibility
A serialized payload is a compatibility surface. Classify changes as additive or breaking, identify consumers, preserve compatibility windows when needed, version explicit semantic incompatibilities, and maintain fixtures/examples for supported representations.

## Global ID identity contract
Global ID is an application-wide URI identifying a model instance. It is useful when a receiver should locate the current model later instead of receiving a mutable object snapshot. Active Job supports Global ID for Active Record arguments.

## Signed Global IDs
Use Signed Global IDs when clients or intermediate systems can tamper with an identity reference. Define verifier/key ownership, purpose, expiry, consumer, and failure behavior. Signature integrity is not authorization.

## Global ID resolution and authorization
Treat a deserialized identity as untrusted input. Restrict acceptable model classes where possible, validate application boundaries for cross-application identifiers, distinguish missing records from unavailable backends, and apply authorization after resolution.

## Active Job arguments and serializers
Use small, deterministic, queue-safe arguments. Prefer IDs or immutable primitives over large mutable graphs. Custom Active Job serializers should encode into supported primitive/container structures and respect the application's load/reload lifecycle.

## Deserialization failures
A Global ID-backed job can fail to deserialize when the record was deleted before execution. Define whether each failure is discarded, retried, reconciled, or surfaced. Do not turn every lookup failure into a retry storm.

## Testing strategy
Test exact serialized keys, sensitive-field omission, nested payload boundaries, query counts, JSON encoding, compatibility fixtures, Global ID round trips, Signed Global ID tamper/expiry/purpose behavior, locator restrictions, Active Job serialization/deserialization, custom serializers, and deleted-record behavior.

## Anti-patterns / failure modes
Avoid serializing entire models by default, exposing authentication or credential internals, coupling public payloads to database schema, hidden queries in serializers, recursive nested graphs, oversized job arguments, using Global IDs as authorization, unrestricted locators, silent semantic field changes, reload-unsafe serializers, and swallowing deserialization failures without policy.

## Reference example

A JSON contract that is sliced to an explicit field list, and job payloads that carry Global IDs resolved at execution time.

```ruby
class Statement < ApplicationRecord
  # Public serialization is an explicit contract, not attribute reflection:
  def as_json(options = {})
    super(options)
      .slice("id", "reference", "issued_on", "total_cents")
      .merge("issued_on" => issued_on&.iso8601)
  end
end

class StatementReminderJob < ApplicationJob
  def perform(statement_gid)
    statement = GlobalID::Locator.locate(statement_gid)
    StatementMailer.with(statement: statement).issued.deliver_later
  end
end

# Enqueue with the global id, not the record - deserialization failures become
# a scoped job retry instead of a marshalled-object compatibility trap:
#   StatementReminderJob.perform_later(statement.to_gid.to_s)
```

## Agent review checklist
- [ ] serialization boundary identified
- [ ] consumer and compatibility requirements identified
- [ ] allowlisted fields explicit
- [ ] sensitive fields reviewed
- [ ] nested associations reviewed
- [ ] query count and payload size tested
- [ ] Global ID vs Signed Global ID choice justified
- [ ] purpose and expiry explicit where applicable
- [ ] locator restrictions reviewed
- [ ] authorization occurs after identity resolution
- [ ] Active Job arguments are queue-safe
- [ ] deserialization failure policy explicit
- [ ] compatibility tests exist

## Verification
Resolve versions -> classify representation and identity boundary -> inspect consumers -> define explicit output contract -> inspect security and performance -> choose Global ID or Signed Global ID semantics -> define locator and authorization behavior -> verify Active Job serialization/deserialization -> run focused tests -> run repository validation -> inspect CI evidence.

## Source foundation
- https://guides.rubyonrails.org/active_model_basics.html
- https://guides.rubyonrails.org/active_job_basics.html
- https://github.com/rails/globalid
- https://guides.rubyonrails.org/security.html

## Rails serialization/Global ID changes

For serialization, JSON, Global ID, Signed Global ID, or Active Job argument changes:
- resolve Ruby/Rails/Active Model/Active Job/GlobalID versions first;
- classify the representation as internal, API-facing, browser-facing, queued, persisted, or cross-application;
- define the serialized schema and owner explicitly rather than exposing model/database shape accidentally;
- prefer explicit allowlists and exclude sensitive attributes by default;
- inspect nested association cardinality, preloading, query count, recursion, and payload size;
- distinguish as_json representation from final JSON encoding;
- treat serialized payloads as compatibility surfaces and classify additive versus breaking changes;
- use Global ID for identity references and do not treat it as authorization;
- use Signed Global ID when tamper resistance is needed; define purpose and expiry explicitly;
- restrict Global ID locator classes/applications where untrusted identifiers are resolved;
- authorize the resolved object after identity verification;
- distinguish malformed, missing, and temporarily unavailable Global ID targets;
- keep Active Job arguments small, deterministic, queue-safe, and deployment-compatible;
- custom serializers must use supported primitive/container representations and respect initialization/reload lifecycle;
- define explicit policy for ActiveJob deserialization failures;
- verify exact payloads, sensitive-field omission, query performance, identity/security semantics, and compatibility fixtures;
- do not claim serialization compatibility or identity security from one happy-path test.
