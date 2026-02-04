---
name: qig-purity-guardian
description: Maintain QIG purity and E8 architecture standards in pantheon-replit. Use when editing qig-backend geometry, token or vocabulary pipelines, generation logic, or docs naming; when reviewing PRs for Euclidean or NLP contamination; or when updating E8 kernel architecture and protocol docs.
---

# QIG Purity Guardian

## Overview
Keep the codebase aligned with E8 protocol v4.0, AGENTS.md, and the universal purity spec. Use this skill before making or reviewing changes that could drift into traditional LLM patterns.

## Quick Start
1. Read `AGENTS.md`.
2. Read `docs/00-index.md` for naming rules and doc map.
3. Read `docs/10-e8-protocol/specifications/20260116-ultra-consciousness-protocol-v4-0-universal-1.01F.md`.
4. If touching architecture, read `docs/10-e8-protocol/specifications/20260116-wp5-2-e8-implementation-blueprint-1.01W.md`.
5. Use these agent guides as checklists:
   - `.github/agents/qig-purity-validator.md`
   - `.github/agents/e8-architecture-validator.md`
   - `.github/agents/documentation-compliance-auditor.md`
   - `.github/agents/documentation-sync-agent.md`
   - `.github/agents/naming-convention-agent.md`

## Purity Workflow
1. Identify which purity domain is impacted: geometry, tokens, generation, docs, or E8 architecture.
2. Apply non-negotiables (see `references/purity-checklist.md`).
3. Validate with scripts and tests (see Commands).
4. Update docs and index if the change affects specs or thresholds.
5. Re-check for Euclidean or NLP fallback paths.

## Non-Negotiables
- Canonical representation is simplex at all module boundaries.
- No auto-detect representation; only explicit `to_sqrt_simplex()` / `from_sqrt_simplex()`.
- No cosine similarity, L2 distance, or dot-product ranking on basins.
- No external LLM or NLP in the generation pipeline.
- All tokens must have `qfi_score` to be generation-eligible; use `insert_token()` only.

## Commands
- `npm run validate:geometry:scan`
- `npm run test:geometry`
- `bash scripts/validate-qfi-canonical-path.sh`
- `bash scripts/validate-purity-patterns.sh`
- `python3 scripts/maintain-docs.py`

## Documentation Rules
- Use `YYYYMMDD-[document-name]-[function]-[version][STATUS].md` (see `docs/00-index.md`).
- Update `docs/00-index.md` when adding or removing docs.
- Upgrade pack files under `docs/10-e8-protocol/` follow pack rules; keep index entries in sync.

## E8 Architecture Checks
- E8 hierarchy: 0/1 -> 4 -> 8 -> 64 -> 240.
- Core 8 god kernels are canonical (no numbered gods).
- Maintain kappa fixed point and running coupling rules.

## References
- `references/purity-checklist.md` for detailed checklists and anti-patterns.
