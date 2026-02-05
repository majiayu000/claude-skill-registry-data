---
name: task-specification-creator
description: |
  ユーザーから与えられたタスクを単一責務の原則に基づいて分解し、
  Phase 1からPhase 11までの実行可能なタスク仕様書ドキュメントを生成する。

  スキル選定は仕様書作成時に動的に行う。使用するスキルはタスクの性質に応じて
  現在利用可能なスキル（.claude/skills/）から選定する。

  Anchors:
  • Clean Code (Robert C. Martin) / 適用: 単一責務の原則 / 目的: タスク分解の基準
  • Continuous Delivery (Jez Humble) / 適用: フェーズゲート / 目的: 品質パイプライン構築
  • Domain-Driven Design (Eric Evans) / 適用: ユビキタス言語 / 目的: 一貫した用語設計

  Trigger:
  タスク仕様書作成, タスク分解, ワークフロー設計, 実行計画作成
  Use when creating task specifications for complex development tasks.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Task Specification Creator

## 概要

ユーザーからの開発タスクを分解し、Phase 1〜Phase 11の実行可能なタスク仕様書を生成するスキル。

**核心的な考え方**:

1. **タスク仕様書を作成する**ことが目的
2. **使用するスキルは仕様書作成時に動的に選定する**
3. 現在利用可能なスキル（`.claude/skills/`）からタスクに適したものを選ぶ
4. タスク完了後は**skill-creator**でフィードバックを記録する

## ワークフロー

```
ユーザー要求
    ↓
decompose-task（タスク分解）
    ↓
┌─────────────────────────────────────┐
│ analyze-skills（利用可能スキル確認）│ ← 並列実行
│ identify-scope（スコープ定義）      │
└─────────────────────────────────────┘
    ↓
design-phases（Phase構成設計）
    ↓
generate-task-specs（タスク仕様書生成）
    ↓
┌─────────────────────────────────────┐
│ output-phase-files（ファイル出力）  │ ← 並列実行
│ update-dependencies（依存関係設定） │
└─────────────────────────────────────┘
    ↓
docs/30-workflows/{{機能名}}/phase-*.md
    ↓
Phase 1〜11 実行
    ↓
PR作成・CI通過
    ↓
docs/30-workflows/completed-tasks/{{機能名}}/ へ移動
```

### 並列実行グループ

| グループ   | 含まれるTask                            | 同期ポイント        |
| ---------- | --------------------------------------- | ------------------- |
| parallel-1 | analyze-skills, identify-scope          | design-phases       |
| parallel-2 | output-phase-files, update-dependencies | skill-feedback-loop |

## システム仕様参照（aiworkflow-requirements連携）【必須】

タスク仕様書作成時、既存システム仕様との整合性を確保するため `aiworkflow-requirements` を**必ず**参照する。

### Phase別参照要件

| Phase | 参照目的                                   | 必須 |
| ----- | ------------------------------------------ | ---- |
| 1     | 既存要件・インターフェース仕様との整合確認 | ✅   |
| 2     | アーキテクチャ・API・データベース仕様参照  | ✅   |
| 3     | 設計レビュー時の仕様準拠チェック           | ✅   |
| 4     | テスト設計時の仕様参照                     | ✅   |
| 5     | 実装時の仕様準拠確認                       | ✅   |
| 6     | リファクタリング時の仕様準拠確認           | ✅   |
| 10    | 仕様変更時のドキュメント更新               | ✅   |

### 仕様書への記載形式

各Phaseドキュメントの「参照資料」セクションに以下を**必ず**含める:

```markdown
### システム仕様（aiworkflow-requirements）

> 実装前に必ず以下のシステム仕様を確認し、既存設計との整合性を確保してください。

| 参照資料 | パス | 内容 |
| -------- | ---- | ---- |
| {{該当する仕様}} | `.claude/skills/aiworkflow-requirements/references/{{ファイル名}}.md` | {{説明}} |
```

**仕様検索**: `node .claude/skills/aiworkflow-requirements/scripts/search-spec.mjs "{{キーワード}}"`
**詳細フロー**: See [references/spec-update-workflow.md](references/spec-update-workflow.md)

## Phase構成（フレームワーク）

タスク仕様書は以下のPhase構成に従って生成する。

