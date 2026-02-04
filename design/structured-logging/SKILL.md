---
name: structured-logging
description: |
  構造化ログのスキーマ設計、ログレベル設計、PIIマスキング、JSONログ実装を支援するスキル。
  ログ要件整理から検証までを一貫して整理する。

  Anchors:
  • Observability Engineering / 適用: ログ設計 / 目的: 可観測性向上
  • 12-Factor App / 適用: 構造化ログ / 目的: JSONログ標準化

  Trigger:
  Use when designing JSON log schemas, defining log levels, applying PII masking, or improving observability.
  structured logging, json logs, log schema, log levels, pii masking
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# structured-logging

## 概要

ログの要件整理からスキーマ設計、PIIマスキング、検証までを体系化する。

---

## ワークフロー

### Phase 1: 要件整理

**目的**: ログ対象イベントと保存要件を整理する

**アクション**:

1. `references/Level1_basics.md` で基本指針を確認する
2. イベント一覧と検索要件を整理する

**Task**: `agents/slog-001-requirements.md` を参照

### Phase 2: スキーマとレベル設計

**目的**: ログスキーマとレベル体系を定義する

**アクション**:

1. `references/log-schema-design.md` を参照する
2. `references/log-level-guide.md` を参照する
3. `assets/log-format-examples.json` を確認する

**Task**: `agents/slog-002-schema-design.md` を参照

### Phase 3: 実装と検証

**目的**: PIIマスキングとログ検証を行う

**アクション**:

1. `references/pii-masking-patterns.md` を参照する
2. `assets/logger-template.ts` を適用する
3. `scripts/validate-log-format.mjs` でログ形式を検証する

**Task**: `agents/slog-003-implementation-review.md` を参照

---

## Task仕様ナビ

| Task | 起動タイミング | 入力 | 出力 |
| --- | --- | --- | --- |
| slog-001-requirements | Phase 1開始時 | システム概要、監視目的 | ログ要件メモ |
| slog-002-schema-design | Phase 2開始時 | ログ要件メモ、既存ログ例 | ログスキーマ |
| slog-003-implementation-review | Phase 3開始時 | ログスキーマ、ログ出力例 | 実装検証レポート |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照
**注記**: Task名は目的に合わせて定義する

---

## ベストプラクティス

### すべきこと

| 推奨事項 | 理由 |
| --- | --- |
| JSON形式で統一する | 検索と集計が容易になる |
| 必須フィールドを固定化する | 分析の一貫性が保てる |
| PIIを分類してマスキングする | セキュリティ事故を防ぐ |
| ログレベルの基準を定義する | 重要度の優先順位が明確になる |

### 避けるべきこと

| 禁止事項 | 問題点 |
| --- | --- |
| プレーンテキストのみのログ | 解析が難しくなる |
| INFOの乱用 | ノイズが増えて監視精度が下がる |
| PIIの生ログ出力 | セキュリティリスクが高まる |
| スキーマ変更の未記録 | 監視ルールが破綻する |

---

## リソース参照

### scripts/（決定論的処理）

| スクリプト | 機能 |
| --- | --- |
| `scripts/validate-log-format.mjs` | ログ形式の検証 |
| `scripts/validate-skill.mjs` | スキル構造の検証 |
| `scripts/log_usage.mjs` | 使用記録の保存 |

### references/（詳細知識）

| リソース | パス | 読込条件 |
| --- | --- | --- |
| 基礎指針 | [references/Level1_basics.md](references/Level1_basics.md) | 要件整理時 |
| 実務指針 | [references/Level2_intermediate.md](references/Level2_intermediate.md) | 実装計画時 |
| 応用指針 | [references/Level3_advanced.md](references/Level3_advanced.md) | 運用設計時 |
| 専門指針 | [references/Level4_expert.md](references/Level4_expert.md) | 高度な最適化時 |
| レベル設計 | [references/log-level-guide.md](references/log-level-guide.md) | ログレベル定義時 |
| スキーマ設計 | [references/log-schema-design.md](references/log-schema-design.md) | スキーマ設計時 |
| PIIマスキング | [references/pii-masking-patterns.md](references/pii-masking-patterns.md) | マスキング設計時 |

### assets/（テンプレート・素材）

| アセット | 用途 |
| --- | --- |
| `assets/log-format-examples.json` | ログ形式の例 |
| `assets/logger-template.ts` | ロガー実装テンプレート |
