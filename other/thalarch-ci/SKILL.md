---
name: thalarch-ci
description: >
  Diagnoses and reviews CI/CD, GitHub Actions, build pipelines, packaging, signing, and release
  automation. Use for failing checks or workflow changes. Separates log evidence from guesses,
  reviews untrusted input and token permissions, and never deploys/releases merely to test a fix
  unless explicitly authorized.
---

# Thalarch CI

## CI failure path

1. Identify the exact failing job/step.
2. Read the relevant log around the first actionable failure.
3. Map it to repository workflow/config/source.
4. Compare with the last known working configuration when possible.
5. Form and test one hypothesis.
6. Fix the smallest source/config surface.
7. Validate workflow syntax/config and targeted build locally where possible.

## Workflow security

For workflow changes inspect:
- untrusted event/input interpolation;
- `pull_request_target` / privileged trigger semantics;
- token permissions;
- secret exposure;
- mutable third-party actions;
- self-hosted runner exposure;
- artifact/download trust boundaries;
- shell injection through expressions/env.

## Side effects

Build/test is not permission to:
- publish;
- deploy;
- sign production artifacts;
- create a release;
- push/merge.

Those need explicit authorization.
