---
name: rails-engines-railties-engineering
description: Design and review Rails Engines and Railties as isolated extension boundaries with explicit boot, routing, configuration, loading, dependency, and host-application contracts.
license: MIT
---
# Rails Engines and Railties Engineering

## Purpose
Use this skill when a Rails codebase introduces, modifies, embeds, mounts, publishes, or integrates an Engine, Railtie, Rails plugin, mountable component, or reusable Rails extension.

## Activate when
Activate for Rails::Engine, Rails::Railtie, Rails plugins and mountable engines, isolate_namespace, engine routes and mounting, engine controllers/models/jobs/mailers/helpers/views, engine configuration, engine initializers and lifecycle hooks, engine generators and rake tasks, engine assets, engine gem dependencies, host overrides/decorations, engine testing, and compatibility changes.

## Core contract
An Engine is an extension boundary within a host Rails application. A Railtie is a narrower extension point for hooking into Rails configuration and lifecycle without necessarily owning a full application boundary. Preserve clear separation between engine ownership, host-application authority, configuration, mount/route exposure, and dependency compatibility. The Rails Engines guide documents engines as miniature applications with isolation, mounting, configuration, testing, autoloading, assets, and overrides.

## Repository inspection
Resolve Ruby, Rails, Bundler, and relevant gem versions. Identify full engine, mountable engine, Railtie-only plugin, or ordinary gem. Inspect engine.rb, railtie.rb, top-level lib file, gemspec, isolate_namespace, engine routes, host mounts, initializers, Zeitwerk paths, generators, rake tasks, assets, migrations, host overrides, dummy application, and compatibility constraints.

## Engine boundary and isolation
Use namespace isolation when engine-owned controllers, models, helpers, routes, tables, and constants must not collide with the host or other engines. Isolation does not provide authorization or tenancy semantics.

## Mounting and routing
Treat mounting as a host-application integration decision. Review mount path, route helpers, constraints, authentication and authorization, URL generation, collisions, and public exposure.

## Engine configuration
Treat engine configuration as a public contract. Define owner, namespace, default, required status, initialization timing, host override semantics, and compatibility. Prefer explicit configuration over arbitrary host globals.

## Railtie and initialization
Use a Railtie when the extension primarily needs Rails configuration, initialization hooks, generators, or framework extension points without a full application boundary. Keep setup narrow and idempotent where lifecycle requires it.

## Engine code ownership
Keep engine-owned classes in the engine namespace where isolation is intended. Prefer supported extension points, composition, callbacks, or narrow decorators over undocumented monkey patches. The host application retains final authority over environment-wide behavior.

## Dependencies and compatibility
Treat the engine gemspec as an executable compatibility contract. Inspect Ruby and Rails requirements, runtime dependencies, transitive framework assumptions, and supported version matrices. Do not depend on private host implementation details without an explicit contract.

## Autoloading and load order
Engine paths and namespaces must satisfy the actual loader contract. Review app directories, lib files, eager loading, autoload roots, reloadable versus once-loaded code, and Railtie/Engine boot timing. Do not add arbitrary require calls to hide structural Zeitwerk errors.

## Generators, tasks, and migrations
Generators, engine tasks, install hooks, and migrations are extension surfaces. Namespace tasks, make generated changes explicit, review migration ownership and reversibility, and avoid unexpected host mutation.

### Installer generators must be rerunnable
An install generator changes a host application, so prove it is safe to run twice:
1. **Generate** against a clean host (the dummy application or a fresh `rails new`).
2. **Verify** every created or modified path, and that nothing outside the declared set changed.
3. **Rerun** the generator; the second run must leave the host unchanged (an empty `git diff`, no duplicated routes, initializer lines, or migrations).
4. **Test** the rerun in a generator test (`Rails::Generators::TestCase`: `run_generator` twice, then `assert_file` contents unchanged).
5. **Document** what the generator changes in the host and how to undo it.

