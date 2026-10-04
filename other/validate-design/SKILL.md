---
name: validate-design
description: 設計書と実装コードの整合性（ドリフト）を検証する。「validate-design」「設計書と実装の整合性チェック」と指示されたとき。
argument-hint: '[all|<設計書パス>|<ソースパス>]'
context: fork
agent: design-validator-agent
---

引数: 設計書と実装コードの整合性を検証してください。

検証対象の決め方（詳細は agent 定義に従う）:

- **未指定・`all`**: 設計ハブ `docs/design-hub.md` から辿れる全設計書
- **設計書のパス**: その1件のみ
- **ソースのパス・領域名**: 対応する設計書を推定して突き合わせる

レポートの出力形式は `assets/report-template.md` を読み込み、そのテンプレートに従って作成してください。
