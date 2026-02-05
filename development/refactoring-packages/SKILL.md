---
name: refactoring-packages
description: パッケージ/モジュール構造の分析とリファクタリング支援。循環依存の検出、責務分離の提案、移行計画の作成を行う。「パッケージ構造を見直したい」「モジュールの依存関係が複雑」「ファイル配置を整理したい」「循環依存を解消したい」といった構造改善リクエストで起動。
---

# Refactoring Packages

パッケージ/モジュール構造を分析し、改善提案と移行計画を作成する。

## ワークフロー

```
1. 現状分析 → 2. 問題特定 → 3. 改善提案 → 4. 移行計画
```

## 1. 現状分析

対象ディレクトリの構造を把握する：

```bash
# ディレクトリ構造
tree -d -L 3 <target>

# ファイル数/ディレクトリ
find <target> -type f | wc -l
```

確認ポイント：
- ディレクトリ深度
- ファイル数/ディレクトリ
- 命名規則の一貫性

## 2. 問題特定

[references/analysis-patterns.md](references/analysis-patterns.md)を参照し問題を検出。

**優先順位**（高→低）：
1. 循環依存（ビルド不可の原因）
2. 神モジュール（変更影響が大きい）
3. 散在機能（開発効率低下）
4. 過度なネスト（可読性低下）

## 3. 改善提案

問題ごとの解決策は[references/analysis-patterns.md](references/analysis-patterns.md)を参照。

## 4. 移行計画

段階的な移行計画を作成：

```markdown
### Phase 1: 準備
- [ ] テストカバレッジ確認
- [ ] 依存関係マップ作成

### Phase 2: 構造変更
- [ ] 新ディレクトリ作成
- [ ] ファイル移動
- [ ] インポートパス更新

### Phase 3: 検証
- [ ] テスト実行
- [ ] ビルド確認
```

## 具体例

### 入力
```
ユーザー: 「auth/モジュールが肥大化している」
```

### 分析
```
auth/
├── mod.rs (800行) ← 神モジュール検出
├── jwt.rs
├── oauth.rs
└── session.rs

問題: mod.rsに認証ロジック、ミドルウェア、エラー型が混在
```

### 出力
```markdown
# パッケージ構造分析レポート

## 検出された問題
1. **神モジュール**: auth/mod.rs (800行、3責務)

## 改善提案
### 提案1: 責務分離
- Before: auth/mod.rs に全ロジック
- After:
  - auth/core.rs (認証ロジック)
  - auth/middleware.rs (ミドルウェア)
  - auth/error.rs (エラー型)
- 理由: 単一責任の原則適用、変更影響範囲の限定

## 移行計画
### Phase 1: 準備
- [ ] 既存テストの確認
### Phase 2: 分割
- [ ] auth/core.rs 作成、ロジック移動
- [ ] auth/middleware.rs 作成
- [ ] auth/error.rs 作成
- [ ] mod.rs を再エクスポートのみに
### Phase 3: 検証
- [ ] cargo test
- [ ] cargo clippy
```
