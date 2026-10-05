---
name: maw-execute-task
description: |
  Adversarial multi-agent development pipeline. Use when the user says "take the next task", "work through tasks", "run the pipeline", or wants to implement a task from the task board with full planning, review, implementation, and QA cycle.
  Supports flags: --worktree (force worktree mode), --no-worktree (force branch-only mode). These override the saved setting for the current run only.
  Supports positional arg: a task number or ID (e.g. `/maw-execute-task 3`, `/maw-execute-task TASK-003`) to run a specific task out of priority order instead of picking the highest-priority pending task.
  Model-invocation is guarded: if invoked by the model rather than an explicit user command, the auto-invoke guard applies (see Invocation guard) — confirmation is required before any state change unless the user disabled the guard in maw/settings.json.
---

# Adversarial Multi-Agent Development

## Settings

Pipeline settings are stored in `maw/settings.json`. The orchestrator checks this file at the start of every run. **Schema v2** (providers are first-class):

```json
{
  "worktree_mode": "always",
  "default_provider": "host",
  "spawn_timeout_min": 30,
  "allow_unverified_profile": false,
  "providers": {
    "claude": { "default_model": "sonnet",      "default_effort": "medium" },
    "codex":  { "default_model": "gpt-6.1-sol", "default_effort": "medium" }
  },
  "agents": {
    "code-reviewer": { "provider": "codex", "model": "gpt-6.1-sol", "effort": "xhigh" },
    "planner":       { "model": "opus" }
  }
}
```

Agent names everywhere are the agent file stems: `clarifier`, `premise-challenge`, `planner`, `plan-reviewer-1`, `plan-reviewer-2`, `implementer`, `code-reviewer`, `fixer`, `qa`.

- `worktree_mode`: `always` — always create a git worktree for the task (default if user picks this); `never` — work on a feature branch directly, no worktree; `ask` — ask the user each time before starting a task
- `default_provider`: `"host"` (literal, default) = the harness this orchestrator is running in; or pin to `"claude"` / `"codex"`.
- `providers.<p>.default_model` / `default_effort`: per-provider defaults, used whenever an agent resolves to provider `<p>` without an explicit model/effort of its own.
- `agents.<name>`: an **atomic partial profile** for one agent — any of `provider`, `model`, `effort`. Values set here are *explicit* (see Step 0.6 resolution). Omitted fields inherit.
- `spawn_timeout_min`: wall-clock cap per external spawn (default 30).
- `shared_memory` (optional, default `true`): `false` turns off the task-folder shared memory — `transcripts/`, `scratch/`, `log.jsonl` — for every stage of the run. It trades cross-stage evidence for fewer tokens per stage; the exact off-behavior is defined once, in the Shared memory section.
- `runner_progress` (optional, default `true`): `false` makes external spawns run with `MAW_RUNNER_PROGRESS=0`, so `scripts/runner.sh` prints only its start and exit lines instead of live event types. The capture file, exit codes, and `runner/` records are unchanged.
- `allow_unverified_profile`: when `true`, a model absent from the capability catalog may be passed through to its provider with a warning instead of being rejected. Default `false`.
- Machine facts (binaries present, login state) are **never** stored here — they are probed fresh each run (Step 0.65).
- `auto_invoke_guard` (optional map): `{ "maw-execute-task": true | false | "never" }`. Governs **model-chosen** invocation of this skill (a human typing the command is never guarded). `true` (default when absent) — before any state change, present the chosen task, resolved profiles, and a cost estimate, and get explicit user confirmation. `false` — unattended model invocation allowed. `"never"` — decline model invocation entirely (the pre-v2 hard-off behavior).

**Legacy schema migration (one-time).** If the file contains v1 fields (`agent_model`, `agent_model_overrides`, `agent_effort`, `agent_effort_overrides`), migrate on first read: `agent_model` → `providers.claude.default_model`; `agent_effort` → `providers.claude.default_effort`; each `agent_model_overrides[n]` → `agents.<n>.model` plus `agents.<n>.provider: "claude"`; same for effort overrides. This is a **merge, not a rewrite**: remove only the four legacy keys, preserve every other key present (known or unknown — `worktree_mode`, `spawn_timeout_min`, `auto_invoke_guard`, future fields). Tell the user what changed and continue. Migration preserves the resolved profiles: a Claude-only setup resolves to exactly the same (model, effort) per agent as before.

Model, effort, **and provider** can also be overridden **per task** in `task.md` (see Step 0.6 precedence) — `task.md` always beats `settings.json`.

If `maw/settings.json` does not exist or `worktree_mode` is missing, the orchestrator **must ask the user** before proceeding (see Step 0.5). If `providers` is missing entirely (and no legacy fields to migrate), the orchestrator **must ask the user** the model/effort question (see Step 0.6).

## Provider capability catalog (v2026-09)

This is a **catalog, not detection** — a versioned reference of known-valid (provider, model, effort) combinations. Availability on this machine is established by the Step 0.65 preflight, never by this table. Update the version stamp when editing.

| Provider | Model | Valid efforts | Notes |
|---|---|---|---|
| claude | `sonnet` | low, medium, high, xhigh, max | alias — resolves to the host's current Sonnet |
| claude | `opus` | low, medium, high, xhigh, max | alias |
| claude | `haiku` | low, medium, high | xhigh/max → reject |
| claude | `fable` | low, medium, high, xhigh, max | premium tier — one-time "confirm cost" prompt per task |
| codex | `gpt-6-astra` | low, medium, high, xhigh, max, ultra | OpenAI premium tier — one-time "confirm cost" prompt per task |
| codex | `gpt-6.1-sol` | low, medium, high, xhigh, max, ultra | codex default; needs codex CLI ≥ 0.159.1 (older CLI + ChatGPT login → HTTP 400 "not supported") |
| codex | `gpt-6-sol` | low, medium, high, xhigh, max, ultra | previous generation |
| codex | `gpt-6-luna` | low, medium, high, xhigh, max | ultra → reject |
| codex | `gpt-5.6-sol` | low, medium, high, xhigh, max, ultra | previous generation |
| codex | `gpt-5.6-terra` | low, medium, high, xhigh, max, ultra | previous generation |
| codex | `gpt-5.6-luna` | low, medium, high, xhigh, max | previous generation; ultra → reject |
| codex | `gpt-5.5` | low, medium, high, xhigh | max/ultra → reject; retires from Codex 2026-10-14 |

Astra is the premium capability choice; the codex default is `gpt-6.1-sol/medium`, the same model OpenAI's Codex catalog uses as its default. It needs codex CLI ≥ 0.159.1: on 0.156 with ChatGPT sign-in it was rejected with HTTP 400, on 0.160 it ran (both checked 2026-10-03). On an older CLI, update it or set `gpt-6-sol` explicitly. Effort lists for the codex rows come from the Codex model metadata (`~/.codex/models_cache.json`, codex 0.160, fetched 2026-10-03). Sources: [OpenAI Codex models](https://learn.chatgpt.com/docs/models) and [Astra API model](https://developers.openai.com/api/docs/models/gpt-6-astra). API reasoning efforts are low through max; `ultra` is the Codex harness delegation mode, also advertised for Astra in the Codex model catalog checked 2026-09-04. This is not a claim that the API accepts `reasoning.effort=ultra`, or that an external Astra stage has passed live acceptance.

Clamp rules (mandatory, after resolution — Step 0.6):

- A resolved (model, effort) pair not valid per this table → **stop and report** the exact pair and the agent. Never silently downgrade an effort or auto-bump a model — the cost change is the user's call.
- `ultra` is valid only when the resolved provider is codex (and the model supports it). Claude-side efforts are the five subagent-variant levels.
- A model not in this table: reject and report — unless `allow_unverified_profile: true`, in which case pass it through to the provider with an explicit warning in the run log and metrics (`(unverified)` suffix in the Model column) and no capability claims; a spawn failure on such a profile is not retried, it is reported.
- Model validity is provider-scoped: `opus` under provider=codex or `gpt-6.1-sol` under provider=claude → stop and report (see Step 0.6 explicit-wins-or-fails).

**Cross-tier dominance notes (July 2026, external benchmarks; historical, not re-measured for Astra or gen-6 Sol/Luna):**

- claude: `fable` at **low** effort outperforms `opus` at max on hard agentic coding (SWE-bench Pro ~75 vs ~69) at roughly half the per-task cost — fable-low is the cheap entry to the premium tier; no opus effort reaches fable. `sonnet` at xhigh can cost **more** than opus at comparable accuracy — sonnet's value zone is low..high; do not chase opus with sonnet-xhigh.
- codex: `gpt-5.6-sol` at medium beats `terra` at xhigh on intelligence benchmarks — terra is a latency/throughput tier, not a catch-up tier; `luna` and `sol` sit on the intelligence-per-cost Pareto frontier. `ultra` on sol is a different mechanism, not a bigger thinking budget: it coordinates parallel subagents with synthesis (~2–3× cost, small single-digit accuracy gains). **Ultra reliability caveat (observed live, Windows, codex 0.145):** ultra's multi-agent code-mode failed its internal host handshake repeatedly (`code-mode host exited during handshake` in stderr — no disk reads possible, ~500k tokens burned with no artifact) while single-agent `xhigh` completed the same stage cleanly. Prefer `xhigh` for external codex stages until ultra is verified on the target machine; treat repeated handshake errors as fatal-env (no retry on the same effort — retry at xhigh is the sanctioned operator move). Ultra spawns that do run need `2× spawn_timeout_min` (multi-agent runs long).
- codex gen-6 (vendor claims, September 2026, not measured here): `gpt-6-sol` makes about half the mistakes of `gpt-5.6-sol` at half its token price ($2/$10 vs $4/$20 per M); `gpt-6.1-sol` is claimed near Astra on agentic coding at one-fifth of Astra's price; `gpt-6-luna` is $0.10/$0.50. On these numbers the 5.6 family has no profile where it is the better buy; keep it only for reproducing older runs.
- Rule of thumb when building profiles: **raise effort within a model for cost control; switch tier for capability; never max-out a lower tier to imitate a higher one** — cross-tier catch-up via effort is Pareto-inefficient on both providers.

---

## Modes

The `Mode:` field in `task.md` controls which subset of the pipeline runs. Valid values:

| Mode | Pipeline | Stops after |
|---|---|---|
| `full` (default) | Clarifier -> Premise Challenge -> Planner -> Plan Rev x2 -> Implementer -> Code Rev -> Fixer -> QA | QA_REPORT.md |
| `small-fix` | Implementer -> Code Rev -> Fixer -> QA | QA_REPORT.md |
| `brainstorm` | Clarifier -> Premise Challenge -> Planner -> Plan Rev x2 | PLAN_FINAL.md (no code written) |
| `deep-research` | Premise Challenge -> Planner (web search emphasis) -> Plan Rev x2 | PLAN_FINAL.md (research report, no code) |

**Backward compatibility:** if the `Mode:` field is missing from `task.md`, default to `full`.

Read `Mode:` right after picking the task (Step 0) and store it as `MODE`. Later steps are gated on this value.

---

## Orchestrator instructions

You are the orchestrator. Do not implement anything yourself. Your job is to spawn agents in sequence and pass artifacts between them via files.

**Invocation guard (first, before anything).** If this run was started by the model (via the Skill tool / autonomous decision) rather than an explicit user command: read `auto_invoke_guard["maw-execute-task"]` from `maw/settings.json` (read-only — no migration yet). Absent or `true` → run **only read-only work** (task pick, in-place task read, profile resolution preview — no settings writes, no migration, no paid probes), then present the task, profiles, providers/data-transfer note, and a cost estimate, and get explicit confirmation; settings migration, preflight probes, and Step 0.8 all happen **after** the confirmation. `false` → proceed unattended, subject to: at most one auto-run per session, probes/retries count toward the run's budget, and the disclosure is logged instead of asked. `"never"` → decline the invocation and tell the user to run the command themselves. A human-typed command skips this guard entirely.

**Dispatch rule.** Each agent resolves to an atomic profile `(provider, model, effort)` per Step 0.6. How you spawn depends on whether that provider is the harness you are running in:

- **Native path** (resolved provider == host harness, hosted in Claude Code): Task tool with named subagents, exactly as below. This is today's behavior — same dispatch, same resolved profiles — when everything resolves to claude.
- **External path** (resolved provider != host harness, or you are hosted in Codex — see the Hosting section): a one-shot CLI spawn per the **External runner contract** section. The spawn prompt *content* is identical on both paths; only the transport differs.

**Native path — agents are named subagents**, generated at install into `.claude/agents/` as `maw-<stem>-<effort>.md` (9 stems × 5 effort levels). Their bodies are static role prompts — you do **not** read them. For each step you call the Task tool with:

- `subagent_type` = `maw-<stem>-<effort>`, where `<effort>` is resolved per Step 0.6 (e.g. `maw-code-reviewer-high`).
- `model` = resolved per Step 0.6.
- `prompt` = the **dynamic spawn prompt** you build for that stem (see "How to build a spawn prompt" below). This is the only thing carrying paths, artifacts, per-mode source, and the project-context overlay — the static body has none of it.

The per-step instructions below are written in native-path vocabulary (`subagent_type=...`). When a step's resolved provider takes the external path, build the same spawn prompt and hand it to the external runner instead; everything else about the step (mode gates, artifact checks, follow-ups) is unchanged.

### Shared memory (transcripts, scratch, log)

Every task carries three orchestrator-owned shared-memory primitives. This section is their single normative definition:

```text
{WORK_ROOT}/{TASK_DIR}/transcripts/
{WORK_ROOT}/{TASK_DIR}/transcripts/.gitignore
{WORK_ROOT}/{TASK_DIR}/scratch/
{WORK_ROOT}/{TASK_DIR}/scratch/.gitignore
{WORK_ROOT}/{TASK_DIR}/log.jsonl
```

`transcripts/.gitignore` is exactly:

```gitignore
*
!.gitignore
```

`scratch/.gitignore` ignores only binary and dump artifacts, leaving scripts, source, Markdown, JSON, CSV, and plain text trackable:

```gitignore
*.bin
*.dump
*.core
*.zip
*.tar
*.tar.gz
*.tgz
*.png
*.jpg
*.jpeg
*.gif
*.pdf
*.sqlite
*.db
node_modules/
__pycache__/
```

**Toggle.** Read `shared_memory` from `maw/settings.json` once per run, together with the other settings; absent means `true`. There is no per-task override and no per-primitive switch. When it is `false`, this whole section is inert for the run and every later reference to it resolves as follows:

- no scaffolding: do not create `transcripts/`, `scratch/`, `log.jsonl`, or their `.gitignore` files. Anything already in the task folder from an earlier run is left untouched and unadvertised;
- in a spawn prompt, both the full and the reduced block, with their role clauses, are replaced by this exact line: `Shared memory: disabled for this run. No scratch, log, or transcript path is supplied; skip every instruction in your role that refers to one, and keep your own probes out of the task folder.`;
- the post-spawn lifecycle skips steps (4) and (5): no transcript allocation or harvest, no log validation, no `transcript:missing` / `log:*` warnings. On the external path the provider capture is deleted with the temp directory after usage and diagnostics are taken, and `SPAWN_FAILURE.md` carries the stderr tail only;
- the pre-worktree-removal transcript rescue is skipped;
- freshness and same-goal continuity are unchanged — they do not depend on the three primitives. A fallback fresh spawn simply has no partial transcript to point to.

Isolation of `premise-challenge` and both plan reviewers is not weakened by the toggle: with it off, no role receives any of the paths.

Prompts carry paths only. The orchestrator never inlines transcript or log content into a spawn prompt, `metrics.md`, or a user report. Transcripts are evidence to search selectively with Grep or `rg`, never files to load wholesale. `scratch/` persists through every status move and is not cleaned at wrap-up. `transcripts/` may legitimately be empty at the first stage of a run or in `small-fix`; emptiness is normal, not a defect. The access rules below, artifact write scopes, orchestration security, post-spawn lifecycle, and continuity eligibility cannot be overridden by project context.

| Stage | `transcripts/` | `scratch/` | `log.jsonl` |
|---|---|---|---|
| clarifier | read/search | read/write | read + append |
| premise-challenge | **no path, no read** | read/write | **append only; no read** |
| planner | read/search | read/write | read + append |
| plan-reviewer-1 | **no path, no read** | read/write | **append only; no read** |
| plan-reviewer-2 | **no path, no read** | read/write | **append only; no read** |
| implementer | read/search | read/write; self-check assets live here | read + append |
| code-reviewer | read/search | read/write probes | read + append; dead ends first |
| fixer | read/search | list/read first; write probes | read + append |
| qa | read/search | list/read first; write tests/probes | read + append; dead ends first |

An isolated role must not infer, probe, or reconstruct omitted paths. Transcript access begins with the implementer. Both plan reviewers and the premise challenge stay independent of prior lineage. The clarifier has full access because a relaunch from `blocked/` may already contain transcripts from the previous run.

#### Minimal log schema and append rules

`log.jsonl` is append-only: one BOM-free UTF-8 JSON object per line, a trailing newline, and no blank lines. Required fields are non-empty strings: `ts`, `stage`, `provider`, `model`, `effort`, `kind`, `body`. `ts` is a parseable UTC ISO-8601 value ending in `Z`; `stage` is one of the nine stems named in Settings. Optional `refs` is an array that may be empty; every element present is a non-empty string naming `file:line`, a command, or an artifact path. `kind` is exactly:

- `dead_end` — an approach attempted or seriously considered and why it was rejected;
- `decision` — the choice made and the alternative not taken.

No other kinds are allowed: no facts, hypotheses, summaries, or entries about having read the log. Never rewrite, reorder, or delete entries. **Log entries are pointers, not evidence**; transcripts, command output, and code are the evidence, and every relevant `ref` must be verified.

Append with Python `open(path, "a", encoding="utf-8", newline="\n")`, or PowerShell `[System.IO.File]::AppendAllText($path, $line, (New-Object System.Text.UTF8Encoding($false)))`. For this file, `>`, `>>`, and locale-default `Add-Content` are forbidden: Windows PowerShell 5.1 redirection writes UTF-16LE and `Add-Content` defaults to the active ANSI code page.

After every spawn attempt and every completed continuation, on success or failure, validate without modifying the file. Never use `jq`. The Python form is:

```python
import datetime as dt, json, pathlib, sys

path = pathlib.Path(sys.argv[1])
raw = path.read_bytes()
errors = []
if raw.startswith(b"\xef\xbb\xbf"):
    errors.append("line 1: leading BOM")
if raw and not raw.endswith(b"\n"):
    errors.append("file: missing trailing newline")
try:
    text = raw.decode("utf-8")
except UnicodeDecodeError as exc:
    errors.append(f"line {raw[:exc.start].count(bytes([10])) + 1}: invalid UTF-8")
    text = raw.decode("utf-8", errors="replace")
required = ("ts", "stage", "provider", "model", "effort", "kind", "body")
stages = {"clarifier", "premise-challenge", "planner", "plan-reviewer-1", "plan-reviewer-2", "implementer", "code-reviewer", "fixer", "qa"}
for number, line in enumerate(text.splitlines(), 1):
    if not line:
        errors.append(f"line {number}: blank")
        continue
    if line.startswith("\ufeff"):
        if number != 1 or not raw.startswith(b"\xef\xbb\xbf"):
            errors.append(f"line {number}: leading BOM")
        line = line[1:]
    try:
        item = json.loads(line)
    except Exception as exc:
        errors.append(f"line {number}: invalid JSON ({exc})")
        continue
    if not isinstance(item, dict):
        errors.append(f"line {number}: not an object")
        continue
    invalid_required = False
    for field in required:
        if not isinstance(item.get(field), str) or not item[field].strip():
            errors.append(f"line {number}: invalid {field}")
            invalid_required = True
    if invalid_required:
        continue
    stamp = item.get("ts")
    if isinstance(stamp, str) and stamp.endswith("Z"):
        try: dt.datetime.fromisoformat(stamp[:-1] + "+00:00")
        except ValueError: errors.append(f"line {number}: invalid ts")
    elif isinstance(stamp, str): errors.append(f"line {number}: invalid ts")
    if item.get("stage") not in stages: errors.append(f"line {number}: invalid stage")
    if item.get("kind") not in {"dead_end", "decision"}: errors.append(f"line {number}: invalid kind")
    refs = item.get("refs")
    if refs is not None and (not isinstance(refs, list) or any(not isinstance(ref, str) or not ref.strip() for ref in refs)):
        errors.append(f"line {number}: invalid refs")
print("\n".join(errors))
```

The PowerShell form is:

```powershell
param([string]$Path)
$Errors = [System.Collections.Generic.List[string]]::new()
$Bytes = [System.IO.File]::ReadAllBytes($Path)
if ($Bytes.Length -ge 3 -and $Bytes[0] -eq 0xEF -and $Bytes[1] -eq 0xBB -and $Bytes[2] -eq 0xBF) { $Errors.Add('line 1: leading BOM') }
if ($Bytes.Length -gt 0 -and $Bytes[$Bytes.Length - 1] -ne 0x0A) { $Errors.Add('file: missing trailing newline') }
try { $Text = (New-Object System.Text.UTF8Encoding($false, $true)).GetString($Bytes) }
catch { $Errors.Add('file: invalid UTF-8 (offset unknown)'); $Text = (New-Object System.Text.UTF8Encoding($false, $false)).GetString($Bytes) }
$Required = @('ts','stage','provider','model','effort','kind','body')
$Stages = @('clarifier','premise-challenge','planner','plan-reviewer-1','plan-reviewer-2','implementer','code-reviewer','fixer','qa')
$Lines = $Text -split "`r?`n"
for ($I = 0; $I -lt $Lines.Count; $I++) {
  $N = $I + 1; $Line = $Lines[$I]
  if ($I -eq $Lines.Count - 1 -and $Line -eq '') { continue }
  if ($Line -eq '') { $Errors.Add("line ${N}: blank"); continue }
  if ($Line[0] -eq [char]0xFEFF) { if ($N -ne 1 -or -not ($Bytes.Length -ge 3 -and $Bytes[0] -eq 0xEF -and $Bytes[1] -eq 0xBB -and $Bytes[2] -eq 0xBF)) { $Errors.Add("line ${N}: leading BOM") }; $Line = $Line.Substring(1) }
  try { $Item = $Line | ConvertFrom-Json -ErrorAction Stop } catch { $Errors.Add("line ${N}: invalid JSON"); continue }
  if ($null -eq $Item -or $Item.PSObject.BaseObject -isnot [System.Management.Automation.PSCustomObject]) { $Errors.Add("line ${N}: not an object"); continue }
  $InvalidRequired = $false
  foreach ($Field in $Required) { if ($Item.$Field -isnot [string] -or [string]::IsNullOrWhiteSpace($Item.$Field)) { $Errors.Add("line ${N}: invalid $Field"); $InvalidRequired = $true } }
  if ($InvalidRequired) { continue }
  $Parsed = [datetimeoffset]::MinValue
  if ($Item.ts -isnot [string] -or -not $Item.ts.EndsWith('Z') -or -not [datetimeoffset]::TryParse($Item.ts, [ref]$Parsed)) { $Errors.Add("line ${N}: invalid ts") }
  if ($Stages -notcontains $Item.stage) { $Errors.Add("line ${N}: invalid stage") }
  if (@('dead_end','decision') -notcontains $Item.kind) { $Errors.Add("line ${N}: invalid kind") }
  if ($null -ne $Item.refs -and ($Item.refs -isnot [array] -or @($Item.refs | Where-Object { $_ -isnot [string] -or [string]::IsNullOrWhiteSpace($_) }).Count -gt 0)) { $Errors.Add("line ${N}: invalid refs") }
}
$Errors
```

Report invalid UTF-8 (the PowerShell form deliberately reports an unknown offset rather than a guessed line), leading BOM, a missing trailing newline, blank lines, non-object or unparseable JSON lines, invalid required fields, non-UTC timestamps, invalid stages or kinds, and malformed `refs`. If neither interpreter is available, use `log:unvalidated`; if defects exist, use `log:malformed=N`. Put the warning in that attempt's metrics outcome, the next stage report, and wrap-up. A malformed or unvalidated log never rejects a valid artifact, triggers a retry, or blocks the pipeline.

#### Transcript allocation and harvest

Before dispatch, reserve `<step>-<stem>.<ext>` if absent, otherwise the smallest unused `<step>-<stem>-retryN.<ext>` for `N` starting at 1; `<step>` is the pipeline step number in the stage heading. A fresh spawn never overwrites an archive, including on a whole-task relaunch from `blocked/`. Only a true continuation of the same agent reuses and replaces its own archive because the new transcript is a strict superset. Filenames never contain an agent id.

The harness marks the native agent id as internal metadata. Keep it only in transient working state and use it only to construct the transcript source path or as `SendMessage`'s `to`. Never put it in `metrics.md`, `SPAWN_FAILURE.md`, `log.jsonl`, `OPEN_DECISIONS.md`, any task artifact, or any user-facing message.

**Native Claude harvest:** the Task tool result returns at launch and carries the agent id; record it transiently but do not harvest yet. Wait for the terminal completion `<task-notification>` and take its `<task-id>` (fall back to the launch record if omitted). Under `${CLAUDE_CONFIG_DIR}` or `~/.claude`, glob `<config>/projects/*/*/subagents/agent-<id>.jsonl`. Exactly one exact-id match is copied to the reserved archive; zero or multiple matches produce `transcript:missing` without changing the stage verdict. If no id surfaced, examine `agent-*.meta.json` sidecars in candidate `subagents/` directories and select exactly one whose `agentType` equals the spawned variant and whose `description` equals the unique per-attempt description passed at launch: `MAW <stem> <TASK-ID> a<attempt>`. Copy only its matching `.jsonl`, never the sidecar. Ignore duplicate notifications for an already completed and archived stage unless this orchestrator initiated a continuation. After a continuation completes, replace the same archive with the longer exact-id transcript.

**External harvest and cleanup ordering:** amend the per-spawn temp-directory contract below with this required order on success, nonzero exit, timeout, and handled cancellation. While temp files still exist, evaluate all four success criteria, parse usage, materialize a sanctioned single-artifact fallback if active, and retain the stderr tail needed for `SPAWN_FAILURE.md`. Then move either provider's `events.jsonl` to the reserved `.jsonl` archive. Older claude `.json` archives remain readable and are never converted or overwritten. Only then delete the temp directory in finally-style cleanup. `stderr.log` and `last-message.md` are not archived. A missing provider capture is `transcript:missing`, not a changed verdict. Cancellation cleanup is best-effort if the process is terminated so hard that control never returns.

#### Freshness and same-goal continuity

