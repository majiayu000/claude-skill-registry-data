---
name: switchbot
description: ローカルの `switchbot` CLI と SwitchBot OpenAPI を使って、SwitchBot デバイスや Hub Mini 配下の赤外線リモコンを確認・操作する。ユーザーが SwitchBot デバイスの状態確認、ライト操作、家電プリセット実行を依頼したときに使う。
---

# SwitchBot Skill

## 概要
`switchbot` CLI を使って、`~/.config/yuiclaw/.env` に保存された `SWITCHBOT_TOKEN` / `SWITCHBOT_SECRET` で SwitchBot OpenAPI v1.1 を呼び出します。Hub Mini 配下の赤外線リモコン操作もここから扱います。

## 前提
- 実行バイナリ: `switchbot`
- 認証情報: `SWITCHBOT_TOKEN`, `SWITCHBOT_SECRET` が `~/.config/yuiclaw/.env` にあること
- 既存実装: `/home/yuiseki/Workspaces/repos/_cli/switchbotcli`

## 基本コマンド

### デバイス一覧
```bash
switchbot devices
switchbot devices --json
```

### ライト操作
```bash
switchbot lights on
switchbot lights off
switchbot lights on --name "リビングのライト"
```

### 朝のプリセット
```bash
switchbot good-morning
```

## 運用ルール
- 物理デバイスや家電に影響するコマンドは、ユーザーが明示的に求めたときだけ実行する。
- 状態確認だけで足りる場合は、まず `switchbot devices` で現在の登録デバイスを把握する。
- 朝の高レベル意図（例: `おはよう`）は `good-morning` スキルから受け取り、このスキルでは `switchbot good-morning` の実行だけを担当する。
