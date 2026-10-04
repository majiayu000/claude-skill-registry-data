---
name: qa-gauntlet
description: >
  Autonomous headless QA loop for Project Aegis: generate scenarios of escalating
  complexity (mission type, platform mix, victory conditions, events, ROE, EMCON)
  grounded in the platform catalog DB, run them through the batch sim harness, and
  remediate every defect via TDD. Runs a fixed 5-tier ladder unattended, commits
  fixes to a QA branch, and delivers a full AAR. Use when the user runs
  /qa-gauntlet, or asks for "QA gauntlet", "escalating complexity QA", "tiered
  scenario stress test", "autonomous sim QA loop", "batch sim defect remediation",
  or "gauntlet AAR". Companions: /qa-gauntlet-forge, /qa-gauntlet-stress,
  /qa-gauntlet-remediation, /qa-gauntlet-calibrate, /qa-gauntlet-ui,
  /qa-gauntlet-mission-thread, /qa-gauntlet-agentic-resilience,
  /qa-gauntlet-combat-ui; team entry /team-qa-gauntlet.
argument-hint: "[--tiers N=5] [--scenarios-per-tier N=4] [--seeds 42,7,123] [--max-fix-attempts 3] [--resume <run-id>]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion
---

# QA Gauntlet — Autonomous Escalating-Complexity Test Loop

You are the **QA Gauntlet Orchestrator**. Run the full loop unattended. This skill
operates under an explicit user-granted autonomy override of the Collaborative
Design Principle: you MAY write scenario files, tests, and fixes, and commit to the
QA branch without per-change approval. All other CLAUDE.md / AGENTS.md rules remain
binding — especially GitNexus impact analysis before every symbol edit,
`detect_changes()` before every commit, and Graphite (`gt`) for all branch work.

**Team (avoid skill bloat):** multi-agent entry is `/team-qa-gauntlet`. Specialists:
`/qa-gauntlet-forge` (variance), `/qa-gauntlet-stress` (orthogonal axes),
`/qa-gauntlet-remediation` (Phase D + **UCA** on presentation Surfaces),
`/qa-gauntlet-calibrate` (saboteur), `/qa-gauntlet-ui` (game UI Smoke/Pressure),
`/qa-gauntlet-mission-thread` (T3+ concurrent-thread honesty),
`/qa-gauntlet-agentic-resilience` (quarantine / hard-gate contract),
`/qa-gauntlet-combat-ui` (engage/kill presentation — **not** Combat UX Slice B).
This file owns the ladder contract; specialist runbooks live in those skills.

**Variance companion:** invoke `/qa-gauntlet-forge` for self-improving scenario /
platform / mission variance (Karpathy-style promote loop). Forge owns candidates,
corpus, recipe weights, and Hindsight bank `qa-gauntlet-forge`; this skill owns
batch execution, oracle gates, and dispatches remediation. See
[`.claude/skills/qa-gauntlet-forge/SKILL.md`](../qa-gauntlet-forge/SKILL.md).

**Autonomy boundary:** if GitNexus impact returns CRITICAL on a symbol a fix must
touch, do NOT edit it. Quarantine the defect (see Phase D), continue the tier with
the remaining scenarios, and surface it prominently in the final report.

## Phase-static model routing

No free model shopping. The orchestrator skill frontmatter stays `model: sonnet`
(or unset — defaults to `sonnet` per coordination-rules). Task spawns follow the
table below. Escalate to `opus` only for CRITICAL quarantine synthesis or
multi-tier AAR conflict. Aliases only: `haiku` / `sonnet` / `opus` — never
version-pinned IDs in skill files.

| Phase | Model | Notes |
|-------|-------|-------|
| Preflight / forge `pre` / scorecard plumbing / expect CSV digest | `haiku` or **no LLM** (script) | Script-first |
| A0 roster digest | `haiku` | |
| A1 / forge `a0` draft | `sonnet` | architect |
| B batch + C oracle CLI | **tools only** | Then `haiku` to summarize exit codes |
| D TDD Red/Green | `sonnet` via `/qa-gauntlet-remediation` | `opus` if CRITICAL / quarantine synthesis |
| forge `post-oracle` promote judgment | `sonnet` after script scorecard | Never override hard gates |
| E / forge `e` | `haiku` | |
| Final AAR distill | `haiku` → `sonnet` prose | `opus` for stuck / multi-tier conflict |

Contract authority: `production/agentic/qa-skills-parallel-task-contract-2026-07-23.md`.

## Invocation

