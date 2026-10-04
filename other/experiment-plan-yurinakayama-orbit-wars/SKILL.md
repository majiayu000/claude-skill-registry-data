---
name: experiment-plan
description: >
  Hypothesis-management decision maker and per-iteration `iterN_plan.md`
  writer for Orbit Wars experiments under `backend/pipeline/`. Reads the
  case's `hypotheses.md` to decide which mode the next iteration should run
  in: (a) **list-consume** when pending hypotheses exist (pick by priority
  and plan it), (b) **deepen** when no pending hypotheses but the previous
  result invites a follow-up (auto-append a new hypothesis to the list and
  plan it), (c) **broaden** when recent results show the genre is poor-fit
  (set `hypotheses.md` state to `paused` and recommend re-running
  `experiment-hypothesize` — no plan written this turn). After deciding,
  for modes (a) and (b) writes one `iterN_plan.md` under
  `docs/experiment/{family}/{yyyymmdd}_case{N}_{topic}/`. Reads existing
  case code for a reality check, runs a minimal hearing on metric / scope,
  and honors the case's `hypotheses.md > 実施しない検証 / 評価 (skip list)`
  so that the plan's 検証方法 section is automatically shortened (e.g.
  300-対戦 skip → ローカル評価を loss curve のみに置換). Stops at the plan;
  does NOT implement code, push commits, or launch GPU training. Does NOT
  enumerate the **initial** hypotheses (that is `experiment-hypothesize`'s
  job). Does NOT do open-ended web research.
  Use whenever the user types `/experiment-plan`, asks for a single
  iteration's plan ("次の iter の plan 作って", "H3 の plan.md だけ書いて",
  "imitation/case1 で dropout を 0.3 に上げる plan を書きたい",
  "rulebase/case2 改良の plan.md だけ先に書いて"), or hands a 1-line
  hypothesis. Don't trigger this skill for initial hypothesis brainstorming
  from scratch (use `experiment-hypothesize`), full-pipeline execution
  including RunPod training (use `experiment-execution`), result
  interpretation after a run finishes (use `experiment-analysis`), or
  large-scale multi-domain feature planning (use `feature-plan`).
---

# Experiment Plan Skill (Orbit Wars)

Owns two responsibilities:

1. **Hypothesis-management decision** — based on `hypotheses.md` state and the latest `iter*_result.md`, decides one of three modes for the next iteration:
   - **list-consume** — pending hypotheses exist → pick the next by priority
   - **deepen** — no pending hypotheses, but the previous result invites a follow-up → auto-append a new hypothesis to the list, then proceed
   - **broaden** — recent results show poor genre fit (e.g. 3 consecutive `rejected`) → set `hypotheses.md` `状態:` to `paused`, recommend re-running `experiment-hypothesize`, and **stop without writing a plan**
2. **Per-iteration `iterN_plan.md` writing** — runs only in modes (a) and (b). Honors `hypotheses.md`'s skip list so the `## 検証方法` section is automatically tailored.

Initial enumeration of hypotheses still belongs to `experiment-hypothesize`. Adoption write-back (checkbox + verdict) still belongs to `experiment-analysis`. This skill only **decides what to plan next** and **writes that plan**.

## When this skill is in charge

- The user typed `/experiment-plan` (with or without an inline hypothesis), **or**
- The user asked for a single-iteration plan: e.g. "H3 の plan を書いて" / "次 iter の plan" / "dropout 0.3 の plan.md だけ"
- The `experiment` loop driver invoked this skill at the top of a tick to choose the next iteration's mode and plan.
- The user did **not** ask for initial hypothesis enumeration (→ `experiment-hypothesize`), execution (→ `experiment-execution`), or analysis (→ `experiment-analysis`).

If the request asks to enumerate the **initial** hypothesis list from scratch, or to do open-ended paper research, redirect to `experiment-hypothesize`.

## Scope boundaries (what this skill does NOT do)

