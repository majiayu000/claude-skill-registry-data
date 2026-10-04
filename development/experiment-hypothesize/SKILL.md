---
name: experiment-hypothesize
description: >
  Hypothesis-list builder for Orbit Wars experiments under
  `backend/pipeline/{imitation|rulebase|reinforce}/case<N>/`. Runs **once** per
  family / case to enumerate the hypotheses worth testing for that genre via
  code investigation + (opt-in) web research + a structured hearing, and emits
  `docs/experiment/{family}/{yyyymmdd}_case{N}_{topic}/hypotheses.md` as a
  checklist together with a skip list (`実施しない検証 / 評価`). The downstream
  `experiment` (loop driver) treats this `hypotheses.md` as the single source
  of truth. Read-only on code: does NOT implement, NOT push, NOT launch RunPod,
  NOT write `iterN_plan.md`. Use whenever the user types
  `/experiment-hypothesize`, or asks to enumerate / brainstorm / organize
  hypotheses for a case — phrases like "case1 の仮説をリストアップして",
  "dropout 周りで試すべき仮説を網羅したい", "新しい case の調査方針を整理したい",
  "hypotheses.md を作りたい", "ジャンル単位でやることを並べて" all count.
  Don't trigger this skill for single-iteration planning of one hypothesis
  (use `experiment-plan`), full-pipeline execution (use `experiment-execution`),
  result interpretation (use `experiment-analysis`), or multi-iteration loop
  orchestration (use `experiment`).
---

# Experiment Hypothesize Skill (Orbit Wars)

Per-case hypothesis-list builder, run **once** per family / case. The single deliverable is `hypotheses.md`. All downstream skills (`experiment-plan` / `experiment-execution` / `experiment-analysis` / `experiment`) consume this file as input.

## When this skill is in charge

- The user typed `/experiment-hypothesize` (explicit trigger), **or**
- The user asked, in plain language, for any of:
  - enumerate hypotheses for a given case
  - brainstorm follow-ups around a knob (e.g. dropout)
  - organize an investigation plan before opening a new case
  - draft a `hypotheses.md`
- The user did **not** ask to plan / implement / run a single hypothesis. Single-shot requests go to `experiment-plan` / `experiment-execution` directly.

If `hypotheses.md` already exists for the target case, ask whether to **rebuild / append / read-only display** before proceeding.

## Scope boundaries (what this skill does NOT do)

- Does not write `iterN_plan.md` or any per-hypothesis plan file. That is `experiment-plan`'s job.
- Does not edit code under `backend/pipeline/`.
- Does not commit or push.
- Does not launch RunPod or run any `dev/*` command.
- Does not iterate. The skill writes `hypotheses.md` once and exits.

## Skill flow

5 phases. Phase 1 = code reality check, Phase 2 = opt-in web research, Phase 3 = hypothesis hearing, Phase 4 = skip list hearing, Phase 5 = write `hypotheses.md`.

### Phase 0 — Confirm the target case

`AskUserQuestion`, 1 question:

| Q | options |
|---|---|
| 対象 case | `imitation/case<既存>` / `rulebase/case<既存>` / `reinforce/case<既存>` / `新規 case を切る` / `Other` (free-text `family/caseN/topic`) |

Description on the first question: `各質問で「Other」を選ぶと自由記述も可能です。`

For a new case, propose the next free number from `ls backend/pipeline/<family>/`. Resolve `{topic}` (snake_case 1–3 words) in the same question (Other recommended).

If a `hypotheses.md` already exists at `docs/experiment/<family>/{yyyymmdd}_case{N}_{topic}/hypotheses.md`, follow up with one more `AskUserQuestion`: `再構築` (back up existing and reset) / `追記` (append new hypotheses only) / `読み直すだけ` (display current contents and exit).

### Phase 1 — Code investigation (read-only)

Read the relevant code so the upcoming hearing is concrete. No user interaction.

