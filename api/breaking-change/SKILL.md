---
name: breaking-change
description: Detect breaking changes between two OpenAPI specs before shipping, so a change that breaks consumers never ships under the same version. Use before merging any API change and in CI on every spec change. OpenAPI 3.x only. Only invoke via the orcinus router.
license: MIT
user-invocable: false
compatibility: Requires the oasdiff CLI (the eval used v1.35.0); install a prebuilt binary from the official releases or with go install github.com/oasdiff/oasdiff@latest.
---

# BREAKING-CHANGE — did the API break, and is it allowed to?

A renamed field or a removed property is invisible in a code review and fatal to a consumer. This skill compares the API spec consumers already use against the spec you are about to ship, and reports every breaking change with the tool — not by eye.

## Rules

- Baseline first. Keep the previous spec (the one consumers already use) under version control. Never compare against a spec you just wrote.
- Run the tool before merging any API change. A breaking change under the same version is a FAIL.
- A breaking change is only acceptable as a new major version, or with an explicit, recorded decision by the user. Never silently.
- Classify every change: breaking (removed endpoint or field, renamed field, type change, a new required field, stricter validation) or non-breaking (a new endpoint, a new optional field).
- Never report "no breaking changes" without running the tool.
- A check that did not run is never reported as passed.

## Steps, in order

### 1. Baseline

The previous spec lives in the repo (for example `docs/api/openapi.yaml` at the last released version). If there is no previous spec, there is no compatibility to break — but the first spec must then be committed as the baseline before any change.

### 2. Candidate

The new spec, produced by the same process that produces the baseline (hand-written or generated — but the same one, so the diff measures the change, not the generator).

### 3. Run

```bash
oasdiff breaking --fail-on ERR baseline.yaml candidate.yaml
```

`--fail-on ERR` is what makes the command fail: without it, `oasdiff breaking` prints the breaking changes and still exits 0. In CI, always pass `--fail-on ERR` — a gate that cannot fail is not a gate. Use `oasdiff changelog baseline.yaml candidate.yaml` for the full list of changes, and `oasdiff validate` on each spec first — a diff between two invalid specs is meaningless.

### 4. Classify

Read the output. Every breaking change is named with its location (endpoint, field, property). Every non-breaking change is an addition. If the tool reports nothing, there is nothing to classify.

### 5. Verdict

- PASS: no breaking changes. The change may ship under the same version.
- FAIL: breaking changes under the same version. Fix by making the change additive (see `api-and-interface-design`), or ship a new version — and only with the user's explicit confirmation.

## Report

Return the report in this form:

- Baseline spec path and version; candidate spec path and version.
- The exact `oasdiff` command run (including `--fail-on ERR`) and its exit code.
- Each breaking change, with its location and what changed.
- Each non-breaking change, listed once.
- Verdict: PASS or FAIL, and what must happen next (make it additive, or ship a new version).

## Scope

OpenAPI 3.x specs only. This skill detects breaking changes in an API contract; it does not test the implementation — that is what unit, E2E, and contract tests are for. It does not cover GraphQL schemas or internal module boundaries (those are `api-and-interface-design`'s concern).

## Sources

Method, in our own words, using oasdiff (oasdiff/oasdiff, Apache-2.0, licence verified from the primary LICENSE file) as-is. No code was copied from oasdiff. Install it from the official releases (a prebuilt binary for your platform, or `go install github.com/oasdiff/oasdiff@latest`); the eval used the official v1.35.0 linux/amd64 release binary, checksum-verified against the release `checksums.txt`.
