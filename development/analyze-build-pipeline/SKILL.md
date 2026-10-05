---
name: analyze-build-pipeline
description: Use when understanding how source transforms to runtime, what gets filtered/compiled/generated, or tracing build-time shaping that affects what code actually runs
---

## Announce at start: "Using codebase-analyzer to analyze the build pipeline."

## Overview

Trace the source -> runtime transformation pipeline. Find filtering, compilation, code generation, and build-time shaping.

**Prerequisite:** Reads `docs/analysis/provenance.md` (from trace-codebase-provenance).

## Process

1. Identify build config files (webpack.config, vite.config, tsconfig, Cargo.toml, Makefile)
2. Map build stages: lint -> compile -> bundle -> optimize -> package -> deploy
3. Find code filtering: what gets included/excluded by build conditions
4. Identify code generation: Protobuf, GraphQL, OpenAPI generators
5. Find build-time constants injected into code
6. Trace environment variable usage in build
7. Produce build pipeline map with filtering report

## Quick Reference

| Build Tool | Config Location | Key Features |
|-----------|----------------|--------------|
| webpack | webpack.config.* | Loaders, plugins, code splitting |
| Vite | vite.config.* | Plugins, define, env replacement |
| esbuild | build script | Bundle, define, external |
| Cargo | Cargo.toml | Features, profiles, build scripts |
| Make | Makefile | Targets, variables, recipes |
| Bazel | BUILD, WORKSPACE | Rules, targets, toolchains |

## Trigger Signals

- **HIGH confidence**: Build conditions that filter tools/capabilities -> `extract-tool-graph`
- **HIGH confidence**: Environment-specific code paths -> affects all downstream analysis
- **MEDIUM confidence**: Code generation step -> provenance verified
- **LOW confidence**: Standard build, no filtering -> no additional deep dive

## Transformation Chain Reasoning

Map the full chain: source -> preprocessor -> compiler -> bundler -> optimizer -> minifier -> output. At each stage: what's added? what's removed? what's transformed? The chain reveals what the final artifact went through.

Every transformation stage is a decision point where code is shaped. A TypeScript file does not become runtime JavaScript unchanged -- it passes through `tsc` (type stripping), possibly `babel` (target downleveling), `webpack`/`vite` (bundling + tree-shaking), a minifier (whitespace + identifier mangling), and potentially a compressor (gzip/brotli). Each stage introduces gaps between what you read in source and what actually executes.

**Key questions at each stage:**

1. **Preprocessor**: What macros expand? What conditionals resolve? (C preprocessor, Sass, PostCSS)
2. **Compiler**: What source constructs survive compilation? What is lowered or polyfilled? (tsc, Babel, javac, go build)
3. **Bundler**: Which modules are tree-shaken away? What gets code-split into separate chunks? (webpack, Rollup, esbuild)
4. **Optimizer**: What inlining occurs? What dead code is eliminated? (Terser, SWC minify, Cargo profile)
5. **Minifier**: What identifiers are renamed? What structural info is lost? (Terser, UglifyJS, strip debug symbols)
6. **Output**: What is the final artifact format and how does it differ structurally from any single source file?

If you skip a stage in your analysis, you have a blind spot about what code actually runs at runtime.

## Configuration Axis Discovery

Every build has axes: ENVIRONMENT, USER_TYPE, PROVIDER, FEATURE_FLAGS. Document each axis and its values. This is the Build Dimension Catalogue that downstream skills depend on.

An axis is any dimension along which the build produces different outputs from the same source. Most codebases have 3-7 axes that multiply into hundreds of potential build variants -- but only a few are actually exercised in practice.

**How to find axes:**

- Scan `DefinePlugin`, `define` in vite/esbuild, `--define` flags for injected constants
- Look at feature flag systems (LaunchDarkly, GrowthBook, Unleash, custom `process.env.FEATURE_*`)
- Check environment-specific entry points (`main.dev.ts` vs `main.prod.ts`)
- Find conditional imports or dynamic `require()`/`import()` gated on build-time values
- Examine Cargo features, Maven profiles, Bazel config_settings

**Catalogue format (write to build-pipeline.md):**

```
AXIS: ENVIRONMENT
  Values: development, staging, production
  Mechanism: NODE_ENV via DefinePlugin
  Impact: enables devtools, changes API URLs, adjusts logging

AXIS: PROVIDER
  Values: aws, gcp, azure
  Mechanism: BUILD_PROVIDER env var, conditional plugin
  Impact: selects cloud SDK, auth module, storage adapter
```

Downstream skills (extract-tool-graph, map-feature-gates) consume this catalogue to know which dimensions to explore. An incomplete catalogue means missed behavior branches.

## Adversarial Lens

If someone wanted to inject code into the build, where would they do it? Check: webpack plugins, postinstall scripts, build-time code generation, bundler transforms. The build pipeline is the most powerful injection point -- it touches everything.

## Red Flags

- Not checking for code generation steps that modify source
- Missing build-time constant injection (DefinePlugin, etc.)
- Ignoring environment-specific build variants
- Skipping a transformation stage in chain analysis (blind spot)
- Failing to document an axis that downstream skills need

## Iron Law

```
Every analyzed build is one filtered slice. You are never seeing the full capability surface.
```

A single build run is one point in a multi-dimensional configuration space. The code you see compiled, bundled, and running is the result of every axis resolved to one specific value. To understand the system, you must map the axes -- not just analyze the one build you happened to run.

## Output Contract

Write `docs/analysis/build-pipeline.md` using standard contract.
Include: pipeline stages, filtering rules, code generation, build-time constants, config axes discovered, transformation chain analysis, Build Dimension Catalogue.