Every stage is a fresh spawn by default on both transports. Continuity is eligible only for (a) a retry after a timeout or transient execution failure, or (b) an implementer re-run after the user amends the plan following `Verdict: PLAN_BLOCKED`; the resolved `(provider, model, effort)` must be unchanged. `premise-challenge`, `plan-reviewer-1`, `plan-reviewer-2`, `code-reviewer`, `fixer`, and `qa` are never continued; no agent continues into another role, and the fixer never continues the implementer. Native continuation uses `SendMessage` to the transiently retained id with a short message naming the failure or amendment and expected artifact path; for `PLAN_BLOCKED`, it also tells the implementer to re-read the amended plan from disk. Never re-paste the original prompt. `SendMessage` is non-blocking, so wait for its terminal completion notification before post-spawn processing or advancement. A missing id, refused/unavailable resume, user cancellation, changed profile, or ambiguous state falls back to a fresh spawn with a new `-retryN` archive and a pointer to the harvested partial transcript. External dispatch is always fresh (`--ephemeral` / `--no-session-persistence`) and degrades to transcripts plus log; unavailable continuity is not a failure. Before any retry or continuation preserve the current artifact with the existing `.prev-<n>.md` rule. A continued run has the same success criteria, one-retry limit, harvest, validation, and its own metrics row.

#### Post-spawn lifecycle

Steps 2 through 9 use one sequence after every attempt: (1) wait for completion; (2) evaluate the four success criteria and parse usage while raw provider output exists; (3) collect failure diagnostics; (4) harvest the transcript; (5) validate `log.jsonl` non-blockingly; (6) append the metrics row with any `transcript:missing`, `log:malformed=N`, or `log:unvalidated` warning; (7) delete the external temp directory; then (8) branch, retry, pause, or advance. Transcript harvest and log validation are not success criteria. On exhausted failure, `SPAWN_FAILURE.md` names the archived partial transcript by filename or says `transcript:missing`, never exposing the agent id.

**Turn discipline — a stage report is not the end of your turn.** Between stages you owe the user a report; you do not owe them a pause. Whenever the mode gate allows the next stage and no blocking gate fired, **spawn it in the same turn as the report**: the report text first, the spawn call after it. Your turn ends when the pipeline has to wait for something, not when you have finished narrating.

Announcing an intention is not spawning. A turn that ends on "continuing", "next up is the implementer", "on to plan review" hands control back to the user while claiming the opposite — from their side the pipeline stopped silently mid-task, and the only way to restart it is a nudge that carries no information. Observed live across two projects: the orchestrator closed a turn with "next — implementation" and stopped, twice in one session, both times after a stage that had succeeded. The longer and better the report, the likelier this is: a satisfying piece of prose feels like a finished turn. If you catch yourself writing a sentence about what you are going to do next, replace the sentence with doing it.

Only these end a turn legitimately: a blocking question (below), a FAIL-class gate (see Rules), a spawn failure whose retry is exhausted, wrap-up, or the user telling you to stop. Setup is its own case and is unaffected: the invocation guard, the Step 0.5 / 0.6 first-run questions, and a preflight failure all end the turn by design — they happen before the task leaves `pending/`, where there is no pipeline to park.

**Blocking vs non-blocking questions.** A question is **blocking** only if the next stage cannot be spawned without the answer:

- an agent's own `## Open questions` relay — clarifier (Step 2), planner (Step 3): the spec or plan is incomplete until answered;
- a FAIL verdict, `PREMISE SUSPECT`, or `PLAN_BLOCKED`;
- an irreversible or outward-facing action the Rules already gate: merging, pushing, deleting a branch, a cost-tier confirmation.

Everything else is **non-blocking**: scope you would have widened, an adjacent defect you noticed, a follow-up worth its own task, a choice between two options where one is defensible. For those — take the defensible option and keep going, recording the call in `{WORK_ROOT}/{TASK_DIR}/OPEN_DECISIONS.md` (create on first use; one dated bullet each: what you decided, what the alternative was, what would flip it). The file is surfaced at wrap-up, so nothing is lost by not asking now.

A question you have yourself labelled as blocking nothing must never stop the pipeline — asking it and then waiting makes your own assessment untrue. Generic user phrasing ("don't ask me", "run autonomously") does not relax the blocking list; it is already the default for everything outside it.

### How to build a spawn prompt

The subagent body already contains the role, instructions, and output format. Your spawn prompt supplies only what is dynamic. Build it as:

1. **Path header** (always, first):
   ```
   Working directory: {WORK_ROOT}/
   Task dir: {WORK_ROOT}/{TASK_DIR}/
   Repo root: {REPO_ROOT}
   ```
2. **Shared-memory block** from the table and exact templates below. Use worktree-correct paths and the resolved identity fields for this attempt. With `shared_memory: false`, the single disabled line from the Shared memory toggle goes here instead.
3. **Stem-specific dynamic content** from the table below. "Inline" = paste the file's contents into the prompt under a labelled `---` block. "Path" = give the path and let the agent read it from disk (its body has the mandatory-read discipline).
4. **Project-context overlay** (Step 0.7) appended at the very end, if `PCTX/` exists.

For every fresh native Task spawn, pass the tool's `description` argument as `MAW {stem} {TASK-ID} a{attempt}`. The attempt counter starts at 1 and increments for each fresh spawn of that stem in this task, including fresh retries and re-spawns. A `SendMessage` continuation is not a fresh spawn: it reuses the prior attempt number and description. The no-id transcript fallback in Shared memory depends on this exact, per-attempt value.

| stem | shared memory | inline into prompt | reference as path | per-mode |
|---|---|---|---|---|
| `clarifier` | full | `task.md` (as "Task:") | — | — |
| `premise-challenge` | reduced / write-only | premise source = `TASK_FINAL.md`, else `task.md` (as "Task — the premise under audit:") | — | source falls back to `task.md` when no `TASK_FINAL.md` |
| `planner` | full | task source = `TASK_FINAL.md` (full/brainstorm) or `task.md` (deep-research) (as "Task:") | — | deep-research: prepend the research-report directive (below) |
| `plan-reviewer-1` | reduced / write-only | — | `TASK_FINAL.md` (task spec), `PLAN.md` (plan to review) | — |
| `plan-reviewer-2` | reduced / write-only | — | `TASK_FINAL.md` (task spec), `PLAN_V2.md` (plan to review) | — |
| `implementer` | full | spec (as "Task:") + plan (as "Implementation plan:") | — | small-fix: spec = `task.md`, plan = the small-fix fallback text (below) |
| `code-reviewer` | full | — | spec, `PLAN_FINAL.md` (final plan), `IMPL_SUMMARY.md` | small-fix: omit the plan line; spec = `task.md` |
| `fixer` | full | spec (as "Task:") + plan (as "Final plan:") | `IMPL_REVIEW.md` (review to act on) | small-fix: spec = `task.md`, plan = the small-fix fallback text (below) |
| `qa` | full | — | spec, `PLAN_FINAL.md`, `IMPL_SUMMARY.md`, `IMPL_REVIEW.md`, `FIX_SUMMARY.md` | small-fix: omit the plan line; spec = `task.md` |

"spec" = `TASK_FINAL.md` in `full` mode, `task.md` in `small-fix` mode. All paths are under `{WORK_ROOT}/{TASK_DIR}/`.

Use this exact **full block**:

```text
Shared memory (paths only; content is never inlined):
- Transcripts: {WORK_ROOT}/{TASK_DIR}/transcripts/ — read/search selectively with Grep or rg; do not load wholesale. The directory may legitimately be empty.
- Scratch: {WORK_ROOT}/{TASK_DIR}/scratch/ — persistent executable evidence; read/write only as your role permits.
- Log: {WORK_ROOT}/{TASK_DIR}/log.jsonl — read and append only. Never rewrite it. Entries are pointers, not evidence: verify every relevant ref against code or command output.
For any log append, stamp stage={stage}, provider={provider}, model={model}, effort={effort}. Write one BOM-free UTF-8 JSON object plus a trailing newline. Required non-empty string fields: ts, stage, provider, model, effort, kind, body. Optional refs is an array that may be empty; every element present must be a non-empty string. kind is exactly dead_end (attempt/rejection) or decision (choice and named alternative). Do not log facts, hypotheses, summaries, or that you read the log. Use the safe append mechanisms in the Shared memory section; never use >, >>, or locale-default Add-Content.
```

Use this exact **reduced / write-only block**:

```text
Shared memory (isolated role; paths only; content is never inlined):
- Scratch: {WORK_ROOT}/{TASK_DIR}/scratch/ — persistent executable evidence; read/write only as your role permits.
- Log append destination: {WORK_ROOT}/{TASK_DIR}/log.jsonl — append only. Do not read log.jsonl. No transcript path is provided; do not infer, probe, or reconstruct one.
For any log append, stamp stage={stage}, provider={provider}, model={model}, effort={effort}. Write one BOM-free UTF-8 JSON object plus a trailing newline. Required non-empty string fields: ts, stage, provider, model, effort, kind, body. Optional refs is an array that may be empty; every element present must be a non-empty string. kind is exactly dead_end (attempt/rejection) or decision (choice and named alternative). Do not log facts, hypotheses, summaries, or that you read the log. Use the safe append mechanisms in the Shared memory section; never use >, >>, or locale-default Add-Content.
```

Append these role clauses to the selected block: implementer writes every self-check script, probe, and measurement under `scratch/` with a descriptive name and leaves it there; code-reviewer and qa, after mandatory artifact loading and disconfirmation, triage `dead_end` entries first and verify relevant refs against primary code/output; fixer and qa list and read `scratch/` before their other role inputs and treat it only as a coverage map—running the author's script is not independent verification. This deliberate prompt/body repetition keeps the rule visible on both native and external dispatch; the normative access matrix and lifecycle remain only in this section.

**Deep-research directive** (prepend to the `planner` spawn prompt only when `MODE` is `deep-research`):

> Mode: deep-research. Focus on researching best practices, existing solutions, and tradeoffs. Use your web search and web fetch capabilities extensively. Output a research report, not an implementation plan. Cite sources with URLs. Compare at least 2-3 alternative approaches. Do not write file-level change steps — the goal is to inform a human decision, not to drive an implementer.

**Deep-research review directive** (prepend to both plan-reviewer spawn prompts only when `MODE` is `deep-research`):

> Mode: deep-research. The artifact under review is a research report, not an implementation plan. Do not demand file-level change steps, rollout plans, or test matrices — their absence is correct here. Review for: claim-source fidelity (do the cited sources actually say this — spot-check them), coverage of alternatives (2-3 compared, fairly), unstated assumptions, stale sources, and whether the comparison actually answers the task's question. Your output is still the revised report, same filename contract.

**Small-fix plan fallback text** (use as the inlined "plan" for `implementer`/`fixer` in `small-fix` mode):

> No plan file — this is small-fix mode. task.md is the spec (inlined above). Make the minimal set of changes needed to satisfy the acceptance criteria. Open every file before editing. Do not expand scope beyond what task.md asks for.

### External runner contract (used whenever a stage's resolved provider takes the external path)

The external path runs a stage as a **one-shot headless CLI process**. Same spawn prompt, same artifact rules, different transport. It exists for cross-provider stages under a Claude Code host, and for all stages under a Codex host (see Hosting).

**Spawns are synchronous.** Run every external spawn in the foreground and wait for it to finish before proceeding; **never** background a spawn and end your own session. A headless orchestrator session that exits kills its child processes and strands the task mid-pipeline in `in_progress/` (observed live: a backgrounded reviewer spawn died orphaned with no artifact). Host background facilities may be used only if the orchestrator remains alive and blocks on completion before the next step. Wait as **one blocking tool call** (the spawn command itself), not a poll loop — polling burns orchestrator turns, and a headless session that exhausts its turn budget mid-wait strands the task exactly like a backgrounded spawn (also observed live). Anyone driving this pipeline headless (`claude -p`) should pass a generous `--max-turns`; external xhigh/ultra spawns run 10+ minutes.

**Per-spawn temp directory.** Create a uniquely named, user-private directory in the OS temp location — POSIX: `SPAWN_TMP=$(mktemp -d "${TMPDIR:-/tmp}/maw-spawn-XXXXXX")`; PowerShell: `$SpawnTmp = Join-Path $env:TEMP ("maw-spawn-" + [System.IO.Path]::GetRandomFileName()); New-Item -ItemType Directory $SpawnTmp`. Everything transient lives inside it: `prompt.md`, the provider's output capture (`events.jsonl` for both providers, plus `last-message.md` for codex), `stderr.log`, and — for codex spawns — the private `codex-home/` described below. Never place transient spawn files inside the task tree. On every exit path—success, failure, timeout, or handled cancellation—follow the Shared memory external ordering: evaluate success, parse usage, materialize if sanctioned, and capture diagnostics; move the provider capture into `transcripts/`; only then delete the whole directory. Session persistence is disabled at the CLI level too (`--ephemeral` / `--no-session-persistence`) so nothing lands outside the spawn dir. At the start of every run, scavenge stale `maw-spawn-*` directories older than a day. Prompts contain task + project-context content: treat a leak as a real leak, not a cosmetic one.

**Prompt assembly (external only):** `<raw agent body>` + blank line + `<the same dynamic spawn prompt you would pass the Task tool>` (path header, shared-memory block, dynamic content, PCTX overlay per Step 0.7) — with one difference: **substitute absolute paths** into the path header and artifact references (`WORK_ROOT_ABS`, absolute `TASK_DIR`). The child's cwd is `WORK_ROOT_ABS`; handing it relative `.worktrees/...` paths double-resolves (`.worktrees/X/.worktrees/X/...`). Raw bodies are installed with the skill at `agents/<stem>.md` relative to this SKILL.md file — resolve them from the installed skill directory, never from `maw/`.

