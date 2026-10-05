---
name: note-publish
description: >
  note.com/dobokunote の有料記事を Playwright × システム Chrome で「下書き作成→公開」する Windows 決定的パブリッシャ。カバー/タイトル/本文(markdown変換)/価格/タグ/有料境界を自動設定し、境界検証ゲート通過後に公開する。Use when user says [note記事公開, note有料記事を投稿, note自動公開, /note-publish].
disable-model-invocation: true
user-invocable: true
argument-hint: "--article <article.md path> [--commit] [--schedule YYYY-MM-DDTHH:MM]"
domain: product
---

`scripts/note-publish.mjs` を駆動し、note 有料記事を**下書き作成→公開**する。`publish-note`（browser-use=Mac・AIエージェント）の **Windows 決定的 Playwright 版**で、`note-magazine-add` と同じ「システム Chrome（`channel:'chrome'`）＋永続プロファイル（`<auth root>/profiles/playwright-note-profile`）＋proxy＋`ignoreHTTPSErrors`」で会社PCの社内プロキシ（TLS傍受）を越える。

## いつ使うか / どちらを使うか

- **このスキル（Windows可・決定的）**: BK マガジン等の有料記事を Windows から公開する。
- `publish-note`（browser-use=Mac）: LLM バックエンドが必要で会社PCプロキシでは不可。Mac 専用。
- **publishing は意図的にユーザー起動限定**（`disable-model-invocation: true`）。エージェントが勝手に公開しない。決定的フローのためサブエージェント化もしない（原則5）。

## CI 経路（ops-write.yml・2026-09-21）

`note.publish`（本スキルの `scripts/note-publish.mjs`）は `ops-write.yml`（dispatch + plan hash）から実行できる。

```
npm run ops-write:plan -- --operation note.publish --args '{"article":"content/note/<dir>/article.md"}'
# hash を確認 → 内容確認 →
gh workflow run ops-write.yml --ref develop -f operation=note.publish -f args='{"article":"..."}' -f plan_sha256=<hash> -f commit=true
```

同カタログには note 系の他操作（`note.update-body` / `note.update-cover` / `note.update-partial` / `note.sync-tags` / `note.price-sweep` / `note.append-cta` / `note.magazine-add-articles` / `note.attach-file` / `note.membership-plan-edit`）もあり、それぞれ対応スクリプトの `--commit` を同じ plan hash ゲートで実行する。真実源 `.claude/config/ci-write-operations.json` / `scripts/lib/ci-write-gate.mjs`。

## 安全弁（収益アカウントのため必須・崩さない）

1. **account=dobokunote を assert**（不一致は即中断・1記事も触らない。誤公開事故の再発防止）
2. **既定は draft**（下書き保存のみ）。実公開は `--commit` 必須
3. `--commit` でも **有料境界が「試験問題/予想問題」H2 の直前にあるか検証**してからのみ投稿（`boundaryBeforeExam=false` は公開中断）
4. 公開後は note 公開ページを実取得し **無料プレビュー/カード/価格** を実体検証（[[feedback_publish_x_false_success]] 偽成功ガード）

## 使い方

```
node scripts/note-publish.mjs --article <article.md path>          # 下書き作成のみ（既定・安全）
node scripts/note-publish.mjs --article <article.md path> --commit # 即時公開（境界検証ゲート付き）
node scripts/note-publish.mjs --article <path> --commit --schedule 2026-06-20T07:00 # 予約投稿（JST）
```

- カバー/タグは記事と同じ年度dir の `img/cover-<type>.png` / `hashtags-<type>.txt` を自動解決（`article-II1.md` → `cover-II1.png`/`hashtags-II1.txt`。無ければ `cover.png`/`hashtags.txt`）。
- 価格・有料/無料は frontmatter `notePricing`/`price`。`notePricing: paid` かつ `price>0` で有料設定。
- **予約投稿（時間ずらし可）**: `--schedule "YYYY-MM-DDTHH:MM"`（JST）で即時公開でなく予約公開（note は現在 無料で予約可）。即時「投稿する」の代わりに 日時設定→日付→時刻→「予約投稿」を操作。**日時を UI で確定できないときは即時公開せず下書きに退避**する安全弁つき。予約 UI selector は `publish-note/references/scheduling.md` 由来で、初回実走の `.tmp/np-sched-*.png` で要確認。

### マガジン一括（バッチ）

