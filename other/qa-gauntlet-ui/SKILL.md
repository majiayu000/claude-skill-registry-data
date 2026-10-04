---
name: qa-gauntlet-ui
description: >
  Game UI Smoke/Pressure track for QA Gauntlet: headless PlayMode + C2/Presentation
  filters, ReplayGolden, Unity Editor C2 Play Mode signoffs (×5), artifact AAR.
  Failures route to /qa-gauntlet-remediation + UCA. Manual UAT stays on /team-qa /
  /smoke-check. Use when /qa-gauntlet-ui, /team-qa-gauntlet --mode ui|ui-smoke,
  or the user asks for "gauntlet UI", "C2 Play Mode pressure", or "UI smoke gauntlet".
argument-hint: "[--run-id <id>] [--unity-version 6000.3.14f1] [--skip-signoff]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task
---

# QA Gauntlet UI — Smoke / Pressure (not UAT)

**Owns:** automated game-UI gates for C2 chrome / presentation Surfaces.  
**Does not own:** headless Demo ladder oracles (`/qa-gauntlet`), forge/calibrate/stress
sim axes, or **manual UAT** (`/team-qa`, `/smoke-check` human batches).

**Manual UAT → `/team-qa`** (and `/smoke-check` for sprint hand-off). Do not invent a
second human click-through loop here.

## When to invoke

| Trigger | Action |
|---------|--------|
| `/team-qa-gauntlet --mode ui` or `ui-smoke` | This skill (full package) |
| `/qa-gauntlet-ui` | This skill |
| Presentation defect mid-ladder | Still `/qa-gauntlet-remediation` + UCA — this skill is proactive gates |

## Hard invariants

- **ZERO-touch** `DelegationBridge.cs`; Baltic v2 hash `17144800277401907079` preserved.
- Prefer headless `dotnet test` before Editor Play Mode; UI is a **client** (ADR-010).
- Script-first: LLM never overrides a failed signoff PASS line or `dotnet` non-zero exit.
- On any red gate → dispatch **`/qa-gauntlet-remediation`** (UCA / pr-finish required for
  UnityAdapter / Presentation / C2 Surfaces). Cite ADR-010 §2–3, ADR-007, ADR-001.

## Run identity

```text
RUN_ID = <arg> | gauntlet-$(date +%Y%m%d-%H%M)-ui
RUN_DIR = production/qa/gauntlet/<RUN_ID>/
```

Create at start: `ui/`, `ui/signoff/`, `run-id.txt`, `git-sha.txt`, `branch.txt`,
`manifest.yaml` (fill verdict at end), `AAR.md` (from template below).

## Package (hard-coded — do not freestyle)

### 1) Headless UI / C2 / Presentation suite (“118-style” filter)

```bash
set -euo pipefail
export PATH="${HOME}/.dotnet:${PATH}"
UA_TEST="src/ProjectAegis.Delegation.UnityAdapter.Tests/ProjectAegis.Delegation.UnityAdapter.Tests.csproj"

require_passed_floor() {
  local log="$1" min="$2" label="$3"
  local passed
  passed="$(grep -Eo 'Passed:[[:space:]]*[0-9]+' "$log" | tail -1 | grep -Eo '[0-9]+' || true)"
  if [ -z "$passed" ]; then
    echo "FATAL: could not parse Passed count from ${log} (${label})" >&2
    exit 1
  fi
  if [ "$passed" -lt "$min" ]; then
    echo "FATAL: ${label} passed=${passed} floor=${min}" >&2
    exit 1
  fi
}

dotnet test "$UA_TEST" \
  --filter "FullyQualifiedName~PlayModeSmoke|FullyQualifiedName~Presentation|FullyQualifiedName~C2|FullyQualifiedName~MapPlaceholder|FullyQualifiedName~MapCanvas|FullyQualifiedName~UnityCsharpScriptHygiene|FullyQualifiedName~Panel|FullyQualifiedName~MessageLog|FullyQualifiedName~SensorC2|FullyQualifiedName~UiIa" \
  -v minimal --nologo | tee "${RUN_DIR}/ui/dotnet-ui-suite.log"
require_passed_floor "${RUN_DIR}/ui/dotnet-ui-suite.log" 118 "UI/C2/Presentation suite"

dotnet test "$UA_TEST" \
  --filter "FullyQualifiedName~UiIa" \
  -v minimal --nologo | tee "${RUN_DIR}/ui/dotnet-uiia.log"
require_passed_floor "${RUN_DIR}/ui/dotnet-uiia.log" 11 "UiIa oracles"
```

Floor: **0 failures** and **mandatory discovery floors** (zero-match is FAIL). Combined
suite ≥118 passed (PlayModeSmoke family included; AGENTS.md PlayModeSmokeHarness ≥20/20).
Dedicated `FullyQualifiedName~UiIa` ≥11. Layout/visuals and manual UAT are not covered.

### 2) ReplayGolden family

