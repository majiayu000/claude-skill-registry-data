---
name: agent-validation-testing
description: |
  エージェントの検証とテストケース設計を専門とするスキル。

  **Anchors:**
  • Test-Driven Development: By Example（Kent Beck）/ 適用: エージェント検証とテストケース設計 / 目的: Red-Green-Refactorパターンに基づく信頼性の高い検証

  **Trigger:**
  エージェント検証・テストケース設計・テスト実装・結果評価・バリデーション実行時に使用

  **公式リソース:**
  - Kent Beck『Test-Driven Development: By Example』: TDDの基本原則と実装パターン
  - Level 1-4のガイドで段階的に習得可能
  - テストケースパターンと実装テンプレート完備

allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Edit
  - Glob
---

# Agent Validation Testing

## 概要

このスキルは、エージェントの検証とテストケース設計を専門とします。テスト駆動開発（TDD）の原則に基づいて、エージェントの動作を検証し、包括的なテストケースを設計・実装します。

Kent Beck著『Test-Driven Development: By Example』の Red-Green-Refactor パターンを適用し、エージェントの信頼性と品質を確保します。詳細な手順や背景は以下を参照してください：

- `references/Level1_basics.md` - 基礎的な検証テスト手法
- `references/Level2_intermediate.md` - 実務的なテストケース設計
- `references/Level3_advanced.md` - 複雑なシナリオの検証
- `references/Level4_expert.md` - エキスパートレベルの手法

## ワークフロー

### Phase 1: 目的と前提の整理

**目的**: タスクの目的と前提条件を明確にする

**アクション**:

1. `references/Level1_basics.md` と `references/Level2_intermediate.md` を確認
2. エージェントの検証対象と検証方法を明確化
3. 必要なテンプレートとスクリプトを特定

**Task**: `agents/analyze-validation-context.md` を参照

### Phase 2: スキル適用

**目的**: スキルの指針に従って具体的な作業を進める

**アクション**:

1. テストケース設計フェーズ（`references/test-case-patterns.md` 参照）
2. テスト実装フェーズ（`assets/test-case-template.json` 活用）
3. 検証実行と結果分析
4. フィードバック反映と改善

**Task**: `agents/design-test-cases.md` を参照

### Phase 3: 検証と記録

**目的**: 成果物の検証と実行記録の保存

**アクション**:

1. `scripts/validate-skill.mjs` でスキル構造を確認
2. テストケースが要件に合致するか確認
3. 検証結果をドキュメント化
4. `scripts/log_usage.mjs` を実行して記録を残す

**Task**: `agents/validate-tests.md` を参照

## Task仕様ナビ

| Task                 | 説明                                 | 参照リソース            | 対応フェーズ |
| -------------------- | ------------------------------------ | ----------------------- | ------------ |
| エージェント検証計画 | 検証対象を特定し、検証方法を設計     | Level1_basics.md        | Phase 1      |
| テストケース設計     | TDD原則に従ったテストケースを設計    | test-case-patterns.md   | Phase 2      |
| テスト実装           | テストコード実装とテンプレート活用   | test-case-template.json | Phase 2      |
| エッジケース検証     | 境界値とエラーケースの検証           | Level2_intermediate.md  | Phase 2      |
| パフォーマンス検証   | 応答時間とリソース使用量の測定       | Level3_advanced.md      | Phase 3      |
| 結果分析と改善       | テスト結果の分析とフィードバック反映 | Level4_expert.md        | Phase 3      |
| バリデーション実行   | スクリプトによる最終検証             | validate-skill.mjs      | Phase 3      |
| 記録保存             | テスト実行記録を自動保存             | log_usage.mjs           | Phase 3      |

## ベストプラクティス

### すべきこと

- **早期にテストを書く**: 実装前にテストケースを設計（TDD）
- **エージェント検証計画を立てる**: 検証対象と検証方法を明確化
- **テストケース設計パターンを活用**: `references/test-case-patterns.md` を参照
- **エッジケースを網羅**: 境界値、エラー条件、異常系を含める
- **テンプレートを活用**: `assets/test-case-template.json` を使用
- **デプロイ前に最終検証**: 本番環境での問題を未然に防止
- **テスト結果を記録**: `scripts/log_usage.mjs` で実行記録を保存
- **フィードバックループを回す**: テスト結果から改善点を抽出

### 避けるべきこと

- **Red-Green-Refactorサイクルを無視する**: TDDの原則に従う
- **テストなしに実装を進める**: バグの温床になる
- **境界値テストを省く**: エッジケースは重要な検証項目
- **テスト結果の分析を怠る**: パターンから学習する
- **アンチパターン適用**: `references/Level2_intermediate.md` の注意点を確認
- **レベルに応じた学習をスキップ**: Level1 → Level4の段階的習得
- **スクリプト検証をスキップ**: 最終確認は自動化スクリプトで実施

## リソース参照

### 学習ガイド（段階的習得）

| レベル | リソース                            | 対象                     | 学習時間 |
| ------ | ----------------------------------- | ------------------------ | -------- |
| 基礎   | `references/Level1_basics.md`       | テスト駆動開発の基本原則 | 2-3時間  |
| 実務   | `references/Level2_intermediate.md` | 実務的なテストケース設計 | 4-5時間  |
| 応用   | `references/Level3_advanced.md`     | 複雑なシナリオの検証     | 6-8時間  |
| 専門   | `references/Level4_expert.md`       | エキスパートレベルの手法 | 8-10時間 |

### パターンとテンプレート

- **テストケース設計パターン**: `references/test-case-patterns.md`
  - Red-Green-Refactorパターン
  - エッジケース検証パターン
  - パフォーマンステストパターン

- **テスト実装テンプレート**: `assets/test-case-template.json`
  - JSON Schema形式のテストテンプレート
  - 再利用可能な構造化テストケース
  - 自動検証対応フォーマット

### 検証ツールとスクリプト

```bash
# スキル構造の検証
node .claude/skills/agent-validation-testing/scripts/validate-skill.mjs

# エージェント検証
node .claude/skills/agent-validation-testing/scripts/validate-agent.mjs --agent <agent-name>

# 使用記録とメトリクス
node .claude/skills/agent-validation-testing/scripts/log_usage.mjs --check
```

### 参考資料

- `references/legacy-skill.md` - 旧SKILL.mdの全文（移行参考）
- `references/requirements-index.md` - 要求仕様の索引（docs/00-requirements と同期）
- 参考書籍: Kent Beck『Test-Driven Development: By Example』

## 変更履歴

| Version | Date       | Changes                                                                                                       |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------- |
| 2.0.0   | 2025-12-31 | agents/3ファイル追加、Phase別Task参照を追加                                                                   |
| 1.1.0   | 2025-12-31 | 18-skills.md仕様への完全準拠: Anchors/Trigger定義、Task仕様ナビ追加、リソース参照整理、ベストプラクティス拡充 |
| 1.0.0   | 2025-12-24 | 初版リリース: スキル構造定義、基本ワークフロー、段階的学習ガイド                                              |
