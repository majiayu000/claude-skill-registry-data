---
name: ntfy
description: Send an ntfy push notification to call the user when work reaches a pause point and user confirmation or manual verification is needed.
---

# ntfy Skill

## 概要
調査や作業が一区切りし、お嬢様（ユーザー）による確認や介入が必要な場合に、プッシュ通知を送信して呼び出します。
**このスキルを発動した場合には、必ず調査や作業を一旦停止して、お嬢様（ユーザー）のご指示を待機しなければなりません。**

ただし、`ASEE` が稼働していてお嬢様がカメラに映っている可能性がある場合は、
まず `owner-attention-call` を優先します。`owner-attention-call` は
`/biometric_status` を見て、

- `ownerPresent=true` なら `asay` + `acaption` で音声呼びかけ
- 見えていない、または音声経路失敗なら `ntfy`

へ自動で切り替えます。

## 制約事項 (重要)
- **無料枠での運用**: ntfy.sh の無料枠にはメッセージ送信数の制限があります。
- **濫用の禁止**: 進捗の細かな報告には使用せず、**マイルストーンの完了、重大なエラーの発生、またはお嬢様の直接の判断が不可欠な場合**のみ、慎重に使用してください。

## 使用条件
- 環境変数 `NTFY_TOPIC` が設定されていること。

## 手順
0. `ASEE` が利用可能なら、まず以下を試す。
   ```bash
   python3 /home/yuiseki/Workspaces/.codex/skills/owner-attention-call/scripts/call_owner.py \
     --message "ユイさま、動作確認のお願いがあります"
   ```
   `mode` が `speech` なら、そのまま待機する。`mode` が `ntfy` のときだけ以降の手順へ進む。
1. `.env` ファイルまたはシステム環境変数から `NTFY_TOPIC` を取得する。
2. 以下の `curl` コマンドを使用して通知を送信する。
   ```bash
   curl -d "<通知内容>" ntfy.sh/<NTFY_TOPIC>
   ```
3. 通知内容には、何が終わったのか、何を確認してほしいのかを簡潔に含める。

## 使用例
- 「マイルストーン1の全タスクが完了しました。最終的な動作確認をお願いします ✨️」
- 「解消不可能なビルドエラーが発生しました。設計方針のご相談をさせてください」
- `ASEE` 稼働中なら、まず `owner-attention-call` で「ユイさま、動作確認のお願いがあります」と話しかけ、見えていない場合だけ `ntfy` を送る