```
/qa-gauntlet [--tiers N=5] [--scenarios-per-tier N=4] [--seeds 42,7,123] [--max-fix-attempts 3] [--resume <run-id>]
```

| Flag | Default | Meaning |
|---|---|---|
| `--tiers` | `5` | Number of complexity tiers to run (1–5) |
| `--scenarios-per-tier` | `4` | Scenarios generated per tier |
| `--seeds` | `42,7,123` | Comma-separated seeds; every scenario × every seed |
| `--max-fix-attempts` | `3` | Max TDD remediation cycles per defect |
| `--resume` | _(none)_ | Continue an existing run from its last completed tier |

**Preferred tools for this skill:** Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion.

## Run identity & artifacts

- `RUN_ID = gauntlet-$(date +%Y%m%d-%H%M)`
- Artifact root: `production/qa/gauntlet/<RUN_ID>/`
  - `manifest.yaml` (tier plan + scenario registry), `tier-N/` (roster, scenario JSONs, CSVs, logs),
    `bugs/` (bug reports), `fixes.md` (TDD fix log), `AAR.md` (final report)
- Branch: `gt create -m "qa: gauntlet <RUN_ID>"` off trunk before any edit. All
  commits land here. Never push with raw git; `gt submit --stack --no-interactive`
  only at the very end, and only if at least one fix was committed.
- If `--resume <run-id>` was passed, read that manifest, find the last completed
  tier, and continue from the next phase instead of starting over.

## Phase 0 — Preflight gates (hard stop on failure)

1. `node .gitnexus/run.cjs analyze` if the GitNexus index is stale
   (check `gitnexus://repo/cmano-clone/context`).
2. Baseline: `dotnet test ProjectAegis.sln` must be fully green. Record the test
   count as the monotonic baseline — it may only grow during this run.
3. Replay determinism gate: run the `replay-verify` skill (golden replays must pass;
   AGENTS.md: ReplayGolden **6/6**). If red, the gauntlet is invalid — stop and report.
4. Smoke: run the `smoke-check` skill.
5. Catalog gate: confirm `assets/data/catalog/baltic_patrol.db` opens and its
   migrations are current (see `sqlite-schema-management` skill). Scenario
   generation is catalog-driven; a stale or broken catalog invalidates the run.
6. Write `manifest.yaml` with the tier plan below, resolved arguments, baseline
   numbers, and git SHA.

## The complexity ladder

Generate `--scenarios-per-tier` scenarios per tier (default 4). Every scenario is
run with every seed in `--seeds` (default `42,7,123`). Each dimension escalates
per this matrix — combine dimensions within a tier, don't cherry-pick one:

| Dim | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Tier 5 |
|---|---|---|---|---|---|
| **Mission type** | Single patrol | Strike OR escort | Escort + strike combined | ASW/AAW multi-mission | Multi-domain theater op (patrol+strike+escort+ASW concurrent) |
| **Platform mix** | 3 surface units/side (~6) | 3 surface + 1 air / side (~8) | 3 surface + 2 air + 1 sub / side (~12) | 3–4 surface + 2 air + 1–2 sub / side (~14) | 4 surface + 3 air + 2 sub blue vs dense red (~16); asymmetric joint mix |
| **Victory conditions** | Survive N ticks | Destroy designated target | Protect HVU + destroy target | Weighted multi-objective scoring | Conditional/dynamic objectives that change on trigger |
| **Events** | None | 1 scripted timed event | Timed event chain | Random injects (seeded) | Cascading adversarial injects (comms loss, sensor degradation, reinforcements) |
| **ROE** | Weapons free, both sides | Weapons tight one side | ID-required engagement criteria | Asymmetric per-side ROE + escalation rules | Mid-mission ROE changes via event |
| **EMCON** | Unrestricted emissions | Passive-only one side | Timed EMCON phases | Dynamic EMCON change on detection | Contested EM: deception emitters + EMCON discipline scored |

Tier N+1 may not start until tier N is green (all scenarios pass all oracles,
after remediation) or explicitly quarantined.

## Orthogonal stress axes

**Specialist skill:** `/qa-gauntlet-stress` (runbook:
[`tools/qa-gauntlet/README-stress-axes.md`](../../../tools/qa-gauntlet/README-stress-axes.md)).
When axes are claimed in the run, invoke that skill for plan → derive → proof gate;
do not re-derive proof modes here.

Three **independent** axes layer onto any tier via pairwise matrix: `ew`,
`logistics`, `weapons` (`production/qa/gauntlet/corpus/stress-axes.yaml`).