**Write the prompt file yourself, in UTF-8. Never build it with shell redirection.** On Windows a `printf`/`cat` redirect goes through the console codepage (cp1251 on this machine), which silently mangles any non-ASCII character in the task, the plan, or a quoted source file before the child ever sees it. The two providers then diverge in the worst possible way: `codex exec` refuses the spawn outright (`Failed to read prompt from stdin: input is not valid UTF-8 (invalid byte at offset N)`), while `claude -p` accepts the corrupted text and answers as if nothing happened. Observed live while building a benchmark harness — a degree sign was enough. Use a small helper that opens the file with an explicit `encoding="utf-8"` and writes the assembled prompt in one go; codex's strictness is the only thing that makes this class of corruption visible at all, so treat that error as a real signal rather than a codex quirk to work around.

**Private `CODEX_HOME` (codex spawns only, mandatory).** A codex child loads **two** ambient instruction sources, and the CLI flags only kill one of them: `-c project_doc_max_bytes=0` suppresses the repo's `AGENTS.md`, but the operator's own `$CODEX_HOME/AGENTS.md` (default `~/.codex/AGENTS.md`) is loaded by a different code path that **no flag disables** — `--ignore-user-config` does not touch it (verified live, codex 0.145). The only thing that blocks it is pointing the child at a different codex home. Before each codex spawn, build one inside the spawn dir and copy exactly **one** file into it:

```sh
mkdir -p "$SPAWN_TMP/codex-home"
cp "${CODEX_HOME:-$HOME/.codex}/auth.json" "$SPAWN_TMP/codex-home/"
```

`auth.json` is what keeps the child logged in, and it is the only file that belongs there. **Do not copy `config.toml`** — it is not inert: `developer_instructions`, `model_instructions_file`, and `experimental_compact_prompt_file` are all config keys that inject text into the child, so copying it re-opens the ambient channel the private home exists to close. Anything the child genuinely needs from config is passed as an explicit `-c` flag instead (see the sandbox key below). Everything else in the real codex home — `AGENTS.md`, `rules/`, `skills/`, `plugins/`, `memories`, sessions, history — is left behind, which is the point. The directory dies with `$SPAWN_TMP`.

**Windows: the sandbox key must be passed explicitly.** On Windows, codex 0.145 permits workspace writes only when `windows.sandbox` is set; with no value the child refuses every write with `patch rejected: writing is blocked by read-only sandbox; rejected by user approval settings`. Since the private home has no `config.toml` (and `--ignore-user-config` would discard it anyway), pass it on the command line: `-c windows.sandbox="unelevated"`. Use `unelevated` — it needs no administrator rights and was verified to write successfully; `elevated` also works if the operator's own config uses it. **Omit this flag entirely on non-Windows hosts.** Project trust (`[projects.*] trust_level`) is **not** part of this: verified matrix on an untrusted path — trusted-without-the-sandbox-key refuses, untrusted-with-the-key writes. Trust does not gate writes here, so never "fix" a refusal by adding trust entries.

**Installed shell runner.** All external stage attempts and the transport probe use `scripts/runner.sh` relative to this installed skill. It requires POSIX `sh` (Git Bash on Windows), with no Python, Node, jq, or compiled helper. Resolve `RUNNER` to that file's absolute path. The orchestrator still assembles provider argv, prepares isolation, creates the private temp directory and UTF-8 `prompt.md`, and archives the old artifact before calling it.

