---
name: searching-library-reference
description: Context7 API を利用して外部ライブラリのAPIドキュメントとコードスニペットを検索・取得します。
---

# ライブラリ API 検索スキル

Context7 API を利用し、プロジェクトで使用しているバージョンに対応したドキュメントとコードスニペットを検索・取得します。

## ワークフロー

進捗に合わせてチェックを入れてください：
ステップ1、2は並列で実行します。
ステップ1、2がどちらも成功したらステップ3、4を並列で実行します。


```
ライブラリAPI検索の進捗:
- [ ] ステップ1: 対象のライブラリのバージョンを取得する
- [ ] ステップ2: ドキュメントを利用可能なライブラリを検索
- [ ] ステップ3: 対象のライブラリのスニペットを取得する
- [ ] ステップ4: 対象のライブラリのドキュメントを取得する
```

### ステップ1: 対象のライブラリのバージョンを取得する

#### プロンプトとしてバージョンが指定されている場合

 バージョンが明示されていればそのバージョンを採用する

#### プロンプトとしてバージョンが指定されていない場合

パッケージマネージャーの設定ファイルからバージョンを取得する

eg: 16.1.0

- package.json
- pnpm-workspace.yaml

#### バージョンが取得できなかった場合

「バージョンが取得できなかったため、ドキュメントの取得ができませんでした」と出力し処理を終了する

### ステップ2: ドキュメントを利用可能なライブラリを検索する

ライブラリの検索 API を使用し、ライブラリを検索します。
レスポンスからマッチするライブラリの id（/owner/repo）と versions を取得します。

```sh
curl "https://context7.com/api/v2/search?query=ライブラリ名" -H "Authorization: Bearer ${CONTEXT7_API_KEY}"
```
eg: curl "https://context7.com/api/v2/search?query=next.js" -H "Authorization: Bearer ${CONTEXT7_API_KEY}"

#### エラーハンドリング

- **ライブラリが見つからない場合**: 「指定されたライブラリ '{ライブラリ名}' は Context7 に登録されていません」と出力し処理を終了する
- **API エラーの場合**: エラー内容を出力し、1回リトライする。リトライも失敗した場合は処理を終了する

### ステップ3: 対象のライブラリのスニペットを取得する

スニペットの取得 API を用いてスニペットを取得します。
ステップ2で取得した id と versions をもとリクエストを行います。
versions は以下の優先順位でマッチングする：
1. 完全一致（例: v16.1.0 = v16.1.0）
2. 同一 major.minor で最新 patch（例: v16.1.x）
3. 同一 major で最新 minor（例: v16.x.x）
4. 利用可能な最新版（フォールバック）

調べたいトピックの数だけリクエストを行います

```sh
curl "https://context7.com/api/v2/docs/code/owner/repo/version?topic=keyword" -H "Authorization: Bearer ${CONTEXT7_API_KEY}"
```

eg: curl "https://context7.com/api/v2/docs/code/vercel/next.js/v16.1.0?topic=Link" -H "Authorization: Bearer ${CONTEXT7_API_KEY}"

#### エラーハンドリング

- **スニペットが見つからない場合**: ステップ4のドキュメント取得結果のみを返す（スニペットなしで続行）
- **API エラーの場合**: エラー内容を出力し、1回リトライする。リトライも失敗した場合はスニペットなしで続行

### ステップ4: 対象のライブラリのドキュメントを取得する

ドキュメントの取得 API を用いて調べたいトピックのドキュメントを取得します。
ステップ2で取得した id と、ステップ3と同じバージョンを使用してリクエストを行います。
調べたいトピックの数だけリクエストを行います

```sh
curl "https://context7.com/api/v2/docs/info/owner/repo/version?topic=keyword" -H "Authorization: Bearer ${CONTEXT7_API_KEY}"
```

eg: curl "https://context7.com/api/v2/docs/info/vercel/next.js/v16.1.0?topic=Link" -H "Authorization: Bearer ${CONTEXT7_API_KEY}"

#### エラーハンドリング

- **ドキュメントが見つからない場合**: ステップ3のスニペット取得結果のみを返す（ドキュメントなしで続行）
- **API エラーの場合**: エラー内容を出力し、1回リトライする。リトライも失敗した場合はドキュメントなしで続行
- **ステップ3,4両方失敗した場合**: 「ライブラリ '{ライブラリ名}' の情報を取得できませんでした」と出力し処理を終了する

