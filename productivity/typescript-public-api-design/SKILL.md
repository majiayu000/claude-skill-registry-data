---
name: typescript-public-api-design
description: Own exported function and module design plus public type ergonomics for TypeScript libraries and backend modules. Use whenever the task is about public entrypoints, `package.json` `exports`, supported import paths, exported function signatures, options objects, overloads versus unions versus generics on a public API, emitted `.d.ts` readability/stability, or whether a public type/API change is compatible for consumers, even if the user frames it as DX cleanup or "make this library API nicer."
---

# TypeScript Public API Design

## Purpose

Own the narrow seam of public TypeScript API design:

- what consumers can import
- what exported functions ask for and return
- what public types expose and imply over time

This skill is about external contract quality, not internal implementation
taste. It does not own general TypeScript cleanup, advanced type tricks as an
end in themselves, framework routing, or internal architecture.

## Specialist Stance

This skill only earns its place if it produces a materially better answer
than generic TypeScript API advice through narrower public-API expertise:

- treat each entrypoint, export, overload, generic, and exposed type as
  compatibility budget
- prefer minimal public complexity over internal convenience
- reason from the consumer view: import path, call site, inference, hover
  text, diagnostics, and semver fallout
- separate observed public surface from guessed public surface
- classify compatibility explicitly instead of hand-waving
- explain why the strongest losing design is too expensive publicly
- lower confidence when emitted types, `exports`, or version/tooling facts are
  inferred instead of observed
- force a more discriminating workflow than generic TypeScript API advice
  would usually apply by default

This skill is not here to re-teach TypeScript basics. It is here to act
like a narrow expert on exported functions, modules, and public type
ergonomics.

If removing this skill would leave the answer mostly unchanged, the skill is
not doing enough work.

If the answer reads like broad "make it more ergonomic" commentary, it is not
yet operating at this skill's quality bar.

## Quality Bar

Reject vague ergonomics commentary.

A good answer from this skill must:

1. identify the primary surface at issue: module surface, call surface, type
   surface, or compatibility/evolution
2. name what evidence is actually visible: `exports`, import paths, exported
   source, emitted `.d.ts`, or explicit assumptions
3. choose the smallest public shape that solves the consumer problem
4. explain the signature choice concretely: overload, union, generic, options
   object, discriminant, or explicit return type
5. state the compatibility posture for the proposed change
6. compare the best tempting alternative and explain why it loses publicly
7. record assumptions, confidence, and at least one residual risk or next
   check when evidence is incomplete
8. stay inside public API design instead of drifting into internal
   architecture, broad style advice, or type-system gymnastics
9. surface at least one public-contract risk, compatibility implication, or
   declaration-surface consequence that would otherwise stay implicit
10. say when the recommendation depends on version-sensitive or tooling-shaped
    behavior rather than durable public-API defaults
11. use explicit evolution controls when the task is about changing a public
    surface over time rather than merely choosing a shape today

If the answer could plausibly come from strong general TypeScript knowledge
without this skill, it is not yet strong enough.

## Scope

- module entrypoints and import-path discipline
- `package.json` `exports`, supported subpaths, and deep-import boundaries
- exported function signatures: parameters, options objects, return shapes, and
  callback contracts
- public type ergonomics: overloads, unions, generics, discriminants, and
  inference quality
- emitted declaration clarity and stability
- compatibility posture for public API evolution

## Public Surface Model

Treat the public surface as three linked contracts:

1. `module surface`
   supported import paths and entrypoints
2. `call surface`
   how exported functions are invoked
3. `type surface`
   what `.d.ts` exposes and what consumer tooling must understand

A strong answer checks all three instead of optimizing only runtime behavior.

## Public Complexity Budget

Default to the smallest surface that remains expressive.

Count these as long-term public costs:

- each exported subpath
- each exported symbol
- each overload
- each generic type parameter
- each ambiguous mode hidden inside one API
- each internal detail leaked through emitted types

Do not add public surface because it is convenient internally or might be
"useful someday."

## Boundaries And Handoffs

Do not absorb adjacent topics.

Hand off when:

- the real issue is strict-mode language semantics, local narrowing, or
  everyday `unknown`/`undefined` discipline
  `typescript-language-core`
- the real issue is advanced conditional, mapped, or template-literal type
  machinery
  `typescript-advanced-type-modeling`
- the real issue is module emit/runtime alignment, ESM/CJS execution behavior,
  or compiler-runtime interop
  `typescript-node-esm-compiler-runtime`
