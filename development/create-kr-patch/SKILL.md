---
name: create-kr-patch
description: >-
  Use for Korean (Hangul) fan translations of retro console or PC games,
  including ROM or disc analysis, text-engine reverse engineering, Hangul fonts
  and custom encodings, script extraction and reinsertion, code hooks,
  reproducible product builds, and emulator verification. Apply it to new
  investigations and follow-up work in existing Korean-patch projects. 레트로
  게임 한글화·한글패치·한글
  패치·ROM 번역의 신규 조사와 기존 프로젝트 후속 작업에 사용한다.
---

# Create a Korean patch for a retro game

## Purpose

Base decisions on evidence from the target game. Keep the evidence and adopted results from the initial survey, fonts and encoding, PoC, extraction, translation, reinsertion, product builds, distributable patches, and runtime verification traceable through completion.

Choose tools, languages, libraries, and fonts based on the target project's existing structure and the current environment. Regardless of those choices, preserve the required capabilities and verification criteria. Look up basic specifications from current primary sources when one straightforward search can recover them.

Treat source-language frequencies and structures from other titles as hypotheses until the target revision confirms them.

## Foundational principle

**Treat each playthrough as the whole product.** Successful paths do not offset a known in-scope defect that can block progress, corrupt text or intended meaning, mislead the player about a choice, break approved terminology or voice, or impair interaction. Fix it, present evidence and feasible options for an explicit human decision to narrow the scope or claim, or withhold the release. See `references/strategy/build-and-verify.md` §6 and `references/strategy/translation-workflow.md` §6.

## Operating principles

1. **Let product closure define the work.** Define the target by what must hold together across its declared scope and claims, not by the current artifact plus the next plausible edit. Credit a result only to the claim it strengthens. Keep the hardest unresolved completion condition—or the one most likely to force redesign—visible, and choose work from it. Among approaches with the same prerequisites and proof scope, prefer the lower total cost of obtaining evidence. See `references/conventions/project-records.md` §1 and `references/strategy/build-and-verify.md` §1·§6.
2. **Keep each evidence loop informative.** Let unresolved uncertainty determine whether static inspection, runtime observation, or both can produce the next discriminating evidence. Keep the exact applicable artifact fixed while affected routes can still yield interpretable evidence; one defect does not require an immediate rebuild. Change the baseline when its question is answered or observation is blocked, contaminated, or unsafe. Conflicting evidence, repeated equivalent evidence, local passes that do not strengthen the cumulative claim, and accumulating exceptions signal reassessment. Restore the baseline, completion condition, and live and rejected explanations; search `references/tips/README.md` by observation before adding another local exception. Cases suggest hypotheses, not repairs. See `references/conventions/project-records.md` §2 and `references/strategy/debugging.md` §2·§3·§5·§6.
3. **Keep product priorities and decision authority separate from implementation.** Current implementation establishes behavior and change cost, not product value. The agent establishes technical facts and feasible options; humans choose product direction, quality, scope, acceptable loss, support, and investment. At a meaningful point of convergence, present the current result and possible gains with their effort, risk, uncertainty, and claim impact. Bind the human choice to that evidence baseline; it is not technical completion or proof that improvement is exhausted. Routine implementation that preserves adopted intent remains the agent's responsibility. See `references/conventions/project-records.md` §1.1 and `references/strategy/translation-workflow.md` §4.1·§5.

## Task-specific guidance

For an existing repository, reconstruct the current code, documents, artifacts, and verification state before choosing the guidance relevant to the next decision. Start with the initial survey when the game or its structure is not yet understood.