| Phase | 名称               | 目的                                     |
| ----- | ------------------ | ---------------------------------------- |
| 1     | 要件定義           | 目的・スコープ・受け入れ基準定義         |
| 2     | 設計               | アーキテクチャ・詳細設計                 |
| 3     | 設計レビューゲート | 要件・設計の妥当性検証                   |
| 4     | テスト作成         | TDD: Red（失敗するテスト作成）           |
| 5     | 実装               | TDD: Green（テストを通す実装）           |
| 6     | リファクタリング   | TDD: Refactor（品質改善）                |
| 7     | 品質保証           | 静的解析・セキュリティ・性能             |
| 8     | 最終レビューゲート | 全体品質・整合性検証                     |
| 9     | 手動テスト検証     | UX・実環境動作確認                       |
| 10    | ドキュメント更新   | ドキュメント更新・仕様反映・**未タスク検出** |
| 11    | PR作成             | コミット・PR・CI確認                     |

**Phase別テンプレート**: See [references/phase-templates.md](references/phase-templates.md)
**出力ディレクトリ構造**: See [references/artifact-naming-conventions.md](references/artifact-naming-conventions.md)

## Phase 11: タスク完了処理【必須】

Phase 11でPR作成・CI通過後、タスクディレクトリを完了タスクフォルダに移動する。

### タスク完了フロー

```
Phase 11: PR作成
    ↓
CI通過確認
    ↓
タスクディレクトリを completed-tasks/ に移動
    ↓
（該当する場合）未タスク指示書を削除
    ↓
変更をコミット・プッシュ
    ↓
ワークフロー完了
```

### 移動手順

```bash
# 1. タスクディレクトリをcompleted-tasksに移動
mv docs/30-workflows/{{タスク名}}/ docs/30-workflows/completed-tasks/

# 2. 移動を確認
ls docs/30-workflows/completed-tasks/ | grep {{タスク名}}

# 3. 変更をコミット
git add docs/30-workflows/
git commit -m "docs(workflows): {{タスク名}}をcompleted-tasksに移動"
git push
```

### 未タスク完了時の追加処理

**未タスク（unassigned-task）から派生したタスクが完了した場合:**

```bash
# 1. 完了タスクディレクトリを移動
mv docs/30-workflows/{{タスク名}}/ docs/30-workflows/completed-tasks/

# 2. 元の未タスク指示書を削除（タスク完了のため不要）
rm docs/30-workflows/unassigned-task/task-{{タスクID}}.md

# 3. 変更をコミット
git add docs/30-workflows/
git commit -m "docs(workflows): {{タスク名}}を完了、未タスク指示書を削除"
git push
```

### 完了条件チェックリスト

| # | 項目 | 必須 |
|---|------|------|
| 1 | PRが作成されている | ✅ |
| 2 | CIが全て通過している | ✅ |
| 3 | タスクディレクトリが `completed-tasks/` に移動済み | ✅ |
| 4 | `artifacts.json` の `status` が `"completed"` | ✅ |
| 5 | （該当時）未タスク指示書が削除済み | 条件 |

**詳細テンプレート**: See [references/phase-templates.md](references/phase-templates.md)

---

## Phase 10: 未タスク検出 & 実装ガイド作成【必須】

Phase 10では2つの必須作業を行う:

1. **未タスク検出**: 技術的負債の可視化と継続的改善
2. **実装ガイド作成**: 概念的説明と技術的詳細のドキュメント化

### Phase 10-2: 未タスク検出

| ソース | 確認項目 | Grepパターン例 |
| --- | --- | --- |
| Phase 3レビュー結果 | MINOR判定の指摘事項 | `outputs/phase-3/` |
| Phase 8レビュー結果 | MINOR判定の指摘事項 | `outputs/phase-8/` |
| Phase 9手動テスト結果 | スコープ外の発見事項 | `outputs/phase-9/` |
| 各Phase成果物 | 「将来対応」「TODO」「FIXME」 | `grep -r "TODO\|FIXME\|将来対応" outputs/` |
| コードベース | TODO/FIXME/HACK/XXXコメント | `grep -rn "TODO\|FIXME\|HACK\|XXX" packages/ apps/` |
| スキルLOGS.md | partial/failure記録 | 各使用スキルのLOGS.md |

