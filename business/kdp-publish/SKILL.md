---
name: kdp-publish
description: >
  ビルド済み Kindle 本（EPUB＋表紙）を Amazon KDP へ入稿し下書き保存→（承認後）出版する。
  詳細記入・カテゴリー選択・原稿/表紙アップロード・原稿処理完了待ち・AI申告・アクセシビリティ・
  価格・出版までを scripts/kdp-publish.mjs（Playwright・永続プロファイルでログイン保存）で駆動し、
  提出前の本棚突合（重複防止）・提出後の catalog.json 更新・LIVE 化後の ASIN 記録は kdp-operator が担う。
  真実源は config/kdp-memo.json（defaults＝共通申告/カテゴリー経路）。EPUB を作る /kindle-build の後工程。
  Use when user asks to [KDP出版, KDP提出, KDP公開, kindleを出版, KDP状態同期, KDPドラフト削除, /kdp-publish].
user-invocable: true
domain: product
---

## 用途

`/kindle-build` で生成した EPUB を、Amazon KDP のブラウザ UI へ自動入稿し出版する。UI 操作は決定的
Playwright スクリプトで、判断（重複突合・未登録本のメタデータ生成・出版可否）は `kdp-operator` が担う。

```
/kindle-build {id}  →  EPUB+表紙（kindle-dist/）
        ↓  npm run sync-kindle-dist -- --downloads {id}   （~/Downloads へ配置）
/kdp-publish {id}   →  KDP 入稿（詳細→カテゴリー→アップロード→AI申告→価格→下書き）
        ↓  人が Kindle Previewer 目視・承認
/kdp-publish {id} --commit-publish  →  出版（不可逆・審査へ）
```

## CI 経路（ops-write.yml・2026-09-21）

`kdp.publish`（出版・risk highest）は `ops-write.yml`（dispatch + plan hash）から実行できる。

```
npm run ops-write:plan -- --operation kdp.publish --args '{"id":"<id>"}'
# hash を確認 → 内容確認 → 人が Kindle Previewer で目視承認済みであること →
gh workflow run ops-write.yml --ref develop -f operation=kdp.publish -f args='{"id":"<id>"}' -f plan_sha256=<hash> -f commit=true
```

不可逆（審査へ提出）のため、`commit=true` を叩く前の目視承認は省略しない。真実源 `.claude/config/ci-write-operations.json` / `scripts/lib/ci-write-gate.mjs`。

## 前提

> [!caution] アカウントの「本の作成数制限」で新規提出が丸ごと止まる（2026-07-30 実測）
> 詳細記入・カテゴリー選択まで正常に進んだ後、ページ2へ遷移する所でモーダルが出て止まる:
> **「本の作成数制限を超えました / このアカウントで提出可能な本の数を超えています。」**
> スクリプトは `ABORT: ページ2へ遷移できず` で終わる（exit 3）。この時点では**本は作成されない**
> ——catalog の `draftAsin` も未記録、本棚にも現れないので、状態は汚れず再実行は安全。
>
> ログの `エラー:` 行には静的な注意書き（「タイトルとサブタイトルは合わせて 200 文字以内」等）が
> 大量に混ざるので**文字列だけ読むと誤診する**。`.tmp/kdp-<id>-03-content-fail.png` を必ず見る。
>
> **回復までの見積りは「数日」ではない**（実測）。2026-07-27 に 10 冊目で到達し、**3 日後の 07-30 に
> 1 冊だけ試しても同じモーダルで弾かれた**。日次リセット型ではない。提出日の実績と推定は
> 戦略ドキュメント [strategy.md](../../../../content/kindle/strategy.md)「提出ペースと作成数制限」を参照。

- **ローカル限定・ログイン済みプロファイル**: 初回のみ人が手動ログイン（CAPTCHA/2FA も人）。以降 `<auth root>/profiles/playwright-kdp-profile` にセッション保持で無人。未ログインなら script が最大2分待つ。
- **EPUB/表紙が Downloads にある**: `npm run sync-kindle-dist -- --downloads <id>` で配置。
- **メタデータ登録済み**: `config/kdp-memo.json` books[id] が必要。未登録（C系/F系/e-02）は kdp-operator ケース2 で先に生成。

## ケース別手順

### 新規提出（下書きまで・出版しない）
```
node scripts/kdp-publish.mjs --id <id>
```
→ 詳細→カテゴリー→原稿/表紙アップロード→**原稿処理完了まで待機**→AI申告→アクセシビリティ→価格→下書き保存。
`.tmp/kdp-<id>-checklist.txt` を出力。発番したドラフト ASIN は catalog.json の `draftAsin` に自動記録（再実行で重複作成しない）。