### Extracting host code into an engine
Extract in slices, never in one big-bang move:
- Each slice moves one coherent responsibility behind the smallest public API the host needs.
- The host's regression suite passes after every slice before the next one starts.
- A slice that needs host internals is a boundary signal: add an explicit configuration or extension point instead of reaching into the host.

## Assets and frontend integration
Engine assets belong to an explicit ownership boundary. Respect the host application's established asset/build strategy, manifest, precompile, fingerprinting, and artifact contracts.

## Testing strategy
Before implementing engine behavior, confirm that the dummy application boots and that one integration test proves the engine mounts and routes. Do not build on an engine whose dummy host cannot boot. Use isolated engine tests plus dummy-application/host integration tests. Cover namespace isolation, mount and routes, configuration, boot, autoloading, host overrides, generators/tasks/migrations, assets, and supported compatibility paths.

## Anti-patterns / failure modes
Avoid unisolated engine leakage, using a Railtie as a full application boundary without justification, arbitrary host constant access, undocumented monkey patches, implicit initializer ordering, routes mounted without explicit security review, hidden global engine configuration, migration collisions, generator side effects, asset-contract bypasses, broad require calls masking Zeitwerk errors, and claiming isolation provides authorization.

## Reference example

An engine with an isolated namespace that exposes its routes and a documented extension point to the host application.

```ruby
# billing/lib/billing/engine.rb
module Billing
  class Engine < ::Rails::Engine
    isolate_namespace Billing

    initializer "billing.append_routes" do |app|
      app.routes.append do
        mount Billing::Engine => "/billing", as: :billing
      end
    end
  end
end

# Host applications extend the engine through its documented interface:
#   Billing.configure do |config|
#     config.invoice_owner = :account
#   end
#
# Engines must not reach into host internals; all hooks flow through configure.
```

## Agent review checklist
- [ ] Engine/Railtie/plugin boundary identified
- [ ] Ruby/Rails/dependency versions resolved
- [ ] namespace/isolation contract explicit
- [ ] mount and route ownership explicit
- [ ] configuration boundary explicit
- [ ] initialization lifecycle inspected
- [ ] autoloading/load order verified
- [ ] gemspec compatibility reviewed
- [ ] host overrides are explicit and narrow
- [ ] generators/tasks/migrations reviewed
- [ ] asset/build integration reviewed
- [ ] dummy/host integration tests exist

## Verification
Resolve versions -> classify Engine vs Railtie -> inspect namespace, mount, configuration, and lifecycle -> inspect autoloading and gemspec -> implement the smallest boundary -> run engine/host integration tests -> run route/autoload/configuration checks -> run repository validation -> inspect CI evidence. Do not claim engine compatibility or isolation from static structure alone.

## Source foundation
- https://guides.rubyonrails.org/engines.html
- https://api.rubyonrails.org/classes/Rails/Engine.html
- https://api.rubyonrails.org/classes/Rails/Railtie.html
- https://guides.rubyonrails.org/autoloading_and_reloading_constants.html
- https://guides.rubyonrails.org/configuring.html

## Rails Engine/Railtie changes

For Rails Engine, Railtie, plugin, or mountable-extension changes:
- resolve Ruby/Rails/Bundler and engine gem versions before implementation;
- classify the extension as Engine, mountable Engine, Railtie-only plugin, or ordinary gem;
- inspect engine/railtie files, gemspec, namespace, mounts, routes, initializers, generators, tasks, assets, migrations, and dummy application;
- keep host application authority explicit; do not leak engine internals into host behavior without a supported contract;
- use namespace isolation and `isolate_namespace` when ownership requires it and do not confuse isolation with authorization;
- treat engine mounts/routes as explicit exposure and security boundaries;
- define engine configuration as a public namespaced contract rather than reading arbitrary host globals;
- coordinate Engine/Railtie lifecycle with initialization/configuration and Zeitwerk rules;
- review gemspec Ruby/Rails constraints and supported compatibility matrices;
- prefer supported host extension points over undocumented monkey patches;
- test engine boot, dummy-host integration, routes/mounting, autoloading, configuration, and changed generators/tasks/assets;
- do not claim Engine compatibility or isolation without executable evidence.