**詳細仕様**: See [agents/generate-unassigned-task.md](agents/generate-unassigned-task.md)

### Phase 10-3: 実装ガイド作成

実装した内容を「概念的な説明」と「技術的な詳細」の両面からドキュメント化する。

#### ドキュメント要件

| セクション | 必須 | 内容 |
| --- | --- | --- |
| 概念的な説明 | ✅ | 中学生にもわかる比喩・例え話を使った説明 |
| 全体アーキテクチャ | ✅ | ASCII図解付きのレイヤー構造説明 |
| データベース設計 | 条件 | テーブル定義 + なぜこの設計にしたか |
| 各層の実装詳細 | ✅ | コード例 + 設計意図の説明 |
| 用語集 | ✅ | 専門用語の読み方・意味・コンテキスト |

#### 記述原則

1. **Why-first（なぜ優先）**: 「何をしたか」より「なぜそうしたか」を重視
2. **対比説明**: 「❌ 悪い例」と「✅ 良い例」を並べて違いを明確化
3. **図解活用**: ASCII図でアーキテクチャ・データフロー・関係性を可視化
4. **コード注釈**: コードスニペットには必ず日本語コメントで意図を補足
5. **読み方併記**: 英語の専門用語にはカタカナ読みを付記

**テンプレート**: See [assets/implementation-guide-template.md](assets/implementation-guide-template.md)

### 出力要件

| 出力物 | 必須 | 配置先 |
| --- | --- | --- |
| 未タスク検出レポート | ✅ | `outputs/phase-10/unassigned-task-report.md` |
| 実装ガイド | ✅ | `outputs/phase-10/implementation-guide.md` |
| 未タスク指示書（該当時） | 条件 | `docs/30-workflows/unassigned-task/` |

## Task仕様ナビ

| Task                     | 責務                       | 実行パターン | 入力             | 出力                  |
| ------------------------ | -------------------------- | ------------ | ---------------- | --------------------- |
| decompose-task           | タスクを単一責務に分解     | seq          | ユーザー要求     | タスク分解リスト      |
| analyze-skills           | 利用可能スキルを確認・選定 | **par**      | タスク分解リスト | スキル選定結果        |
| identify-scope           | スコープ・前提・制約を定義 | **par**      | タスク分解リスト | スコープ定義          |
| design-phases            | Phase構成を設計            | **agg**      | 上記の集約       | フェーズ設計書        |
| generate-task-specs      | タスク仕様書を生成         | seq          | フェーズ設計書   | タスク仕様書一覧      |
| output-phase-files       | 個別Markdownファイルを出力 | **par**      | タスク仕様書一覧 | phase-\*.md           |
| update-dependencies      | Phase間の依存関係を設定    | **par**      | タスク仕様書一覧 | 依存関係マップ        |
| skill-feedback-loop      | skill-creatorでFBを記録    | seq          | 実行結果         | LOGS.md更新           |
| generate-unassigned-task | 未完了タスク指示書を生成   | cond         | レビュー課題     | unassigned-task/\*.md |

**実行パターン凡例**:

- `seq`: シーケンシャル（前のTaskに依存）
- `par`: 並列実行（他と独立）
- `cond`: 条件分岐の起点
- `agg`: 集約処理（並列の終点）

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照
**注記**: 1 Task = 1 責務。複数責務を1ファイルに入れない。

## スキルフィードバック【必須】

**各Phase完了時に使用したスキルへのフィードバックを必ず記録する。** これはスキル品質改善・利用状況追跡の中核プロセス。

### 記録タイミング

| イベント       | 記録内容                                           |
| -------------- | -------------------------------------------------- |
| Phase完了時    | 使用した各スキルの結果（success/failure/partial）  |
| スキル選定時   | 選定理由と期待される効果                           |
| 問題発生時     | failure/partialとして記録し、改善点を備考に追加    |

### 記録コマンド

