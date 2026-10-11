---
name: typescript-node-esm-compiler-runtime
description: Own TypeScript plus Node.js ESM compiler/runtime correctness. Use whenever the real question is why TypeScript compiles but Node fails, how `tsconfig`/`package.json`/entrypoint/runtime mode must align, whether relative imports should use `.js` or `.ts`, how `nodenext`/`node20`/`verbatimModuleSyntax`/`rewriteRelativeImportExtensions` affect emitted artifacts, or how dev/test runners drift from production, even if the user frames it as an ESM migration, `ERR_MODULE_NOT_FOUND`, tsx or ts-node trouble, import alias breakage, or "works locally but fails in CI/prod."
---

# TypeScript Node ESM Compiler Runtime

## Purpose

Use this skill to reason about TypeScript plus Node.js ESM correctness as one
joined toolchain problem.

This skill owns the seam where all of the following must agree:

- what Node will load and how it classifies modules
- what TypeScript resolves, preserves, rewrites, or emits
- what files and import strings actually exist on disk

It is not a general TypeScript style guide, not a generic ESM migration guide,
and not a substitute for broader runtime/devops design.

## Specialist Stance

The goal is not to re-teach mainstream ESM advice.

The goal is to reason more narrowly and more exactly about this seam than
generic ESM guidance would.

This skill should add value by:

- forcing the first plausible ESM fix to prove itself against runtime truth,
  compiler truth, and artifact truth
- surfacing mismatches and hidden constraints instead of flattening them into
  "ESM is tricky"
- preferring the smallest honest toolchain contract over option piles, loaders,
  and migration folklore
- separating what was inspected from what was merely inferred
- explaining why the tempting workaround still leaves drift or future breakage
- ending with the smallest check that could falsify the recommendation

If removing this skill would leave the answer basically unchanged, the skill is
not doing enough work.

## Expert Goal

Do not spend time restating most mainstream Node, TypeScript, and ESM
basics.

This skill succeeds only when it materially improves the reasoning process:

- narrow the problem to the exact compiler/runtime seam instead of answering
  with broad migration commentary
- turn vague module-system advice into explicit runtime contracts and failure
  semantics
- identify the strongest hidden mismatch, the strongest tempting shortcut, and
  the first place the recommendation can still fail
- reduce the configuration and tooling surface instead of decorating a drifted
  setup with more options

Do not restate known best practices. The skill succeeds only when the
final answer is more discriminating, more minimal, and more falsifiable than
generic ESM guidance.

## Expert Thinking Contract

Use this skill to improve answer quality along four axes:

1. `Truth-source discipline`
   Distinguish Node runtime truth, TypeScript compiler truth, and artifact
   truth on disk.
2. `Minimality`
   Recommend the fewest settings and runtime conventions that preserve
   correctness. Every option must close a named mismatch.
3. `Failure concreteness`
   Name the likely runtime failure mode, the first discriminating check, and
   the layer where the problem actually begins.
4. `Honest uncertainty`
   Lower confidence when the real start command, `package.json`, effective
   `tsconfig`, or emitted output has not been inspected.

The skill succeeds only if it makes the answer more exact, more
discriminating, and more operationally honest than generic ESM guidance.

## Relationship To Shared Research

Start with the local references in this skill.

Load `references/toolchain-invariants.md` by default.

Load `references/package-and-specifier-contracts.md` when the question turns
on:

- `package.json` `"type"`, `"exports"`, or `"imports"`
- `.mjs/.cjs` versus `.js`
- `.js` versus `.ts` relative specifiers
- whether an alias belongs in `tsconfig.paths` or the Node runtime contract
- CJS interop shape from an ESM entrypoint

Load `references/mode-specific-hard-anchors.md` when the answer needs compact
concrete anchors rather than only abstract reasoning, especially for:

- canonical `tsc -> dist -> node` posture
- native `.ts` execution caveats and its real limits
- `.mts/.cts` versus `.mjs/.cjs` mixed-format cases
- source-map pairing between compiler output and Node runtime flags
- runner or loader choices that might drift from the production contract

Load `references/minimal-config-surfaces.md` when the question turns on the
smallest correct config shape for:

- `tsc -> dist -> node`
- Node native `.ts` execution with type stripping
- runner-mediated dev/test flows that must stay honest about production parity

Load `references/runtime-failure-modes.md` when the task is triage, debugging,
or a "why does Node fail after compile?" question.

Load `references/unfamiliar-codebase-checklist.md` when auditing an existing
repository or when the true runtime contract is still unclear.

