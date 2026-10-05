---
name: publish-ig-bs
description: >
  Playwright（永続プロファイル）で Meta Business Suite を自動操作し、Instagram
  カルーセル（画像 2-10 枚）または **リール（reels/video.mp4）** を予約投稿する。
  content/sns/instagram 配下の carousel/ または reels/ を読み取り 1 パックずつ投稿。
  予約（--schedule）と即時（--now）の両方に対応し、IG 投稿の唯一の経路（旧 Graph API scripts/publish-ig.mjs は 2026-06-17 全廃）。
  Use when user says "IG予約投稿", "インスタ予約", "リール予約", "Business Suite 投稿".
  **初回 / セレクタ更新後は必ず --dry-run で事前検証すること**。
disable-model-invocation: true
argument-hint: "post <pack> --schedule <YYYY-MM-DDTHH:MM> [--reel] [--dry-run] [--pause] [--keep-fb] | login"
domain: sns
---

Playwright で Business Suite（business.facebook.com）のコンポーザを自動操作し、Instagram カルーセルを予約投稿する。設計は [[publish-x]] に倣う（永続プロファイル・システム Chrome で bot 回避・偽成功を出さない fail-safe・dry-run 必須）。

## CI 経路（2026-09-21）

**投稿も本スキル（Business Suite Playwright）を CI で回す。** Meta の利用制限で Graph API トークンを発行できないため、
`scripts/ig-graph-publish.mjs`（公式 API・即時公開のみ）は制限が解けたときの代替として残すが主経路ではない。
CI 実行は `ops-write.yml`（dispatch + plan hash）で、セッションは encrypted-state（`login-collectors.yml` と同じ
`restore-auth-state`）。手順:

```
npm run ops-write:plan -- --operation instagram.publish-bs --args '{"pack":"<exam>/<pack>","schedule":"YYYY-MM-DDTHH:MM"}'
# → 表示された hash と inputs（パック配下の caption/画像の sha256）を確認してから
gh workflow run ops-write.yml --ref develop -f operation=instagram.publish-bs -f args='{...同じ JSON...}' -f plan_sha256=<hash> -f commit=true
```

`commit=false` なら plan だけ。`--reel` は args に `"reel": true`。CI は headless なので初回は `commit=false` で plan を確認し、
Mac の `--dry-run` でセレクタが生きていることを確かめてから `commit=true` に進む（Business Suite の UI 変更で
セレクタが外れたら Issue `ops-write-instagram` が立つ）。予約スロットの実体確認（プランナー月ビュー）はローカル。

## 既存予約・公開済み投稿を改修するとき

[SNS 投稿画像ポリシー §0.1](../../../knowledge/reference/sns-image-policy.md) を先に読む。新規投稿フローを既存投稿の編集代わりに再実行しない。投稿 ID・予約の実体・変更可能項目を確認し、対応する編集処理がない場合はその不足を明示する。保存後の実表示と予約日時・公開状態の再照合までを外部更新の完了条件とする。

## ⚠️ 重要 1: IG 投稿の唯一の経路（予約 --schedule ／ 即時 --now）

- 旧 Graph API ルート **`scripts/publish-ig.mjs` は 2026-06-17 に全廃**。IG 投稿は本スキルに一本化された。
- 予約投稿（Graph API 非対応だった）に加え、即時公開も `--now` で本スキルが担う（fail-safe が緩むため検証用・非推奨）。
- **ToS リスク**: ブラウザ自動操作は Meta 利用規約上グレー〜違反。アカウント制限の可能性は自己責任。

## ⚠️ 重要 2: セレクタは 2026-06-09 に dry-run で実測確定済み（最終確定クリックのみ未実走）

`SEL` は実アカウント（Doboku-note / dobokunotecom）の dry-run で全工程を実測確定済み。ただし React UI は変わるため、**初回・1週間以上空いた後・失敗時は必ず `--dry-run` を回し**、`.local/playwright-ig-bs-debug/dry-run-scheduled-ready.png` で「Instagram 単独・日時・確定ボタン『日時を指定』」を目視してから本番投稿する。失敗時は `*-missing.png` を見て下表と `SEL` を更新。

