---
name: adr-writer
description: 設計上の決定事項を ADR 形式で記録し、docs/adr 配下に出力する
metadata:
  short-description: ADR作成（出力先固定）
---

# adr-writer

この skill は、設計上の意思決定を ADR（Architecture Decision Record）として記録する。

## 出力先

- ADR は必ず `docs/adr/` 配下に出力する。
- 1つの意思決定につき 1ファイルとする。

## ファイル命名規則

- `{連番4桁}-{短い英語要約}.md`
  - 例: `0003-tts-engine-abstraction.md`
- 連番は既存の ADR を確認したうえで次の番号を使用する。

## 出力形式

以下の構成で Markdown ファイルを作成する。

### Title

- 決定内容を一文で表す

### Context

- 背景
- 課題
- 前提条件

### Decision

- 採用した案
- 採用理由

### Consequences

- 利点
- 欠点
- 今後発生しうる影響

### Alternatives

- 検討した他の案（簡潔でよい）

## ルール

- 事実と決定事項のみを書く。
- 実装詳細やコード断片は含めない。
- 既存 ADR と矛盾がある場合は明示する。
