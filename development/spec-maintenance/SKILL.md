---
name: spec-maintenance
description: 仕様書（docs/spec）と受け入れ基準の更新手順を指示するスキル。画面/機能/権限に変更がある作業で使う。
---

# 仕様メンテナンス

## 目的
- 仕様と実装の乖離を防ぐ
- 画面/権限/合格基準を常に最新化する

## 更新対象
- `docs/spec/screens.md`（画面一覧）
- `docs/spec/user-app.md`（ユーザー仕様）
- `docs/spec/admin.md`（管理仕様）
- `docs/spec/acceptance.md`（合格基準）

## 手順
1. 変更した画面や導線を洗い出す
2. 画面一覧にURL/権限/目的を追記する
3. 影響する機能要件と権限要件を更新する
4. 合格基準に新しい達成条件を追記する
5. READMEのドキュメント一覧が最新か確認する
