---
name: executor-resolver
description: タスクの性質を LLM ベースで深く分析し、適切な executor（claudecode/codex/coderabbit/user）を判定する専門 Skill。キーワードベースの単純判定を置き換える。
---

# Executor Resolver Skill

タスクの性質を深層分析し、最適な executor を判定する Skill。

> **設計意図**: キーワードベースの単純判定では見逃される複雑なケースに対応。
> タスクの複雑さ、技術要件、依存関係を総合的に分析して判定。

---

## Purpose

- **タスク性質分析**: 複雑さ、タイプ、テスト要否を判定
- **executor 判定**: LLM ベースの深い分析で最適な executor を決定
- **判定根拠の提示**: 判定理由と代替案を明示
- **subtask 単位アサイン**: 各 subtask に適切な executor を割り当て

---

## When to Use

```yaml
triggers:
  - pm SubAgent が playbook 作成時に executor を決定する際
  - subtask ごとの executor アサインが必要な場合
  - 複雑なタスクで executor 判定に迷う場合

invocation:
  # pm SubAgent からの呼び出し
  Task(
    subagent_type='executor-resolver',
    prompt='タスク内容または subtask リスト'
  )

  # または Skill として呼び出し
  Skill(skill='executor-resolver', input='タスク内容')
```

---

## Integration with pm.md

```yaml
pm_flow:
  step_0: ユーザープロンプトを受ける
  step_0.5: prompt-analyzer を呼び出す
  step_0.6: executor-resolver を呼び出す（executor 判定）
  step_1: 分析結果を基に understanding-check を実施
  step_2: ユーザー承認を得る
  step_3: playbook を作成する（executor 情報を含む）

連携方法:
  1. pm が executor-resolver を呼び出す
  2. executor-resolver がタスク分析と executor 判定を返す
  3. pm が判定結果を playbook の各 subtask に適用
```

---

## Executor 定義（play/template/plan.json 準拠）

```yaml
claudecode:
  説明: Claude Code が直接実行（デフォルト）
  適用条件:
    - ドキュメント作成・編集
    - 設定ファイルの軽微な変更
    - ファイル操作（移動、コピー、削除）
    - 設計・計画立案
    - 調査・分析
    - 軽量なコード修正（10行以下）
  不適用条件:
    - 複雑なロジック実装
    - 大規模なコード変更（50行以上）

codex:
  説明: Codex CLI でコード生成
  適用条件:
    - 本格的なコード実装
    - 複雑なロジック・アルゴリズム
    - リファクタリング
    - テストコード作成
    - API 実装
    - 50行以上の新規コード
  判定シグナル:
    - 「実装」「コーディング」キーワード
    - .ts/.tsx/.js/.jsx/.py 等のコード拡張子への変更
    - npm test, npm build 等のコマンド実行が必要

coderabbit:
  説明: CodeRabbit CLI でコードレビュー
  適用条件:
    - コードレビュー
    - セキュリティチェック
    - 品質チェック
    - PR 前の自動レビュー
  判定シグナル:
    - 「レビュー」「チェック」「品質」キーワード
    - レビュー対象コードの指定

user:
  説明: CLI 外の手動作業
  適用条件:
    - 外部サービス登録（Vercel, GCP, Stripe）
    - API キー取得
    - 手動デプロイ
    - 意思決定
    - 支払い情報入力
  判定シグナル:
    - 「登録」「サインアップ」「契約」
    - 「API キー」「シークレット」「環境変数設定」
    - 「選んでください」「決めてください」
```

---

## Output Format

```yaml
resolution:
  task_analysis:
    complexity: high|medium|low
    type: coding|documentation|configuration|review|manual
    requires_testing: true|false
    estimated_lines: {概算行数}
    
  executor_decision:
    recommended: claudecode|codex|coderabbit|user
    confidence: high|medium|low
    rationale: "{判定理由}"
    alternatives:
      - executor: "{代替 executor}"
        reason: "{代替を選ぶ場合の理由}"
  
  subtask_assignments:
    - subtask_id: "{ID}"
      executor: "{executor}"
      rationale: "{理由}"
```

---

## Related Files

| ファイル | 役割 |
|----------|------|
| .claude/skills/executor-resolver/agents/executor-resolver.md | SubAgent 定義 |
| .claude/skills/prompt-analyzer/SKILL.md | プロンプト分析（連携元） |
| .claude/skills/golden-path/agents/pm.md | pm SubAgent（呼び出し元） |
| play/template/plan.json | executor 定義の原本 |
