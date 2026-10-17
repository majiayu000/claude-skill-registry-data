---
name: rails-zeitwerk
description: Use when creating, moving, renaming, loading, reloading, eager-loading, namespacing, inflecting, or debugging Ruby/Rails constants and file paths under Zeitwerk.
license: MIT
---

# Rails Zeitwerk

## Purpose
Treat Ruby file layout, constant definitions, namespaces, autoload paths, reloading, eager loading, and initialization as one executable contract.

Rails uses Zeitwerk loaders for application autoloading, reloading, and eager loading. Within autoload paths, file names must match the constants they define and directories act as namespaces.

## Activate when
- adding, moving, or renaming classes/modules
- changing app/* or autoloaded lib/* code
- adding custom autoload paths
- adding namespaces or changing inflections
- debugging NameError/Zeitwerk::NameError
- debugging production boot/eager-load failures
- changing initializers that reference application constants
- changing reloadable/once-loaded code
- working with engines/custom root namespaces
- diagnosing circular dependencies or shadowed files
- running Zeitwerk/eager-load checks

## Repository inspection
Inspect Ruby/Rails/runtime profile, config/application.rb, config/environments/*, config/initializers/*, app/ structure, lib/ and custom autoload/eager-load paths, Rails.autoloaders configuration, inflections/acronyms, engines, explicit require/require_dependency calls, and boot/eager-load/reload tests.

Do not infer a loader failure from a filename alone; inspect root, namespace, inflector, and constant definition together.

## Fundamental mapping
Within a Zeitwerk-managed root:
```text
users_controller.rb -> UsersController
admin/payments_controller.rb -> Admin::PaymentsController
```
Rails documents this file/constant contract.

Apply the one-file/one-top-level-constant rule. Rails upgrade guidance explicitly requires separating unrelated top-level constants into their own files under Zeitwerk.

## Roots and namespaces
Each autoload root represents a top-level namespace by default. Avoid nested autoload roots unless their namespace semantics are deliberate.

Prefer existing Rails autoload paths. Rails automatically manages existing app subdirectories, while custom paths should use config.autoload_paths.

Do not use wildcard autoload roots to make arbitrary subdirectories roots.

## lib handling
Modern Rails supports config.autoload_lib(ignore:) for application code that should be autoloaded/eager-loaded while excluding non-application subdirectories such as assets, tasks, templates, and generators.

Before autoloading lib: inventory its subdirectories, identify non-Ruby/runtime files, configure ignores, and verify eager loading.

## Initializers and reloadable constants
Initializers run at boot and do not repeat on reload. Do not directly reference reloadable application constants from initializers when the configuration must track reloads.

Use config.to_prepare when reloadable code must be configured on boot and after reload. Rails documents this pattern and notes the callback should be idempotent.

Use after_initialize only for behavior intentionally limited to boot.

## Reloadable vs once-loaded
Main application code is normally managed by the main loader and can reload. Once-loaded code is managed separately and is appropriate when long-lived framework configuration stores the class/module object across reloads. Rails documents this for middleware and serializers.

Do not cache reloadable class/module objects in long-lived registries, constants, framework configuration, or singletons.

## Stale objects
Reloading replaces class/module objects. Existing instances can remain instances of the old class after reload. Rails explicitly warns against caching reloadable classes/modules.

## Inflections
Rails normally maps basenames using String#camelize. If html_parser.rb must define HTMLParser, configure an intentional inflection/acronym rather than renaming unrelated code. Rails supports global acronyms and per-loader inflector overrides.

Prefer the narrowest inflection change that fits the repository contract.

## require and require_dependency
Do not add require calls for application constants managed by Rails autoloaders. Rails documents that application classes are available without manual requires.

Investigate legacy require_dependency usage instead of copying it into new Zeitwerk code. Rails upgrade guidance notes known require_dependency use cases have been eliminated under Zeitwerk.

Ordinary require remains appropriate for code outside the managed autoload boundary or intentionally explicit load boundaries.

## Eager loading
Treat eager loading as both a production boot concern and a structural consistency check. Under Zeitwerk, autoloading and eager loading should agree on the file/constant contract.

For production-only loading failures:
```text
development autoload -> production eager load -> derive expected constant -> inspect structure/inflection -> fix -> verify
```

## Circular dependencies and shadowing
Avoid constant-level circular dependencies. Inspect duplicate filenames across roots, duplicate constant ownership, ignored paths defining managed constants, and generated/source collisions.
Zeitwerk documents circular dependencies, shadowed files, and introspection as explicit concerns.

## Engines and custom root namespaces
When an engine or custom namespace is involved, inspect its loader configuration and root ownership instead of assuming the main application's Object namespace. Zeitwerk supports custom root namespaces.

## Debugging procedure
```text
1. capture exact exception/path
2. identify loader/root
3. derive expected constant
4. inspect actual definition
5. inspect inflector/acronyms
6. inspect roots/ignored paths
7. inspect initialization timing
8. check eager loading
9. fix structural boundary
10. rerun loader verification
11. rerun affected tests
```
Do not fix a Zeitwerk::NameError with arbitrary require statements before resolving the structural mismatch.

## Rails verification
Prefer repository-supported checks such as:
```bash
bin/rails zeitwerk:check
bin/rails runner 'Rails.application.eager_load!'
```
Run only commands supported by the target application.

## Generic Zeitwerk verification
For a non-Rails loader, use the installed Zeitwerk loader's check/eager-load/introspection facilities and version-specific API.

## Anti-patterns / failure modes
- manual require hiding a path/constant mismatch
- require_dependency added without a demonstrated need
- nested roots without a namespace model
- wildcard autoload paths
- one file defining unrelated top-level constants
- incorrect acronym handling
- ambiguous explicit namespaces
- reloadable constants referenced from long-lived initializers
- cached reloadable class/module objects
- ignoring eager-load failures because development works
- mutating private ActiveSupport::Dependencies internals
- global inflections for one local naming edge case

## Reference example

Zeitwerk made checkable: the directory is the namespace, acronyms are declared once, and bin/rails zeitwerk:check runs in CI.

```ruby
# config/initializers/inflections.rb
ActiveSupport::Inflector.inflections(:en) do |inflect|
  inflect.acronym "API"
end

# Directory is the namespace - these pairings are what zeitwerk:check asserts:
#   app/services/billing/engine.rb      -> Billing::Engine
#   app/services/billing/api_client.rb  -> Billing::APIClient   (acronym-aware)
#   app/models/invoice.rb               -> Invoice
#
# Rules that keep autoload sound:
#   - one constant per file, file name matches the constant's last segment
#   - no manual require of autoloadable paths
#   - app/ defaults are eager-loaded in production; verify with zeitwerk:check
#
# CI gate: bin/rails runner "Rails.autoloaders.main.eager_load; puts 'eager ok'"
```

## Agent review checklist
- [ ] runtime/Rails version resolved
- [ ] loader/root identified
- [ ] path-to-constant mapping verified
- [ ] namespace ownership verified
- [ ] nested roots avoided or justified
- [ ] lib handling verified
- [ ] inflections/acronyms verified
- [ ] initializer timing checked
- [ ] reloadable vs once-loaded boundary checked
- [ ] stale class/module references considered
- [ ] require usage justified
- [ ] eager loading verified
- [ ] engine/custom namespace behavior checked when relevant
- [ ] focused tests run
- [ ] final diff reviewed

## Verification
Never claim Zeitwerk correctness from a unit test alone. For Rails, run the repository's Zeitwerk/eager-load verification and affected tests. For loader errors, report the failing path, expected constant, actual definition, loader configuration, and verification result.

## Source foundation
Rails Autoloading and Reloading Constants Guide: https://guides.rubyonrails.org/autoloading_and_reloading_constants.html
Zeitwerk documentation: https://github.com/fxn/zeitwerk

## Zeitwerk/autoloading changes

For Ruby/Rails constants and file-layout changes:
- resolve the loader/runtime version first;
- verify path-to-constant and namespace ownership;
- inspect inflections and autoload roots;
- distinguish reloadable and once-loaded code;
- check initializer lifecycle;
- run Zeitwerk/eager-load verification when available;
- do not hide structural loading errors with arbitrary require/require_dependency calls.
