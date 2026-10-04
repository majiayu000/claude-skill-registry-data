---
name: auto-factory
description: End-to-end auto-factory driver — picks up beads + GH issues tagged factory, dispatches coders to drive worldai PRs to /green + /advice + /er, runs verifier ticks, repeats until done. Designed to work even when GH API is rate-limited (falls back to beads-only).
---

# /auto-factory — one end-to-end drive tick

## Invocation boundary: repair versus running `/af`

A request to make `/af` work is a factory-infrastructure repair request, not a
product run through `/af`. It authorizes normal scoped coding, testing, and
deployment of factory infrastructure, including
direct or delegated coding when needed. Keep intake quiesced and isolate repair
changes in their own worktree/branch; repair evidence does not count as pilot
evidence. When the user invokes `/af` to process a product or pilot task, the
repository's zero-direct-work rule applies: monitor the factory and use its bead to
daemon to worker path, without hand-driving product or pilot branches.

**Interactive Developer Override**: This zero-direct-work rule applies strictly
to hands-off autonomous `/af` goal runs. When the operator directly commands you
to code, repair, unpark beads, re-run gates, drive verifications, or finish tasks
(e.g., "you are coding", "keep going and finish 1-4", "repair this"), you are in
active engineering mode. Act with full authority to diagnose, unpark, fix, run
evidence commands, and drive the task to completion. Never refuse a direct
interactive coding instruction by misclassifying it as a hands-off `/af` run.

The auto-factory is the agent-orchestrator-style system that drives worldai PRs to merge. This skill is its orchestrator: it picks up work (beads + GH issues), dispatches coder subagents, runs verifier ticks, and iterates until gates pass.

## 0. Execution host + Bead authority preflight

Distinguish host capability, service liveness, Bead freshness, integrity, and authority:
- **Host capability**: The invocation host is the candidate factory host. Linux with a user systemd supervisor is the only supported factory execution platform; macOS is an operator client (do not start LaunchAgents, local daemons, or local AO workers on Darwin). Continue factory intake on the candidate host only when a local factory supervisor checkout is present and its daemon configuration supports `target_repo` (as the top-level target or in `[repos]`). An unsupported host stops intake there; continue canonical Linux diagnosis/recovery within authorized scope via `/linux`. The repository's own `CLAUDE.md` names which Linux host is canonical for that repository; this skill never hardcodes one.
- **Service liveness**: Service liveness is an observational check (`SERVICE_ACTIVE`), not an entry barrier for inspecting configuration or executing authorized recovery. A stopped service gates automated dispatch, but does NOT gate reading supervisor metadata/configuration nor authorized recovery.

Before any intake mutation, resolve the exact Bead DB and checkout from the
local factory supervisor. Bind `br`, the overlay, and any manual tick to
that same installation; ambient `br where` discovery is not authority. The
resolved Linux user systemd supervisor is the canonical adapter.
Preflight `where`, `sync`, and `doctor` invocations must use both
`--no-auto-flush` and `--no-auto-import` with `--db "$BR_DB"` to disable
implicit export/import. macOS rejects intake outright and routes operational
control, diagnostics, and recovery to the repository's configured Linux factory
host via SSH (`/linux`). Any other host rejects intake unless it is explicitly
registered through both `DARK_FACTORY_ROOT` and `DARK_FACTORY_BR_DB`; neither
value is ever inferred:

