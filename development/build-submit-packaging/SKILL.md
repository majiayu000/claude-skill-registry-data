---
name: build-submit-packaging
description: "Use for reusable build submit packaging recipes in software and coding-agent work."
---

# Build, package & submit — recipes (generic tier)

On-demand recipes (3). Trigger→action heuristics; pull the relevant one when its situation arises.

#### 1. Native LLM-calling Nim: SSL flag with a compile-time guard, shell to the vendor CLI for cloud auth
`generic`

When compiling an LLM-calling Nim binary, enabling the LLM layer must also enable SSL (Nim's `-d:ssl` flips stdlib httpclient to HTTPS) because provider endpoints like api.anthropic.com and api.openai.com are HTTPS-only; add a static compile-time `{.error.}` guard so hand-builds that forget the SSL flag fail loudly at build time rather than at runtime. When constrained to a subdirectory and forbidden from editing shared files, implement HTTP/JSON with the standard library (Nim std/httpclient + std/json) rather than a third-party HTTP package that would touch the shared lockfile.
  <sub>sources: bitworld/among_them/players/mod_talks/README.md, bitworld/among_them/players/mod_talks/build_modulabot.py, bitworld/among_them/players/mod_talks/LLM_SPRINTS.md, bitworld/among_them/players/mod_talks/LLM_VOTING.md</sub>

#### 2. Split a feature into a compile-ordered PR stack, not topic-wise
`generic`

Split a single coherent feature into a compile-dependency-ordered PR stack (scaffolding types/helpers first, the heavy consumer second, wiring last) rather than by topic: e.g. trace work shipped as 3 stacked PRs each compiling alone (1: branchId/chatLines fields + fired() helpers + branch calls; 2: TraceWriter/tuning_snapshot modules + tests; 3: CLI/FFI/runner wiring + design doc). Splitting by what-compiles-without-what is more reliable than splitting by topic. Stage a tooling migration so failures stay bisectable: combine non-risky setup phases (pyproject + toolchain validation) into one commit, but land the Dockerfile swap and the first league submission as separate commits, and do the docs rewrite LAST because it bakes in real league/division IDs.
  <sub>sources: opencode:ses_2202cf626ffenXSjna0lj4fEs2, archive/cogames_playground/bulbacog/designs/COWORLD_MIGRATION.md</sub>

#### 3. Branch-id / line-number manifest drift is a pending-commit state, not a bug
`generic` · ⚠ _session-derived, unverified_

A generated manifest that records code positions (branch ids, line numbers, e.g. a BRANCH_IDS.md) drifts whenever you insert or move code, so a smoke/CI check comparing it against HEAD is reporting a pending-commit state, not a real failure. Regenerate and commit the manifest together with the change rather than treating the smoke-step failure as a bug.
  <sub>sources: opencode:ses_21fdab7c0ffeyW9gOCR3FyrI7b</sub>
