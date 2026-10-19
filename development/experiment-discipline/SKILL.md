---
name: experiment-discipline
description: "Use for reusable experiment discipline recipes in software and coding-agent work."
---

# Experiment discipline — recipes (generic tier)

On-demand recipes (14). Trigger→action heuristics; pull the relevant one when its situation arises.

#### 1. Deployed behavior is the built image, not your checkout: verify the running artifact
`generic` · ⚠ _session-derived, unverified_

'Latest source' is not 'what is running': in one case the player was unpatched on origin/main, the server was fixed at mettagrid 0.26.20, but the published hosted-game image was pinned to 0.26.17 (pre-fix), so the broken thing was the deployed image. To answer 'is the bug upstream-resolved?' separate (1) what local code does, (2) what the failure does at runtime, (3) whether the deployed image runs that code; capture the image's pinned dependency versions and check the live pod's image/env. A merged-looking PR can ship a capability OFF by default (a reporter inference-credentials PR added the capability but defaulted it off; the PR even showed mergedAt:null while closed), and an adjacent PR is not your fix - PR #15221 added AWS_REGION to already opted-in pods, but the real failure was the historical inference-enable flag never reaching the pod (a direct-Anthropic 404 proving inference was never selected), so a region fix cannot move a 404. Before trusting post-fix verification, compare build vs run timestamps: a coworld-runner:latest digest rebuilt at 22:25 UTC made a 22:22 probe run on the OLD runner. Crewrift's deployed behavior is tied to an ECR image build (public.ecr.aws .../crewrift:latest, rejected as linux/arm64 - point local runs at a downloaded linux/amd64 image instead).
  <sub>sources: claude-code:3837ef5e-3e9c-41bc-b290-df5865581698, claude-code:cd2e0b52-b541-4e03-9fd3-798db4591603, codex:019e8a74-7b9b-77b3-a5f9-968a746f6d93, codex:019e8afb-efcd-7ca0-820f-0320501ef2fa (+4)</sub>

#### 2. A green count is meaningless if tests don't run, don't collect, stub the failing integration, or pass for the wrong reason
`generic` · **negative result**

Several silent false-green modes recur. Writing a test file is not running it: a Nim test module that only got a static read for syntax never caught type/signature/logic errors — treat un-compiled, un-run test code as unverified, with compile+run as the real gate. A green count can hide zero execution: ~1200 lines of OCR tests used bare `from perception import ...` while the module was `orpheus.perception`, so they were skipped on import error and 'passed' by never collecting, and parametrized tests over `fixtures_for_view('<view>')` silently generate ZERO cases when no fixture matches — defend with strict pytest collection or an asserted expected-count, and fail hard or explicitly skip-with-reason on empty parametrization. A test can also pass for the WRONG reason: assert the full ORDERED set not just the first item (an OCR test 'passed' only because a dropped first line aligned the expected second), align fixtures with the ACTUAL selection predicate (a test set arrow_visible while logic keyed on icon_visible/active), and lock in the behavioral invariant (target held across perception flicker). A test that generates a code/policy file must IMPORT it (the cogames suite missed an empty-class-body bug by patching short_names instead of exercising strip-to-empty), and a green smoke test must use REAL captured frames (testdata/phase_*.bin, 8192-byte frames per phase) — a blank frame reproduces the all-noop validation-gate failure and gives a false negative. When tests stub/monkeypatch the exact integration that fails in production, the green suite is false confidence: a pydantic import error, contract regex contamination, and an incomplete action table were all masked by stubs, so keep at least one end-to-end test running the real pipeline against real game source. Make malformed-frame coverage explicit: feed the partial observations a live server emits (chat with no chatroom, overworld with no self-position, role-reveal with null role/team, unknown color/shape, non-positive room size) and assert the belief state degrades gracefully. Write belief-update tests one-behavior-per-test from hand-constructed perception dataclasses, not parsed frames, so failures point at the update rule not parsing.
  <sub>sources: claude-code:d59631cb-a50e-42e8-a102-56ffb0864b55, codex:019e0142-683b-72a2-b8b7-d3f985d5e433, codex:019e03bc-5520-7e72-aa5c-a572ead62b91, codex:019e03bf-6d47-7093-a40b-351c325bde5a (+6)</sub>