予約モード未確認のまま確定すると即時公開が誤爆しうる（[[publish-x]] の 2026-04-18 事故と同型）。本スクリプトは「最終ボタンが**『日時を指定』**表示（=予約モード）になるまで確認できなければ中止」する fail-safe を持つ（即時公開ボタンは『公開する』で別物）。

### IG 単独化の副作用（実測で判明）
- 投稿先ドロップダウンで Facebook ページ option（`role=option` / `aria-selected`）を外すと **Instagram 単独モード**に切り替わる。
- Instagram 単独の選択状態を検証できない場合は確定せず停止する。
- IG 単独モードではメディアボタンが **「写真・動画を追加」**（FB+IG 時は「写真を追加」）に変わる → `SEL.addMedia` は `/写真.*追加/` で両対応。
- IG 単独だと予約セクションは **Instagram 1 行のみ**（FB+IG だと 2 行）。`setSchedule` は全行に同一日時を入れるため両構成で安全。
- アカウント名が違う環境では env `IG_BS_FB_PAGE` / `IG_BS_IG_ACCOUNT` で上書き。

## 前提条件

1. **システム Chrome がインストール済み**（Playwright 同梱 Chromium は Meta に bot 判定されやすい）
2. **初回ログイン**（一度だけ。2FA はブラウザ上で手動）:
   ```bash
   npx tsx .claude/skills/social/publish-ig-bs/publish-ig-bs.ts login
   ```
   → `business.facebook.com/latest` に入るとセッションが `<auth root>/profiles/playwright-ig-bs-profile/` に保存され自動終了。
3. **セッション切れ時**: 同じ `login` で再ログイン。
4. **SingletonLock エラー時**:
   ```bash
   pkill -f "playwright-ig-bs-profile" 2>/dev/null; rm -f <auth root>/profiles/playwright-ig-bs-profile/SingletonLock
   ```

## 使い方

```bash
# 1) 利用可能なパックを探す（carousel/img + carousel/caption.txt を持つもの）
ls content/sns/instagram/civil-1/theme-packs/

# 2) dry-run（初回必須。予約確定の手前まで実行しスクショ）
npx tsx .claude/skills/social/publish-ig-bs/publish-ig-bs.ts post \
  "civil-1/theme-packs/hoki-labor/pack-01" --schedule 2026-06-10T07:00 --dry-run

# 3) 予約ウィジェットのセレクタを対話採取（Inspector を schedule 手前で起動）
npx tsx .claude/skills/social/publish-ig-bs/publish-ig-bs.ts post \
  "civil-1/theme-packs/hoki-labor/pack-01" --schedule 2026-06-10T07:00 --pause

# 4) 本番予約投稿（dry-run 成功後に --dry-run を外す）
npx tsx .claude/skills/social/publish-ig-bs/publish-ig-bs.ts post \
  "civil-1/theme-packs/hoki-labor/pack-01" --schedule 2026-06-10T07:00
```

## 引数

| パラメータ | 必須 | 説明 |
|---|---|---|
| `post <pack>` | ✓ | パックのパス。`content/sns/instagram` 相対 or 絶対/プロジェクト相対。`carousel/img/*.png` + `carousel/caption.txt`（または直下 `img/` + `caption.txt`）を含むこと |
| `--schedule <dt>` | ※ | 予約日時 JST（`YYYY-MM-DDTHH:MM`）。Meta 制約: 約20分後〜カルーセル75日先／リール29日先。`--now` と排他 |
| `--now` | ※ | 予約せず即時公開（fail-safe が緩むため非推奨。検証用） |
| `--dry-run` | - | 確定の手前で停止しスクショ（**初回・セレクタ更新後は必須**） |
| `--pause` | - | schedule 手前で `page.pause()`（Playwright Inspector でセレクタ採取） |
| `--keep-fb` | - | Facebook 同時投稿トグルを触らない（既定は IG 単独に寄せる） |

※ `--schedule` か `--now` のいずれか一方が必須。

## パック構造（読み取り対象）

```
<pack>/
  carousel/
    caption.txt        # そのまま投稿キャプションになる（IG 上限 2200 文字）
    img/
      00-cover.png     # ソート順 = カルーセル並び順（2-10 枚）
      01-problem.png
      ...
```

