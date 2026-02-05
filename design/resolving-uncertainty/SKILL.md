---
name: resolving-uncertainty
description: Turns ambiguity into an Uncertainty Register, prioritizes items, and produces observation tasks/experiments with evidence and decision rules. Use when the user mentions uncertainty/unknowns/assumptions/validation/investigation/hypotheses/risks or cannot decide (不確実性, 曖昧, 未知, 前提, 仮説, 検証, 調査, 優先順位, 観測, 意思決定).
---

# Resolving Uncertainty

## What this Skill does
このSkillは、曖昧な状況や意思決定の停滞を「不確実性の台帳（Uncertainty Register）」として外在化し、
優先順位を付け、最小の観測タスク（実験/計測/調査）に落として前へ進める。

## Outputs (choose what fits)
- Markdown:
  - Uncertainty Register（台帳）
  - Prioritized Top-N（上位N）
  - Observation Backlog（観測タスク一覧）
- Optional machine-readable plan:
  - `uncertainty_plan.json` を生成し、`scripts/validate_uncertainty_plan.py`で検証してから実行する

## Operating principles
- 1項目 = 1つの不確実性（疑問文）に分解する
- スコアは真理ではなく「観測リソース配分」のために使う
- 観測タスクは「結果が出たら意思決定が進む」形にする（判定規則と証拠を必須にする）
- 時間がない場合は、質問で止まらず、仮定を置いて Register に“仮定”として記録する

## Procedure
### Step 0: Frame the decision
次を1〜3行で明確化する。
- 決めたいこと（Decision）
- 期限（When）
- 失敗時の損失（Stakes）
- 制約（Constraints）

### Step 1: Itemize uncertainties
`assets/uncertainty-register.md` を使って、まず10個まで項目化する。
足りない場合のみ増やす。
必要なら `references/triage-questions.md` を使って抜けを探す。

### Step 2: Normalize & de-duplicate
各項目を次の形に揃える：
- 「〜は本当に成り立つか？」の疑問文
- 既に“観測で答えが出ている”ものは uncertainty から外し、事実として別枠へ

### Step 3: Rank (prioritize)
各項目に 1〜5 でスコアを付ける（詳細は `references/scoring.md`）。
- Impact（影響度）
- Evidence（根拠の強さ）※弱いほど不確実
- Urgency（緊急度）
- Effort（観測コスト）

Priority の計算例：
Priority = Impact × (6 - Evidence) × Urgency ÷ Effort

上位N（通常3〜5）を選ぶ。

### Step 4: Convert to observation tasks
上位Nについて `assets/observation-task.md` を使い、観測タスクに落とす。
必ず含める：
- Hypothesis（仮説）
- Method（現物/証拠/知識）
- Timebox（上限時間）
- Decision rule（採用/撤回の条件）
- Evidence artifact（ログ/スクショ/計測/テスト結果など）

観測方法のカタログは `references/observation-methods.md` を参照。

### Step 5: Plan-validate-execute (optional, recommended for high stakes)
複雑・大量・破壊的な作業に繋がる場合：
1) `uncertainty_plan.json` を先に出力
2) `python scripts/validate_uncertainty_plan.py uncertainty_plan.json` を実行
3) エラーがあれば plan を修正して再検証
4) OK なら実行に進む
5) 実行後、Register に Evidence をリンクしてステータス更新

### Step 6: Close the loop
各項目を Validated / Rejected / Accepted に更新し、Evidence を必ず残す。
意思決定が絡む場合は `assets/decision-record.md` を使って決定と理由を残す。

## Examples
例：要件が曖昧で決められない
- 入力：「この機能、ユーザーが本当に必要か分からない。技術的にも不安。どう進める？」
- 出力：
  1) Decision/Constraints
  2) Uncertainty Register（10件以内）
  3) Top-3優先不確実性
  4) 観測タスク（仮説/手順/判定/証拠/タイムボックス）

より詳しい例は `references/example.md` を参照。
