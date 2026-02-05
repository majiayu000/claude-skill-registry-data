---
name: state
description: このワークスペースの state.md 管理、playbook 運用の専門知識。state.md の更新、focus の切り替え、done_criteria の判定、CRITIQUE の実行時に使用する。
---

# Workspace Management Skill

このワークスペース固有の管理知識を提供します。

## state.md の構造

```yaml
# 必須セクション
focus:
  current: <focus-value>    # setup | product | plan-template
  project: plan/project.md  # プロジェクト計画ファイル

playbook:
  active: <playbook-path>   # 現在の playbook パス
  branch: <branch-name>     # playbook に紐づくブランチ

goal:
  milestone: <milestone-id> # 現在のマイルストーン
  phase: <phase-id>         # 現在のフェーズ
  done_criteria:            # 達成条件（テストとして扱う）
    - criteria1
    - criteria2

session:
  last_start: <timestamp>   # セッション開始時刻
  last_clear: <timestamp>   # 最後の /clear 実行時刻

config:
  security: admin           # セキュリティレベル
  toolstack: A              # A: Claude Code only | B: +Codex | C: +Codex+CodeRabbit
```

## focus の有効値と編集権限

| focus.current | 用途 | main での Edit/Write |
|---------------|------|---------------------|
| setup | 新規ユーザーのセットアップ | 許可 |
| product | 新規ユーザーのプロダクト開発 | 許可 |
| plan-template | テンプレート編集 | 許可 |
| thanks4claudecode | ワークスペース作業 | ブロック（ブランチ必須）|
| workspace | 一般的なワークスペース作業 | ブロック（ブランチ必須）|

**常に編集可能**: state.md, README.md

## CRITIQUE の実行方法

done と判定する前に必ず実行:

```
[CRITIQUE]
done_criteria 達成の証拠:
  - {criteria}: {PASS|FAIL} - {具体的な証拠}
playbook 自体の妥当性: {問題なし|修正が必要}
成果物の動作確認: {確認済み|未確認}
判定: {PASS|FAIL}
```

## state.md 更新のルール

1. phase 完了時は state.md の goal.phase を次の phase に更新
2. playbook 完了時は playbook.active を null または次の playbook に更新
3. done_criteria を満たしたら証拠と共に記録

## playbook 必須ルール

```yaml
条件:
  playbook.active: null

対応:
  1. 作業開始禁止
  2. まず playbook を作成

手順:
  1. plan/template/playbook-format.md を読む
  2. ユーザーにヒアリング:
     - 何を作るか（ゴール）
     - 完了条件は何か（done_criteria）
     - フェーズ分割
  3. plan/playbook-{name}.md を作成
  4. state.md の playbook.active を更新
  5. 作業開始

なぜ必須か:
  - playbook なし = done_criteria なし = 完了判定不可能
  - 「計画なしで作業 → 自己報酬詐欺」の防止
```

## playbook 作成テンプレート

```yaml
# plan/playbook-{name}.md

## meta
project: {プロジェクト名}
branch: {ブランチ名}
created: {今日の日付}
derives_from: {project.milestone の ID}

## goal
summary: {1行の目標}
done_when:
  - {最終完了条件1}
  - {最終完了条件2}

## phases
- id: p1
  name: {フェーズ名}
  goal: {このフェーズの目標}
  executor: claudecode
  done_criteria:
    - {完了条件1}
    - {完了条件2}
  status: pending
```
