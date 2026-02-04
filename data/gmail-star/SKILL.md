---
name: gmail-star
description: Gmail のメッセージをスター化/解除する。「スターを付けて」「スター化」「星を付ける」「スター解除」「星を外す」「Gmail スター」「スターを消す」などで起動。
allowed-tools: [Read, Bash]
---

# Gmail Star

Gmail のメッセージをスター化/解除します。

## 引数

- メッセージID (必須): スター化/解除するメッセージのID

## 実行方法

### スターを付ける

```bash
python plugins/shiiman-google/skills/gmail-list-unread/scripts/google_gmail.py star --ids <message-id>
```

### スターを解除する

```bash
python plugins/shiiman-google/skills/gmail-list-unread/scripts/google_gmail.py unstar --ids <message-id>
```

### 複数メッセージを一括でスター化

```bash
python plugins/shiiman-google/skills/gmail-list-unread/scripts/google_gmail.py star --ids <id1>,<id2>,<id3>
```

### プロファイル指定

```bash
python plugins/shiiman-google/skills/gmail-list-unread/scripts/google_gmail.py star --profile <profile-name> --ids <message-id>
```

## 関連操作

- スター付き一覧を確認: `gmail-list-starred` を実行

## 注意事項

- トークン未作成の場合は「Google ログイン」と言って認証を行ってください
