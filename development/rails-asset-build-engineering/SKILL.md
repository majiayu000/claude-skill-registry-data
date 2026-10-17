---
name: rails-asset-build-engineering
description: Use when designing, implementing, reviewing, testing, or debugging Rails JavaScript/CSS asset loading, bundling, compilation, development processes, and production asset builds.
license: MIT
---

# Rails Asset and Build Infrastructure Engineering

## Purpose

Treat the asset/build layer as a deployment and runtime boundary, not merely frontend tooling. The authoritative design depends on the Rails version, dependency graph, asset strategy, JavaScript/CSS package manager, build commands, development process, and production artifact contract.

## Activate when

- choosing or changing Importmap, jsbundling-rails, cssbundling-rails, Propshaft, Sprockets, or another asset pipeline;
- changing JavaScript or CSS build commands;
- changing package-manager/runtime dependencies;
- modifying `bin/dev`, Procfiles, Foreman/Overmind-style process orchestration, or development watchers;
- changing asset precompile behavior;
- debugging missing assets, stale bundles, digest issues, module resolution, CSS compilation, or build-only production failures;
- changing Node/Bun/npm/pnpm/yarn versions used by Rails builds;
- changing Docker/CI build stages that produce frontend artifacts;
- reviewing development/production parity or reproducible asset builds;
- integrating third-party JavaScript/CSS dependencies;
- reviewing source maps, public artifacts, cache headers, or CDN delivery;
- testing asset/build contracts.

Do not activate for a pure browser UI change when the repository's existing build contract is untouched.

## Repository inspection

Before changing the asset/build boundary, inspect:

1. Ruby/Rails/Bundler versions and resolved gems;
2. Propshaft/Sprockets and importmap/jsbundling/cssbundling dependencies;
3. package.json and lockfile actually used by the repository;
4. package manager and runtime version declarations;
5. `bin/dev`, Procfile.dev, Docker, CI, and release scripts;
6. application JavaScript/CSS entrypoints;
7. importmap configuration and pinning;
8. bundler/compiler configuration;
9. asset precompile tasks and environment configuration;
10. public asset output and digest behavior;
11. CDN/proxy/cache configuration;
12. source-map policy and production exposure;
13. test/system-test asset loading assumptions;
14. deployment artifact boundaries.

Never infer the build strategy from the presence of a single package file. Inspect the actual executable path used by development, CI, and production.

## Strategy selection

Choose the smallest strategy consistent with the repository and product constraints.

### Importmap

Use when browser-native ES modules and server-managed pins satisfy the dependency/runtime requirements. Avoid introducing a Node build pipeline solely because JavaScript exists.

### JavaScript bundling

Use when the application requires a bundler for dependency transformation, TypeScript/transpilation, code splitting, package processing, or other capabilities that the current strategy cannot provide.

### CSS bundling

Use when CSS requires a build-time language/toolchain, imports, transformations, minification, or framework processing that the current pipeline does not provide.

### Propshaft/Sprockets

Treat the asset pipeline as an artifact-resolution and digest/cache boundary. Do not conflate static asset fingerprinting with JavaScript/CSS source transformation.

## Dependency and runtime contracts

The asset toolchain is part of the application runtime contract.

Pin or constrain:

- Node/Bun/runtime versions;
- package manager;
- lockfile;
- Rails asset-related gems;
- browser-target assumptions;
- build flags;
- environment variables affecting compilation.

Do not silently update the package manager or runtime as part of an unrelated feature.

## Development process

`bin/dev` and equivalent process orchestration must have explicit ownership.

For each process define:

- command;
- port/socket;
- restart behavior;
- environment;
- log behavior;
- dependency ordering;
- graceful shutdown;
- failure semantics.

A watcher failure must not be mistaken for a healthy Rails server.

## Build determinism

A production build should be reproducible from the declared source and dependency artifacts.

Review:

- committed lockfiles;
- deterministic package-manager install;
- Ruby/Bundler lock state;
- environment-dependent build inputs;
- timestamps/randomness;
- generated artifacts;
- network access during build;
- native dependencies;
- cache invalidation.

Do not claim reproducibility merely because one local build succeeded.

## Development/production parity

Development and production may use different optimization modes, but they must preserve the same module resolution, CSS semantics, asset names, and runtime contracts.

Explicitly identify intentional differences such as:

- watcher versus one-shot build;
- unminified versus minified output;
- source maps;
- cache headers;
- CDN delivery;
- local versus compiled dependencies.

## CI and deployment

CI should validate the actual build path used for release.

Review:

- dependency installation;
- cache keys;
- asset compilation;
- artifact persistence;
- runtime versions;
- environment variables;
- failure propagation;
- deployment ordering;
- rollback compatibility.

Do not make production deployment depend on an undocumented developer-local build artifact.

## Security

Treat package dependencies and build scripts as a supply-chain boundary.

Review:

- lockfile changes;
- install scripts;
- executable package hooks;
- private registry credentials;
- build-time secrets;
- source-map exposure;
- untrusted asset filenames/paths;
- CDN trust;
- generated HTML/JS/CSS content.

Never expose secrets through frontend environment variables merely because the bundler can read them.