### 出版（不可逆・承認後）
```
node scripts/kdp-publish.mjs --id <id> --publish-only --commit-publish
```
→ draftAsin の価格ページへ直行して「Kindle本を出版」。価格/ロイヤリティが期待値と不一致なら出版せず停止。

> **`--publish-only` を付ける**（2026-07-27 の実運用で確立）。`--commit-publish` 単独は
> **全フローを最初からやり直す**ため約1分では終わらない。`--publish-only` は詳細/カテゴリーに
> 触れず価格ページへ直行する。
>
> 全フローのやり直し自体は 2026-08-03 に通るようにした（下記「途中で落ちた本の再開」）。

> **実行の間に Chrome を止めてプロファイルを正常化する**（必須）。下書き直後に出版を走らせると
> 前段の Chrome とプロファイルが競合し、**エラーも出さず無言でハングする**（2026-07-27 に3回発生。
> 症状＝node は生きているが CPU がほぼ増えず、ブラウザプロセスが 0、スクショも更新されない）。
> さらにハングを `kill -9` すると `Default/Preferences` の `exit_type` が `Crashed` になり、
> 次回起動時に復元ダイアログでまたハングする。手順は `scripts/kdp-batch.mjs` の `cleanProfile()`
> （プロセス kill → `Default/Preferences` の `exit_type` を `Normal` へ戻す → `Singleton*` 削除）。

### 途中で落ちた本の再開（2026-08-03 に修復）

同じ `node scripts/kdp-publish.mjs --id <id>` を再実行すれば、catalog の `draftAsin` から既存ドラフトへ
入り直す。**重複作成はしない**。以前は再開すると必ず途中で落ちていた 2 点を修正済み:

| 症状 | 実体 | 対処（実装済み） |
|---|---|---|
| `[cat] L0 "Kindle本" 選択失敗。候補: ` → ABORT | 保存済みドラフトはカテゴリー modal のカウンタではなく **「本の現在のカテゴリー › <末端>」** 表示になる。旧コードは前者しか見ずカテゴリー未設定と誤判定していた | 後者も読み、期待する末端（`categoryLeaf`）と一致すれば skip。**不一致なら従来どおり ABORT**（ドリフト検知） |
| 表紙だけ無言で落ち、価格ページへ進めず ABORT | 原稿と同時に投げると表紙側 AJAX だけ失敗することがある。旧コードは表紙を**一切検証していなかった** | 「表紙のアップロードに成功しました」＋サムネイル実在を実査し、未達なら最大 3 回まで再アップロード。3 回失敗で ABORT |

> [!caution] 表紙の成功文言は原稿と違う
> 原稿＝「原稿 (xxx.epub) を**正常にアップロード**しました」／表紙＝「表紙の**アップロードに成功**しました」。
> さらに KDP は成功・失敗の全メッセージを**非表示テンプレとして DOM に常駐**させるので、HTML 全文を
> 検索すると常に両方ヒットする。判定は必ず `innerText`（可視分のみ）で行う。2026-08-03 に
> 「正常にアップロード」で表紙を判定して**偽の ABORT** を出した。

### 一括提出（複数冊）

```
npm run kdp-batch -- f-10 f-11 f-12          # 下書き→出版（不可逆）
npm run kdp-batch -- --draft-only f-10       # 下書きまで
```

`scripts/kdp-batch.mjs` が「配置 → 下書き → プロファイル掃除 → 出版 → catalog 更新」を
1冊あたり約3.5分で回し、異常時は即中断する（2026-07-27 に10冊を無人処理した実績）。
提出済み（`in_review`/`live`）の id は SKIP、作成数制限に当たったら残りに触れず exit 2。

> [!note] zsh 版は 2026-08-03 に退役
> 旧 `scripts/kdp-batch.sh` は `zsh` と `pgrep` に依存し、**Windows では 1 行も動かなかった**
> （Git Bash に `pgrep` が無い）。同じ役割が 2 つあると環境ごとに別物を保守することになるため
> `.mjs` に一本化した。プロセス掃除だけ `win32`=PowerShell / それ以外=`pkill` で分岐する。

**KDP 新規/実績浅アカウントは本の作成数制限あり**（過去 d-03 提出時、2026-07-27 に f-08 で到達）。
到達すると詳細ページで **モーダル「本の作成数制限を超えました／このアカウントで提出可能な本の数を
超えています」** が出て「保存して続行」が効かず、script は `ABORT: ページ2へ遷移できず` で止まる。
**この ABORT のログには 200 字制限などページ常設のヒント文も一緒に列挙されるので、文言だけで
原因を判断せず `.tmp/kdp-<id>-03-content-fail.png` を必ず見る**（2026-07-27 に文字数超過と誤診した）。
回復後に残りの id を `kdp-batch` へ渡して再開する。**「数日で回復」は誤り**——2026-07-27 の到達後、
3 日経った 07-30 に 1 冊だけ試しても弾かれた（実測）。回復判定は推測せず、1 冊だけ提出を試して
確かめる（制限に当たっても**本は作成されない**ので状態は汚れない）。まとめて出さず分割する。
提出日の実績と上限の推定 → [strategy.md](../../../../content/kindle/strategy.md)「提出ペースと作成数制限」。

