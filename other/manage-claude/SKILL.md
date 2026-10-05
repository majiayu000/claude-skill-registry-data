---
name: manage-claude
description: Manage and monitor the Claude Code agent running in the a-claude tmux session.
---

# manage-claude Skill

`tmux` セッション `a-claude` で稼働している Claude Code エージェントを管理・操作するためのスキルです。

## 出来ること

- **ステータス確認**: `claude-latest-status` スキルを活用し、現在のタスク実行状況を把握する
- **メッセージ送信**: `tmux send-keys` を使用して、Claude に指示や情報を送信する
- **レスポンス回収**: `tmux capture-pane` を使用して、Claude の思考結果や返答を読み取る
- **モーダル管理**: `/usage` 等のモーダル画面から `Escape` を送信して復帰させる

## 利用枠（Usage）の確認

- **コマンド**: `/usage` を送信する。
- **挙動**: **モーダル（Modal）**。全画面またはサブウィンドウで利用状況が表示され、プロンプトが一時的に消える。
- **注意点**: 表示後に **必ず `Escape` キーを送信** してモーダルを抜けなければならない（抜けない限り、後続のプロンプト入力が受け付けられない）。

## 管理対象

- **tmux session**: `a-claude`
- **Session files**: `~/.claude/projects/**/*.jsonl`

## 推奨ワークフロー

1. `claude-latest-status` で現在の状態を確認する
2. 必要に応じて `tmux capture-pane` で詳細な画面出力を確認する
3. `tmux send-keys` でメッセージを送信する際、モーダル状態（`Esc to cancel` 等）であれば `Escape` を先に送信し、**一拍（1〜3秒）置いてから** `Enter` を送る（ペースト直後の `Enter` はコマンド実行ではなく単なる改行として扱われる罠があるため）
4. 作業が完了（または入力待ち）になるまで `claude-latest-status` で監視を続ける
