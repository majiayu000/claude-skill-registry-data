---
name: absolute-path-checker
description: Verify no absolute paths exist in implementation code when discussing tests, refactoring, portability, or directory hierarchy
allowed-tools: [Grep, Read, Edit, Bash]
---

ポータビリティ確保のため、実装コード内の絶対パス（`/Users/`, `/home/`, `~`）を検出し相対パスに変換する。

## 検索

```bash
grep -r "/Users/" --include="*.ts" --include="*.js" .
grep -r "/home/" --include="*.ts" --include="*.js" .
```

## 判断

| 検出箇所 | 対応 |
|---------|------|
| 実装コード内リテラル | 相対パスに変換（必須） |
| テスト結果・ログ | 許容（テスト期待値には含めない） |
| 設定デフォルト値 | 環境変数または相対パスに置換 |
| ドキュメント・コメント | 許容 |

## 変換の優先順位

1. 既存変数（`baseDir`, `Deno.cwd()` 等）を使う
2. `import.meta.url` から算出する（Deno/ESM）
3. 相対パスリテラル（`./data/file.txt`）にする

パス結合は `join()` / `resolve()` を使い、文字列連結は避ける。`Deno.env.get("HOME")` 等の環境変数経由は許容。修正後はテスト実行で確認する。
