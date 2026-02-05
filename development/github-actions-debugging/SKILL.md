---
name: github-actions-debugging
description: |
  GitHub Actionsワークフロー実行時のデバッグとトラブルシューティング。

  Anchors:
  • Continuous Delivery (Jez Humble) / 適用: パイプライン失敗の診断 / 目的: フィードバックループ短縮
  • Site Reliability Engineering (Google) / 適用: ログベース障害分析 / 目的: 体系的エラー診断

  Trigger:
  Use when debugging failed GitHub Actions workflows, analyzing workflow logs, enabling debug logging, troubleshooting permission/secret/cache/timeout issues, or diagnosing runner environment problems.
  Keywords: github actions, workflow error, failed job, ACTIONS_STEP_DEBUG, ACTIONS_RUNNER_DEBUG, permission denied, cache miss, timeout, runner diagnostics
tags:
  - github-actions
  - ci-cd
  - debugging
  - troubleshooting
---

# GitHub Actions Debugging Skill

## 概要

GitHub Actionsワークフロー実行時のエラー診断、デバッグログ有効化、環境トラブルシューティングを体系的に実施します。

## ワークフロー

### Phase 1: エラー特定

**目的**: ワークフローログから失敗の根本原因を特定する

**Task**: `agents/error-identification.md`

**アクション**:

1. ワークフローログまたは実行IDを取得
2. `scripts/analyze-logs.mjs` でログを分析
3. `references/troubleshooting-guide.md` でエラーパターンをマッチング
4. エラー診断レポートを生成

**次のフェーズ**: エラーカテゴリに応じて Phase 2, 3, または 4 へ

### Phase 2: デバッグログ有効化

**目的**: 詳細なデバッグログを収集できる状態にする

**Task**: `agents/debug-enablement.md`

**アクション**:

1. エラー診断レポートからデバッグレベルを判断
2. `references/debug-logging.md` で設定方法を確認
3. リポジトリシークレット設定手順を生成
4. ワークフロー再実行とクリーンアップ手順を提供

**次のフェーズ**: 再実行後、Phase 1 に戻る

### Phase 3: コンテキスト検査

**目的**: GitHub Actionsの実行コンテキストから問題を特定する

**Task**: `agents/context-inspection.md`

**アクション**:

1. 必要なコンテキストオブジェクト（github、env、runner等）を決定
2. `references/diagnostic-commands.md` でコンテキスト検査コマンドを確認
3. コンテキストダンプ用のワークフロー修正案を生成
4. コンテキスト情報を分析してレポート作成

**次のフェーズ**: 環境問題が疑われる場合 Phase 4 へ

### Phase 4: 環境診断

**目的**: ランナー環境のリソースとツールを診断する

**Task**: `agents/environment-diagnosis.md`

**アクション**:

1. 診断対象（ディスク、メモリ、ツールバージョン等）を決定
2. `references/diagnostic-commands.md` で診断コマンドを確認
3. 環境診断用ワークフローステップを生成
4. 環境情報を分析して解決策を提供

**次のフェーズ**: 解決策実装後、Phase 1 で検証

## Task仕様（ナビゲーション）

各Taskは `agents/` ディレクトリに配置されています。実行直前に該当するTaskファイルを読み込んでください。

| Task名                 | ファイル                          | 入力                        | 出力                     |
| ---------------------- | --------------------------------- | --------------------------- | ------------------------ |
| **エラー特定**         | `agents/error-identification.md`  | ログファイルまたは実行ID    | エラー診断レポート       |
| **デバッグログ有効化** | `agents/debug-enablement.md`      | エラー診断レポート          | デバッグ有効化手順書     |
| **コンテキスト検査**   | `agents/context-inspection.md`    | エラー診断レポート          | コンテキスト分析レポート |
| **環境診断**           | `agents/environment-diagnosis.md` | エラー/コンテキストレポート | 環境診断レポート         |

## リソース参照

### references/（知識外部化）

| リソース               | パス                                                                       | 内容                                  |
| ---------------------- | -------------------------------------------------------------------------- | ------------------------------------- |
| デバッグログ           | [references/debug-logging.md](references/debug-logging.md)                 | ACTIONS_STEP_DEBUG/RUNNER_DEBUGの詳細 |
| 診断コマンド           | [references/diagnostic-commands.md](references/diagnostic-commands.md)     | コンテキスト検査・環境診断コマンド    |
| トラブルシューティング | [references/troubleshooting-guide.md](references/troubleshooting-guide.md) | 一般的なエラーパターンと解決策        |

