---
name: file-watcher-security
description: |
  ファイル監視システムのセキュリティ対策を実装するスキル。パストラバーサル・シンボリックリンク攻撃の防止、最小権限の原則に基づく権限管理、多層防御アーキテクチャを設計・実装。

  Anchors:
  • Threat Modeling（Adam Shostack） / 適用: STRIDEモデル / 目的: 脅威の体系的分類
  • Web Application Security（Andrew Hoffman） / 適用: 入力検証 / 目的: パストラバーサル対策
  • OWASP Cheat Sheet / 適用: 防御パターン / 目的: 実装レベルのセキュリティ

  Trigger:
  Use when implementing file watcher security, preventing path traversal attacks, detecting symbolic link attacks, designing access control, or conducting security audits.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Task
---

# ファイル監視システムのセキュリティ設計

## 概要

ファイル監視システムのセキュリティ対策を実装するスキル。パストラバーサル攻撃・シンボリックリンク攻撃を防止し、最小権限の原則とDefense in Depthに基づく多層防御アーキテクチャを設計・実装する。

## ワークフロー

### Phase 1: 脅威分析

**目的**: ファイル監視システムの脅威を特定し、防御設計を策定

**アクション**:

1. [references/basics.md](references/basics.md) で脅威の基本概念を確認
2. STRIDEモデルで脅威を体系的に分類
3. パストラバーサル・シンボリックリンク攻撃シナリオを分析
4. 多層防御アーキテクチャを設計

**Task**: [agents/threat-analysis.md](agents/threat-analysis.md) を参照

### Phase 2: セキュリティ実装

**目的**: 脅威モデルに基づく防御機能の実装

**アクション**:

1. [references/patterns.md](references/patterns.md) で実装パターンを確認
2. パス検証・シンボリックリンク検出ロジックを実装
3. [assets/secure-watcher.ts](assets/secure-watcher.ts) をカスタマイズ
4. 権限管理設定を実装

**Task**: [agents/security-implementation.md](agents/security-implementation.md) を参照

### Phase 3: セキュリティ監査

**目的**: 実装のセキュリティ検証

**アクション**:

1. `scripts/validate-security.mjs --all` でセキュリティ検証
2. `scripts/security-audit.sh` で監査を実行
3. テストケースで脆弱性をチェック
4. `scripts/log_usage.mjs --result success` で記録

## Task仕様ナビ

| Task                                                                   | 用途             | 入力         | 出力                   |
| ---------------------------------------------------------------------- | ---------------- | ------------ | ---------------------- |
| [agents/threat-analysis.md](agents/threat-analysis.md)                 | 脅威分析         | システム要件 | 脅威モデル・防御設計書 |
| [agents/security-implementation.md](agents/security-implementation.md) | セキュリティ実装 | 脅威モデル   | セキュアコード・設定   |

## ベストプラクティス

### すべきこと

- パスを処理前に必ず正規化・検証する（許可リスト方式）
- シンボリックリンクはデフォルトで監視対象外とする
- 最小権限の原則を適用し、監視プロセスの権限を制限
- Defense in Depth設計で複数の防御層を配置
- Fail-Safeデフォルト（エラー時は拒否）を適用
- セキュリティイベントを監査ログに記録

### 避けるべきこと

- ユーザー入力をパス指定に直接使用
- シンボリックリンクを透過的にフォロー
- 広い権限でプロセスを実行
- 単層防御に依存
- 拒否リスト方式（許可リスト方式を使う）

## リソース参照

### references/（詳細知識）

| リソース     | パス                                                     | 内容                       |
| ------------ | -------------------------------------------------------- | -------------------------- |
| 基本概念     | [references/basics.md](references/basics.md)             | 脅威・セキュリティ原則     |
| 実装パターン | [references/patterns.md](references/patterns.md)         | パス検証・リンク検出       |
| 脅威モデル   | [references/threat-model.md](references/threat-model.md) | STRIDEモデル・攻撃シナリオ |

### assets/（テンプレート）

| テンプレート      | 用途                           |
| ----------------- | ------------------------------ |
| secure-watcher.ts | セキュアな監視実装テンプレート |

### scripts/（検証・監査）

| スクリプト            | 用途             | 使用例                                        |
| --------------------- | ---------------- | --------------------------------------------- |
| validate-security.mjs | セキュリティ検証 | `node scripts/validate-security.mjs --all`    |
| security-audit.sh     | セキュリティ監査 | `./scripts/security-audit.sh`                 |
| log_usage.mjs         | 利用記録         | `node scripts/log_usage.mjs --result success` |

## 変更履歴

| Version | Date       | Changes                                                           |
| ------- | ---------- | ----------------------------------------------------------------- |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様に完全準拠。agents/を2つに統合、references/を刷新 |
| 1.1.0   | 2025-12-31 | frontmatter改訂、構成再編                                         |
| 1.0.0   | 2025-12-24 | 初版作成                                                          |
