---
name: team-qa-gauntlet
description: >
  Orchestrate the QA Gauntlet pressure-test team without bloating a single skill.
  Routes to specialist skills: qa-gauntlet (ladder run), qa-gauntlet-ui (game UI
  Smoke/Pressure), qa-gauntlet-combat-ui (engage/kill presentation),
  qa-gauntlet-mission-thread (concurrent-thread honesty),
  qa-gauntlet-agentic-resilience (quarantine / hard-gate contract),
  qa-gauntlet-forge (variance), qa-gauntlet-calibrate (saboteur),
  qa-gauntlet-stress (orthogonal axes), qa-gauntlet-remediation (Phase D TDD + UCA).
  Use when the user runs /team-qa-gauntlet, or asks for "gauntlet team",
  "pressure-test team", "gauntlet UI", or multi-agent gauntlet dispatch.
argument-hint: "[--run-id <id>] [--mode full|ladder|ui|ui-smoke|combat-ui|mission-thread|agentic-resilience|forge|calibrate|stress] [--tiers N]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion
---

# Team QA Gauntlet — Pressure-Test Orchestrator

You are the **Gauntlet Team Lead**. Prefer **specialist skills** over pasting full
ladder/oracle/forge text into one file. Authority for detailed procedures remains
in the specialist `SKILL.md` files under `.claude/skills/`.

**Not** a substitute for `/team-qa` (human sprint QA package / **manual UAT**).

## Team composition

| Role / skill | Owns |
|--------------|------|
| **`/qa-gauntlet`** | Ladder Phase 0–E, batch driver, oracle gates, AAR handoff |
| **`/qa-gauntlet-ui`** | Game UI Smoke/Pressure: PlayMode+C2 filters, ReplayGolden, C2 signoffs ×5 |
| **`/qa-gauntlet-combat-ui`** | Combat-presentation gates (Engage/Kill/CombatDomains). **Not** Slice B |
| **`/qa-gauntlet-mission-thread`** | T3+ concurrent mission-thread honesty (not vocabulary-only intent) |
| **`/qa-gauntlet-agentic-resilience`** | CRITICAL quarantine, retries, BLOCKED, never-LLM-override |
| **`/qa-gauntlet-forge`** | Variance, recipes, promote, Hindsight bank `qa-gauntlet-forge` |
| **`/qa-gauntlet-calibrate`** | Saboteur mutants, kill-rate matrix |
| **`/qa-gauntlet-stress`** | Orthogonal axes `weapons` / `ew` / `logistics`, proof gate |
| **`/qa-gauntlet-remediation`** | Phase D TDD; **UCA gate** on presentation Surfaces |

## Mode routing

| `--mode` | Dispatch |
|----------|----------|
| `full` (default) | `qa-gauntlet` + required forge hooks + **agentic-resilience** on Phase D/AAR; **mission-thread** when Mission-type row is T3+; stress when claimed. Do **not** auto-run combat-ui or C2 ui |
| `ladder` | `qa-gauntlet` only |
| `ui` / `ui-smoke` | **`qa-gauntlet-ui` only** (do not rewrite or run ladder prose) |
| `combat-ui` | **`qa-gauntlet-combat-ui` only** — not Slice B, not C2 signoffs |
| `mission-thread` | **`qa-gauntlet-mission-thread` only** |
| `agentic-resilience` | **`qa-gauntlet-agentic-resilience` only** |
| `forge` | `qa-gauntlet-forge` phases only |
| `calibrate` | `qa-gauntlet-calibrate` |
| `stress` | `qa-gauntlet-stress` plan → derive → proof gate |

### `--mode ui` / `ui-smoke` (summary)

Hard package lives in **`/qa-gauntlet-ui`** — invoke that skill and follow it exactly:

1. `RUN_DIR=production/qa/gauntlet/gauntlet-<timestamp>-ui/`
2. Headless “118-style” UnityAdapter filter (PlayMode/C2/Presentation/Panel/…)
3. `UiIa` IA oracles (selection, COMMS, planning, PanelSettings) via `/qa-gauntlet-ui`
4. `ReplayGolden` filter
5. Unity Editor C2 Play Mode signoffs ×5
6. AAR + `manifest.yaml`
7. Any failure → **`/qa-gauntlet-remediation`** (+ UCA for presentation Surfaces)

