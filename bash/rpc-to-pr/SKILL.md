---
name: rpc-to-pr
description: Connect RPC をローカルで叩き、curl コマンドとレスポンスを現在ブランチの PR ディスクリプション末尾に追記する。動作確認エビデンスを PR に残したい時に使う。
---

# Connect RPC 動作確認 → PR 追記

## 概要

ローカルで Connect RPC エンドポイントを curl で叩き、結果（curl コマンド + レスポンス JSON）を現在ブランチに紐づく PR の body 末尾に追記するスキル。

RPC を叩くだけで PR への記録が要らないなら `/local-rpc-test` を使う。
そちらはリポジトリごとの接続設定を持ち、トークンも自動発行される。

## 前提

- 現在ブランチが GitHub にプッシュ済みで、紐づく PR が存在すること
- `gh` CLI が認証済みであること
- proto ファイルがプロジェクト内にあること

## 実行手順

### 1. proto ファイルの検索とメソッド選択

`.proto` を Glob 検索（`**/*.proto`）し、`package` 名・`service` 定義・`rpc` メソッド・リクエスト型のフィールド構造を抽出する。
引数でメソッドが指定されていればそれを使い、無ければ一覧を出してユーザーに選んでもらう。

### 2. 接続先の決定

デフォルトは `http://localhost:<port>` で、ポートはプロジェクトの設定（compose, README, `cmd/`）から推定。引数で指定があればそれを使う。

**Note**: 内部運用 RPC など host にポートマッピングされていないケースもある。その場合は `docker exec <container> curl ...` パターンで叩く必要があるため、ホスト直叩きで接続拒否されたら docker exec も試す。プロジェクト固有のアクセス方法は memory を参照。

### 3. トークンの取得

- 環境変数 `RPC_TOKEN` があればそれを使う（curl 内で `$RPC_TOKEN` として参照）
- なければユーザーに JWT トークンの入力を求める
- 認証不要のエンドポイント（内部 RPC 等）はスキップ
- **トークンをファイルに書かない。echo / cat で出さない。**

### 4. リクエストボディの構築

proto のメッセージ定義からフィールドを抽出し、JSON を提示。引数で `'{"key":"value"}'` 形式があればそれを使う。不足はユーザーに聞く。

### 5. curl の実行

```bash
curl -s --location 'HOST/PACKAGE.SERVICE/METHOD' \
  --header 'Content-Type: application/json' \
  --header "Authorization: $RPC_TOKEN" \
  --data 'REQUEST_BODY'
```

レスポンスを `jq` で整形して保存（実行はするが、トークンは表に出さない）。レスポンスサイズが大きい場合は次のステップで方針を確認。

### 6. レスポンスサイズと内容の確認

レスポンスが大きい場合（数十件超 / 数 KB 超）は全件貼らない:

- 件数や主要フィールドのバリエーションを集計してユーザーに提示
- 「全件 / 各バリエーション 1 件ずつの抜粋 / 単一サンプルのみ」のいずれかを選んでもらう
- 個人情報（個人の氏名・email・電話番号等）が含まれる場合はマスク方針を確認（学校名・会社名などの組織名や ID は実データのまま貼ってよい）

### 7. 現在ブランチの PR を検出

```bash
BRANCH=$(git branch --show-current)
gh pr list --head "$BRANCH" --json number,url,title --limit 5
```

- 0 件: 「現在ブランチ `$BRANCH` に紐づく PR が見つかりません。PR 番号を指定してください」とユーザーに確認
- 1 件: そのまま採用、番号を表示して確認
- 複数件: 一覧表示して選択させる

### 8. 既存 body の取得

```bash
gh pr view <number> --json body --jq .body > /tmp/pr-body.md
```

### 9. body 末尾に追記して更新

追記フォーマット（**Authorization ヘッダのトークンは `<TOKEN>` でマスク**）:

````markdown

## RPC 動作確認

```bash
curl -s --location 'HOST/PACKAGE.SERVICE/METHOD' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: <TOKEN>' \
  --data 'REQUEST_BODY'
```

<details>
<summary>レスポンス</summary>

```json
{
  ...
}
```

</details>
````

更新:

```bash
gh pr edit <number> --body-file /tmp/pr-body-updated.md
```

更新後、PR URL を表示する。

### 10. 複数メソッドを連続で確認する場合

2 回目以降は **追記方式**（既存セクションは消さずに `## RPC 動作確認 (2)` のように連番を振る）。複数 RPC を 1 PR で確認するケースを想定。

## 引数の形式

```
/rpc-to-pr                                  → 対話的に選択
/rpc-to-pr SomeMethod                       → メソッド指定
/rpc-to-pr SomeMethod '{"foo":"bar"}'       → メソッド + ボディ
/rpc-to-pr --pr 123 SomeMethod              → PR 番号を明示
```

## 注意事項

- **トークン漏洩防止**: PR body にトークン実値が混入しないこと。`Authorization: <TOKEN>` で必ずマスク。レスポンス JSON にトークン相当のフィールド（access_token 等）が含まれる場合もマスクするか、ユーザーに確認する
- **個人情報マスク**: 学校名・会社名などの組織名や ID は実データのまま貼る（証跡価値を保つ）。個人を特定できる情報（氏名・email・電話番号等）が含まれる場合のみ、一部マスクは半端なので対象フィールドを一括でダミー化する
- `gh pr edit` は body 全置換なので、必ず `gh pr view --json body` で取得した既存 body の末尾に追記する形にすること
- 既に同じセクションが末尾にある場合（再実行など）は連番化（`(2)`, `(3)` ...）して残す
- PR が draft かどうかに関係なく動作する
- プロジェクト固有のアクセス方法（host 非公開 / docker exec / 認証バイパス等）は memory やプロジェクトの CLAUDE.md を参照
