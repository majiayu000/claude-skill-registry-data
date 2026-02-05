---
name: typescript-taste
description: Apply rigorous TypeScript type design with strong inference, minimal constraints, and sound fallbacks.
metadata:
  short-description: TypeScript type design taste
---

# TypeScript Type Taste

Use this skill for strict TypeScript type design and tradeoff-driven generic design.

## Examples

Read only when a concrete example is needed.

- Inference alignment: align generics to the primary type — references/INFERENCE_ALIGNMENT.md
- Unreachable branches: encode impossible paths with never — references/UNREACHABLE_BRANCH.md
- Union call sites: avoid impossible intersections — references/UNION_CALL_SITES.md
- Constraint minimalism: keep constraints minimal — references/CONSTRAINT_MINIMALISM.md

## Workflow

1) Identify the primary input surface such as function params, config object, or constructor.
2) Align generics to that surface so inference follows the call site.
3) Constrain only what is necessary and avoid structure that blocks valid inputs.
4) Encode unreachable branches with never and use unknown only when reachability is uncertain.
5) Derive result types from inputs with infer or indexed access.
6) Validate mixed call paths so unions stay usable and do not collapse into intersections.

## Heuristics

- Prefer whole-type constraints over inner type parameters when no inner type is clearly primary.
- Keep generic names short and consistent, and only make them descriptive when it reduces confusion.
- Avoid parallel generics that can be derived from inputs.
- Use minimal constraints that preserve inference and soundness.

## Checks

- Inference: callers get the right type without explicit generics.
- Compatibility: unions remain unions and do not collapse into intersections.
- Strictness: works under strict, exactOptionalPropertyTypes, and noUncheckedIndexedAccess.
