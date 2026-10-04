---
name: experiment-execution
description: >
  Execution runner for Orbit Wars experiments under `backend/pipeline/`. Takes
  a single hypothesis (one line in `hypotheses.md` or one `iterN_plan.md`) and
  drives the full cycle inline in the main session: case implementation →
  local smoke test (1-episode self-play, mandatory) → `dev/test-backend` →
  push & RunPod GPU launch → in-flight monitoring (progress / steps / loss /
  GPU·CPU·memory) → on failure, stop & terminate the pod and relaunch
  (auto-recover) → evaluation → `iterN_result.md`. Honors the
  `hypotheses.md` skip list (e.g. `300 対戦 skip` → evaluation is reduced to
  training-log only, `smoke skip` → skip the 1-ep self-play, `RunPod 不使用` →
  full local pipeline). Use whenever the user types `/experiment-execution`,
  or asks to run / execute / iterate / kick off an experiment, train a new
  model, launch a RunPod run, propose a new case, or write up an experiment
  result — even if they don't explicitly say "execute", phrases like
  "imitation/case1 で dropout を試したい", "rulebase/case2 を改良して回したい",
  "runpod で学習を回して結果まとめて", "新しい case を切って学習させたい",
  "iter5_plan.md に従って実装して回して", "H3 を実行して" all count. Don't
  trigger this skill for hypothesis-only discussion (use `experiment-plan` /
  `experiment-hypothesize`), interactive result interpretation after a run
  finishes (use `experiment-analysis`), read-only code review, plain bug
  fixes, or Kaggle submission requests.
---

# Experiment Execution Skill (Orbit Wars)

Drives one hypothesis through plan → implementation → smoke → test → push → RunPod → monitoring → evaluation → `iterN_result.md` inline in the main session. Honors the `hypotheses.md` skip list to short-circuit phases (skip eval, skip replay, skip smoke, skip RunPod, skip auto-recover).

## When this skill is in charge

- The user typed `/experiment-execution` (explicit trigger), **or**
- The user asked, in plain language, for any of:
  - launching a new case and training it
  - iterating an existing case and retraining
  - kicking off a RunPod training run
  - writing up the result of a recent run
- The user did **not** already pre-specify the entire pipeline themselves (e.g. "just run `dev/runpod train abc123`" — at that point, just run it).

If the user is asking for **read-only review**, **dead-code cleanup**, **Kaggle submission**, or **infra-only work**, redirect to the matching skill/agent.

## What "an experiment" means in this repo

- **Family** — `imitation` / `rulebase` / `reinforce`.
- **Case** — `case<N>` under `backend/pipeline/<family>/`.
- **Hypothesis** — one sentence + adoption threshold.
- **Compute target** — local CPU only / RunPod GPU.
- **Skip list** — read from `hypotheses.md > 実施しない検証 / 評価` and used to short-circuit phases.

Comply with `.claude/rules/docs.md` and `.claude/rules/backend/pipeline.md`.

## Skill flow

8 phases. Phase 4.5 (smoke test) is mandatory. Phase 6 specifies which `dev/runpod tail` source to use. Phase 6.5 makes pod terminate explicit on auto-recover.

### Phase 1 — Resolve the input source

Resolution priority:

1. **Explicit `iterN_plan.md`** — if a plan already exists, hypothesis / scope / metric / skip list are read from the plan; the skill only does minimal confirmation.
2. **`hypotheses.md` H{n} reference** — e.g. "H3 を実行して" → pull the line from `hypotheses.md`, internally call `experiment-plan` to write `iterN_plan.md`, then continue to Phase 2.
3. **Free-text hypothesis** — internally write `iterN_plan.md` first, then continue.

Items to confirm (extract from `iterN_plan.md` / `hypotheses.md`; ask 1–2 questions only if missing):

1. family / case
2. one-sentence hypothesis + scope
3. primary metric + default episode count (when `300 対戦 skip` is set, mark `対戦評価 skip`)
4. compute target (RunPod GPU / local CPU only)
5. skip list (smoke skip / dev/test-backend skip / replay 分析 skip / RunPod 不使用 / auto-recover 不使用)

### Phase 2 — Reality check

Parallel `Bash`:

```bash
git status --short
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
ls backend/pipeline/<family>/
ls docs/experiment/<family>/
```

If the tree is dirty and a RunPod launch is planned, decide with the user (commit / stash / proceed without RunPod).

### Phase 3 — Confirm or write `iterN_plan.md`

If Phase 1 found no `iterN_plan.md`, run an `experiment-plan`-equivalent flow internally (skip list honored to auto-shorten `## 検証方法`). Otherwise reuse the existing plan.

If the user scoped the request to "plan only", stop here.

### Phase 4 — Implement the case

Comply with `.claude/rules/backend/pipeline.md`:

- `pipeline/<family>/case<N>/main.py` exists, exposes `agent(obs)`, uses `sys.path.insert(0, str(Path.cwd()))`
- Intra-package imports are **relative**
- New case → register in `backend/src/dataset/selfplay/agents.py` (`AGENT_REGISTRY`)
- Add dev-only directories to `backend/pipeline/.submitignore`

For existing-case extension, prefer **adding a new module** (`policy_v2.py`, `features_v3.py`) — preserves a comparable baseline.

### Phase 4.5 — Local smoke test (mandatory)

**Always run unless skip list explicitly sets `smoke test (1-episode self-play) を skip`**. When skipped, surface a one-line note before moving to Phase 5.

In order:

1. Import sanity:
   ```bash
   cd backend && uv run python -c "from pipeline.<family>.case<N>.baseline.agent import agent; print(agent)"
   ```
2. **1-episode self-play smoke** (new):
   ```bash
   cd backend && uv run python -m dataset.selfplay.run --case <family>/case<N> --episodes 1 --seed 0
   ```
   Or call the case's smoke harness. Failure here means **no remote launch**. This 1-episode pass is the last line of defense before paying for GPU time.
3. **`dev/test-backend`** (mandatory unless skip list disables it):
   ```bash
   dev/test-backend
   ```
4. Submit-shape changes → dry-run validator:
   ```bash
   uv run --directory backend python -m submit submit <family>/case<N> --dry-run -m "dry-run"
   ```

On failure, optionally delegate to `python-build-resolver`. Always pass before progressing to RunPod.

### Phase 5 — Launch RunPod GPU

If skip list sets `RunPod を使わない (local CPU only)`, **skip Phases 5 / 6 / 6.5 entirely** and go to Phase 7 (local evaluation).

Otherwise:

```bash
git push origin <branch>
dev/runpod train <commit-sha> [--case <caseN>] [--cloud-type SECURE|COMMUNITY|ALL]
```

Pre-flight:
- `git status` clean
- commit pushed

Save `run_id` / commit SHA / case / start time. Report 3 lines after launch and immediately set up the Phase 6.5 cron monitor.

### Phase 6 — Inline reactive monitoring during the run

Respond to user requests with the right command:

| user says | command | what you get |
|---|---|---|
| "今どこ?" / "進捗教えて" | `dev/runpod status <run_id>` | pod state / S3 progress marker / latest metrics |
| "train ログ見せて" | `dev/runpod tail <run_id> --source train` (live) or `dev/runpod logs <run_id>` (post-mortem) | training stdout (step / loss / lr / val_metric) |
| "setup ログ見せて" | `dev/runpod tail <run_id> --source onstart` | onstart.log (env setup / dvc pull / driver / mountpoint) |
| "GPU 使用率は?" | `dev/runpod tail <run_id> --source gpu` | nvidia-smi 10s sample (utilization / VRAM / temp) |
| "成果物今ある?" | `dev/runpod pull <run_id>` | DVC, falling back to S3 |
| "止めて" | confirm, then `dev/runpod stop <run_id>` | (surface forfeited cost in 1 line) |
| "lr も変えたい" | treat as a new iter; do not touch the in-flight run; queue `iterN+1_plan.md` | — |

**NEVER** claim "succeeded" until artifacts (`best.pt`, metrics JSON) are pulled and inspected.

For asynchronous notification on completion, use `dev/runpod watch <run_id>` (desktop notification) or `dev/runpod train --watch` at launch time.

### Phase 6.5 — Cron-driven periodic health check & auto-recover

If skip list sets `auto-recover loop を使わない`, register the cron in monitor-only mode (notify, no stop / fix / relaunch).