Load `../_shared-hyperresearch/deep-researches/typescript-node-esm-compiler-runtime.md`
only when:

- the codebase is unfamiliar and the local references are not enough
- the answer depends on version-sensitive Node or TypeScript caveats
- the recommendation depends on nuanced trade-offs around type stripping,
  `nodenext` versus frozen Node modes, source maps, or loader behavior
- you need the wider investigation map rather than the compact local lens

Version anchor: TypeScript 5.9 and Node.js 24 LTS+ ESM. If the real toolchain
differs, say so explicitly and reduce confidence.

## Relationship To Neighbor Skills

- Use `typescript-language-core` when the real issue is TS type semantics or
  strict-mode language behavior rather than compiler/runtime alignment.
- Use `node-runtime-devops-spec` when the main question is boot flow, env
  loading, shutdown, or deployment/runtime shape beyond module and emit
  correctness.
- Use a broader architecture skill when the real problem is package/module
  decomposition after the compiler/runtime contract is already settled.

If the task crosses seams, keep this skill focused on compiler/runtime truth
and hand off the rest explicitly.

## Use This Skill For

- deciding whether the runtime is compiled JS, native `.ts`, or runner-driven
- choosing `.js` versus `.ts` relative specifier strategy
- choosing `module`, `moduleResolution`, `verbatimModuleSyntax`,
  `rewriteRelativeImportExtensions`, or related settings when they change
  runtime correctness
- checking `package.json` `"type"`/`"exports"`/`"imports"` against emitted
  files and start commands
- auditing `dist/` artifact correctness and source-map posture
- debugging `ERR_MODULE_NOT_FOUND`, `ERR_UNSUPPORTED_DIR_IMPORT`, format
  mismatches, alias drift, or "works in tsx but not in node dist"
- deciding whether Node native type stripping is actually compatible with the
  code shape

## Toolchain Truth Model

Treat every task in this seam as a three-system alignment problem:

1. `Runtime truth`
   What Node actually executes: entry command, package `"type"`, file
   extensions, ESM resolver rules, and loader behavior.
2. `Compiler truth`
   What TypeScript accepts, how it resolves specifiers, and what it preserves
   or emits.
3. `Artifact truth`
   The real emitted files and the exact import strings that exist on disk.

The answer is incomplete if it cannot say which of these three is currently
authoritative for the failure or design choice.

Import strings are runtime ABI, not a stylistic detail.

## Preferred Defaults

- Default production posture: `tsc -> dist -> node` unless the task explicitly
  commits to native `.ts` execution.
- When Node executes emitted JS, prefer Node-oriented compiler modes instead of
  bundler-style assumptions.
- For `tsc -> dist -> node`, prefer `.js` relative specifiers in source so the
  emitted JS is already runtime-correct.
- Use `.ts` relative specifiers only when the runtime truly executes `.ts`
  files and the code shape stays inside that mode's constraints.
- Prefer `package.json#imports` over `tsconfig.paths` when Node itself must
  understand an internal alias.
- Treat loaders, runner magic, and extensionless-resolution tricks as
  workarounds to justify, not defaults to assume.

## Reasoning Obligations

Do not stop at the first answer that sounds plausible. A strong answer in this
seam must make the following explicit when relevant:

- which runtime mode is actually in play
- which package boundary or extension rule decides module format
- which compiler settings materially affect runtime behavior or emit
- whether the emitted or executed files were inspected or merely assumed
- whether the advice is a stable platform invariant, a compiler choice, a
  tool-specific workaround, an explicit assumption, or a handoff
- what the strongest tempting shortcut is and why it still loses
- what the first likely failure is if one assumption turns out false

If the answer does not classify the recommendation at that level, it is still
too vague.

## Input Sufficiency And Confidence

Before answering, identify the minimum missing facts:

- what exact command runs the code in development, tests, CI, and production
- whether Node executes `.js` from `dist/`, `.ts` directly, or a runner/loader
  path
- what the nearest `package.json` says about `"type"`, `"exports"`, and
  `"imports"`
- what the effective `tsconfig` says about module and emit behavior
- what relative import strings look like in source and, if applicable, in
  emitted output

If the repo is available, inspect the real files instead of assuming them.
Prefer `tsc --showConfig` when layered `tsconfig` files may hide the effective
truth.

Confidence guidance:

- `high` when runtime mode, package truth, effective compiler settings, and at
  least one executed or emitted artifact were inspected
