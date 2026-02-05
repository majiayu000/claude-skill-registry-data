---
name: レビュー解決の証跡を CAS に保存してリンク
description: >
  修正パッチとテストログを CAS に格納し、タスクへ role 付きでリンクする。
  再現性と追跡可能性を担保するための Skill。
---

# 使い方
- 修正コミットの差分（patch）を CAS へ保存し、task に role:"patch" でリンク
- テスト実行ログも CAS へ保存し、task に role:"log" でリンク

## 手順
1. 差分パッチを CAS に保存（URI を得る）
2. `POST /tasks/{hid}/links` に `{ uri, role:"patch" }` で登録
3. テストログも CAS に保存し、`role:"log"` で登録

## 例
- `examples/review_links.http`
