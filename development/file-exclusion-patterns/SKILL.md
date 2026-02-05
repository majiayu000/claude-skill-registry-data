---
name: file-exclusion-patterns
description: |
  ファイル監視システムにおける効率的な除外パターン設計の専門知識。.gitignore互換のglob pattern、プラットフォーム固有の一時ファイル除外、パフォーマンス最適化のための早期除外戦略を提供。

  Anchors:
  • The Pragmatic Programmer / 適用: ファイル監視・パターン設計 / 目的: 実用的な除外戦略とglob構文の習得
  • Software Engineering at Google / 適用: パフォーマンス最適化・クロスプラットフォーム対応 / 目的: 早期除外戦略とOS間の統一設定
  • Refactoring / 適用: パターンの保守性 / 目的: 重複を排除し明確な意図を持つ設計

  Trigger:
  Use when designing file exclusion patterns, optimizing .gitignore files, improving file watching performance, or implementing cross-platform exclusion rules.
  Keywords: gitignore, glob pattern, file watching, chokidar, build optimization, node_modules, platform-specific, .DS_Store, Thumbs.db, performance tuning
version: 1.2.0
level: 1
last_updated: 2025-12-31
allowed-tools:
  - Bash
  - Edit
  - Glob
  - Grep
  - Read
  - Write
---

# ファイル除外パターン設計

## 概要

ファイル監視システムにおける効率的な除外パターン設計の専門知識を提供します。

.gitignore互換のglob pattern、プラットフォーム固有の一時ファイル除外、パフォーマンス最適化のための早期除外戦略により、ビルドシステムやファイル監視ツールの効率を大幅に改善できます。

詳細な手順や背景は `references/Level1_basics.md` と `references/Level2_intermediate.md` を参照してください。

## ワークフロー

### Phase 1: 要件分析とTask選択

**目的**: プロジェクト要件を分析し、適切なTaskを選択する

**アクション**:

1. プロジェクトタイプ、対象プラットフォーム、パフォーマンス要件を確認
2. 下記の「Task仕様ナビ」から実行すべきTaskを選択
3. `references/Level1_basics.md` で基礎知識を確認

**Task選択ガイド**:

- 新規プロジェクト → Pattern Designer
- 複数OS対応 → Platform Optimizer
- パフォーマンス問題 → Performance Tuner
- 検証が必要 → Pattern Validator

### Phase 2: Task実行

**目的**: 選択したTaskを実行し、除外パターンを設計・最適化する

**アクション**:

1. `agents/` の該当Task仕様書を参照
2. Task仕様に従って必要な入力を準備
3. Task実行（必要に応じて複数Taskを順次実行）
4. 各Taskの成果物を次のTaskへ引き継ぐ

**Task実行順序の例**:

```
Pattern Designer → Platform Optimizer → Performance Tuner → Pattern Validator
```

### Phase 3: 検証と記録

**目的**: 成果物の検証と実行記録の保存

**アクション**:

1. Pattern Validator で最終検証を実施
2. 生成されたパターンファイルをプロジェクトに適用
3. `scripts/log_usage.mjs` を実行して記録を残す

**検証コマンド**:

```bash
node .claude/skills/file-exclusion-patterns/scripts/log_usage.mjs \
  --result success \
  --phase "Phase 2" \
  --agent "pattern-designer"
```

## Task仕様ナビ

各Taskの詳細仕様は `agents/` ディレクトリに配置されています。実行直前に該当ファイルを読み込んでください。

### Pattern Designer

**ファイル**: `agents/pattern-designer.md`

**目的**: プロジェクト要件に基づいた除外パターンの設計

**入力**:

- プロジェクト情報（言語、パッケージマネージャ、ビルドツール等）
- カスタム要件（追加の除外パターン）

**出力**:

- .gitignore形式の除外パターンファイル
- 設計メモ（パターン選択の根拠）

**参照リソース**:

- `references/Level1_basics.md` - 基本パターン
- `references/standard-patterns.md` - プロジェクト別テンプレート
- `references/glob-pattern-guide.md` - glob構文リファレンス

**使用タイミング**:

- 新規プロジェクトで.gitignoreを作成する時
- 既存パターンを見直したい時
- プロジェクトタイプに応じた標準パターンが必要な時

### Platform Optimizer

**ファイル**: `agents/platform-optimizer.md`

**目的**: Windows/macOS/Linux対応の最適化

**入力**:

- ターゲットプラットフォーム（Windows, macOS, Linux）
- ベース除外パターン（Pattern Designerの出力）

**出力**:

- プラットフォーム最適化パターン
- プラットフォーム互換性レポート

**参照リソース**:

- `references/platform-specific-exclusions.md` - OS別パターン集
- `references/Level3_advanced.md` - クロスプラットフォーム戦略

**使用タイミング**:

- 複数OSで開発するプロジェクトの設定時
- OS固有の一時ファイルを除外したい時
- プラットフォーム間の互換性問題を解決したい時

### Performance Tuner

**ファイル**: `agents/performance-tuner.md`

**目的**: パフォーマンス最適化のためのパターン配置

**入力**:

- 除外パターンセット
- プロジェクト統計情報（ファイル数、ディレクトリ構造等）

**出力**:

- 最適化済み除外パターン（処理順序を最適化）
- パフォーマンス改善レポート

**参照リソース**:

- `references/Level2_intermediate.md` - 早期除外戦略
- `references/Level4_expert.md` - 大規模システム最適化

**使用タイミング**:

- ファイル監視が遅い時
- ビルド時間を短縮したい時
- 大規模プロジェクトでパフォーマンス問題が発生した時

### Pattern Validator

**ファイル**: `agents/pattern-validator.md`

**目的**: 除外パターンの検証と修正提案

**入力**:

- 検証対象パターン
- プロジェクトコンテキスト（任意）

**出力**:

- 検証レポート（構文チェック、機能チェック）
- 修正済みパターン（問題がある場合）

**参照リソース**:

- `references/glob-pattern-guide.md` - 正しいglob構文
- `references/Level3_advanced.md` - アンチパターン集

**使用タイミング**:

- パターン設計後の最終確認時
- 既存パターンの問題を診断したい時
- アンチパターンを検出したい時

## ベストプラクティス

### すべきこと

- **プロジェクト分析**: Pattern Designerでプロジェクトタイプに適したベースパターンを選択する
- **glob構文の確認**: `references/glob-pattern-guide.md` で正しい構文を参照する
- **OS対応**: Platform Optimizerで複数OSの一時ファイルを適切に除外する
- **パフォーマンス重視**: Performance Tunerで頻繁にマッチするパターンを上位に配置する
- **検証の実施**: Pattern Validatorで構文エラーやアンチパターンをチェックする
- **段階的実装**: Task仕様に従い、入力→処理→検証のフローを守る
- **記録の保存**: `scripts/log_usage.mjs` で実行結果を記録し、継続的改善に活用する

### 避けるべきこと

- **検証スキップ**: Pattern Validatorを使わずにパターンを本番適用することを避ける
- **アンチパターン**: `**/node_modules/*/` などの誤ったglob構文を使用しない
- **プラットフォーム無視**: OS固有の違いを考慮せず、すべての環境で同じパターンを使わない
- **順序の軽視**: パフォーマンスを無視した無秩序なパターン配置を避ける
- **過剰な否定パターン**: `!` による否定パターンを多用しすぎない（保守性低下）
- **知識の欠如**: globパターンの仕様を理解せずに見よう見まねでパターンを書かない
- **テスト不足**: 実際のプロジェクトで動作確認せずに複雑なパターンを導入しない

## リソース参照

### Task仕様書（agents/）

実行直前に読み込む、Taskの詳細仕様書：

```bash
# Pattern Designer - 基本パターン設計
cat .claude/skills/file-exclusion-patterns/agents/pattern-designer.md

# Platform Optimizer - プラットフォーム最適化
cat .claude/skills/file-exclusion-patterns/agents/platform-optimizer.md

# Performance Tuner - パフォーマンス最適化
cat .claude/skills/file-exclusion-patterns/agents/performance-tuner.md

# Pattern Validator - パターン検証
cat .claude/skills/file-exclusion-patterns/agents/pattern-validator.md
```

