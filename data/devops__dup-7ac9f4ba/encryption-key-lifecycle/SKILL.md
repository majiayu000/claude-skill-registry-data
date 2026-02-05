---
name: encryption-key-lifecycle
description: |
  暗号化鍵のライフサイクル管理（生成、ローテーション、失効、バックアップ）のベストプラクティスを提供するスキル。

  Anchors:
  - NIST SP 800-57 / 適用: 鍵ライフサイクル全般 / 目的: 業界標準準拠
  - AWS KMS Best Practices / 適用: クラウド鍵管理 / 目的: クラウド実装パターン
  - Continuous Delivery (Jez Humble) / 適用: 自動化設計 / 目的: ローテーション自動化

  Trigger:
  Use when implementing key generation, rotation, revocation, backup strategies, or managing cryptographic key lifecycle.
  encryption key, key rotation, key lifecycle, key management, cryptographic keys, HSM, KMS
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Encryption Key Lifecycle

## 概要

暗号化鍵のライフサイクル管理を支援するスキル。鍵の生成から廃棄までの全フェーズにおけるセキュリティベストプラクティスを提供する。

## ワークフロー

### Phase 1: 鍵生成戦略

**目的**: 適切な暗号化鍵生成方法とパラメータを決定

**アクション**:
1. 用途に応じた鍵タイプを選択（対称/非対称）
2. 鍵長と暗号アルゴリズムを決定
3. 鍵生成環境のセキュリティ要件を確認
4. 初期鍵マテリアルの生成手順を策定

**Task**: `agents/key-generation-strategy.md` を参照

### Phase 2: ローテーションポリシー

**目的**: 鍵ローテーションの頻度と手順を策定

**アクション**:
1. ローテーション間隔を決定（リスク評価に基づく）
2. ローテーション手順を文書化
3. 旧鍵の移行期間を設定
4. 自動ローテーションの実装を検討

**Task**: `agents/rotation-policy.md` を参照

### Phase 3: 失効プロセス

**目的**: 鍵漏洩や廃棄時の失効手順を確立

**アクション**:
1. 失効トリガー条件を定義
2. 緊急失効手順を策定
3. 失効通知プロセスを確立
4. 影響範囲の特定と対応手順を文書化

**Task**: `agents/revocation-process.md` を参照

## Task仕様（ナビゲーション）

| Task | 起動タイミング | 入力 | 出力 |
|------|----------------|------|------|
| key-generation-strategy | 鍵生成設計時 | 暗号化要件 | 鍵生成戦略書 |
| rotation-policy | ローテーション設計時 | 鍵生成戦略書 | ローテーションポリシー |
| revocation-process | 失効設計時 | ローテーションポリシー | 失効手順書 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- 鍵マテリアルは暗号学的に安全な乱数生成器（CSPRNG）で生成
- 環境ごとに異なる鍵を使用（本番/ステージング/開発）
- 鍵のバックアップはオフライン環境で暗号化して保管
- 定期的なローテーションを自動化
- アクセスログを監査証跡として保持

### 避けるべきこと

- ソースコードに鍵をハードコーディング
- 鍵を平文で保存・転送
- ローテーション期間を過度に長く設定
- 単一の鍵を複数用途で共有
- 失効した鍵の再利用
- MD5/SHA1/DES等の非推奨アルゴリズムの使用

**詳細**: See [references/rotation-procedures.md](references/rotation-procedures.md)

## リソース参照

### agents/（Task仕様書）

| Task | パス | 用途 |
|------|------|------|
| 鍵生成戦略 | See [agents/key-generation-strategy.md](agents/key-generation-strategy.md) | アルゴリズム・鍵長選定 |
| ローテーション | See [agents/rotation-policy.md](agents/rotation-policy.md) | 定期更新設計 |
| 失効プロセス | See [agents/revocation-process.md](agents/revocation-process.md) | 緊急対応・廃棄 |

### references/（詳細知識）

| リソース | パス | 用途 |
|----------|------|------|
| ローテーション手順 | See [references/rotation-procedures.md](references/rotation-procedures.md) | ローテーション詳細 |

### scripts/（決定論的処理）

| スクリプト | 用途 | 使用例 |
|------------|------|--------|
| `generate-keys.mjs` | 鍵生成 | `node scripts/generate-keys.mjs --algorithm AES --size 256` |
| `log_usage.mjs` | 使用ログ記録 | `node scripts/log_usage.mjs --result success` |

### assets/（テンプレート）

| テンプレート | 用途 |
|--------------|------|
| `key-policy-template.md` | 鍵管理ポリシー文書テンプレート |

## 変更履歴

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-01-01 | 18-skills.md仕様完全準拠、agents追加、構造最適化 |
| 1.0.0 | 2025-12-24 | 初版作成 |
