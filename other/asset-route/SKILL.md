---
name: asset-route
description: >
  Git の外に置くアセット（画像・PDF・レンダー・原本）の置き場を「誰が使うか」で決め、正確なコマンドへ導く。
  サイトが配信する→public R2 / GitHub Actions が読み書きする→private R2 / 人か手元のスクリプトだけ→Google Drive vault。
  新しいアセット群を追加するとき、既存 group を別 tier へ移すとき、R2 か Drive か迷ったときに使う。
  Use when user asks to [アセットの置き場, R2 か Drive か, 退避先を決める, asset-route, 新しい画像群をどこに置く, group を Drive へ移す].
domain: ops
---

置き場ルールの真実源は [asset-storage-policy.md](../../../knowledge/reference/asset-storage-policy.md) §1。
このスキルは**判断を再現する決定木**と、**その判断に対応するコマンド**だけを持つ。

## 決定木

1. **サイト（`doboku-note.com`）がその実体を配信するか？** — `<img src>`・`og:image`・`_redirects` 301 の先・配布 ZIP の URL
   → **`audience: site`** → public R2 `doboku-note`（`asset-storage.json`、`bucket: public`）。
   記事図版は `r2-sync.yml` が自動同期、OGP は `ogp-supply.yml` が生成・供給する。**手で offload しない**。
2. **GitHub Actions がその実体を読むか書くか？** — `.github/workflows/*.yml` を grep して確かめる（憶測で「CI が使う」と言わない。
   2026-09-05 の調査で、動画レンダー・Kindle・IG 公開のワークフローは**存在しなかった**）
   → **`audience: ci`** → R2（`bucket: private` か `byVisibility`）。現在この区分のグループは無い（2026-09-29 まで note カバー PNG が該当）。
3. **それ以外＝人か手元のスクリプトだけが使う** → **`audience: human`** → Google Drive vault `マイドライブ/doboku-note/`
   （`drive-vault.json`）。原本 PDF・ページ画像・文字起こし・配布 PDF・未投稿レンダー・Kindle・ココナラ素材。
   - R2 に残す例外は `asset-storage.json` の `audienceException` に 20 字以上の理由を書く（例: git 履歴 bundle 2.65GB）。
     理由が書けないなら例外ではない。

「著作権物だから private R2」は判断軸ではない。著作権物でも人しか読まないなら Drive、public に出せないのは両 tier とも同じ。

## 置き場ごとのコマンド