`<pack>/img` + `<pack>/caption.txt`（carousel/ なし）でも可。投稿後 `<pack>/status.json` に `carousel.{status,scheduled_at,...}` を記録。

## 実測セレクタ表（2026-06-09 dry-run 検証済み）

| 操作 | セレクタ（`SEL` 内） | 備考 |
|---|---|---|
| コンポーザ判定 | 「投稿の詳細」テキスト / `role=button name=キャンセル` | モード非依存 |
| 投稿先を開く | `getByRole("combobox", { name: /^投稿先\s/ })`（実測 2026-09-11。旧 UI のみ FB ページ名へフォールバック） | boundingBox で開を確認 |
| FB を外す | `role=option name=Doboku-note` の `aria-selected` を true→クリック→false 検証 | IG 単独化 |
| メディア追加 | `role=button name=/写真.*追加/` → filechooserへ1枚ずつ投入 | 各サムネのCDN読込と既存画像順の維持を確認後に次へ。多枚一括投入は完了順に並び替わるため禁止（2026-09-11実測） |
| キャプション | `[contenteditable=true][role=textbox]` / `textarea` → clipboard paste + read-back 検証。10枚カルーセルで欄が遅延描画される現行UIは左ペイン末尾へ自動スクロールして再探索 | 日本語 OK |
| 予約 ON | `role=switch name=日時を設定` の `aria-checked` | これで日時欄が出現 |
| 日付 | `input[placeholder="yyyy/mm/dd"]` に `YYYY/MM/DD` | 全行に同一日時 |
| 時 / 分 | `input[aria-label="時間"]` / `input[aria-label="分"]` に `HH` / `MM` | 24時間。午後時刻は AM/PM 要確認 |
| 予約確定 | `role=button name=日時を指定`（即時は `公開する`） | 予約 ON で「公開する」→「日時を指定」に変化 |
| 予約モード検証 | 上記「日時を指定」ボタンが visible か | fail-safe の要 |
| 確定後の成功検知 | タイトル `/日時が指定されました\|時間を節約\|.../` or `role=button name=後で` | 下記の通り **複数パターン** |

> **時刻欄は `role="spinbutton"`**: 値は `.value` でなく `aria-valuenow`（ゼロ埋め無し "8" 等）。`keyboard.type("08")` で設定し `aria-valuenow` を `parseInt` 比較で検証＋リトライ。`.fill()`/`inputValue()` は効かない（2026-06-09 に分が既定値のまま残る事故あり）。
>
> **確定後の成功モーダルは Meta が出し分ける**（実測 2 種）: ①「投稿の日時が指定されました」＋宣伝アップセル（後で / 宣伝）②「今から投稿を日時指定で時間を節約できます」（後で / 別の投稿を日時指定）。**共通の「後で」ボタン**＋タイトル文言で成功判定し、「後で」で閉じる。`✅ 予約成功` ログは信用せず必ずプランナーで実体確認。

セレクタを直したら**この表と `SEL` を同時に更新**。

カルーセルは `scripts/lib/instagram-image-upload.mjs` で画像を直列に送る。各画像の処理を最大120秒待ち（遅延時も追加送信せず待つ）、完成サムネのURLパスと入力順を記録し、予約編集で開き直した一覧の並びも照合する。表紙だけが先頭にあればよいとせず、途中の説明と最後のCTAまで順序を確認する。既存予約の修正は対象投稿IDを確認して「投稿の編集」を使い、元の本文・予約日時・アカウントを保つ。

## リール（`--reel`）2026-06-09 実機検証済み

`--reel` で `reels/video.mp4` + `reels/caption.txt` を読み、リールを予約投稿する。カルーセルとは別 UI フロー。

```bash
# 予約（初回・更新後は --dry-run 必須）
npx tsx .claude/skills/social/publish-ig-bs/publish-ig-bs.ts post \
  "cem/exam-packs/r04/pack-07" --reel --schedule 2026-06-20T09:00 [--dry-run]
```

