---
name: Full Scan
description: Apply the same operation to all files matching a glob pattern. Use this skill whenever you need to process multiple files systematically, such as fixing guideline violations, unifying code style, or fixing type errors. Always use this skill when working with multiple files that match a pattern.
---

# Full Scan

## Instruction

ユーザーは例えば以下のような形式で依頼します：

```
<パターン>に対して<処理>を適用してください
```

例：
- "packages/**/*.tsxに対してガイドライン違反を修正してください"
- "src/**/*.ts"にマッチするファイル全てについて、フォーマットを修正して"

### 1. 既存セッションの確認

まず、`full_scan_progress.json`が存在するかチェックします。

```bash
python3 .claude/skills/full_scan/full_scan.py info
```

- **ファイルが存在し、同じ目的のセッションの場合**:
  - 途中から再開します（ステップ3へ）

- **ファイルが存在するが、異なる目的の場合**:
  - ユーザーに確認します：
    - 既存のセッションを継続するか
    - 新しいセッションを開始するか（既存データは削除されます）

- **ファイルが存在しない場合**:
  - 新しいセッションを開始します（ステップ2へ）

### 2. 新規セッションの初期化

```bash
# セッションを初期化
python3 .claude/skills/full_scan/full_scan.py init "<処理の目的>"

# パターンを追加（複数可）
python3 .claude/skills/full_scan/full_scan.py add "<glob_pattern>"
python3 .claude/skills/full_scan/full_scan.py add "<glob_pattern2>"

# 状態確認
python3 .claude/skills/full_scan/full_scan.py info
```

### 3. ファイルの処理ループ

次の5件のファイルを取得し、処理を実行します：

```bash
python3 .claude/skills/full_scan/full_scan.py next
```

各ファイルに対して：

1. ファイルの内容を確認
2. 指定された処理を実行（例：ガイドライン違反の修正）
3. 処理が完了したファイルを記録

```bash
# 処理完了をマーク（複数ファイルを一度に指定可能）
python3 .claude/skills/full_scan/full_scan.py complete path/to/file1.tsx path/to/file2.tsx
```

### 4. 進捗確認と繰り返し

```bash
# 進捗確認
python3 .claude/skills/full_scan/full_scan.py stats
```

未処理のファイルが残っている場合は、ステップ3に戻ります。

### 5. 完了

全てのファイルの処理が完了したら、ユーザーに報告します。

## コマンドリファレンス

### `init <purpose>`
新しいスキャンセッションを初期化します（既存データは削除されます）。

```bash
python3 .claude/skills/full_scan/full_scan.py init "TypeScriptファイルのガイドライン違反を修正"
```

### `add <pattern> [--purpose|-p <purpose>]`
globパターンにマッチするファイルを追加します。

```bash
python3 .claude/skills/full_scan/full_scan.py add "packages/**/*.tsx"
python3 .claude/skills/full_scan/full_scan.py add "src/**/*.ts" --purpose "型エラーの修正"
```

### `next`
未処理のファイルを5件返します。

```bash
python3 .claude/skills/full_scan/full_scan.py next
```

出力例：
```
packages/web/src/App.tsx
packages/web/src/NoteList.tsx
packages/web/src/NoteItem.tsx
```

### `complete <path> [<path2> ...]`
指定されたパスを処理済みとしてマークします。

```bash
python3 .claude/skills/full_scan/full_scan.py complete packages/web/src/App.tsx packages/web/src/NoteList.tsx
```

### `info`
現在のスキャンセッションの情報を表示します。

```bash
python3 .claude/skills/full_scan/full_scan.py info
```

出力例：
```
Purpose: TypeScriptファイルのガイドライン違反を修正
Patterns: packages/**/*.tsx, packages/**/*.ts
Total files: 20
Completed: 5
Pending: 15
Progress: 25.0%
```

### `stats`
進捗統計を表示します。

```bash
python3 .claude/skills/full_scan/full_scan.py stats
```

## データ構造

`full_scan_progress.json` の構造：

```json
{
  "purpose": "TypeScriptファイルのガイドライン違反を修正",
  "patterns": ["packages/**/*.tsx", "packages/**/*.ts"],
  "files": {
    "packages/web/src/App.tsx": true,
    "packages/web/src/NoteList.tsx": false,
    "packages/web/src/NoteItem.tsx": false
  }
}
```

- `purpose`: スキャンセッションの目的
- `patterns`: 検索に使用したglobパターンのリスト
- `files`: ファイルパスと処理状態（`true`: 処理済み、`false`: 未処理）