```bash
# フィードバック記録（各スキルごとに実行）
node .claude/skills/task-specification-creator/scripts/log_usage.mjs \
  --skill {{skill-name}} --result {{success|failure|partial}} --phase {{phase-number}}

# Phase完了・成果物登録
node .claude/skills/task-specification-creator/scripts/complete-phase.mjs \
  --workflow docs/30-workflows/{{機能名}} --phase {{N}} --artifacts "..."

# スキル仕様準拠チェック（skill-creatorに委譲）
node .claude/skills/skill-creator/scripts/quick_validate.mjs .claude/skills/{{skill-name}}
```

### Phase仕様書への記録形式

各Phase仕様書の「スキルフィードバック記録」セクションに以下を**必ず**記載:

```markdown
## スキルフィードバック記録

| スキル          | 結果    | 備考                           |
| --------------- | ------- | ------------------------------ |
| {{skill-name}}  | success | {{使用目的と結果の簡潔な説明}} |
```

**フィードバックフロー**: See [references/feedback-flow.md](references/feedback-flow.md)

## artifacts.json 更新【必須】

**各Phase完了時に `artifacts.json` を必ず更新する。** これはPhase管理・成果物追跡の中核ファイル。

### 更新タイミング

| イベント         | 更新内容                                           |
| ---------------- | -------------------------------------------------- |
| Phase完了時      | `phases.{N}.status` → `completed`、`completedAt` 追加 |
| 成果物作成時     | `phases.{N}.artifacts` に成果物情報を追加          |
| lastUpdated更新  | 常に現在のタイムスタンプに更新                     |

### 更新形式

```json
{
  "phases": {
    "N": {
      "status": "completed",
      "completedAt": "2026-01-04T16:00:00Z",
      "artifacts": [
        {
          "type": "document",
          "path": "outputs/phase-N/{{ファイル名}}.md",
          "description": "{{成果物の説明}}"
        }
      ]
    }
  }
}
```

### チェックリスト

Phase完了時に以下を**すべて**実行すること:

| # | 項目                                         | 対象ファイル                    |
| - | -------------------------------------------- | ------------------------------- |
| 1 | Phase仕様書のステータスを `完了` に更新      | `phase-N-*.md`                  |
| 2 | Phase仕様書に `完了日` を追加                | `phase-N-*.md`                  |
| 3 | Phase仕様書の完了条件をすべてチェック        | `phase-N-*.md`                  |
| 4 | **スキルフィードバックを記録**【必須】       | `phase-N-*.md` + LOGS.md        |
| 5 | **`artifacts.json` の該当Phaseを更新**【必須】 | `artifacts.json`               |
| 6 | `index.md` のPhase一覧テーブルを更新         | `index.md`                      |

**重要**: 項目4と5は必須。これらを省略するとワークフロー追跡が破綻する。

**詳細**: See [references/artifact-naming-conventions.md](references/artifact-naming-conventions.md)

## ベストプラクティス

### すべきこと

- 各Phaseを独立したMarkdownファイルとして出力
- タスクに応じて適切なスキルを動的に選定し、選定理由を明記
- Phase完了後に使用したskillをskill-creatorでフィードバック記録
- **各Phase完了時に `artifacts.json` を必ず更新**
- 100人中100人が同じ理解で実行できる粒度で記述
- コード成果物はプロジェクトディレクトリに配置（outputs/ではない）
- TodoWriteでサブタスクを管理し、進捗を可視化

### 避けるべきこと

- スキルを固定的に決めつける
- スキル選定理由を省略
- skill-creatorでのフィードバック記録を省略
- **`artifacts.json` の更新を忘れる**
- 1つのファイルに全Phaseを詰め込む
- コード成果物を `outputs/` 配下に配置する

**詳細**: See [references/quality-standards.md](references/quality-standards.md)

## リソース参照

### agents/（Task仕様書）

| Task                 | パス                                                                         |
| -------------------- | ---------------------------------------------------------------------------- |
| タスク分解           | See [agents/decompose-task.md](agents/decompose-task.md)                     |
| スキル分析           | See [agents/analyze-skills.md](agents/analyze-skills.md)                     |
| スコープ特定         | See [agents/identify-scope.md](agents/identify-scope.md)                     |
| フェーズ設計         | See [agents/design-phases.md](agents/design-phases.md)                       |
| タスク仕様書生成     | See [agents/generate-task-specs.md](agents/generate-task-specs.md)           |
| 個別ファイル出力     | See [agents/output-phase-files.md](agents/output-phase-files.md)             |
| 依存関係更新         | See [agents/update-dependencies.md](agents/update-dependencies.md)           |
| スキルフィードバック | See [agents/skill-feedback-loop.md](agents/skill-feedback-loop.md)           |
| 未完了タスク生成     | See [agents/generate-unassigned-task.md](agents/generate-unassigned-task.md) |