Invocation: `sh "$RUNNER" "$WORK_ROOT_ABS" "$SPAWN_TMP" "$CAPTURE" "$ARTIFACT_ABS" -- command args...`. `CAPTURE` is `events.jsonl` for both providers (`result.json` remains accepted by the helper for non-streaming callers). `ARTIFACT_ABS` is the expected stage artifact (the probe's output for preflight); use `-` only for a sanctioned single-artifact materialization, then materialize and validate before accepting success. Pass arguments separately, never as an evaluated command string. The runner refuses an existing artifact or reused capture directory, runs synchronously in the work root, and redirects the child's stdout/stderr directly to files without decoding. An internal shell loop waits for the child and uses `awk` to display newly captured event types and tool-call activity about once a second; it does not print prompt text, tool payloads, or reasoning content. This display is best-effort, never a JSON validator or an input to stage decisions. Every displayed line lands in your own tool result; with `runner_progress: false` in settings, prefix the invocation with `MAW_RUNNER_PROGRESS=0` and the runner prints only its start and exit lines.

It records UTC `runner/started` before invocation, then `runner/exit-code`, `runner/finished`, and `runner/artifact` (`present`, `missing`, or `materialize`) inside the spawn directory. Exit 64 means wrapper setup refusal; exit 65 means the child exited zero but the artifact is absent, empty, or a symlink; other child failures retain their exit code. Progress output is best-effort: a closed host stdout disables display without terminating the child or losing its file capture. A child's own 64/65 is distinguished by `runner/exit-code`. These files are transport diagnostics, not a new task ledger. A missing completion record is an interrupted or incomplete attempt, never success. Keep the directory until the Shared memory post-spawn lifecycle has consumed diagnostics and archived the capture; the runner never cleans it up.

Runner exit zero is **not** a stage verdict: terminal events, provider errors inside JSON, stage contracts, usage, retries, metrics, and transcript harvest remain the orchestrator's responsibility. So do wall-clock timeout and cancellation of the entire child tree: supervise the runner command with the host's process facility, wait for confirmed termination, and then harvest. The runner deliberately provides no portable process-tree kill claim. Its `started` record does not remove the need to write an interrupted-attempt metrics row.

**Reference invocations.** Use POSIX sh / Git Bash, including from a PowerShell host: invoke the Git installation's `bin/sh.exe -lc` with `sh` and the shell-quoted absolute path of a UTF-8 launch script containing the shell form below. The login shell supplies Git's Unix utilities on PATH; bare `sh.exe` from PowerShell may not find them. The launch script lives in `SPAWN_TMP` and contains only properly shell-quoted argv, never interpolated prompt text. Do not pipe prompt text through PowerShell. Use absolute forward-slash paths on Windows; always quote paths. `$ARTIFACT_ABS` denotes the stage's output or the sanctioned `-` fallback above.

codex (POSIX sh / Git Bash; `$SEARCH` is `--search` for planner and both plan reviewers, empty for every other stem; `$WINSB` is empty on POSIX hosts and `-c windows.sandbox="unelevated"` on Windows):
```sh
CODEX_HOME="$SPAWN_TMP/codex-home" sh "$RUNNER" "$WORK_ROOT_ABS" "$SPAWN_TMP" events.jsonl "$ARTIFACT_ABS" -- \
  codex $SEARCH exec -s workspace-write -C "$WORK_ROOT_ABS" -m "$MODEL" \
  -c model_reasoning_effort="$EFFORT" --ignore-user-config -c project_doc_max_bytes=0 $WINSB --ephemeral \
  --json -o "$SPAWN_TMP/last-message.md" -
```

- `--search` is a **top-level** codex flag (before `exec`), not an exec flag. Only `planner` and the two plan reviewers get it (their contracts require web verification).
- The isolation measures are mandatory as a set: `-c project_doc_max_bytes=0` (repo `AGENTS.md`), the private `CODEX_HOME` holding only `auth.json` (user-level instructions and config), and `--ignore-user-config` (config layering). Never drop any of them.
- **A write refusal is not a sandbox degradation.** First check that the child's write targets are inside `WORK_ROOT_ABS`, not `SPAWN_TMP`; then check that Windows spawns received `-c windows.sandbox="unelevated"`. Only after both are ruled out is a refusal a genuine read-only environment.
- No `--skip-git-repo-check`: a repo-check failure means `WORK_ROOT` is wrong — stop and investigate.

claude (POSIX sh / Git Bash):
```sh
sh "$RUNNER" "$WORK_ROOT_ABS" "$SPAWN_TMP" events.jsonl "$ARTIFACT_ABS" -- \
  claude -p --model "$MODEL" --effort "$EFFORT" --permission-mode acceptEdits \
  --setting-sources "" --no-session-persistence --output-format stream-json --verbose
```

The runner sets cwd for both providers. The empty `--setting-sources` argument is passed by sh directly, avoiding PowerShell 5.1's empty-argument dropping. Run the isolation canary through this runner once per machine before trusting it; accepting the CLI flag alone does not prove isolation.

- Sandbox/permissions: every stage gets a writable workspace — all stages write artifacts into `{TASK_DIR}` (inside `WORK_ROOT` in both persistence modes). Codex sandbox is always `workspace-write`; claude runs `acceptEdits`. Role discipline ("review stages don't modify code files") is enforced by the role body + downstream review — the same trust model the native path uses — not by the OS sandbox.
- **Windows note (corrected 2026-07-28, codex 0.145).** An earlier revision of this contract claimed nested codex "degrades `workspace-write` to read-only on Windows" and treated that as the normal case. It does not. Every observed refusal came from the two by-design rules above — a write target outside the workspace, or an unset `windows.sandbox` — and with the invocation as written here, nested codex writes normally on Windows, `implementer` and `fixer` included. Materialization stays in the contract as a fallback for a genuinely read-only environment, **not** as the expected Windows path; do not reach for it before the two checks above come back clean. For **single-artifact stages** (clarifier, premise-challenge, planner, both plan reviewers, code-reviewer, qa-report) the sanctioned fallback is **materialization**: instruct the agent that its complete artifact IS its final message, then the orchestrator takes codex `last-message.md` or claude's terminal `result` string from `events.jsonl`, writes that text verbatim to the expected artifact path and validates it per the stage contract. Never use this fallback for implementer/fixer (they must mutate the workspace — a read-only degradation there is a fatal preflight/spawn failure, not something to materialize around).
- Timeout: `spawn_timeout_min` (default 30; 2× for codex `ultra`) wall-clock per spawn; on expiry kill the process, record `timeout` in metrics, and apply the failure flow below.
- **Host tool limits are not spawn failures.** If your host's shell tool caps a single call below the spawn timeout (e.g. a 10-minute cap per call), wait in **repeated blocking segments** on the same spawn — re-invoke a wait/liveness check each time the tool call expires — never background the spawn and never declare failure on a tool-call timeout. Before writing `SPAWN_FAILURE.md` for any external spawn, verify the spawn **process actually exited**; a live process means your wait expired, not the spawn — resume waiting (observed live: an orchestrator wrote a failure record for a reviewer that was still running and later delivered its artifact).

**Success criteria (all four required):**

1. Runner exit code 0 and recorded child exit code 0 (native dispatch: successful tool completion).
2. A valid terminal event in `events.jsonl`: codex `turn.completed`; claude `type: result` with `subtype: success` and `is_error: false`. Parse JSON; progress labels do not establish success. A provider error inside JSON is a failed attempt even when the process exits zero.
3. The expected artifact file(s) exist **and are newly created by this spawn** — before spawning, if the expected artifact already exists (retry/resume), rename it to `<name>.prev-<n>.md` first.
4. The artifact passes its stage contract (see Stage artifact contracts below).

**Failure classification and flow.** Classify before reacting:

| Class | Examples | Reaction |
|---|---|---|
| fatal (auth / config / profile / isolation) | login expired mid-run, CLI rejects a flag, unverified-profile model rejected by provider | **no retry** — straight to the failure report |
| transient execution | nonzero exit with work started, missing/malformed artifact, no terminal event | **retry once** (same profile), with an explicit instruction appended to write the output file before finishing |
| timeout | wall-clock cap hit, process killed | retry once |
| user cancellation | — | no retry; report and stop (task stays where it is if before Step 0.8, else user decides) |

Both attempts use the Shared memory post-spawn lifecycle and get metrics rows. When the reaction is exhausted (fatal, or the retry also fails): use the retained stderr tail and archived partial transcript filename (or `transcript:missing`) in `{TASK_DIR}/SPAWN_FAILURE.md` (stage, resolved profile, failure class, exit status/terminal event, last ~30 lines of stderr), then move the task to `blocked/` using the same mechanics as the QA NEEDS_FIXES path (worktree-aware, both persistence modes — including the local-only copy-back rule from Step 10, commit in git-tracked mode), reconcile the roadmap, and report to the user. This flow applies to native-path spawn failures too (it generalizes the old "retry once" rule).

**Usage parsing for metrics:** codex — from the `turn.completed` event's `usage` object (`input_tokens`, `cached_input_tokens`, `output_tokens`, `reasoning_output_tokens`); claude external — from the terminal `type: result` event's usage fields in `events.jsonl`; duration — your own wall-clock around the process. Parse failure → `n/a` cells, never a blocked pipeline.

### Stage artifact contracts

Applied as success criterion 4 on both native and external paths. "Fresh" = created by this spawn (criterion 3). Verdict strings are exact.

| Stem | Artifact (in `{TASK_DIR}`) | Contract |
|---|---|---|
| clarifier | `TASK_FINAL.md` | fresh, non-empty; `## Open questions` section triggers the user relay in Step 2 |
| premise-challenge | `PREMISE_CHALLENGE.md` | fresh, non-empty; contains verdict `PREMISE HOLDS` or `PREMISE SUSPECT` |
| planner | `PLAN.md` | fresh, non-empty |
| plan-reviewer-1 | `PLAN_V2.md` | fresh, non-empty |
| plan-reviewer-2 | `PLAN_FINAL.md` | fresh, non-empty |
| implementer | `IMPL_SUMMARY.md` | fresh, non-empty; `Verdict: PLAN_BLOCKED` triggers the pause in Step 6 |
| code-reviewer | `IMPL_REVIEW.md` | fresh, non-empty; contains verdict `PASS`, `NEEDS_WORK`, or `FAIL` |
| fixer | `FIX_SUMMARY.md` | fresh, non-empty |
| qa | `QA_REPORT.md` | fresh, non-empty; contains verdict `SHIP`, `NEEDS_FIXES`, or `REJECT` |

Deeper structure (headings, finding lists) is each body's own output contract; the orchestrator checks existence, freshness, and the verdicts it branches on — it does not lint prose.

### Hosting (which harness is running this orchestrator)

This SKILL.md is installed on two surfaces: `.claude/skills/` (Claude Code) and `.agents/skills/` (Codex CLI). Determine your host once at startup — you know which harness you are.

- **Hosted in Claude Code:** native path available for provider=claude (Task tool + named subagents). Any codex-provider stage → external runner (`codex exec`).
- **Hosted in Codex CLI:** there is no Task-tool/named-subagent mechanism in this pipeline's contract — **every** stage goes through the external runner: claude-provider stages via `claude -p`, codex-provider stages via `codex exec` (yes, codex-under-codex uses the external one-shot too: it guarantees a fresh context, the isolation flags, and parseable usage). Effort for claude external spawns is the `--effort` flag — subagent variants are irrelevant on this host.

  **The Codex host itself is not context-isolated, and that is accepted.** An interactive `codex` session loads the operator's `$CODEX_HOME/AGENTS.md` plus any repo `AGENTS.md` at startup, and neither can be suppressed from inside the session (`--ignore-user-config` and `project_doc_max_bytes` are `exec`-only / project-only; the user-level doc has no off switch at all). So the orchestrator running under Codex always carries the operator's personal instructions. This is deliberate: the host is the operator's own seat, the same way a Claude Code host carries the user's `CLAUDE.md`. Two rules make it safe:

  - **This SKILL.md outranks ambient instructions for anything it specifies** — pipeline order, mode gates, artifact contracts, folder state machine, commit policy, spawn flags. An `AGENTS.md` line that conflicts (e.g. "never commit", "always run tests before finishing", "delegate to sub-agents") does not override the contract; if you cannot reconcile the two, stop and tell the user which instruction conflicts with which step instead of silently picking one.
  - **Ambient instructions never reach the pipeline.** They stay in the host process: every stage is an external spawn with its own isolation (private `CODEX_HOME`, `project_doc_max_bytes=0`), so no agent inherits them. Do not paraphrase host `AGENTS.md` content into spawn prompts — that would smuggle it in through the back door.

  **Windows sandbox model (verified live, codex 0.145):** a sandboxed Codex host cannot run this pipeline on Windows. Its sandbox executes child processes as a separate sandbox user (`CodexSandboxOffline`) whose ACLs cannot read the real user's `~/.codex` or `~/.claude` credentials — every nested provider auth check fails, and this is correct security, not a bug; `shell_environment_policy` cannot fix it (setting `CODEX_HOME` still hits `UnauthorizedAccess`). `workspace-write` additionally protects `.git`, so state-machine commits fail from a sandboxed host. Therefore hosting MAW under Codex on Windows requires the operator to launch the orchestrator with the sandbox disabled (a deliberate trusted-local-run decision, equivalent to a permissive Claude Code permission mode). Nested `codex exec` children, by contrast, write normally on Windows when spawned as the runner contract specifies (private `CODEX_HOME` + `-c windows.sandbox="unelevated"`, write targets inside the workspace) — the "nested children are always read-only" claim in an earlier revision was a misdiagnosis, corrected 2026-07-28. `claude -p` children are not codex-sandboxed and write artifacts directly.

Everything else — mode gates, artifact contracts, folder state machine, metrics, PCTX overlay — is host-independent. When a state-mutation snippet in this file is written in bash and your host shell is PowerShell, apply the intent with the PowerShell equivalent (quoted absolute paths; `Move-Item`/`Copy-Item`/`New-Item -Force`; `git` commands are identical).

### Step 0 — Pick a task

**If the user passed a task number or ID** (e.g. `/maw-execute-task 3`, `/maw-execute-task 003`, `/maw-execute-task TASK-003`): normalize it to `TASK-NNN` (zero-pad to 3 digits) and look for the matching folder in `maw/tasks/pending/`. If not found there, also check `maw/tasks/blocked/` — running `/maw-execute-task TASK-003` on a blocked task is a valid way to retry it. **Do not move it yet** — read it in place; the single move `blocked/ → in_progress/` happens at Step 0.8 like every other start. If the task exists in `in_progress/` or `done/`, refuse and report to the user. If the ID matches nothing, list available pending/blocked IDs and stop.

**Otherwise (no arg):** scan `maw/tasks/pending/` for task folders. Read each `task.md` to find priorities. Pick the highest-priority task (or the first one if priorities are equal).

If no pending tasks exist, report that to the user and stop.

**Do NOT move the folder yet.** The task stays in `pending/` (or `blocked/`, for a retry) until every pre-spawn check passes — Steps 0.5, 0.6, and 0.65 run against the task **in place**, so any failure (invalid mode, clamp violation, missing/unauthenticated provider) leaves the board untouched and nothing half-started gets committed. The move, its commit, and the roadmap reconcile all happen in Step 0.8.

**Read the `Mode:` field** from the task's `task.md` (in place). Store as `MODE`. If missing, default to `full`. Valid values: `full`, `small-fix`, `brainstorm`, `deep-research`. Any other value -> stop and report to the user.

Also read the `Type:` field — useful for agent context but does not affect pipeline shape. Read the optional `Domains:` line if present (comma-separated domain names) and store it as `DOMAINS` — Step 0.7 uses it to pre-inject project-context domain modules. Missing line → no pre-injected domains (the Step 0.7 catalog still covers self-load). Read the optional `Providers:` / `Models:` / `Effort:` lines now too — Step 0.6 consumes them.

### Step 0.5 — Check worktree mode

**CLI override:** If the user invoked `/maw-execute-task --worktree`, set `USE_WORKTREE=true` and skip the rest of this step. If `/maw-execute-task --no-worktree`, set `USE_WORKTREE=false` and skip.

Read `maw/settings.json`. If the file does not exist or `worktree_mode` is missing:

1. Ask the user:
   ```
   How should the pipeline handle branching?
   1. Worktree (default) — create a git worktree for each task. Isolated from main, safe for parallel work.
   2. Branch only — checkout a feature branch directly, no worktree. Simpler, but blocks the main working tree.
   3. Ask each time — prompt before every task.
   ```
2. Save the answer to `maw/settings.json`:
   ```bash
   mkdir -p maw
   cat > maw/settings.json << 'EOF'
   {
     "worktree_mode": "always"
   }
   EOF
   ```
   (replace `"always"` with `"never"` or `"ask"` based on user's choice). If the file already exists with other keys — a user may pre-create it with only `shared_memory` or `runner_progress` — merge `worktree_mode` into it instead of overwriting.

If `worktree_mode` is `"ask"`, ask the user now:
```
Use worktree for this task, or branch only?
```

Store the effective choice for this run in a variable `USE_WORKTREE` (true/false). All subsequent steps use this variable.

### Step 0.6 — Resolve the per-agent profile (provider, model, effort)

**First-run config.** Read `maw/settings.json`. If it has legacy v1 fields, migrate (see Settings). If `providers` is missing and there is nothing to migrate, ask the user once:

```
1. Model for pipeline agents?
   a. Sonnet (default) — all 9 agents on sonnet.
   b. Customize — sonnet by default, pick a different model for specific agents.
2. Effort level for pipeline agents?
   a. Medium (default) — real effort, no per-agent tuning.
   b. Customize — medium by default, raise/lower effort for specific agents.
```

For each "Customize", ask which agents and which value, then write schema-v2 `maw/settings.json`, preserving `worktree_mode` (read the existing file first, merge — do not clobber other fields). Asked only once — on later runs the fields are present and this prompt is skipped. (Providers beyond the host are never configured by interrogation — the user adds them to settings or task.md when they want them.)

**Per-task overrides.** `task.md` may carry optional header lines:

```
Providers: default=codex, premise-challenge=claude
Models: default=gpt-6-luna, code-reviewer=gpt-6.1-sol
Effort: code-reviewer=xhigh
```

Parse each line as comma-separated tokens: `default=<v>` (or a bare `<v>`) sets the task-wide value for that dimension; `<agent-name>=<v>` sets it for one agent. Missing line / missing token → no per-task value at that level. Unknown token syntax → stop and report.

**Resolution algorithm (per agent). The profile is atomic — resolve provider first, then model/effort within that provider's scope:**

1. **Provider**: task.md per-agent > task.md task-wide > `settings.agents.<n>.provider` > `settings.default_provider` > host harness. (`"host"` resolves to the harness running this orchestrator.)
2. **Model and effort — explicit-wins-or-fails:**
   - A value is **explicit for this agent** if it came from task.md per-agent (`<agent>=v`) or `settings.agents.<n>`. An explicit value that is invalid for the resolved provider → **stop and report** the exact pair (e.g. "code-reviewer: model `opus` is not a codex model"). Never silently substitute.
   - A value is **inherited** if it came from task.md `default=` or a provider default. An inherited value invalid for the resolved provider → fall through to `providers.<p>.default_model` / `default_effort`, then to built-ins (`claude: sonnet/medium`, `codex: gpt-6.1-sol/medium`). A task-wide `Models: default=opus` therefore means "opus wherever the provider is claude" and does not break the one codex agent.
3. **Clamp** the resolved triple against the Provider capability catalog (see that section). Any violation → stop and report.

**Normative examples (truth table):**

| Situation | Result |
|---|---|
| zero-config, Claude Code host | every agent (claude, sonnet, medium) — same resolved profiles as v1 |
| zero-config, Codex host | every agent (codex, gpt-6.1-sol, medium) |
| `Providers: code-reviewer=codex`, nothing else | code-reviewer (codex, gpt-6.1-sol, medium); rest host defaults |
| `Providers: code-reviewer=codex` + `Models: default=opus` | code-reviewer (codex, gpt-6.1-sol, medium); rest (claude, opus, medium) |
| `Providers: code-reviewer=codex` + `Models: code-reviewer=opus` | HARD FAIL — explicit cross-provider contradiction |
| migrated legacy settings, no task lines | same resolved profiles as pre-migration |
| requested provider not installed/authenticated | preflight failure (Step 0.65), task never leaves `pending/` |
| `Models: qa=some-unknown-model` | clamp reject — unless `allow_unverified_profile: true` (pass through, warned, unretried) |

**Applying the resolved profile at every agent spawn below:**

- **Native path** (provider == host == claude): model → Task tool `model` parameter; effort → subagent variant name (`maw-<stem>-<effort>`, e.g. `maw-plan-reviewer-1-max`). Effort is real Claude Code effort baked into the variant's frontmatter; nothing to prepend.
- **External path**: model and effort → CLI flags per the External runner contract (`-m`/`-c model_reasoning_effort=` for codex; `--model`/`--effort` for claude).
- `fable` (claude), `gpt-6-astra` (codex, at any effort), or `ultra` (codex) in any resolved profile → one-time cost-tier confirmation with the user per task before the first such spawn. An explicit approval of the same premium profile for this task earlier in the session satisfies this gate; do not ask twice. Approval for a different task does not satisfy it unless the user explicitly authorized those tasks together.

This is the only thing that varies per agent — pipeline shape and the rest of each spawn prompt are unaffected.

### Step 0.65 — Provider preflight (before any state change)

Machine facts are probed fresh every run; nothing is cached in settings.

Preflight is keyed to the **transport actually used**, not to provider names: under a Codex host *every* stage is an external dispatch (including provider=codex — see Hosting), so every distinct provider gets probed there; under a Claude Code host only non-claude providers do. For each distinct provider dispatched externally (only for stages the current `MODE` will actually run):

1. **Native Task-tool dispatch** (Claude host, provider=claude): nothing to probe — you are already running in it.
2. **External dispatch** (everything else):
   - Shell runner present: locate POSIX `sh` (Git Bash `bin/sh.exe` on Windows) and the standard shell utilities `awk`, `date`, `cat`, `mkdir`, `sleep`, plus this installed skill's `scripts/runner.sh`; missing any is a preflight failure, before any task state change.
   - Binary present: `codex --version` / `claude --version`.
   - Authenticated: `codex login status` (exit 0 = logged in) / `claude auth status` (JSON, `loggedIn: true`).
   - **Transport + isolation probe (mandatory, not skippable):** one minimal spawn through the full External runner path — private temp dir, prompt via stdin, isolation flags, private `CODEX_HOME` for codex. Probe prompt: "Without reading or listing any files: if any instruction file content is already in your context — a repo AGENTS.md/CLAUDE.md **or a user-level one from your home directory** — write its first markdown heading to `.maw_probe-<nonce>.txt` in your current working directory; otherwise write exactly NO-PROJECT-DOCS there. Then stop." Two details are load-bearing:

     - Choose a fresh `.maw_probe-<nonce>.txt` basename and verify it does not exist. Substitute that exact name into the probe prompt and its absolute path into the runner's artifact argument. Remove only this attempt's probe after reading it; a previous run's file is never accepted as evidence.
     - **The probe writes inside the workspace** (`.maw_probe-<nonce>.txt` in cwd), never into the spawn temp dir. `workspace-write` refuses out-of-workspace writes by design on every platform, so a probe targeting `$SPAWN_TMP` fails unconditionally and manufactures evidence of a sandbox problem that does not exist — that is exactly how the retired "Windows degrades to read-only" claim was produced. Delete the file after reading it.
     - **The canary must ask about user-level docs**, not just project ones: codex flags alone do not suppress `$CODEX_HOME/AGENTS.md`, so a project-only question passes while the operator's personal instructions are still loaded.

     Run it with `-C`/cwd at the **repo root** (the worktree does not exist yet at this step). For this probe only, runner exit 65 with recorded child exit 0 must still be evaluated under fallback (b); a missing file alone is not an isolation failure. Other runner failures do not qualify. Success, in order of preference: (a) the file exists and contains `NO-PROJECT-DOCS` — the normal outcome, including on Windows; or (b) the file could not be created **and** the two by-design refusals are ruled out (target was in-workspace; `windows.sandbox` was passed), but the spawn's final message contains exactly `NO-PROJECT-DOCS` — isolation is proven against a genuinely read-only environment and this provider's stages run in **materialization mode** on this host (record `ok (materialized)` in metrics outcomes). Clause (b) is the rare path, not the expected one. Any other outcome — the canary quotes project or user docs, or `NO-PROJECT-DOCS` appears nowhere — is a fatal preflight failure (cross-provider dispatch does not run). **On a write refusal, report the diagnosis, not a verdict:** state which of the two by-design rules was checked and quote the child's stderr; the tell is in its second half — `rejected by user approval settings` points at configuration, not at a removed sandbox. Note that project trust (`[projects.*] trust_level`) does not gate writes and adding trust entries is not a fix. This single probe validates transport mechanics (child process, stdin encoding, flags accepted, filesystem access) **and** the ambient-context isolation canary, per machine, before the board is touched. Probe tokens are discarded; log one line.

**Auth & data policy (v1).** While checking auth, also *identify the auth mode* (codex: `codex login status` output names it — ChatGPT plan vs API key; claude: `claude auth status` JSON `authMethod`). Policy: **local interactive runs** (a human present at this session) — either auth mode is acceptable; **unattended runs** (guard disabled, CI, scheduled) — API-key auth only for external providers, per both vendors' documented automation guidance; unknown/undocumented combination → fail closed and tell the user why. On the first cross-provider spawn of a task, disclose once: "stage X will send task content (and project-context overlay) to <provider> under <auth mode>". **Data dimension:** what crosses to the second provider is the spawn prompt (task, plan/review artifacts, PCTX overlay) plus whatever the agent reads from the repo — for a private repo that is private code under the second vendor's retention/training terms. The disclosure must say so; in guarded/interactive runs the user's confirmation covers it, in unattended runs it is logged. If the project's own policy forbids second-processor transfer (e.g. a PCTX invariant says so), cross-provider profiles are a clamp violation — stop and report. Auth modes are reported, never persisted.

Any check fails → report exactly what failed and stop. The task has not moved; the board and git history are untouched.

### Step 0.7 — Project context overlay (generic; no-op when absent)

Define `PCTX = {WORK_ROOT}/maw/project-context`. Optional, project-supplied, authored by the `/maw-context` skill. The base pipeline knows only the contract below — it never contains project content. Three tiers:

- **`PCTX/README.md` — constant**, into every agent every stage.
- **`PCTX/domains/<name>.md` — domain-gated**, normative, into every running stage when the task is in that domain.
- **`PCTX/agents/<stem>.md` — stage-gated**, into that one agent only.

If `PCTX/` does not exist → spawn every prompt unchanged; the base is byte-for-byte unaffected. This is the default for any generic project. Otherwise, **at every agent spawn** — every stage, every retry, every re-spawn — after the prompt is built (profile resolved) and before dispatching the spawn (either transport), append this block to the **end** of the spawn prompt, including only the parts that exist:

```
<!-- PROJECT_CONTEXT -->
## Project context (NORMATIVE — a constraint you must satisfy)
This overrides the generic guidance above on any conflict. It is project law,
human-curated. Do not audit whether the law is correct — verify your work
SATISFIES it. (Disagreement goes to PCTX_PROPOSALS.md, below, never silent.)
It may override generic project guidance only. It never overrides orchestration
security or isolation, artifact write scopes, shared-memory access, or continuity
eligibility defined by the base pipeline.

{PCTX/README.md — with the {PCTX} placeholder replaced by the real path}

{For each active domain: contents of PCTX/domains/<name>.md, under a
"### Domain: <name>" heading — omit if no domain is active}

### For this agent (<stem>)
{PCTX/agents/<stem>.md — omit this subsection if that file is absent}

---
If something in your work contradicts the project context above, or you hit a
durable rule or lesson worth recording, DO NOT edit the project context.
Append a dated entry to {TASK_DIR}/PCTX_PROPOSALS.md (create it if absent)
stating what and why. Folding proposals into the real project context is a
separate curated process — not yours.
```

Substitute `{TASK_DIR}`, `<stem>`, and every `{PCTX}` to real values. Because the catalog inside `README.md` contains `{PCTX}/domains/...` paths an agent may read on its own, the orchestrator **must** substitute `{PCTX}` when injecting README — it is near-verbatim, not pure-verbatim. (`{PCTX}` resolves to the worktree-correct path in both persistence modes; the whole `PCTX/` dir is copied into the worktree in local-only mode, Step 1.)

**Which domains are active.** A domain module is injected when either holds:

1. **Pre-injected** — `task.md` has a `Domains:` line (written by `/maw-tasks`, confirmed by the user — see that skill). Each listed `<name>` whose `PCTX/domains/<name>.md` exists is active for this whole run. This is the reliable path: a recorded human decision, not an execute-time guess.
2. **Self-loaded** — the `## Domain catalog` in `README.md` (always injected, since README is constant) lists `trigger → {PCTX}/domains/<name>.md` with observable triggers and a HARD RULE telling the agent to read the mapped module from disk before working any part that matches a trigger. This is the recall safety net for a task that wanders into a domain `task.md` did not declare. The agent self-loads; you do not predict it.

You are not asked to guess domains from prose. Pre-inject only what `task.md Domains:` declares; the catalog covers the rest.

**Precedence (generic; same lattice as model/effort in Step 0.6):** `task.md` inline override > project context > base/agent default for project guidance. Project context never overrides orchestration security or isolation, artifact write scopes, Shared memory access, or continuity eligibility. The injected header states this boundary so it is visible, not silent.

This is the only project-specific seam: conditional reads plus one append plus `{PCTX}` substitution. Agent bodies are never modified for project specifics.

### Step 0.8 — Move the task to in_progress (first state change)

Everything above passed. Now:

```bash
TASK_ID="TASK-001"  # replace with actual ID; source dir is pending/ or blocked/ (retry)
mkdir -p maw/tasks/in_progress
mv "maw/tasks/pending/$TASK_ID" "maw/tasks/in_progress/$TASK_ID"   # or maw/tasks/blocked/$TASK_ID
```

(PowerShell host: `New-Item -ItemType Directory -Force maw\tasks\in_progress; Move-Item -LiteralPath "maw\tasks\pending\$TASK_ID" "maw\tasks\in_progress\$TASK_ID"`.)

**Roadmap reconcile.** If `maw/ROADMAP.md` exists: check it against the `## Dependencies` sections of the remaining `maw/tasks/pending/` task.md files (`task.md` is source of truth; regenerate on disagreement — never edit a task.md to match the graph), and drop the task just moved out of the pending graph. If it does not exist, skip — it is optional and maintained by `/maw-tasks`.

**If `maw/` is NOT in `.gitignore`** (git-tracked mode):
```bash
git add maw/ && git commit -m "task: start $TASK_ID"
```

**If `maw/` IS in `.gitignore`** (local-only mode): skip the commit — files are not tracked.

### Step 1 — Create branch (and worktree if enabled)

Read the `Branch:` field from the task's `task.md` to get the branch name (e.g. `feature/add-rate-limiting`).

**If `USE_WORKTREE` is true (worktree mode):**

```bash
TASK_ID="TASK-001"           # replace with actual ID
BRANCH="feature/add-rate-limiting"  # from task.md Branch: field
WORKTREE_DIR=$(echo $BRANCH | tr '/' '-')  # feature-add-rate-limiting
WORK_ROOT=".worktrees/$WORKTREE_DIR"

# Before removing a stale task worktree, apply the in_progress form of the
# pre-worktree-removal transcript rescue below if that task directory exists.
git worktree remove --force $WORK_ROOT 2>/dev/null || true
git branch -D $BRANCH 2>/dev/null || true
git worktree add $WORK_ROOT -b $BRANCH
```

**If local-only mode** (`maw/` IS in `.gitignore`): `maw/` is gitignored, so the freshly-added worktree does **not** contain it. Copy the task folder and the project-context overlay (if present) into the worktree, or every agent — and the Step 0.7 overlay — will silently see nothing:

```bash
mkdir -p $WORK_ROOT/maw/tasks/in_progress
cp -r maw/tasks/in_progress/$TASK_ID $WORK_ROOT/maw/tasks/in_progress/
[ -d maw/project-context ] && cp -r maw/project-context $WORK_ROOT/maw/
[ -f maw/ROADMAP.md ] && cp maw/ROADMAP.md $WORK_ROOT/maw/
```

**If git-tracked mode** (`maw/` NOT in `.gitignore`): nothing to copy — both are already in the checkout.

All subsequent agents work exclusively inside `$WORK_ROOT/`. They must not touch the main branch.

The task folder is available at `$WORK_ROOT/maw/tasks/in_progress/$TASK_ID/` — this is where all artifacts are written. Create `metrics.md` there now (see the Metrics ledger section), then, unless `shared_memory` is `false`, create the Shared memory scaffolding before any agent is spawned. In local-only mode do this after the copy-in above. Initialization is idempotent: create only missing files/directories; never truncate `log.jsonl`, delete scratch, or replace an existing transcript. Use BOM-free UTF-8 for `log.jsonl`, exact `transcripts/.gitignore` content from Shared memory, and the listed binary/dump patterns for `scratch/.gitignore`.

Define shorthands for prompts:
- `TASK_DIR=maw/tasks/in_progress/$TASK_ID`
- `WORK_ROOT=.worktrees/$WORKTREE_DIR`
- `WORK_ROOT_ABS=$(cd "$WORK_ROOT" && pwd)` — canonical absolute form; external spawns use this for `-C`/cwd and for all paths in their prompts (PowerShell: `(Resolve-Path $WORK_ROOT).Path`)

**If `USE_WORKTREE` is false (branch-only mode):**

```bash
TASK_ID="TASK-001"           # replace with actual ID
BRANCH="feature/add-rate-limiting"  # from task.md Branch: field

git checkout -b $BRANCH
```

All subsequent agents work in the repo root directory. They must not push to main.

The task folder is available at `maw/tasks/in_progress/$TASK_ID/` — this is where all artifacts are written. Create `metrics.md` there now (see the Metrics ledger section), then, unless `shared_memory` is `false`, create the Shared memory scaffolding before any agent is spawned. Initialization is idempotent: create only missing files/directories; never truncate `log.jsonl`, delete scratch, or replace an existing transcript. Use BOM-free UTF-8 for `log.jsonl`, exact `transcripts/.gitignore` content from Shared memory, and the listed binary/dump patterns for `scratch/.gitignore`.

Define shorthands for prompts:
- `TASK_DIR=maw/tasks/in_progress/$TASK_ID`
- `WORK_ROOT=.` (repo root)
- `WORK_ROOT_ABS=$(pwd)` — external spawns use the absolute form (PowerShell: `(Get-Location).Path`)

---

**From this point forward, all paths in agent prompts use `{WORK_ROOT}` and `{TASK_DIR}`.** In worktree mode `WORK_ROOT` is `.worktrees/{WORKTREE_DIR}`, in branch-only mode it is `.` (the repo root).

This scaffolding runs in every mode, including `small-fix`, `brainstorm`, and `deep-research`; it also upgrades an in-flight task from an older MAW version on the next orchestrator touch.

### Step 2 — Clarifier agent (conditional)

**Mode gate:** skip this step entirely if `MODE` is `small-fix` or `deep-research`. In `small-fix`, `task.md` IS the spec and is used directly by the Implementer. In `deep-research`, the Planner works directly from `task.md` without a clarification pass.

For `full` and `brainstorm`: spawn only if the task description is thin (no acceptance criteria, no technical context, ambiguous scope). Skip if already detailed enough.

Spawn `clarifier`: `subagent_type=maw-clarifier-<effort>` (effort/model resolved per Step 0.6), `prompt` built per "How to build a spawn prompt" — path header + full Shared memory block + inline `task.md` as "Task:". Use the Shared memory post-spawn lifecycle. You do not read the agent body.

**After agent finishes:** read `{WORK_ROOT}/{TASK_DIR}/TASK_FINAL.md`. If it contains a non-empty `## Open questions` section — present those questions to the user, wait for answers, then append them under `### Resolved questions` and remove the `## Open questions` section. (The clarifier is a subagent and cannot ask the user directly — relaying its questions is the orchestrator's job, same pattern as Step 3.)

If the clarifier is skipped **for any reason** — the thin-check pass in `full`/`brainstorm` **or the mode gate in `deep-research`** — write `{WORK_ROOT}/{TASK_DIR}/TASK_FINAL.md` with the original task content yourself. Downstream stages (both plan reviewers, planner question relay) reference `TASK_FINAL.md`; it must exist in every mode that reaches them. (`small-fix` needs no `TASK_FINAL.md`: its pipeline uses `task.md` as the spec throughout and never runs the plan reviewers.)

### Step 2.5 — Premise challenge (isolated; conditional)

**Mode gate:** skip if `MODE` is `small-fix` (scope is contained, no planning stage — the premise risk is low and is covered later by the repro discipline). Runs in `full`, `brainstorm`, `deep-research`. Runs **before** the planner on purpose: a rotten premise must be caught before any planning is spent on it.

Why this exists: every later stage verifies the *solution within the premise* and inherits the premise's lineage (task.md → TASK_FINAL → plan → reviews). Nothing else attacks the premise itself. This is the one isolated check that does, and the only thing that historically catches a wrong premise is a concrete counter-example from outside the lineage.

Spawn `premise-challenge`: `subagent_type=maw-premise-challenge-<effort>` (effort/model per Step 0.6), `prompt` built per the table — path header + reduced/write-only Shared memory block + inline the premise source as "Task — the premise under audit:". **Pass it only** the premise source (`TASK_FINAL.md` if it exists, else `task.md`), scratch, append-only log destination, and working/repo paths — **never** a transcript path, log-read permission, your own root-cause writeup, a summary, the plan, or any reviewer note. Use the Shared memory post-spawn lifecycle. The agent investigates primary sources (code at `file:line`, an executable result it runs, the raw failing artifact) itself; isolation from the lineage is the whole point. Do **not** add the "weaker agent" adversarial framing to the spawn prompt here — this agent has its own evidence-bound framing baked into its body; the adversarial framing is for solution reviewers only.

**After agent finishes:** read `{WORK_ROOT}/{TASK_DIR}/PREMISE_CHALLENGE.md`.

- Verdict `PREMISE HOLDS` → proceed to Step 3.
- Verdict `PREMISE SUSPECT` → **treat exactly like a FAIL verdict** (see Rules): pause, surface `PREMISE_CHALLENGE.md` to the user verbatim, wait for instructions. Do not spawn the planner. The premise, not the plan, is what is in question — the user decides whether to amend `task.md`/`TASK_FINAL.md` and re-run, or override.

### Step 3 — Planner agent

**Mode gate:** skip if `MODE` is `small-fix`.

**Source file:**
- `full` or `brainstorm`: `TASK_FINAL.md`
- `deep-research`: `task.md` directly

Spawn `planner`: `subagent_type=maw-planner-<effort>` (effort/model per Step 0.6), `prompt` built per the table — path header + full Shared memory block + inline the task source as "Task:". Use the Shared memory post-spawn lifecycle. For `deep-research` mode, prepend the **Deep-research directive** from the spawn-prompt section above (it lives in this SKILL.md now, not in the agent body).

**After agent finishes:** read `{WORK_ROOT}/{TASK_DIR}/PLAN.md`. If "Open questions" is non-empty — present to user, wait for answers, append to `TASK_FINAL.md` under `### Resolved questions`.

### Step 4 — Plan reviewer 1

**Mode gate:** skip if `MODE` is `small-fix`.

Spawn `plan-reviewer-1`: `subagent_type=maw-plan-reviewer-1-<effort>` (effort/model per Step 0.6), `prompt` built per the table — path header + reduced/write-only Shared memory block + the paths of `TASK_FINAL.md` (task spec) and `PLAN.md` (plan to review). It receives scratch and log append only: no transcript path and no log read. Use the Shared memory post-spawn lifecycle. These artifacts are referenced as paths, not inlined — the agent body has the mandatory-read discipline and loads them from disk itself. For `deep-research` mode, prepend the **Deep-research review directive** from the spawn-prompt section above.

### Step 5 — Plan reviewer 2 (final plan)

**Mode gate:** skip if `MODE` is `small-fix`.

Spawn `plan-reviewer-2`: `subagent_type=maw-plan-reviewer-2-<effort>` (effort/model per Step 0.6), `prompt` built per the table — path header + reduced/write-only Shared memory block + the paths of `TASK_FINAL.md` (task spec) and `PLAN_V2.md` (plan to review). It receives scratch and log append only: no transcript path and no log read. Use the Shared memory post-spawn lifecycle. The artifacts are referenced as paths, not inlined — the agent body loads them from disk itself. For `deep-research` mode, prepend the **Deep-research review directive** from the spawn-prompt section above.

### Step 6 — Implementer agent

**Mode gate:** skip if `MODE` is `brainstorm` or `deep-research`. Jump to Step 10.

Spawn `implementer`: `subagent_type=maw-implementer-<effort>` (effort/model per Step 0.6), `prompt` built per the table — path header + full Shared memory block + inline the spec as "Task:" and the plan as "Implementation plan:". Use the Shared memory post-spawn lifecycle. For `small-fix` mode, follow the small-fix row in the spawn-prompt table above (spec = `task.md`, plan = the small-fix fallback text).

**After agent finishes:** read `{WORK_ROOT}/{TASK_DIR}/IMPL_SUMMARY.md`. If it contains `Verdict: PLAN_BLOCKED` — **treat exactly like a FAIL verdict**: pause, surface `IMPL_SUMMARY.md` to the user verbatim, wait for instructions. Retain the transient agent id, resolved profile, and archive mapping while paused. If the user amends `PLAN_FINAL.md` and requests a re-run, apply Shared memory's continuity rule; if planning restarts or the profile changes, spawn fresh. Do **not** spawn the code-reviewer. The plan, not the code, is what is in question — the user decides whether to amend `PLAN_FINAL.md`, restart planning, or override. This is the implementer's pre-flight escape hatch for catching a broken-presupposition plan before wrong code materializes.

### Step 7 — Code reviewer (read-only)

**Mode gate:** skip if `MODE` is `brainstorm` or `deep-research`.

Spawn `code-reviewer`: `subagent_type=maw-code-reviewer-<effort>` (effort/model per Step 0.6), `prompt` built per the table — path header + full Shared memory block + the paths of the spec, `PLAN_FINAL.md`, and `IMPL_SUMMARY.md` (referenced as paths, loaded by the agent itself). Use the Shared memory post-spawn lifecycle. For `small-fix` mode, follow the small-fix row in the table: omit the plan line, spec = `task.md`.

### Step 8 — Implementation fixer

**Mode gate:** skip if `MODE` is `brainstorm` or `deep-research`.

Spawn `fixer`: `subagent_type=maw-fixer-<effort>` (effort/model per Step 0.6), `prompt` built per the table — path header + full Shared memory block + inline the spec as "Task:" and the plan as "Final plan:", plus the path of `IMPL_REVIEW.md` (loaded by the agent itself). Use the Shared memory post-spawn lifecycle. For `small-fix` mode, follow the small-fix row: spec = `task.md`, plan = the small-fix fallback text.

### Step 9 — QA agent

**Mode gate:** skip if `MODE` is `brainstorm` or `deep-research`.

Spawn `qa`: `subagent_type=maw-qa-<effort>` (effort/model per Step 0.6), `prompt` built per the table — path header + full Shared memory block + the paths of the spec, `PLAN_FINAL.md`, `IMPL_SUMMARY.md`, `IMPL_REVIEW.md`, and `FIX_SUMMARY.md` (referenced as paths, loaded by the agent itself). Use the Shared memory post-spawn lifecycle. For `small-fix` mode, follow the small-fix row: omit the plan line, spec = `task.md`.

### Step 10 — Wrap up

**First, regardless of mode or verdict:** append the per-provider `**SUBTOTAL**` rows and the final `**TOTAL**` row to `{WORK_ROOT}/{TASK_DIR}/metrics.md` (see the Metrics ledger section) before the status-move commands below, so the totals land in the same commit as the final status move.

**Also regardless of mode or verdict:** if `{WORK_ROOT}/{TASK_DIR}/OPEN_DECISIONS.md` exists, surface it in your final report — every entry verbatim, not a summary. These are the calls you made instead of stopping to ask (see Turn discipline); wrap-up is where the user gets to overrule them, and an entry the user never sees is the same as never having recorded it. Absent file → nothing to surface, which is the normal case for a task with no judgement calls.

**Also regardless of mode or verdict:** if `maw/ROADMAP.md` exists, regenerate it after the status move from the remaining `maw/tasks/pending/` task.md `## Dependencies` sections (same generation rule as `/maw-tasks` Step 5). This task has now left `in_progress/`, so its pending dependents must be re-derived — a `blocked by` whose blocker is now in `done/` is satisfied and that edge drops; one whose blocker went to `blocked/` stays, annotated. This is the symmetric counterpart to the Step 0 reconcile (Step 0 handles `pending→in_progress`, this handles `in_progress→done|blocked`). In git-tracked mode include it in the same status-move commit (`git add maw/`). If `maw/ROADMAP.md` does not exist, skip.

**Local-only + worktree rule (applies to every status move below, and to the failure flow's `blocked/` move).** In local-only mode the worktree's `maw/` is a **copy** (Step 1); the main tree's ignored `maw/` is authoritative. Moving only the worktree copy would strand the original in `in_progress/` and lose all artifacts when the worktree is removed. So after moving the task folder inside the worktree, sync back to the main tree before any cleanup:

```bash
# from the repo root; STATUS is done|blocked
mkdir -p "maw/tasks/$STATUS"
cp -r "$WORK_ROOT/maw/tasks/$STATUS/$TASK_ID" "maw/tasks/$STATUS/$TASK_ID"
rm -rf "maw/tasks/in_progress/$TASK_ID"
```
(PowerShell: `New-Item -ItemType Directory -Force "maw\tasks\$Status"; Copy-Item -Recurse -LiteralPath "$WorkRoot\maw\tasks\$Status\$TaskId" "maw\tasks\$Status\"; Remove-Item -Recurse -Force "maw\tasks\in_progress\$TaskId"`.)

**Roadmap in local-only + worktree:** never copy `ROADMAP.md` back from the worktree — the worktree has no `pending/` tasks (Step 1 copies only the active task), so a graph regenerated there would be built from nothing and would clobber the real one. Regenerate the roadmap **in the main tree, after the copy-back**, from the main tree's `maw/tasks/pending/` — that is where the authoritative pending set lives.

Git-tracked mode needs none of this copy-back — the tracked status move is committed on the branch and arrives via merge. In branch-only + git-tracked mode, ignored `transcripts/` remains in the same task folder through the `mv`. Branch-only mode has no worktree to rescue. Local-only `cp -r` copies ignored files too, so `transcripts/`, `scratch/`, and `log.jsonl` already travel back. Transcript retention is unlimited in v1; nothing prunes the archives, so `done/` grows over time.

**Pre-worktree-removal transcript rescue (git-tracked + worktree only).** This is one status-aware invariant for every path that removes a task worktree, including Step 1 stale-worktree cleanup, SHIP merge cleanup, and blocked/failure cleanup. Immediately before `git worktree remove`, determine whether the task is under `in_progress/`, `done/`, or `blocked/` inside the worktree, create that matching task directory in the main tree, and copy/merge only `transcripts/` without overwriting an existing archive. Step 1 uses `in_progress`; wrap-up uses `done` or `blocked`. If the task directory or its transcript directory does not exist, there is nothing to rescue. Then remove the worktree. The rescue is required because ignored transcripts do not travel through a commit or squash merge and `git worktree remove --force` deletes ignored files.

POSIX, from the repository root with `STATUS=in_progress|done|blocked`:

```sh
mkdir -p "maw/tasks/$STATUS/$TASK_ID/transcripts"
cp -rn "$WORK_ROOT/maw/tasks/$STATUS/$TASK_ID/transcripts/." \
       "maw/tasks/$STATUS/$TASK_ID/transcripts/"
```

PowerShell 5.1, from the repository root:

```powershell
$Src  = "$WorkRoot\maw\tasks\$Status\$TaskId\transcripts"
$Dest = "maw\tasks\$Status\$TaskId\transcripts"
New-Item -ItemType Directory -Force $Dest | Out-Null
# No -Force and no wildcard with -LiteralPath: copy file by file and skip names already present.
Get-ChildItem -LiteralPath $Src -File -Recurse | ForEach-Object {
  $Relative = $_.FullName.Substring($Src.Length).TrimStart('\')
  $Target = Join-Path $Dest $Relative
  $TargetDir = Split-Path -Parent $Target
  New-Item -ItemType Directory -Force $TargetDir | Out-Null
  if (-not (Test-Path -LiteralPath $Target)) { Copy-Item -LiteralPath $_.FullName $Target }
}
```

**Mode gate for plan-only modes:** if `MODE` is `brainstorm` or `deep-research`:

1. Verify `{WORK_ROOT}/{TASK_DIR}/PLAN_FINAL.md` exists. If not, something went wrong — report to the user and stop.
2. Move the task folder to `done/`:
   ```bash
   cd $WORK_ROOT
   mkdir -p maw/tasks/done
   mv maw/tasks/in_progress/$TASK_ID maw/tasks/done/$TASK_ID
   ```
3. **If git-tracked mode:**
   ```bash
   git add maw/ && git commit -m "task: finalize $TASK_ID ($MODE)"
   ```
4. Report to the user: mode, task ID, one-line summary of PLAN_FINAL.md, list of artifacts (`TASK_FINAL.md` if present, `PREMISE_CHALLENGE.md` unless small-fix, `PLAN.md`, `PLAN_V2.md`, `PLAN_FINAL.md`).
5. Do NOT offer to merge — nothing was implemented. No branch merge is applicable unless the user explicitly asks (e.g. to keep the plan artifacts on main).
6. Stop here.

**Otherwise (`full` or `small-fix`):**

1. Read `{WORK_ROOT}/{TASK_DIR}/QA_REPORT.md`. Get the verdict.

2. If verdict is **SHIP**:
   - Move the task folder to `done/` inside the worktree:
     ```bash
     cd $WORK_ROOT
     mkdir -p maw/tasks/done
     mv maw/tasks/in_progress/$TASK_ID maw/tasks/done/$TASK_ID
     ```
   - **If git-tracked mode** (maw/ not in .gitignore):
     ```bash
     git add maw/ && git commit -m "task: complete $TASK_ID"
     ```
   - Report to the user with verdict + one-line summary + artifact list.
   - Ask if they want to merge:
     - **Worktree mode:** `git checkout main && git merge --squash $BRANCH && git commit`, then apply the pre-worktree-removal transcript rescue above before cleanup: `git worktree remove --force $WORK_ROOT && git branch -D $BRANCH`
     - **Branch-only mode:** `git checkout main && git merge --squash $BRANCH && git commit && git branch -D $BRANCH`

3. If verdict is **NEEDS_FIXES** or **REJECT**:
   - Move the task folder to `blocked/` inside the worktree:
     ```bash
     cd $WORK_ROOT
     mkdir -p maw/tasks/blocked
     mv maw/tasks/in_progress/$TASK_ID maw/tasks/blocked/$TASK_ID
     ```
   - **If git-tracked mode** (maw/ not in .gitignore):
     ```bash
     git add maw/ && git commit -m "task: block $TASK_ID — QA issues"
     ```
   - List the blocking issues and ask the user how to proceed.

---

## Metrics ledger

Every task folder carries a `metrics.md` next to `task.md`: `{WORK_ROOT}/{TASK_DIR}/metrics.md`. It is a pure accounting artifact — it is **never** substituted into any agent prompt, so agents do not see it. It rides with the task folder through every status move and, in git-tracked mode, is committed by the existing `git add maw/` at each transition (no extra commit logic).

**Create it once**, right after the task folder is in place in `in_progress/` (Step 1), before the first spawn:

```markdown
# Metrics — TASK-NNN

| # | Step | Agent | Provider | Model | Effort | Outcome | Tool uses | In-tok | Out-tok | Total-tok | Duration |
|---|------|-------|----------|-------|--------|---------|-----------|--------|---------|-----------|----------|
```

**After every agent spawn or continuation completes** — every agent, every step, every retry or re-spawn, both transports — append one row: incrementing `#`, step number, agent name (suffix `(retry)` / `(re-spawn N)` when applicable), resolved provider/model/effort, a short outcome (a verdict like `PASS`/`SHIP`/`PREMISE HOLDS`/`PLAN_BLOCKED`, or `ok` / `no-output` / `timeout` / `spawn-fail(exit=N)`), then the numeric columns per transport. A continuation adds `(continued #N)` to the Agent cell, where `N` is the metrics row number of the prior attempt for that stage—never an agent id. Existing attempt markers remain, so a cell can read `implementer (retry, continued #6)`. Outcome cells may suffix `transcript:missing`, `log:malformed=N`, or `log:unvalidated`.

- **Native Claude (Task tool):** after the terminal completion notification, read its Task result `<usage>` trailer (`total_tokens`, `tool_uses`, `duration_ms`). In-tok/Out-tok = `—`, Total-tok = `total_tokens`, Duration from `duration_ms` as `Xm Ys`.
- **External codex:** from the `turn.completed` usage in `events.jsonl`: In-tok = `input_tokens` (cached input is a **subset** of it — do not add it again), Out-tok = `output_tokens` (reasoning is a subset likewise), Total-tok = In+Out. Note cached/reasoning figures, if interesting, in a footnote line under the table — never in the sums. Tool uses = `n/a` (codex does not emit it). Duration = your wall-clock.
- **External claude:** from the terminal `type: result` event in `events.jsonl` (`--output-format stream-json --verbose`). Field mapping is fixture-verified per machine (acceptance matrix); until you have parsed a real result on this setup, write `n/a` in the token columns rather than guessing paths. Tool uses `n/a` unless present. Duration = your wall-clock.

One spawn = one row; nothing is overwritten. Any field you cannot parse → `n/a`, never a guess, never a blocked pipeline.

Worked continuation example:

```markdown
| 7 | 6 | implementer (retry, continued #6) | claude | opus | high | ok; log:malformed=1 | 19 | — | — | 48231 | 8m 14s |
```

Never substitute transcript or log content into this ledger; `metrics.md` remains accounting only and agents never see it.

**At wrap-up (Step 10), before the final status move**, append one `**SUBTOTAL <provider>**` row per provider used (sums of that provider's In/Out/Total-tok and Tool uses) and one final `**TOTAL**` row containing only: spawn count in the Agent column (e.g. `10 spawns / 9 agents`), summed Tool uses, and summed Duration. **Do not sum token counts across providers** — different tokenizers are different currencies; the per-provider subtotals are the accounting.

## Adversarial framing

Every review agent (Plan Rev 1, Plan Rev 2, Code Rev, Fixer, QA) receives role-based adversarial framing: the artifact under review was **"written by a weaker agent"** (or "weaker model" — equivalent). This is intentional. It triggers skepticism and forces the agent to verify claims against actual code rather than trusting what was written. The orchestrator (you) always applies this framing when spawning review agents — even if in reality all agents run on the same model. **Important:** the framing is role-based ("the artifact's author was weaker"), never sequence-based ("the previous stage / the previous agent"). Sequence wording teaches the spawned agent that it sits inside a pipeline and tempts it to drive that pipeline. Keep framing about the artifact's author, not about position.

The framing comes with an implicit constraint: **change only what you can verify is wrong**. Rewriting correct code "to be safe" introduces new bugs. If uncertain — document the concern in the review artifact; a human reviews the artifact after the run.

This framing reduces, but cannot eliminate, a deeper defect: every solution reviewer verifies the solution *within the premise the orchestrator framed* and inherits that premise's lineage; same-lineage reviewers raise false-consensus confidence, not accuracy, and a model cannot repair a wrong premise from inside the context that contains it (arXiv 2506.01332, 2310.01798; the fix is independent evidence, not a fiercer arguer — arXiv 2506.13609). Step 2.5's premise-challenge is the structural mitigation: an isolated agent fed only the task and the real system, never the lineage. It does **not** receive the "weaker agent" adversarial framing — that points at prior *work*, not at the *frame*. The defect is reduced, not removed; the human remains the last line on the residue.

---

## Context propagation to subagents

**Invariant (verified in this harness):** a Task-spawned named subagent starts with a fresh conversation and no parent conversation history, but the native path does receive the loaded `CLAUDE.md` hierarchy, memory, and a git-status snapshot. The parent's artifacts, PCTX overlay, and conversation still do not reach it automatically, and `@`-imports do not transitively carry the task-specific material a stage needs. Put dynamic inputs in the spawn prompt or give explicit disk paths.

This is why the Step 0.7 overlay exists at all, and why it must be inlined rather than referenced. It also imposes discipline whenever the project overlay *points* at a doc/lesson/notebook instead of pasting it:

1. **Make normative docs reachable explicitly.** Do not write only "follow CLAUDE.md"—ambient project conventions are not a substitute for the task's curated stage inputs. Either inline the relevant rules, or give an explicit instruction to `Read <path> fully before acting`. For tight-budget review stages (plan reviewers, code reviewer, fixer, QA), inline-quote the 3–10 most relevant rules instead of "Read fully".
2. **Inline relevant lessons surgically.** If the overlay points at a lessons file / project notebook and a specific entry applies to *this task's risk area*, inline those 1–3 sentences under a "Lessons from prior work" heading in the spawn prompt. Never paste the whole notebook — that drowns signal and burns budget. Relevance is your judgement as orchestrator (you have the full picture); this is curation, not enforcement.
3. **Quote concrete `file:line` references** instead of "look at the existing patterns".

**Anti-patterns:** "follow CLAUDE.md" as a substitute for task-specific inputs; "you know the codebase" (fresh conversation); trusting `@`-imports to carry task artifacts or PCTX; dumping an entire notebook into every spawn (overload).

**External spawns have the same property, enforced differently:** the child CLI runs with ambient-context discovery disabled (isolation flags **and**, for codex, the private `CODEX_HOME` — both are in the External runner contract, and the flags alone are not enough), so it too sees only its body + the spawn prompt string + what it reads from disk itself. The inline-context discipline above applies identically to both transports.

**Future-mode alternatives (not used by default, noted for consumers).** Per-subagent `memory:` frontmatter (Claude Code v2.1.33+) gives a named subagent its own persistent MEMORY.md — a per-stage silo, not shared. Fork mode (`CLAUDE_CODE_FORK_SUBAGENT=1`, experimental) makes a subagent inherit the full parent conversation including `CLAUDE.md` — at the cost of context isolation. MAW stays on the inline-context-in-spawn-prompt pattern until one of these matures or Issue #27661 ships native propagation. Project-specific paths and excerpts always live in the `PCTX` overlay, never in this base file.

---

## Rules for the orchestrator

- Never implement anything yourself. You only spawn agents and move files/folders.
- **Code commits are your responsibility, not the agents'.** After implementer and after fixer return, if the working tree has uncommitted code changes, commit them on the task branch (`git add -A && git commit -m "<type>: <summary> (TASK-NNN)"`) before the next spawn — otherwise a worktree/branch can reach wrap-up with nothing committed (observed live). Task-folder artifacts keep their own `task:` commits per the persistence rules; don't mix the two in one commit.
- Each agent is fresh by default; continuity exists only for the two same-goal cases defined in Shared memory. No parent conversation history crosses stages.
- Every spawn uses the full resolved profile `(provider, model, effort)` from Step 0.6 (task.md beats settings.json) and the transport from the Dispatch rule. Native path: `model` parameter + `subagent_type=maw-<stem>-<effort>`. External path: the runner contract's flags. Never spawn without a resolved, clamped profile.
- After every spawn attempt or completed continuation, run the Shared memory post-spawn lifecycle and append a row to `metrics.md`. No attempt is exempt—clarifier, reviewers, QA, retries, re-spawns, continuations, and failures all get a row.
- Before every spawn (either transport), apply the Step 0.7 project-context overlay (no-op if `PCTX/` is absent), substituting `{PCTX}` to the real path. Pre-inject domain modules per `task.md Domains:`; never guess domains from prose — the constant catalog is the self-load net. Never bake project specifics into the agent bodies — the overlay is the only seam. Never let a pipeline agent write into `PCTX/`; agents only append proposals to the task-local `PCTX_PROPOSALS.md`.
- `maw/ROADMAP.md` (if present) is a derived view of the task.md `## Dependencies` sections — never authoritative. On any disagreement, task.md wins and the graph is regenerated, never the reverse. It is optional; absence is not an error.
- Spawn failures follow the failure classification table in the External runner contract: fatal classes (auth/config/profile/isolation) are **never** retried; transient/timeout classes retry once with an explicit instruction to write the output file before finishing. Exhausted → `SPAWN_FAILURE.md`, task → `blocked/`, roadmap reconcile, commit (git-tracked), report. For native Task-tool failures there is no `stderr.log` or terminal event — record the Task result's error text in `SPAWN_FAILURE.md` instead; the classification and flow are otherwise identical.
- Never merge to main without user confirmation.
- If any agent produces a FAIL verdict — or `premise-challenge` returns `PREMISE SUSPECT`, or `implementer` returns `PLAN_BLOCKED` — pause, report to user (surface the artifact verbatim), wait for instructions before continuing. **In an unattended/headless run this means stop**: move the task to `blocked/` with the artifact surfaced in your final output. Generic non-interactive phrasing ("ask nothing", "run to completion") is NOT authorization to override a FAIL gate — only an explicit operator statement naming that specific gate is (e.g. "if premise challenge returns SUSPECT, proceed anyway").
- **A report between stages does not end your turn** — when the mode gate allows the next stage and no blocking gate fired, the spawn goes in the same turn as the report. See Turn discipline; "continuing" without a spawn call is a stop, whatever the sentence says.
- **Only blocking questions pause the pipeline** — the list is closed (agent `## Open questions`, FAIL / `PREMISE SUSPECT` / `PLAN_BLOCKED`, merge/push/branch-delete/cost-tier confirmations). Anything else: decide, log it in `OPEN_DECISIONS.md`, continue, surface at wrap-up.
- **Primary source over proxy (premise audit).** For any task that is a retry, a relaunch, or marked premise-suspect, hand `premise-challenge` the primary artifact (the raw failing test / log / repro / code), never your own writeup or a summary of it. A `PREMISE_CHALLENGE` verdict that cites only a derived artifact (a summary, a prior mandate, a log line used as a proxy for a fact) is invalid — it must cite a primary source: code at `file:line`, an executable result, or a direct observation of the real system. A repro or observation predicate is a deliverable to be produced, not a conclusion to be asserted. What counts as the primary source / repro harness for a given project is supplied by that project's `PCTX` overlay, not hardcoded here.
- Status changes are folder moves (`mv maw/tasks/pending/X maw/tasks/in_progress/X`), not edits to a file.
- In git-tracked mode (maw/ not in .gitignore): always commit status transitions so they propagate correctly through worktrees and merges.
- In local-only mode (maw/ in .gitignore): skip all maw/tasks/ commits — only commit code changes.
