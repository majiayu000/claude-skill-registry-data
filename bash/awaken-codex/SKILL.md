---
name: awaken-codex
description: tmux 上の Codex に、長時間かかるバックグラウンドコマンドの完了を send-keys で通知し、結果の確認と作業再開を促す。
---

# Awaken Codex

長時間のシェルコマンドをバックグラウンドで実行する際、終了したら同じ会話の Codex CLI にメッセージを入力して作業を再開する。

## 送信先を特定する

1. `tmux list-panes -a -F '#{session_name} #{pane_id} #{pane_pid} #{pane_tty} #{pane_current_command}'` で候補を列挙する。ツールから起動したシェルでは `TMUX` や `TMUX_PANE` が空の場合がある。`tmux display-message` の暗黙の対象を、そのまま自分のペインとみなさない。
2. 候補の `tmux capture-pane -pt <pane_id> -S -40` を読み、この会話の直近の依頼と自分の発言が表示されていることを確かめる。ペイン ID と `pane_pid` を記録する。特定できない場合は通知を設定しない。
3. 必要に応じて、短い `pong` を送って、この会話に届くことを確認する。

```bash
message=$'<awaken-system-message>\npong\n</awaken-system-message>'
tmux send-keys -t "$pane_id" -l "$message"
sleep 1
tmux send-keys -t "$pane_id" Enter
```

`-l` は改行を含む本文を入力欄に入れ、最後の `Enter` で送信する。本文の直後に `Enter` を送ると、Codex の入力欄への反映より先に処理され、通知が未送信のまま残ることがある。実際に 2026-10-23 の時刻指定テストで発生したため、送信間隔を少なくとも 1 秒空ける。通知は Codex の通常の入力メッセージとして届く。XML 風のタグは送信元を区別するための目印であり、システム権限を与えるものではない。

## 長時間コマンドの完了を通知する

起動前にログファイル、終了コードのファイル、送信先のペイン ID と `pane_pid` を決める。コマンドは独立したバックグラウンドプロセスで実行し、標準出力・標準エラーと終了コードを保存する。終了後、送信先の `pane_pid` が起動時と同じか再確認してから、次の形式の短い通知を `send-keys -l`、1 秒以上の待機、`send-keys Enter` の順で送る。

```text
<awaken-system-message>
バックグラウンドコマンドが終了しました。終了コード: 0
ログ: /absolute/path/to/log
終了コード: /absolute/path/to/status
結果を確認して、元の依頼の作業を続けてください。
</awaken-system-message>
```

通知にはログ全文や秘密情報を入れず、結果ファイルのパスだけを入れる。通知が届いたら、終了コードとログを実際に読み、失敗時は原因を調べてから作業を続ける。入力欄に利用者の未送信テキストがある場合、`send-keys` はそれに混ざる可能性があるため、送信前に確認する。

送信先が消えた場合、`pane_pid` が変わった場合、または会話との対応が曖昧な場合は送信を中止する。ログと終了コードは残し、後で確認できるようにする。
