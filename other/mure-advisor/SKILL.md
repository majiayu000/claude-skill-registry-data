---
name: "mure-advisor"
description: "Tiered per-turn advisor for main session + WhatsApp. Cheap watcher + heavy escalation. Pure annotation, two surfaces."
scope: harness
invocation: workflow
---

# mure-advisor — Per-Turn Watchdog for Main Session + WhatsApp

## Purpose

A second pair of eyes on every main-lane response. NOT a self-critique step inside the lane — a structurally independent model that reads the lane's draft + recent context + the user's input, then emits an annotation. Provides adversarial-ally coverage in conversational flow without slowing the main response.

## Tiered architecture (mandatory)

### Tier 1 — cheap watcher (always-on)

Runs every main-lane turn. Default prime: Sonnet 5. Eligible pool:
- `anthropic/claude-sonnet-5` (prime)
- `anthropic/claude-haiku-4-5` (recon + cheap research lanes; eligible as watcher when Sonnet 5 is capped)
- `ollama-cloud/deepseek-v4-flash` (when subscription active)
- `deepseek-v4-flash:direct` (via direct API; subject to daily cap — see §Budget)

**Haiku is NOT a heavy-advisor fallback.** Per owner (2026-07-09): Haiku's lane is recon + cheap research. Heavy-tier failure never falls through to Haiku; Haiku stays in the cheap / recon lanes.

Output: a per-turn note in the canonical schema (see §Note schema). The watcher LLM-judges escalation; no flag-config file maintained.

### Tier 2 — heavy advisor (escalation-only)

Only runs when the watcher escalates. Eligible pool:
- `anthropic/claude-opus-4-8` (anchor — heaviest)
- `deepseek-v4-pro:direct` (Think Max mode; subject to daily cap — see §Budget)
- `zai/glm-5.2` (Z.ai quota pool)
- `minimax-portal/MiniMax-M3` (Minimax Ultra tier; vision-capable cross-modal at 1M ctx)

**Heavy-tier fallback chain (binding):** Opus 4.8 → DeepSeek V4-Pro Think Max → GLM-5.2 → MiniMax-M3. The dispatcher advances on quota / failure. Haiku is NOT in this chain.

**Hard security rule:** on security-relevant turns, heavy MUST be Opus 4.8. Sonnet 5 is explicitly disqualified for cybersecurity per `model-audit-2026-07-09.md`. The dispatcher enforces this; the heavy variant pick for sentinel/adjudicator/architect turns is non-negotiable.

### Out of scope for now

- **Fable-5 EXCLUDED** — limited access until 2026-07-12, then PPT, then unavailable. When access returns, evaluate against the auditor's notes before re-adding.
- **GLM-5.2** gated by Z.ai weekly quota — checking on 2026-07-10 reset before relying on it for sustained load.

## Budget (binding)

### DeepSeek direct API daily cap

Per owner (2026-07-09): **max $1.0-1.5 USD per day** on DeepSeek direct API (V4-Pro Think Max + V4-Flash combined).

Dispatcher enforcement:
- Track daily spend in `_SYSTEM/state/deepseek-burn.jsonl` (one row per dispatch with $amount).
- At **80% of cap**: surface a `deepseek-cap-warning` to operator via the advisor notes channel (severity: watch).
- At **100% of cap**: refuse new DeepSeek dispatches, fall back to the next eligible model in the chain (GLM-5.2 → M3 for heavy; Haiku → M3 for watcher cheap).
- Failed dispatches emit a `deepseek-cap` event to the operator dashboard.

Default cap: $1.25/day (mid-band; operator can adjust in `_SYSTEM/state/mure-advisor.json`). The cap is operator-tunable, hard-stop is non-negotiable.

### Per-tier burn reporting

Each tier surfaces daily / weekly / monthly burn totals to the operator dashboard. Tunable thresholds warn at 80%, stop at 100%.

## Note schema (binding)

Every emitted note MUST conform. Source of truth: `_SYSTEM/research/advisor-note-schema-2026-07-09.md`.

```json
{
  "id":         "<uuid v4>",
  "turnId":     "<chat turn id>",
  "laneId":     "<dispatched lane id>",
  "model":      "<model string>",
  "tier":       "watcher|heavy",
  "severity":   "info|watch|warn|block",
  "summary":    "<one-line, <=140 chars>",
  "nextMove":   "<concrete action>",
  "confidence": 0.0-1.0,
  "evidenceRef": [{"kind":"file:line|url|trace","value":"..."}],
  "scope":      "this-turn|next-turn|both"
}
```

Notes below `injectionFloor` (default 0.5) are NOT injected into next-turn context — operator signal hygiene.

## Trigger

- **Watcher:** every turn.
- **Heavy:** watcher escalates on: logical contradiction, missed branch, protected-path risk, overconfident unverified claim, scope creep, security-sensitive content.

## Authority

**Pure annotation. Post-hoc. Never blocks delivery.** The chat model has already replied; the operator sees the note and the next turn's injection arrives one turn later. Origin: `rene-branch-patterns:29-32` (`directive-guard.mjs` is observe-only, never blocks — same posture at higher fidelity).

