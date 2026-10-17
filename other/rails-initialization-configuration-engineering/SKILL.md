---
name: rails-initialization-configuration-engineering
description: Design Rails boot, initialization, configuration, environment, and lifecycle boundaries with explicit ownership, ordering, reload, security, and failure contracts.
license: MIT
---
# Rails Initialization and Configuration Engineering

## Purpose
Use this skill when Rails boot behavior, configuration, initializers, environment settings, lifecycle hooks, load paths, framework defaults, or runtime configuration changes.

## Activate when
Activate for config/application.rb, config/environments, config/initializers, config/environment.rb, config/boot.rb, config.ru, config.x, load_defaults, before_initialize, after_initialize, to_prepare, environment variables, credentials, boot-time dependency wiring, eager loading, reloading, startup validation, or initializer performance.

## Core contract
Rails boot is a lifecycle, not a single initializer file. Treat configuration declaration, environment configuration, initialization, autoloading/reloading, runtime configuration, and secrets as separate boundaries. Configuration ownership, precedence, and lifecycle timing are behavior.

## Repository inspection
Resolve Ruby/Rails versions. Inspect application/environment/boot/config.ru files, initializers, Gemfile/lockfile, load_defaults, config namespaces, Zeitwerk paths, configuration sources, consumers, external boot dependencies, and boot logging. Compare test, development, and production paths.

## Configuration ownership
Assign every setting to one explicit owner: framework config, application config, environment config, secret credential, deploy/runtime setting, or derived runtime state. Prefer the narrowest stable namespace and search consumers before changing keys.

## Configuration precedence
Map actual precedence among defaults, application config, environment config, credentials, and deployment environment variables. Preserve repository-specific precedence. Do not silently change fallback semantics or expose secrets.

## Initialization ordering
Treat initializer dependencies as a graph. Prefer lifecycle hooks over incidental filename order, make registration idempotent when reloading can occur, and never execute business workflows merely because the process boots.

## Lifecycle hooks and reloading
Choose boot-once, preparation, or runtime behavior deliberately. Do not retain reloadable classes/instances across reloads or register duplicate callbacks/subscribers. Coordinate autoloaded constants with Zeitwerk.

## External dependencies at boot
Minimize network/database/filesystem work during boot. If required, bound timeouts, distinguish required from optional dependencies, define failure behavior and readiness semantics, and avoid indefinite retries. Prefer lazy runtime access when boot-time availability is not a hard contract.

## Environment separation
Treat test, development, and production differences as explicit contracts. Review caching, eager loading, reload, logging, error reporting, jobs, database, assets, endpoints, and configuration sources independently.

## Secrets and configuration safety
Never log secret values or commit plaintext secrets. Do not expose server-only configuration to client bundles. Validate required settings without printing values and use the repository's established credential/encryption mechanism.

## Boot-time performance
Measure initializer duration, eager-load cost, dependency loading, network/database calls, allocations, and duplicate registration. Defer optional work when lifecycle semantics permit; do not disable required framework initialization to hide cost.

## Testing strategy
Use configuration tests for precedence, initializer tests for registration/lifecycle, Zeitwerk checks for autoloading, boot smoke tests for startup, integration tests for consumers, and production-like boot checks for deployment-critical settings. Avoid developer-local secret/environment dependencies.

## Anti-patterns / failure modes
Avoid business workflows in initializers, hidden ordering dependencies, unbounded boot network calls/retries, secrets in logs/client configuration, duplicate reload registration, mutable constants as configuration stores, undeclared environment dependencies, unverified framework-default changes, swallowed boot errors, and tests that pass only because a developer machine supplies configuration.

## Reference example

Custom configuration declared on the app, validated once at boot, read through one accessor.

```ruby
# config/application.rb
module Billing
  class Application < Rails::Application
    config.load_defaults 8.0

    config.x.billing = {
      provider: ENV.fetch("BILLING_PROVIDER", "sandbox"),
      timeout_seconds: ENV.fetch("BILLING_TIMEOUT", "5").to_f
    }
  end
end

# config/initializers/00_config_contract.rb - fail at boot, not at first request
Rails.application.config.after_initialize do
  provider = Rails.configuration.x.billing[:provider]
  unless %w[sandbox live].include?(provider)
    raise ArgumentError, "BILLING_PROVIDER must be sandbox or live, got #{provider.inspect}"
  end
end

# Call sites: Rails.configuration.x.billing.fetch(:timeout_seconds)
```

## Agent review checklist
- [ ] Ruby/Rails versions resolved
- [ ] boot/configuration files inspected
- [ ] ownership and precedence explicit
- [ ] lifecycle phase explicit
- [ ] reload/eager-load behavior checked
- [ ] external boot dependencies justified
- [ ] secret handling reviewed
- [ ] environment differences tested
- [ ] boot performance considered
- [ ] failure is explicit and diagnosable

## Verification
Resolve versions -> inspect configuration/lifecycle -> identify ownership/precedence -> inspect initializer dependencies -> implement smallest change -> run focused tests -> run autoload/boot verification -> run repository validation -> inspect CI evidence. Do not claim boot correctness from static inspection alone.

## Source foundation
- Rails Configuring guide: https://guides.rubyonrails.org/configuring.html
- Rails Autoloading and Reloading guide: https://guides.rubyonrails.org/autoloading_and_reloading_constants.html
- Rails Security guide: https://guides.rubyonrails.org/security.html
- Rails Getting Started guide: https://guides.rubyonrails.org/getting_started.html

## Rails initialization/configuration changes

For Rails boot and configuration changes:
- resolve Ruby/Rails versions and inspect actual boot/configuration files before implementation;
- identify configuration ownership and actual precedence across defaults, application config, environment, credentials, and deployment settings;
- treat initializer dependencies as lifecycle contracts rather than incidental filename ordering;
- choose boot, preparation, or runtime execution deliberately;
- coordinate reload-sensitive setup with Zeitwerk and make repeated registration safe;
- minimize network/database/filesystem work during boot and bound any required external dependency;
- make required boot invariants fail fast with actionable, secret-free diagnostics;
- keep credentials and server-only configuration out of logs and client-visible bundles;
- inspect development/test/production configuration independently;
- test configuration precedence, initializer registration, boot failure, reload behavior, and production-like startup where applicable;
- measure boot-time performance before optimizing;
- report observed validation evidence and do not claim boot correctness from static inspection.
