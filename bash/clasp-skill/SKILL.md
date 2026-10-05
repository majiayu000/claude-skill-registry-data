---
name: clasp
description: "GASデプロイ。clasp push / deploy / clone / create / logs。GASプロジェクトの初期化・プッシュ・Webアプリ/ライブラリデプロイ・ログ取得。Google Apps Script deployment via clasp: push, deploy web app / library, rollback, logs."
---

# Clasp（GAS プロジェクト管理）

Google Apps Script を CLI から操作するスキル。

## リファレンス索引

用途に応じて該当ファイルを Read する。

| やりたいこと | 参照先 |
|---|---|
| **コードをプッシュしたい** | このファイル「push フロー」節（下） |
| 初めて使う・インストール・`clasp login` | `references/setup.md` |
| GASプロジェクトと接続する（初回接続・ケースA/B 判定） | `references/init.md` |
| Web エディタの変更を取り込む（`clasp pull`・日常同期） | `references/pull.md` |
| マルチ環境（開発/リリース）の配布版 push | `references/deploy-dist.md` |
| デプロイ・ロールバック・バージョン戻し（ライブラリ・ウェブアプリ） | `references/deploy.md` |
| GAS ウェブアプリの iframe 問題・画像表示 | `references/webapp.md` |
| `clasp logs` で実行ログを取得 | `references/logs.md` |

---

## push フロー（最頻出）

### 前提
- `.clasp.json` が存在すること
- `clasp` がインストールされていること

### 1. `appsscript.json` の確認・作成

なければ作成。既存ならスコープの過不足をチェック。

```json
{
  "timeZone": "Asia/Tokyo",
  "dependencies": {},
  "exceptionLogging": "STACKDRIVER",
  "runtimeVersion": "V8",
  "oauthScopes": [
    "https://www.googleapis.com/auth/spreadsheets"
  ]
}
```

**プロジェクトに必要なスコープのみ追加する。** 実際には `https://www.googleapis.com/auth/` プレフィックスを付ける。

**よく使う権限一覧:**
| 権限 | 用途 |
|------|------|
| `gmail.readonly` | Gmail の読み取り |
| `gmail.send` | メール送信 |
| `drive` | Google Drive 操作 |
| `documents` | Google Docs 操作 |
| `spreadsheets` | スプレッドシート操作 |
| `forms` | Google Forms の作成・編集 |
| `calendar` | Google Calendar 操作 |
| `script.scriptapp` | トリガー設定 |
| `script.external_request` | UrlFetchApp（外部 API 呼び出し） |
| `script.container.ui` | UI ダイアログ・サイドバー表示 |

### 2. `.clasp.json` の確認

```bash
ls .clasp*.json
```

**複数ファイルがある場合（例: `.clasp.dev.json`, `.clasp.prod.json`）:**
- ユーザーにどの環境へ push するか確認する
- 一時的に選択された設定ファイルを `.clasp.json` にコピーし、push 後に元へ戻す
- `.clasp.json` を永続的に切り替える場合は、その意図をユーザーに確認してから行う

```bash
CLASP_BAK=".clasp.json.bak.$(date +%Y%m%d%H%M%S)"
node -e "const fs=require('fs');fs.existsSync('.clasp.json')&&fs.copyFileSync('.clasp.json',process.argv[1])" "$CLASP_BAK"
printf '%s\n' "$CLASP_BAK" > .clasp.json.bak-path
node -e "const fs=require('fs');fs.copyFileSync(process.argv[1],'.clasp.json')" ".clasp.<env>.json"
```

### 2.5. `.claspignore` の確認（push 対象の除外）

`.claspignore` は push 対象から外すファイルを指定する（`.gitignore` と似た書式）。

