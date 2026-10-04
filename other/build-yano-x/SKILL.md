---
name: build-yano-x
description: Build, test, publish locally, stage, and assemble the Java 25 JVM-only Yano X repository against an exact Yano Maven/ZIP build identity. Use for clean builds, local coordinated Yano/Yano X development, artifact inventory checks, distribution assembly, release rehearsals, or diagnosing differences between source/test and full distribution builds.
---

# Build Yano X

## Prepare

1. Read `AGENTS.md`, `docs/BUILD_AND_TEST.md`, and, for archives,
   `docs/BUILD_DISTRIBUTIONS.md`.
2. Inspect both repositories with `git status --short`; preserve unrelated
   work and never commit automatically.
3. Require Java 25.
4. Resolve one exact Yano version and the ordinary JVM ZIP produced by that
   same build. Released versions download through Gradle from the matching
   `bloxbean/yano` GitHub release; local or staged builds use an explicit
   `yanoJvmDist`. Never mix version identities.

## Select the build tier

For source compilation, unit tests, and repository-boundary checks, run:

```bash
./gradlew test verifyArtifactInventory verifyJvmOnlyBuild \
  -PyanoVersion=<yano-version>
```

For coordinated unpublished work, first run in the sibling Yano repository:

```bash
./gradlew publishToMavenLocal :app:yanoDistZip \
  -PskipSigning=true --no-parallel
```

Then opt in to Maven Local explicitly in Yano X:

```bash
./gradlew test verifyArtifactInventory verifyJvmOnlyBuild \
  -PyanoVersion=<published-yano-version> \
  -PuseMavenLocal=true --offline
```

For a clean full build against a released Yano version:

```bash
./gradlew clean build \
  -PyanoVersion=<published-yano-version> \
  -PskipSigning=true
```

For a release rehearsal, publish all coordinates to a new empty staging
repository after the clean build:

```bash
./gradlew publishAllPublicationsToInternalRepository \
  -PinternalRepository=<empty-staging-directory> \
  -PyanoVersion=<published-yano-version> \
  -PskipSigning=true
```

Use `distributionCheck` when only distribution gates are required. Do not
invent a special lean base ZIP; Yano X consumes Yano's ordinary JVM ZIP. Add
`-PyanoJvmDist=/absolute/path/to/yano-<same-build-identity>.zip` for local or
staged inputs.

## Diagnose failures

- Treat `config/artifacts-v1.json` as the artifact and bundle identity source
  of truth.
- If source tests pass but `build` fails, inspect the distribution task and its
  exact Yano Maven/ZIP inputs; Yano X bundles are built from project outputs.
- If input verification fails, compare `yanoVersion`, the base ZIP root, the
  host JAR implementation version, and the Yano distribution manifest.
- If bundle verification fails, inspect duplicate/missing contributions,
  embedded host API classes, bundle dependency ranges, and default versus
  optional plugin selection.
- If dependency resolution unexpectedly uses local artifacts, remember Maven
  Local is allowed only with `-PuseMavenLocal=true`.
- Never work around `verifyJvmOnlyBuild` with native tasks; Yano X is JVM-only.

## Report

Report the exact Yano version, ZIP path, Yano X version, commands run, failed
gate if any, and generated distribution paths. Distinguish a focused source
test from a clean full distribution build.
