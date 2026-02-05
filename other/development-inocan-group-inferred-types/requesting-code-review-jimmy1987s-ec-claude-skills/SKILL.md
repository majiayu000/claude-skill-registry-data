---
name: requesting-code-review
description: 當完成任務、實作主要功能或在合併前驗證工作符合需求時使用
---

# 請求程式碼審查

分派 hi-skills:code-reviewer 子代理以在問題級聯之前捕獲它們。

**核心原則：** 早審查，常審查。

## 何時請求審查

**強制：**
- 子代理驅動開發中每個任務之後
- 完成主要功能之後
- 合併到 main 之前

**可選但有價值：**
- 卡住時（新視角）
- 重構之前（基線檢查）
- 修復複雜錯誤之後

## 如何請求

**1. 獲取 git SHA：**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # 或 origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. 分派 code-reviewer 子代理：**

使用 Task 工具與 hi-skills:code-reviewer 類型，填寫 `code-reviewer.md` 中的模板

**佔位符：**
- `{WHAT_WAS_IMPLEMENTED}` - 你剛建置的內容
- `{PLAN_OR_REQUIREMENTS}` - 它應該做什麼
- `{BASE_SHA}` - 起始提交
- `{HEAD_SHA}` - 結束提交
- `{DESCRIPTION}` - 簡要摘要

**3. 根據反饋行動：**
- 立即修復關鍵問題
- 在繼續之前修復重要問題
- 記下次要問題供稍後處理
- 如果審查者錯了，反駁（附理由）

## 範例

```
[剛完成任務 2：新增驗證函數]

你：讓我在繼續之前請求程式碼審查。

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[分派 hi-skills:code-reviewer 子代理]
  WHAT_WAS_IMPLEMENTED：對話索引的驗證和修復函數
  PLAN_OR_REQUIREMENTS：docs/plans/deployment-plan.md 中的任務 2
  BASE_SHA：a7981ec
  HEAD_SHA：3df7661
  DESCRIPTION：新增 verifyIndex() 和 repairIndex()，包含 4 種問題類型

[子代理返回]：
  優點：乾淨的架構，真實的測試
  問題：
    重要：缺少進度指示器
    次要：魔術數字 (100) 用於報告間隔
  評估：準備好繼續

你：[修復進度指示器]
[繼續任務 3]
```

## 與工作流程整合

**子代理驅動開發：**
- 每個任務之後審查
- 在問題複合之前捕獲它們
- 在移動到下一個任務之前修復

**執行計劃：**
- 每批次（3 個任務）之後審查
- 獲取反饋，應用，繼續

**臨時開發：**
- 合併前審查
- 卡住時審查

## 危險信號

**絕不：**
- 因為"很簡單"而跳過審查
- 忽略關鍵問題
- 在未修復的重要問題下繼續
- 與有效的技術反饋爭論

**如果審查者錯了：**
- 用技術推理反駁
- 展示證明它工作的程式碼/測試
- 請求澄清

參見模板：requesting-code-review/code-reviewer.md