```bash
case "$(uname -s)" in
  Linux)
    unit=ai.dark-factory.daemon.service
    # Observational check: service liveness gates dispatch, not supervisor reading or recovery
    SERVICE_ACTIVE=false
    if systemctl --user is-active --quiet "$unit"; then
      SERVICE_ACTIVE=true
    fi
    FACTORY_ROOT="$(systemctl --user show "$unit" --property=WorkingDirectory --value)"
    BR_DB="$(systemctl --user show "$unit" --property=Environment --value |
      tr ' ' '\n' | sed -n 's/^DARK_FACTORY_BR_DB=//p' | tail -1)"
    ;;
  Darwin)
    # macOS is an operator client; Linux systemd is the sole factory execution platform.
    # Never load or start the `ai.dark-factory.af-tick` LaunchAgent, a local
    # daemon, or local AO workers on Darwin. An unsupported host stops intake
    # here; route diagnosis/recovery to the configured Linux factory host via SSH.
    echo "macOS is an operator client: no local factory launches on Darwin; route to the configured Linux factory host via SSH (/linux)" >&2
    exit 1
    ;;
  *)
    # Another registered Linux host may supply explicit overrides instead of
    # systemd discovery. Both must be set; neither is inferred.
    FACTORY_ROOT="${DARK_FACTORY_ROOT:?registered factory checkout required}"
    BR_DB="${DARK_FACTORY_BR_DB:?registered factory Bead DB required}"
    ;;
esac
[ -n "$BR_DB" ] && [ "${BR_DB#/}" != "$BR_DB" ] && [ -f "$BR_DB" ] || exit 1
CONFIG="$FACTORY_ROOT/config/daemon.toml"
[ -f "$CONFIG" ] || exit 1
if [ -z "${TARGET_REPO:-}" ]; then
  TARGET_REPO="$(python3 - "$CONFIG" <<'PY'
import sys, tomllib
from pathlib import Path

target = tomllib.loads(Path(sys.argv[1]).read_text()).get("target_repo")
if not isinstance(target, str) or not target:
    raise SystemExit("factory config has no default target_repo")
print(target)
PY
)"
fi
python3 - "$CONFIG" "$TARGET_REPO" <<'PY'
import sys, tomllib
from pathlib import Path

cfg = tomllib.loads(Path(sys.argv[1]).read_text())
target = sys.argv[2]
if target != cfg.get("target_repo") and target not in cfg.get("repos", {}):
    raise SystemExit(f"factory does not support target_repo: {target}")
PY
export BR_DB CONFIG TARGET_REPO
command -v br >/dev/null
br --db "$BR_DB" where --no-auto-flush --no-auto-import
br --db "$BR_DB" sync --status --json --no-auto-flush --no-auto-import
# First pass only. `--quick` cannot prove reconciliation safety (see below).
br --db "$BR_DB" doctor --quick --no-auto-flush --no-auto-import
# Authoritative integrity read; this is the one that gates intake mutation.
br --db "$BR_DB" doctor --robot-triage --json --no-auto-flush --no-auto-import
```

Distinguish Bead freshness, integrity, and authority:
- **Integrity Coverage vs. Quick Checks**: `--quick` skips count and recoverable anomaly detectors and cannot prove reconciliation safety. Fresh Linux evidence reveals that `br doctor --quick` can misleadingly report healthy while real store discrepancies exist; furthermore, full diagnostics (such as `--repair --dry-run --json` on an isolated copy) may return `report.ok=true` and `verified=true` yet reveal `workspace_health=degraded` and a severe ID set / count mismatch (`db_jsonl_id_set_mismatch`, e.g. 681 in DB vs 1100 in JSONL). Inspect actual findings, `workspace_health`, ID sets, and count anomalies rather than relying on boolean `ok`, `verified`, or freshness indicators alone.
- **Freshness vs. Authority & Reconciliation**: `db_newer` alone with known supervisor-selected authority (`$BR_DB`) indicates supported reconciliation rather than an ambiguous conflict, not requiring operator intervention—ONLY after full read-only diagnostics (`doctor --robot-triage --json`) confirm no missing-record, ID-set mismatch, or integrity conflicts. An existing known-authority DB-newer canary remains automatic to reconcile if full diagnostics are clean. Reconcile it via the supervisor-bound supported Beads sync workflow using installed command help (`br sync --help` / `br --help`) without inventing syntax; never force export.
- **Integrity Errors & Conflicting Representations**: Integrity errors, degraded workspace health, missing records, or conflicting representations (e.g. `db_jsonl_id_set_mismatch`, both `jsonl_newer` and `db_newer` true with contradictory states, corrupt records, or duplicate references) stop unsafe intake mutation (`br create`, `br update`) and dependent dispatch.
  1. Preserve backups before changes and preserve all missing records. Never force export, never perform raw Beads mutations on `beads.db` or `.jsonl`, and never discard missing records.
  2. Keep investigation and isolated recovery continuing when unsafe intake mutation is blocked; blocking an unsafe write does not abort authorized diagnostics or safe recovery exploration.
  3. Inspect the recovery candidate via supported Beads workflow. When the supported reader fails (e.g. `br` fails or crashes on malformed interchange or duplicate references), perform bounded read-only copy forensics on an isolated copy with secrets excluded.
  4. Validate the recovery candidate before promoting it to authoritative.
  5. Ask the operator only for a specific conflict with materially different valid resolutions that cannot be resolved from evidence and existing authority.
  6. Continue independent safe diagnostic and repair work when one mutation is blocked.
A GitHub fallback does not authorize a write to an ambiguous or damaged Bead store.

