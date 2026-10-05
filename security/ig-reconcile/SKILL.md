---
name: ig-reconcile
description: >
  Instagram の公開状態をライブのグリッド＋プランナーと照合し（現状確認）、ローカル SoT
  (posted.json/status.json) のドリフトを是正し、未公開パックを安全に予約投稿まで運ぶ運用スキル。
  CI 週次 snapshot（`login-collectors.yml` の `verify-ig-status`・encrypted-state）でドリフトを検出→posted.json backfill / draft 誤記録是正→`ig-publish-auditor`
  で公開可否ゲート→`publish-ig-bs` で衝突しない時間帯へ予約→プランナーで実体確認。投稿/予約は
  operator 確認後のみ・公開済み投稿の削除は対象外（不可逆）。Use when user asks to
  [IG公開状態を確認, インスタ公開状態, 未公開を予約投稿, IGのSoTドリフト是正, IG status reconcile, /ig-reconcile].
disable-model-invocation: true
argument-hint: "[--backfill] [--schedule-unpublished] [--exam=cem]"
domain: sns
---

IG カルーセルの「実際に公開されているか（現状確認）」と「未公開の予約投稿」を、毎回ゼロから手作業せず**反復実行**するためのオーケストレーションスキル。設計の真実源は [.claude/knowledge/reference/ig-publish-reconcile.md](../../../../.claude/knowledge/reference/ig-publish-reconcile.md)。

## 既存予約・公開済み投稿を改修するとき

[SNS 投稿画像ポリシー §0.1](../../../knowledge/reference/sns-image-policy.md) を先に読む。新規投稿フローを既存投稿の編集代わりに再実行しない。投稿 ID・予約の実体・変更可能項目を確認し、対応する編集処理がない場合はその不足を明示する。保存後の実表示と予約日時・公開状態の再照合までを外部更新の完了条件とする。

## なぜ必要か（このスキルが生まれた経緯）

手動投稿のあと `posted.json` を残し忘れる／`status.json` を `draft` のまま放置するドリフトが頻発する（2026-06-25、keyword-packs 18件中 6件が未記録・1件 draft 誤記録・削除済み黒背景の旧 URL が記録残存）。`ig-status` はローカルしか見ず検知できなかった。本スキルはライブ照合を起点に SoT を実態へ寄せ、未公開を予約まで運ぶ。

## アカウント SSOT

実アカウントは **`@dobokunotecom`**。アカウントとプロフィール表示値の機械可読SSOTは [`config/ig-account.json`](../../../../config/ig-account.json)。Xは別アカウント `@doboku373`（`config/x-account.json`）。スクリプトはハンドルを誤ると空振りするので、必ずconfig経由で参照する。

## フロー

### 1. 照合（現状確認・read-only）

照合は CI 週次 `login-collectors.yml`（encrypted-state・`verify-ig-status --no-planner`・PR #549） が Playwright で `.claude/state/ig-reconcile/snapshot.json` を `source:"graph-api"` で書く。本スキルはその snapshot を読むのが既定で、Playwright 版 `verify-ig-status` はプランナー実体確認が要るときのフォールバックとして残す。

```bash
npm run verify-ig-status            # 全パック / npm run verify-ig-status -- --exam=cem で絞る
npm run verify-ig-status -- --json  # 機械処理用
```

ドリフトを 7 分類で出す（真実源は reference の表）:
`published_recorded`(整合) / `published_UNrecorded`(★要 backfill) / `draft_misrecorded`(★) / `recorded_but_gone`(★記録 URL が削除済み) / `scheduled`(予約済み) / `unpublished`(未公開＝予約候補) / `anomaly`(★同テーマ重複・要人手判断)。スナップショットは `.claude/state/ig-reconcile/snapshot.json`。

> Playwright + ログイン済み `<auth root>/profiles/playwright-ig-bs-profile` が必要。**ローカル実行限定**（会社 PC のプロキシ下では外部到達不可）。セッション切れは `publish-ig-bs ... login` で再ログイン。