### references/（詳細知識）

| リソース                 | パス                                                                                       |
| ------------------------ | ------------------------------------------------------------------------------------------ |
| Phase別テンプレート      | See [references/phase-templates.md](references/phase-templates.md)                         |
| フィードバックフロー     | See [references/feedback-flow.md](references/feedback-flow.md)                             |
| 品質基準                 | See [references/quality-standards.md](references/quality-standards.md)                     |
| 成果物命名規則           | See [references/artifact-naming-conventions.md](references/artifact-naming-conventions.md) |
| 未完了タスクガイドライン | See [references/unassigned-task-guidelines.md](references/unassigned-task-guidelines.md)   |
| レビューゲート判定基準   | See [references/review-gate-criteria.md](references/review-gate-criteria.md)               |
| システム仕様更新         | See [references/spec-update-workflow.md](references/spec-update-workflow.md)               |

### assets/（テンプレート）

| テンプレート               | パス                                                                                   |
| -------------------------- | -------------------------------------------------------------------------------------- |
| Phase仕様書テンプレート    | See [assets/phase-spec-template.md](assets/phase-spec-template.md)                     |
| スキル実行指示テンプレート | See [assets/skill-execution-template.md](assets/skill-execution-template.md)           |
| フィードバック記録         | See [assets/feedback-record-template.md](assets/feedback-record-template.md)           |
| 未完了タスクテンプレート   | See [assets/unassigned-task-template.md](assets/unassigned-task-template.md)           |
| メインタスクテンプレート   | See [assets/main-task-template.md](assets/main-task-template.md)                       |
| 実装ガイドテンプレート     | See [assets/implementation-guide-template.md](assets/implementation-guide-template.md) |

### scripts/（決定論的処理）

| スクリプト                     | 用途                            | 使用例                                                                         |
| ------------------------------ | ------------------------------- | ------------------------------------------------------------------------------ |
| `log_usage.mjs`                | フィードバック記録              | `node scripts/log_usage.mjs --skill tdd-principles --result success --phase 4` |
| `validate-phase-output.mjs`    | Phase出力ファイル検証           | `node scripts/validate-phase-output.mjs docs/30-workflows/{{機能名}}`          |
| `validate-skill-selection.mjs` | スキル選定の検証（存在確認）    | `node scripts/validate-skill-selection.mjs docs/30-workflows/{{機能名}}`       |
| `complete-phase.mjs`           | Phase完了・成果物登録・依存更新 | `node scripts/complete-phase.mjs --workflow <path> --phase <N> --artifacts ""` |

## 変更履歴

| Version | Date       | Changes                                                                       |
| ------- | ---------- | ----------------------------------------------------------------------------- |
| 2.6.0   | 2026-01-05 | Phase 11タスク完了処理【必須】を追加、completed-tasks移動フローを明文化、未タスク完了時処理を追加 |
| 2.5.0   | 2026-01-05 | 実装ガイドPart2に「なぜ」の設計理由説明を必須化、用語集セクション追加         |
| 2.4.0   | 2026-01-05 | Phase 10-3: 実装ガイド作成【必須】を追加、implementation-guide-template.md追加 |
| 2.3.0   | 2026-01-05 | Phase 10未タスク検出【必須】化、generate-unassigned-task.mdを5セクション構造に更新 |
| 2.2.0   | 2026-01-04 | スキルフィードバック【必須】化、チェックリストをテーブル形式に改善            |
| 2.1.0   | 2026-01-04 | artifacts.json更新の必須化を追加、Phase完了時チェックリスト追加               |
| 2.0.0   | 2026-01-04 | 責務分離: skill仕様チェックをskill-creatorへ委譲、references/へ詳細移動       |
| 1.1.0   | 2026-01-03 | スキル仕様準拠チェック追加、リソース参照形式統一、実行パターン追加            |
| 1.0.0   | 2025-12-28 | 初版作成                                                                      |
