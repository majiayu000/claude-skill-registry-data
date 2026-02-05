---
name: color-pipeline-implementer
description: Implement or adjust the core color pipeline (parse, normalize, scale, resolve) guided by src/planning/spec-v0.3.md and src/planning/roadmap-v0.3.md.
---

# Color Pipeline Implementer

Use this skill when implementing or adjusting the color pipeline stages. Use the v0.3 docs as the source of truth.

## Workflow

1. Read `src/planning/spec-v0.3.md` and the relevant phase in `src/planning/roadmap-v0.3.md`.
2. Implement parsing in `src/utils/parseColor.ts` (hex/rgb to OKLCH, preserve alpha).
3. Implement normalization in `src/engine/normalize.ts` (clamp L/C/H, defaults, basic validation).
4. Implement base scales and semantic resolution in `src/engine/` as per spec ordering.
5. Add focused tests for each stage before moving to the next change.

## Guardrails

- Keep logic incremental; avoid skipping phase boundaries.
- Preserve output contracts (`ResolvedColor`, `ColorMeta`) as defined in `src/types`.
- Keep BaseResolvedColor runtime shape stable.
- Prefer small PR-sized changes with clear acceptance criteria.
