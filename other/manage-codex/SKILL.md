---
name: manage-codex
description: Manage and monitor the Codex agent running in the a-codex tmux session.
---

# manage-codex Skill

`tmux` セッション `a-codex` で稼働している Codex エージェントを管理・操作するためのスキルです。

## 出来ること

- **ステータス確認**: `codex-latest-status` スキルを活用し、現在のタスク実行状況を把握する
- **メッセージ送信**: `tmux send-keys` を使用して、Codex に指示や情報を送信する
- **レスポンス回収**: `tmux capture-pane` を使用して、Codex の思考結果や返答を読み取る
- **中断・再開**: `Ctrl-C` の送信によるタスクの中断など、実行制御を行う

## 利用枠（Usage/Status）の確認

- **コマンド**: `/status` を送信する。
- **挙動**: **非モーダル（Non-modal）**。実行するとその場にステータスが表示され、即座にプロンプトに戻る。
- **注意点**: 表示後に `Escape` を送る必要はない。そのまま次の指示を送信可能。

## 管理対象

- **tmux session**: `a-codex`
- **Session files**: `~/.codex/sessions/**/*.jsonl`

## 推奨ワークフロー

1. `codex-latest-status` で現在の状態を確認する
2. 必要に応じて `tmux capture-pane` で詳細な画面出力を確認する
3. `tmux send-keys` でメッセージを送信し、**一拍（1〜3秒）置いてから** `Enter` を送る（ペースト直後の `Enter` はコマンド実行ではなく単なる改行として扱われる罠があるため）
4. 作業が完了（または入力待ち）になるまで `codex-latest-status` で監視を続ける
