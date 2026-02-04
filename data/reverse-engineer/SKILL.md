---
name: reverse-engineer
description: 既存コードを分析して詳細設計書を自動生成
---

# リバースエンジニアリング・ワークフロー (v1.3)

既存のソースコードを分析し、詳細設計書を自動生成するワークフロー。
設計書のないプロジェクトの追加開発や、レガシーコード理解に活用する。

## 入力

$ARGUMENTS（対象モジュール/ディレクトリのパス）

## 出力言語

**設計書は必ず日本語で記述すること。**
コード内のシンボル名（struct, enum, fn等）は原文のまま、説明は日本語で記載。

## 前提条件

| 項目 | 要件 |
|------|------|
| Serena | プロジェクト設定済み（`serena_activate_project()`） |
| 対象コード | コンパイル/構文エラーなし |
| 権限 | `docs/designs/reverse/` への書き込み権限 |

---

## 全体フロー

| Phase | 名称 | 内容 |
|-------|------|------|
| 0 | スコープ確認 | 言語検出、対象ファイル一覧、ユーザー確認 |
| 1 | コード分析 | シンボル抽出、依存関係、テスト、コメント |
| 2 | 設計書生成 | テンプレートに従い設計書作成 |
| 3 | 品質検証 | 整合性・網羅性チェック |
| 3.5 | AIレビュー | `detailed-design-reviewer` skill（8点以上、オプション） |
| 3.8 | ユーザー承認 | 生成前の最終確認（`approval-gate` skill） |
| 4 | 出力 | ファイル生成 |

> **Phase規約**: `workflow-phase-convention` skill を参照

---

## Phase 0: スコープ確認

### 言語検出

| ファイル | 言語 |
|---------|------|
| `Cargo.toml` | Rust |
| `package.json` | JavaScript/TypeScript |
| `pyproject.toml` | Python |
| `go.mod` | Go |

### Serena ツール

```
serena_list_dir(relative_path="$TARGET_PATH", recursive=True, skip_ignored_files=True)
serena_find_file(file_mask="Cargo.toml", relative_path=".")
```

### ユーザー確認

対象パス、言語、ファイル数を提示し `1. 続行` / `2. 修正` / `3. 中断` を選択（番号選択）。

---

## Phase 1: コード分析

### 1.1 シンボル抽出

```
serena_get_symbols_overview(relative_path="src/xxx/mod.rs", depth=2)
serena_find_symbol(name_path_pattern="MainStruct", include_body=True)
```

### 1.2 依存関係解析

```
# Rust
serena_search_for_pattern(substring_pattern="^use\\s+", relative_path="src/xxx/")

# TypeScript
serena_search_for_pattern(substring_pattern="^import\\s+", relative_path="src/xxx/")
```

### 1.3 テストケース分析

```
serena_find_file(file_mask="*test*.rs", relative_path=".")
serena_get_symbols_overview(relative_path="tests/xxx_test.rs", depth=1)
```

### 1.4 コメント抽出

```
# Rust: ///
serena_search_for_pattern(substring_pattern="^\\s*///", relative_path="src/xxx/")

# Python: docstring
serena_search_for_pattern(substring_pattern='"""', relative_path="src/xxx/")
```

---

## Phase 2: 設計書生成

> **テンプレート**: `detailed-design-templates` skill の「リバースエンジニアリング設計書テンプレート」を使用

### 必須セクション

1. 概要（目的、スコープ）
2. モジュール設計（構成、依存関係図）
3. データ型定義（enum、struct、trait）
4. コアロジック（主要関数）
5. エラーハンドリング
6. テスト方針
7. 未解決事項・推測

---

## Phase 3: 品質検証

### 整合性チェック

| チェック項目 | 確認方法 |
|-------------|---------|
| 全公開struct/enum記載 | シンボル比較 |
| 全公開関数記載 | シンボル比較 |
| モジュール依存関係 | import解析 |
| エラー型記載 | Error enum検索 |

---

## Phase 3.5: AIレビュー（オプション）

```
task(subagent_type="detailed-design-reviewer", prompt="設計書をレビュー...")
```

| スコア | アクション |
|--------|----------|
| 8点以上 | Phase 3.8へ |
| 6-7点 | 修正して再レビュー（最大3回） |
| 5点以下 | Phase 1からやり直し |

> `--skip-review` フラグで省略可能

---

## Phase 3.8: ユーザー承認【必須】

> **共通仕様**: `approval-gate` skill を参照

生成結果サマリー（抽出シンボル数、未解決事項数）を表示し確認。

| 選択肢 | アクション |
|--------|----------|
| `1` | Phase 4へ |
| `2` | Phase 2に戻る |
| `3` | キャンセル |

> 番号を選択してください（1-3）:

---

## Phase 4: 出力

### 出力先

| 条件 | 出力先 |
|------|--------|
| 既存設計書なし | `docs/designs/reverse/{module-name}.md` |
| 既存設計書あり | `docs/designs/reverse/{module-name}_v{N}.md` |

---

## サーキットブレーカー

| 条件 | アクション |
|------|----------|
| 対象ファイル100件超 | サブモジュール単位での分割を提案 |
| 解析エラー | スキップして未解決事項に記録 |
| 非対応言語 | エラー終了 |
| レビュー3回失敗 | 警告マーク付与して続行 |

---

## エラーハンドリング

| Phase | エラー | 対処 |
|-------|--------|------|
| 0 | パス不存在 | 正しいパスを再指定 |
| 0 | 言語検出失敗 | 手動で言語指定 |
| 1 | LSP未起動 | `serena_activate_project()` 実行 |
| 2 | テンプレート適用エラー | Phase 1結果を確認 |
| 4 | 書き込み失敗 | 権限・容量確認 |

---

## 対応言語

| 言語 | サポート |
|------|:--------:|
| Rust | O |
| TypeScript | O |
| Python | O |
| Go | △ |
| Java | △ |

---

## 使用例

```bash
/reverse-engineer src/notification/
/reverse-engineer src/ --skip-review
```

---

## 制限事項

1. 設計意図の推測限界（「なぜそう実装したか」は不明）
2. 非公開シンボルは詳細度が低い
3. 動的言語の型推論は不完全な場合あり
4. 外部ライブラリの詳細は含まれない

---

## 参考

| スキル/ドキュメント | 用途 |
|-------------------|------|
| `detailed-design-templates` skill | 設計書テンプレート |
| `workflow-phase-convention` skill | Phase命名規約 |
| `approval-gate` skill | ユーザー承認ゲート |
| [詳細設計ワークフロー](./detailed-design-workflow.md) | 新規設計時 |

---

## 変更履歴

| バージョン | 変更内容 |
|-----------|---------|
| 1.3.0 | 出力言語セクション追加、日本語記述を明示化 |
| 1.2.0 | 前提条件追加、TypeScript/Python例追加 |
| 1.1.0 | Phase番号修正、`--skip-review`追加 |
| 1.0.0 | 初版作成 |
