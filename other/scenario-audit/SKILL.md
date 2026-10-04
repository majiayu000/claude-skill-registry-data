---
name: scenario-audit
description: "Validate scenario content against the canonical database, determinism constraints, and editor tooling: ID resolution, provenance, seed/replay compliance, Cli validate round-trip, briefing/victory consistency. Produces a per-scenario PASS/FAIL report with fix routing."
argument-hint: "[scenario-path | all] [--quick]"
allowed-tools: Read, Glob, Grep, Bash, Write, AskUserQuestion, Task
model: sonnet
agent: scenario-content-specialist
user-invocable: true
---

# Scenario Audit

Scenarios are the product at Release stage. This audit proves a scenario is
loadable, database-faithful, deterministic, and honest about its own victory
conditions.

Scenario locations: `data/scenarios/`, `assets/data/scenarios/`. Editor
tooling: `src/ProjectAegis.MissionEditor.Cli` (see its tests for current verb
surface). Sim-side scenario model: `src/ProjectAegis.Sim/Scenario/`.

---

## GitNexus Discovery Integrated Steps

GitNexus is used for discovery and safety (planning + verification only; no src edits from this skill):

1. Enumerate scenarios via Glob (`data/scenarios/*.policy.json`, `assets/data/scenarios/*.policy.json`, examples under `data/scenarios/examples/`).
2. For each scenario, note last commit via Bash (`git log -1 --format=%h -- <path>`).
3. Optional discovery: use GitNexus MCP `query` or `context` on scenario loading paths to surface test/harness coverage and related symbols (informational only for audit evidence; cite counts/risk).
4. In checks involving entity references, note any GitNexus-indexed catalog symbols if cross-referenced in code paths (planning context only).
5. Pre-fix and post-fix (in Phase 4): run `detect_changes` (if changes staged) or node .gitnexus/run.cjs detect_changes to confirm only scenario content touched.
6. Re-index advisory: if index stale, note it; re-analyze is out of scope for content audit.

Hybrid execution: prefer `dotnet run --project src/ProjectAegis.MissionEditor.Cli -- scenario_validate <path>` ; fall back to direct JSON read + schema for parse when CLI unavailable. Invoke `/replay-verify [scenario]` (or sub-set) for determinism on golden-backed scenarios.

## Phase 1: Inventory

**GitNexus discovery (mandatory first step):**

Use query and context on the following symbols before any file operations:
- `gitnexus query` with `search_query="ScenarioValidationEngine ScenarioDocumentJsonLoader BrokenRefRule DbRefRule TlBranchRule PatrolZoneRule StrikeReachabilityRule FerryReachabilityRule DoctrineInheritanceRule EventGraphComplexityRule ScenarioValidationExportGate ScenarioPolicyRepository catalog resolve ReachabilityCalculator"`
- `gitnexus context` (name=ScenarioValidationEngine), (name=BrokenRefRule), (name=ScenarioDocumentJsonLoader), (name=ScenarioValidationExportGate), (name=ScenarioPolicyRepository), (name=DbRefRule), (name=ValidationRules) (include calls to loaders, catalog binding, EventGraph, ID provenance and rule call chains).

Resolve the argument:
- No argument or `all` → every `.scenario.json` and `*.policy.json`.
- Specific path → that single file (must end in `.scenario.json` or `.policy.json`).

**Discovery commands (runnable):**
- `Glob` glob="data/scenarios/**/*.scenario.json"
- `Glob` glob="data/scenarios/*.policy.json"
- `Glob` glob="assets/data/scenarios/**/*.scenario.json"
- `Glob` glob="assets/data/scenarios/*.policy.json"
- `Glob` glob="data/scenarios/examples/*.scenario.json"

For every resolved path:
1. `Bash` `git log --oneline -1 -- <path>` (capture last-modified commit).
2. `Read` `<path>` (limit 40 lines) + targeted `Grep`:
   - `Grep` pattern="\"metadata\"|\"seed\"|\"policyId\"|\"tlBranch\"|\"dbRef\"|\"dbSnapshotId\"" glob="<path>"
   - `Grep` pattern="\"patrolZone\"|\"targetIds\"|\"assignedUnitIds\"|\"missions\"" glob="<path>"
   - For `.policy.json`: `Grep` pattern="\"id\"|\"engage\"|\"detection\"|\"replay\"" glob="<path>"
