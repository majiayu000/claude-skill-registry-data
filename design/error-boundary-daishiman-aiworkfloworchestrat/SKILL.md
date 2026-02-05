---
name: error-boundary
description: |
  ReactのError Boundary実装とエラーハンドリング戦略を専門とするスキル。
  堅牢なエラー処理とユーザーフレンドリーなフォールバックUIを実現する。

  Anchors:
  • The Pragmatic Programmer / 適用: エラー処理の実践原則 / 目的: 品質維持と堅牢性向上
  • React Error Boundary / 適用: クラッシュ回復UI実装 / 目的: 予期しない障害対応

  Trigger:
  Use when implementing error boundaries, creating crash recovery UI, designing async error handling, or setting up error monitoring.
  error boundary, componentDidCatch, getDerivedStateFromError, fallback UI, error reporting
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Error Boundary

## 概要

Error Boundaryを使用してReactアプリケーションの予期しないエラーをキャッチし、ユーザーフレンドリーなフォールバックUIで対応する実装スキル。

## ワークフロー

### Phase 1: 目的と前提の整理

**目的**: エラーハンドリング戦略を定義する

**アクション**:

1. `references/error-boundary-basics.md` でError Boundaryの基本パターンを確認
2. 対象のアプリケーション構造に応じたエラー処理の方針を決定
3. 使用する参照リソース・テンプレート・スクリプトを特定

### Phase 2: スキル適用

**目的**: Error Boundaryとフォールバック機構を実装する

**アクション**:

1. `references/recovery-strategies.md` で回復戦略を確認
2. `assets/error-boundary-template.md` でコンポーネント実装例を参考にする
3. `references/fallback-ui-patterns.md` でUIパターンを選択して実装
4. `scripts/analyze-error-handling.mjs` でエラーハンドリング戦略を検証

### Phase 3: 検証と記録

**目的**: 実装の品質確認とフィードバック記録

**アクション**:

1. 実装したError Boundaryが各エラーケースを正しくキャッチするか確認
2. フォールバックUIがユーザーにとって適切な情報を提供しているか確認
3. `scripts/log_usage.mjs` で実行結果と改善点を記録

## Task仕様ナビ

複雑なエラーハンドリング実装では、以下のTaskを使用して処理を分離し、メインコンテキストを汚さずに完了させる。

| タスク                   | Task仕様                                  | 説明                                                 | 入力                                 | 出力                           | 関連リソース                                                               |
| ------------------------ | ----------------------------------------- | ---------------------------------------------------- | ------------------------------------ | ------------------------------ | -------------------------------------------------------------------------- |
| **Error Boundary実装**   | `agents/error-boundary-implementation.md` | クラッシュ時にエラーをキャッチするコンポーネント実装 | コンポーネント構成、エラー種別       | Error Boundaryコンポーネント   | `assets/error-boundary-template.md`, `references/error-boundary-basics.md` |
| **フォールバックUI設計** | `agents/fallback-ui-design.md`            | エラー時に表示するUIの実装                           | エラーメッセージ仕様、ユーザーUX要件 | フォールバックUIコンポーネント | `references/fallback-ui-patterns.md`, `assets/error-fallback-template.md`  |
| **エラー監視設定**       | `agents/error-monitoring-setup.md`        | エラーログ・レポート機構の実装                       | アナリティクス要件、通知対象         | エラーレポート機構             | `references/error-reporting.md`                                            |

**Task使用のタイミング**:

- Phase 2でError Boundary実装とフォールバックUI設計を並行して進める場合、各Taskを別窓で実行
- エラー監視設定は実装完了後、Phase 3の一環として実行

## ベストプラクティス

### すべきこと

- エラーバウンダリーを適切な階層に配置する（ページ単位、セクション単位で検討）
- フォールバックUIで「何が起きたか」と「ユーザーが取るべき行動」を明確に伝える
- エラー情報をログ・監視システムに送信して本番環境の問題を早期発見する
- 非同期エラー（Promise, async/await）も含めた包括的なエラーハンドリング設計を行う
- 開発環境ではエラースタックトレースをエラーUIに表示して調査を容易にする

### 避けるべきこと

- Error Boundaryでサイレントに全てのエラーをキャッチして無視する（ログ記録なし）
- 技術的なエラーメッセージをユーザーに直接表示する
- Error Boundaryのコンポーネント数が多すぎて管理が煩雑になる
- エラーからの回復機構（リトライ、状態リセット）なしにフォールバックUIのみ表示する

## リソース/スクリプト参照

### 参考資料（references/）

| リソース                   | 用途                                   |
| -------------------------- | -------------------------------------- |
| `error-boundary-basics.md` | Error Boundaryの基本実装パターン       |
| `recovery-strategies.md`   | エラー回復戦略、リトライロジック       |
| `fallback-ui-patterns.md`  | ユーザーフレンドリーなエラーUIパターン |
| `error-reporting.md`       | エラーログ・監視・レポート機構         |

### テンプレート（assets/）

- **error-boundary-template.md**: Error Boundaryコンポーネントの実装テンプレート
- **error-fallback-template.md**: フォールバックUIコンポーネントの実装テンプレート

### スクリプト（scripts/）

| スクリプト                   | 用途                   | 使用例                                                          |
| ---------------------------- | ---------------------- | --------------------------------------------------------------- |
| `analyze-error-handling.mjs` | エラーハンドリング検証 | `node scripts/analyze-error-handling.mjs --help`                |
| `log_usage.mjs`              | フィードバック記録     | `node scripts/log_usage.mjs --result success --phase "Phase 3"` |

## 変更履歴

| Version | Date       | Changes                                |
| ------- | ---------- | -------------------------------------- |
| 3.0.0   | 2026-01-01 | 18-skills.md仕様完全準拠、Level1-4削除 |
| 2.0.0   | 2025-12-31 | Task仕様ナビ追加、Anchors・Trigger統合 |
| 1.0.0   | 2025-12-24 | 初期版作成                             |