**`.claspignore` が無い場合のデフォルト挙動（clasp 3.x）**: いったん全ファイルを無視し、
`rootDir` 配下の `appsscript.json` / `.gs` / `.js` / `.ts` / `.html` だけを push 対象にする。
さらに `.git/**` と `node_modules/**` は常に除外される。
→ つまり**素の JS/HTML プロジェクトなら無くても実害は出にくい**が、対象を明示したい場合は作る。

典型例（ドキュメント・テストを push しない）:

```
*.md
node_modules/**
tests/**
```

push 対象の事前確認は `clasp show-file-status`（旧 alias: `clasp status`）。

### 3. `clasp push` 実行

**重要: Git Bash では clasp の出力がキャプチャされない問題があるため、必ず Node.js 経由で実行すること。**

```bash
run_clasp_push() {
  local push_status=0
  local restore_status=0

  node -e "const{execSync}=require('child_process');try{execSync('clasp push --force',{stdio:'inherit'})}catch(e){process.exit(e.status||1)}" || push_status=$?

  # 複数環境のため一時切替した場合だけ、push 後に .clasp.json を復元
  node -e "const fs=require('fs');let bak=process.argv[1];const marker='.clasp.json.bak-path';if(!bak&&fs.existsSync(marker)){bak=fs.readFileSync(marker,'utf8').trim()}if(bak&&fs.existsSync(bak)){fs.copyFileSync(bak,'.clasp.json');fs.unlinkSync(bak)}if(fs.existsSync(marker)){fs.unlinkSync(marker)}" "${CLASP_BAK:-}" || restore_status=$?

  [ "$restore_status" -eq 0 ] || { echo "failed to restore .clasp.json" >&2; return "$restore_status"; }
  [ "$push_status" -eq 0 ] || { echo "clasp push failed" >&2; return "$push_status"; }
}

run_clasp_push
```

### 確認ポイント
- 「Pushed X files.」というメッセージが表示されることを確認
- このメッセージが出ない場合は push されていないので、再実行
- エラー時は内容を確認して修正を試みる

### OAuth スコープ不足エラー

新しい GAS API（FormApp, DriveApp 等）を使うコードを追加した場合、`oauthScopes` に対応する権限を追加しないと実行時エラーになる。

```
Exception: 指定された権限では FormApp.create を呼び出すことができません。
必要な権限: https://www.googleapis.com/auth/forms
```

**対処:**
1. `appsscript.json` の `oauthScopes` に不足しているスコープを追加（上記権限一覧を参照）
2. `clasp push` で反映
3. ユーザーが GAS エディタまたはスプレッドシートから関数を実行すると、権限の再承認ダイアログが表示される

### リマインダー（バインドスクリプトのみ）

`clasp push` 成功後、push 先がバインドスクリプト（スプレッドシートに紐づくプロジェクト）の場合、スプレッドシート名を日付付きにリネームするようリマインダーを表示する。

- 開発版: 「📝 開発版スプレッドシートを「{プロジェクト名}_開発版_YYYYMMDD」にリネームしてね！」
- 配布版: バインド先スプレッドシートの誤上書き防止やバージョン識別が必要な運用では、`deploy-dist.sh` テンプレート内のコメント位置に日付付きリネームのリマインダー echo を追加する

---

## デプロイ種別の判定（必須）

**デプロイを依頼されたら、必ず種別を判定してから手順を選ぶ。**

| 種別 | 判定ヒント | 更新手順 |
|------|-----------|---------|
| **ライブラリ** | `doGet`/`doPost` なし | `clasp deploy -i <id>` で CLI 更新可 → `references/deploy.md` |
| **ウェブアプリ** | `doGet`/`doPost` あり | 既存デプロイは CLI 更新可。更新後に既存 URL の動作確認必須 → `references/deploy.md` |

**初回ウェブアプリ作成、実行ユーザー、アクセス権限の変更は GAS UI で行う。** 既存 URL に新しいコードバージョンを反映するだけなら `clasp update-deployment <id>` または `clasp deploy -i <id>` を使えるが、更新後は必ず公開 URL を開いて確認する。