- the real issue is runtime validation or untrusted-input modeling beyond the
  public API seam
  `typescript-runtime-boundary-modeling`
- the real issue is framework or domain behavior rather than TypeScript public
  surface design

Keep this skill narrow even when neighboring seams are nearby.

## Relationship To Shared Research

This skill is the topic-specialist consumer of the shared
`typescript-public-api-design` research boundary. Do not turn it into a broad
TypeScript or library-architecture survey.

Start with this skill file and its local references.

Load `../_shared-hyperresearch/deep-researches/typescript-public-api-design.md`
only when:

- the question is version-sensitive or tooling-sensitive
- the codebase is unfamiliar and the local references are not enough
- you need deeper nuance on `exports`, declaration emission, overload rules, or
  TypeScript 5.9 inference changes
- the first answer still feels too generic and needs a deeper audit map

Version anchor: TypeScript 5.9 public library and backend-module surfaces.
If the codebase depends on another TS version or another module/publication
story, say so explicitly.

## Read These References When You Need Them

- public surface discipline, export curation, and declaration review:
  `references/public-surface-rules.md`
- choosing overloads, unions, generics, options objects, and callback shapes:
  `references/signature-choice-guide.md`
- compatibility classification and confidence calibration:
  `references/compatibility-and-confidence.md`
- audit order for unfamiliar packages or modules with uncertain public truth:
  `references/unfamiliar-codebase-checklist.md`
- pressure-test prompts for turning a plausible answer into a stronger public
  API recommendation:
  `references/reasoning-pressure-test.md`
- managed public evolution, deprecation, visibility, and release-surface
  controls:
  `references/evolution-and-visibility-rules.md`
- version-sensitive and tooling-sensitive public-surface traps:
  `references/version-and-tooling-sensitivity.md`

## Input Sufficiency And Confidence

Before answering, identify whether you have:

- visible `package.json` `exports`, `types`, or `typesVersions`
- visible exported source or emitted `.d.ts`
- real consumer call sites or only a design description
- actual TypeScript/module expectations or only assumptions

Prefer evidence in this order:

1. emitted `.d.ts` plus package metadata plus exported source
2. exported source plus package metadata
3. prompt-only description

Do not speak as if a path is public just because it exists in the repo.
Do not speak as if a type shape is stable just because the source "looks fine"
if the emitted declaration surface was not checked.

Confidence guide:

- `high`
  public entrypoints and declaration shape are visible
- `medium`
  source is visible but emitted types or package metadata are inferred
- `low`
  only prompt text or partial snippets are available

Name the missing fact that would most change the recommendation.

Use `references/unfamiliar-codebase-checklist.md` when the repo is unfamiliar
or the task is an audit rather than a greenfield API design choice.

Use `references/reasoning-pressure-test.md` when the first answer sounds right
but is not yet clearly better than generic TypeScript API advice.

Use `references/evolution-and-visibility-rules.md` when the task changes a
public API over time, needs a deprecation story, or needs visibility/release
discipline rather than a one-shot signature choice.

Use `references/version-and-tooling-sensitivity.md` when module mode,
`typesVersions`, declaration emission, TS version, or consumer runtime/tooling
could change what the public API actually means.

## Workflow

### 1. Confirm Boundary Fit

- decide whether the real question is about what consumers import, call,
  infer, or rely on over time
- if not, hand off instead of stretching this skill

### 2. Map The Actual Public Surface

- list supported entrypoints and subpaths
- list the exported functions and public types under discussion
- identify whether the task changes module surface, call surface, type surface,
  or compatibility policy
- treat `package.json` `exports` and emitted `.d.ts` as closer to public truth
  than folder structure

### 3. Choose The Primary Decision Bucket

Put the problem in one primary bucket before solving it:

- module surface discipline
- signature shape
- public type ergonomics and inference
- compatibility and evolution

If several apply, say which is primary and which are side effects.

### 4. State The Consumer Contract First

Before recommending a change, say what rule or contract does the work.

Examples:

- "`exports` decides which import paths are supported"
- "the first matching overload wins"
- "a generic should relate types instead of decorating the signature"
- "an options object buys growth room but increases shape surface"

This keeps the answer anchored in contract design instead of taste.

### 5. Choose The Smallest Honest Public Shape

Prefer:

- one canonical entrypoint or a small deliberate set
- named exports over accidental file-structure exposure
- explicit return types on exported functions when they stabilize emitted
  declarations
