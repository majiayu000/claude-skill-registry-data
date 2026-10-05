---
name: scout-asp
description: >
  A8.net の提携アフィリエイトを Playwright で操作する（doboku-note 版・転職一本スコープ）。
  list=申込中/参加中の承認状態を確認（主用途・口座横断）、search=doboku ニッチ語で未提携案件を狙い撃ち検索、
  import-partnered=提携中を catalog 取込、scout/apply=A8 カテゴリ09(仕事)自動開拓・週次上限で申請（doboku-note で）、
  check-approval=承認昇格、harvest=承認済みの広告コード取得（doboku-note）→affiliate-creatives.ts への手配置候補を出力。
  Use when user says "A8確認", "アフィリエイト承認確認", "申請済みアフィリを見る", "A8案件を探す", "A8提携状況", "scout-asp".
  **初回 or セレクタ更新後は必ず `list --dry-run --headed` で実機ダンプ→セレクタ確定すること**.
  **search/scout の出力は candidate 以外（blocked / dup / vertical未解決 / 閾値未満）も必ず表示する**
  ＝「candidate 0 件」を「該当なし」と誤読しないこと.
disable-model-invocation: true
argument-hint: "<list|search|import-partnered|scout|apply|check-approval|harvest> [--keyword <語>] [--program <pid>] [--dry-run] [--headed] [--limit N] [--max N]"
domain: affiliate
---

> [!important] candidate 0 件 ≠ 該当なし
> `search` / `scout` は候補にならなかったものも**必ず内訳を出す**（2026-07-27 修正）。
>
> | バケット | 意味 | catalog |
> |---|---|---|
> | `candidate` | 3軸に写像でき、閾値以上 | 登録 |
> | `blocked` | blocklist（Red Line: 転職一本・講座/教材/スクール系は不可） | 登録しない |
> | `対象外業種` | `offTargetKeywords`（薬剤師/看護/介護 等）＝**規約NGではないが読者と無関係** | 登録しない |
> | `dup` | 既存 creative と重複 | 登録しない |
> | `vertical未解決` | doboku の 3軸（civil-career / pe-career / career）に写像できない | `pending-vertical` |
> | `閾値未満` | score < `minScore`（既定 0.35） | 登録しない・**表示はする** |
>
> 以前は「閾値未満」と「vertical 未解決」が黙って捨てられており、`candidate 0 件 (blocked 0 / dup 0)` が
> ヒット 0 と区別できなかった。実際には施工管理 2 件・建設 転職 4 件がヒットしていた
> （2026-07-27 の建設案件調査で発覚）。**拾うかどうかは人が決める**ので、機械は必ず見せる。

A8.net メディア管理画面 (media-console.a8.net) を Playwright（永続プロファイル）で操作し、提携アフィリエイトの
**確認 → 開拓 → 申請 → 承認 → コード取得** を回す。判定はすべて決定的コアに委譲し、SSOT（配置）判断だけ人が持つ。

> **正典は `.claude/knowledge/reference/a8-affiliate-pipeline.md`**。本 skill は手順のみ。スコア式・blocklist・vertical 写像・
> 申請上限は `.claude/scripts/ads/data/a8-curated.json`、状態機械は `a8-scout-core.mjs`、抽出仕様は
> `a8-code-core.mjs` が SSOT。stats47 の `scout-asp` を doboku（転職一本）へ移植・スリム化したもの。

## doboku 固有の方針（stats47 との違い）

- **転職一本**: scout は A8 カテゴリ **09(仕事) のみ**巡回（curated `categoryCodeToVertical`）。講座/教材/書籍/添削は
  `blocklistKeywords` で恒久除外（2026-06-25 廃止・memory `affiliate-career-only` の Red Line）。
- **register は手キュレーション**: doboku の creative SSOT は `src/config/affiliate-creatives.ts`（3枠・意図配置・
  カニバリ回避）。stats47 のような `AFFILIATE_ADS[]` 自動追記機構は無い。よって **harvest は「配置候補（SidebarAdCreative 形 +
  mats 追記案）を catalog の adDraft に出力するまで」で止め、確定配置は人が判断**する（1ページ1ピクセル・vertical セグメント・
  campaign 窓を壊さないため）。

## 前提: 初回セットアップ (1 回だけ・人間)

1. **A8 手動ログイン** (credential は env に置かない・永続プロファイル方式):
   ```bash
   node .claude/skills/ads/scout-asp/scripts/login.mjs   # 本体 ~/doboku-note で実行 (worktree 不可)
   ```
