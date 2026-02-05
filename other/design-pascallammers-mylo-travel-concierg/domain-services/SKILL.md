---
name: domain-services
description: |
  ドメイン駆動設計におけるドメインサービスの識別・設計・実装を専門とするスキル。
  エンティティや値オブジェクトに属さないドメインロジックを適切にモデル化する。

  Anchors:
  • Domain-Driven Design (Eric Evans) / 適用: サービス識別パターン / 目的: ドメインロジックの適切な配置
  • Implementing DDD (Vaughn Vernon) / 適用: サービス実装ガイドライン / 目的: 実践的な設計指針
  • Clean Architecture (Robert Martin) / 適用: 依存性逆転の原則 / 目的: テスト容易性の確保

  Trigger:
  Use when identifying domain services, implementing cross-aggregate operations, designing service boundaries, separating domain and application services.
  domain service, cross-aggregate, stateless, domain logic, service boundary
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Domain Services

## 概要

ドメイン駆動設計におけるドメインサービスの識別・設計・実装を専門とするスキル。エンティティや値オブジェクトに属さないドメインロジックを適切にモデル化し、貧血ドメインモデルを回避する。

## ワークフロー

### Phase 1: サービス候補の識別

**目的**: ドメインサービスが必要な箇所を特定

**アクション**:

1. ドメインモデル（集約・エンティティ）を把握
2. エンティティに属さないドメインロジックを識別
3. 複数集約にまたがる操作を特定
4. ステートレスに実装可能か評価

**Task**: `agents/service-candidate-identifier.md` を参照

### Phase 2: サービス設計

**目的**: ドメインサービスのインターフェースと責務を設計

**アクション**:

1. サービスの責務を明確化
2. ドメイン言語でインターフェースを設計
3. 依存関係を設計（抽象に依存）
4. テンプレートを使用して実装

**Task**: `agents/service-designer.md` を参照

### Phase 3: 検証と記録

**目的**: DDD原則への準拠を検証

**アクション**:

1. `scripts/validate-service-design.mjs` で検証
2. ステートレス性・ドメイン言語・依存性を確認
3. `scripts/log_usage.mjs` で記録

**Task**: `agents/service-validator.md` を参照

## Task仕様ナビ

| Task                         | 起動タイミング | 入力           | 出力               |
| ---------------------------- | -------------- | -------------- | ------------------ |
| service-candidate-identifier | Phase 1開始時  | ドメインモデル | サービス候補リスト |
| service-designer             | Phase 2開始時  | 候補リスト     | サービス仕様書     |
| service-validator            | Phase 3開始時  | サービス設計   | 検証レポート       |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項           | 理由                   |
| ------------------ | ---------------------- |
| ステートレスに設計 | テスト容易性・再利用性 |
| ドメイン言語を使用 | ビジネス理解の促進     |
| 単一責務に集中     | 保守性向上             |
| 抽象に依存         | 依存性逆転の原則       |
| べき等性を考慮     | 信頼性・再試行容易性   |

### 避けるべきこと

| 禁止事項                   | 問題点               |
| -------------------------- | -------------------- |
| 状態を持つサービス         | テスト困難・副作用   |
| 技術用語の使用             | ドメイン知識の希薄化 |
| エンティティロジックの抽出 | 貧血ドメインモデル   |
| インフラへの直接依存       | テスト困難・結合度増 |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                             | 機能               |
| -------------------------------------- | ------------------ |
| `validate-service-design.mjs`          | サービス設計の検証 |
| `analyze-service-responsibilities.mjs` | 責務分析           |
| `log_usage.mjs`                        | フィードバック記録 |
| `validate-skill.mjs`                   | スキル構造の検証   |

### references/（詳細知識）

| リソース         | パス                                        | 読込条件           |
| ---------------- | ------------------------------------------- | ------------------ |
| サービスパターン | `references/service-patterns.md`            | パターン参照時     |
| サービス境界     | `references/service-vs-application.md`      | 境界設計・判断時   |
| 使用判断基準     | `references/when-to-use-domain-services.md` | サービス候補判断時 |

### assets/（テンプレート）

| アセット                     | 用途                         |
| ---------------------------- | ---------------------------- |
| `domain-service-template.ts` | ドメインサービステンプレート |

## 変更履歴

| Version | Date       | Changes                              |
| ------- | ---------- | ------------------------------------ |
| 2.1.0   | 2026-01-01 | エージェント追加・検証スクリプト追加 |
| 2.0.0   | 2026-01-01 | 18-skills.md仕様完全準拠版に再構築   |
| 1.0.0   | 2025-12-24 | 初版作成                             |
