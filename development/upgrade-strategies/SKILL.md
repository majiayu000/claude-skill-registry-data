---
name: upgrade-strategies
description: |
  アップグレード戦略の専門スキル。
  段階的移行、後方互換性、リスク軽減を提供します。

  Anchors:
  • 『Release It!』（Michael Nygard） / 適用: アップグレード戦略 / 目的: 安全な更新

  Trigger:
  バージョンアップグレード時、マイグレーション計画時、依存関係更新時に使用
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Upgrade Strategies

## 概要

依存関係の安全なアップグレード戦略と段階的更新手法を専門とするスキル。本スキルは、複雑なバージョン管理、互換性検証、段階的ロールアウト、リスク最小化を含む包括的なアップグレード戦略の策定と実行をサポートします。

詳細な手順や背景は `references/Level1_basics.md`（基礎）、`references/Level2_intermediate.md`（実務）、`references/Level3_advanced.md`（応用）、`references/Level4_expert.md`（専門）を参照してください。

## ワークフロー

### Phase 1: 計画策定

**目的**: アップグレード計画を策定し、リスクを評価する

**Task**: `agents/upgrade-planning.md`

**入力**:

- package.json、ロックファイル、アップグレード対象

**出力**:

- アップグレード計画書、互換性マトリクス

### Phase 2: 依存関係分析

**目的**: 依存関係グラフを構築し、影響範囲を把握する

**Task**: `agents/dependency-analysis.md`

**入力**:

- package.json、ロックファイル

**出力**:

- 依存関係レポート、競合・脆弱性情報

### Phase 3: テスト戦略設計

**目的**: アップグレードの安全性を検証するテスト計画を設計する

**Task**: `agents/test-strategy.md`

**入力**:

- 影響範囲、既存テストスイート

**出力**:

- テスト計画書、テストケース

### Phase 4: 段階的ロールアウト

**目的**: アップグレードを段階的に展開し、モニタリングを行う

**Task**: `agents/rollout-execution.md`

**入力**:

- アップグレード計画、テスト計画、環境情報

**出力**:

- ロールアウトレポート

## Task仕様（ナビゲーション）

| Task                   | 役割                   | 参照先                          |
| ---------------------- | ---------------------- | ------------------------------- |
| upgrade-planning.md    | アップグレード計画策定 | `agents/upgrade-planning.md`    |
| dependency-analysis.md | 依存関係分析           | `agents/dependency-analysis.md` |
| test-strategy.md       | テスト戦略設計         | `agents/test-strategy.md`       |
| rollout-execution.md   | 段階的ロールアウト実行 | `agents/rollout-execution.md`   |

## ベストプラクティス

### すべきこと

- **前提条件の確認**: `references/Level1_basics.md`を参照し、アップグレード前に環境・依存関係を完全に把握する
- **段階的実施**: 本番環境への一括アップグレードを避け、開発→ステージング→本番の段階的展開を実施する
- **互換性検証**: `references/strategy-selection-guide.md`に基づき、アップグレード前に詳細な互換性テストを実施する
- **ロールバック計画の事前準備**: `references/rollback-procedures.md`に従い、問題発生時の復旧手順を明確にしておく
- **テスト自動化**: `references/tdd-integration.md`を参照し、アップグレード検証をテスト化・自動化する
- **ドキュメント更新**: アップグレード計画、テスト結果、変更内容を記録・共有する
- **チーム間のコミュニケーション**: 変更スケジュール、影響範囲、リスク要因を関係者に事前通知する

### 避けるべきこと

- 十分なテストなしに本番環境でアップグレードを実行しない
- 単一バージョンへの一括アップグレードにより複数の破壊的変更を同時に導入しない
- ロールバック手段なしにアップグレードを開始しない
- 依存関係の相互影響やバージョン競合を考慮せずにアップグレードを進めない
- アップグレード前のバックアップやスナップショット作成を省略しない
- 既知の問題や互換性の警告を無視して進めない
- 自動スクリプトによるアップグレードを十分にレビューなしで実行しない

## リソース参照

### references/ - 学習リソース

| ファイル                      | 対象Level | 説明                                                                           |
| ----------------------------- | --------- | ------------------------------------------------------------------------------ |
| `Level1_basics.md`            | 1         | アップグレード戦略の基礎概念、バージョン管理、依存関係の基本的な扱い方         |
| `Level2_intermediate.md`      | 2         | 段階的アップグレード計画、テスト戦略、ロールバック手順、実務的な注意点         |
| `Level3_advanced.md`          | 3         | 複雑な依存関係の解決、自動化スクリプト、パフォーマンス検証、CI/CD統合          |
| `Level4_expert.md`            | 4         | エンタープライズレベルのアップグレード戦略、大規模マイグレーション、リスク管理 |
| `automation-patterns.md`      | 2-4       | アップグレード自動化パターン、スクリプト設計、CI/CD パイプラインの実装         |
| `rollback-procedures.md`      | 2-3       | ロールバック手順、フォールバック戦略、復旧テスト、タイムラインの設定           |
| `strategy-selection-guide.md` | 1-3       | アップグレード戦略の選択基準、メリット・デメリットの比較、適用シーン別ガイド   |
| `tdd-integration.md`          | 2-4       | テスト駆動型アップグレード、テストケースの設計、回帰テストの自動化             |
| `legacy-skill.md`             | -         | 旧SKILL.mdの全文（参考資料）                                                   |

### scripts/ - 自動化スクリプト

| スクリプト           | 機能                                                               |
| -------------------- | ------------------------------------------------------------------ |
| `check-upgrades.mjs` | アップグレード前の環境チェック、依存関係の分析、互換性レポート生成 |
| `validate-skill.mjs` | スキル構造の検証、リソース・テンプレートの整合性確認               |
| `log_usage.mjs`      | スキル使用記録の保存、実行統計の自動更新、評価スコアの計算         |

```bash
node .claude/skills/upgrade-strategies/scripts/check-upgrades.mjs --help
node .claude/skills/upgrade-strategies/scripts/validate-skill.mjs --help
node .claude/skills/upgrade-strategies/scripts/log_usage.mjs --help
```

### assets/ - テンプレート

| テンプレート               | 用途                                                                     |
| -------------------------- | ------------------------------------------------------------------------ |
| `upgrade-plan-template.md` | アップグレード計画書のテンプレート（段階、リスク評価、テスト計画を含む） |

```bash
cat .claude/skills/upgrade-strategies/assets/upgrade-plan-template.md
```

## 変更履歴

| Version | Date       | Changes                                                                                               |
| ------- | ---------- | ----------------------------------------------------------------------------------------------------- |
| 1.1.0   | 2026-01-01 | agents/にTask仕様書を作成、ワークフローを4フェーズに再構成                                            |
| 1.0.1   | 2025-12-31 | 18-skills.md仕様への準拠、Task仕様ナビ追加、Anchors/Trigger/allowed-tools追加、ベストプラクティス拡充 |
| 1.0.0   | 2025-12-24 | Spec alignment and required artifacts added                                                           |