- `medium` when most of the contract is visible but one important layer is
  still inferred
- `low` when the answer is built mainly from prompt description or partial
  config

If confidence is not high, say what to inspect next before anyone should rely
on the recommendation.

## Diagnostic Workflow

1. Confirm the execution mode.
   Decide whether the runtime is:
   - compiled JS via `node dist/...`
   - native `.ts` execution through Node type stripping
   - runner-mediated execution such as `tsx`, `ts-node`, or loader-driven flows
2. Read the runtime truth.
   Inspect the actual start command, entrypoint path, nearest `package.json`,
   and any extension or `"type"` rules that decide whether `.js` means ESM or
   CJS.
3. Read the compiler truth.
   Inspect effective `tsconfig` settings that shape resolution or emit, not
   just the top-level file if `extends` may change the result.
4. Read the artifact truth.
   Inspect source specifiers and, when applicable, one or two emitted files in
   `dist/` to see whether the import strings already match what Node will
   resolve.
5. Classify the mismatch.
   Name whether the problem is:
   - stable Node ESM behavior
   - TypeScript emit or resolution behavior
   - runner or loader drift
   - package boundary or alias mismatch
   - unsupported syntax/runtime expectation mismatch
6. Choose the smallest correct fix.
   Remove drift instead of stacking more tooling. Keep only the settings and
   conventions that preserve the actual runtime contract.
7. Pressure-test the shortcut.
   Name the most tempting workaround and why it would still leave hidden drift
   or future breakage.
8. Return concrete next checks.
   End with the smallest validation step that proves the recommendation on the
   real toolchain.

## Failure Smells

- extensionless relative imports in a Node ESM runtime
- directory imports used as if Node ESM searched `index.js`
- `.ts` import paths in code that is supposed to emit runnable JS without a
  matching rewrite strategy
- `tsconfig.paths` or IDE aliases treated as if Node resolves them natively
- `package.json` `"type"` disagrees with the file format that the emitted code
  assumes
- `tsx` or `ts-node` passes locally while `node dist/...` is the real
  production contract
- `verbatimModuleSyntax` is absent even though import preservation matters
- advice recommends an experimental loader or specifier-resolution trick as the
  baseline contract
- the answer names `nodenext`, `node20`, or `rewriteRelativeImportExtensions`
  without saying which runtime mode makes that choice correct

## Escalate When

Escalate if:

- the real issue is ordinary TypeScript typing or API design rather than
  module/runtime alignment
- the question is dominated by process lifecycle, container entrypoints, or env
  handling rather than compiler/runtime correctness
- the actual runtime is bundler-first or browser-first rather than Node service
  execution
- the codebase hides the true runtime contract behind generated build logic and
  you cannot inspect the real start/build path
- version-sensitive behavior could change the answer materially and the version
  is unknown

## Deliverable Shape

Always return the final recommendation using these sections:

1. `Runtime Mode`
   State what is actually executed and which layer is authoritative.
2. `Observed Facts And Assumptions`
   Separate inspected facts from inferred setup.
3. `Compiler / Package Contract`
   Name the `tsconfig` and `package.json` choices that matter.
4. `Artifact / Specifier Contract`
   State what import strings and files must exist for the runtime to work.
5. `Failure Mode Or Risk`
   Name the concrete runtime failure or the likely failure if left unchanged.
6. `Minimal Recommendation`
   Give the smallest fix or config surface that preserves correctness.
7. `Rejected Shortcut`
   Name the most tempting workaround and why it loses.
8. `Confidence And Next Checks`
   State confidence and the smallest validation step.

If the task is an audit rather than a single bug, keep the same output shape
but turn the recommendation into the current contract plus the required
corrections.

## Quality Bar

Reject shallow ESM commentary.

A good answer from this skill must:

- identify the actual runtime mode instead of assuming one
- classify claims as platform invariant, compiler behavior, workaround,
  assumption, or handoff
- anchor the answer in real package/config/artifact evidence when available
- be more discriminating than generic ESM guidance, not just longer
- name at least one concrete runtime failure mode or mismatch seam
- surface at least one hidden dependency, mismatch, or falsification check
  that materially changes the recommendation
- prefer the smallest justified config surface over option accumulation
- explain why the strongest tempting shortcut still loses
- lower confidence when effective config or runtime truth is inferred
- hand off cleanly when the problem is really about another seam

The answer is not good enough if it stays at broad "migrating to ESM"
talking points instead of tying the recommendation to the repo's actual
runtime, compiler, and artifact contract.
