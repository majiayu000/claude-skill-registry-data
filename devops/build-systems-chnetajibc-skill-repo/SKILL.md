---
name: build-systems
description: "Build systems: source-compile-bundle-transform-test-package-artifact-deploy. Diagnose resolution, cache, reproducibility, env drift, native deps."
---

# build-systems

Reproduce locally, then fix the system — not the symptom.
## Inspection

Reproduce with clean tree + locked deps; identify the failing layer (resolve/compile/bundle/test/package) before theorizing.

## Decision rules

Fix at the layer found; suspect caches, then env drift, then native deps; pin what drifted; document the toolchain.


## Activate when

- Broken/slow/flaky builds; new build, bundle, or packaging setup; native-dependency failures.

## Do NOT activate for

- CI workflow config (see ci-cd, devops/github-actions); dependency selection (see package-management).

## Procedure

1. Reproduce with a clean tree and locked deps; record the exact failing command and output.
2. Isolate the layer: resolution → compile → bundle/transform → test → package. Bisect config changes, don't rewrite the pipeline.
3. Suspect caches first (stale, poisoned, or machine-specific); then environment drift (toolchain versions vs lockfiles/CI images); then native deps (headers, ABI, platform).
4. Fix at the layer found; pin what drifted; document the required toolchain in the repo.
5. Verify: clean build green twice in a row, CI agrees with local, no secrets in build logs.

## Failure modes

Rewriting the pipeline for a cache problem; unpinned toolchain drifting between local and CI; secrets in build logs.

## Escalation

CI config → devops/github-actions; dependency selection → tooling/package-management.
