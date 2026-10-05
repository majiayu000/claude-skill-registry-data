---
name: gkeep
description: Google Keep CLI (個人アカウント対応) を操作してノートの検索・取得・作成を行う。重要な情報の参照や、新規メモの作成に使用する。
---

# Google Keep CLI (Personal) Skill Runbook

## 概要
`gkeep` CLI ツールを使用して、個人用 Google Keep アカウントのノートを操作します。`gogcli` ではアクセスできない個人アカウントのデータを、`gkeepapi` を通じて安全に読み書きします。

## 前提
- 実行コマンド: `gkeep`
- 認証設定: `gkeepapi_credential.json` を利用。
- 特徴: デフォルトで「ピン留めされたノート」を優先的に表示します。

## 基本コマンド

### 1. ノートの一覧取得
```bash
gkeep notes ls              # ピン留めされたノートのみ表示
gkeep notes ls --all        # 全てのノートを表示
gkeep notes ls --json       # JSON形式で出力
```

### 2. ノート内容の取得
ID またはタイトルでノートを特定して取得します。
```bash
gkeep notes get "固定費メモ"
gkeep notes get <note_id> --json
```

### 3. ノートの作成
```bash
gkeep notes create --title "タイトル" --text "本文内容" --label "ラベル名" --pinned
```

### 4. 設定管理
```bash
gkeep config get email
gkeep config set master_key <key>
```

## AI 秘書としての活用シナリオ
- **重要情報の参照:** ユーザーがピン留めしている重要なノートを `gkeep notes get` で取得し、タスクの遂行や質問への回答に役立てる。
- **知識の蓄積:** 調査した結果や重要なログを `gkeep notes create` で Keep に残し、ユーザーの記憶を補助する。

## 運用ルール
- ノートが見つからない場合は、タイトルが正確か、または `--all` で検索範囲を広げることを検討する。
