---
name: acomm-receive
description: >
  acomm ブリッジ経由でお嬢様からのメッセージを受信して標準出力し終了する。
  `acomm --receive` を実行してユーザーの返信を待ち受ける。
  使用場面: acomm-discord や ntfy スキルでお嬢様に問いかけた後、返答を受け取って次の作業に進む場合。
  チャンネル指定: `--discord` `--slack` `--ntfy` で絞り込み可能。
  タイムアウト指定: `--timeout <秒>` で待機上限を設定（超過すると exit 1）。
  受信したメッセージはそのまま stdout に出力されるため、変数に代入して後続処理に使える。
---

# acomm-receive Skill

## 概要

`acomm --receive` は acomm ブリッジに接続し、お嬢様からの最初の入力（`Prompt` イベント）を受け取ったら
その本文を stdout へ出力して即終了する。バックログ（過去メッセージの再送）は自動的にスキップする。

**手動確認フローの典型パターン:**

```bash
# 1. 問いかけを送信
acomm --agent "ビルドエラーが解消できません。作業を継続してよいでしょうか？" --discord

# 2. 返答を受け取る（変数に代入）
response=$(acomm --receive --discord --timeout 120)

# 3. 返答内容に応じて分岐
echo "お嬢様の返答: $response"
```

## 前提条件

- `yuiclaw daemon` が起動中であること（`yuiclaw daemon status` で確認）
- `/tmp/acomm.sock` が存在すること

## コマンド

```bash
acomm --receive [--discord] [--slack] [--ntfy] [--timeout <秒>]
```

| オプション | 説明 |
|---|---|
| `--discord` | Discord チャンネルからの入力のみ受理 |
| `--slack` | Slack チャンネルからの入力のみ受理 |
| `--ntfy` | ntfy チャンネルからの入力のみ受理 |
| `--timeout <秒>` | 指定秒数内に受信できなければ exit 1 で終了 |
| （なし） | 全チャンネルの最初の入力を受理 |

## 終了コード

| コード | 意味 |
|---|---|
| 0 | メッセージ受信成功（stdout にテキストを出力済み） |
| 1 | タイムアウト、またはブリッジ接続エラー |

## 使用例

```bash
# Discord からの返答を待つ（120秒以内）
response=$(acomm --receive --discord --timeout 120)
echo "受信: $response"

# チャンネル指定なし（どこからでも最初のメッセージ）
acomm --receive --timeout 60

# タイムアウトなし（無制限に待機）
acomm --receive --discord
```

## 注意事項

- `--receive` は最初の 1 件を受信した時点で終了する。複数メッセージを処理したい場合は再度呼び出す。
- お嬢様が返答した内容が全文そのまま stdout に出力される（整形・要約なし）。
- ブリッジが起動していない場合は即 exit 1。`yuiclaw daemon start` で事前起動すること。