端末間の引き継ぎは、先に [asset-storage-policy.md §1-3](../../../knowledge/reference/asset-storage-policy.md#1-3-端末間引き継ぎの完了条件) の接続・容量・復元確認を行う。マウントが無いだけで転送不能と判断しない。Driveコネクターを利用できる場合は既存フォルダーを特定して個別ファイルを転送し、全バイト読み戻しの記録を `node scripts/drive-connector-register.mjs --receipt <json> [--commit]` で既存台帳へ登録する。ZIPを置いただけの状態と、個別復元可能な状態を区別する。

| audience | 台帳 | 追加・同期 | 取り戻し | 検査 |
|---|---|---|---|---|
| site / ci | `.claude/state/assets/manifest.json` | `node scripts/asset-offload.mjs --group <id> [--include-untracked] --commit` | `npm run asset-hydrate -- --group <id>` | `npm run check-asset-storage` |
| human | `.claude/state/assets/drive-manifest.json` | `npm run drive-vault-sync -- --group <id> --commit` | `npm run drive-vault-sync -- --pull --group <id>` | `npm run check-drive-vault` |

教材文字起こしの既存 group は `source-transcript`（Drive の各原資料内 `ocr/`）。新しい原本は先に
`config/reference-sources.json` へ登録し、文字起こし frontmatter からその ID を指す。詳細は
`.claude/knowledge/reference/reference-sources-policy.md`。

どちらも既定は dry-run。書き込みは `--commit`。**ローカル削除・untrack・R2 側の削除は別操作・別承認**。

## 新しい group を足すとき

1. 決定木で audience を決める。
2. `site` / `ci` なら `asset-storage.json` に `audience` つきで group を追加。`human` なら `drive-vault.json` に
   `status: active`・`vaultDir`（3 フォルダのどれか: 原資料PDF / 制作物 / アーカイブ）・`keyFrom`・`reason` を書く。
3. `npm test`（`tests/asset-storage.test.mjs` / `tests/drive-vault.test.mjs` が audience と衝突を固定）と
   `npm run check-drive-vault`（同じパスが両 tier に一致しないか）を通す。
4. `.gitignore` に実体のパターンを足す（拡張子で書く・台帳と README は除外しない）。
5. `asset-storage-policy.md` §1 の「各 group の行き先」表に 1 行足す。

## 既存 group を R2 から Drive へ移すとき（順序は必須）

```bash
node scripts/drive-vault-sync.mjs --group <id> [--from-r2] [--dedupe-by-sha]            # 1 dry-run
node scripts/drive-vault-sync.mjs --group <id> [--from-r2] [--dedupe-by-sha] --commit   # 2 vault へ（読み直し sha256）
node scripts/drive-vault-sync.mjs --group <id> --verify --deep --cloud --out .tmp/<id>-ok.txt  # 3 台帳・vault・クラウド md5 の 3 者一致
node scripts/delete-r2-objects.mjs --bucket private --from-manifest-group <id> [--commit]      # 4 R2 側を消す（byVisibility は --bucket public も）
node scripts/asset-offload.mjs --forget-group <id> --commit                                    # 5 R2 台帳から外す（Drive 側で保全確認できたキーだけ）
# 6 asset-storage.json から group を削除・drive-vault.json 側を status: active・tests のサンプルを差し替え・docs
```

- **3 を飛ばして 4 へ行かない。** マウントへ書けた＝クラウドへ上がった、ではない（Drive クライアントの同期は非同期）。
  `--cloud` は rclone リモート `doboku-gdrive` が要る（`rclone config` で Google Drive バックエンド・ブラウザ OAuth・人が 1 回）。
  未設定なら fail-closed で止まる。
- `--from-r2` は R2 にしか実体が無い group（教材 PDF 等）向け。R2 台帳のキーで引く（`logicalPath` の旧値は使わない）。
- `--dedupe-by-sha` は vault の `dedupeScan`（原資料PDF/）配下に同じ sha256 があればコピーせず採用（`adopted: true`）。
  手で置いた原本と二重化しない。
- `byVisibility` の group（IG レンダー）は public / private の両バケットにキーがあるので、4 を `--bucket` ごとに 2 回。

## つまずきどころ

- **マウントが無い**: `resolveVaultRoot()` が `{ root: null, reason }` を返す。Google ドライブ アプリを起動するか
  `DOBOKU_DRIVE_VAULT=/path` で指定。CI には無いのが正常（`check-drive-vault` は「実体検査 0 件」と出す）。
- **`stat` のサイズが 16,777,216**: ストリーミングマウントのプレースホルダ。cloud-only のファイルは読むまで実サイズが分からない。
  `realBytesAndHashes()`（読んで測る）を使い、`statSync.size` で比較しない。
- **Windows 会社 PC**: 候補は `G:/マイドライブ/doboku-note`・`%USERPROFILE%/Google Drive/マイドライブ/doboku-note`。
  マウント経由の `drive-vault-sync` はプロキシを使わない。コネクター経由は利用可能な接続と取得機能を確認する。
- **`check-asset-storage` の not-offloaded**: Drive 台帳に載っているか active な Drive group に一致するファイルは数えない。
  出たら R2 tier の未退避＝`asset-offload`。
- **reels の wav/mp4・YouTube Shorts mp4**（`sns-archived-media`）も 2026-09-05（DN-0170）から Drive vault `制作物/SNS音声動画/`
  （旧 `upload-sns-r2`＝public R2 系統は廃止）。パック単位の退避可否は `sns-archive-auditor`（[sns-archive-policy.md](../../../knowledge/reference/sns-archive-policy.md)）。