- unions over overloads when the return shape does not vary
- overloads only when different call forms intentionally produce different
  result types
- generics only when they improve consumer inference by relating types across
  the signature
- options objects when configuration is numerous or likely to evolve
- discriminated unions when public modes or result variants need safe narrowing

Do not export helpers, internal intermediate types, or extra subpaths without
an explicit consumer-facing reason.

### 6. Pressure-Test Ergonomics Against Public Cost

Check four things:

- call-site friction
- inference quality
- hover and error readability
- extension path under future changes

If one design is only "more flexible" internally but heavier publicly, prefer
the smaller public shape.

Also ask: what is the tempting first API recommendation here, and what
public-contract consequence does it leave implicit?

### 7. Run The Tooling-Sensitivity Gate

- ask whether `typesVersions`, module mode, `verbatimModuleSyntax`, conditional
  exports, or TS-version behavior could change what consumers actually see
- ask whether emitted `.d.ts` stability depends on inference, `lib.d.ts`, or
  declaration-generation behavior
- if yes, make that dependency explicit instead of presenting the guidance as a
  durable universal rule

### 8. Classify Compatibility Explicitly

For any proposed change, say whether it is:

- `non-breaking`
- `conditionally breaking`
- `breaking`

State:

- what changed
- which consumers are affected
- why the classification fits
- what assumption would change the classification

### 9. Add An Evolution Story When Needed

When the task is not just "pick a shape" but "change a public shape", say how
the surface should evolve:

- immediate switch
- additive expansion
- deprecation period
- visibility trimming or release-tag control

Use explicit public mechanisms such as deprecation markers, curated exports,
and declaration/release-surface review instead of relying on informal team
memory.

### 10. Compare The Best Losing Alternative

Common losing alternatives:

- extra overloads instead of one union or options object
- a generic parameter that does not really relate types
- exporting whole internal utility types "for completeness"
- allowing deep imports instead of curating supported subpaths
- widening the public surface now "just in case"

Name the strongest tempting loser and say why it is too costly on the public
surface.

### 11. Calibrate Confidence And Next Check

- use high confidence only when public entrypoints and declaration shape are
  visible
- lower confidence when the package metadata, emitted types, or consumer usage
  pattern is inferred
- name the smallest next check that would falsify the recommendation if it is
  wrong

### 10. Audit Or Pressure-Test When Needed

- when the repo is unfamiliar, run the checklist instead of jumping straight
  to a redesign
- when the first answer is plausible but still broad, run the pressure test
- when version or tooling behavior could change the public surface, say so
  explicitly instead of burying it in the recommendation
- when the draft feels "already good enough," check whether it is actually
  better than generic API guidance or merely correct in a generic way
- when the change is evolutionary rather than greenfield, make the deprecation,
  visibility, or release-surface control explicit

## Preferred Defaults

- Treat `package.json` `exports` as the owner of supported public import paths.
- Prefer stable curated entrypoints over file-structure-shaped deep imports.
- Prefer the fewest exported symbols that still make the consumer job clear.
- Give exported functions explicit return types when that stabilizes
  declaration output and reviewability.
- Prefer unions over overloads when only parameter types vary and the return
  shape does not.
- Use overloads only when different call forms intentionally produce different
  result types.
- Put more specific overloads before more general ones.
- Use generics only when they improve inference by relating types across the
  signature.
- Default to options objects when optional settings are numerous or likely to
  evolve.
- Use discriminated unions for public result or mode shapes when consumers must
  branch safely.
- Prefer `unknown` to `any` for public boundaries that intentionally accept
  arbitrary input.
- Prefer explicit deprecation and curated visibility controls over "we just
  won't mention this anymore" when evolving a public surface.
- Treat readable emitted types as part of the API, not as documentation
  garnish.

## Failure Smells

- "ergonomic" advice that never mentions import-path support or emitted type
  shape
- compatibility claims with no consumer-side classification
- exporting internals because they might be useful someday
- treating deep imports as safe just because the files exist
- overload sets that differ only in tail arguments or callback arity
- generics that add ceremony without improving inference
- option bags with unclear modes or hidden mutual exclusivity
- huge anonymous return types that leak internal detail into `.d.ts`
- confidence that ignores missing `exports`, `.d.ts`, or TS-version facts
- version/tooling-shaped advice presented as if it were universally stable
- public-surface changes with no deprecation or visibility story
- drifting into clever type construction when a smaller public shape would do
