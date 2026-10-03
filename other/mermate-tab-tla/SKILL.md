---
name: mermate-tab-tla
description: Stage 4 tab (TLA+) of the Mermate pipeline — formal spec generation from a mastered run, SANY parse, TLC model check, spec edit/revalidate, and the Specula engine bridge. Use when editing TLA+ generation, verification, repair, the /api/render/tla endpoints, or specula-engine integration. Formal-method decisions defer to the specification-master-agent tree.
---

# Mermate Tab 4 · TLA+ (tla)

Operates under `mermate` master invariants. All specification-quality judgments defer to `specification-master-agent` (Minimum Acceptable Skeleton: TypeOK, Init, named actions with UNCHANGED, non-trivial invariant + inductiveness, fairness only when liveness requires).

## Stage Identity (from `STAGE_REGISTRY.tla`, public/js/mermaid-gpt-app.js)
- Label: **TLA+** · reveal: `STAGE 4 · TLA+` · color `#a78bfa`
- Expected duration: ≈1–2 min · enhance default: OFF · no upload (spec is generated)
- **IPO contract**:
  - Input: mastered run (`run_id` + diagram)
  - Process: Specula generation → SANY parse → TLC model check
  - Output: verified formal spec + config, invariants, traces

## Owning Code
- Backend: `server/routes/tla.js` —
  - `POST /api/render/tla` (generate, lines 71–637)
  - `POST /api/render/tla/edit` (edit → validate → persist, lines 787–977)
  - `POST /api/render/tla/revalidate` (SANY+TLC repair loop, lines 710–785)
  - `GET /api/render/tla/status`, `GET /api/render/tla/errors/:run_id`
- Toolchain: `vendor/tla2tools.jar` (SANY + TLC; Java 11+ required)
- Engine: `server/routes/specula.js` + pinned submodule `specula-engine/` (`GET /api/specula/health`, `POST /api/specula/validate-tlc`)
- Tests: `test/test-tla-compiler.js`

## Stage Invariants
1. **Verification before progression**: `progressionUpdate` unlocking `ts` is emitted only when SANY parses the spec; TLC results (invariant violations, error traces) ride the response — they are never swallowed.
2. Generated specs meet the Minimum Acceptable Skeleton or the stage reports `tla_failed` with structured SANY/TLC errors readable via `/api/render/tla/errors/:run_id`.
3. Edited specs re-validate before persist; an edit that breaks SANY never overwrites a verified artifact.
4. Spec generation is grounded in the mastered run's diagram — no free invention of variables or actions absent from the source architecture.

## Anti-Patterns (Reject)
- Emitting TLA+ that has not passed SANY (see `tla-syntax`; classic ASCII operators, `==`, `#`, `/\`, `\/`).
- Treating TLC timeouts as success; a timeout is reported as inconclusive.
- Hand-tuning generated invariants in client code instead of the repair loop.

## Verification
- `node --test test/test-tla-compiler.js`
- `curl -s http://localhost:3333/api/render/tla/status` — toolchain availability
- Citation grounding for spec claims: `specification-master-agent` → `references/disalg-bib-dict.md`
