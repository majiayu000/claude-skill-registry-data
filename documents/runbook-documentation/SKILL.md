---
name: runbook-documentation
description: |
  運用ランブックの作成・保守スキル。本番システムの障害対応、トラブルシューティング手順、
  リカバリーワークフロー、運用知識の共有を標準化し、信頼性の高いシステム運用を実現する。

  Anchors:
  • Site Reliability Engineering (Google) / 適用: ランブックパターン、ポストモーテム / 目的: 運用の卓越性と信頼性
  • The Practice of System and Network Administration (Limoncelli) / 適用: 手順書標準化 / 目的: 再現可能な運用
  • Incident Management for Operations (Mogull) / 適用: インシデント対応 / 目的: 効果的な危機対応

  Trigger:
  Use when creating runbooks, documenting incident procedures, standardizing operational workflows,
  building troubleshooting guides, establishing recovery procedures, improving on-call readiness.
  runbook, incident response, troubleshooting, recovery procedures, operational documentation, on-call playbook
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# runbook-documentation

## 概要

運用ランブックの作成・保守スキル。本番システムの障害対応、トラブルシューティング手順、
リカバリーワークフロー、運用知識の共有を標準化し、信頼性の高いシステム運用を実現する。

## ワークフロー

```
scope-definition → information-gathering → runbook-creation
                                                 ↓
                    maintenance ← validation
```

### Task 1: スコープ定義（scope-definition）

ランブックの対象範囲と優先度を明確にする。

**Task**: `agents/scope-definition.md` を参照

### Task 2: 情報収集（information-gathering）

ランブック作成に必要な運用知識を収集・整理する。

**Task**: `agents/information-gathering.md` を参照

### Task 3: ランブック作成（runbook-creation）

標準化されたフォーマットでランブックを作成する。

**Task**: `agents/runbook-creation.md` を参照

### Task 4: 検証（validation）

ランブックの実効性を確保する。

**Task**: `agents/validation.md` を参照

### Task 5: 保守（maintenance）

ランブックを最新状態に保ち継続的に改善する。

**Task**: `agents/maintenance.md` を参照

## Task仕様（ナビゲーション）

| Task                  | 責務           | 入力                      | 出力                   |
| --------------------- | -------------- | ------------------------- | ---------------------- |
| scope-definition      | スコープ定義   | システム仕様、要件        | スコープ定義書         |
| information-gathering | 情報収集       | インシデント履歴、SME知識 | 情報収集レポート       |
| runbook-creation      | ランブック作成 | 収集された情報            | ランブックドキュメント |
| validation            | 検証           | ランブックドラフト        | 検証レポート           |
| maintenance           | 保守・継続改善 | 既存ランブック、フィード  | 更新されたランブック   |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照
**注記**: 1 Task = 1 責務。複数責務を1ファイルに入れない。

## ベストプラクティス

### すべきこと

- 明確な目的と適用条件を記載（いつ使うべきかを即座に判断可能）
- 前提条件とアクセス権限を明記（実行前に準備すべきことが明確）
- 各ステップに期待される結果を記述（進行状況と成功判定が可能）
- ロールバック手順を含める（失敗時の安全な復旧パスを確保）
- エスカレーション基準を明示（判断に迷わない）
- 最終更新日と担当者を記録（鮮度と問い合わせ先が明確）
- コマンド例を実際に動作するもので記載（コピペで実行可能）
- 想定所要時間を記載（作業計画とエスカレーション判断に有用）
- アラートとメトリクスへのリンクを含める（状況把握が迅速）

### 避けるべきこと

- 曖昧な判断基準（「適切に」「必要に応じて」は判断不能）
- 暗黙の前提知識（初見の人が実行できない）
- 複数の目的を1つのランブック（使い分けが困難）
- 古い情報の放置（信頼性低下と誤操作リスク）
- 手順の欠落やスキップ（実行できない、途中で詰まる）
- エラーケースの未記載（予期しない状況で停止）
- 専門用語の羅列（理解の障壁）
- 「詳しくは○○さんに聞いて」（属人化の温床）

**詳細**: See [references/quality-criteria.md](references/quality-criteria.md)

## リソース参照

### references/（詳細知識）

**注記**: references/ は責務/ドメイン単位で分割し、1ファイル=1責務を基本とする。

| リソース             | パス                                                                       | 読込条件               |
| -------------------- | -------------------------------------------------------------------------- | ---------------------- |
| 基礎概念             | See [references/Level1_basics.md](references/Level1_basics.md)             | 初回利用時             |
| 構造パターン         | See [references/Level2_intermediate.md](references/Level2_intermediate.md) | Task 3開始時           |
| 検証手法             | See [references/Level3_advanced.md](references/Level3_advanced.md)         | Task 4開始時           |
| エキスパートパターン | See [references/Level4_expert.md](references/Level4_expert.md)             | Task 5または複雑要件時 |
| ランブックパターン集 | See [references/runbook-patterns.md](references/runbook-patterns.md)       | Task 3実行時           |
| 品質基準             | See [references/quality-criteria.md](references/quality-criteria.md)       | 検証・レビュー時       |

### scripts/（決定論的処理）

**注記**: scripts/ は責務単位で分割し、1スクリプト=1責務（処理/検証）を基本とする。

| スクリプト                       | 用途                       | 使用例                                                                   |
| -------------------------------- | -------------------------- | ------------------------------------------------------------------------ |
| `scripts/validate-runbook.mjs`   | ランブック構造の検証       | `node scripts/validate-runbook.mjs --file ./runbooks/db-failover.md`     |
| `scripts/check-completeness.mjs` | 必須セクションの完全性確認 | `node scripts/check-completeness.mjs --directory ./runbooks`             |
| `scripts/log_usage.mjs`          | フィードバック記録         | `node scripts/log_usage.mjs --result success --phase "runbook-creation"` |

### assets/（テンプレート）

**注記**: assets/ は用途/責務単位で分離し、1アセット=1用途を基本とする。

| テンプレート                            | 用途                         |
| --------------------------------------- | ---------------------------- |
| `assets/runbook-template.md`            | 基本ランブックテンプレート   |
| `assets/incident-response-template.md`  | インシデント対応ランブック   |
| `assets/troubleshooting-template.md`    | トラブルシューティングガイド |
| `assets/recovery-procedure-template.md` | リカバリー手順書             |
| `assets/checklist-template.md`          | オペレーションチェックリスト |

## 変更履歴

| Version | Date       | Changes                                                     |
| ------- | ---------- | ----------------------------------------------------------- |
| 2.0.0   | 2026-01-02 | 18-skills仕様完全準拠・agents/references/scripts/assets完備 |
| 1.0.0   | 2025-12-31 | 初回リリース                                                |
