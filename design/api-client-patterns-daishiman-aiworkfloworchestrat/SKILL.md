---
name: api-client-patterns
description: |
  外部API統合における構造的パターンと腐敗防止層（Anti-Corruption Layer）の設計を専門とするスキル。API クライアントの設計、データ変換、パターンの実装を支援します。

  **Anchors**:
  • 『RESTful Web APIs』（Leonard Richardson, Mike Amundsen）/ 適用: API仕様分析と設計 / 目的: 外部API統合の基盤構築
  • 『Design Patterns』（Gang of Four）/ 適用: APIクライアント抽象化 / 目的: Adapter Patternによるインターフェース統合と保護
  • 『Domain-Driven Design』（Eric Evans）/ 適用: 境界層実装 / 目的: Anti-Corruption Layerによる外部API変更の影響隔離
  • 『Design Patterns』（Gang of Four）/ 適用: 統合インターフェース設計 / 目的: Facade Patternによる複雑なAPI統合の簡潔化
  • 『API Design Best Practices』（複数の標準仕様）/ 適用: データ変換ロジック / 目的: 型安全な形式変換と検証

  **Triggers**:
  • APIクライアントを設計する必要がある時に使用
  • 外部データを内部ドメインモデルに変換する必要がある時に使用
  • 腐敗防止層の境界を設計する必要がある時に使用
  • 外部API変更の影響を最小限に抑えたい時に使用
  • 複数のAPI統合を管理する必要がある時に使用

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# API Client Patterns

## 概要

外部API統合における構造的パターンと腐敗防止層（Anti-Corruption Layer）の設計を専門とするスキル。API クライアントの構造化設計、データ変換パターン、統合インターフェースの実装を支援します。

詳細な手順や背景は `references/Level1_basics.md` と `references/Level2_intermediate.md` を参照してください。

## ワークフロー

### Phase 1: 要件の明確化と設計方針の決定

**目的**: タスクの要件を理解し、適切なパターンを選定する

**アクション**:

1. 統合対象のAPI仕様を確認
2. 必要な変換レベルと境界を決定
3. `references/Level1_basics.md` で基礎パターンを確認

**Task**: `agents/analyze-client-requirements.md` を参照

### Phase 2: パターン実装と検証

**目的**: 選定したパターンを実装し、要件を満たしているか確認する

**アクション**:

1. `assets/api-client-template.ts` と `assets/transformer-template.ts` を参照
2. 関連リソース（adapter-pattern.md、anti-corruption-layer.md など）に基づいて実装
3. 型安全性とエラーハンドリングを確認

**Task**: `agents/implement-client-pattern.md` を参照

### Phase 3: 検証と記録

**目的**: 成果物の品質を確認し、ナレッジを記録する

**アクション**:

1. `scripts/validate-api-client.mjs` で実装の検証
2. `scripts/log_usage.mjs` で使用記録を保存
3. 実装パターンのドキュメント化

**Task**: `agents/validate-client.md` を参照

## Task仕様ナビ

| Task                      | 概要                                                | 対応する Phase | リソース                                              |
| ------------------------- | --------------------------------------------------- | -------------- | ----------------------------------------------------- |
| APIクライアント設計       | APIの構造と仕様を分析し、クライアントの骨組みを設計 | Phase 1, 2     | Level1_basics.md, adapter-pattern.md                  |
| データ変換パターン        | 外部APIデータを内部ドメインモデルに変換             | Phase 2        | data-transformer-patterns.md, transformer-template.ts |
| Anti-Corruption Layer実装 | API変更の影響を隔離する境界層の実装                 | Phase 1, 2     | anti-corruption-layer.md, Level2_intermediate.md      |
| Facade設計                | 複数APIを統合した統一インターフェースの設計         | Phase 1, 2     | facade-pattern.md, Level3_advanced.md                 |
| エラーハンドリング        | APIエラーの統一的な処理と変換                       | Phase 2        | Level2_intermediate.md, Level3_advanced.md            |
| 型安全性確保              | TypeScriptによる型定義と検証の実装                  | Phase 2        | Level1_basics.md, api-client-template.ts              |
| 実装検証                  | 実装の品質確認とバリデーション                      | Phase 3        | validate-api-client.mjs                               |

## ベストプラクティス

### すべきこと

- 外部API仕様を詳細に分析した上で設計を開始する
- 変換ロジックを独立した関数に分離する
- APIの変更に強い設計を心がける（Anti-Corruption Layer）
- 型定義を先に作成し、型安全性を確保する
- エラーハンドリングを一貫性を持たせて実装する
- ドメインモデルとAPI仕様の差異を明確に文書化する

### 避けるべきこと

- APIデータをそのまま内部モデルとして使用する
- 変換ロジックを多数の箇所に分散させる
- エラーハンドリングを各クライアントで異なる実装にする
- 型定義なしで実装を進める
- アンチパターンや注意点を確認せずに進める

## リソース参照

### リソース読み取り

```bash
# 基礎から専門的内容まで段階的に学習
cat .claude/skills/api-client-patterns/references/Level1_basics.md
cat .claude/skills/api-client-patterns/references/Level2_intermediate.md
cat .claude/skills/api-client-patterns/references/Level3_advanced.md
cat .claude/skills/api-client-patterns/references/Level4_expert.md

# パターン別詳細
cat .claude/skills/api-client-patterns/references/adapter-pattern.md
cat .claude/skills/api-client-patterns/references/anti-corruption-layer.md
cat .claude/skills/api-client-patterns/references/data-transformer-patterns.md
cat .claude/skills/api-client-patterns/references/facade-pattern.md
```

### テンプレート参照

```bash
cat .claude/skills/api-client-patterns/assets/api-client-template.ts
cat .claude/skills/api-client-patterns/assets/transformer-template.ts
```

### スクリプト実行

```bash
node .claude/skills/api-client-patterns/scripts/validate-api-client.mjs --help
node .claude/skills/api-client-patterns/scripts/validate-skill.mjs --help
node .claude/skills/api-client-patterns/scripts/log_usage.mjs --help
```

## 変更履歴

| Version | Date       | Changes                                                   |
| ------- | ---------- | --------------------------------------------------------- |
| 3.0.0   | 2025-12-31 | agents/3ファイル追加、Phase別Task参照を追加               |
| 2.0.0   | 2025-12-31 | 18-skills.md仕様に準拠、Task仕様ナビ、Trigger/Anchors追加 |
| 1.0.0   | 2025-12-24 | 初期仕様と成果物の整備                                    |
