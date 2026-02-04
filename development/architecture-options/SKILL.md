---
name: architecture-options
description: 設計案を複数提示し、比較可能な形で整理する
metadata:
  short-description: 設計案の比較
---

# architecture-options

この skill は、設計案を比較検討できる形で提示する。

## 出力ルール

- 設計案は 2〜4 個に限定する。
- すべての案を同じ評価軸で記載する。
- ファイルの編集や追加、削除などは行わない。

## 各案に含める内容

- 概要（1〜2行）
- Pros（利点）
- Cons（欠点・リスク）
- 影響範囲
  - contracts
  - api
  - bot
  - db
  - docs

## 禁止事項

- 単一案のみの提示
- 結論の押し付け