### 学習リソース（references/）

必要時に読み込む知識ベース：

```bash
# レベル別ガイド
cat .claude/skills/file-exclusion-patterns/references/Level1_basics.md
cat .claude/skills/file-exclusion-patterns/references/Level2_intermediate.md
cat .claude/skills/file-exclusion-patterns/references/Level3_advanced.md
cat .claude/skills/file-exclusion-patterns/references/Level4_expert.md

# 専門リソース
cat .claude/skills/file-exclusion-patterns/references/glob-pattern-guide.md
cat .claude/skills/file-exclusion-patterns/references/platform-specific-exclusions.md
cat .claude/skills/file-exclusion-patterns/references/standard-patterns.md
```

### スクリプト実行（scripts/）

決定論的な処理を確実に実行：

```bash
# スキル構造の検証
node .claude/skills/file-exclusion-patterns/scripts/validate-skill.mjs

# 使用記録とメトリクス更新
node .claude/skills/file-exclusion-patterns/scripts/log_usage.mjs \
  --result success \
  --phase "Phase 2" \
  --agent "pattern-designer" \
  --notes "Node.js monorepo pattern created"
```

### テンプレート・ツール（assets/）

出力で使用する素材：

```bash
# パターンビルダーテンプレート
cat .claude/skills/file-exclusion-patterns/assets/pattern-builder.ts
```

### よく使うコマンド

```bash
# gitignore パターンを検証
npx gitignore-parser .gitignore

# ファイル監視の除外設定をテスト
chokidar 'src/**/*' --ignore 'node_modules/**'

# git で除外されているか確認
git check-ignore -v path/to/file

# 既にgit追跡されているファイルをキャッシュから削除
git rm --cached path/to/file
```

## トラブルシューティング

### パターンが効かない

**症状**: .gitignoreに追加したのにファイルが除外されない

**原因と対処**:

1. 既にgit追跡されている → `git rm --cached <file>` でキャッシュクリア
2. glob構文が間違っている → Pattern Validatorで検証
3. 否定パターンの順序 → 除外パターンの後に `!` パターンを配置

### パフォーマンスが改善しない

**症状**: 除外パターンを追加したが監視が遅い

**原因と対処**:

1. パターンの順序が非効率 → Performance Tunerで最適化
2. 複雑すぎるパターン → シンプルなディレクトリ除外に変更
3. 除外漏れ → Pattern Designerで標準パターンを確認

### プラットフォーム間で動作が異なる

**症状**: WindowsとmacOSで除外結果が違う

**原因と対処**:

1. パスセパレータの問題 → `/` を使用（`\` は避ける）
2. 大文字小文字の扱い → Platform Optimizerで確認
3. OS固有ファイルの除外漏れ → `references/platform-specific-exclusions.md` を参照

## メトリクスとフィードバック

このスキルの使用状況とパフォーマンスは `EVALS.json` と `LOGS.md` で追跡されます。

**レベルアップ条件**:

- Level 1: 基本的な使用（1回以上、成功率50%以上）
- Level 2: プラットフォーム最適化の習得（5回以上、成功率70%以上）
- Level 3: パフォーマンスチューニングの習得（10回以上、成功率80%以上）
- Level 4: エキスパートレベルの運用（20回以上、成功率90%以上）

**フィードバックの記録**:

```bash
# 成功時
node scripts/log_usage.mjs --result success --phase "Phase 2" --agent "pattern-designer"

# 失敗時（改善のヒントを含める）
node scripts/log_usage.mjs --result failure --notes "glob syntax error detected"
```

## 変更履歴

| Version | Date       | Changes                                                                                                       |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------- |
| 1.2.0   | 2025-12-31 | 18-skills.md完全準拠: agents/追加、description更新、Task仕様ナビ刷新、EVALS.json/LOGS.md追加、references/補完 |
| 1.1.0   | 2025-12-31 | Task仕様ナビ追加・トリガー/アンカー定義・ベストプラクティス拡充                                               |
| 1.0.0   | 2025-12-24 | 初版リリース - 基本構造とリソース整備                                                                         |
