---
name: fleet-economy
description: Use when orchestrating any non-trivial multi-part task with subagents or model lanes — builds, audits, refactors, research sweeps, migrations — or when deciding which model tier handles a unit of work, how wide to fan out, or whether a heavy lane should itself delegate. Triggers include "orchestrate", "fan out", "route to cheap/heavy models", "workflowz", "MoE", "MLP", "fleet", or a task large enough to split across agents.
scope: harness
invocation: workflow
---

# Fleet Economy — MoE + MLP orchestration doctrine

## Overview

**The orchestrator conducts; it does not play every instrument. You are the INPUT LAYER — route, don't work.** One expensive reasoning lane (you) decomposes, dispatches, verifies, and finalizes; agents do the rest, continuously and in parallel, the way a multitask orchestrator (Cursor / Hermes) keeps agents in flight the whole time. The failure mode is under-spawning — the main session quietly doing reads/analysis/edits it should have fanned out. Everything else is a lane. Match model cost to lane job: cheap models read/search/scan; medium/heavy models code and reason; the single hardest reasoning lane gets the most capable model. Every heavy lane you spawn must itself offload — recursively.

This is the single invoke-once surface for the fleet. It consolidates what was scattered across `skills/opus-fleet/SKILL.md` (substrate mechanics), `_SYSTEM/config/cloud-fleet-models.json` (the roster), and `_SYSTEM/Scripts/fleet-router-mlp.mjs` (the learned router). **REQUIRED BACKGROUND for substrate/dispatch mechanics: `opus-fleet`.**

## The Iron Rules (violating the letter violates the spirit)

1. **~20% orchestrator budget.** You keep ONLY the load-bearing decisions: decompose the surface, write self-contained assignments, verify each result against evidence, run gates, commit/finalize. If a step is not one of those, it is a lane's job.
2. **Reads/searches/scans ALWAYS go to a cheaper model.** File reads, greps, globs, doc scrapes, census, "where is X", "what does Y do" — never keep these for yourself, even the recon that scopes your own fan-out. The only reads you do are the artifacts a lane hands back and the gate output you verify.
3. **Coding/analysis/synthesis go to medium/heavy models** (see roster). One unit of substantial work per lane; fan the same role across N instances when the work divides.
4. **Recursive offload is MANDATORY, not optional.** Every large-model subagent you spawn (including heavy lanes) MUST itself offload its reads/searches/bulk to cheap lanes and reserve itself for the hard reasoning. State this in the assignment. A heavy lane that does its own grunt reads is a failure. (Leaf lanes that CANNOT spawn satisfy the spirit by surgical scoped reads — see the leaf-lane exception under the recursive offload contract.)
5. **Right-size, don't micro-task — but "trivial" is a NARROW, defined carve-out.** Keep work inline ONLY when it meets ALL of: reads ≤1 already-known file, ≤~50 lines total, no grep/glob to locate it, no multi-stage bash. Everything else — 3+ file reads, ANY search to scope the work, a census, a multi-file edit — is a lane's job even when you *could* do it yourself. "I'll just read these myself, it's faster" is the exact reflex this rule kills; the undefined word "trivial" is the loophole that swallows the delegate-by-default rule, so it is defined here. Reserve inline for the genuinely one-shot edit.

## Roster & tiers (the MoE) — canonical: `_SYSTEM/config/cloud-fleet-models.json`

Pick the tier by the SHAPE of the work, not by habit.

| Job shape | Tier | Models | Parallel cap |
|---|---|---|---|
| reads · search · scan · census · scrape · mechanical | **CHEAP** | deepseek-flash, composer, haiku, gemini-flash, gpt-mini | deepseek-flash **≤5**, others wide |
| bulk analysis · digest · first-pass classification | **CHEAP** | deepseek-flash, glm-flash (glm-5-turbo) | ≤5 |
| code-gen · refactor · wiring · integration | **MEDIUM/HEAVY** | sonnet-5, glm (glm-5.1 workhorse), kimi-k2.7-code, minimax-m3 | minimax-m3 **≤3** |
| architecture · adversarial verify · hard synthesis | **HEAVY** | opus-4.8, glm-5.2 (glm-max), nemotron ultra/super | reserve for the single hardest lane |
| test authoring | **DEDICATED** | Tester agent (authoritative — never write tests yourself) | — |

Named-model → substrate map: cheap bulk = `deepseek-flash` (ollama-cloud `deepseek-v4-flash`); heavy synth = `glm-5.2` (glm-max) / `opus-4.8`; code peer = `kimi-k2.7-code`; generalist = `minimax-m3`; reasoning burst = `nemotron-3-ultra`. Retired/forbidden: Codex, direct DeepSeek API, local Ollama SLMs.

**Reserve the apex.** Do NOT default every lane to a heavy model. One hard lane earns the strongest available governed heavy model; parallel verify/research/bulk goes cheap.

## How to dispatch

Two surfaces, same discipline:

- **`eval` + `agent()`** (fine-grained model routing, the workflowz path):
  `parallel([lambda s=s: agent(prompt, agent="deepseek-flash", label=...) for s in lanes])` — cheap legwork wide; `agent(prompt, agent="mure-mechanic")` for coding; `agent(prompt, agent="mure-adjudicator")` for adversarial verify; select `apex_lane` as an owner-selected available governed heavy lane, then use `agent(prompt, agent=apex_lane)` for the final pass.