| Decision area | Document | Use it to determine |
|---|---|---|
| Initial survey | `references/strategy/initial-survey.md` | Completion-critical conditions, actual dependencies, initial volume, unresolved populations, and revision-specific facts |
| Fonts and encoding | `references/strategy/font-strategy.md` | Code-to-glyph mapping, total repertoire, active working set, representation, and runtime reachability |
| Name entry and user strings | `references/strategy/name-entry.md` | Input repertoire, editing state, committed records, glyph supply, redisplay consumers, and persistence |
| Text extraction | `references/strategy/text-extraction.md` | Population and volume, consumer-defined boundaries and tokens, reversible artifacts, and round trips |
| PoC | `references/strategy/poc.md` | Whether a PoC is needed and what a visibility, representative end-to-end, or conditional PoC must establish |
| Reinsertion and hooks | `references/strategy/reinsertion.md` | Boundary policies, reference completeness, hooks, space, and consumer invariants |
| Translation | `references/strategy/translation-workflow.md` | Translation work and agent assignment, context, approved terminology and voice, protected information and consumer constraints, and high-impact semantic decisions |
| Build and verification | `references/strategy/build-and-verify.md` | Reproducible artifacts, checks enforced by the product build, distribution boundaries, integrity and runtime verification, text and interaction QA, and release readiness |
| Debugging and issue handling | `references/strategy/debugging.md` | Gameplay routes, target-state access, what state intervention can establish, causes, fixes, and regression evidence |
| Graphics text | `references/strategy/graphics-text.md` | Pixel-text population, protected visual assets, and consumer-path verification |
| Compression | `references/strategy/compression.md` | Verified transformation boundaries, consumer compatibility, and repacking verification |
| Runtime asset reachability | `references/strategy/runtime-assets.md` | Storage, lookup, load or transform, residency, and consumption as one connected claim |

Apply the relevant conventions when designing or validating artifacts, exchange data, or records. Keep an existing repository structure when it already preserves the same responsibilities and constraints.

| Scope | Document | Use it for |
|---|---|---|
| Project-wide implementation | `references/conventions/project-conventions.md` | Repository vocabulary and ownership; tooling build, analysis, product build, test, artifact verification, and runtime verification boundaries; machine-code verification; round-trip equivalence and denominator; final-write verification; external-component reproducibility; and source assets |
| Translation artifacts | `references/conventions/translation-artifacts.md` | Source preservation, control tokens, review states, and eligibility as product build inputs |
| Project records | `references/conventions/project-records.md` | Human strategic decisions, survey and PoC decisions, graphics-text catalog, HITL observations, QA evidence, and issue states |
| Analysis and product build data | `references/conventions/data-formats.md` | Character maps, controls, pointers, translation links, reinsertion policies, and font-rendering profiles |

Read a platform document only when a constraint involving hardware, the medium, address space, or rendering can change the current decision.

| Platform | Document |
|---|---|
| SNES | `references/platforms/snes.md` |
| Mega Drive | `references/platforms/megadrive.md` |
| Sega Saturn | `references/platforms/saturn.md` |
| PlayStation | `references/platforms/ps1.md` |
| Dreamcast | `references/platforms/dreamcast.md` |
| PC Engine and CD-ROM² | `references/platforms/pce.md` |
| PC-98 | `references/platforms/pc98.md` |
| Game Gear | `references/platforms/gg.md` |
| Game Boy and Game Boy Color | `references/platforms/gb.md` |
| NES and Famicom | `references/platforms/nes.md` |
| Nintendo DS | `references/platforms/nds.md` |

For an unlisted platform, establish only the constraints that can change the current decision.

## Artifact requirements

Violating one of these requirements invalidates the affected release claim. A mechanically invalid input or artifact must also stop the product build unless the declared development/PoC input policy permits it. Record every exception and the resulting limit on the claim.

- Never commit source ROM or disc images, or unauthorized third-party assets. Follow `references/conventions/project-conventions.md` §6.
- Plan every final change from an immutable source and fail on overlapping writers, protected-range writes, or unexplained final differences. Follow `references/conventions/project-conventions.md` §5.2.
- Never silently skip or substitute a character whose glyph or encoding is missing. An unmapped character fails the product build. A product build under the development/PoC input policy may proceed only under `references/conventions/translation-artifacts.md` §5 and cannot produce a release candidate.
- A rule-based batch transformation that changes translated prose requires prior human approval of the rule, pre-transformation text, scope, and expected impact. Follow `references/strategy/translation-workflow.md` §5.2.