### 状態同期（LIVE 化の記録・重複突合）
```
node scripts/kdp-publish.mjs --sync-status   # .tmp/kdp-sync-status.json
```
→ kdp-operator が catalog と突合し、in_review→live 遷移・新規 ASIN を catalog/08戦略doc/README の3箇所へ。

**catalog 駆動のタイトル検索**で各冊を本棚に問う方式（2026-07-30 に列挙方式から置換）。本棚の列挙は
ページネーションで先頭10冊しか DOM に無く、`title-setup/kindle/` の ID も 13〜14 桁の内部ID（例
`YJ0R3ZX4TJV`）で ASIN ではないため、live 33 冊の口座で 10 件しか拾えず半分が著者ID様のゴミだった。
検索なら本棚の総数にもページ送りにも左右されない。

自己検証つき: catalog に ASIN がある本を1件も再現できなければ **exit 1（検査不成立）**。
`found:false` を「本棚に無い」の証拠として使ってよいのは exit 0 のときだけ。

**ライブ価格も突合する**（2026-08-03 追加）。本棚行の `¥価格` を `livePriceJpy` として持ち帰り、
`catalog.priceJpy` と比べて `PRICE DRIFT <id>: live ¥X ≠ catalog ¥Y` を出す。**KDP UI で手動改定
すると catalog/spec と割れるが、これまで検知手段が無かった**——初回実行で 7 冊（A-01〜A-06・d-01）の
ドリフトが出た。突合できた件数と比較不能件数も併記する（未提出の本は live 価格が無いので比較不能）。

> [!caution] 出版直後の「レビュー中」は ASIN がまだ無い
> 行の抽出条件を「ASIN あり or 下書き」にすると、**レビュー中の本が丸ごと消えて `found:false`**
> になる。これを「本棚に無い」と読むと重複作成に直結する（2026-08-03 に f-09 で実測。ブラウザで
> 本棚を見てレビュー中・¥990・ASIN なしを確認した）。状態語（販売中/レビュー中/出版準備中/下書き等）
> も行の根拠に含める。

### 既刊の価格改定
```
node scripts/kdp-publish.mjs --id <id> --set-price            # dry-run（AI申告の要否・現在価格・目標価格で入れた場合の日本の実効レートを表示。保存しない）
node scripts/kdp-publish.mjs --id <id> --set-price --commit   # 保存（公開価格が変わる）
```
価格の真実源は `scripts/kindle-specs/<id>.json` の `price`（spec の無い A 系は catalog の `priceJpy`）。**spec だけ直して実行**すれば、成功時に catalog の `priceJpy` と `priceHistory` をスクリプトが書き戻す。片側だけ直った状態は `npm run check-kindle-prices`（CI ゲート）が止める。宛先は catalog の `draftAsin`（title-setup の内部ID）で、欠けていれば `--sync-status` が本棚から補完する。

- **AI 申告**: KDP が必須化した。未回答の既刊（2026-07 提出分など）は出版が「この項目は必須です」で弾かれるため、`--commit` 時にコンテンツページで config の `aiDeclaration` を入れて下書き保存してから価格へ進む。回答済みの本は書き換えない。
- **印税率**: 70% 帯は **¥250〜¥1,650**（2026-09-23 に KDP 価格ページの告知で ¥1,250 から拡大を確認）。日本・インド・ブラジル・メキシコの 70% は KDP セレクト登録が条件で、未登録だとプランのラジオが 70% のままでも日本は 35% になる。`catalog.royalty` は**日本の実効レート**を表し、価格入力後の日本の行のレートが一致しないと保存せずに止まる（2026-09-23 d-00/d-03 で実測）。
- **成功判定**: 出版ボタン押下後に価格ページを離れ（本棚 `?publishedId=` へ遷移）、エラー表示が無いこと。本文の文言では判定しない（旧判定は「下書きとして保存」の「保存」に一致して失敗を成功と誤報した）。失敗時はエラー文・該当欄・全体スクショ（`.tmp/kdp-<id>-price-fail-full.png`）を出して exit 4。
- **一緒に公開されるもの**: 保存済みで未出版の変更（原稿差し替えの下書き等）も同時に出版される。`--sync-status` が「未出版の変更あり」を一覧にするので、中身を把握してから実行する。

保存直後の本は「変更事項のレビュー中」になり **pricing ページが本棚へリダイレクトされる**。同じ `--set-price` で読み直しても検証できないので、**本棚の表示価格**（`--sync-status` の価格突合）で確かめる。反映は最大 72h。

