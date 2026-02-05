---
name: functional-non-functional-requirements
description: |
  機能要件と非機能要件の分類と定義スキル。要件を適切なカテゴリに分類し、漏れなく体系的に管理するための方法論を提供する。

  Anchors:
  • ISO/IEC 25010 品質モデル / 適用: NFR分類と品質特性定義 / 目的: 8品質特性による網羅的カバレッジ
  • Don't Make Me Think (Steve Krug) / 適用: ユーザビリティ要件定義 / 目的: 直感性と認知負荷の測定基準
  • Software Requirements (Karl Wiegers) / 適用: 要件品質検証 / 目的: SMART原則による検証可能性確保

  Trigger:
  Use when classifying requirements into functional and non-functional categories, defining measurable quality attributes for NFRs, or validating requirements completeness and consistency.
  requirements, functional, non-functional, NFR, quality attributes, ISO 25010, SMART criteria, measurability
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Functional and Non-Functional Requirements

## 概要

機能要件と非機能要件の分類と定義スキル。要件を適切なカテゴリに分類し、漏れなく体系的に管理するための方法論を提供する。

**適用範囲**: ソフトウェア開発プロジェクトの要件定義フェーズ

## ワークフロー

### Phase 1: 要件分析（Requirements Analysis）

**目的**: プロジェクトの要件を収集・分析し、初期リストを作成する

**アクション**:

1. プロジェクト概要とステークホルダー要求を収集
2. [references/classification-guide.md](references/classification-guide.md) で分類基準を確認
3. 要件を機能要件と非機能要件に暫定分類

**Task**: `agents/requirements-analyst.md` を参照

### Phase 2: 要件分類（Requirements Classification）

**目的**: 要件をFR/NFRに厳密に分類し、NFRを品質特性別に細分化する

**アクション**:

1. [references/quality-attributes.md](references/quality-attributes.md) でISO 25010品質特性を確認
2. NFRを品質特性別に細分化
3. [references/nfr-templates.md](references/nfr-templates.md) でテンプレートを適用

**Task**: `agents/requirements-classifier.md` を参照

### Phase 3: 要件検証（Requirements Validation）

**目的**: 分類済み要件の品質を検証し、完全性・一貫性を確保する

**アクション**:

1. [references/measurement-guide.md](references/measurement-guide.md) でNFR測定可能性を確認
2. `scripts/check-nfr-coverage.mjs` で品質特性カバレッジをチェック
3. [assets/nfr-definition-template.md](assets/nfr-definition-template.md) で最終成果物を作成

**Task**: `agents/requirements-validator.md` を参照

## Task仕様（ナビゲーション）

| Task                    | 起動タイミング | 入力                 | 出力               |
| ----------------------- | -------------- | -------------------- | ------------------ |
| requirements-analyst    | Phase 1        | ステークホルダー要求 | 要件初期リスト     |
| requirements-classifier | Phase 2        | 要件初期リスト       | 分類済み要件リスト |
| requirements-validator  | Phase 3        | 分類済み要件リスト   | 最終要件定義書     |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- 「何をするか」は機能要件、「どのように/どの程度」は非機能要件として分類
- NFRには必ず測定可能な目標値を設定（SMART原則）
- ISO 25010の8品質特性でNFRの網羅性を確認
- Task実行前に該当する `agents/*.md` を読み、入出力を確認する
- Phase完了後に `scripts/log_usage.mjs` で記録を残す

### 避けるべきこと

- 機能と品質の混同（「高速な検索機能」→ FR: 検索機能 + NFR: 応答時間）
- 測定不可能なNFR（「使いやすい」→「3クリック以内で目的達成」）
- セキュリティの一括分類（認証機能はFR、暗号化方式はNFR）

**詳細**: See [references/classification-guide.md](references/classification-guide.md) → よくある間違い

## リソース参照

### references/（知識外部化）

| リソース    | パス                                                                     | 内容                     |
| ----------- | ------------------------------------------------------------------------ | ------------------------ |
| 分類ガイド  | [references/classification-guide.md](references/classification-guide.md) | FR/NFR分類基準、記述形式 |
| 品質特性    | [references/quality-attributes.md](references/quality-attributes.md)     | ISO 25010、FURPS+モデル  |
| NFRテンプレ | [references/nfr-templates.md](references/nfr-templates.md)               | NFR記述パターン          |
| 測定ガイド  | [references/measurement-guide.md](references/measurement-guide.md)       | NFR測定可能性のガイド    |

### scripts/（決定論的処理）

| スクリプト               | 用途                   | 使用例                                        |
| ------------------------ | ---------------------- | --------------------------------------------- |
| `check-nfr-coverage.mjs` | 品質特性カバレッジ確認 | `node scripts/check-nfr-coverage.mjs`         |
| `log_usage.mjs`          | フィードバック記録     | `node scripts/log_usage.mjs --result success` |
| `validate-skill.mjs`     | 構造検証               | `node scripts/validate-skill.mjs`             |

### assets/（テンプレート）

| テンプレート                 | 用途                   |
| ---------------------------- | ---------------------- |
| `nfr-definition-template.md` | 最終成果物テンプレート |

## 品質特性チェックリスト

NFR網羅性を確認するための簡易チェックリスト：

- [ ] パフォーマンス: 応答時間、スループットの目標は？
- [ ] スケーラビリティ: 将来の成長に対応できるか？
- [ ] セキュリティ: 認証、認可、暗号化の要件は？
- [ ] 可用性: SLAの目標は？
- [ ] 信頼性: 障害時の動作は？
- [ ] 保守性: テスト、デプロイの要件は？
- [ ] ユーザビリティ: アクセシビリティ要件は？
- [ ] 互換性: 対応ブラウザ、デバイスは？

**詳細**: See [references/quality-attributes.md](references/quality-attributes.md)

## 変更履歴

| Version | Date       | Changes                                   |
| ------- | ---------- | ----------------------------------------- |
| 1.1.0   | 2026-01-02 | references/を整理、18-skills.md仕様準拠   |
| 1.0.1   | 2025-12-31 | EVALS.json, LOGS.md, agents/ Task仕様追加 |
| 1.0.0   | 2025-12-24 | 初版作成                                  |
