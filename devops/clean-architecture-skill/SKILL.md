---
name: clean-architecture-skill
description: Apply clean architecture principles with vertical slicing, dependency rule, clear layer boundaries, and feature-first organization - language-agnostic
license: Apache-2.0
compatibility: opencode
category: Code Quality
---

## What I do

Structure codebases by vertical feature slices + horizontal layers (domain ← application ← infrastructure ← presentation), enforce the dependency rule (source dependencies point inward only), define contracts at boundaries.

## When to use me

- Structuring a new codebase or module; deciding where a piece of code belongs
- Reviewing whether a boundary is real (enforced) or decorative

Canonical house layouts: frontend `features/<feature>/{_components,_containers,hooks}` + `domains/<feature>`; backend `modules/<module>/{domain,application,infrastructure,presentation}` (domain holds interfaces, infrastructure holds implementations).

## House Learnings

### Learning: `doc-claimed-purity-vs-reality`
A layer rule documented but violated by >10 call sites is a false contract — leaving doc and code in disagreement trains every developer to ignore both. Either enforce the boundary with tooling (`no-restricted-imports` per-directory overrides, `madge --circular`, dependency-cruiser in CI) or rewrite the doc to describe reality. Never let architecture docs and code drift — the drift becomes the de facto standard.
Detection: `rg "from '@prisma/client'|from 'pg'" src/domain/ -l | wc -l` · `npx madge --circular --extensions ts src/domain/`

### Learning: `cross-container-hook-borrowing`
A feature container must NEVER import from a sibling container via relative path (`../../_containers/ReportDetail/useReportDetail`) — invisible coupling that breaks silently on refactor. If two containers need one hook, extract to the feature's `hooks/` (intra-feature) or `domains/{feature}/hooks/` (cross-feature). Containers import ONLY from `@/`-aliased shared locations or their own feature's `hooks/`.
Detection: `rg "from\s+['\"](\.\./)+.*_containers" --type ts --type tsx`

> Removed 2026-09: layered/hexagonal/clean-architecture comparison essays, dependency-rule diagrams, vertical/horizontal boundary walkthroughs, cross-cutting-concern lists, frontend/backend directory deep-dives, steps/common-issues ceremony — textbook architecture knowledge; the two codified learnings are this config's real additions.