Otherwise (default):

1. Use the `schedule` skill (cron) at 10-min cadence (extend to 15–20 min for very long ETAs).
2. Each tick runs `dev/runpod status <run_id>` (+ `dev/runpod logs <run_id> --tail 20` when unhealthy) and applies:

| state | action |
|---|---|
| RUNNING + metrics advancing | no-op |
| RUNNING + metrics stalled for 2 consecutive checks | soft warning to user; no auto-stop |
| EXITED + success marker (`best.pt` + metrics JSON in S3) | cancel cron → Phase 7 |
| EXITED + failure (non-zero / OOM / crash) | **trigger auto-recover loop** |
| Cost cap exceeded | stop pod → surface to user immediately (no auto-relaunch) |

**Auto-recover loop** (failure path):

1. **Stop & terminate the pod** — `dev/runpod stop <run_id>`. Then **terminate / detach volume** to ensure the pod stops billing. Always perform an explicit terminate even if the pod looks crashed.
2. **Pull artifacts & logs**: `dev/runpod pull <run_id> --from s3` + `dev/runpod logs <run_id>`
3. **Diagnose**: env/setup error (first-pass against memories `project_runpod_onstart_pitfalls` and `project_runpod_5_traps_2026_05_04`) / code bug / config / OOM / experiment code bug
4. **Fix** in the worktree:
   - Code/config bug → edit, `dev/test-backend`, commit + push
   - OOM → batch size / GPU class change
   - Onstart / env → fix `dev/runpod` script or case-level setup
   - Infra flake (RunPod outage / GPU node lottery) → surface to user and stop (no auto-relaunch)
5. **Re-launch** with the new SHA: `dev/runpod train <new-sha> --case <caseN>`.
6. **Re-arm cron** for the new `run_id`, continue Phase 6.5.

Each step emits a Japanese status message ≤ 3 lines. When Phase 7 starts or the user terminates, cancel the cron and confirm via `dev/runpod ps` that no stale pod remains.

### Phase 7 — Evaluation and `iterN_result.md`

Honor the skip list to determine evaluation scope:

- **`ローカル self-play 300 対戦を行わない` ON** → judge from training logs only (loss curve / val_metric). Replace `## Numbers` with a training-log table.
- **`100 対戦のみ` ON** → run 100-episode self-play; if `n<300 で結論を出さない` is also ON, fix decision = `inconclusive`.
- **default (300 ep)** → standard evaluation (≥300 ep).

In order:

1. `dev/runpod pull <run_id>` to fetch artifacts to `data/output/models/<family>/case<N>/runs/<run_id>/`.
2. Run the case's evaluation script (`backend/pipeline/<family>/case<N>/evaluation/compare_*.py` or similar) — skip when not applicable.
3. Decision is based on **local match outcomes only** (no Kaggle publicScore / skill rating).
4. Write `iterN_result.md` next to `plan.md`:

```markdown
# {Family}/case{N} — {Topic} (iter{N}) RESULT

> 関連: iterN_plan.md / hypotheses.md
> run_id: {run_id} / commit: {sha} / case: {caseN}
> 開始: {start} / 終了: {end} / コスト: ${cost}

## Summary
{1 段落: 仮説は支持されたか?}

## Numbers
{skip list に従い、対戦評価 table or 学習ログ table}

| metric | value | note |
|---|---|---|

## Diagnosis
{なぜ機能した / しなかったか}

## Decision
- 採否: {adopted | rejected | inconclusive}
- 次の一手: {follow-up 仮説 or `dev/runpod promote <run_id>` (user 確認必須)}

## Artifacts
- model: `data/output/models/<family>/case<N>/runs/<run_id>/best.pt`
- metrics: ...
```

5. Report to the user in 3–5 lines: hypothesis result / key metrics / decision / result.md path.

### Phase 8 — Provisional write-back to `hypotheses.md`

Even if `experiment-analysis` will run later, append exactly **one row** to the `hypotheses.md` Iteration log when `iterN_result.md` is finalized:

```
| {N} | {start} | H{n} | iterN_plan.md | {run_id} | {primary metric} | {adopted/rejected/inconclusive} | iterN_result.md | (analysis 未実施) |
```

