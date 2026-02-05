---
name: vsa-pattern-selector
description: >
  Blazor VSA パターンカタログからの適切なパターン選択支援。新機能追加、
  CRUD 操作、クエリ実装、状態遷移、バウンダリー設計などの文脈で、
  catalog/index.json の ai_decision_matrix に基づいて最適なパターンを
  提案する。Feature Slice、Pipeline Behavior、Domain Pattern、
  Query Pattern などから文脈に応じたパターンを選択。
allowed-tools:
  - Read
  - Glob
  - Grep
---

# VSA Pattern Selector

このスキルは、Blazor VSA パターンカタログからの適切なパターン選択を支援する。

機能の設計・実装時に、適切なパターンを自動的に提案する。

---

## パターン選択フローチャート

```
ユーザーの要求を分析
    ↓
【STEP 1】カテゴリを特定

├─「〇〇機能を作って」「〇〇画面を追加」
│   → Feature Slices（垂直スライス）
│
├─「すべての Command に〇〇」「システム全体で〇〇」
│   → Pipeline Behaviors（横断的関心事）
│
├─「一覧を取得」「検索」「レポート」
│   → Query Patterns
│
├─「状態遷移」「操作可否」「型安全 ID」
│   → Domain Patterns
│
├─「同時実行制御」「トランザクション保証」
│   → Infrastructure Patterns
│
└─「UI 状態管理」「リアルタイム更新」
    → UI Patterns

【STEP 2】具体的なパターンを選択（下記テーブル参照）

【STEP 3】パターン YAML を読む
    → catalog/features/*.yaml または catalog/patterns/*.yaml
```

**迷った場合**: `feature-slice` をデフォルトで選択

---

## Feature Slices（垂直スライス）

完全な機能を縦に実装するパターン。**最も頻繁に使用**。

| パターン ID | 用途 | トリガーフレーズ |
|------------|------|-----------------|
| feature-create-entity | エンティティ作成 | 「〇〇を作成」「新規登録」「追加」 |
| feature-search-entity | 検索・一覧表示 | 「〇〇を検索」「一覧画面」「フィルタ」 |
| feature-update-entity | エンティティ更新 | 「〇〇を編集」「更新」「変更」 |
| feature-delete-entity | エンティティ削除 | 「〇〇を削除」「消す」「除去」 |
| feature-import-csv | CSV インポート | 「CSV を取り込む」「一括登録」 |
| feature-export-csv | CSV エクスポート | 「CSV に出力」「ダウンロード」 |
| feature-approval-workflow | 承認ワークフロー | 「承認」「稟議」「ワークフロー」 |

---

## Query Patterns（データ取得）

| パターン ID | 用途 | トリガーフレーズ |
|------------|------|-----------------|
| query-get-list | 全件/一覧取得 | 「一覧を取得」「リスト」 |
| query-get-by-id | ID 指定取得 | 「ID で取得」「詳細表示」 |
| query-get-by-period | 期間指定取得 | 「今日/今週/期間」「日付範囲」 |
| complex-query-service | 複合条件クエリ | 「空き検索」「NOT EXISTS」「未割当」 |

---

## Domain Patterns（ドメインモデル）

| パターン ID | 用途 | トリガーフレーズ |
|------------|------|-----------------|
| boundary-pattern | 操作可否判定 | 「〇〇できるか」「権限チェック」「優先権」 |
| domain-state-machine | 状態遷移 | 「ステータス」「状態遷移」 |
| domain-validation-service | 業務ルール検証 | 「重複チェック」「〜のみ可能」「前提条件」 |
| domain-typed-id | 型安全 ID | 「強い型付け」「ProductId」 |
| domain-timeslot | 時間枠管理 | 「予約時間」「タイムスロット」 |
| domain-ordered-queue | 順序付きキュー | 「順番」「キュー」「Position」「Ready 状態」 |

---

## Pipeline Behaviors（横断的関心事）

| 順序 | パターン ID | 用途 | トリガーフレーズ |
|:---:|------------|------|-----------------|
| 100 | validation-behavior | 入力検証 | 「バリデーション」 |
| 200 | authorization-behavior | 認可チェック | 「権限」「ロール」 |
| 350 | caching-behavior | キャッシュ | 「キャッシュ」「高速化」 |
| 400 | transaction-behavior | トランザクション | 「トランザクション」 |
| 550 | audit-log-behavior | 監査ログ | 「監査」「履歴」「証跡」 |

---

## Infrastructure Patterns

| パターン ID | 用途 | トリガーフレーズ |
|------------|------|-----------------|
| concurrency-control | 同時実行制御 | 「楽観ロック」「悲観ロック」「ダブルブッキング」 |

---

## 条件付き必読パターン

特定の条件下で **必ず読むべき** パターン。

| 条件 | 必読パターン | 理由 |
|------|-------------|------|
| UI がある | boundary-pattern | AI バイアスで忘却されやすい |
| 状態遷移がある | domain-state-machine | 遷移制約の明確化 |
| 重複チェックがある | domain-validation-service | 複数エンティティの検証 |
| 予約/ダブルブッキング | concurrency-control | 同時実行制御が必須 |
| **順番管理がある** | domain-ordered-queue | Position 管理（FR-018 対策） |
| **「〜のみ可能」** | domain-validation-service | 複合前提条件（FR-017 対策） |
| **優先権のある操作** | boundary-pattern | Ready 状態の優先権（FR-021 対策） |

---

## ドメイン別推奨パターン

### 図書館・貸出管理

- audit-log-behavior（貸出・返却履歴）
- concurrency-control（同時貸出防止）
- domain-ordered-queue（予約順番管理）★FR-018
- domain-validation-service（全コピー貸出中のみ予約可能）★FR-017
- boundary-pattern（Ready 予約者の優先権）★FR-021

### 金融・決済

- audit-log-behavior（決済履歴）
- idempotency-behavior（重複決済防止）
- concurrency-control（残高更新）

### 予約システム

- domain-timeslot（予約時間枠）
- complex-query-service（空き検索）
- concurrency-control（ダブルブッキング防止）

### 承認ワークフロー

- feature-approval-workflow（承認機能）
- domain-state-machine（承認状態遷移）
- domain-approval-history（承認履歴）

---

## パターン YAML の読み方

各パターン YAML には以下のセクションがある：

| セクション | 内容 |
|-----------|------|
| `ai_selection_hints` | トリガーフレーズ、決定ロジック |
| `implementation.template` | コードテンプレート |
| `ai_guidance.common_mistakes` | 頻出ミス |
| `evidence.implementation_file` | 実装例ファイルパス |

---

## 参照

詳細は以下を参照：
- `catalog/LLM_PATTERN_INDEX.md` - パターン選択早見表
- `catalog/index.json` - ai_decision_matrix
- `catalog/DECISION_FLOWCHART.md` - パターン選択アルゴリズム
