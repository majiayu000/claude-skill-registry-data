---
name: parallel-jobs-gha
description: |
  GitHub Actionsの並列ジョブ実行とジョブ依存関係管理のスキル。needs構文による依存関係制御、outputs/artifacts/cacheを活用したデータ受け渡し、matrix戦略による並列度調整を提供する。

  Anchors:
  • The Pragmatic Programmer (Andrew Hunt, David Thomas) - CI/CDパイプラインの段階的改善による実行時間短縮とリソース効率化
  • GitHub Actions公式ドキュメント - needs構文、outputs、artifacts、cacheの正確な実装
  • Continuous Delivery (Jez Humble, David Farley) - フィードバックサイクル短縮とパイプライン最適化

  Trigger:
  Use when implementing parallel job execution in GitHub Actions, managing job dependencies with needs syntax, or optimizing workflow performance through parallelization.

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# GitHub Actions Parallel Jobs Skill

## 概要

GitHub Actionsのワークフローにおいて、needs構文による依存関係制御、outputs/artifacts/cacheを活用したジョブ間データ受け渡し、matrix戦略による並列度調整を実現するスキル。CI/CDパイプラインの実行時間短縮とリソース効率化を目的とする。

## ワークフロー

### Phase 1: 分析

1. 並列化の目的を明確化する（実行時間短縮/リソース効率化/早期失敗検出）
2. 現在のワークフロー構造を把握する
3. ジョブ間の依存関係を洗い出す
4. データ受け渡し要件を特定する（outputs/artifacts/cache）
5. Analysis Taskで分析レポートを作成する

### Phase 2: 実装

1. 分析レポートに基づきワークフロー設計を行う
2. needs構文でジョブ依存関係を定義する
3. データ受け渡しを実装する（outputs/artifacts/cache）
4. matrix戦略で並列度を調整する
5. Implementation Taskでワークフロー定義を生成する

### Phase 3: 検証

1. ワークフロー構文を検証する
2. ジョブ依存関係の循環参照を確認する
3. データ受け渡しの整合性を確認する
4. Validation Taskで検証レポートを作成する
5. 実行記録をLOGS.mdとEVALS.jsonに保存する

## Task仕様ナビゲーション

| Task               | ファイル                   | 役割                                 | 入力                                                     | 出力                                       |
| ------------------ | -------------------------- | ------------------------------------ | -------------------------------------------------------- | ------------------------------------------ |
| **Analysis**       | `agents/analysis.md`       | 並列化要件の分析と適用パターンの選定 | 現在のワークフロー定義、並列化の目的・要件               | 分析レポート                               |
| **Implementation** | `agents/implementation.md` | 並列ジョブ実行とジョブ依存関係の実装 | 分析レポート、既存ワークフロー定義（任意）               | 実装済みワークフロー定義、ジョブ依存関係図 |
| **Validation**     | `agents/validation.md`     | 実装されたワークフローの検証と記録   | 実装済みワークフロー定義、ジョブ依存関係図、分析レポート | 検証レポート、EVALS.json、LOGS.md          |

## ベストプラクティス

### すべきこと

- **段階的な並列化**: シーケンシャルなワークフローから徐々に並列化を進める
- **依存関係の最小化**: 不要なneedsを避け、真に依存するジョブのみを連鎖させる
- **データ受け渡しの使い分け**: 文字列はoutputs、ファイルはartifacts、依存関係はcacheを活用する
- **クリティカルパスの最適化**: ワークフロー全体の実行時間を決定する最長パスを短縮する
- **早期失敗の実現**: 高速で重要なチェック（lintなど）を先に実行し、失敗時は後続ジョブをスキップする
- **明確な命名規則**: ジョブ名、artifact名、output名を統一し、可読性を高める

### 避けるべきこと

- **過剰な並列化**: リソース制限を超える並列ジョブ実行（GitHub Actionsの同時実行制限に注意）
- **循環依存**: needsによる循環参照はエラーとなる
- **大きなoutputs**: outputsは文字列のみ対応、大きなデータはartifactsを使用する
- **不要なartifacts**: 一時ファイルや巨大なnode_modulesのアップロードは避ける（cacheを使用）
- **検証の省略**: ワークフロー構文やジョブ依存関係の検証を怠らない

## リソース参照

### references/（詳細知識）

