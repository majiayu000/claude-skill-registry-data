---
name: code-cleanup
description: >-
  This skill should be used when the user asks to clean up or simplify a
  codebase; find dead code, dead features, orphaned files, stale configuration,
  or unused dependencies; detect duplicate or split-brain implementations,
  authorities, caches, parsers, validation, or lifecycles; finish a partial
  migration; remove speculative abstractions or misleading comments; or perform
  an exhaustive every-file cleanup audit. Also trigger when cleaning
  AI-generated code, agent trajectory residue, hallucinated dependencies, or a
  passing patch that is larger than the behavior requires. Not for
  formatting-only cleanup, feature development, or a generic code review with
  no cleanup intent.
---

# Code Cleanup

Understand the whole product before judging its code: who uses it, what they
need, its functional and non-functional goals, boundaries, supported workflows,
non-goals, and pivots.

Review every relevant file in that product boundary, including cooperating
repositories. Dead code often sits outside recent changes. Follow features
through construction, state, persistence, protocols, deployment, recovery,
tests, settings, assets, scripts, and documentation.

Look beyond unused symbols. Find code that compiles, runs, or passes tests but
no longer helps the product; complete dead feature islands whose members keep
one another looking alive; split-brain implementations and parallel
lifecycles; half-removed features; abandoned optimizations and future-proofing;
dead members hidden in large files; misleading comments; unused packages,
imports, features, configuration, environment variables, defaults, and
settings; and residue left by an agent's abandoned approaches.

Tests, helpers, and comments inside a dead island do not prove that it is alive.
Zoom out until the product responsibility is clear, then be willing to delete
the whole obsolete responsibility rather than only its obvious leaves.

When relevant, briefly check compatibility, dependency provenance, concurrent
work, runtime evidence, and UI intent without turning them into a checklist.

Preserve unrelated user work and real external compatibility. Validate the
surviving product with the repository's actual gates and a real boundary when
compilation or mocks are insufficient.