### スクリプト（scripts/）

- **`scripts/analyze-logs.mjs`**: ワークフローログ分析スクリプト
  - 引数: `<log-file-path>`
  - 出力: エラーパターン、失敗ステップ、推奨アクション
  - 失敗時: ログファイルパスの確認、ファイル形式の検証
- **`scripts/log_usage.mjs`**: 使用記録・自動評価スクリプト
  - 引数: `--result <success|failure> [--phase <phase-name>] [--notes <notes>]`
  - 出力: LOGS.mdへの記録、EVALS.jsonの更新
- **`scripts/validate-skill.mjs`**: スキル構造検証スクリプト
  - 引数: なし
  - 出力: 構造検証結果、エラー一覧

### テンプレート（assets/）

- **`assets/debug-workflow.yaml`**: デバッグログ有効化ワークフローテンプレート

## ベストプラクティス

### すべきこと

- Phase 1（エラー特定）から開始し、体系的に診断を進める
- `scripts/analyze-logs.mjs` を活用してログ分析を効率化する
- デバッグログは段階的に有効化（STEP_DEBUG → RUNNER_DEBUG）
- コンテキスト検査では secrets コンテキストをダンプしない
- デバッグ完了後はシークレットを削除する

### 避けるべきこと

- ログの手動分析から始める（スクリプトを優先）
- すべてのデバッグログを一度に有効化する（段階的アプローチ）
- センシティブ情報を含むコンテキストをダンプする
- 診断コマンドでランナーに過負荷をかける
- 推測に基づいた解決策を実行する（references/を参照）

## クイックリファレンス

### よくあるエラーパターン

| エラー                 | 原因                  | 参照先                                   |
| ---------------------- | --------------------- | ---------------------------------------- |
| **Permission denied**  | GITHUB_TOKEN 権限不足 | `references/troubleshooting-guide.md` §1 |
| **Cache miss**         | キャッシュキー不一致  | `references/troubleshooting-guide.md` §2 |
| **Timeout**            | ジョブ実行時間超過    | `references/troubleshooting-guide.md` §3 |
| **Secret not found**   | シークレット未設定    | `references/troubleshooting-guide.md` §4 |
| **Runner out of disk** | ディスク容量不足      | `references/diagnostic-commands.md` §3   |

### デバッグログ有効化

| 方法                     | スコープ               | 用途                       |
| ------------------------ | ---------------------- | -------------------------- |
| **ACTIONS_STEP_DEBUG**   | リポジトリシークレット | ステップ実行の詳細ログ     |
| **ACTIONS_RUNNER_DEBUG** | リポジトリシークレット | ランナープロセスの診断ログ |

## コマンドリファレンス

### ログ分析

```bash
# ワークフローログをダウンロード
gh run view <run-id> --log > workflow.log

# ログを分析
node .claude/skills/github-actions-debugging/scripts/analyze-logs.mjs workflow.log
```

### デバッグログ有効化

```bash
# リポジトリシークレットを設定
gh secret set ACTIONS_STEP_DEBUG --body "true"
gh secret set ACTIONS_RUNNER_DEBUG --body "true"

# ワークフローを再実行
gh run rerun <run-id>

# クリーンアップ
gh secret remove ACTIONS_STEP_DEBUG
gh secret remove ACTIONS_RUNNER_DEBUG
```

### リソース参照

```bash
# デバッグログ詳細
cat .claude/skills/github-actions-debugging/references/debug-logging.md

# 診断コマンド
cat .claude/skills/github-actions-debugging/references/diagnostic-commands.md

# トラブルシューティング
cat .claude/skills/github-actions-debugging/references/troubleshooting-guide.md
```

## 検証と記録

### スキル構造検証

```bash
node .claude/skills/github-actions-debugging/scripts/validate-skill.mjs
```

### 使用記録

```bash
node .claude/skills/github-actions-debugging/scripts/log_usage.mjs \
  --result success \
  --phase "error-identification" \
  --notes "Permission error resolved"
```

## 変更履歴

| Version | Date       | Changes                                                        |
| ------- | ---------- | -------------------------------------------------------------- |
| 2.1.0   | 2026-01-02 | references/を整理、Level1-4削除、18-skills.md仕様準拠          |
| 2.0.0   | 2025-12-31 | 18-skills.md spec準拠、agents/追加、Progressive Disclosure適用 |
| 1.0.0   | 2025-12-24 | 初版リリース                                                   |