| Axis | Proof mode | Control sibling |
|---|---|---|
| `weapons` | `differential-token` (`NO_AMMO`) | **Required** |
| `ew` | `differential-aggregate` (`Detected`) | **Required** |
| `logistics` | `config-only` (GAP-13) | — |

- Plan with `plan_stress_matrix`; report `estimatedRuns` / `dropped` before execute.
  Shipped catalog `tiers=[1..5], seeds=3, max_configs=24` → ~105 runs.
- **Budget anchors — do not conflate:** default ladder **60** runs; corpus regression
  ~**117** (tiered policies × 3 seeds). Matrix ~1.75× ladder — not "cheaper than ladder."
  Treat corpus cost as ceiling; lower `max_configs` if exceeded.
- `logistics` is **never** reported proven. `weapons` proven only on **strict increase**
  vs control (presence-only is invalid — baseline already emits many `NO_AMMO`).
- Forge recipes: `stress-weapons-*`, `stress-ew-*`, `stress-logistics-config-only`.

## Per-tier loop

### Phase A — Scenario generation (parallelizable with tier N execution)

**Forge pre + A0 (required).** Before roster drafting for tier 1 (and again when
starting each new tier's A0), invoke `/qa-gauntlet-forge`:

```
/qa-gauntlet-forge --run-id <RUN_ID> --tier <N> --phase pre
/qa-gauntlet-forge --run-id <RUN_ID> --tier <N> --phase a0
```

Forge recalls Hindsight bank `qa-gauntlet-forge`, loads
`production/qa/gauntlet/corpus/` (coverage-map, recipe weights, hard-cases),
writes `forge/mid-tier-plan.yaml`, and drafts ephemeral candidates under
`production/qa/gauntlet/<RUN_ID>/forge/candidates/` (gitignored). Prefer
under-covered catalog platforms from the coverage map. Do **not** commit
candidates until forge promotion after oracle.

**A0 — Platform roster from the catalog.** Before scenario drafting, spawn
`sim-data-specialist` to assemble the tier's platform roster from real data:

- Query the catalog DB `assets/data/catalog/baltic_patrol.db` (schema per
  `src/ProjectAegis.Data/Catalog` and the `sqlite-schema-management` skill) for
  platform, sensor, and weapon IDs matching the tier's platform-mix row —
  including each platform's `CatalogEmcon` emissions profile and archetype bindings.
- For tiers 4–5 (UAV/drone/swarm, asymmetric near-future mixes), draw from
  `data/catalog/near_future_archetypes.json` and
  `data/catalog/speculative_platforms.json`; sensors from
  `data/catalog/sensors_baltic.json`.
- Cross-check plausibility (ranges, speeds, loadouts) against the offline
  reference export in `docs/reference/cmano-db/` where a real-world analog exists.
- Output: `tier-N/roster.json` — the only platform/sensor/weapon IDs the
  architect may reference.

**A1 — Drafting.** Spawn `military-simulation-architect` (Task tool) with the
tier row from the matrix, `tier-N/roster.json`, and the schema of an existing
scenario under `data/scenarios/` as reference. It must produce the scenario JSONs
into `production/qa/gauntlet/<RUN_ID>/tier-N/` — referencing only roster IDs,
with EMCON postures consistent with each platform's `CatalogEmcon` profile —
plus a one-line intent + expected-outcome oracle per scenario (e.g. "Blue wins by
HVU survival; Red fires ≤ X missiles under tight ROE").

**A1b — Mission-thread honesty (T3+ required).** When the ladder **Mission type**
row is T3 or higher, invoke `/qa-gauntlet-mission-thread --run-id <RUN_ID> --tier <N>`
before A2. Vocabulary-only thread claims are `scenario-data` (do not duplicate the
checklist here).

**A2 — Validation.** Validate every generated scenario before running:

- **Catalog resolution (oracle 0):** every entity, sensor, and weapon ID in the
  scenario resolves against `tier-N/roster.json` (and therefore the catalog DB).
  Unresolved ID → `scenario-data` defect, regardless of whether the sim tolerates it.
- `pwsh tools/mission-editor/Invoke-ScenarioValidate.ps1 <file>` (or the
  mission-editor CLI equivalent via `dotnet run --project src/ProjectAegis.MissionEditor.Cli`)
- Run the `scenario-audit` skill on the batch.

Invalid scenario → send back to the architect with the validator output, max 2
regeneration attempts, then drop it and log why.

**Parallel Task note (Phase A — contract: `production/agentic/qa-skills-parallel-task-contract-2026-07-23.md`):**
Starting A0/A1 for tier N+1 while tier N executes (Phase B) is **required** when
feasible, not optional. Rules:
- **Independent domain** = disjoint write paths and no shared mutable counters (BUG-NNN, RUN_ID). Scenario generation is data-only and cannot conflict with code fixes.
- **Self-contained Task prompt:** each spawned Task must include scope / goal / constraints / return summary.
- **One-turn dispatch:** issue all independent Task calls in a single orchestrator turn before waiting on any result.
- Surface **BLOCKED** immediately; always produce a partial report.

### Phase B — Execution (canonical driver)

Run the shipped driver — do NOT hand-roll batch loops or oracle checks:

```bash
tools/qa-gauntlet/run-gauntlet.sh --run-id <RUN_ID> [--tiers "1 2 3 4 5 extra"] \
  [--seeds 42,7,123] [--roving 2]
```

Optional stress proof after ladder: `--stress-proof-evidence PATH` or invoke
`/qa-gauntlet-stress`.

The driver resolves dotnet itself (PATH, then `~/.dotnet/dotnet`), loads the ladder
contract from `tools/qa-gauntlet/ladder.yaml` (tier → scenarios + ticks), runs each
tier's batch plus an identical repeat batch, filters anchor seeds via
`evaluate_run.py filter-seeds`, runs `gauntlet_oracle_eval` on those rows (strict
gate: `GauntletPolicyStrictKeys` in `ProjectAegis.Data` — unknown `gauntlet.*` keys
fail closed inside `GauntletOracleEvaluator`; legacy `gauntlet.emcon` warns),
evaluates roving rows separately in observe mode, and invokes
`tools/qa-gauntlet/evaluate_run.py` for tier and run verdicts. Roving seeds are
derived from the run id and recorded in `roving-seeds.txt` (reproducible).

For generated (Phase A) scenarios not in the shipped ladder, stage them into
`data/scenarios/` first or run the Demo batch directly, then call
`evaluate_run.py tier` on the tier dir — the oracle set is identical either way.

## Script-first mechanical gates

Hard gates **must** be driven by CLI tools — not LLM reinterpretation of raw
results data:

- **Oracle evaluation:** always run `dotnet run --project src/ProjectAegis.MissionEditor.Cli -- gauntlet_oracle_eval …` (see Phase C). Do not ask an LLM to interpret `results.csv` directly against `gauntlet.expect` fields.
- **Forge scoring:** always run `python3 tools/qa-gauntlet/forge_scorecard.py` before any promote judgment. LLM (`sonnet`) may apply judgment only *after* the scorecard output is present.
- **Class `oracle` defects** → expect-regen runbook only. Batch at tier ticks → CSV → update `gauntlet.expect` envelopes programmatically. **No hand-editing envelopes.**
- After tools run, `haiku` may summarize exit codes / logs. It **must not** override `Passed=false` without a formal triage-class promotion (reclassifying from `sim-code` to `oracle` requires the qa-lead justification flow, not an LLM opinion alone).

### Phase C — Oracle evaluation (hard gate — no stability-only green)

**Required:** every scenario policy MUST include `gauntlet.intent` and machine-checkable
`gauntlet.expect` (fields: `side`, `minKills`, `maxMissilesFired`, `minDenials`,
`maxDenials`, `minScore`, `maxScore`, `requireNonEmptyFingerprint`). Missing expect
is an automatic tier fail.

**Required:** after batch, run the shipped evaluator via CLI and write `tier-N/oracle-eval.json`:

```bash
dotnet run --project src/ProjectAegis.MissionEditor.Cli -- gauntlet_oracle_eval \
  --policy-dir production/qa/gauntlet/<RUN_ID>/tier-N \
  --csv production/qa/gauntlet/<RUN_ID>/tier-N/results.csv \
  --out production/qa/gauntlet/<RUN_ID>/tier-N/oracle-eval.json
```

A tier is **not** green on stability/fingerprint alone — if the evaluator returns
`Passed=false` (CLI exit 1), the tier fails and defects are opened.

**CI:** PR workflow `.github/workflows/gauntlet-oracle.yml` runs Demo batch + this CLI
(fail-closed). Local dry-run mirrors that job.

**Hindsight re-test:** closed defects live in `production/qa/gauntlet-defect-registry.json`.
Re-run a closed defect after a fix:

```bash
tools/qa-gauntlet/retest-defect.sh <defect-id> --out-dir <scratch>
```

**Oracles are code:** read `tier-N/verdict.json` and run-level `verdict.json` from
`evaluate_run.py`. Any `"status": "fail"` fails the tier. Spawn `qa-lead` only to
*triage*, not re-derive. `roving_observe` is warn-only.

**Forge post-oracle (required).** After oracle-eval.json is written for the tier:

```
/qa-gauntlet-forge --run-id <RUN_ID> --tier <N> --phase post-oracle
```

If stress axes were claimed, forge must record stress-proof evidence (see forge
`program.md` + `/qa-gauntlet-stress`). Locked eval is never edited by forge.

Every failed oracle becomes a defect via `bug-triage`: `scenario-data`, `sim-code`,
`oracle`, or `flaky`.

### Phase D — TDD remediation (max `--max-fix-attempts` per defect, default 3)

**Dispatch `/qa-gauntlet-agentic-resilience`** for CRITICAL GitNexus / stalled Task /
LLM-vs-script-gate conflicts (quarantine contract). Then
**dispatch `/qa-gauntlet-remediation`** for each defect (keeps this skill lean).

Summary contract:

1. **Red** — minimal xUnit in co-located `*.Tests`; fixed seed; confirm RED.
2. **Impact** — GitNexus upstream; CRITICAL → quarantine.
3. **Green** — minimal fix (`c-sharp-engineer` / `determinism-engineer`).
4. **Verify** — full suite ≥ baseline; ReplayGolden green; re-run scenario × seeds.
5. **Commit** — `detect_changes()`; Graphite on QA branch; append `fixes.md`.
6. Attempts exhausted → revert, quarantine, continue.

**UCA gate:** if Surface is `UnityAdapter/Bridge/**`, Presentation, or C2 projection
façade, remediation **must** load **unity-csharp-architect** + `pr-finish`
(ADR-010/007/001; ZERO-touch `DelegationBridge.cs`). See AGENTS.md.

Parallel fixes: `production/agentic/qa-skills-parallel-task-contract-2026-07-23.md`.

### Phase E — Tier gate

Re-run every previously-failed scenario × seed. Tier is green when all
non-quarantined scenarios pass all oracles. Record the tier summary in the
manifest. Retain learnings via hindsight skills.

**Forge mid-tier (required):**

```
/qa-gauntlet-forge --run-id <RUN_ID> --tier <N> --phase e
```

## Final phase — AAR & handoff

After tier 5 (or an unrecoverable halt):

1. `/qa-gauntlet-forge --run-id <RUN_ID> --phase final` — require `forge/promote-log.md`
   if forge ran.
2. AAR must include: "Last oracle calibration: **2026-07-31**, kill rate **7/7**
   (`production/qa/gauntlet/calibration-2026-07-31-full-after-blindspot-close/report.md`)"
   — run `/qa-gauntlet-calibrate` if oracles/goldens changed since that report.
3. Defect class counts table; qa-lead sign-off; `detect_changes` vs main.
4. `gt submit --stack --no-interactive` if fixes/promotions committed; do NOT merge.
5. List every `QUARANTINED-CRITICAL` item for humans.

## Hard rules recap

- Never edit a symbol without `impact` first; never ignore HIGH/CRITICAL silently.
- Never commit without `detect_changes()`.
- Never use raw `git push` / `gh pr create` — Graphite only.
- Test count is monotonic; a fix that deletes tests is invalid.
- Every fix starts from a failing test. No test, no fix.
- Scenarios may only reference platform/sensor/weapon IDs present in the tier roster.
- Budget guard: if a single tier exceeds 12 defects or the run exceeds remediation budget, halt to Final phase.
- Presentation Surfaces → UCA / pr-finish via `/qa-gauntlet-remediation`.

## See also

- `/team-qa-gauntlet` — multi-agent orchestrator (preferred entry for full pressure team).
- `/qa-gauntlet-ui` — game UI Smoke/Pressure (`--mode ui`); not part of this ladder contract.
- `/qa-gauntlet-combat-ui` — engage/kill presentation (`--mode combat-ui`); not Slice B.
- `/qa-gauntlet-mission-thread` — T3+ concurrent-thread honesty.
- `/qa-gauntlet-agentic-resilience` — quarantine / never-LLM-override.
- `/qa-gauntlet-forge` — variance companion; Hindsight bank `qa-gauntlet-forge`.
- `/qa-gauntlet-stress` — orthogonal axes + proof gate.
- `/qa-gauntlet-remediation` — Phase D TDD + UCA presentation gate.
- `/qa-gauntlet-calibrate` — saboteur / kill-rate.
- `/team-qa` — human sprint QA package / **manual UAT** (not a substitute for the gauntlet ladder).
- `/smoke-check` — Phase 0 preflight.
