---
name: gsc-review
description: >
  月次 GSC index coverage レビューのオーケストレータ。CI（index-coverage.yml）が更新した
  url-inspection スナップショットと data/gsc/index-coverage.json を gsc-index-auditor で診断し、
  .claude/knowledge/reference/gsc-management.md の「観測・判断ログ」へユーザー判断つきで追記する流れを統括する。
  performance（CTR/rank）は /weekly-improve（metrics-analyzer）、CWV は performance-auditor の担当で直交。
  Use when user asks to [GSC月次レビュー, index coverage確認, インデックス率, /gsc-review].
user-invocable: true
domain: site
---

月次の GSC **index coverage** レビューを回すオーケストレータ。「サイトの何割が Google に登録され、未登録の原因は何か」を継続管理する。設計・閾値・判断マトリクスの真実源は [.claude/knowledge/reference/gsc-management.md](../../../../.claude/knowledge/reference/gsc-management.md)。

## いつ使うか

> [!important] 通常は GitHub Actions が自動で記録する（2026-08-06〜）
> `.github/workflows/gsc-auto-review.yml`（金 JST 12:00）が、未記録の inspection-batch を見つけると
> `gsc-index-auditor` を起動し観測ログへ `### YYYY-MM-DD（月次・自動レビュー）` を自動追記する。
> **本スキルは応急・深掘り・上書き用**＝①月初から金曜を待たずに見たい ②自動エントリの判断を
> 人が上書きしたい ③ `gsc-auto-review.yml` が失敗・沈黙した（`npm run check-gsc-auto-review` が DUE / `automation-failure`
> Issue が立った）とき。自動エントリと同日付で手動エントリを足してよい（append-only）。

- 毎月 `index-coverage.yml`（CI・月初 JST 11:00）が走った**翌日以降**（最新スナップショットが develop に commit 済みの状態）
- index coverage の急変を疑うとき

> performance（impressions/CTR/順位の改善候補）は守備範囲外＝`/weekly-improve`（`metrics-analyzer`）へ。本スキルは coverage 専任。

## 前提（計測は CI 供給が正）

ローカルで GSC API を叩かない（creds 未設定・会社 PC はプロキシ遮断。`measurement-incidents.md` 2026-06-05）。本スキルは **CI がコミット済みのスナップショットを読む**だけ。最新が無い/古いときは「`index-coverage.yml` を `workflow_dispatch` で回してから再実行」と案内する。

## 手順

1. **データ確認**
   - `data/gsc/url-inspection/` の最新ファイルの日付を確認
   - `data/gsc/index-coverage.json` の最新エントリ日付を確認
   - 最新 batch が当月でなければ、CI 未実行と判断し `gh workflow run index-coverage.yml` を案内（実行はユーザー判断）

2. **診断（gsc-index-auditor を起動）**
   - サブエージェント `gsc-index-auditor` を呼ぶ（最新 batch と history を読ませる）
   - 返ってくる診断（indexed_ratio・前回差分・原因バケット・hygiene URL・データ健全性フラグ）を受け取る

3. **観測・判断ログ追記の下書き提示**
   - `.claude/knowledge/reference/gsc-management.md` 末尾の「観測・判断ログ」セクションに追記する Markdown 下書きを作る（日付・数値・診断・**推奨アクション**）
   - 数値は history.json を引用。原因バケットは auditor の判定を踏襲

4. **ユーザー判断 → 確定**
   - ユーザーが「何を打ち手にするか（被リンク獲得 / コンテンツ統合 / 量の抑制 / hygiene 即修正 / 様子見）」を決める
   - 決定を加えて `gsc-management.md` の観測・判断ログへ Edit で追記（人間の意思決定記録）
   - hygiene の 404/redirect は具体タスクとして `.claude/todo/` へ起票を提案

## 出力

- 会話内に diagnosis サマリー
- `.claude/knowledge/reference/gsc-management.md` の観測・判断ログへ 1 エントリ追記（ユーザー承認後）
- 必要なら `.claude/todo/` に hygiene 修正タスク

## 深掘り（理由別の例 URL が要るとき）

本スキルは CI（API/sitemap）データで coverage 全体を診断する。**「クロール済み-未登録」等の理由ごとに
どの URL がそうなっているか**は API では取れない（GSC UI のみ）。同月内に `/google-search-growth`
（ローカル・要 Google ログイン）を併走すると、理由別 UI CSV を取得して API データと URL 突合し、
修正アクション（FIX_TECHNICAL / REDIRECT_LEGACY / CONSOLIDATE / NOINDEX 候補）へ分類できる。
期限は `check-gsc-ui-due` を weekly-review が surface。両者は同じ観測・判断ログを共有。
判定は日数だけではない＝**最後の完全取得（`lastComplete`）から 30 日**、または
**直近の実行が不完全（`lastAttempt.complete !== true`）**のいずれかで DUE（2026-07-30 改訂）。

## やらないこと

- GSC データの取得（CI の責務）／history.json への追記（CI の `append-coverage-history.mjs`）
- 理由別 UI CSV の取得（`/google-search-growth`＝ローカル手動・月次）
- performance / CWV の分析（`/weekly-improve` / `performance-auditor`）
- 修正の自動実施（ユーザー判断 + 各 Generator）

## 参照

- `.claude/knowledge/reference/gsc-management.md` — GSC 管理 SSOT（分業/閾値/判断マトリクス/観測ログ）
- `.claude/agents/gsc-index-auditor.md` — 診断 Evaluator（本スキルが起動）
- `.github/workflows/index-coverage.yml` — 月次取得 CI
- `.claude/skills/management/weekly-improve/SKILL.md` — performance 側（直交・補完）