Do **not** flip the hypothesis-row checkbox here (that is `experiment-analysis` Phase 4.5's job). Phase 8 only adds the Iteration log row.

Skip Phase 8 entirely when `hypotheses.md` does not exist (one-shot invocation).

Kaggle submission is out of scope (per `.claude/rules/command.md`; explicit approval + `dev/submit`).

## Risk gates this skill enforces

- **Cost-cap overruns auto-stop.** Phase 6.5 stops the pod and never auto-relaunches when the cost cap is exceeded. Recovery from crash / OOM / bug is fine; budget overruns require user approval.
- **Smoke test (1-ep self-play) is mandatory by default.** Honor skip list only when the user explicitly disabled it. This is the last line of defense before remote training spend.
- **Auto-recover always terminates the pod.** Stop alone is insufficient; ensure the pod is terminated and the volume detached so charges stop.
- **Cancel the Phase 6.5 cron when Phase 7 starts or the user terminates the run.**
- **Honor the `hypotheses.md` skip list** (300 対戦 / replay / smoke / RunPod / auto-recover flags all map to phase short-circuits).
- **Hypothesis-row checkboxes belong to `experiment-analysis`.** This skill only appends an Iteration log row.
- **n<300 verdicts are fixed at `inconclusive`.** Per memory `project_imitation_case1_phase3`.
- **Never use Kaggle publicScore / skill rating as evidence.**
- **Don't launch RunPod from a dirty tree.**
- **Canonical-weights update (`dev/runpod promote`) and Kaggle submission are out of scope.** User must approve those individually.

## Common shapes

| User says… | Skill behavior |
|---|---|
| "imitation/case1 で dropout を 0.3 にして回して" | Phase 1 (1 question to confirm full RunPod run) → Phases 2–8 inline. |
| `/experiment-execution H3` | Phase 1 pulls H3 from `hypotheses.md` → internally write the plan → Phases 2–8. |
| "case4 の plan.md だけ先に書いて" | Phases 1–3 only; skip Phases 4 onwards. |
| "さっきの run xxx の結果を docs にまとめて" | Phase 1 + 7 + 8 only (pull + eval + result.md + Iteration log row). |
| "今 RunPod で回ってる run は終わった?" | Phase 6 inline status. |
| "やっぱり lr も変えたい" (mid-flight) | Treat as a new iter; do not touch the in-flight run; queue `iterN+1_plan.md`. |
| "smoke 飛ばして直接 RunPod" | Check skip list; if absent, ask one confirmation; only then proceed without smoke. |

## Things to avoid

- Spawning a subagent for the long-running portion (Phases 5–6). Inline is required so the user can interject.
- Forgetting to cancel the Phase 6.5 cron at Phase 7 / on terminate.
- Auto-relaunching after a cost-overrun stop. Crashes / bugs / OOM are recoverable; budget overruns need explicit user approval.
- Polling more frequently than every 5 minutes (cache waste, no signal).
- Citing Kaggle publicScore as the success metric.
- Creating a new experiment directory when the user is iterating (use `iterN_*.md` instead).
- Putting machine-generated artifacts under `docs/experiment/` (those go to `data/output/experiment/`).
- Claiming a run finished before pulling and inspecting artifacts.
- Flipping the hypothesis-row checkbox in `hypotheses.md` (Phase 8 only adds Iteration log rows).
- Running the default eval flow without checking the skip list (e.g. running 300 episodes when `300 対戦 skip` is set wastes GPU).
- Stopping a pod without terminating it. Attached volume = ongoing charges.

## Communication cadence

- One short message at each phase boundary (plan written / case implemented / smoke green / tests green / RunPod launched / run finished / result written). Each ≤ 3 lines.
- After RunPod launch, surface run_id + ETA, then return control. Do not narrate while waiting.
- Status checks: ≤ 3 lines (status / latest metric / ETA delta).
- End each turn with what's next, e.g. "run_id=abc123, ETA ~45min — `status` で進捗、`止めて` で中断、`結果まとめて` で完了後の集計に進みます".

## Language

- Internal reasoning and thinking should be in English
- **All user-facing output, AskUserQuestion labels/descriptions, and result reports must be in Japanese** (per `.claude/CLAUDE.md`)