### 2. ドリフト是正（非破壊・operator 確認のうえ）

- `published_UNrecorded` → 該当パックの `posted.json` をライブ URL/日付で **backfill**（`ig-status mark <pack> carousel --url=... --note=...` か直接編集）。
  **`ambiguous: true` が付いたエントリは backfill しない**（`matched=1` でも複数パックが同じ投稿を主張＝一意対応ではない。未投稿のパックへ「投稿済み」を書き込む事故になる。2026-08-27 実測で 72 件中 48 件が該当）。`ambiguousWith` に衝突相手が入る。
- `draft_misrecorded` → `status.json` の `carousel:"draft"`/`posted:false` を実態へ是正。
- `recorded_but_gone` → 記録 URL が削除済み。白版へ貼り直し済みなら新 URL へ更新、孤児なら note 付きで記録。
- `anomaly`（重複投稿・逆方向の衝突）→ **自動処理しない**。`ig-publish-auditor` のフラグを人へ提示し判断を仰ぐ。

### 3. 未公開の予約投稿

1. `unpublished` 各パックを **`ig-publish-auditor`**（Evaluator）に渡し公開可否ゲート（caption 実在/品質・画像枚数・draft 痕跡・スライド整合）。Bash 不可なので親（このスキル）が reconcile JSON ＋ パック内容（caption.txt / img 一覧 / status）をテキストで渡す。
2. `ready` のみ、既存キュー（07:30/12:00/17:00/21:00 等）と**衝突しない時間帯**へ予約。既定は **19:00/日**（本運用で確立した空き帯）。スロットは reference の方法で確認。
   ```bash
   npx tsx .claude/skills/social/publish-ig-bs/publish-ig-bs.ts post "cem/keyword-packs/<slug>" --schedule 2026-MM-DDT19:00
   ```
   初回・1週間以上空いた後は `--dry-run` を必ず先に。
3. **プランナーで実体確認**（月ビューの時刻チップ抽出。週送りボタンは効かず／日セルのクリックは投稿作成画面を開くので禁止）。`verify-ig-status`（planner あり）か reference の手順で 19:00 スロットの実在を目視。

## 安全弁（必読）

- **報告＋提案が既定**。posted.json 編集・予約投稿・どれも **operator 確認後のみ**実行する。
- **公開済み投稿の削除は本スキル対象外**（不可逆）。黒背景の貼り直し等は個別判断で手動。
- **鉄則: リール≠カルーセル。同テーマのリールが存在することはカルーセル削除の根拠にならない**。削除・重複判定の前に投稿の型（`/p/`=カルーセル・`/reel/`=リール・「オリジナル音源」表示）を必ず確認する。`verify-ig-status` の `type_mismatch` が機械ガード（rio 事故の再発防止）。
- **「予約成功モーダル＋status.json」だけを信用しない**。必ずプランナー実体確認（[[publish-ig-bs]] の偽成功検証と同じ規律）。
- **コミットは並行セッション保護のため develop を別 worktree で**行う（`git worktree add <dir> develop` → 編集 → pathspec commit → push → worktree 撤去）。共有 worktree では `git commit` も pathspec 必須・commit 先 branch 確認。真実源 → reference「並行セッションとコミット」。

## 関連

- `verify-ig-status`（`scripts/verify-ig-status.mjs`）= 照合エンジン（read-only）。`ig-status` = ローカル投稿記録 CRUD。
- `publish-ig-bs` = 予約投稿エンジン（本スキルが呼ぶ）。
- `ig-publish-auditor`（Evaluator）= 公開可否ゲート＋異常検出。
- 週次: CI `login-collectors.yml`（encrypted-state・`verify-ig-status --no-planner`・PR #549） が `.claude/state/ig-reconcile/snapshot.json` を書き、`/weekly-review` はそれを読む（実行しない）。`verify-ig-status` はプランナー実体確認が必要なときのローカルフォールバック。
