---
name: rbac-implementation
description: |
  ロールベースアクセス制御（RBAC）の設計と実装パターンを提供するスキル。
  最小権限の原則に基づくロール体系設計、多層アクセス制御、
  権限チェックロジック、ポリシーエンジン構築を支援。

  Anchors:
  • 『Web Application Security』（Hoffman）/ 適用: アクセス制御設計 / 目的: セキュアな権限実装
  • NIST RBAC Model / 適用: ロール階層設計 / 目的: 標準準拠の権限モデル
  • OWASP Access Control Cheat Sheet / 適用: 実装パターン / 目的: セキュリティベストプラクティス

  Trigger:
  Use when designing role-based access control, implementing permission checks, building policy engines, or setting up multi-layer authorization.
  rbac, role, permission, authorization, access control, policy, middleware, least privilege

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# ロールベースアクセス制御（RBAC）実装

## 概要

ロールベースアクセス制御（RBAC）の設計と実装パターンを提供するスキル。最小権限の原則に基づくロール体系設計から、多層アクセス制御、ポリシーエンジン構築までを段階的にガイドします。

## ワークフロー

### Phase 1: 要件整理

**目的**: アクセス制御の要件とシステムの権限モデルを整理する

**アクション**:

1. 保護対象リソースを特定（API、データ、機能）
2. アクター（ユーザー種別）を列挙
3. 必要な権限操作（CRUD + 特殊操作）を定義

**Task**: `agents/organize-requirements.md` を参照

### Phase 2: ロール体系設計

**目的**: 適切なロールと権限の体系を設計する

**アクション**:

1. ロール階層（admin > manager > user > guest）を設計
2. 各ロールへの権限割り当てを決定
3. ロール継承とオーバーライドルールを定義

**Task**: `agents/role-design.md` を参照

### Phase 3: 多層実装

**目的**: ミドルウェア、APIルート、データ層で一貫した権限チェックを実装

**アクション**:

1. 認証ミドルウェアでロール取得
2. APIルートで権限チェック
3. データ層でRow-Level Securityを適用

**Task**: `agents/multi-layer-control.md` を参照

### Phase 4: 権限チェック実装

**目的**: 効率的で保守しやすい権限チェックロジックを実装

**アクション**:

1. 権限チェック関数/デコレーターを実装
2. キャッシュ戦略で権限照会を最適化
3. 監査ログでアクセス履歴を記録

**Task**: `agents/permission-check.md` を参照

### Phase 5: 検証

**目的**: RBAC設定の正確性とセキュリティを検証

**アクション**:

1. 権限マトリクスのカバレッジを確認
2. 権限昇格の脆弱性をテスト
3. ロール変更時の影響範囲を検証

**Task**: `agents/implement-rbac.md` を参照

## Task仕様ナビ

| Task                  | 起動タイミング | 入力             | 出力             |
| --------------------- | -------------- | ---------------- | ---------------- |
| organize-requirements | Phase 1開始時  | システム要件     | 要件定義書       |
| role-design           | Phase 2開始時  | 要件定義書       | ロール設計書     |
| multi-layer-control   | Phase 3開始時  | ロール設計書     | 多層実装コード   |
| permission-check      | Phase 4開始時  | 多層実装コード   | 権限チェック実装 |
| implement-rbac        | Phase 5開始時  | 権限チェック実装 | 検証済みRBAC     |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                           | 理由                   |
| ---------------------------------- | ---------------------- |
| 最小権限の原則を適用               | 攻撃面を最小化         |
| 多層防御を実装                     | 単一点障害を防止       |
| 権限チェックを集中管理             | 一貫性確保、保守性向上 |
| 権限変更を監査ログに記録           | セキュリティ監査対応   |
| ロールと権限の対応をドキュメント化 | 可読性と保守性を確保   |
| テストで権限昇格を検証             | 脆弱性の早期発見       |

### 避けるべきこと

| 禁止事項                   | 問題点                         |
| -------------------------- | ------------------------------ |
| 権限チェックの分散実装     | 一貫性を失い、抜け漏れ発生     |
| ハードコード化した権限     | 保守性低下、変更困難           |
| 過剰な権限付与             | 最小権限の原則違反             |
| ドキュメントなしの権限体系 | チーム間での認識齟齬           |
| 権限テストなしの本番運用   | セキュリティインシデントリスク |
| Row-Level Securityの省略   | データ層での防御欠如           |

## リソース参照

### references/（詳細知識）

| リソース   | パス                                                                                 | 読込条件               |
| ---------- | ------------------------------------------------------------------------------------ | ---------------------- |
| ロール設計 | [references/role-permission-design.md](references/role-permission-design.md)         | ロール設計時           |
| 多層制御   | [references/multi-layer-access-control.md](references/multi-layer-access-control.md) | 多層実装時             |
| 基礎ガイド | [references/Level1_basics.md](references/Level1_basics.md)                           | 初回実装時             |
| 応用ガイド | [references/Level3_advanced.md](references/Level3_advanced.md)                       | ポリシーエンジン構築時 |

### scripts/（決定論的処理）

| スクリプト                         | 機能                 |
| ---------------------------------- | -------------------- |
| `scripts/validate-rbac-config.mjs` | RBAC設定の検証       |
| `scripts/log_usage.mjs`            | スキル使用履歴の記録 |

### assets/（テンプレート）

| アセット                             | 用途                |
| ------------------------------------ | ------------------- |
| `assets/rbac-middleware-template.ts` | RBAC Middleware雛形 |

## 変更履歴

| Version | Date       | Changes                                    |
| ------- | ---------- | ------------------------------------------ |
| 3.0.0   | 2026-01-02 | 18-skills.md仕様完全準拠、ワークフロー改善 |
| 2.0.0   | 2025-12-31 | Task仕様ナビ追加                           |
| 1.0.0   | 2025-12-24 | 初版                                       |