### ドラフト削除（テスト残骸）
```
node scripts/kdp-publish.mjs --list-drafts               # 本棚確認
node scripts/kdp-publish.mjs --delete-drafts <ASIN>      # 下書きのみ・下書き assert
```

### カテゴリー末端の較正（新しい系統で verified:false のとき）
```
node scripts/kdp-publish.mjs --diag-category --asin <既存draft ASIN>
```
→ カスケード最深 select の候補（=「場所」チェックボックスの選択肢）を実測。`books[id].kdp.categoryLeaf` に設定。

### 既刊の原稿・表紙の差し替え
```
node scripts/kdp-publish.mjs --id <id> --update-manuscript [--commit]                 # 原稿(EPUB)だけ・下書き保存まで
node scripts/kdp-publish.mjs --id <id> --update-cover [--commit [--commit-publish]]    # 表紙だけ・既定 scripts/kindle-dist/<id>.jpg
```

**上げた版の記録（2026-09-29）**: 新規の下書き保存・出版・原稿の差し替え・表紙の差し替えが成功すると、上げた EPUB・表紙の sha256 と日時を `catalog.json` の各冊の `uploaded` に書く（`scripts/lib/kindle-uploaded.mjs`）。管理画面のコンテンツ台帳（`/content/ledger?c=kindle`）は、手元でビルドしてある版とこの記録を比べて「本文（EPUB）・画像（表紙）」の済・ずれを出す。KDP の公開ページは機械で照合しないので、ずれ＝「手元を直したがまだ入稿していない」の意味。公開中・審査中の48冊は 2026-09-29 の手元の版を上げた版とみなして記録した（`via: baseline`）。
両モードとも catalog の live＋ASIN、本棚の「販売中」行、コンテンツページのタイトル/ASIN を照合してから触る（details/pricing は触らない。表紙の再出版だけ pricing で価格一致を確かめて出版ボタンを押す）。修正版は**既存差し替え**（新規作成禁止・[[kindle-dup-prevention]]）。編集ページは Amazon の再認証（/ap/signin）を挟むことがあり、パスワードは人がブラウザで入れる。

## kdp-operator への委譲

高レベル指示（「c-01 を提出」「未登録本のメタ生成」「LIVE 化を記録」「重複確認」）は `kdp-operator`
（Orchestrator・sonnet）へ。出版・削除は同エージェントの安全弁（承認 gate・下書き assert）配下で実行。

## 検証

- **原稿処理**: script は「ファイルの処理が完了しました。原稿チェックが完了しました」まで待つ（表紙の「正常にアップロード」で早期完了と誤認しない）。「処理中に問題」検知で即 fail。
- **出版後**: 「おめでとう／レビュー中／提出されました」文言を確認して初めて成功報告。
- **提出後**: `--sync-status` で本棚実体と catalog を突合。

## トラブルシューティング

| 症状 | 原因/対処 |
|---|---|
| 「ファイルの処理中に問題が見つかりました」 | EPUB に **.svg 拡張子の JPEG** が混入（KDP が拡張子で SVG 解析→失敗・epubcheck は通る）。`build-pe1-kindle.mjs` は修正済（`.svg`→`.jpg` 正規化）。`unzip -l <epub> \| grep -c .svg` が 0 か確認し 0 でなければ再ビルド（[[kdp-svg-named-jpeg-bug]]） |
| カテゴリーが「本のカテゴリーを追加します」で進めない | 末端は4つ目のドロップダウンでなく**「場所」パネルのチェックボックス**。技術士系=工学・技術・環境▸☑技術士。A/E系は `--diag-category` で確認 |
| AI申告で「画像の作成に使用したAIツールを指定します」 | 画像=AI生成 を選ぶとツール名が必須。config `defaults.aiDeclaration.imageTool` を記入（表紙背景の生成元） |
| 価格ページへ進めない | AI申告未完 or アクセシビリティ未回答。新規アップロード時は affirmation チェックボックスも必要（script が自動チェック） |
| 連続実行で Chrome がハング | 永続プロファイルのロック競合。`<auth root>/profiles/playwright-kdp-profile/Singleton*` を削除し1プロセスずつ実行 |

## 参照

- `scripts/kdp-publish.mjs` — 入稿・出版パブリッシャ
- `scripts/lib/kdp-common.mjs` — SSOT 読取り・defaults/override・検証
- `.claude/agents/kdp-operator.md` — 運用オーケストレーター（本スキルの委譲先）
- `config/kdp-memo.json` — KDP 入稿 SSOT
- `scripts/kindle-published/catalog.json` — 全書籍レジストリ
- [/kindle-build](../kindle-build/SKILL.md) — 前工程（EPUB 生成）
- [strategy.md](../../../../content/kindle/strategy.md) — 出版戦略・出版済み一覧