```bash
dotnet test "$UA_TEST" \
  --filter ReplayGolden -v minimal --nologo | tee "${RUN_DIR}/ui/replay-golden.log"
require_passed_floor "${RUN_DIR}/ui/replay-golden.log" 6 "ReplayGolden"
```

Floor: **0 failures** and **≥6 passed** (AGENTS.md ReplayGolden **6/6**). Reference total
for the family may be higher (e.g. 17) — never treat a 0-discovery green as PASS.

### 3) Unity Editor C2 Play Mode signoffs (×5)

Editor: Hub version **must** match `unity/ProjectAegis/ProjectSettings/ProjectVersion.txt`
(pinned `6000.3.14f1`). Default path Linux: `$HOME/Unity/Hub/Editor/<ver>/Editor/Unity`.

```bash
VER="$(awk -F': ' '/^m_EditorVersion:/{print $2; exit}' unity/ProjectAegis/ProjectSettings/ProjectVersion.txt)"
UNITY="${UNITY:-$HOME/Unity/Hub/Editor/${VER}/Editor/Unity}"
PROJ="unity/ProjectAegis"
for METHOD in RunBatch RunClassifyBatch RunDoctrineBatch RunImportBatch RunBeginExecutionBatch; do
  set +e
  timeout 300s "$UNITY" -batchmode -nographics \
    -projectPath "$PROJ" \
    -executeMethod "ProjectAegis.Unity.Editor.C2PlayModeSignoffBatchRunner.${METHOD}" \
    -logFile "${RUN_DIR}/ui/signoff/${METHOD}.log"
  status=$?
  set -e
  if [ "$status" -ne 0 ]; then
    echo "FATAL: Unity ${METHOD} exit ${status}" >&2
    exit "$status"
  fi
  grep -q 'C2PlayModeSignoffBatchRunner PASS:' "${RUN_DIR}/ui/signoff/${METHOD}.log" || exit 1
done
```

| Method | Scenario (signoff) |
|--------|-------------------|
| `RunBatch` | `baltic-patrol-comms` |
| `RunClassifyBatch` | `baltic-patrol-classify` |
| `RunDoctrineBatch` | `baltic-patrol-mission-roe` |
| `RunImportBatch` | `baltic-patrol-classify` |
| `RunBeginExecutionBatch` | `baltic-patrol-classify` |

`--skip-signoff` only when Editor unavailable — mark AAR **BLOCKED (signoff)** and
do not claim full UI PASS.

### 4) Invariants snippet → `ui/invariants.txt`

- `grep -r 17144800277401907079 tests/ data/` (hits > 0)
- Confirm no intentional `DelegationBridge.cs` edits in the working tree for this run

### 5) Failure routing

| Failure | Route |
|---------|--------|
| `dotnet` UI suite / ReplayGolden red | `/qa-gauntlet-remediation` (TDD); UCA if Surface is presentation |
| Signoff `FAIL` / `SIGNOFF_ERROR:` / missing PASS | Same; prefer reproduction via failing headless test first |
| Compile / plugin DLL | Refresh `tools/copy-delegation-assemblies.sh`, re-run; still remediation if code fix |
| Manual visual/feel gaps | **Stop** — hand off to `/team-qa` / `/smoke-check` (not this skill) |

## AAR template

Write `production/qa/gauntlet/<RUN_ID>/AAR.md`:

```markdown
# Gauntlet UI-track AAR — <RUN_ID>

**Team:** `/team-qa-gauntlet --mode ui` → `/qa-gauntlet-ui`
**Verdict:** PASS | FAIL | BLOCKED

| Gate | Result |
|------|--------|
| Headless UI/C2/Presentation suite | N/N |
| IA oracles (`UiIa`) | N/N |
| ReplayGolden filter | N/N |
| C2 signoff ×5 | PASS/FAIL each |
| Hash / DelegationBridge | OK / note |
| Remediation / UCA | N/A \| dispatched `<ids>` |

**Manual UAT:** not in scope — use `/team-qa` / `/smoke-check`.
**Ladder:** not run — use `/qa-gauntlet` / `--mode ladder`.
```

Also write `manifest.yaml` with `track: game-ui`, gate exits, and `remediation_required`.

## Success

- All automated gates green **or** defects filed + `/qa-gauntlet-remediation` invoked.
- Artifacts under `production/qa/gauntlet/<RUN_ID>/`.
- No claim of manual UAT completion.
- No edits to `/qa-gauntlet` ladder contract for UI purposes.

## See also

- `/team-qa-gauntlet` — orchestrator (`--mode ui` / `ui-smoke`)
- `/qa-gauntlet-combat-ui` — engage/kill presentation (`--mode combat-ui`); not Slice B
- `/qa-gauntlet-remediation` — Phase D + UCA
- `/qa-gauntlet` — headless sim ladder (separate)
- `/team-qa`, `/smoke-check` — **manual UAT / sprint smoke**
- Reference run: `production/qa/gauntlet/gauntlet-20260817-1626-ui/`