- 2 種のリールを扱える（どちらも `<dir>/video.mp4` + `<dir>/caption.txt` フォールバックで読む）:
  - **フルリール**: `<pack>/reels/video.mp4`（4問・長尺）。生成は `ig-reel-create`。
  - **1問1リール（推奨）**: `<pack>/reels-pp/q<N>/video.mp4`（36-45秒）。生成は `per-problem-shorts.mjs --ig-mode`。post の引数に q ディレクトリを渡す。
- **カバー（サムネ）を明示設定**: パックに `cover.png`（reels-pp）または `reels/img/00-cover.png`（旧構造）があれば、**編集ステップでファイルアップロードしてサムネを確定**する（Meta 自動抽出任せにしない）。`per-problem-shorts.mjs --ig-mode` は `cover.png`（論点カバー＝先頭スライド）を出力する。カバーを指定したパックは、編集 UI やアップロードを確認できなければ停止する。未指定パックだけ Meta 自動サムネを使う。`reels/cover.png` にも対応。
- **動画・音声・カバーは git に持たない（JIT）**: mp4・wav・cover.png は再生成可能な派生物で gitignore（コミットは slide-data + script.txt + caption.txt。wav は Drive vault 退避＝`drive-vault-sync --group sns-archived-media`／script.txt から再生成可）。**`video.mp4`・`wav` が無いのは正常** — 投稿時に生成し、予約後に削除する。`scripts/publish-reel-jit.mjs`（生成→予約→mp4/cover削除）が1コマンド化。
- 投稿後 `status.json` に `reel.{...}` を記録（caption.txt / status.json は追跡）。

### リールフローの実測（カルーセルとの差分）

| 操作 | セレクタ／挙動 |
|---|---|
| 入口 | ホーム → `role=button name="リール動画を作成"` → `/latest/reels_composer` |
| 動画追加 | `role=button name="動画を追加"` → filechooser。**アップ後 ~20-40s 処理待ち**（自動生成サムネ出現で判定） |
| 投稿先 IG 単独化 | カルーセルと同じ `role=option`（FB ページを外す） |
| キャプション | 共通（contenteditable textbox） |
| ステップ送り | 3 ステップ（作成→編集→シェアする）。**右下の「次へ」を座標で click**（サムネ送りの「次へ」ZWSP を誤爆しない）。カバー等の処理中で無効なら押さず最大180秒待つ |
| カバー設定（2026-06-24 実機確定） | カバーありなら **`role=button「編集」`クリック → 「サムネイル」節へスクロール → `画像をアップロード`タブ → パネル内の`画像をアップロード`で `filechooser` → `cover.png` 投入**（`画像を変更`表示で確定）。**「次へ」送りでは編集が自動完了して飛ぶ**ため編集タブを直接押す。サムネ＝「カバー」ではなく「サムネイル」ラベル。指定カバーの設定失敗時は確定せず停止。スクショは `.local/playwright-ig-bs-debug/reel-cover-*` |
| 予約 | シェアするで `role=button name="日時を指定"` → 日付/時刻（共通 spinbutton）→ 確定 `role=button name="公開日時を指定"` |
| 即時 | `role=button name="今すぐシェア"`（`--now`） |
| fail-safe | 「公開日時を指定」ボタンが出るまで確認できなければ中止（即時シェア誤爆防止） |

## 「予約完了」ログを信用しない（実体検証）

`✅ 予約投稿 完了` / `✅ リール予約 完了` ログは成功の証拠にしない。Business Suite の **プランナー（コンテンツ → カレンダー/予定）** を開き、当該カルーセル/リールが正しい日時・正しいアカウント（Instagram のみ）で予約キューに実在することを目視するまで「完了」と報告しない。

## スクリプト本体

`.claude/skills/social/publish-ig-bs/publish-ig-bs.ts`

## 混在バッチ

`batch <json>` は `items: [{packArg, schedule, kind}]` を順番に処理する。`kind` は `carousel` または `reel`（省略は既存互換で `reel`）。日時は JST の `YYYY-MM-DDTHH:MM`。初回は両形式を `post ... --dry-run` で検証する。途中失敗時は停止し、再投入前に実予約と各 `status.json` を照合する。
