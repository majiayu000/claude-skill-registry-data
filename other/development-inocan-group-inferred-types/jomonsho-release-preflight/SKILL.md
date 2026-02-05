---
name: jomonsho-release-preflight
description: Jomonsho のリリース前チェックリストを実行する。
metadata:
  short-description: リリース前チェック (lint/typecheck/tests/Playwright)。
---

# Jomonsho Release Preflight（日本語）

チェック方針（スピードと品質の両立）:
  - 軽微な変更（UI文言・軽いリファクタ）: 1) lint 2) typecheck
  - 中規模変更（ロジック/Hook/サービス周辺）: 1) lint 2) typecheck 3) Jest
  - 重要変更（同期/ホスト操作/観戦/Presence/リセット/Safe Update/状態機械）:
    1) lint 2) typecheck 3) Jest 4) 対象E2Eを2回連続

チェックリスト（ユーザーの指示がない限りこの順番で実行）:

1) Lint / Typecheck:
   - npm run lint
   - npm run typecheck

2) Jest（単体テスト）:
   - npm test

3) Playwright E2E（対象を絞る / workers=1 / エミュレータ必須）:
   - npx firebase emulators:exec --only firestore,auth,database \
     "npx playwright test --workers=1 <spec>"
   - 同じ E2E を2回連続で実行（フレーク検出）

4) git status がクリーンであることを確認:
   - git status --porcelain=v1

報告:
- 実行したコマンドと PASS まとめ
- 失敗内容と修正点