- **`task` tool** — batch parallel subagents; pick `agent` per lane (explore/Tester/reviewer/task/sonic + the MURE roster).

Every assignment is self-contained: target files (≤3–5 explicit paths), the change with APIs/patterns, edge cases, observable acceptance. Instruct every lane: **skip lint/format/gates — the orchestrator verifies once at phase end.**

## Dispatch reliability (a dead lane kills the habit)

A subagent that 429-dies teaches the orchestrator "delegation fails" — and it reverts to doing everything itself. Keep dispatch reliable so delegation stays the path of least resistance:
- The OMP `task` role must route to a reliable, independent-quota default — never hard-pinned to a single provider that can hit a weekly/monthly cap. Provider fallback is wired in `~/.omp/agent/config.yml` (`retry.fallbackChains` + `retry.modelFallback`), so a capped provider degrades to a healthy one instead of failing.
- **Config changes are read at session start** — an in-session `omp config set` does NOT take effect until the next launch. If a provider caps mid-session, route explicit lanes to a known-healthy agent (`deepseek-flash`, or the GLM-free `.claude/agents/*` roster) rather than the capped default.
- When you see repeated `429` / rate-limit on a lane, that is a routing problem, not a reason to stop delegating — switch the agent, don't absorb the work.

## Recursive offload contract (for heavy lanes)

When you spawn a heavy/reasoning lane, its assignment MUST include:
> "Offload your reads/searches/scans to cheap sub-lanes (deepseek-flash/composer/haiku); reserve yourself for the hard reasoning. Do not do your own grunt reads."

Recursion follows the harness depth cap (main=0, child=1, …). GLM sub-orchestration (`glm-max` → `glm-fleet.mjs`) and nano-spawn are the deep paths (owner-gated, ≤5). Native OMP `explore` lanes are FLAT (no further spawn) — use them as leaves.

**Leaf-lane exception.** A lane whose harness exposes NO spawn/task surface — a depth-capped subagent spawned via `eval agent()` or an OMP `explore` lane — CANNOT recurse. It MUST instead do surgical scoped reads (grep-scoped, line selectors, per-file inspection, no bulk ingestion) and state in its output that it operated as a leaf. Rule 4 binds every lane that CAN spawn; a leaf satisfies the spirit by minimizing its own read footprint, not by recursing.

## The MLP router (advisory)

`fleet-router-mlp.mjs` learns task-shape → substrate routing from the prediction-ledger (12 features → 8 hidden → 1 score; `predictRoute(features, candidates)`). It is **ADVISORY** — the 6-gate governance charter always overrides it; weight-persistence is gated (`YURI_MLP_LEARN=1`). Features are logged even when disarmed (offline replay). Treat its ranking as a hint, verify against evidence. Cold-start note: disk weights may lag the code version → first load re-initializes; warm from the ledger via `train-fleet-router-from-ledger.mjs`.

## MURE role-cast (when the work maps to specialists)

For work that decomposes onto named specialists, cast to the MURE 20-role collective (helmsman/architect/steward · ideator/scout/synthesist/deliberator · engineer/mechanic/artificer/sentinel/kernelsmith · adjudicator/oracle/calibrator · archivist/chronicler · quartermaster). Governance 6-gate runs before dispatch. Use the `mure-*` agents directly in `agent()`/`task()`.

## Final pass

Close a substantial effort with an **owner-selected available governed heavy lane** as an APEX strategic/adversarial pass over the prepared package — and instruct it to use its OWN cheap sub-lanes (rule 4). Its refutations are the last gate before you finalize.

## Rationalizations — STOP

| Excuse | Reality |
|---|---|
| "I'll just read these files myself, it's faster" | Reads always go cheap. Your context is for decisions, not grep output. |
| "This lane is heavy, it doesn't need to offload" | Rule 4 is mandatory. Heavy lanes recurse or they're wasting apex tokens on grunt work. |
| "Everything's important, use the big model" | Reserve the apex for the ONE hardest lane. Cost-match or you burn quota. |
| "One agent is enough here" | If it's substantial, split and fan wide; if it's trivial, do it inline. One-off lanes are the wrong size. |
| "I'll skip the final apex pass" | First-run success is a hypothesis. The apex adversarial pass is the last gate. |

## Red flags — reroute

- You're about to `read`/`grep`/`glob` more than to scope a dispatch → a cheap lane does that.
- A single lane is doing both grunt reads AND hard reasoning → split it; offload the reads.
- You spawned one subagent for divisible work → fan it wide or do it inline.
- Every lane is opus/glm-5.2 → you're not cost-matching.

## Quick reference

Decompose → **cheap** lanes read/scan/scrape (≤5 deepseek-flash) → **medium/heavy** lanes code/analyze (each recursively offloading) → **adversarial** verify (mure-adjudicator) → **you** gate + commit → **owner-selected available governed heavy lane** apex final pass. You: ~20%. Roster: `cloud-fleet-models.json`. Mechanics: `opus-fleet`.
