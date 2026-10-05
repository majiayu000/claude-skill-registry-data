---
name: stop-asee-acam
description: ASEE と ACAM の backend / viewer を停止する。ユーザーが「asee, acam 停止」「ASEE を止めて」「ACAM Viewer を止めて」など依頼したときに使う。
---

# stop-asee-acam

`ASEE Viewer` と `ACAM Viewer` は通常 `repos/asee/tmp_main.sh` / `repos/acam/tmp_main.sh` と `tmux` セッションで起動されます。
停止時はまずその経路を使い、孤児化したプロセスだけ fallback で掃除します。

## 実行

通常はこのスクリプトを実行します。

```bash
/home/yuiseki/Workspaces/.codex/skills/stop-asee-acam/scripts/stop_asee_acam.sh
```

## オプション

- `--status-only`: 停止せず、現状だけ表示する
- `--dry-run`: 実行予定コマンドだけ表示する

```bash
/home/yuiseki/Workspaces/.codex/skills/stop-asee-acam/scripts/stop_asee_acam.sh --status-only
```

## 補足

- `DISPLAY` 未指定時は `:0`, `:1`, `:2` を順に probe して使えるものを選ぶ
- `tmp_main.sh stop` で止まり切らない場合に備え、`tmux kill-session` と `pkill` fallback を含む
- 最後に `ps` と `wmctrl` で `ASEE` / `ACAM` の backend / viewer が残っていないことを確認する