3. Record:
   - Type: `.scenario.json` (missions + metadata) or `.policy.json` (policy profile + replay section)
   - `metadata.seed` presence and value (if present)
   - `policyId`, `tlBranch`, `dbRef` / `dbSnapshotId`
   - Mission count + types (Patrol/Stroke/Ferry) or detection/engage id lists
   - Format indicators (editVersion, required fields per schema)

Build inventory list/table with one row per item (path, type, seed present?, key metadata fields, last commit).

## Phase 2: Checks (per scenario)

**GitNexus discovery (mandatory first step before any check):**

Repeat before checks:
- `gitnexus query` `search_query="ScenarioValidationEngine Validate BrokenRefRule ReachabilityRule PatrolZoneRule StrikeReachabilityRule DoctrineInheritanceRule DbRefRule TlBranchRule EventGraphComplexityRule ScenarioValidationExportGate catalog cross-ref" task_context="per-scenario checks" goal="map exact rule order, catalog ID resolution for units/targets/sensors in missions and policy detection/engage, loader paths, export gate"`
- `gitnexus context` for `ScenarioValidationEngine`, `BrokenRefRule`, `StrikeReachabilityRule`, `PatrolZoneRule`, `DoctrineInheritanceRule`, `ScenarioDocumentJsonLoader`, `ScenarioPolicyRepository`, `ScenarioValidationExportGate`.

**Spawn via Task (for deep per-item execution):**

Spawn `scenario-content-specialist` via `Task`. Pass:
- Inventory list from Phase 1
- Scope (`--quick` or full)
- GitNexus summary (symbols, call chains, catalog resolve logic)
- Explicit instruction: "Perform checks using CLI first; fallbacks only if CLI unavailable. Use only Read/Glob/Grep/Bash on scenario/policy files. Report per check with exact evidence. Never edit src or goldens."

Collect results from the specialist before continuing.

**Severity mapping:**

| Level   | Definition                                      | From rules / examples                          |
|---------|-------------------------------------------------|------------------------------------------------|
| BLOCKER | Prevents parse, export, or sim (Error severity, CLI exit 1) | Parse fail, DB_MISMATCH (DbRefRule), BROKEN_REF, PATROL_ZONE_DEGENERATE, STRIKE_NO_TARGETS, STRIKE_UNREACHABLE / FERRY_UNREACHABLE (Reachability*), missing/invalid tlBranch |
| HIGH    | Integrity or determinism risk on non-golden     | Missing provenance (hand-typed overrides contradicting catalog), determinism without clean replay |
| MEDIUM  | Behavioral / honesty issues                     | Dead triggers, reachability warnings, victory/briefing mismatch, EventGraph soft warnings |
| LOW     | Sanity / smoke                                  | Balance OOB, minor doctrine notes (Info findings) |

`--quick` = checks 1–2 only.

**For each `.scenario.json` (in inventory order):**

1. **Parses / schema-valid (BLOCKER)**
   - CLI (primary):  
     `Bash` `dotnet run --project src/ProjectAegis.MissionEditor.Cli -- scenario_validate <path>`  
     (exact verb from Program.cs). Capture stdout (ValidationReportJsonDto) + exit code.  
     0 + no blocking findings = pass. Any Error = BLOCKER. Note CLI output verbatim.
   - Fallback (CLI unavailable or authoring docs path):  
     `Read` full file.  
     Load: `ScenarioDocumentJsonLoader.LoadFromFile(<path>)` (respects camelCase, trailing commas, comments per data/scenarios/scenario-document.schema.json).  
     Resolve catalog (CLI catalog commands or InMemory Baltic fixture path).  
     `ScenarioValidationExportGate.EvaluateExport(scenario, catalog, new ValidationConfig())` or direct `ScenarioValidationEngine.Validate(...)`.  
     Inspect `report.CanExport(...)` and `findings` for Error level.

