---
name: opus-fleet
description: "Standing operating model — Opus (and its glm-5.2 Opus-equivalent) orchestrates while spawned workers do the work across three substrates: native Sonnet/Haiku Agents, z.ai GLM lanes (glm-fleet.mjs), AND ollama-cloud peer lanes (ollama-fleet.mjs), ALWAYS at max reasoning / --reasoning high, then the orchestrator reviews, corrects, and finalizes. Ships copy-paste dispatch templates, the GLM tier roster, dual-substrate routing, the governed autonomous loop, and Agent-not-Workflow discipline. Use to start or run this model on any non-trivial build, research, multi-file edit, audit, refactor, or fan-out task."
version: 1.1.0
status: active
triggers:
  - /opus-fleet
  - opus orchestrates
  - spawn agents
  - fan out agents
  - three lane execution
  - research code testing lanes
  - max reasoning agents
  - agent fleet
  - glm fleet
  - zai fleet
  - dual substrate
  - glm-fleet
scope: harness
invocation: workflow
---

# opus-fleet — Opus orchestrates, Sonnet/Haiku agents execute

The default way to run any non-trivial task. The main **Opus** session never grinds parallelizable work itself — it **orchestrates**: decompose → dispatch a fleet of **Sonnet + Haiku Agents** (always max reasoning) across three lanes → **review and correct every result** → finalize. Greater quality, and cheaper — Sonnet bills a separate weekly pool, so the fan-out barely touches the Opus quota.

Canonical rule: [`.claude/memory/feedback-opus-orchestrates-sonnet-haiku-agents.md`](../../.claude/memory/feedback-opus-orchestrates-sonnet-haiku-agents.md). This skill is the **quick-start + discipline** for it.

## When this fires

Every substantial task — build, research, multi-file edit, audit, verification, refactor. Skip only trivial single reads and pure conversation.

**Fleet sizing — don't under-spawn.** Native Agents are FLAT (they can't spawn sub-agents — `Explore` has no Agent tool, and the model keeps them leaf-only). So trade depth for BREADTH: fanning out **up to ~12 parallel native Agents in one message is encouraged** when the work divides that way (Sonnet bills a separate weekly pool — breadth is cheap). Recursion depth is the GLM / `nano-spawn` substrate's job, capped at **depth 5** (heavy tier) with decaying per-level fan-out. Self-size to the task — but the failure mode here is timidity, not excess.

## The model at a glance

```
                 ┌───────────────────────────┐
                 │   OPUS  (this session)     │
                 │  decompose · judge · plan  │
                 │  synthesize · review · ship│
                 └───────────────────────────┘
                  ↑            ↑            ↑
        ┌─────────┘            │            └─────────┐
  ┌───────────┐         ┌─────────────┐         ┌───────────┐
  │ RESEARCH  │         │  CODE-GEN   │         │  TESTING  │
  │ scan code │         │ new files,  │         │ scripts,  │
  │ docs, APIs│         │ patches,    │         │ browser,  │
  │           │         │ refactors   │         │ logs      │
  └───────────┘         └─────────────┘         └───────────┘
        Sonnet + Haiku Agents — ALWAYS at MAX reasoning
```

## Quick start — copy-paste dispatch

Run independent lanes **in parallel** (multiple `Agent` calls in one message). Every prompt is self-contained and ends with the max-reasoning directive.

```
Agent(
  description: "<3-5 word label>",
  subagent_type: "Explore"   // read-only research; or "general-purpose" for edits/bash
  model: "sonnet",           // sonnet = judgment/code-gen; haiku = read/scan/mechanical
  prompt: `Use MAXIMUM reasoning depth — be exhaustive and rigorous.
           <ROLE>: <Research | Code-generation | Testing> lane for an Opus-orchestrated task in <repo>.
           CONTEXT (self-contained — you lack the conversation): <what changed / state>.
           TASK: <exact, bounded>.
           DO NOT: touch protected paths; commit; rewrite dated history.
           RETURN: <exact format — table / verdict / diff>.`
)
```

## Model routing

| Lane | Default model | Use when |
|------|---------------|----------|
| Research (classify, judge, prior-art) | **sonnet** | needs judgment over what it finds |
| Research (census, grep-survey, read-dump) | **haiku** | mechanical breadth, go heavy |
| Code-generation (patches, new files, refactors) | **sonnet** | correctness matters |
| Testing (run scripts, parse logs, verify) | **haiku** | mechanical execution + report |

