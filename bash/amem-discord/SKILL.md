---
name: amem-discord
description: "`amem keep` を使った進捗記録時に、`~/.config/yuiclaw/.env` を事前に読み込んで Discord ミラー（`acomm --discord --agent`）を有効化する。必要に応じて `acomm --discord --agent` で直接通知する。"
---

# amem-discord Skill

`amem` 記録と Discord 通知を一体運用するときの手順です。

このリポジトリでは、まず `amem keep` で活動記録を残し、その際に `~/.config/yuiclaw/.env` を読み込むことで Discord ミラーが有効になる前提です（設定済みの場合）。

## 使う場面

- 作業の進捗を `amem` に記録しつつ、Discord にも反映したいとき
- マイルストーン完了を短く通知したいとき
- ユーザーから「amem-discord で報告して」と言われたとき

## 基本手順（推奨）

1. 環境変数を読み込む（Discord ミラー用）
2. `amem keep` で活動記録を追加する

```bash
set -a; source ~/.config/yuiclaw/.env; set +a; amem keep "<what was done>" --kind activity --source <codex|gemini|claude>
```

例:

```bash
set -a; source ~/.config/yuiclaw/.env; set +a; amem keep "remotion-hatebu の台本生成CLIを追加し、genで script.yaml 生成を確認" --kind activity --source codex
```

## 直接 Discord 通知（必要時のみ）

ミラー設定が無い、または `amem` 記録とは別に即時通知したい場合だけ `acomm` を使います。

```bash
set -a; source ~/.config/yuiclaw/.env; set +a; acomm --discord --agent "<short progress message>"
```

例:

```bash
set -a; source ~/.config/yuiclaw/.env; set +a; acomm --discord --agent "remotion-hatebu: hatebu→テーマ分類→掛け合い台本生成まで完了。VOICEVOX起動待ち"
```

## 運用ルール

- まず `amem keep` を優先する（記録が正）
- Discord メッセージは短く、要点だけにする
- API キーや個人情報などの秘匿情報は送らない
- 細かすぎる頻度で連投しない（節目ごと）

## トラブルシュート

- `amem` が無い:
  - `amem` スキルの手順に従い、`/home/yuiseki/Workspaces/repos/amem` の `cargo run -q -- ...` を使う
- Discord に流れない:
  - `set -a; source ~/.config/yuiclaw/.env; set +a` で export しているか確認
  - ミラー設定が未構成なら `acomm --discord --agent` を直接使う