2. **Entity ID resolution (BLOCKER)**
   - CLI already surfaced (DB_MISMATCH, BROKEN_REF).
   - `Grep` pattern="\"assignedUnitIds\"|\"targetIds\"|\"patrolZone\"|sensor|weapon" glob="<path>"
   - Catalog cross-ref: `Bash` `dotnet run --project src/ProjectAegis.MissionEditor.Cli -- catalog_platform_browse` (or equivalent) + `Grep` on `data/catalog/*.json` and `assets/data/catalog/*.json` for every unit/target/sensor id.
   - Rules exercised: `DbRefRule` (dbRef / dbSnapshotId must resolve via catalog.TryResolveDbRef), `BrokenRefRule` (literal `ref:` prefixes must match units in same document).
   - Policy link: if `policyId` present, load linked `.policy.json` and cross-ref its detection/engage ids.

3. **Provenance (HIGH)**
   - `Read` metadata section.
   - Rules: `TlBranchRule`, `TlReleaseTrainRule`, `DbRefRule` (binding must match catalog snapshot branch).
   - Verify every referenced platform/weapon/sensor carries catalog provenance (no contradicting inline numeric overrides for stats that live in DB).
   - `Grep` pattern="combatRadius|hp|sensorRange|magazine" glob="<path>" (flag hand-typed values).

4. **Determinism (BLOCKER for golden-backed scenarios, HIGH otherwise)**
   - Seed check (mandatory): `Grep` pattern='"seed":\s*[0-9]+' glob="<path>" or `Read` metadata.seed. Must be present (ulong root per schema; used for RNG).
   - Delegate: invoke `/replay-verify` (or Task spawn of replay-verify on the scenario name extracted from path/policy). Confirm same seed produces identical world hash + order log.
   - If policyId present: also inspect linked `.policy.json` "replay" section.
   - `--quick` still requires the seed declaration check.

5. **Victory/briefing honesty (MEDIUM)**
   - `Grep` pattern="victory|brief|win|score|condition|objective" glob="<path>" (case-insensitive).
   - Compare declared victory conditions against actual missions + event triggers that affect scoring.
   - Cross-check policy ROE + mission roeOverride.

6. **Trigger reachability (MEDIUM)**
   - CLI validate runs the reachability rules.
   - Direct rules: `PatrolZoneRule` (≥3 waypoints), `StrikeNoTargetsRule`, `FerryDestinationRule`, `StrikeReachabilityRule`, `FerryReachabilityRule` (catalog positions + combat radius + fuel via ReachabilityCalculator.HaversineNm).
   - `Grep` for events/triggers + cross-ref all referenced entity/zone IDs.
   - `EventGraphComplexityRule` for trigger graph health (hard cap + soft warnings).
   - Evidence: CLI finding codes or manual "id X in trigger Y does not resolve".

7. **Balance smoke (LOW)**
   - `Grep` missions + `unitReadiness`.
   - Verify sides have the assets the (briefing) description promises.
   - Cross `policyId` engage/detection counts vs. declared OOB.

**For each `.policy.json` (separate path):**