- Does not enumerate the **initial** hypothesis list (`experiment-hypothesize`'s job). Auto-appending a single follow-up hypothesis in deepen mode is allowed.
- Does not run open-ended web research. Quick spot-checks (one URL the user names) are OK.
- Does not edit code under `backend/pipeline/`.
- Does not commit, push, or launch RunPod.
- Writes at most **one** plan file per invocation (`iterN_plan.md`). In broaden mode, no plan file is written.
- Adoption write-back (hypothesis-row checkbox + verdict) is `experiment-analysis`'s job. This skill only **adds** a row in deepen mode.

## Skill flow

5 steps. **Step 0.5 (mode decision) is the new front door**; the rest is the existing single-plan flow.

Each invocation returns one of three outcomes (the loop driver / user reads the report to decide what's next):

| Mode | When | Side effect on `hypotheses.md` | Plan file written? |
|---|---|---|---|
| **list-consume** | pending `- [ ]` hypotheses exist | none | yes (`iterN_plan.md`) |
| **deepen** | no pending hypotheses, but the most recent verdict is `adopted` or `inconclusive` and `where_to_focus_next` exists | append `- [ ] (auto, deep) H{n+1}: ...` | yes (`iterN_plan.md`) |
| **broaden** | (a) header `状態:` is `paused`, or (b) the last 3 iters are all `rejected`, or (c) no pending and the latest verdict invites no follow-up | rewrite `状態:` to `paused`; append a comment to Iteration log explaining the trigger | **no** — recommend `/experiment-hypothesize` and stop |

### Step 0 — Locate the hypothesis & target directory

Resolve the hypothesis being planned and where the experiment directory lives.

Resolution priority:

1. **Inline argument** — `/experiment-plan imitation/case1 dropout 0.3` → family/case + 1-sentence hypothesis confirmed.
2. **Reference into hypotheses.md** — `/experiment-plan H3` or "H3 の plan" → search `docs/experiment/<family>/...`, take the H3 line from the first matching `hypotheses.md`.
3. **Free-text natural language** — heuristically infer family / case / hypothesis from the overview. If ambiguous, run **at most 1** `AskUserQuestion`.

Target directory:

- If `docs/experiment/<family>/{yyyymmdd}_case{N}_{topic}/` already exists, reuse it → add `iterN_plan.md`.
- Otherwise create it (`{yyyymmdd}` from session `currentDate`, `{topic}` derived as snake_case 1–3 words from the hypothesis).
- **iter numbering**: `ls` existing `iter*_plan.md` in the directory; new file = `max(N) + 1`.
- If a plain `plan.md` (no `iter` prefix) exists and you are introducing the iter scheme for the first time, rename it to `iter1_plan.md` first, then write `iter2_plan.md`. Surface the rename to the user in one line before executing it (per `.claude/rules/docs.md`).

### Step 0.5 — Hypothesis-management decision (new)

**Skip this step entirely** when the invocation already names a specific hypothesis (inline argument like `/experiment-plan imitation/case1 dropout 0.3` or `/experiment-plan H3`). The user has already chosen, so no decision is needed — go to Step 1 with that hypothesis.

Run this step when:
- The user invoked `/experiment-plan` without a specific hypothesis, **or**
- The `experiment` loop driver invoked this skill at the top of a tick.

Inputs to read (no user interaction):
- `hypotheses.md` for the target case (header state, pending list, Iteration log)
- The 1–3 most recent `iter*_result.md` (verdicts and `Decision` sections; the `where_to_focus_next` and `次の一手` notes will inform deepen)

Decision tree (apply in order; first match wins):

1. **broaden — paused** — header `状態:` is already `paused` (set by a previous run or by the user) → emit broaden outcome.
2. **broaden — 3 consecutive rejections** — the last 3 rows of the Iteration log all have verdict = `rejected`, AND no pending `- [ ]` row offers a different mechanism → emit broaden outcome.
3. **list-consume** — at least one pending `- [ ]` hypothesis exists. Pick by priority: P1 first, then P2, then P3, skipping `(deferred)` and skipping any row with an unmet `depends on H{m}`. Within the same priority, take the topmost row.
4. **deepen** — no pending hypotheses but the most recent `iterN_result.md` has verdict ∈ {`adopted`, `inconclusive`} and provides `where_to_focus_next` or a `次の一手` line that names a concrete follow-up. Append exactly one row to the `## 仮説リスト` section:
   ```markdown
   - [ ] (auto, deep) H{n+1}: {one-sentence follow-up} — derived from iterN result
   ```
   Then proceed with this newly appended hypothesis.
5. **broaden — exhausted without follow-up** — fall-through (no pending, no follow-up signal). Emit broaden outcome.

Side effects of each branch:

- **list-consume / deepen** → continue to Step 1 with the picked hypothesis. (Deepen also writes the new row to `hypotheses.md` before continuing.)
- **broaden** → write back to `hypotheses.md`:
  - rewrite header `状態:` to `paused`
  - append a one-line comment to Iteration log: `# paused: <reason> → /experiment-hypothesize で再構築推奨`
  - update `最終更新` date

  Then **stop without writing a plan file**. Report to the user (in Japanese, ≤ 3 lines):
  > ジャンル paused: {reason}。`hypotheses.md` の状態を更新しました。次は `/experiment-hypothesize` で仮説リストを再構築してください。

  Do **not** auto-spawn `experiment-hypothesize`.

If `hypotheses.md` does not exist (one-shot single-hypothesis invocation with no list), skip this step and treat the input as list-consume mode with one synthetic hypothesis.

### Step 1 — Reality check (read-only)

No user interaction. Read:

- `backend/pipeline/<family>/case<N>/` — `main.py`, `agent.py`, primary policy / feature modules. Goal: identify changed files by path.
- The same directory's `hypotheses.md` (if present) — extract the skip list, primary metric, default episode count, exception conditions.
- Recent `iter*_result.md` / `iter*_analysis.md` (1–2 files, if any) — referenced from the plan's `関連:` line.

Surface a 3–5 line orientation to the user (in Japanese):

> 対象: `pipeline/<family>/case<N>/`、現状: X / Y / Z。`hypotheses.md` の skip list: {主要 2-3 件}。関連 iter: {paths}。

### Step 2 — Minimal hearing

`AskUserQuestion`, **at most 3 questions in one round**. Selection + Other format. Items already pinned by the skip list / `hypotheses.md` are **not** asked again.

| Possible Q | When to ask | Example options |
|---|---|---|
| **Scope** (which files / modules change) | Always (skip if Step 1 already pinned it) | `policy.py 修正` / `policy_v2.py 新設 (推薦: baseline 保持)` / `features.py 拡張` / `Other` |
| **Hyperparameter / config change** | Only when the hypothesis involves a param sweep | `before → after` via Other |
| **Estimated RunPod runtime** | Only when RunPod execution is expected | `~30min` / `~1h` / `~3h` / `Other` |
| **Validation override** | Only when overriding skip list per-hypothesis (exception condition) | `skip list 通り` ⭐ / `300 対戦を追加実施` / `Other` |

`Kaggle publicScore` is never offered as a metric. The `hypotheses.md` `主要メトリクス` / `既定 episode 数` are honored as defaults; ask explicitly only when overriding.

If `hypotheses.md` does not exist (one-shot invocation, e.g. `/experiment-plan` with a single hypothesis only), add 1 question to capture metric / episode count (default `≥300` per memory `project_imitation_case1_phase3`).

### Step 3 — Write `iterN_plan.md`

Target path:

```
docs/experiment/{family}/{yyyymmdd}_case{N}_{topic}/iterN_plan.md
```

Template (the `## 検証方法` section must reflect the skip list):

```markdown
# {Family}/case{N} — {Topic} (iter{N})

> 作成日: {yyyy-mm-dd}
> 仮説 ID: {H{n} | 単発}
> hypotheses.md: {path | 「未作成 (単発)」}
> 関連: {prior iter*_result.md / analysis.md paths}
> スコープ: {one-line scope}

## 仮説 (Hypothesis)
{one-sentence hypothesis} — {why it should work}

## 既存コードの現状 (from Step 1)
- 主要モジュール: `backend/pipeline/<family>/case<N>/...` の {要点}
- 過去 iter の所見: {related result.md/analysis.md の 1-2 行}

## スコープ (Scope)
- 変更ファイル: `backend/pipeline/<family>/case<N>/...`
- ハイパーパラメータ / config: {before → after}
- データセット / 特徴量変更: {if any, else 「なし」}

## 実装ステップ (Implementation outline)
1. {step with file path}
2. ...

## 検証方法 (Validation method)

### スキップする検証 (from hypotheses.md skip list)
- {例: ローカル self-play 300 対戦を行わない (loss curve のみで採否)}
- {例: replay 分析は実施しない}
- {例外条件があれば: 例 H3 のみ inconclusive 時に 300 対戦追加}

### 実施する検証
- ローカル: `dev/test-backend` + `uv run --directory backend pytest tests/pipeline/<family>/case<N> -x`
- (submit-shape 変更時) `uv run --directory backend python -m submit submit <family>/case<N> --dry-run`
- リモート: `dev/runpod train --case {caseN}` (RunPod skip 時は「不要」と明記)、想定所要時間 {if known}
- 評価: 対戦相手 {opponents}、エピソード数 {N | 「対戦評価 skip」}、主要メトリクス {metric}、採否しきい値 {threshold}

## リスク / 既知の不確実性
- {1-2 行}
```

Use `Write` (new file) or `Edit` (after rename). If Step 1 found an existing `plan.md` to rename, perform that too.

### Step 4 — Report

Report to the user in 3 lines or fewer (in Japanese). Always lead with the chosen mode so the loop driver / user can see the branch outcome:

- mode: `list-consume` / `deepen` / `broaden`
- (list-consume / deepen) written path + hypothesis 1 sentence + scope
- (deepen) note that a new row was appended to `hypotheses.md`
- (broaden) reason + recommendation: `/experiment-hypothesize で再構築`
- next-step suggestion: `/experiment-execution` (when a plan was written) or none (broaden)

Do not auto-spawn `experiment-execution` or `experiment-hypothesize`.

## Risk gates this skill enforces

- **Apply the decision tree in order.** broaden(paused) → broaden(3 rejected) → list-consume → deepen → broaden(exhausted). Do not skip steps or invent new branches.
- **Deepen appends only one row per invocation.** Multiple follow-ups in a single tick obscures attribution and inflates the queue.
- **Broaden never auto-spawns `experiment-hypothesize`.** Only rewrite `状態:` and recommend.
- **Don't flip existing hypothesis-row checkboxes.** That belongs to `experiment-analysis`. This skill only **adds** a row in deepen mode (and only writes header/state in broaden mode).
- **Honor the `hypotheses.md` skip list.** When `300 対戦 skip` is set, replace evaluation with `loss curve のみ` in `## 検証方法`. `Kaggle publicScore は引用しない` is default ON.
- **Avoid duplicate iter numbers.** Always `ls` existing `iter*_plan.md` and use `max(N)+1`.
- **Don't perform iteration migration silently.** When renaming an existing `plan.md` to `iter1_plan.md`, surface it in one line first (per `.claude/rules/docs.md`).
- **Never use Kaggle publicScore as a success metric.**
- **Don't run broad web research.** A user-specified single-URL spot-check is OK; broader surveys go to `experiment-hypothesize` / `research-retrieval`.
- **No code edits, commits, or RunPod launches.** Strictly a plan writer (and minimal `hypotheses.md` editor for state / appended row).

## Common shapes

| User says… | Skill behavior |
|---|---|
| `/experiment-plan H3` | Step 0 pulls H3 (inline hypothesis) → Step 0.5 skipped → Step 1 reality check → Step 2 only confirms skip-list overrides → Step 3 writes `iterN_plan.md`. Mode = list-consume. |
| `/experiment-plan imitation/case1 で dropout 0.3` | Step 0 inline → Step 0.5 skipped → if no `hypotheses.md`, treat as one-shot list-consume and ask metric / episode count once. |
| "次 iter の plan を作って" (no specific hypothesis) | Step 0 confirms case in 1 question → **Step 0.5 picks the mode**. Pending list non-empty → list-consume; empty + adopted/inconclusive last result → deepen (append row); else → broaden (paused). |
| (loop tick) `experiment` invokes this skill at the top of a tick | Step 0 skipped (case known) → Step 0.5 picks mode → Steps 1–3 if list-consume / deepen, otherwise stop and return broaden. |
| "case1 の仮説を全部リストアップして" | Initial brainstorming — belongs to `experiment-hypothesize`. Redirect. |
| "case1 paused になったから幅出しして" | Belongs to `experiment-hypothesize`. Redirect (this skill only **decides** to broaden; it does not enumerate the new list). |

## Things to avoid

- Skipping Step 0.5 when invoked without an inline hypothesis. The decision must be visible in the report.
- Appending more than one deepen row per invocation.
- Auto-spawning `experiment-hypothesize` on broaden. Recommend by name only.
- Flipping an existing hypothesis-row checkbox (that's `experiment-analysis`'s job).
- Listing multiple hypotheses inside this skill. One invocation = one hypothesis = one plan file (or zero in broaden).
- Silently overriding `hypotheses.md`'s `主要メトリクス` / `既定 episode 数` / skip list. Always confirm in Step 2.
- Asking 5+ questions. Default to ≤ 3 by leaning on stored defaults.
- Creating two `iter1_plan.md` files. `ls` first.
- Leaving an unprefixed `plan.md` next to a new `iter2_plan.md`. Always propose the rename.
- Running web research inside this skill. Broad surveys belong elsewhere.
- Embedding implementation code into `iterN_plan.md`. Plans reference paths and outline steps.
- Including Kaggle publicScore as a success metric.
- Auto-running `experiment-execution`.

## Language

- Internal reasoning and thinking should be in English
- **All user-facing output, AskUserQuestion labels/descriptions, and the written plan body must be in Japanese** (per `.claude/CLAUDE.md`)
