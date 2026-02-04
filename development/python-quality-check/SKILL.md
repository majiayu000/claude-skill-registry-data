---
name: python-quality-check
description: PEP8、クリーンコード原則、Pythonのベストプラクティスに基づいてコード品質をチェック。Pythonプロジェクトでコード品質チェック、リント、フォーマットを依頼された時に使用。
---

# Python コード品質チェック

PEP8、クリーンコード原則、Pythonのベストプラクティスに基づいてコード品質をチェックし、改善を行います。
Ruff のみを使用し、isort・Black 相当の機能も Ruff で実行します。

## 実行手順

以下のコマンドを順番に実行してください：

### 1. Ruffによるリントチェックと自動修正（import整理含む）
```bash
uv run ruff check --fix .
```
- コードの潜在的な問題、未使用のimport、スタイル違反を検出
- import文の自動整理（isort相当、Iルール）
- 自動修正可能な問題は修正
- 手動対応が必要な問題があれば詳細を報告

### 2. Ruffによるコードフォーマット（Black相当）
```bash
uv run ruff format .
```
- PEP8準拠の一貫したコードスタイルを適用
- 行の長さ、空白、引用符などを自動修正
- Black互換のフォーマットを適用

## pyproject.toml 推奨設定

```toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # Pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]

[tool.ruff.lint.isort]
known-first-party = ["your_package_name"]
```

## 報告形式

各コマンドの実行結果を以下の形式で報告してください：

### 📋 コード品質チェック結果

**1. Ruff check (リント・import整理)**
- 状態: ✅ 完了 / ⚠️ 修正あり / ❌ 要対応
- 自動修正: （あれば列挙）
- 手動対応必要: （あれば詳細と対応方法を説明）

**2. Ruff format (フォーマット)**
- 状態: ✅ 完了 / ⚠️ 修正あり
- 修正ファイル: （あれば列挙）

### 総合評価
全てのチェックがパスした場合は「✅ コード品質チェック完了」、対応が必要な場合は具体的な改善提案を提示。

## エラーハンドリング

- ツールが見つからない場合: `uv add --dev ruff` の実行を提案
- 設定ファイルの問題: 上記の pyproject.toml 設定例を提示
- 構文エラーがある場合: リントツール実行前にPythonの構文エラーを報告
