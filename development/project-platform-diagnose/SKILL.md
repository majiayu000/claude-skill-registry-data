---
name: project-platform-diagnose
description: Diagnostic project overlay for environment-dependent build, install, startup, CI, container, headless, terminal, or runtime failures. Not for ordinary logic bugs or known release packaging changes.
---

# Project Platform Diagnose

This overlay can stand alone for environment-only triage. Add matching language
or discipline guidance when the diagnosis reaches source code or a specialized
implementation boundary.

## When to use

The problem differs by operating system, architecture, terminal, shell, CI,
container, headless mode, installed runtime, service environment, or another
platform fact.

## Not for

Do not use this as primary for a reproducible logic bug (use the matching
principle skill and add `project-core-dev` only when repository-specific
completion evidence is not concrete), a known config-contract defect
(`project-config-and-tests`), Playwright harness or browser installation repair
(`setup-playwright`), vendored dependency ownership (`project-vendor-boundary`),
or release artifact layout (`project-release-maintainer`). Start here only while
the environment remains a plausible cause, then hand off when the failure is
isolated.

## Diagnostic Workflow

1. Inspect the failing command's side effects before rerunning it. Reproduce it
   within existing authority, using an isolated or check-only variant when
   needed, and capture exit status and relevant output. A failed install,
   migration, or deployment is not automatically safe to repeat. Separate build
   or install failures from startup and runtime failures.
2. Record only relevant non-secret facts: OS, architecture, runtime and tool
   versions, shell or terminal mode, local versus CI or container, filesystem
   and permission assumptions, and required services. Never dump the full
   environment or expose credentials.
3. Compare a working and failing environment when both exist. Build the smallest
   difference set and change one plausible variable at a time.
4. Prefer built-in diagnostics and reproducible smoke checks. Use temporary
   directories, disposable containers, or other reversible probes when
   available; clean up created state.
5. Classify direct observations separately from hypotheses. Distinguish an
   environment limitation, missing dependency, install defect, unsupported
   platform, config defect, and app regression before recommending a fix.
6. Report whether the issue reproduced, the discriminating evidence, remaining
   unknowns, and the next smallest probe. Implement a code, config, setup, or
   release fix when the request includes repair, using the matching skill and
   existing authorization; otherwise report the diagnosis.

Do not make permanent machine changes, install system dependencies, or start
external services or GUI applications merely to test a hypothesis without the
required authorization.