## Surface (dual)

1. **Visible annotation** in main chat / WhatsApp reply.
2. **One-turn-lag injection** into chat-model context for the NEXT turn via `additionalContext` (precedent: `directive-guard.mjs`).

The note's `scope` field controls: `this-turn` (visible only), `next-turn` (injected only), `both`.

## Scope (channels)

Main session + WhatsApp only by default. NOT subject to advisor annotation:
- Autonomous cron-triggered tasks
- Dedicated MURE lane dispatches (engineer / scout / etc. run with their own result-packet discipline, not advisor notes)
- Sub-sessions without the operator in the loop

Advisory for sub-session lanes is a future feature (operator-configurable).

## Arming

- Watcher lane DISARMED by default. Arm via either:
  - Session env: `YURI_ADVISOR=1`
  - Persistent flag: `touch _SYSTEM/state/mure-advisor.enabled` (gitignored)
- Heavy escalation auto-armed when watcher armed.
- Config changes (pool eligibility, schema version, injectionFloor, budget cap) — owner-gated.

## Integration with MURE

- `mure.mjs --advisor-status` → live watcher tier + last-N notes + per-tier escalation rate + deepseek-burn today.
- `mure.mjs --variants advisor` → current variant picks per tier.
- Telemetry: every emission logged to `_SYSTEM/state/advisor-ledger.jsonl` with full schema; per-line: turn id, lane, model, tier, severity, confidence, scope.
- The mure-calibrator reads the ledger for Brier scoring; outputs feed the variant matrix's MLP re-ranker (see mure-role-variant-matrix skill).

## Reinforcement / calibration

- Watcher and heavy outputs feed `mure-calibrator` continuously.
- Tracked over time:
  - Watcher escalation rate — target 5-15% of turns.
  - Heavy note acceptance rate — operator adopts the `nextMove` how often?
  - Per-model precision/recall — does the model producing the most notes correlate with rightness?
  - Confidence calibration — notes with confidence=0.9 should be right ~90% of the time.
  - DeepSeek burn vs cap.
- Outputs route to MLP re-ranker (cheap-tier selection) and to the operator dashboard for trust calibration.

## Failure modes

- **Watcher over-escalation (> 30% rate):** the cheap tier is too cautious; tune the LLM-judge prompt, lower its default escalation threshold.
- **Watcher under-escalation (< 3% rate):** the cheap tier is rubber-stamping; swap prime or downgrade from Sonnet 5 to a more skeptical model.
- **Heavy always-on by accident:** DO NOT DO. Apex-blowout. The tiering is the load-bearing architectural choice — disable via the disarm flag if a regression silently lifts the gate.
- **Tier-1 model hallucinating heavy escalation signal:** confidence < 0.6 on heavy-promote → drop the promotion. Confidence ≥ 0.85 → strong promotion.
- **Note injection polluting context:** raise `injectionFloor`; or for a single noisy model, swap it out of the watcher pool.
- **DeepSeek cap exceeded mid-day:** dispatcher auto-falls back; operator sees `deepseek-cap-warning` first, then `deepseek-cap` event.

## Anti-patterns (in code OR docs)

- Self-critique step in the main lane (no — must be a separate model).
- Heavy advisor running every turn (no — apex blowout; tiering is binding).
- Block-on-severity (no — authority is pure annotation; severity-block is declarative for the record only).
- Flag-config file maintained by hand (no — escalation is LLM-judged).
- Notes without schema compliance (no — silent failures rot the ledger).
- Falling through to Haiku for heavy-advisor failure (no — Haiku is recon only; heavy chain is Opus → DVP → GLM-5.2 → M3).
- DeepSeek spend unbounded (no — daily cap is binding).

## Related

- Source schema: `_SYSTEM/research/advisor-note-schema-2026-07-09.md` (v1.0.0).
- Recon: `_SYSTEM/research/rene-branch-patterns-2026-07-09.md` (precedent: `directive-guard.mjs`).
- Audit: `_SYSTEM/research/model-audit-2026-07-09.md` (model eligibility).
- Adversarial review: invoked against `_SYSTEM/research/adversarial-review-advisor-design-2026-07-09.md` (4-fix reconciliation).
- Fleet doctrine: skills/fleet-economy/SKILL.md (apex-reservation rule, ~35% orchestrator budget after the 20→35 update).
- Variant matrix: skills/mure-role-variant-matrix/SKILL.md (the watcher prime + heavy picks are seeds here).

## Versioned authority

v1.0.0 — created 2026-07-09. Revision incorporated: DeepSeek daily cap + M3 in Tier 2 + Haiku tier clarification. Pending Skill Workshop approval.

## Change log

- 2026-07-09 — initial draft per grill round + Opus 4.8 adversarial review (HV03).
- 2026-07-09 (rev 1) — added MiniMax-M3 to Tier 2 heavy pool; added DeepSeek direct-API daily budget cap ($1.0-1.5/day); clarified Haiku is recon/cheap (NOT heavy fallback); added heavy-tier fallback chain Opus → DVP → GLM-5.2 → M3.
