---
name: checkpoint-manager
description: タスクの進捗を追跡・管理するスキル。会話開始時に未完了タスクを確認、新規タスク依頼時にタスク開始を提案、作業完了時に完了報告を提案。チェックポイントシステムと連携。
---

# チェックポイント管理スキル

タスクの進捗を一貫性を持って追跡・報告するためのスキルです。

## 自動提案のタイミング

| 状況 | 提案内容 |
|------|----------|
| 会話開始時 | 「未完了タスクを確認しますか？」 |
| 新しいタスク依頼時 | 「チェックポイントを開始しますか？」 |
| 指示書を読み込む前 | 「指示書使用を記録しますか？」 |
| 作業の区切り | 「進捗を報告しますか？」 |
| 作業完了時 | 「タスクを完了しますか？」 |

## ワークフロー概要

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  pending    │    │  start      │    │  progress   │    │  complete   │
│  確認       │ → │  開始       │ → │  進捗報告   │ → │  完了       │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                          ↓
                   ┌─────────────┐
                   │ instruction │
                   │ 指示書管理  │
                   └─────────────┘
```

詳細は [workflow.md](workflow.md) を参照。

## コマンド一覧

### タスク管理

```bash
# 未完了タスクの確認
scripts/checkpoint.sh pending

# 新しいタスクを開始（タスクIDは自動生成）
scripts/checkpoint.sh start "<タスク名>" <ステップ数>

# 進捗を報告（指示書使用中のみ）
scripts/checkpoint.sh progress <task-id> <current> <total> "<status>" "<next>"

# タスクを完了（すべての指示書が完了している必要あり）
scripts/checkpoint.sh complete <task-id> "<result>"

# エラーを報告
scripts/checkpoint.sh error <task-id> "<message>"
```

### 指示書管理

```bash
# 指示書の使用を開始
scripts/checkpoint.sh instruction-start "<path>" "<purpose>" [task-id]

# 指示書の使用を完了
scripts/checkpoint.sh instruction-complete "<path>" "<result>" [task-id]
```

### 状態確認

```bash
# タスクの詳細履歴を表示
scripts/checkpoint.sh summary <task-id>
```

## 使用シナリオ

### シナリオ1: 会話開始時

ユーザーが新しい会話を開始したとき、未完了タスクがないか確認を提案：

```
AI: 未完了のタスクがあるか確認しましょうか？

# 実行
scripts/checkpoint.sh pending
```

### シナリオ2: 新規タスク依頼時

ユーザーが「○○を実装して」などの依頼をしたとき：

```
AI: チェックポイントを開始しますか？
    タスク名: [ユーザーの依頼内容]
    推定ステップ: [作業の複雑さから推定]

# 実行
scripts/checkpoint.sh start "機能実装" 5
# → タスクID: TASK-123456-abc123
```

### シナリオ3: 指示書使用時

指示書を読み込む前に記録：

```
AI: 指示書の使用を記録しますか？

# 実行
scripts/checkpoint.sh instruction-start "instructions/ja/presets/web_api.md" "REST API開発" TASK-123456-abc123
```

### シナリオ4: 作業の区切り

一定の作業が完了したとき：

```
AI: 進捗を報告しますか？
    現在: 2/5 ステップ
    状況: 設計完了
    次: 実装開始

# 実行
scripts/checkpoint.sh progress TASK-123456-abc123 2 5 "設計完了" "実装開始"
```

### シナリオ5: 作業完了時

タスクが完了したとき：

```
AI: タスクを完了しますか？
    成果: [作業の成果をまとめ]

# 実行（指示書完了を先に）
scripts/checkpoint.sh instruction-complete "instructions/ja/presets/web_api.md" "3エンドポイント実装" TASK-123456-abc123

# その後タスク完了
scripts/checkpoint.sh complete TASK-123456-abc123 "REST API 3エンドポイント実装完了"
```

## ワークフロー制約

| 制約 | 内容 |
|------|------|
| 進捗報告 | 指示書使用中のみ実行可能 |
| タスク完了 | すべての指示書が完了している必要あり |
| タスクID省略 | 指示書コマンドでは警告表示 |

## 判断基準

### タスク開始を提案する条件

- ユーザーが具体的な作業を依頼した
- 複数ステップが予想される作業
- 「実装して」「作成して」「修正して」などのキーワード

### 進捗報告を提案する条件

- 一定量のコード変更があった
- テストが通った/失敗した
- 作業の区切りが明確

### タスク完了を提案する条件

- ユーザーが「完了」「できた」と言った
- すべての要求が満たされた
- テストがパスした

## 注意事項

- タスクIDは自動生成（例: TASK-123456-abc123）
- ステータスとアクションは短く明確に
- 同じタスクでは同じタスクIDを使用
- `scripts/checkpoint.sh` はプロジェクトルートから実行