Mandatory reads (skip those that don't apply):

- `ls backend/pipeline/<family>/` — confirm existing case numbers and the next free slot.
- For an existing case: `backend/pipeline/<family>/case<N>/` — `main.py`, `agent.py`, primary policy / feature modules.
- `ls docs/experiment/<family>/` — surface prior experiment directories. Read 1–2 recent `result.md` / `iter*_result.md` files to capture what has already been tried + adopted / rejected.
- `backend/src/dataset/selfplay/agents.py` — `AGENT_REGISTRY` (relevant when registering a new case).

Surface a 3–5 line orientation report to the user (in Japanese):

> `pipeline/<family>/case<N>/` の現状: X / Y / Z。過去 iter で採用済み: A、却下済み: B。次の調査余地: C / D。

### Phase 2 — Web research (opt-in)

`AskUserQuestion`, 1 question:

| Q | options |
|---|---|
| 外部 web 調査 | `不要 — Phase 1 のコード調査で十分` / `必要 — Other で具体的なクエリを指定` / `必要 — トピックを skill 側で提案` |

If the user picks "不要", skip to Phase 3.

If "必要", run `WebSearch` / `WebFetch` for 2–4 queries (time-box: ≤ 5 minutes). Bias toward authoritative sources (Kaggle writeups, arXiv, official docs, well-cited GitHub). Capture findings as 1–3 bullet points per source — these will be folded into Phase 5's References section. If the topic warrants a deeper survey, recommend `/research-retrieval` and stop.

### Phase 3 — Hypothesis hearing

`AskUserQuestion` runs in **at most 2 rounds** (max 4 questions per round). Selection format with free-text via "Other".

**Round 1: Draft, edit, prioritize**

Generate 5–10 hypothesis drafts from Phase 1 (code) + Phase 2 (web) findings, present them, then ask:

| Q | options |
|---|---|
| 草案のうち採用するもの (multi-select) | `H1: ...` / `H2: ...` / ... / `Other` (add new hypothesis as free-text) |
| 削除する仮説 (multi-select、任意) | `H3 を消す` / `H5 を消す` / ... / `なし` |
| 優先順位の付け方 | `skill 提案順 (新規性 + 工数低い順)` ⭐推薦 / `ユーザが手動で並び替え` / `期待効果順` / `Other` |

**Round 2: Shared metadata** for the selected hypotheses

| Q | options |
|---|---|
| 最大 iteration 数 (この hypotheses.md 全体) | `仮説リストを使い切るまで` ⭐推薦 / `5` / `10` / `Other` |
| 主要メトリクス (default) | `local self-play win rate vs. {opponent}` ⭐推薦 / `loss curve のみ` / `behavior 指標 (例: 序盤 neutral 確保率)` / `Other` |
| 既定 episode 数 | `≥300` ⭐推薦 (memory `project_imitation_case1_phase3` 由来) / `100` ⚠️ / `Other` |
| 仮説間の依存関係 | `なし` / `あり (Other で「H4 depends on H1」のように記述)` |

`Kaggle publicScore` is never offered (project rule, memories `project_om_finding` / `project_case5_validation`).

### Phase 4 — Skip list hearing (実施しない検証 / 評価)

`AskUserQuestion`, 1 round, multi-select with Other free-text. Bucketed by category:

**Q1. Analysis skips** (multi-select; "どれもスキップしない" を選んだ場合は他選択を無視して空とする)
- `どれもスキップしない (default)` — skip list の分析項目はすべて実施 (default `n<300 で結論を出さない` のみ自動 ON)
- `300 対戦による評価はしない` — 学習中 val_acc / loss curve や 30 ep 挙動確認だけで採否
- `replay 分析 (experiment-analysis) は実施しない`
- `n<300 結果で結論を出さない` ⭐default ON
- `Other`

**Q2. Execution skips**
- `どれもスキップしない (default, Recommended)`
- `smoke test (1-episode self-play) を skip`
- `dev/test-bot を skip`
- `RunPod GPU を使わない (local CPU only)`
- `auto-recover loop を使わない (失敗時は手動)`
- `Other`

**Conflict checks**:
- User selects `Kaggle publicScore を採否に使う` → reject (project rule, cite memories). Project default `Kaggle publicScore は引用しない` / `skill rating は使わない` are always ON and never asked here.
- User selects `n<300 で結論を出す` → warn (cite memory `project_imitation_case1_phase3`) and confirm before allowing.

No individual confirmation dialog is required for `smoke test skip` / `dev/test-bot skip` — record the user's choice as-is.

**Per-hypothesis exceptions**: free-text input via Other. Examples like "Q1 で 300 対戦 skip だが H4 だけは 300 対戦したい" are recorded in Phase 5's `例外条件` section.

### Phase 5 — Write `hypotheses.md`

Output path (per `.claude/rules/docs.md`):

```
docs/experiment/{family}/{yyyymmdd}_case{N}_{topic}/hypotheses.md
```

- `{yyyymmdd}` — session injected `currentDate` (NOT shell `date`)
- `{topic}` — snake_case from Phase 0
- For "追記" mode, overwrite the same path (Phase 0 already backed it up).

Template:

```markdown
# Hypotheses — {family}/case{N} {topic}

> 作成日: {yyyy-mm-dd}
> 最終更新: {yyyy-mm-dd}
> 状態: in_progress
> 最大 iteration: {N | リスト消化まで}
> 主要メトリクス: {例: ローカル self-play win rate vs. baseline_v5}
> 既定 episode 数: {300 | 100 | ...}

## 実施しない検証 / 評価 (skip list)

### 評価
- {例: ローカル self-play 300 対戦を行わない (学習 loss curve のみで採否)}
- {例: Kaggle publicScore は引用しない (project rule)}

### 分析
- {例: replay 分析は実施しない}
- {例: n<300 結果で結論を出さない}

### 実行
- {例: なし | smoke test skip ⚠️ | RunPod を使わない}

### 例外条件
- {例: H4 のみ「採否が inconclusive なら 300 対戦を追加実施」}

## 仮説リスト (priority 順)

- [ ] (P1) H1: {一文 hypothesis} — {期待効果 / mechanism}
- [ ] (P1) H2: {...}
- [ ] (P2, depends on H1) H3: {...}
- [ ] (P3) H4: {...}
- [ ] (deferred) H5: {...}  # 工数大 / 後回し

## Iteration log

(各 iter 完了時に experiment-analysis / experiment が追記)

| iter | 開始 | 仮説# | plan path | run_id | 主要メトリクス | 採否 | result path |
|---|---|---|---|---|---|---|---|

## 参考 (References)  # Phase 2 を実施した場合のみ

- {URL} — {1 行所感}
```

Write directly via `Write`, then report 3–5 lines to the user (in Japanese):

- written path
- hypothesis count + priority distribution
- key skip-list entries
- next-step suggestion: `/experiment` to consume the list, or `/experiment-plan` for a single iteration

Do not auto-spawn `experiment-plan` / `experiment`. Wait for the user to invoke them.

## Risk gates this skill enforces

- **Never offer Kaggle publicScore as a metric.** Skip-list keeps it default ON; reject if the user tries to remove it.
- **Warn on n<300.** When 100-episode evaluation is selected in Phase 4, surface a one-line warning citing memory `project_imitation_case1_phase3`.
- **Confirm smoke / test-backend skips.** One explicit confirmation dialog each before they take effect.
- **Do not edit code.** Read-only; only `hypotheses.md` is written.
- **Time-box web research to ≤ 5 minutes.** Deeper surveys belong to `/research-retrieval`.
- **Don't silently overwrite an existing `hypotheses.md`.** Phase 0 must offer rebuild / append / read-only.

## Common shapes

| User says… | Skill behavior |
|---|---|
| `/experiment-hypothesize imitation/case1 dropout` | Phase 0 skipped (target given). Phase 1 reads case1. Phase 2 likely 不要. Phases 3–5 produce 5–10 hypotheses + skip list and write `hypotheses.md`. |
| "case4 の harass 周りで仮説を並べて、Lux S3 の解法も参考にして" | Phase 0 confirms case4. Phase 2 runs web research on Kaggle Lux writeups. |
| "case1 の hypotheses.md もう古いから作り直して" | Phase 0 picks `再構築`, backs up the existing file, resets. |
| "実験プランを書いて" (vague) | Belongs to `experiment-plan`. Redirect. |

## Things to avoid

- Running this skill more than once for the same case to grow `hypotheses.md`. Rule: 1 case = 1 `hypotheses.md`.
- Running Phase 2 web research for more than 5 minutes. Deeper surveys belong to another skill.
- Writing `iterN_plan.md` content into `hypotheses.md`. Keep file responsibilities separate.
- Leaving the skip list empty. Project defaults (`Kaggle publicScore は引用しない`, `n<300 で結論を出さない`) must always appear.
- Overwriting an existing `hypotheses.md` without user confirmation.
- Including Kaggle publicScore as a success metric on any hypothesis.
- Auto-spawning `experiment-plan` or `experiment` after writing the file. Suggest by name only.

## Language

- Internal reasoning and thinking should be in English
- **All user-facing output, AskUserQuestion labels/descriptions, and the written `hypotheses.md` body must be in Japanese** (per `.claude/CLAUDE.md`)