#### 3. Validate parsers and pipelines against real captured artifacts and a ground-truth oracle, never only synthetic fixtures
`generic` · _see related: U0372 (other tier)_

Never trust a parser or perception module validated only against your own synthetic fixtures: if every test input came from the same fixture helper, the parser has only ever read what that helper produces. Capture at least one REAL artifact from an actual run and re-run the parser against it before declaring it correct. Validate a ported/rewritten module byte-exact against a ground-truth oracle on a fixed fixture set before merging: build the oracle as a small program that imports the original implementation, runs each fixture, and serializes computed output fields to checked-in JSON sidecars (more robust than scraping the original tests' assertion strings, and trivially extended to new fields). For a layered pipeline the highest-value tests are the integration seams and the negative paths/invariants (empty state doesn't crash; an already-handled item isn't re-processed; each handler processes an event exactly once), because two stages can each pass in isolation while their interface is wrong. When rewriting a rule, write a test for exactly the corner case where the old and new rules disagree, and encode each observed real-world false-positive as a regression test.
  <sub>sources: auggie:5d1ff8d5-2505-4dca-af45-56d3070363e2, claude-code:10f74020-e0e6-4515-8d0c-f071d41766ad, claude-code:e32290d2-800b-4c28-8f9d-ac6f65e9ae76, players/archive/players/among_them/coborg/DESIGN.md (+8)</sub>

#### 4. Cap paid inference with a same-code-path mock provider and a generation cache
`generic` · tool: `--llm-mock:fixtures.jsonl` · _see related: U0373 (other tier)_

Cap paid inference during development: default the iterate loop to a mock/deterministic provider and spend real tokens only on a deliberate, budgeted smoke test. Implement the mock on the SAME code path as live (e.g. a fixture-replay provider with strict FIFO and kind-mismatch detection that auto-errors when fixtures run out, so the system degrades to its real fallback) — this exercises the real code minus the network call, costs nothing, and lets the acceptance matrix cover {no-mock, mock-basic, mock-errored} to test success AND error handling. When iterating a model/classifier against a shared, queue-bound inference worker, build a generation cache: generate reference and test outputs once, then read the cache offline so iteration runs in seconds with zero worker calls.
  <sub>sources: claude-code:b952ba45-d32f-4ce0-a227-c691de8c588f, codex:019e13e1-e883-7fe0-93b4-54adeac75285, codex:019e14a5-e574-7770-953b-17019f2f5e74, bitworld/among_them/players/mod_talks/LLM_SPRINTS.md (+1)</sub>

#### 5. Revert a speculative dependency added to chase a crash once nothing imports it
`generic` · **negative result** · ⚠ _session-derived, unverified_

A speculative dependency added to chase a crash is a dead end if nothing in your own source actually imports it; revert it once you find the true root cause. (Concrete instance: adding torch to a local venv to fix a player crash was wrong — nothing in the source imported torch, the crash came from a dependency inside the image, and the real bug was a wrong policy URI; cleanup was `uv remove torch && uv sync`.)
  <sub>sources: claude-code:c6fec691-565c-406d-b7dd-37e9387f5475</sub>

#### 6. When culling tests, distinguish obsolete from currently-inconvenient
`generic` · ⚠ _session-derived, unverified_

When aggressively culling a test suite, distinguish obsolete from currently-inconvenient: tests removed for heavy external deps (e.g. ML/runtime libs) may still be load-bearing for the repo's mission, so confirm a test is truly redundant before deleting and be ready to restore deletions when the human pushes back.
  <sub>sources: auggie:c9f833a1-50e8-4526-8839-f438394f903e</sub>

#### 7. Bind tests to the live implementation, update behavior/stage tests in the same edit, and test at the true blast radius
`generic` · ⚠ _session-derived, unverified_

Bind tests to the live implementation, not to a spec or design doc: inspect the real module APIs, dataclass field names, and existing test conventions first, because tests against an assumed API pass by accident or fail for the wrong reason. When a refactor swaps a stub for real behavior, expect placeholder-asserting tests to fail and update them toward the new real output rather than bending the implementation back toward the stub; distinguish a test encoding a real contract from one encoding a temporary placeholder. A change that shifts when downstream behavior triggers (e.g. adding hysteresis/debouncing) breaks fixture/replay-based behavior tests, so update those alongside the unit test and run focused tests first to isolate sequencing mistakes before the full suite. Add a focused regression assertion to the existing test for a bug class rather than a new file. When a change touches a public constructor used across the codebase, run the FULL suite because the blast radius exceeds the one file edited. When the suite surfaces a failure outside your blast radius, triage it as a pre-existing unrelated regression and report it separately before 'fixing' it. Before mass-rewriting failing-to-collect imports, confirm the file's intended run command and which package copy it targets, since identically-named files may run against parallel packages and a blind rewrite would 'fix' them into the wrong layout.
  <sub>sources: codex:019e03bf-982c-7fc0-8ba9-d4c640feb779, codex:019e067b-643a-7100-abdb-8d6a0c79d242, codex:019e081d-ff5d-7111-90ab-9b441207a6ee, codex:019e04e9-c357-7c71-a255-929f3a97fda1 (+5)</sub>

#### 8. Smoke-import scaffolds, write full coverage then tighten, confine synthetic payloads to unit tests, and never claim green when the real suite didn't run
`generic` · ⚠ _session-derived, unverified_

Smoke-test a freshly scaffolded module set with one import-everything command (`python -c "from <pkg> import a,b,c; print('OK')"`) before moving on — cheap, and catches circular imports and cross-module reference errors. A smoke test that merely asserts imports are not None ('22 imports are not None') gives no signal; assert the module's __all__ matches a known export list to get a real API-stability contract. When given a line budget for a generated test file, write full coverage and verify it passes, then tighten while preserving test names and coverage (37 tests tightened to a 700-line target, green in ~0.04s) — do not pre-trim coverage to hit the number. When a sandbox blocks dependency installation, fall back to dependency-free verification (syntax compile, --help smoke test, a direct golden-fixture detector check with a temporary stub) and state plainly that the full suite never executed; do not claim green, and name the remaining risk. Synthetic fixtures leak into results and create false signals: a hand-made synthetic packed frame (bytes([0x0F]) * 8192) made only to smoke-test a path produced a saved e2e label reading 'corrupted/unreadable' that looked like a pipeline bug — confine synthetic payloads to unit tests and clearly label demo/e2e artifacts so a later reader doesn't mistake fixture noise for real behavior. The generator's own unit tests passing is necessary but not sufficient; regenerate any checked-in sample output bundles whenever the generator changes, then run the generated-artifact tests, because stale committed artifacts silently diverge from the current generator and the generated agents' tests are the real signal.
  <sub>sources: codex:019e03bf-982c-7fc0-8ba9-d4c640feb779, codex:019e067b-643a-7100-abdb-8d6a0c79d242, codex:019e06a0-5754-74e0-baf2-771853591aaa, codex:019e090d-a88d-76f2-b1f5-cd3e4eda9381 (+2)</sub>

#### 9. Grep every world for the same gap when a clean-builder fix applies to one, and sweep for disabled tests / dead shims before committing
`generic` · ⚠ _session-derived, unverified_

When a fix applies to one location, grep every analogous location for the same gap before declaring done, especially a gap whose failure only appears on a clean machine: merging one fix may not surface the others because the broken state was masked locally (a resolution bug present in multiple repos was hidden because the failure only showed on a clean checkout). Before committing, run a disabled-test sweep (no new skips/xfails in the files you touched) and check for unused backwards-compatibility aliases; remove a compat shim nothing consumes rather than shipping a dead alias.
  <sub>sources: codex:019e74bf-7764-7fd2-82e5-8f66c5ff9e1d, codex:019e9354-431e-7ae1-95a8-358bb4cf53de</sub>

#### 10. Commit after EVERY A/B experiment — code + notebook + regenerated index in one commit; never bisect uncommitted changes
`generic`

Commit the working tree immediately after every experiment or coherent checkpoint, not only when asked, as one commit pairing the code change with its log/notebook entry and any regenerated index in the SAME commit. Accumulating uncommitted changes makes bisection destructive: ~30 stacked uncommitted experiments left no per-experiment checkpoint, and an ad-hoc git checkout of individual files silently created inconsistent cross-file state and destroyed in-progress edits. Per-experiment commits make diff/revert between a good and bad state trivial. NEVER bisect uncommitted changes by mixing git stash with git checkout HEAD on individual files, because checkout overwrites edits the stash never saved; if changes are uncommitted, bisect by toggling config flags or stashing the whole tree.
  <sub>sources: archive/cogames_playground/alpha_cog/experiments/notebook/protocol.md, alpha_cog/AGENTS.md, ses_21ad34e50ffeH2H7gvf2BD1BAq, ses_21b3c677dffe3YCY8JnACrbDmu (+1)</sub>

#### 11. Grep for TEMP/DEBUG markers before evaluation and prepare a concrete revert before risky edits
`generic` · ⚠ _session-derived, unverified_

Temporary debug overrides left in policy code (a '# TEMP: force mask to 3 on frame 100' line) survive refactors and silently corrupt results — routinely grep any player for TEMP/DEBUG/forced-action markers as a pre-evaluation audit. For risky policy edits follow an explicit workflow: bookmark current state -> write down exactly what you'll do -> do it -> test -> if it fails, note it and revert, with a concrete revert command prepared IN ADVANCE (git checkout action.nim, or a /tmp backup).
  <sub>sources: ses_201972733ffexPIP9mq6yEDpqJ, ses_21a708a4dffeBXpeHY15fnGABP</sub>

#### 12. Prove a diagnosis with xfail reproducers and a disproven-theory checkpoint; commit per phase
`generic` · ⚠ _session-derived, unverified_

For a multi-root-cause bug, write expected-failure (xfail) reproducer tests FIRST, one per cause, confirm each fails for the INTENDED reason (run its body, check the specific assertion error), then fix phase-by-phase flipping each xfail to a real pass -- this prevents declaring victory on a test that passes for the wrong reason. When a debugging session goes in circles, write a structured checkpoint report (theories, what was tried, results, theories concretely DISPROVEN with their disproof, most-promising remaining and how to test them). Commit per coherent sub-phase with that phase's tests green so each reviewable commit aligns to a design-doc boundary.
  <sub>sources: opencode:ses_21e25877effeMecaawB2dUys7v, opencode:ses_21eb30b06ffeL6353Ov27zhdA1, opencode:ses_21b7f7f7cffeDDc56Goq1NPBmv</sub>

#### 13. Self-audit research reports, calibrate confidence per category, and verify quickstarts from PyPI
`generic` · **negative result** · ⚠ _session-derived, unverified_

After producing a research report, run a self-audit pass: scan generated docs for hard claims, re-verify installed/imported package paths and CLI output against source, and look for contradictions or claims from a misrouted command. Calibrate confidence per claim CATEGORY, not one number: mechanics from installed source ~95%, strategy heuristics ~70-80%, public tournament details ~60-70% (can change), CLI shortcuts low (stale-shebang risk). To verify a new-user quickstart, reproduce in a fresh venv (Python 3.12) installing from PyPI, NOT the monorepo: a cogames binary on PATH and uv source overrides mask published behavior -- walk the tutorial until the first real error.
  <sub>sources: opencode:ses_2240b911bffeRPYWAkhpoMH1eS, opencode:ses_225b0e431ffeBSef5TF1fgbUHN, opencode:ses_225c247a2ffeNgrsANZfMMyih3</sub>

#### 14. Cull a lesson contradicted by later evidence, but record why
`generic` · **negative result**

Treat a lesson contradicted by later evidence as a finding: cull it, but record a note in the commit message explaining the contradiction, because negative results are themselves valuable signal that prevents re-learning the same dead end.
  <sub>sources: optimizers/.cursor/skills/lessons-review/SKILL.md</sub>
