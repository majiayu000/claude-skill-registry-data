---
name: experiment
description: >
  Hypothesis-list–driven iteration loop for Orbit Wars experiments under
  `backend/pipeline/{imitation|rulebase|reinforce}/case<N>/`. The single
  source of truth is the target case's `hypotheses.md` (created by
  `experiment-hypothesize`). Hears 3 things from the user via `AskUserQuestion`:
  (1) the target `hypotheses.md` path, (2) the max iteration count, and (3)
  the loop cadence. Registers a `schedule` (cron) or `loop` (short interval)
  job whose body is "call `experiment-plan` (which decides list-consume /
  deepen / broaden), then `experiment-execution`, then `experiment-analysis`,
  once". Each tick = one hypothesis = one plan → run → analyze cycle. The
  loop driver itself does NOT decide deepen / broaden — `experiment-plan`
  Step 0.5 owns that. The driver only reads the plan's reported mode: a
  broaden outcome stops the loop and surfaces the `/experiment-hypothesize`
  suggestion; list-consume / deepen continue the cycle. Repeats until
  hypotheses are exhausted, max iterations are hit, or the user stops the
  loop. **This skill is invoked ONLY by explicit user request** (typed
  `/experiment` or said "仮説リストを回したい / iteration loop で実験したい /
  hypotheses.md を消化して"). Don't auto-trigger this skill from
  natural-language experiment requests — those go to `experiment-hypothesize`
  (hypothesis enumeration) / `experiment-plan` (single plan) /
  `experiment-execution` (single run + RunPod) / `experiment-analysis`
  (single replay post-mortem) instead.
---

# Experiment Skill (Orbit Wars — iteration loop)

Iteration orchestrator that consumes `hypotheses.md` in priority order. One tick = one hypothesis = one `experiment-plan` → `experiment-execution` → `experiment-analysis` cycle.

This skill itself does no heavy lifting. It delegates to the four child skills:
- Hearing → confirm target `hypotheses.md` and loop settings
- Register the loop via `schedule` / `loop`
- On each tick: pick the next hypothesis from `hypotheses.md` by priority → call the three child skills in order → write results back → branch on deepen / broaden

## When this skill is in charge

- The user typed `/experiment` (explicit trigger), **or**
- The user explicitly asked for a multi-iteration loop: "`hypotheses.md` を消化して", "仮説 5 個を順に試したい", "iteration loop で実験回して", "止めるまで仮説リストを消化し続けて".
- The user did **not** ask for a single experiment. Single-shot requests go to `experiment-execution` directly. Hypothesis enumeration goes to `experiment-hypothesize`.

If the target case has no `hypotheses.md`, **redirect to `experiment-hypothesize` first**. This skill is built around an existing `hypotheses.md`; it does not start from an empty list.

## Skill flow

### Phase 0 — User hearing (3 questions)

Run **one round** of `AskUserQuestion` (3 questions). Selection + Other format. The first question's description: `各質問で「Other」を選ぶと自由記述も可能です。`

1. **Target `hypotheses.md` path** — `ls docs/experiment/<family>/*/hypotheses.md`, surface up to 5 candidates as `family/case<N>/{topic} (残 X 仮説)`. `Other` accepts a free-text path. If no matching file exists, suggest `/experiment-hypothesize で先に作成` and **terminate this skill** (we don't start from an empty list).

2. **Max iterations (stop condition)**:
   - `1` (smoke) / `3` / `5` ⭐推薦 / `10` / `仮説リストを使い切るまで` / `上限なし (ユーザー停止指示まで)` ⚠️ / `Other`
   - When "上限なし" is selected, surface a one-line RunPod cost-accumulation warning.

3. **Loop cadence**:
   - `loop 60s` / `loop 5m` / `schedule */15min` / `schedule hourly` / `schedule daily` / `逐次 (周期なし、前のティックが完了したら即次)` ⭐推薦 / `Other`
   - **Cadence vs. tick duration must align**: a tick that includes imitation training + RunPod evaluation runs 30 minutes to several hours. A cron interval shorter than this means concurrent launches = doubled GPU spend. When `schedule` is selected, confirm cadence ≥ expected tick duration. Short cadences are fine when `RunPod を使わない` is set in the skip list.

### Phase 1 — Inspect `hypotheses.md` state

Read the chosen `hypotheses.md`:

- If the header `状態:` is `paused` / `stopped`, ask "Resume?" in 1 question (Yes → write back to `in_progress`; No → terminate).
- Count pending (`- [ ]`) hypotheses in the list. Zero → tell the user "all consumed; want to enumerate more? → `/experiment-hypothesize`" and terminate.
- Cache the `実施しない検証 / 評価 (skip list)` in memory (each tick passes it through to child skills; transparent passthrough).

**Don't use a queue file.** `hypotheses.md` is the single source of truth.

### Phase 2 — Register the loop

Per the cadence chosen in Phase 0:

#### `loop` cadence

Call the `loop` skill as `/loop {interval} /experiment`. The Phase 3 tick driver re-reads `hypotheses.md` on every wake-up and decides its own state.

#### `schedule` cadence

Call the `schedule` skill to register a cron job whose body is "run a `/experiment` tick in this worktree". One cron firing = one tick. On stop, cancel the cron.

#### `逐次` cadence

No `loop` / `schedule` registration. Run a `while not stopped` loop directly in the main session. Each tick runs in foreground; the next tick starts as soon as the previous one finishes. **Lowest collision risk** when RunPod training is in the loop.

### Phase 3 — Tick driver (1 iteration)

Each tick performs these steps in order (= one hypothesis = one cycle). **The driver does not decide deepen / broaden itself — `experiment-plan` Step 0.5 owns that decision. The driver reads the mode from `experiment-plan`'s report and acts accordingly.**

1. **Read `hypotheses.md`** (every time; do not hold in-memory state across cron firings).

2. **Pre-check stop conditions** (only conditions the driver can decide alone):
   - Completed (`- [x]`) iter count ≥ max iterations → cancel cron / loop, report, terminate.
   - Header `状態:` is already `stopped` (user-set) → exit immediately.
   - `状態:` = `paused` → exit (the previous tick's `experiment-plan` already set this; surface the broaden suggestion once and stop).

   The "no pending hypothesis" condition is **not** decided here — let `experiment-plan` handle it (it may emit deepen instead of stopping).

3. **Call `experiment-plan` with no specific hypothesis** — `Skill(skill="experiment-plan")`. The skill runs Step 0.5 (mode decision) and returns one of three outcomes. The driver reads the mode from the report:

   | Mode reported by experiment-plan | Driver behavior |
   |---|---|
   | `list-consume` | `iterN_plan.md` was written for the priority-picked hypothesis. Continue to step 4. |
   | `deepen` | One follow-up hypothesis was appended to `hypotheses.md` and `iterN_plan.md` was written for it. Continue to step 4. |
   | `broaden` | `状態:` was rewritten to `paused`; no plan file. **Stop the loop**, cancel the cron, surface the "/experiment-hypothesize で再構築推奨" line, and terminate. |

4. **Call `experiment-execution`** — Skip its Phase 1 (hypothesis is already pinned by the plan), run Phases 2–8: reality check → implementation → smoke (mandatory unless skip list disables it) → tests → push → RunPod → monitoring → auto-recover → evaluation → `iterN_result.md` → append a provisional row to the Iteration log. Capture `run_id` and the primary metric.

5. **Call `experiment-analysis`** — Phase 1.5 defaults to "直前 iter のみ". When the skip list contains `replay 分析を行わない`, run in skip mode. Phase 4.5 writes the **adoption verdict only** (checkbox flip + Iteration log row update + `最終更新`). It does **not** touch `状態:` and does **not** append new hypotheses.

6. **Per-tick report** (≤ 3 lines):
   - iter N/{max}: mode (list-consume / deepen) + family/case + hypothesis (one sentence)
   - primary metric + verdict
   - next-tick schedule (`schedule` → next cron time, `loop` → interval, `逐次` → "starting next hypothesis immediately"). On the next tick, `experiment-plan` may emit broaden if rejections accumulated.

### Phase 4 — Stop and finalize

The loop stops when:

- max iterations reached
- all hypotheses consumed
- genre is `paused` (3 consecutive rejections) — surface the broaden suggestion
- the user says "stop"

A failed tick does not auto-pause the loop. Failures are recorded in the `hypotheses.md` Iteration log as `失敗` (by `experiment-execution`); the hypothesis row stays `- [ ]` so the user can re-queue later. Whether consecutive failures indicate a structural problem is a user judgment call.

On stop:

1. **Cancel cron / loop** — always remove the `schedule` job; stop the `loop`. Tear down any `dev/runpod watch` you launched. Confirm via `dev/runpod ps` that **no stale cron / pod remains**.
2. **Update `hypotheses.md` state** — rewrite the header `状態:` to `completed` (all consumed) / `paused` (consecutive rejected) / `stopped` (user stop), and append a one-line stop reason to the Iteration log.
3. **Aggregate report** (5–10 lines, Japanese):
   - completed iter count / max
   - verdict counts (adopted / rejected / inconclusive)
   - highest win-rate iter (family/case + run_id + win-rate)
   - `hypotheses.md` path + each iter's result.md / analysis.md path
   - recommended next action (e.g. "iter3 で +5pp 採用、`dev/runpod promote <run_id>` 実行 (user 確認後) → Kaggle submit は別途手動承認" / "ジャンル paused、`/experiment-hypothesize` で再構築推奨")

## Risk gates this skill enforces

- **Loop is invoked only on explicit request.** Single-shot natural-language requests do not trigger it.
- **Redirect when `hypotheses.md` is missing.** Don't start from an empty list; suggest `/experiment-hypothesize`.
- **RunPod GPU cost accumulates.** Surface a one-line cost warning when "上限なし" is selected in Phase 0.
- **Cadence ≥ expected tick duration.** Concurrent launches = doubled GPU spend.
- **Always cancel cron / loop on stop and confirm no pod is left running.**
- **`hypotheses.md` is the single source of truth.** No in-memory state across cron firings. Queue files are abolished.
- **Mode decision belongs to `experiment-plan` Step 0.5.** The tick driver does not decide list-consume / deepen / broaden itself — it reads the plan's reported mode and stops on broaden.
- **Adoption write-back belongs to `experiment-analysis`.** The tick driver does not flip checkboxes.
- **Never auto-spawn `experiment-hypothesize` on broaden.** Surface the suggestion and stop the loop.
- **Kaggle submission and `dev/runpod promote` are out of scope.** Canonical-weights updates and submissions require explicit user approval.
- **Pass the `hypotheses.md` skip list straight through to child skills.** Do not override it inside the loop driver.

## Common shapes

| User says… | Skill behavior |
|---|---|
| `/experiment` | Phase 0 hearing → confirm target `hypotheses.md` → Phase 2 register loop → Phase 3 starts ticks. |
| "imitation/case1 の hypotheses.md を 5 個分回して、夜中に回しておきたい" | Phase 0 confirms path / max=5 / `schedule hourly` (after aligning RunPod tick duration) → register cron → aggregate report in the morning. |
| "止めるまで仮説出し続けたい" | Phase 0 max="上限なし" + RunPod cost warning → recommend `逐次` → report each tick, continue until the user says stop. |
| "仮説 1 個だけ試して" | Not a loop — redirect to `/experiment-execution`. |
| "今走ってるループ止めて" | Phase 4: cancel cron / loop → set `hypotheses.md` state to `stopped` → aggregate report. |
| "case1 の hypotheses.md がまだ無い" | Redirect: `/experiment-hypothesize で先に作成してください`. |
| "rejected 続きで paused になった" | Surface the broaden suggestion (`/experiment-hypothesize`). No auto-spawn. |

## Things to avoid

- Pulling single-shot requests into the loop. Without an explicit loop request, call the child skills directly.
- Starting the loop without `hypotheses.md`. Always redirect.
- Skipping the cadence-vs-tick-duration alignment check. Concurrent launches double GPU spend.
- Forgetting to cancel cron / loop on stop. Stale crons trigger unintended RunPod launches and charges.
- Creating a queue file. `hypotheses.md` is the single store.
- Toggling hypothesis-row checkboxes from the tick driver (that is `experiment-analysis`'s job).
- Deciding deepen / broaden in the tick driver (that is `experiment-plan` Step 0.5's job).
- Calling `experiment-plan` with a specific hypothesis from the loop. Always call it without args so Step 0.5 can decide the mode for this tick.
- Citing Kaggle publicScore in the verdict.
- Auto-running `dev/runpod promote` or Kaggle submission from the loop.
- Auto-spawning `experiment-hypothesize` after consecutive rejections (suggest only).

## Language

- Internal reasoning and thinking should be in English
- **All user-facing output, AskUserQuestion labels/descriptions, and tick reports must be in Japanese** (per `.claude/CLAUDE.md`)
