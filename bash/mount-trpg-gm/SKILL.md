---
name: mount-trpg-gm
description: 將本機 trpg-gm Pi package（Skill + Guard Extension）安裝到共用的全域 Pi 設定，讓 Piweb 與 Piscord 都能載入。當使用者說「掛上 TRPG extension」、「安裝 TRPG skill 給 Piweb/Piscord」、「找不到 trpg-gm」或要求修復 TRPG package discovery 時使用。
compatibility: Requires Bash, Python 3, Pi CLI, and the local /home/chihmin/src/trpg-gm-skill checkout.
---

# Mount TRPG GM for Piweb and Piscord

Piweb worker 與 Piscord gateway 都以 `HOME=/home/chihmin` 啟動，而且每則訊息都會 spawn 新的 Pi process。兩者共用 `~/.pi/agent/settings.json`，因此只安裝一次全域 Pi package；不要複製 Skill、不要建立兩份 checkout，也不要修改兩個服務的 mount。

## 執行

```bash
bash ~/.pi/agent/skills/mount-trpg-gm/scripts/mount.sh
```

腳本會：

1. 驗證 `/home/chihmin/src/trpg-gm-skill` 包含 `package.json`、`SKILL.md` 與 Guard Extension。
2. 執行全域 `pi install /home/chihmin/src/trpg-gm-skill`；重複執行仍保持單一 package entry。
3. 用 `pi list` 驗證 package 已解析至完整 checkout。
4. 顯示 `pi-discord-gateway.service` 與 `piweb-worker.service` 狀態。
5. **不重啟服務**，避免中斷目前正在執行這個 Skill 的 Discord/Piweb 回覆；下一則訊息啟動的新 Pi process 就會讀到 package。

若 checkout 位於不同路徑，可明確覆寫：

```bash
TRPG_GM_REPO=/absolute/path/to/trpg-gm-skill \
  bash ~/.pi/agent/skills/mount-trpg-gm/scripts/mount.sh
```

## 完成後驗證

向 Piscord 或 Piweb 發送一則**新的訊息**：

```text
請使用 trpg-gm skill，開一個新團。
```

不要把 `/trpg-gm` 當成 Discord slash command；Piscord 沒有註冊這個 command。Pi TUI 才使用：

```text
/skill:trpg-gm
```

若下一則訊息仍找不到，先執行腳本測試並回報輸出，不要直接重啟或重裝所有 Pi 服務：

```bash
bash ~/.pi/agent/skills/mount-trpg-gm/tests/run-tests.sh
```
