---
name: bugfix-format
description: バグ修正ドキュメントのフォルダ構造と形式。/fixコマンドが参照する。
---

# バグ修正ドキュメント

## 保存場所
`openspec/bugs/fixed/`

## ファイル名
`YYYY-MM-DD-[バグ名].md`（例: `2025-01-10-api-timeout.md`）

## テンプレート

```markdown
# [バグ名]

作成日: YYYY-MM-DD
ブランチ: fix/[ブランチ名]

## バグの概要
[ユーザー入力内容]

## 類似例
- 既知/新規: [既知 or 新規]
- 参考: [ファイル名 or なし]

## 根本原因
[技術的な原因]

## 修正内容
[修正方法]

## 変更ファイル
- path/to/file

## テスト結果
[結果]
```