2. **セレクタ実機チューニング** (A8 の DOM は stats47 由来の推測値。初回だけ確定が要る):
   ```bash
   npx tsx .claude/skills/ads/scout-asp/scripts/a8-browser.ts list --dry-run --headed
   # → .local/playwright-a8-debug/ に page 構造 + スクショをダンプ。
   #    a8-browser.ts の A8 定数 (URL/セレクタ) を実機に合わせて調整する。
   ```

## モード

`/scout-asp [list|import-partnered|scout|apply|check-approval|harvest]`。

| モード | 動作 |
|---|---|
| `list` | **申込中(審査待ち) + 参加中(承認済み) を読み、配置済み mat と突合して表示**（主用途＝申請済みアフィリの承認確認）。承認済みは catalog に approved 反映。**注: A8 の list は口座横断＝doboku-note と stats47 の提携が混在（webSiteId フィルタは効かない）** |
| `search` | **doboku ニッチ語（curated `searchKeywords`）で `/program/search/keyword` を狙い撃ち検索** → 既提携/blocklist を除外 → candidate upsert。`--keyword <語>` で単発検索も可。カテゴリ検索(scout)より doboku 向き |
| `import-partnered` | 提携中の全プログラムを全ページ巡回 → catalog に approved で取り込む（申請不要で harvest 直行） |
| `scout` | A8 カテゴリ09検索(1ページ) → scoreAndRank → catalog に candidate upsert（ニッチには `search` 推奨） |
| `apply` | candidate 上位を週次上限内で自動申請 → applied。**申請前に webSiteId=doboku-note を選択（誤サイト防止）**・`check-a8-apply-budget` が上限強制 |
| `check-approval` | applied 全件を参加中一覧で再走査し approved に昇格 |
| `harvest` | approved の広告コード取得（**websiteId=doboku-note 選択**）→ parse → adDraft（配置候補）を catalog に出力（confirmed 配置は手判断）。`--program <pid>` で狙い撃ち |

## サブコマンド直呼び

```bash
npx tsx .claude/skills/ads/scout-asp/scripts/a8-browser.ts list [--dry-run] [--headed]
npx tsx .claude/skills/ads/scout-asp/scripts/a8-browser.ts search [--keyword <語>] [--dry-run] [--limit N]
npx tsx .claude/skills/ads/scout-asp/scripts/a8-browser.ts import-partnered
npx tsx .claude/skills/ads/scout-asp/scripts/a8-browser.ts scout [--dry-run] [--limit N]
npx tsx .claude/skills/ads/scout-asp/scripts/a8-browser.ts apply [--dry-run] [--max N]
npx tsx .claude/skills/ads/scout-asp/scripts/a8-browser.ts check-approval [--dry-run]
npx tsx .claude/skills/ads/scout-asp/scripts/a8-browser.ts harvest [--dry-run] [--limit N] [--program <pid>]
node .claude/scripts/ads/check-a8-apply-budget.cjs                # 今週の申請残枠
npm run test:ads                                                 # 純関数コアのユニットテスト (node:test・30件)
```

## 制約 (必ず守る)

- **ローカル限定**（プロファイルは `.local/`・GitHub Actions では動かない）。OS は問わない＝Mac パスが実在しなければリポジトリルートへフォールバック（2026-07-27 可搬化・Windows 実走確認済み）。
- **セッション失効 (isLoggedIn 失敗) は catalog に error 記録して正常終了** — パイプラインを壊さない。再ログインは人間。
- **審査落ち (rejected) は再申請しない**。
- **申請は週 `weeklyApplyMax` 件まで**（`a8-curated.json`。A8 スパム判定回避。初期 5）。
- **講座/教材/書籍/添削は blocklist で恒久除外**（転職一本の Red Line）。
- **creative の確定配置（affiliate-creatives.ts / affiliate-mats.json 追記）は手判断**。harvest は候補出力まで。
- **node_modules 不在時は先に `npm install --legacy-peer-deps`**（tsx/playwright に必要）。

## 関連

- 正典ルール: `.claude/knowledge/reference/a8-affiliate-pipeline.md`
- 認証方式: `.claude/knowledge/reference/playwright-auth-profiles.md`（a8 profile）
- コア: `.claude/scripts/ads/lib/{a8-scout-core,a8-code-core}.mjs` / 申請上限 `.claude/scripts/ads/check-a8-apply-budget.cjs`
- ブラウザ: `.claude/skills/ads/scout-asp/scripts/{a8-browser.ts,login.mjs}`
- カタログ: `data/a8/catalog.json`（状態機械）/ curated: `.claude/scripts/ads/data/a8-curated.json`
- 配置先 SSOT: `src/config/affiliate-creatives.ts` / `src/config/affiliate-mats.json` / `.claude/knowledge/reference/affiliate-operations.md`
