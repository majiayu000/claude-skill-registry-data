---
name: evolve-migrate
description: Migrate AICP from one foundation to another — switch model backend (Hermes → Qwen3 — already done; Qwen3 → next-gen), swap inference runtime (LocalAI → vLLM, hypothetical), move storage (filesystem DLQ → real queue per `infra-queue`), upgrade Python (3.11 → 3.12). Distinct from `config-migrations` (config schema only) and `evolve-integrate` (NEW capability vs REPLACEMENT). Loads when the operator says "migrate from X to Y" / "swap LocalAI for X" / "move DLQ to Redis" / "upgrade Python".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# evolve-migrate

Migrate AICP from one foundation to another — full REPLACEMENT of an
existing system. Distinct from `evolve-integrate` (additive) and
`config-migrations` (schema-only). This skill is for substantive
foundational swaps that touch multiple AICP layers.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: "migrate from X to Y", "swap LocalAI for vLLM",
  "move DLQ to Redis", "upgrade Python to 3.12", "replace the router"
- **Replacement scope**: an existing major component is being entirely
  swapped (not extended)
- **Multi-layer touch**: the migration affects code + config + docs +
  tests + operator workflow

Do NOT load when:

- The concern is config schema only (load `config-migrations`)
- The concern is NEW capability (load `evolve-integrate`)
- The concern is API versioning of an existing surface (load `evolve-api-version`)

## Operations

### Operation 1 — Author a migration decision

**When**: contemplating a foundational swap.

**Process**:

1. Per Knowledge Evolution Standards, decision page at
   `wiki/decisions/00_inbox/migrate-<X>-to-<Y>.md`:
   - WHY: what does Y enable that X doesn't / fix that X has wrong?
   - ALTERNATIVES: at least 2 (e.g., "stay on X with workaround", "go
     to Z instead of Y")
   - REVERSIBILITY: how hard is it to roll back?
   - SCOPE: what layers (backend, config, tests, docs, operator workflow)
     are touched?
   - DEPRECATION TIMELINE: cutover date, parallel-run window
2. Operator approves before any code changes
3. Reference example: `wiki/decisions/01_drafts/qwen3-8b-as-main-reasoning-model.md`
   (Hermes → Qwen3 was an actual migration; the doc captures the rationale)

**Quality bar**: the decision page is the migration's contract.
Skipping it produces under-scoped migrations that miss layers.

### Operation 2 — Execute migration with parallel-run window

**When**: decision approved; build the new foundation alongside the old.

**Process**:

1. Build Y (new) without removing X (old). Both must work simultaneously
2. Add a feature flag (per `config-feature-flags`) to switch between
   X and Y per-invocation
3. Default to X (old) initially; let operator opt-in to Y for testing
4. Validate Y on representative workload (per `quality-performance`)
5. Once validated, flip the default to Y; deprecate X

**Quality bar**: parallel-run is the safety net. Cutover-without-parallel
breaks the world if Y has unforeseen issues.

### Operation 3 — Cutover and remove X

**When**: Y has been default for 1-2 release cycles without rollback.

**Process**:

1. Per `config-migrations` deprecation pattern, mark X as deprecated
   in code with warnings
2. Wait one more release cycle for stragglers
3. Remove X's code, config, tests, docs
4. Update CLAUDE.md to reflect Y as the only option
5. Document the cutover in CHANGELOG

**Quality bar**: NEVER remove X same-release as flipping the default.
That's a hard cutover with no escape route if Y has hidden issues.

### Operation 4 — Roll back if Y fails

**When**: Y has unrecoverable issues post-cutover.

**Process**:

1. Re-flip the default to X via the feature flag (assuming X is still
   in code per Operation 2)
2. Document the rollback in `wiki/decisions/00_inbox/<migration>-rollback.md`
   — what failed, what's needed before re-attempt
3. Restart the migration plan with the new constraints learned

**Quality bar**: rollback should be a SINGLE config flip if Operation 2
was done correctly. If rollback requires code edits, the parallel-run
window was inadequate.

## Gotchas

- **Detection**: agent migrates without parallel-run.
  **Rule**: ALWAYS build Y alongside X first; cutover via feature flag.
  **Reasoning**: hard cutover removes the rollback path; production
  issues become un-fixable mid-incident.

- **Detection**: agent removes X same-release as flipping default to Y.
  **Rule**: 1-2 release cycles between default-flip and X-removal.
  **Reasoning**: hidden Y issues surface in production over weeks; X
  needs to remain available as fallback during that window.

- **Detection**: agent skips the decision page "because the migration is obvious".
  **Rule**: every migration needs a decision page. Even obvious migrations
  benefit from the alternatives + reversibility analysis.
  **Reasoning**: future operators inheriting the migrated system need to
  know WHY; "obvious" today is opaque tomorrow.

- **Detection**: agent migrates only code, forgetting docs / tests / operator workflow.
  **Rule**: migration scope must list ALL layers (code + config + docs +
  tests + operator workflow). Address each.
  **Reasoning**: orphaned docs/tests teach operators the OLD way; they
  follow the docs and find broken behavior.

- **Detection**: agent treats `evolve-migrate` as same as `config-migrations`.
  **Rule**: `config-migrations` is schema only; `evolve-migrate` is the
  broader replacement (code + config + tests + docs).
  **Reasoning**: scoping correctly avoids mid-migration scope creep.

## Reference exemplars

- `wiki/decisions/01_drafts/qwen3-8b-as-main-reasoning-model.md` — actual
  migration decision (Hermes → Qwen3); shows the full alternatives +
  rationale + reversibility analysis
- `wiki/decisions/01_drafts/localai-over-ollama-vllm-for-multi-model-orchestration.md` —
  decision NOT to migrate (chose LocalAI over alternatives); shows
  reverse-direction analysis
- `aicp/backends/` — backend layer where most migrations land
- `config/profiles/` — where feature-flag overlays for parallel-run live
- `wiki/decisions/00_inbox/aicp-mcp-tool-surface-audit-2026-04-19.md` —
  example of a multi-cycle migration plan (deprecate → wait → remove)

## Domain context

AICP has migrated foundations before: Hermes-7B → Qwen3-8B (model
backend) is the canonical example. The pattern there: alternatives
considered, reversibility documented, profile-overridable so per-profile
operators could test. Future migrations (e.g., LocalAI → vLLM if ever
needed) should follow the same pattern. AICP's profile system is the
parallel-run vehicle.

## Related skills

| Skill | When to use |
|-------|-------------|
| `evolve-integrate` | When ADDING a new system (not replacing) |
| `evolve-api-version` | When the migration is API surface only |
| `config-migrations` | When the migration is config schema only |
| `architecture-propose` | When the migration requires major architectural design first |
| `pm-changelog` | When documenting the migration in release notes |
| `ops-rollback` | When executing the rollback in production |
