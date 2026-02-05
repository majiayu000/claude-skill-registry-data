---
name: create-notification-plugin
description: 互動式建立多平台通知插件的完整流程
allowed-tools: AskUserQuestion, Bash
---

# 建立通知插件流程

## 簡介

這個 skill 會引導您建立包含三個作業系統版本的通知插件（Windows、macOS、Linux）。

**重要：你必須嚴格按照以下步驟順序執行，不可跳過任何步驟。**

## 執行步驟

### 1. 收集插件資訊

**第一步：你必須立即使用 AskUserQuestion tool 一次性收集所有必要資訊。**

使用以下格式向用戶詢問：

**必須詢問的問題清單：**

1. **插件 ID**（問題：「請輸入插件 ID（英文識別名稱，例如：mario、my-sound）」）
   - header: "插件 ID"
   - 提供選項建議，但允許用戶自訂

2. **插件名稱**（問題：「請輸入插件顯示名稱（例如：瑪利歐音效、我的音效）」）
   - header: "插件名稱"
   - 提供選項建議，但允許用戶自訂

3. **作者名稱**（問題：「請輸入作者名稱」）
   - header: "作者名稱"
   - 提供選項：預設值 "Lucas Yang" 或自訂

4. **作者 Email**（問題：「請輸入作者 Email」）
   - header: "作者 Email"
   - 提供選項：預設值 "yangchenshin77@gmail.com" 或自訂

5. **notification.wav 音檔路徑**（問題：「請輸入 notification.wav 音檔的完整路徑」）
   - header: "通知音檔"
   - 說明：當 Claude Code 執行結束時播放
   - 提供常見路徑建議或自訂

6. **stop.wav 音檔路徑**（問題：「請輸入 stop.wav 音檔的完整路徑」）
   - header: "停止音檔"
   - 說明：當 Claude Code 被停止時播放
   - 提供常見路徑建議或自訂

**注意：**
- 插件描述已固定為「當 Claude Code 執行結束或停止時，自動播放提示音通知用戶」
- 你必須等待用戶回答所有問題後才能繼續下一步

### 2. 驗證音檔路徑

**第二步：你必須使用 Bash tool 驗證用戶提供的音檔路徑是否存在。**

執行以下命令（將 `{notificationAudioPath}` 和 `{stopAudioPath}` 替換為用戶提供的實際路徑）：

```bash
test -f "{notificationAudioPath}" && echo "✅ Notification audio exists" || echo "❌ Notification audio NOT found"
test -f "{stopAudioPath}" && echo "✅ Stop audio exists" || echo "❌ Stop audio NOT found"
```

**重要檢查點：**
- 如果**任何一個**音檔不存在，你必須：
  1. 停止執行
  2. 向用戶顯示錯誤訊息，明確指出哪個音檔不存在
  3. 請用戶檢查路徑並重新執行 skill
  4. **不可繼續執行後續步驟**

- 只有**兩個音檔都存在**時，才能繼續下一步

### 3. 執行 Node.js 腳本建立插件

**第三步：你必須使用 Bash tool 執行 Node.js 腳本來建立插件。**

**執行命令格式：**

```bash
node scripts/create-notification-plugin.js \
  --id "{id}" \
  --name "{name}" \
  --author-name "{authorName}" \
  --author-email "{authorEmail}" \
  --notification-audio "{notificationAudioPath}" \
  --stop-audio "{stopAudioPath}"
```

**重要說明：**
- 將所有 `{...}` 佔位符替換為步驟 1 收集到的實際值
- 腳本路徑位於 `scripts/create-notification-plugin.js`
- 如果作者名稱或 Email 用戶選擇使用預設值，仍然要傳遞參數
- 必須等待腳本執行完成後才能繼續下一步
- 如果腳本執行失敗，向用戶顯示錯誤訊息並停止執行

### 4. 顯示建立結果

**第四步：解析腳本輸出並向用戶顯示完整的建立結果。**

腳本執行成功後，你必須向用戶清楚地顯示：

1. **已建立的插件目錄**（通常會有三個）：
   - `plugins/{id}-win`
   - `plugins/{id}-mac`
   - `plugins/{id}-linux`

2. **已更新的檔案**：
   - `.claude-plugin/marketplace.json`
   - `README.md`

3. **安裝指令**（提供三個平台的安裝命令）：
   - `/plugin install {id}-win@ycs77-notifications`
   - `/plugin install {id}-mac@ycs77-notifications`
   - `/plugin install {id}-linux@ycs77-notifications`

**顯示格式範例：**

```
✅ 插件建立成功！

已建立的插件：
  - plugins/{id}-win
  - plugins/{id}-mac
  - plugins/{id}-linux

已更新的檔案：
  - .claude-plugin/marketplace.json
  - README.md

安裝指令（根據您的作業系統選擇）：
  Windows: /plugin install {id}-win@ycs77-notifications
  macOS:   /plugin install {id}-mac@ycs77-notifications
  Linux:   /plugin install {id}-linux@ycs77-notifications
```

## 重要提示

**執行限制：**
- 插件 ID 應使用小寫字母和連字符，例如 `my-sound`
- 音檔必須是 WAV 格式
- 腳本會自動更新 `.claude-plugin/marketplace.json` 和 `README.md`
- 如果插件目錄已存在，腳本會自動覆蓋（有警告訊息）

**故障排除：**
- 如果步驟 3 沒有執行，請確認音檔驗證通過
- 如果腳本執行失敗，檢查錯誤訊息並向用戶說明問題