**Manual UAT → `/team-qa`** (and `/smoke-check`). UI mode must not invent a second
human QA loop.

### `--mode combat-ui`

Invoke **`/qa-gauntlet-combat-ui`**. Headless Engage/Kill/CombatDomains filters only.
Do **not** implement Combat UX Slice B (DRG-165–170). Do **not** run C2 Play Mode ×5.

### `--mode mission-thread`

Invoke **`/qa-gauntlet-mission-thread`** against `tier-N` policies (T3+). Vocabulary-only
thread claims are **FAIL** → remediation class `scenario-data`.

### `--mode agentic-resilience`

Invoke **`/qa-gauntlet-agentic-resilience`**. Quarantine CRITICAL GitNexus; never let an
LLM override `Passed=false` / `hardGatesPass=false`.

### Slice A/B/C (coordinator)

| Role | Slice A | Slice B | Slice C |
|------|---------|---------|---------|
| mission-thread | Concurrent kill-chain lanes | Out | Out |
| agentic-resilience | Fail-closed agent contract | Out | Out |
| combat-ui | Replay/engage presentation gates | Out (DRG-165–170) | Out |

Each specialist SKILL.md owns inputs, evidence paths, and entry/exit. This file only routes.

## Parallel contract

Follow `production/agentic/qa-skills-parallel-task-contract-2026-07-23.md`:

- **File-disjoint** Tasks only; one-turn dispatch before waiting.
- Scenario generation (forge `a0`) may overlap tier N batch when write paths disjoint.
- Remediation: parallel only after GitNexus `impact` shows disjoint blast radii; serial merge to QA branch.
- UI mode: headless `dotnet test` and Editor signoff are **serial on the same project**
  (Unity lock); do not parallel two Unity Editor instances on one `unity/ProjectAegis`.

## Hard invariants (team-wide)

- Locked eval: `GauntletOracleEvaluator`, Demo batch internals, ReplayGolden fixtures,
  `.github/workflows/gauntlet-oracle.yml` — **never** edit for "learning."
- **`DelegationBridge.cs`** zero-touch; Baltic v2 hash `17144800277401907079` preserved.
- Catalog IDs from roster/DB only; no CatalogWriteGate mutations without EXTEND-ONLY path.
- Graphite for branch/PR; GitNexus `impact` before every symbol edit; `detect_changes()` before commit.
- Script-first hard gates — LLM never overrides `Passed=false` / `hardGatesPass=false`.
- Machine-readable route table: `tools/qa-gauntlet/specialist-routing.yaml` (DRG-199).
  Informs later DRG-200 / DRG-201 — do not implement those tickets here.

## Presentation defects → UCA

If a defect Surface is under `UnityAdapter` / presentation bridges / C2 chrome
(including failures from `--mode ui`):

1. Invoke **`/qa-gauntlet-remediation`** (not ad-hoc fix).
2. That skill loads **unity-csharp-architect** + `pr-finish` (ADR-010/007/001).

See AGENTS.md Unity / C# architecture skill section.

## Success

- Specialist skills invoked by name; no duplicate full ladder prose in this file.
- `--mode ui` ⇒ AAR under `production/qa/gauntlet/<RUN_ID>/` per `/qa-gauntlet-ui`.
- `--mode combat-ui` ⇒ `/qa-gauntlet-combat-ui` (not Slice B).
- `--mode full` T3+ ⇒ `/qa-gauntlet-mission-thread`; Phase D ⇒ `/qa-gauntlet-agentic-resilience`.
- AAR cites latest calibrate report when forge/ladder ran.
- Stress claimed ⇒ `qa-gauntlet-stress` proof gate evidence attached.
- UI track never claims manual UAT complete.

## See also

- `/qa-gauntlet`, `/qa-gauntlet-ui`, `/qa-gauntlet-combat-ui`
- `/qa-gauntlet-mission-thread`, `/qa-gauntlet-agentic-resilience`
- `/qa-gauntlet-forge`, `/qa-gauntlet-calibrate`
- `/qa-gauntlet-stress`, `/qa-gauntlet-remediation`
- `/team-qa` — human sprint package / **manual UAT**
- `/smoke-check` — sprint smoke hand-off
- `tools/qa-gauntlet/README-stress-axes.md`
- Reference UI run: `production/qa/gauntlet/gauntlet-20260817-1626-ui/`