| リソース       | パス                                                                       | 内容                                       |
| -------------- | -------------------------------------------------------------------------- | ------------------------------------------ |
| 基礎知識       | See [references/Level1_basics.md](references/Level1_basics.md)             | 基礎知識と適用タイミング                   |
| 中級           | See [references/Level2_intermediate.md](references/Level2_intermediate.md) | リソース/スクリプト/テンプレート活用       |
| 上級           | See [references/Level3_advanced.md](references/Level3_advanced.md)         | Progressive Disclosure設計とトークン最適化 |
| エキスパート   | See [references/Level4_expert.md](references/Level4_expert.md)             | フィードバックループと改善サイクル         |
| データ受け渡し | See [references/data-passing.md](references/data-passing.md)               | outputs/artifacts/cache活用パターン        |
| ジョブ依存関係 | See [references/job-dependencies.md](references/job-dependencies.md)       | needs構文と依存関係グラフ                  |

### scripts/（決定論的処理）

| スクリプト           | 用途               | 使用例                                                          |
| -------------------- | ------------------ | --------------------------------------------------------------- |
| `visualize-deps.mjs` | 依存関係可視化     | `node scripts/visualize-deps.mjs .github/workflows/ci.yml`      |
| `validate-skill.mjs` | スキル構造検証     | `node scripts/validate-skill.mjs`                               |
| `log_usage.mjs`      | フィードバック記録 | `node scripts/log_usage.mjs --result success --phase "Phase 3"` |

### assets/（テンプレート）

| テンプレート             | 用途                                                                                         |
| ------------------------ | -------------------------------------------------------------------------------------------- |
| `parallel-workflow.yaml` | 5つの実装例（基本CI/CD、マルチプラットフォーム、複雑グラフ、条件付き実行、失敗ハンドリング） |

## 主要概念

### 依存関係パターン

- **シーケンシャル**: A → B → C → D（直列実行）
- **ファンアウト**: A → (B, C, D)（分岐並列）
- **ファンイン**: (A, B, C) → D（集約）
- **ダイアモンド**: A → (B, C) → D（最も一般的なCI/CDパターン）

### データ受け渡し手法

- **Outputs**: 文字列データ（環境変数、設定値、バージョン情報など）
- **Artifacts**: ファイル（ビルド成果物、レポート、ログなど）
- **Cache**: 依存関係（node_modules、.cache、ビルドキャッシュなど）

### 条件付き実行

- **always()**: 前ジョブの結果に関わらず実行（レポート生成、クリーンアップ）
- **success()**: 前ジョブが成功した場合のみ実行（デプロイ、リリース）
- **failure()**: 前ジョブが失敗した場合のみ実行（エラー通知、ロールバック）

## トラブルシューティング

### よくあるエラーと解決方法

#### 1. 循環依存エラー

**エラー**: `Cycle detected in job dependencies`

**原因**: needsによる循環参照（A → B → C → A）

**解決方法**:

- `scripts/visualize-deps.mjs`で依存関係グラフを可視化
- 循環を構成するジョブの依存関係を見直す
- 必要に応じてジョブを分割または統合する

#### 2. Artifactサイズ制限エラー

**エラー**: `Artifact size exceeds maximum allowed size`

**原因**: Artifactの合計サイズが10GB（無料プラン）を超過

**解決方法**:

- 不要なファイルを除外（`.artifactignore`を使用）
- `node_modules`はcacheを使用し、artifactには含めない
- 大きなファイルは圧縮してからアップロード
- 保持期間を短縮（デフォルト90日→7日など）

#### 3. 同時実行制限エラー

**エラー**: ジョブがキューに長時間留まる

**原因**: GitHub Actionsの同時実行制限（無料プラン: 20ジョブ/リポジトリ）

**解決方法**:

- matrix戦略の並列度を調整（`max-parallel`を設定）
- 優先度の低いジョブは`concurrency`グループでシリアル化
- クリティカルパス以外のジョブを別ワークフローに分離

#### 4. Outputsが取得できない

**エラー**: `needs.job_name.outputs.output_name`が空

**原因**:

- outputs定義の構文エラー
- 前ジョブがスキップされた
- outputsに改行や特殊文字が含まれる

**解決方法**:

- outputs定義を確認（`outputs:`配下に正しく定義されているか）
- 前ジョブの実行ログで値が設定されているか確認
- 改行はJSON形式でエスケープ（`toJSON()`を使用）

#### 5. Cacheヒット率が低い

**症状**: キャッシュが頻繁にミスする

**原因**:

- キャッシュキーが不安定（日時やランダム値を含む）
- ファイルパスのパターンが広すぎる
- キャッシュサイズが10GBを超え、古いキャッシュが削除される

**解決方法**:

- キャッシュキーを安定化（`hashFiles('**/package-lock.json')`を使用）
- restore-keysでフォールバック戦略を設定
- 不要なファイルを除外してキャッシュサイズを削減
