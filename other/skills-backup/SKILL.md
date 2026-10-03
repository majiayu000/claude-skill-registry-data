---
name: skills-backup
description: 將 ~/.hermes/skills/ 目錄下的所有技能備份至 GitHub 儲存庫
trigger: 當使用者要求備份技能、同步技能到 GitHub 或在新增重要技能後需要持久化儲存時。
---

# Skills Backup Workflow

此技能用於將本地的 Hermes skills 備份至指定的 GitHub 儲存庫，確保工作流的持久化與跨設備同步。

## 步驟

1. **進入技能目錄**：
   切換至 `~/.hermes/skills/` 目錄。

2. **檢查 Git 狀態**：
   執行 `git status` 確認當前分支與變更情況。

3. **暫存變更**：
   執行 `git add .` 將所有新增、修改或刪除的技能檔案納入暫存區。

4. **提交變更**：
   使用具有描述性的 commit 訊息提交，例如：
   `git commit -m "Backup skills: $(date +'%Y-%m-%d %H:%M:%S')"`

5. **推送至 GitHub**：
   執行 `git push origin main` 將變更推送至遠端儲存庫 `git@github.com:AyaSakura-comp/hermes-skills.git`。

## 注意事項與陷阱

- **SSH 金鑰**：確保執行環境已配置對應的 SSH Key 以便通過 `git@github.com` 進行身份驗證。
- **分支名稱**：預設使用 `main` 分支，若儲存庫使用 `master` 請適時調整。
- **衝突處理**：若遠端有更新，可能需要先執行 `git pull --rebase` 以避免衝突。

## 驗證步驟

- 確認 `git push` 回傳成功訊息。
- (選用) 檢查 GitHub Repo 網頁端確認檔案已更新。