## Caching and artifacts

Define cache identity for:

- dependency caches;
- compiled bundles;
- fingerprinted assets;
- CDN objects;
- browser caches.

A cache hit must not silently return artifacts built from a different dependency graph or source revision.

Prefer immutable fingerprinted artifacts for deployable static assets where the repository's delivery model supports them.

## Testing strategy

Test the asset/build boundary separately from browser behavior.

Cover:

- clean dependency installation;
- JavaScript build;
- CSS build;
- asset precompile;
- module resolution;
- digest/fingerprint output;
- missing dependency failure;
- production-like build environment;
- `bin/dev` process contract where material;
- system tests using the same asset contract as deployment.

Avoid relying solely on screenshots or manual browser verification.

## Anti-patterns / failure modes

- mixing multiple asset strategies without an explicit boundary;
- adding Node/Bun solely because a simple Importmap-compatible dependency exists;
- silently changing package manager/runtime;
- committing generated deploy artifacts without a repository policy;
- building production assets from an uncommitted local tree;
- using mutable CDN URLs as the source of truth for production dependencies;
- exposing secrets through client-side build variables;
- treating a watcher as equivalent to a successful production build;
- sharing dependency/build caches across incompatible lockfiles;
- assuming Sprockets/Propshaft performs JavaScript/CSS transformation it does not perform;
- claiming production parity from development success.

## Reference example

Importmap-based asset wiring with an explicit vendor path, leaving fingerprints and digest URLs to Propshaft.

```ruby
# config/importmap.rb
pin "application"
pin "@hotwired/turbo-rails", to: "turbo.min.js", preload: true
pin "@hotwired/stimulus", to: "stimulus.min.js"

# config/initializers/assets.rb
Rails.application.config.assets.paths << Rails.root.join("vendor/javascript")

# app/javascript/application.js - the single entry point importmap loads:
#   import "@hotwired/turbo-rails"
#   import "controllers"
#
# Propshaft fingerprints and serves; no node toolchain unless the repo says so.
# Precompile is exercised in CI (bin/rails assets:precompile) - not discovered in prod.
```

## Agent review checklist

- [ ] Rails/Ruby and asset-related dependency versions resolved
- [ ] actual package manager/runtime identified
- [ ] asset strategy identified
- [ ] JS/CSS entrypoints identified
- [ ] dev process contract inspected
- [ ] production build path inspected
- [ ] lockfile/cache behavior reviewed
- [ ] artifact/digest/cache contract explicit
- [ ] secrets excluded from client build
- [ ] CI executes the release-relevant build
- [ ] clean-build verification exists
- [ ] production-like verification exists
- [ ] scope does not include an unjustified toolchain migration

## Verification

For an asset/build change:

resolve Rails and toolchain versions
-> inspect package manager and asset strategy
-> inspect dev/CI/release commands
-> define artifact and dependency contracts
-> implement the smallest justified change
-> run clean build/precompile verification
-> run production-like verification
-> run repository validation
-> inspect CI evidence

Do not claim asset/build correctness without build evidence.

## Source foundation

- Rails Asset Pipeline guide: https://guides.rubyonrails.org/asset_pipeline.html
- Rails JavaScript in Rails guide: https://guides.rubyonrails.org/working_with_javascript_in_rails.html
- Importmap for Rails: https://github.com/rails/importmap-rails
- jsbundling-rails: https://github.com/rails/jsbundling-rails
- cssbundling-rails: https://github.com/rails/cssbundling-rails
- Propshaft: https://github.com/rails/propshaft

## Rails asset/build changes

For Rails asset/build changes:
- resolve Ruby/Rails, asset-pipeline, package-manager, and JavaScript/CSS runtime versions before changing tooling;
- inspect the actual development, CI, and production build commands rather than inferring the toolchain from package files;
- classify the boundary as asset pipeline, Importmap, JS bundling, CSS bundling, development process, dependency/runtime, artifact/cache, or release build;
- choose the smallest repository-consistent asset strategy; do not migrate toolchains merely because another tool is familiar;
- treat lockfiles, runtime versions, build scripts, and install hooks as executable dependency contracts;
- make `bin/dev`/Procfile.dev process ownership and failure propagation explicit;
- require reproducible dependency installation and production-like asset builds for release-relevant changes;
- ensure CI executes the actual release-relevant asset/precompile path;
- review dependency install scripts, private registries, build-time secrets, source maps, CDN dependencies, and generated client artifacts as supply-chain/security boundaries;
- ensure dependency/build caches are invalidated by relevant lockfile/source/runtime changes;
- distinguish development watchers from successful production builds;
- add deterministic clean-build/precompile/system verification and inspect CI evidence;
- do not claim production parity or reproducibility from a single local build.

## Book cross-reference: *Modern Front-End Development for Rails*

Chapters 1 and 5–7 compare Rails frontend setup, CSS handling, TypeScript, JavaScript/CSS bundling, Propshaft, and import maps. Treat the chapter set as a decision-space overview rather than a prescription to migrate tools. Inspect the lockfile, Rails version, deployment build path, and current asset pipeline before changing bundling or adding packages.
