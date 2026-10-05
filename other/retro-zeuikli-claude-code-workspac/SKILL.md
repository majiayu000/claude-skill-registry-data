---
name: retro
description: Session 回顧報告：提取本次對話的關鍵決策、完成事項與改善建議。適合 session 結束前或 /compact 前使用。
disable-model-invocation: true
context: fork
---

# Retro — Session 回顧

## 觸發條件

- Session 即將結束，需要產出可存入 Auto Memory 的摘要
- `/compact` 或 `/clear` 前，確保關鍵決策不遺失
- 週期性審視工作效率（每週一次）

## 摘取原則

**只保留人類可讀的內容**：

- ✅ 使用者的 prompt / 指令
- ✅ Claude 的說明、決策推理、摘要
- ❌ 工具呼叫（Bash 指令、檔案讀寫、搜尋查詢）
- ❌ 工具回傳結果（命令輸出、檔案內容）
- ❌ 系統訊息與 `<system-reminder>` 標籤

## 報告格式（IMRaD 結構）

```markdown
# Session Review — [日期] — [主題/目標]

## Introduction（目標與背景）
- **Goal**: 本次 session 要達成什麼？
- **Context**: 相關背景（專案名稱、任務階段、已知阻塞點）

## Methods（工作方式）
- **Approach**: 達成目標的高層次步驟
- **Tools/Technologies**: 主要用到的工具、語言、框架
- **Workflow Pattern**: 對話流程類型（線性 / 迭代 / 探索 / debug 迴圈）

## Results（產出成果）
- **Completed**:
  - [項目 1]
  - [項目 2]
- **Partially Completed**:
  - [項目 — 剩餘工作]
- **Not Started / Deferred**:
  - [項目 — 原因]

## Discussion

### 效率審查
本次 session 哪裡可以更有效率：
- **[問題]**：[發生什麼] → **建議**：[更好的做法]

### CLAUDE.md 改善建議
本次 session 發現哪些摩擦點應該寫進 CLAUDE.md：
- **新增**：`[建議內容]` — [原因：可以預防什麼摩擦]
- **修改**：`[現有段落]` → `[建議改動]` — [原因]

### 待追蹤項目
- [ ] [下次 session 要繼續的工作]
- [ ] [需要進一步研究的主題]
```

## 執行步驟

1. **掃描本次對話**，過濾掉工具呼叫和工具結果
2. **識別 session 目標**（從最初幾條 user 訊息推斷）
3. **整理完成事項**（實際產出：新增檔案、修復 bug、做的決策）
4. **分析效率**：找出可以批次處理的重複任務、需要多次釐清的模糊 prompt
5. **提出 CLAUDE.md 改善建議**：本次有哪些重複給的指示應該寫進去
6. **用上面的模板產出報告**

## 與 Auto Memory 的整合

回顧報告的「待追蹤項目」和「完成事項」適合用 `/memory` 加入 Auto Memory，確保跨 session 持久化。關鍵決策也應同步更新。

## Gotcha

- 若 session 很短或瑣碎，縮短報告即可，不要強塞每個段落
- CLAUDE.md 建議要具體且可操作，不要寫「增加更多文件」這類空泛建議
- 效率審查應建設性，聚焦在下次可改善的具體模式
