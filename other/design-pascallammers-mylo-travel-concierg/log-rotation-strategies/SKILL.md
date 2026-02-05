---
name: log-rotation-strategies
description: |
  Node.jsアプリケーションのログローテーション戦略設計・実装スキル。PM2、logrotate、Winston、集中ログシステムを活用した効率的ログ管理を提供。

  Anchors:
  • 『Site Reliability Engineering』(Google) / 適用: ログ管理SLO / 目的: 運用卓越性
  • 『Systems Performance』(Brendan Gregg) / 適用: ディスクUSEメソッド / 目的: キャパシティプランニング
  • PM2-logrotate Module / 適用: サイズ/時間ベースローテーション / 目的: 自動ログ管理

  Trigger:
  Use when configuring log rotation, optimizing disk capacity for logs, designing log retention policies,
  or integrating with centralized logging systems (ELK, Datadog, CloudWatch, Loki).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Log Rotation Strategies

> **相対パス**: `SKILL.md`
> **読込条件**: スキル使用時（自動）

---

## 概要

Node.js アプリケーションのログローテーション戦略を設計・実装するスキル。

**対象領域**:

- PM2 logrotate によるプロセスマネージャー統合
- Winston DailyRotateFile によるアプリケーションレベル制御
- logrotate (Linux) によるシステムレベル管理
- 集中ログシステム（ELK/Datadog/CloudWatch/Loki）への統合

---

## ワークフロー

### Phase 1: 要件分析

**Task**: `agents/analyze-requirements.md`

| 入力                               | 出力             |
| ---------------------------------- | ---------------- |
| アプリケーション情報、ビジネス要件 | 要件分析レポート |

**参照**: `references/basics.md`

### Phase 2: 戦略設計

**Task**: `agents/design-strategy.md`

| 入力             | 出力       |
| ---------------- | ---------- |
| 要件分析レポート | 戦略設計書 |

**参照**: `references/rotation-patterns.md`, `references/log-aggregation.md`

### Phase 3: 実装

**Task**: `agents/implement-rotation.md`

| 入力       | 出力             |
| ---------- | ---------------- |
| 戦略設計書 | 実装完了レポート |

**参照**: `references/pm2-logrotate-guide.md`, `assets/winston-rotation.template.ts`

### Phase 4: 検証

**Task**: `agents/validate-setup.md`

| 入力             | 出力             |
| ---------------- | ---------------- |
| 実装完了レポート | 検証完了レポート |

**参照**: `scripts/analyze-log-usage.mjs`

---

## ベストプラクティス

| すべきこと                                | 避けるべきこと             |
| ----------------------------------------- | -------------------------- |
| ログ生成量を事前に分析                    | 無制限ログ出力             |
| サイズ/時間/ハイブリッド方式を適切に選択  | ローテーション世代数未指定 |
| ecosystem.config.js に pm2-logrotate 統合 | ログフォーマット未標準化   |
| compress: true でディスク使用量削減       | 集約前の重要ログ削除       |
| 定期的なログディレクトリ監視              | 検証なしの本番デプロイ     |

---

## Task ナビゲーション

| Task                      | 目的                               | 参照リソース             |
| ------------------------- | ---------------------------------- | ------------------------ |
| `analyze-requirements.md` | ログ生成パターンの定量分析         | `basics.md`              |
| `design-strategy.md`      | ローテーション方式・パラメータ決定 | `rotation-patterns.md`   |
| `implement-rotation.md`   | 設定ファイル作成・適用             | `pm2-logrotate-guide.md` |
| `validate-setup.md`       | 動作検証・本番運用可否判断         | `scripts/`               |

---

## リソース参照

### References

| ファイル                 | 内容                                   | 読込条件       |
| ------------------------ | -------------------------------------- | -------------- |
| `basics.md`              | ログローテーション基礎概念・用語       | 初回使用時     |
| `rotation-patterns.md`   | サイズ/時間/ハイブリッド方式の選択基準 | 戦略設計時     |
| `pm2-logrotate-guide.md` | PM2 logrotate 設定詳細ガイド           | PM2 使用時     |
| `log-aggregation.md`     | 集中ログシステム選定・統合ガイド       | スケール検討時 |

### Assets

| ファイル                       | 内容                                     |
| ------------------------------ | ---------------------------------------- |
| `winston-rotation.template.ts` | Winston DailyRotateFile 設定テンプレート |

### Scripts

| スクリプト              | 用途                     |
| ----------------------- | ------------------------ |
| `analyze-log-usage.mjs` | ログ使用量分析・容量予測 |
| `log_usage.mjs`         | スキル使用記録・自動評価 |

---

## 関連スキル

- `logging-observability` - ログ観測可能性とモニタリング
- `disk-management` - ディスク容量管理
- `pm2-configuration` - PM2 設定全般
