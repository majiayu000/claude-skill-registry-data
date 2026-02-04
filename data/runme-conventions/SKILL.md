---
name: runme-conventions
description: |
  Runme.dev形式の実行可能マークダウン作成・編集用規約。
  使用タイミング:
  (1) マークダウンファイルに実行可能なコードブロックを追加（verify.md, README.mdなど）
  (2) Runme.devセル設定の追加・編集（name, cwd, excludeFromRunAllなど）
  (3) runme fmtでフォーマット適用
  (4) 既存Runmeファイルの修正・改善
allowed-tools: Read, Bash(runme fmt:*)
---

# Runme.dev規約

## クイックスタート

コードブロックにJSON形式でセル設定を追加:

````markdown
```bash {"name":"deploy","cwd":"../mcp-server"}
npm run deploy
```
````

## 主要オプション

| オプション | 説明 | 例 |
|-----------|------|-----|
| `name` | タスク名（`runme run <name>`で実行） | `{"name":"deploy"}` |
| `cwd` | 作業ディレクトリ（mdファイルからの相対パス） | `{"cwd":"../mcp-server"}` |
| `excludeFromRunAll` | `runme run --all`から除外 | `{"excludeFromRunAll":"true"}` |
| `ignore` | CLI・ノートブック変換から完全除外（runme listにも表示されない） | `{"ignore":"true"}` |

## フォーマット

コミット前に`runme fmt`を実行してVSCode拡張機能との差分を防止:

```bash
runme fmt -w --filename <target.md>
```

## 詳細リファレンス

- **全セルオプション**: [references/cell-options.md](references/cell-options.md)
- **ベストプラクティス**: [references/best-practices.md](references/best-practices.md)
- **公式ドキュメント**: https://docs.runme.dev/configuration/cell-level