1マガジン分（`article-*.md` 全部）の公開は **`note-publish-magazine`** を使う（1記事ずつ `note-publish --commit` を直列実行・**冪等**〔frontmatter に noteUrl あればskip〕・1記事最大2回試行・失敗で停止→再実行で再開・公開順 R03→R08-yosou × II1→II2→III）。**偽成功ガード（2026-07-01）**: 即時公開分は「noteUrl が書けた」だけで OK とせず、書き戻した noteId が note API で実在するか照合し、確定 404（幻 id）なら fail 停止する（工事82-87 が fail=0 のまま未公開だった再発防止）。**連続投稿スロットル対策（DN-0118・2026-08-22 実測）**: 即時公開31本目以降で「投稿する」が完了しなくなる現象を確認（20分待機で解消）。既定で**25本(`--batch-size`)ごとに20分(`--cooldown-minutes`)自動クールダウン**する（予約投稿時は対象外）。**バッチ完了後は必ず `npm run verify-note-status`**（fm=published↔ライブ404 を検出）で全件確証してから完了報告する。公開前の単品価格揃えは **`note-price-sweep`**（frontmatter `price` を一括スイープ・既定 1980→500・CRLF保持）。

```
node scripts/note-price-sweep.mjs --dir <magazineDir> --commit          # Step1: 価格スイープ（→ pathspec commit）
node scripts/note-publish-magazine.mjs --dir <magazineDir> --commit     # Step2: 18記事を直列公開（→ writeback を pathspec commit）
# 明示リスト＋時間ずらし予約投稿（無料記事16本など）:
node scripts/note-publish-magazine.mjs --list <manifest.txt> --schedule-start 2026-06-20T07:00 --interval-hours 24 --commit
```

無料記事（`article.md`）や対象を厳密に絞るときは `--pattern article.md` / `--list <manifest.txt>`（1行1パス・# コメント可）。**時間ずらし予約投稿**は `--schedule-start "YYYY-MM-DDTHH:MM"` ＋ `--interval-hours N`（既定24・slot i = start + i×interval・TZ非依存）。長尺（18記事≈25分）なので `run_in_background` ＋ article-1 watcher で早期検証推奨。BK マガジン公開の全体パイプライン（sweep→publish→create→cover→add→attach-pdf→SoT→verify→push）は [[project_pe_construction_bk_magazines]] が真実源。**PDF 添付（`note-attach-pdf`）は 1日100件のアップロード上限あり＝1日最大5マガジン**に注意（記事公開の画像 eyecatch は別枠）。

## 自動化される工程 / 手動の例外

| 工程 | 自動 |
|---|---|
| account ゲート / 新規エディタ / カバー(eyecatch) / タイトル / 本文(ClipboardEvent paste・markdown変換) | ✅ |
| 価格（Shadow DOM `input#price` を JS setter で上書き） | ✅ |
| タグ（公開設定パネルの「ハッシュタグを追加する」→type+Enter・先頭30） | ✅ |
| **有料境界**（有料エリア設定画面で「試験問題/予想問題」H2 直前の「ラインをこの場所に変更」を DOM順で特定→クリック→検証） | ✅ |
| **リンクカード化**（CTA の URL 単独行） | ✅ 自動（type 方式） |

### リンクカード化の仕組み（type 方式・2026-06-15 確定）

note の埋め込み検出は **`keyboard.type`（実入力）で起動し、synthetic な `ClipboardEvent` paste では起動しない**（v1〜v5 の paste/Enter 系は全失敗、v6/v7 の type で確定。真実源 `.claude/knowledge/reference/note-api-verification.md` L101「URL単独行で入力→Enterでリンクカード化」）。

実装（step 6）: 本文を bulk paste すると URL はプレーン文字列になるので、各 URL 行を **Range API で選択 → `Delete` → `keyboard.type(url)` → `Enter`** で「その場」をカードへ置換（周囲テキストは保持）。[[feedback_note_link_card]] 準拠（カードの方が CTR 高い）。

## 既知の限界・運用

- 1記事ずつ実行（バッチは呼び側でループ）。実行ごとに `/new` が空ドラフトを生成するため、失敗時は残った空ドラフトを削除する。
- **冪等**: frontmatter に `noteUrl`（https）があれば**スキップ**（バッチ再実行で重複公開しない）。公開成功時に `noteUrl`/`noteId`/`notePublishedAt`/`noteStatus`（published／予約=reserved）を**当該 article.md frontmatter へ自動記録**。
- スクショ: `.tmp/np-boundary.png`（境界画面）/ `.tmp/np-final.png`（最終）。
- 公開後 URL は記事 frontmatter `noteUrl`/`noteId` と `note-magazines.ts`（マガジン全記事公開後に `published:true`）へ反映する（[[feedback_no_price_in_mdx_body]]・真実源 `src/lib/note-magazines.ts`）。

## 参照

- `scripts/note-publish.mjs` — 本体
- `.claude/skills/social/publish-note/` — browser-use 版（Mac・手順の元）。本スキルはその Windows Playwright 版
- `.claude/skills/social/note-magazine-add/` — 公開後のマガジン収録（別操作）
- `.claude/knowledge/reference/note-api-verification.md` — 公開状態の実体検証