`Explore` = read-only (can't edit) — safest for research. `general-purpose` = full tools — for edits/bash. Never spawn an Agent to read one known file (do it inline).

## The orchestrator loop (Opus keeps these)

1. **Decompose** into independent lanes; identify what genuinely parallelizes.
2. **Dispatch** parallel Agents (one message, multiple calls), each self-contained, each at max reasoning.
3. **Review + correct** — first-run agent output is a hypothesis. Verify every load-bearing claim against local evidence; override what's wrong.
4. **Finalize** — Opus only: scoped-pathspec commit, push, irreversible/outward calls, protected-path discipline. Agents never finalize.

## Hard rules (failure-anchored)

- **Agent, never Workflow.** Workflow `agent()` bills the main/Opus quota; the `Agent` tool with `model:"sonnet"` bills the separate Sonnet pool. <!-- @anchor: v1 | failure: FB:WORKFLOW-BILLS-MAIN-QUOTA-NOT-SONNET | regression: .claude/memory/feedback-no-workflow-tool-use-agent-only.md -->
- **Always max reasoning.** The Agent tool has no effort param, so keep the orchestrator at max effort (agents inherit) AND pin `Use MAXIMUM reasoning depth` as the first line of every agent prompt. <!-- @anchor: v1 | failure: FB:OPUS-ORCHESTRATES-SONNET-HAIKU-AGENTS | regression: .claude/memory/feedback-opus-orchestrates-sonnet-haiku-agents.md -->
- **Verify every agent result.** A Haiku testing lane (2026-06-22) couldn't run its check, *guessed from reading code*, and reported the guard would BLOCK existing `.claude` files — direct evidence showed WARN. Override agent guesses with local runs. <!-- @anchor: v1 | failure: opus-fleet-haiku-warn-block-misguess-2026-06-22 | regression: SKILL.md self-test (verify agent claim before trusting) -->
- **Agents earn their keep.** Same session, a Sonnet research lane found a real ENOENT (`yuri-supercharge-gate.mjs` pointing at a deleted test) that the solo pass missed — the fan-out is not theater. <!-- @anchor: v1 | failure: none | regression: none -->
- **Self-contained prompts.** Agents lack the conversation; an underspecified prompt returns confident garbage. Always include state + constraints + return format.
- **GLM lanes: never `tee`/`>`, always `--out`.** A second reader on the z.ai/Anthropic stream triggers transport:EPIPE (fixed root cause — don't reintroduce). `glm-fleet.mjs` collects each lane's text from its own `--out` file. <!-- @anchor: v1 | failure: FB:GLM-ZAI-BUILD-LANE | regression: .claude/memory/feedback-glm-zai-build-lane.md -->
- **GLM agents run at `--reasoning high`.** That is the GLM max-equivalent — there is no higher tier. Pin it on every GLM task (the native-Agent "max reasoning" analogue). <!-- @anchor: none -->
- **The GLM fleet is DISARMED by default.** `glm-fleet.mjs` dry-runs (zero spend, zero fan-out) without `YURI_GLM_FLEET=1`; arming it — and `YURI_SWARM_CONVERGENCE` / `YURI_NANOSWARM_SPAWN` — is owner-gated (durable z.ai spend + process fan-out are not git-reversible). <!-- @anchor: v1 | failure: FB:ARMING-IMPROVEMENTS-SELF-GOVERNABLE | regression: .claude/memory/feedback-arming-improvements-self-governable.md -->
- **Verify GLM output locally — lanes over-claim.** A peer lane reporting "done" is a hypothesis (precedent: 18/19 false "done", a raw arithmetic hallucination). Re-check against local evidence before trusting, exactly as with native agents. <!-- @anchor: v1 | failure: FB:NANO-SWARM-ORCHESTRATION | regression: .claude/memory/feedback-nano-swarm-orchestration.md -->

## Anti-rationalization table

| Excuse | Reality |
|--------|---------|
| "This is small, I'll just do it solo." | Then it's trivial → fine. But "multi-file / multi-step / needs a survey" is exactly the fan-out case; solo is slower and misses things (the ENOENT above). |
| "Workflow is right here and easier." | Workflow drains the Opus quota and is banned here. `Agent(model:"sonnet")` is the only fan-out path. |
| "The agent said it passed, ship it." | Agent output is a hypothesis. The Haiku lane *guessed wrong* this session. Verify against a local run before trusting. |
| "Max reasoning costs too much." | Sonnet bills a separate weekly pool. The cost concern is inverted — fan out liberally. |
| "I'll skip the context, the agent will figure it out." | It can't — it has no conversation history. Underspecified → confident garbage. Self-contained prompt every time. |
| "GLM is the read-only / advisory lane." | Wrong — GLM lanes carry the full harness (write / edit / bash) and build exactly like native Agents; `glm-5.2` is an Opus-peer. Route by quota / context / recursion / native-tool-need, never by a capability tier that doesn't exist. |
| "I'll pipe the GLM call through `tee` to watch it." | That triggers transport:EPIPE. Use `--out` and read the file. Never a second stream reader on the lane. |
| "Arm the autonomous loop so it just runs unattended." | Arming spends durable budget + fans out processes — owner-gated, always. Build + smoke DISARMED; the owner flips the flag. |

## Optional — loop until done

For unknown-size discovery, wrap rounds with the convergence governor `_SYSTEM/Scripts/swarm-convergence.mjs` (obligation floor + critical-signal block + adversarial "what's missing" pass + damping). DISARMED by default (`YURI_SWARM_CONVERGENCE=1`). Use when one fan-out round isn't provably complete.

## z.ai GLM fleet — the second substrate

The native Claude fleet has a full **twin**, not a sidekick: a **z.ai GLM lane fleet** dispatched through `_SYSTEM/Scripts/glm-fleet.mjs`. Every GLM lane runs the complete YURI operator harness via `llm-lane.mjs` — `read`/`grep`/`search`/`xref` **and** `write_file`/`edit_file`/`bash` — so it **develops, designs, codes, writes files, and runs/self-verifies** exactly like a native Agent. It is a peer build substrate — never read-only or advisory. `glm-max` (glm-5.2, 1M context) is an **Opus-peer**: on par or better at reasoning, coding, and visual design. It bills the z.ai plan (independent of the Anthropic quota), runs at **`--reasoning high`** (the GLM max-equivalent), and the same three lanes mirror onto it — Research, Code-generation, Testing — all doing real work.

The fullest mirror is **`ai claude-zai`**: a complete Claude Code session running on GLM (`OPUS→glm-5.2`, `SONNET→glm-4.7`, `HAIKU→glm-flash`) — the exact same setup as this one, on z.ai. Reach for it for a full interactive GLM build session; use `glm-fleet.mjs` to fan GLM peers out in parallel from here.

DISARMED by default → **dry-run** (prints the plan, spends nothing). Arm (owner-gated) via EITHER the session env `YURI_GLM_FLEET=1` OR a persistent local flag `touch _SYSTEM/state/glm-fleet.enabled` (gitignored, reversible by `rm`). `glm-fleet.mjs --list` shows the current arm state.

GLM tier roster (mirrors Opus/Sonnet/Haiku):

| Tier | alias | model | ctx | use |
|------|-------|-------|-----|-----|
| Opus-peer · orchestrator | `glm-max` | glm-5.2 | 1M | heavy reasoning, design, architecture, code, synthesis (premium) |
| Sonnet · workhorse | `glm` | glm-4.7 | 200K | code-gen, refactor, analysis, judgment |
| Haiku · fast build | `glm-flash` | glm-4.7-flash | 200K | census, scan, fast edits, test-runs (free) |
| Haiku+ · concurrency | `glm-flashx` | glm-4.7-flashx | 200K | wide cheap fan-out (paid) |
| Sub-orch overflow | `glm-sub-orch` | glm-5.1 | 200K | when glm-max is quota-gated |
| Reactive · voice | `glm-turbo` | glm-5-turbo | 200K | sub-4s interactive |
| Vision | `glm-vision` | glm-4.6v | 64K | screenshots, images (live-verified) |
| OCR | `glm-ocr` | glm-ocr | 32K | document / PDF extraction (needs image payload) |

Live-probe 2026-06-22: `glm-max`, `glm`, `glm-flash`, `glm-turbo`, `glm-5.1`, `glm-vision` verified live. `glm-flashx` (id accepted but empty output — likely not provisioned) and `glm-ocr` (needs an image payload) are UNVERIFIED via the text path — registered, not yet relied on.

Dispatch programmatically:

```js
import { glmFleet } from './glm-fleet.mjs'; // path relative to the importing file; the shell form below is location-independent
const { results, runDir } = await glmFleet([
  { lane: 'glm-max',   label: 'DESIGN',  prompt: `Use MAXIMUM reasoning depth. ROLE: design + architecture lane ... RETURN: design doc + RESULT_LABEL` },
  { lane: 'glm',       label: 'CODEGEN', prompt: `Use MAXIMUM reasoning depth. ROLE: code-generation lane — write/edit the files directly and self-verify by running them ... RETURN: diff summary + RESULT_LABEL` },
  { lane: 'glm-flash', label: 'TEST',    prompt: `Use MAXIMUM reasoning depth. ROLE: testing lane — run the suite, parse logs, report ... RETURN: results + RESULT_LABEL` },
], { concurrency: 3 });   // needs YURI_GLM_FLEET=1, else dry-run
```

Or from the shell (collect via `--out` — NEVER `tee`/`>`):

```bash
YURI_GLM_FLEET=1 node _SYSTEM/Scripts/glm-fleet.mjs --tasks '[{"lane":"glm-max","label":"ORCH","prompt":"..."}]' --concurrency 3
# results land in .claude/jobs/<run>/results/<label>.json   ·   dry-run plan: drop YURI_GLM_FLEET or add --dry-run
```

## ollama-cloud fleet — the third substrate

The third peer fleet: **ollama-cloud lanes** dispatched through `_SYSTEM/Scripts/ollama-fleet.mjs` — cross-family models (not Claude, not GLM) carrying the full YURI operator harness via `llm-lane.mjs`, so they build, code, write, and self-verify like any other lane. ONE base `ollama-cloud` lane fans out across the roster by `--model <X>:cloud`; the ollama Pro plan allows **3 concurrent**. It bills the ollama plan (independent of both the Anthropic and z.ai quotas) and is the **cheapest bulk fan-out** — reach for it to spread wide, cheap, parallel work.

Roster (tier → model), all at `--reasoning high`:
- `flash` → `deepseek-v4-flash:cloud` — **default bulk**, best quality-per-usage, blast freely
- `minimax` → `minimax-m3:cloud` · `kimi` → `kimi-k2.7-code:cloud` — the efficient working trio
- `nemotron` → `nemotron-3-ultra:cloud` (heavy reasoning) · `deepseek-pro` → `deepseek-v4-pro:cloud` (true-1M input; ~2× usage — avoid for bulk) · `gemma` → `gemma4:31b-cloud`

DISARMED by default → **dry-run** (prints the plan, spends nothing). Arm (owner-gated) via EITHER `YURI_OLLAMA_FLEET=1` OR `touch _SYSTEM/state/ollama-fleet.enabled` (gitignored, reversible by `rm`). `ollama-fleet.mjs --list` shows the arm state + roster.

```bash
# 3-model peer fan-out (needs YURI_OLLAMA_FLEET=1, else dry-run)
YURI_OLLAMA_FLEET=1 node _SYSTEM/Scripts/ollama-fleet.mjs --tasks '[{"tier":"flash","label":"R1","prompt":"..."},{"tier":"kimi","label":"R2","prompt":"..."}]' --concurrency 3
# results → .claude/jobs/<run>/results/<label>.json   ·   live smoke: --smoke   ·   dry-run: drop the env / add --dry-run
```

The key hydrates from the macOS keychain at the LANE layer (`models.json` `keychain_service: YURI_OS_MUSUBI:OLLAMA_API_KEY`), so a spawned lane authenticates without the `ai` wrapper or an exported `OLLAMA_API_KEY` (root-cause fix 2026-06-23 — every caller benefits, not just the wrapper).

## Multi-substrate routing — three equal build fleets

NOT a capability tier. All three fleets have the SAME powers — read, write, edit, bash, design, code, test, self-verify. GLM and ollama-cloud are peer extensions of Claude Code, never advisory or read-only. Route by operational fit, then spread work across ALL THREE for max throughput on independent quotas:

| factor | native Claude Agents | z.ai GLM lanes | ollama-cloud lanes |
|---|---|---|---|
| build powers | read · write · edit · bash · test | identical | identical |
| quota pool | Claude / Sonnet weekly | z.ai plan | ollama Pro (independent — run all three at once) |
| recursion | FLAT (leaf-only) | recursive via `nano-spawn`, depth ≤ 5 | FLAT (peer fan-out, 3 concurrent) |
| max context | per-model | `glm-5.2` = 1M | 1M input (deepseek-v4 family) |
| reasoning / coding tier | Opus / Sonnet / Haiku | `glm-5.2` / `glm-4.7` / `glm-flash` | nemotron / minimax / kimi / deepseek-v4 |
| native MCP / browser / computer-use | yes | no | no |
| finalize (commit / push) | no — orchestrator only | no — orchestrator only | no — orchestrator only |

The only hard native-only needs are MCP tools, browser, and computer-use. Everything else either fleet does equally. Default to spreading a large build across all three on their independent quotas, in parallel: native (Anthropic), GLM (z.ai), ollama-cloud (ollama Pro) — three quota pools = up to ~3× throughput. `glm-max` is a first-class orchestrator/red-teamer; the ollama lane is the cheap bulk muscle (`deepseek-v4-flash` for breadth, `deepseek-v4-pro` reserved for true-1M / hardest jobs).

## Spawning a sub-orchestrator (Opus-equivalent fan-out)

A spawned orchestrator — a native `general-purpose` Agent OR a `glm-max` lane — can run this fleet model itself if handed the protocol. Inject `FLEET_PROTOCOL_PREAMBLE` (exported from `glm-fleet.mjs`) as the first block of its prompt; glm-5.2's 1M context also lets you paste this whole SKILL.md verbatim. That is how "the Opus and Opus-equivalent spawns sub-dispatch with this knowledge."

Honest caveat: native Claude subagents are **flat** — `Explore` has no Agent tool and the standing model keeps the native fleet leaf-only (Opus is the sole native spawner). Compensate with breadth (up to ~12 parallel; see Fleet sizing). Real recursion lives on the GLM substrate via the governed `nano-spawn` path (`YURI_NANOSWARM_SPAWN=1`, owner-gated) at **depth ≤ 5**. Until that is armed, "sub-orchestration" means a `glm-max` lane calling `glm-fleet.mjs` for its own peer round.

## The governed autonomous loop

One owner input → a fully governed fleet:

1. **Decompose** — Opus splits into leaves, each tagged substrate `native` | `glm` | `both`; build the obligation ledger (`swarm-convergence.buildObligationLedger`).
2. **Dispatch** — native Agents (one message, parallel) + `glmFleet(...)` in parallel; each self-contained, max reasoning / `--reasoning high`.
3. **Aggregate** — read native returns + `.claude/jobs/<run>/results/*.json` into one pool.
4. **Adversarial verify** — `swarm-convergence.runAdversarialPass` with a `glm-max` runner ("what's missing"); Opus re-verifies load-bearing claims against local evidence.
5. **Converge** — `converge(...)`; not converged → re-dispatch `nextRoundWork`, capped ≤ 3 rounds (damping force-stops on budget).
6. **Finalize** — Opus only: scoped-pathspec commit, push, irreversible/outward calls.

Arm the quality gate with `YURI_SWARM_CONVERGENCE=1`; the `nano-barrier` safety block (orphans/contested claims) is always on regardless. Both the convergence arm and the GLM-fleet arm are owner-gated.

**Runnable now — `_SYSTEM/Scripts/runSwarm.mjs`** (the audit's missing "orchestrator binary"). The GLM-substrate version of this loop is wired into one entry point: `runSwarm({leaves:[{id,lane,prompt}]}, {rounds,concurrency})` runs decompose-ledger → `glmFleet` dispatch → `aggregatePoolOutputs` → `runAdversarialPass` (glm-max) → `converge` → re-dispatch only the gap leaves (obligation-floor failures **and** adversarial gaps; null-leaf gaps re-run all; ≤rounds) → `finalizeGuard` → manifest. CLI: `node _SYSTEM/Scripts/runSwarm.mjs --leaves-file leaves.json --rounds 3`. **ARMED** via the gitignored flags `_SYSTEM/state/swarm-convergence.enabled` + `_SYSTEM/state/glm-fleet.enabled` (env vars still work). Live-verified end-to-end (a 2-leaf armed run converged round 1; hermetic tests cover gap re-dispatch, floor-failure re-dispatch, and disarmed-no-spend). The NATIVE substrate stays Opus-orchestrated (Agent tool) and pairs with this at the top. The recursive (Level-B) `nano-spawn`/`dispatchPool` depth is wired but its deep-arm is deferred to hardening (the audit's livelock/lease seams).

## Specialized roles — MURE (built 2026-06-22)

The roles seam is now realized as **MURE** (群れ) — a 20-role self-governing agent collective in `_SYSTEM/config/fleet-roles.json` + `_SYSTEM/mure/`. Each role = `{id, archetype, capabilities, substrate, lane, autonomyClass, mathHooks, goalScope, independentOf}`. Use it instead of hand-casting lanes when a task wants named roles:

```bash
node _SYSTEM/mure/mure.mjs --roster        # the 20 roles, 6 groups
node _SYSTEM/mure/mure.mjs --demo           # DISARMED plan of a sample task → roles → leaves (zero spend)
node _SYSTEM/mure/company.mjs --task-file t.json   # cast a real task; armed (YURI_MURE_ARMED / _SYSTEM/state/mure.enabled) → live GLM dispatch
```

`company.runCompany(task)` casts each subtask to its best-matching role (capability match), gates every decision through the 6-gate self-governance charter (`governance.mjs`), and splits the work: GLM roles → runSwarm leaves (dispatched), native roles → Agent specs (for THIS Opus session to spawn). The math layer is wired into role decisions via `math-bridge.mjs` (decision-sim goal-scoring, quantum order-effect, energy veto, prediction Brier). DISARMED by default; arming is owner-gated; finalize stays Opus/owner. Full manual: `_SYSTEM/mure/README.md`.

## Session Notes

- **2026-06-22 (v1.0.0, created):** Built via the model itself — Sonnet research lane (overlap audit + discoverability mechanics: byte-0 frontmatter, `skill-recall` ranks `description` not `triggers`, `skill-sync --sync` publishes `skills/`→`.claude/skills/`), Opus synthesized + registered, Haiku testing lane verified discoverability. Corrections caught this session: Haiku WARN/BLOCK misguess (→ verify-agent-output rule), research found an ENOENT solo missed. Tools: Agent (Explore/sonnet, general-purpose/haiku), Write, Edit, Bash, skill-sync, skill-recall. Errors: none on build. Registered in `skills/domain-index.json` → `01-agent-assembly`; alias `commands/opus-fleet.md`.
- **2026-06-22 (v1.1.0, dual-substrate):** Added the z.ai GLM fleet as the second substrate. Built `_SYSTEM/Scripts/glm-fleet.mjs` (parallel GLM dispatcher on `lane-dispatch.mjs` retry + semaphore, DISARMED dry-run default, `@capability: glm-fleet-dispatch`, `FLEET_PROTOCOL_PREAMBLE` for sub-orchestrators). Wired GLM tier roster into `models.json` (+glm-4.7-flash/flashx, glm-4.6v, glm-ocr) + `llm-lane.mjs` aliases (glm-max=5.2, glm=4.7, glm-flash→4.7-flash remapped off 4.5-air, glm-sub-orch=5.1, glm-vision=4.6v, glm-ocr). Added 5 sections (GLM fleet, dual-substrate routing, sub-orchestrator injection, governed autonomous loop, roles seam) + 4 hard rules + 3 anti-rat rows. GLM reasoning ceiling = `high`. Verified: models.json valid, `glm-flash`→`glm-4.7-flash` resolves, `glm-fleet --list`/`--smoke --dry-run` clean. Built by Opus directly (integration-critical); research via 3 Sonnet Explore lanes (zai internals, governance inventory, online GLM benchmarks) + 1 Sonnet Plan lane (build design); HTML viz approved pre-build. Arming the loop stays owner-gated.
- **2026-06-23 (v1.2.0, third substrate):** Added the **ollama-cloud peer fleet** — `_SYSTEM/Scripts/ollama-fleet.mjs` (mirrors glm-fleet on `lane-dispatch.mjs` retry + semaphore; ONE base `ollama-cloud` lane + `--model <X>:cloud`; roster tiers flash/minimax/kimi/nemotron/deepseek-pro/gemma; DISARMED dry-run default; `@capability: ollama-fleet-dispatch`) + `ollama-fleet.test.mjs` (9/9 red/grey/green). Root-cause RELIABILITY fix: the 3 ollama-cloud lanes in `models.json` lacked `keychain_service`, so `llm-lane.mjs` keychain hydration was skipped for any non-`ai`-wrapper caller → `missing_key`; added `keychain_service: YURI_OS_MUSUBI:OLLAMA_API_KEY` to all 3 (lane-layer fix → every caller benefits). Verified: armed 3-model LIVE smoke (flash 2s + minimax 9s + kimi 33s, all ok, key UNSET → keychain hydrated end-to-end at concurrency 3). Sections added: "ollama-cloud fleet" + "Multi-substrate routing" (dual→triple). Built by Opus directly. Arming stays owner-gated (flag NOT created; smoke via transient env only). Tools: Bash, Read, Edit, Write, capability-scan, llm-lane, keychain probes.
