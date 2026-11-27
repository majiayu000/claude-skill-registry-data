---
name: drive-upload
description: ローカルのファイル(PDF・画像など数 MB のバイナリ)を、Google Drive の専用フォルダへパス指定で上げる手順(rclone、drive.file)と、Drive にある既存の大きなファイル(10 MB 超など、コネクタで取れないもの)を取る手順(rclone backend copyid、drive.readonly)。Drive にアップロード・Drive へ上げて・PDF を Drive に置いて・画像を Drive へ・ローカルのファイルを Drive に保存・Drive から取る・Drive からダウンロード・Drive のファイルを読む・10 MB 超のファイル、といった文脈で使う。upload a local file to Google Drive, download a large file from Google Drive, rclone copy to Drive, rclone backend copyid、といった英語の文脈でも使う。claude.ai の Drive コネクタは中身を base64 の文字列で受けるので、数 MB のファイルの書き込みには使わず、`download_file_content` は 10 MB 超を拒否する。
---

claude.ai の Google Drive コネクタ(`create_file`)は、ファイルの中身を `base64Content` / `textContent` の文字列で受け取る。
数 MB の PDF は base64 で数 MB の文字列になり、エージェントが一字も違えずに出力するのは現実的でない(1 文字の誤りで壊れ、気づくのは
Drive で開いたとき)。ローカルのファイルを Drive へ上げるときは、**`rclone` でパスを指定して上げる**。

設計と初回セットアップ(本人の作業)は `docs/gdrive-upload.md`。この手順書は、セットアップ済みのあとの使い方。

## 1. 前提を確かめる

```
rclone listremotes          # gdrive-agent: が出ること
rclone lsd gdrive-agent:    # エラーなく終わること(空でもよい)
```

- `gdrive-agent:` が無ければ、セットアップが済んでいない。`docs/gdrive-upload.md` の初回セットアップを、本人と 1 手順ずつ進める
  (GCP・同意画面・OAuth クライアント・ブラウザ認可は、本人にしかできない)。クライアントシークレットや token を、チャット・Issue・PR に貼らせない。
- `rclone lsd` が認可のエラーを返すときは、refresh token が失効している(Testing のままだと 7 日)。`rclone config reconnect gdrive-agent:` を本人に
  依頼する(ブラウザの認可を伴う)。

## 2. 上げる

```
rclone copy <ローカルのファイル> gdrive-agent:<purpose>/
```

- 書き込み先は、リモートの根(`root_folder_id` で固定した専用フォルダ `rclone/uploads`)の下の `<purpose>/`。`<purpose>` は小文字・ハイフン区切り
  (`docs/cloud-artifacts-and-runbooks.md` §1.2)。フォルダは無ければ作られる。
- **scope は `drive.file` で、rclone が作ったものしか触れない**。Drive の画面で作った既存のフォルダへは直接書けない。「既存のフォルダへ」と
  頼まれたら、専用フォルダへ上げて、本人が Drive の画面で移す運用だと伝える(`drive` のフルスコープへ広げる案は採っていない)。
- 同名のファイルは `copy` が上書きする(中身が同じなら何もしない)。消す操作(`delete`・`purge`・`sync`)は、本人の依頼が無い限り使わない。

## 3. 読み戻して報告する

外部システムへの書き込みは、ツールの戻り値でなく、読み戻した状態だけを報告する(共有 `AGENTS.md`)。

```
rclone lsf --format pi gdrive-agent:<purpose>/     # p=パス i=Drive の ID
rclone md5sum gdrive-agent:<purpose>/<ファイル名>   # ローカルの md5sum と突き合わせる
md5sum <ローカルのファイル>
```

- ローカルと Drive の md5 が一致し、サイズも一致したら、アップロードできたと報告する。一致しない・出てこないときは、そう報告する。
- 報告には、読み戻しに使ったコマンドと、Drive の ID(`i`)を添える。Drive の画面で開く URL は、ID から本人が辿れる(`https://drive.google.com/file/d/<ID>/view`)が、
  共有の設定は変えない(リンク共有・権限の変更は本人の判断)。

## 4. Drive の既存のファイルを取る(読み取り側、#969)

書き込み用の `gdrive-agent`(`drive.file`)は、rclone が作ったファイルしか読めないので、Drive にある既存のファイルには使えない。
既存のファイルを取るには、**読み取り専用の別のリモート `gdrive-read`(`drive.readonly`)**を使う。claude.ai の Drive コネクタの
`download_file_content` は 10 MB 超を拒否し、ブラウザ操作は組織のポリシーで `drive.google.com` を開けないことがある(回避しない)。
そのときの手段がこれである。10 MB 以下で、コネクタで取れるなら、コネクタでよい。

```
rclone listremotes          # gdrive-read: が出ること
rclone backend copyid gdrive-read: <ファイルの ID> <保存先のディレクトリ>/
```

- `gdrive-read:` が無ければ、読み取り側のセットアップが済んでいない。`docs/gdrive-upload.md` の「読み取り側のセットアップ」を、本人と 1 手順ずつ進める
  (ブラウザの認可は本人にしかできない)。
- ファイルの ID は、Drive の URL `https://drive.google.com/file/d/<ID>/view` の `<ID>` か、コネクタの `search_files` / `get_file_metadata` が返す ID。
- 保存先のパスは `/` で終える(ファイル名はそのまま。`/` で終えないと、最後の要素がファイル名になる。`rclone backend help drive` の `copyid`)。
- 取れたら、サイズを Drive のメタデータの `fileSize`(コネクタの `get_file_metadata`)と突き合わせて報告する(`ls -l` か `stat` の値)。一致しない・取れないときは、そう報告する。
- `gdrive-read` は読み取り専用で、書き込みには使わない。リモートを作る手順で、token が会話に出ないようにする(下記と `docs/gdrive-upload.md`)。

## やらないこと

- 書き込み用の `gdrive-agent` を、`drive`・`drive.readonly` など、別の scope で作らない(`drive.file` が、書き先の外への書き込みを許可の範囲で不可能にしている)。
  既存のファイルを読むための `drive.readonly` は、別のリモート `gdrive-read` に分ける(§4)。
- `rclone.conf` を宣言的に生成しない(`programs.rclone` は手書きのリモートと token の更新を壊す)。ファイルをリポジトリに入れない。
- クライアントシークレット・token・`rclone.conf` の中身を、出力しない・貼らない。`rclone config show` と、`--no-output` を付けない
  `rclone config create` は、リモートの設定(access token と refresh token を含む)を標準出力へ書く。本人に頼む手順でも、会話に入る形
  (`!` 付きの実行)では `--no-output` を付ける(#969)。