- Direct parse: `Read` full file.
- `Grep` pattern='"detection"|"engage"|"observerId"|"sensorId"|"targetId"|"replay"' glob="<path>"
- Use ScenarioPolicyRepository logic equivalent: ensure id loadable; extract engage + detection arrays.
- Catalog cross-ref for every id appearing in detection[] and engage fields (observer, sensor, target, platforms) via `Grep` on catalog JSONs + CLI catalog commands.
- Replay section: if present, record `checkpointIntervalTicks` and tie to determinism seed check.
- Cross-reference: any `.scenario.json` declaring `"policyId": "<this-id>"` must be consistent (units in scenario missions must be addressable by the policy's detection/engage ids).
- No CLI `scenario_validate` path; all checks via Read + Grep + catalog cross-ref.

After all checks for an item, emit findings list with:
- Check number + title
- Severity
- Evidence (exact CLI line / rule name / json snippet / GitNexus symbol)
- Concrete remediation (scenario/policy file edit only)

## Phase 3: Report

Present executive summary + per-scenario table + key findings + routing in conversation.

**Severity table (used for findings):**

| Level | Definition |
|-------|------------|
| **BLOCKER** | Prevents load, ID resolution, or determinism for golden scenarios. Must fix before release. |
| **HIGH** | Breaks provenance or high-confidence fidelity; likely to cause downstream failures. |
| **MEDIUM** | Inconsistency (briefing vs. actual) or reachability issues; impacts play quality. |
| **LOW** | Balance smoke or polish; advisory. |

**Report template (written to file):**

```markdown
# Scenario Audit Report

**Date**: [YYYY-MM-DD]
**Scope**: [scenario-path | all] [--quick]
**Scenarios audited**: [N]
**GitNexus index**: [fresh | stale note]
**Audited by**: scenario-content-specialist via /scenario-audit
**Quick mode**: [yes/no — checks 1-2 only]

---

## Executive Summary

| Verdict | Count |
|---------|-------|
| PASS | [N] |
| PASS-WITH-FINDINGS | [N] |
| FAIL | [N] |
| NOT RUN (partial) | [N] |

**Overall Verdict**: PASS / PASS-WITH-FINDINGS / FAIL (any BLOCKER present)

**Re-run required after fixes**: Yes — Phase 2 checks re-executed on changed scenarios.

---

## Per-Scenario Results

| Scenario | Format | Checks Passed | BLOCKERs | Verdict | Evidence |
|----------|--------|---------------|----------|---------|----------|
| [name.policy.json] | v2 / unknown | 7/7 | 0 | PASS | Cli exit=0; 42/42 entity IDs resolved (GitNexus: 18 upstream refs); seed=42; replay hash 0xDEADBEEF match (A==B, A==golden); briefing matches triggers; no orphans |
| [other] | v2 | 3/7 | 2 | FAIL | BLOCKER: Cli validate failed (schema error on zone); BLOCKER: orphan platform "XX-99" not in DB; HIGH: provenance drift on speed stat |
... (one row per scenario)

---

## Detailed Findings

### [scenario] — BLOCKER-001
**Severity**: BLOCKER
**Check**: 1 (Parses)
**Evidence**: `dotnet run --project src/ProjectAegis.MissionEditor.Cli -- scenario_validate <path>` → exit 1; "missing required field: triggers[0].zone"
**Remediation (content only)**: Add zone definition or correct reference in scenario JSON.
**Route**: scenario-content-specialist

### [scenario] — HIGH-002
...
[repeat per finding; include file:line or json path for evidence; cite GitNexus when used for discovery]

---

## Routing Summary

- DB gaps / missing entities / provenance contradictions → database-intelligence-lead
- Cli defects / validate round-trip failures / command surface bugs → /bug-report (c-sharp-engineer)
- Determinism failures / seed issues / replay divergence on goldens → baseline-warden + determinism-engineer
- Content fixes (IDs, briefings, triggers, OOB sanity in scenario files) → scenario-content-specialist (this agent, gated Phase 4)
- Golden baseline impact → baseline-warden (coordinate; never edit goldens here)

---

## Next Steps

1. Route findings per table.
2. For content-only fixes: enter Phase 4 (gated).
3. Re-run `/scenario-audit [affected] --quick` (then full) after any changes.
4. For golden scenarios: pair with `/replay-verify [name]` before/after.
5. Include this report (or link) in release gate evidence.
```

**Verdict keywords**: PASS (all checks clean, no BLOCKERs/HIGHs), PASS-WITH-FINDINGS (BLOCKER-free but MEDIUM/HIGH present), FAIL (one or more BLOCKERs), NOT RUN (runner/Cli unavailable for one or more checks — record evidence from prior runs; does not auto-FAIL).

Present the executive summary, per-scenario table, and routing.

Ask: "May I write this report to `production/qa/scenario-audit-[date].md`?"

Write only after explicit approval (use AskUserQuestion for the decision if needed).

## Phase 4: Fix loop (gated, content only)

**Gate**: Enter only after user explicitly approves via AskUserQuestion or "yes" to "Enter content fix loop for failing scenarios?" Never auto-enter.

**Scope contract (hard)**: ONLY `data/scenarios/**` and `assets/data/scenarios/**`. NEVER edit `src/**`, `tests/regression/**` (goldens), DB files, or any non-scenario content. Violations abort and escalate.

**Process (per failing scenario, batch where safe):**

1. Isolate failing checks from Phase 2 for that scenario only.
2. Propose minimal content edit(s) (e.g., correct ID spelling, add missing zone ref in JSON, align briefing text to actual triggers).
3. Show proposed change (diff or before/after snippet).
4. Ask: "May I write this fix to `data/scenarios/[name].policy.json`?" (list every file for multi-file packs).
5. On approval: use Write/Edit.
6. **Re-run checks**: Immediately re-execute Phase 2 checks (targeted: the failed ones first, then full or --quick) for the edited scenario. Capture new evidence.
7. If still failing: iterate (new proposal + ask). If clean: mark fixed for that scenario.
8. After batch: present updated table snippet. Ask again before writing any updated report section or full re-report.

**NOT RUN handling (mirrors replay-verify)**: If Cli or replay runner unavailable during re-run, record as NOT RUN for that check; do not treat as PASS. Require user confirmation of local/CI results before advancing verdict.

**Hybrid + GitNexus in loop**: After each content edit, run GitNexus detect_changes (planning only) to confirm scope respected. Re-invoke Cli validate + simulate_sample.

**Never**: Do not propose or apply sim logic, golden updates, or DB changes here. Route those.

## Dispatching Parallel Agents

Use the dispatching-parallel-agents superpowers pattern (see `dispatching-parallel-agents/SKILL.md` and dispatch-sprint patterns) when N > 2 scenarios are in scope (e.g., `all`, or explicit list of 3+).

**Pattern**:
- Identify independent per-scenario domains: each scenario file is a self-contained, independent domain with zero shared mutable state or cross-scenario data dependencies in the audit.
- Coordinator (main /scenario-audit run) performs inventory (Phase 1 + GitNexus discovery), then for N>2 dispatches.
- Spawn focused `Task` sub-agents, each with **isolated context** containing ONLY one scenario path + its minimal metadata (format note, last commit).
- Sub-task prompt contract (exact output requirement): "return structured findings for this scenario" (no report writing, no other scenarios, no global state).
- Sub-agents run checks in parallel (limited by available context/tools).
- Coordinator aggregates the returned structured blocks into the master table, applies overall verdict, handles routing.
- For N ≤ 2: run serially (no dispatch overhead).

**Explicit rule**: "Use dispatching-parallel-agents when N>2."

**Example sub-task prompt** (passed to Task):
```
You are an isolated scenario-audit worker. Your entire scope is ONE scenario:

scenario_path: data/scenarios/baltic-patrol.policy.json
quick: false
checks: all (or 1-2 if --quick)

Instructions:
- Perform ONLY Phase 2 checks for this single scenario file.
- Use Cli (dotnet ... scenario_validate --path ...), direct JSON read for IDs/provenance/briefing, invoke replay-verify only if golden-backed for this scenario.
- GitNexus discovery is optional/parent-provided; do not re-run broad impacts unless needed for this file.
- Return ONLY structured findings using this exact contract (no prose outside blocks, no other scenarios, no file writes):

**SCENARIO_FINDINGS_START**
Scenario: baltic-patrol.policy.json
Format: v2
Checks Passed: 7/7
BLOCKERs: 0
Verdict: PASS
Evidence: |-
  Cli: exit 0
  IDs: 42/42 resolved (no orphans)
  Determinism: seed=42 declared; replay-verify PASS (A==B, A==golden, hash=0x...)
  Briefing: matches (victory triggers present)
  GitNexus note: 12 upstream consumers in harnesses
**SCENARIO_FINDINGS_END**

Do not write reports. Do not edit. Isolated one-scenario context only. Stop after returning the block.
```

Coordinator parses the **SCENARIO_FINDINGS_*** blocks from each Task result, collates, then proceeds to Phase 3 presentation + "May I write".

Sub-agents must not share state (different Task invocations, no common temp files outside their scenario).

## Edge Cases, Collaborative Protocol, Escalation Table, Next Steps

**Edge cases**:
- Cli unavailable / NOT RUN: fall back to JSON parse + manual catalog lookup (via Bash or read catalog fixtures); record "Cli: NOT RUN (reason)" per check. Verdict computed from available evidence; mirror replay-verify NOT RUN handling — never auto-PASS or auto-FAIL solely on NOT RUN.
- No declared seed: treat as HIGH (or BLOCKER if golden-backed).
- Golden scenario divergence: BLOCKER; hand to baseline-warden + determinism-engineer + re-run /replay-verify.
- Mixed verdicts across scenarios: overall = FAIL if any BLOCKER anywhere; else PASS-WITH-FINDINGS if any non-BLOCKER findings.
- Empty inventory: report "No scenarios matched" with overall PASS (vacuously).
- Format version unknown: note in Format column; still attempt checks 2+.
- `--quick` + determinism/golden: still note that full determinism was not checked.

**Collaborative Protocol** (exact match to determinism-audit + replay-verify + scenario-content-specialist + stub):
- "May I write" before any Write (report or fixes).
- Peers / approvers for "May I write" + approval before Write: scenario-content-specialist (self for content), baseline-warden (goldens/determinism), database-intelligence-lead (DB), c-sharp via /bug-report.
- Show draft/summary first; list every file for multi-scenario or multi-fix.
- Use AskUserQuestion for decisions (enter fix loop? resolve drift/DRIFT cases? confirm NOT RUN interpretation?).
- Scope only scenario content: re-state in every Phase 4 proposal.
- Re-run checks after fixes: mandatory before claiming improvement.
- Never auto-fix or auto-write.
- "Present ... Ask: May I write this report to production/qa/scenario-audit-[date].md ?"

**Escalation table** (from stub + agent + determinism/replay patterns):

| Situation | Route to |
|-----------|----------|
| DB gaps, missing entities, provenance contradictions in catalog | database-intelligence-lead |
| Cli defects, validate failures, command surface / round-trip bugs | /bug-report (c-sharp-engineer) |
| Determinism failures, missing seed on golden, replay divergence | baseline-warden + determinism-engineer |
| Content fixes (scenario JSON only) | scenario-content-specialist (gated Phase 4) |
| Golden baseline or fingerprint impact suspected | baseline-warden (coordinate; do not edit goldens) |
| Attempt to edit src/** or goldens | technical-director (abort, policy violation) |
| Scope creep beyond scenario content | producer / technical-director |
| Ambiguous victory/briefing intent | creative-director or military-research-specialist |
| NOT RUN on critical gate check | user confirmation required (local/CI); do not gate on it |

**Next steps** (after report or loop):
- Route per table.
- Re-audit affected scenarios post-fix (`/scenario-audit [path]`).
- Pair golden scenarios with `/replay-verify`.
- Include `production/qa/scenario-audit-*.md` (or latest) + GitNexus notes in release / Polish gates.
- For large packs: use dispatching (N>2) then serial closeout.
- Update scenario-policy-ids.md or catalog if DB issues surfaced.

## Examples of Invocation and Sample Output Table

**Invocation examples**:
- `/scenario-audit data/scenarios/baltic-patrol.policy.json`
- `/scenario-audit all`
- `/scenario-audit all --quick`
- `/scenario-audit baltic-v*-patrol*.policy.json`
- `/scenario-audit data/scenarios/baltic-patrol.policy.json data/scenarios/baltic-patrol-comms.policy.json`

**Sample per-scenario output table** (embedded in Phase 3 report + conversation):

| Scenario | Format | Checks Passed | BLOCKERs | Verdict | Evidence |
|----------|--------|---------------|----------|---------|----------|
| baltic-patrol.policy.json | v2 | 7/7 | 0 | PASS | Cli=0; 42 entities resolved; seed=42; replay PASS (hash match); briefing OK; GitNexus 30+ harness refs |
| baltic-patrol-mine-transit-hazard.policy.json | v2 | 5/7 | 1 | FAIL | BLOCKER (check 1): Cli exit=1 (missing zone ref in trigger); HIGH (check 3): hand-typed speed override vs DB; Evidence: validate JSON report + catalog diff |
| baltic-v3-patrol.policy.json | v2 | 6/7 | 0 | PASS-WITH-FINDINGS | Cli=0; IDs OK; seed present; MEDIUM (check 5): briefing lists "destroy all" but only 2/3 victory triggers present; LOW balance smoke OK |

**Overall Verdict: FAIL** (1 BLOCKER)

(Then: routing block + "May I write this report to `production/qa/scenario-audit-2026-07-05.md`?")

For NOT RUN sample row: `... | 4/7 | 0 | NOT RUN | Cli: NOT RUN (dotnet unavailable); JSON parse passed; IDs manual 38/42; determinism: confirmed via prior replay-2026-*.md` |