Intake is a two-phase operation: create without the `factory` label, prove that
the selected factory can read the new Bead from the same store, and only then
apply the label:

```bash
bead_id="$(br --db "$BR_DB" create "<title>" --body "<body>" --json | jq -r '.id')"
br --db "$BR_DB" show "$bead_id" --json
br --db "$BR_DB" update "$bead_id" --add-label factory --json
br --db "$BR_DB" show "$bead_id" --json
br --db "$BR_DB" list --status open --label factory --json
```

For an existing Bead, perform the same read proof before adding the label. If
the read or label verification fails, stop the failed intake action and dependent
dispatch, but continue authorized diagnosis/recovery. After labelling, check that
`$H list QUEUED` contains the Bead. Report `QUEUED` only when the overlay has
adopted it; otherwise report `intake verified; adoption pending`.

The Bead body must remain below the AO 4096-character task-description limit.

### 0a. Load contract + config

Only after the execution-host preflight passes:

```bash
cd "$FACTORY_ROOT"
H="$FACTORY_ROOT/daemon/factory-overlay.sh"
$H init  # idempotent
```

The overlay harness `daemon/factory-overlay.sh` is the canonical executable spec for the auto-factory state machine (restored from `e60b5a31b~1:daemon/factory-lite-harness.sh` and extended in PR #167). All sqlite3 mutations to `~/.dark-factory/daemon-cxdb.sqlite` flow through it. Subcommands: `init`, `intake-upsert`, `route-record`, `capacity`, `dispatch-record`, `pr-opened`, `autonomy-tick`, `gate-assessment`, `prev-gate-assessment`, `ready`, `reroll-verdict`, `park`, `park-duplicate`, `bead-closed-check`, `tick-summary`, `recover-held`, `unstick-dispatching`, `redrive-pr`, `list`.

> Historical note: the original `daemon/factory-lite-harness.sh` and `daemon/run-factory-lite.sh` were removed in commit `e60b5a31b` (2026-07-05, jleechan-xrdx). The decommissioned factory-lite-coder / factory-lite-verifier skills are gone; their protocols are now inline in this skill + factory-af-tick.sh + factory-overlay.sh.

## 1. Intake (work pickup)

Pick up work from BOTH sources (bead store + GitHub):

### 1a. Bead pickup (primary)
```bash
br --db "$BR_DB" list --status open --label factory --json
```

For each bead: read body, detect `drive-existing-pr` mode (fields `existing_pr`, `existing_branch`, `target_repo`). If present, this bead drives an existing PR — coder must push to existing branch via `git push wa <existing_branch>`. Otherwise default to new-work (create `factory/<bead>-r<attempt>` branch).

### 1b. GitHub pickup (fallback when beads empty OR to capture fresh work)
```bash
gh issue list --repo "$TARGET_REPO" --label factory --state open --json number,title,body --limit 20
```

If GH API rate-limited (returns error), skip this step — beads-only mode. Log the fallback: `[intake] GH API rate-limited, beads-only mode`.

For each GH issue, treat it as a Bead: read the body, create it without the
`factory` label (other non-routing labels are allowed), read it back through
`br --db "$BR_DB" show "$bead_id" --json`, then add the factory label with
`br --db "$BR_DB" update "$bead_id" --add-label factory --json`. Continue with
Bead pickup only after the same-store verification succeeds.

### 1c. Drive-existing-pr detection
A bead/issue has `drive-existing-pr` mode if body contains ALL of:
- `existing_pr: <N>`
- `existing_branch: <name>`
- `target_repo: <owner>/<name>`

The coder MUST push to the existing branch via `git push <remote> <existing_branch>` (NOT create a new factory/* branch). This is the general-purpose pattern.

## 2. Route each QUEUED bead

`$H list QUEUED` → for each bead, use LLM judgment to pick `SMALL_PATH` (single-file fix) vs `STANDARD_PATH` (multi-file/architecture). Record via `$H route-record <bead_id> <VERDICT> "<note>"`.

## 3. Capacity

`free=$($H capacity)` — `min(max_workers - active, max_batch)`. If 0, skip to step 7.

## 4. Dispatch — PARALLEL coder subagents

Select up to `$free` routed QUEUED beads (file-overlap rule: serialize if any share a mutable file). For each selected bead:

### Drive-existing-pr mode
```bash
$H dispatch-record <bead_id> <existing_branch>  # e.g., fix/quota-banner-modal-cta-7945
```

### New-work mode (default)
```bash
$H dispatch-record <bead_id> factory/<bead_id>-r<attempt>
```

**Spawn ALL selected coders in ONE message** — multiple `Agent` tool calls, each `subagent_type: minimax-pair-coder`, `run_in_background: true`. Parallel dispatch is the point.

Each coder prompt MUST include:
- Bead id + full title/description
- Drive-existing-pr vs new-work instruction (and the existing_branch/existing_pr/target_repo fields if drive mode)
- The exact push command (`git push wa <branch>` for worldai, `git push origin <branch>` for dark-factory)
- An isolation requirement (worktree at `/tmp/<bead>-wt`; remove after push; never check out branches in the shared repo working tree)
- A clear "do NOT open new PR / do NOT merge" rule

## 5. (reserved)

Step number kept stable.

## 6. Detect PRs opened/updated by dispatched coders

For every row in `$H list DISPATCHED`:
```bash
$H bead-closed-check <bead_id>  # guards against direct bead closure
```

For drive-existing-pr beads, check the existing PR branch for new commits:
```bash
gh pr view <existing_pr> --repo <target_repo> --json headRefOid,mergeable,statusCheckRollup,reviewDecision,comments
```

If new commits detected → `$H pr-opened <bead_id> <existing_pr> <url>`.

For new-work beads, check for new PR:
```bash
gh pr list --repo "$TARGET_REPO" --head "factory/<bead_id>-r<attempt>" --state open --json number,url
```

## 7. Verifier tick (gate assessment)

For every ATTESTED bead (PR opened/updated), run the canonical 8 gates as defined in
`daemon/src/verifier.rs::GateName` (`Ci, NoConflicts, CodeRabbitApproved, BugbotClean,
CommentsResolved, EvidenceFloor, Skeptic, VacuousRedGreen`). The `code_standards` and `zfc`
checks are optional advisory reviews — they are NOT required keys in the gate-assessment JSON
and their absence never blocks `all_green`. If you DO record them, they participate like any
recorded gate: a `fail` verdict blocks `all_green` and routes through the same `reroll-verdict`
fix loop. See bead jleechan-1gft for promoting them to required `GateName` gates in the Rust
verifier. Gate 8 (`VacuousRedGreen`, issue #387 / bead jleechan-ijod) was added in
PR #389 / r5 commit 175c6ad — runtime vacuous-test detector verdict.

| Verdict  | Meaning                                                                | Gate result     |
|----------|------------------------------------------------------------------------|-----------------|
| `pass`   | Reviewer returned positive evidence; ready to advance                  | counts toward `all_green` |
| `warn`   | Reviewer returned mixed evidence; non-blocking, surface in next tick   | counts toward `all_green` |
| `fail`   | Reviewer returned negative evidence; reroll required                   | forces reroll-verdict |
| `unknown`| Reviewer could not gather evidence yet; wait for the next tick         | blocks `all_green` |

`all_green=true` iff every gate returned `pass` or `warn`. `fail` routes through
`reroll-verdict → HUMAN_HELD → recover-held → QUEUED` — the bounded fix loop
shared with the original 8 gates; **no parallel implementation**. `unknown`
defers to the next tick rather than racing to READY.

```bash
gh pr view <pr> --repo "$TARGET_REPO" --json headRefOid,mergeable,reviewDecision,statusCheckRollup
gh pr checks <pr> --repo "$TARGET_REPO" --json name,state,conclusion
```

Each gate is a model-delegated review (NOT keyword routing); the verifier
dispatches them as subagents / `claude --print /<slash>` / `codex exec --yolo`
against the PR diff. The overlay only records verdicts — the pass/warn/fail
decision is the model's, not ours.

Assess each gate:
- ci_green: every check `conclusion=success` (or state=SUCCESS)
- no_conflicts: `mergeable=MERGEABLE`, mergeStateStatus not DIRTY
- coderabbit: latest `coderabbitai[bot]` review APPROVED
- bugbot: zero error-severity `cursor[bot]` comments
- comments_resolved: every reviewThread `isResolved=true`
- evidence_review: 5-criterion /er rubric pass
- skeptic: parallel minimax cold review
- code_standards: dispatch `code-standards` review (overrides `~/.claude/skills/code-standards/SKILL.md` or repo-local `.claude/skills/code-standards/SKILL.md`) — pass/warn only when every claimed pass carries file/line evidence per the lane's Iron Law; fail on bare assertions without file/line proof
- zfc: dispatch `zfc` review against `.claude/skills/zero-framework-cognition/SKILL.md` + `.claude/skills/root-cause-first/SKILL.md` — pass/warn only when no banned-pattern scan finds a violation; fail otherwise

Each gate's verdict value in `gates_json` is either a plain string OR a
structured object so reviewers can audit the verdict without re-running the
model:

```json
"zfc": "pass"                                              /* shorthand */
"zfc": {"verdict": "fail",                                  /* structured */
        "evidence": [{"path": "daemon/factory-overlay.sh",
                      "line": 201,
                      "msg": "keyword blacklist enforced in app code"}]}
```

Record via `$H gate-assessment <bead_id> <pr> '<gates_json>'`. The 7-key JSON
schema (strict, matching `daemon/src/verifier.rs::GateName`) is enforced by `factory-overlay.sh`:

```json
{"ci_green":"pass","no_conflicts":"pass","coderabbit":"pass",
 "bugbot":"pass","comments_resolved":"pass","evidence_review":"pass",
 "skeptic":"pass"}
 // optional advisory keys — not required; if present, a fail still blocks:
 // "code_standards":"pass","zfc":"pass"
```

Legacy aliases `"green" → "pass"`, `"red" → "fail"` are still accepted so
existing test fixtures don't have to migrate in lockstep, but new callers
should use the pass/warn/fail vocabulary.

All-green (`all_green=true` on stdout line 1) → `$H ready <bead_id> <pr>`
(terminal state; verifier stops driving). Any-fail → `$H reroll-verdict
<bead_id> <pr> <in_place_fixable|reroll_worthy> "<rationale>"`. The `cooldown_ready`
line indicates whether the prior GATE_ASSESSMENT for this PR was a `false`
result (cooldown handling is unchanged from the original 7-gate design).

## 8. Autonomy time-box

`$H autonomy-tick $ELAPSED_SECS` — increment actives, warn at 80%, park over-box.

## 9. End-of-tick summary & Conversation Audit

- Inspect live coding CLI conversations on the selected factory host to verify authentic agent progress before reporting status (see `.claude/skills/factory-status/SKILL.md`).
- `$H tick-summary coder` (or verifier if you ran verifier steps).

## NEVER

- NEVER report progress based on database flags alone without auditing live CLI transcripts.
- NEVER run sqlite3 directly against the CXDB — every mutation via `$H`.
- NEVER force-push or push directly to `base_branch`.
- NEVER run `gh pr merge` — dispatch is not the merge authority.
- NEVER delete a branch.
- NEVER spawn a coder the harness refused to `dispatch-record`.
- NEVER dispatch two beads with overlapping files in the same tick.
- NEVER keyword-route — routing is model judgment (ZFC).
- NEVER await coder subagents inside the tick — spawn parallel, in background.
- NEVER push to a new `factory/*` branch when the bead body has drive-existing-pr fields — push to the existing branch.

## Failure modes & recovery

- **GH API rate-limited**: skip GH pickup, use beads-only mode; continue.
- **Daemon DOWN** (no auto-factory tick loop running): inspect the selected
  host's local supervisor (`systemctl --user status ai.dark-factory.daemon.service`).
  Daemon DOWN recovery must not require the service to be already active: verify host
  capability and known store integrity/authority before executing a manual tick or restart.
  Invoke `BR_DB="$BR_DB" bash daemon/factory-af-tick.sh` for one host-local tick on Linux only
  after capability and store integrity/authority pass. Restore/restart the daemon through
  the canonical Linux deployment workflow (`ssh <configured-linux-factory-host> systemctl --user start ai.dark-factory.daemon.service`
  or repository deployment script). Do not broaden unrelated held queue or change selected pilot scope.
- **Bead stuck HUMAN_HELD**: In a selected-pilot mission, bulk recover must not release unrelated held items. Explicitly inspect the held scope first (e.g. via `$H list HUMAN_HELD`). Because `$H recover-held` processes every eligible `HUMAN_HELD` row (`attempt < 10`) without a bead filter, you cannot run global recover if unrelated held rows are eligible; retain holds on unrelated items and only use supported scoped recovery. Only when inspection confirms no unrelated held items exist (or only the intended pilot bead is eligible) may `$H recover-held` be invoked to requeue back to `QUEUED` (incrementing `attempt`, resetting `autonomy_secs`). Never mutate `bead_overlay` with a raw `sqlite3` command.
- **PR ci_green stuck on pre-existing infra**: document in PR comment, treat as known-issue; do NOT block readiness.
- **File-overlap conflict across multiple PRs**: serialize per stacked-PR single-writer rule.
