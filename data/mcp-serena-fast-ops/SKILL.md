---
name: mcp-serena-fast-ops
description: Fast code operations using Serena MCP (1-3s) for symbol search, memory read/write, and basic code editing in LoRAIro project
allowed-tools: mcp__serena__find_symbol, mcp__serena__get_symbols_overview, mcp__serena__search_for_pattern, mcp__serena__list_dir, mcp__serena__read_memory, mcp__serena__write_memory, mcp__serena__list_memories, mcp__serena__find_referencing_symbols, mcp__serena__replace_symbol_body, mcp__serena__insert_after_symbol, mcp__serena__insert_before_symbol
---

# Serena Fast Operations Skill

このSkillは、SerenaのMCPツールを使った高速コード操作（1-3秒）の最適な使い方を提供します。

## 使用タイミング

Claudeは以下の場合にこのSkillを自動的に使用すべきです：

- **シンボル検索**: クラス、関数、メソッドの定義を探す
- **ファイル構造把握**: プロジェクトのディレクトリ構造を理解する
- **短期メモリ操作**: 現在の開発進捗や一時的な判断を記録・参照する
- **基本コード編集**: シンボル単位での実装、挿入、置換
- **参照追跡**: シンボルの使用箇所を特定する

## Serena高速操作パターン

### 1. シンボル検索（1-3秒）

#### get_symbols_overview - ファイル構造の概要取得
```
用途: ファイル内のトップレベルシンボル（クラス、関数、変数）の一覧を取得
タイミング: 新しいファイルを初めて調査する時
パラメータ:
  - relative_path: 対象ファイルの相対パス
```

#### find_symbol - 名前パスでシンボルを検索
```
用途: 特定のクラス、メソッド、関数を検索
タイミング: シンボル名が分かっている時
パラメータ:
  - name_path: シンボルの名前パス (例: "ThumbnailWidget/handle_click")
  - relative_path: 検索範囲を絞る場合のパス（省略可）
  - include_body: コード本体を含めるか (True/False)
  - depth: 子シンボルの深さ (例: 1でメソッド一覧)
  - substring_matching: 部分一致検索を有効化
```

#### search_for_pattern - 正規表現パターン検索
```
用途: 特定のコードパターンや文字列を検索
タイミング: シンボル名が不明確で、パターンマッチングが必要な時
パラメータ:
  - substring_pattern: 正規表現パターン
  - relative_path: 検索範囲（ファイルまたはディレクトリ）
  - restrict_search_to_code_files: コードファイルのみに限定
  - paths_include_glob: 含めるファイルパターン
  - paths_exclude_glob: 除外するファイルパターン
```

### 2. Memory操作（短期・進捗記録）

#### list_memories - 利用可能なメモリ一覧
```
用途: プロジェクトに存在するメモリファイルを確認
タイミング: 関連するメモリを探す時、プロジェクト状況を把握する時
```

#### read_memory - 現在の進捗・状況確認
```
用途: プロジェクト固有の短期メモリを読み込む
タイミング: 実装前の状況確認、過去の判断を参照する時
使用例:
  - current-project-status: プロジェクト全体の状況
  - active-development-tasks: 現在の開発タスク
  - 実装記録: 具体的実装の詳細と根拠
```

#### write_memory - 開発進捗・一時的判断の記録
```
用途: 現在の実装進捗や一時的な判断を記録
タイミング: 実装中の進捗記録、次のステップのメモ、一時的な課題記録
記録内容:
  - 現在の実装状況と次のステップ
  - 進行中の開発判断
  - 一時的な課題と解決策
  - デバッグ情報と検証結果
```

### 3. コード編集（シンボル単位）

#### replace_symbol_body - シンボル本体の置換
```
用途: 関数、メソッド、クラス全体を書き換える
タイミング: 実装の大幅な変更、リファクタリング
パラメータ:
  - name_path: 対象シンボルの名前パス
  - relative_path: ファイルパス
  - body: 新しいシンボル本体
```

#### insert_after_symbol - シンボルの後に挿入
```
用途: 新しいメソッド、関数、クラスを追加
タイミング: 機能追加、ファイル末尾への追加
パラメータ:
  - name_path: 基準シンボルの名前パス
  - relative_path: ファイルパス
  - body: 挿入するコード
```

#### insert_before_symbol - シンボルの前に挿入
```
用途: import文の追加、前置き的なコードの挿入
タイミング: 依存関係追加、ファイル先頭への追加
パラメータ:
  - name_path: 基準シンボルの名前パス
  - relative_path: ファイルパス
  - body: 挿入するコード
```

### 4. 参照追跡

#### find_referencing_symbols - シンボルの参照箇所検索
```
用途: あるシンボルがどこで使われているかを特定
タイミング: リファクタリング影響確認、削除前の依存確認
パラメータ:
  - name_path: 対象シンボルの名前パス
  - relative_path: シンボルが定義されているファイル
```

## 効率的な使い方のガイドライン

### コード調査の推奨手順
1. **概要把握**: `get_symbols_overview` でファイル構造を理解
2. **詳細検索**: `find_symbol` で目的のシンボルを特定
3. **影響確認**: `find_referencing_symbols` で参照箇所を確認
4. **編集実行**: `replace_symbol_body` / `insert_*` で実装

### Memory-Firstアプローチ
1. **実装前**: `list_memories` → `read_memory` で現在状況確認
2. **実装中**: `write_memory` で進捗と判断を継続記録
3. **完了後**: 次のタスクのために `write_memory` で状況更新

### パフォーマンス最適化
- **Fast operations (1-3s)**: Serenaツールを優先使用
- **Full file read**: 最後の手段として使用、可能な限りシンボル単位で取得
- **Progressive disclosure**: 必要な情報のみを段階的に取得

## LoRAIro固有の注意点

### プロジェクト構造
- **ソースコード**: `src/lorairo/` 配下（メイン実装）
- **テスト**: `tests/` 配下
- **設定**: `config/lorairo.toml`
- **ローカルパッケージ**: `local_packages/genai-tag-db-tools`, `local_packages/image-annotator-lib`

### 重要なアーキテクチャパターン
- **Repository Pattern**: データベース操作は `src/lorairo/database/` のリポジトリ経由
- **Service Layer**: ビジネスロジックは `src/lorairo/services/` のサービス層
- **Direct Widget Communication**: GUI間通信は直接Signal/Slot接続

### Memory命名規則
- **current-project-status**: プロジェクト全体状況
- **active-development-tasks**: 現在の開発タスク
- **{feature}_implementation_{date}**: 具体的実装記録
- **archived_***: 完了タスクのアーカイブ

## Examples
詳細な使用例は [examples.md](./examples.md) を参照してください。

## Reference
Serenaツールの完全なAPIリファレンスは [reference.md](./reference.md) を参照してください。
