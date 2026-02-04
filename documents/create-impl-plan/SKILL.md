---
name: create-impl-plan
description: |
  Generate implementation plan and task list from PRD.
  Use when: creating implementation plans, generating task lists, breaking down PRD into actionable tasks.
  Keywords: implementation plan, task list, implementation, PRD breakdown, development planning.
---

# 從 PRD 生成任務清單

## 目標

引導 AI 助手根據現有的產品需求文件（PRD）創建詳細的、逐步的 Markdown 格式任務清單。該任務清單應指導開發人員完成實作。

## 工作流程脈絡

### 整體開發流程

本指令是 claude-code-config 三步驟開發流程中的**第二步：實作規劃**。完整流程如下：

1. **【選用】需求研究 (`/research`)**：深入調查技術問題、探索解決方案、產出研究文件
2. **需求澄清 (`/create-prd`)**：透過問答釐清需求、產出 PRD 文件
3. **【當前】實作規劃 (`/create-impl-plan`)**：分析 PRD 和程式碼庫、產出任務清單和驗收測試
4. **任務執行 (`/process-task-list`)**：逐一實作任務、執行驗收測試

### 當前階段的輸入與輸出

**輸入來源**（至少需要 PRD 或 Research 其中之一）：
- **PRD 文件**：包含功能需求和高層次技術方向（產品導向任務）
- **Research 文件**：包含技術分析和解決方案（技術導向任務）
- 現有程式碼庫（用於了解架構和慣例）

**三種常見流程**：
1. **Research + PRD**：完整流程，前期有深入研究和產品規劃
2. **只有 PRD**：技術明確，直接從產品需求開始
3. **只有 Research**：技術導向任務，從研究結論直接產出實作計畫

**輸出目標**：
- implementation.md（任務清單和實作要點）
- acceptance.feature（Gherkin 格式驗收測試）
- 目標讀者：**開發者（初級到中級）**
- 閱讀目的：理解實作任務、技術細節、驗收標準

### 當前階段的職責範圍

**應該包含**：
- 詳細的實作任務清單（5-7 個主要任務）
- 每個任務的具體實作要點（技術層面的指導）
- 需要建立或修改的檔案清單
- 詳細的 Gherkin 驗收測試場景
- **實作參考資訊章節**：承接 research 和 PRD 的技術細節

**不應該包含**：
- 商業背景和使用者價值的重複說明（這些在 PRD 中）
- 過度詳細的逐行程式碼（這是執行時的產物）

### 與其他階段的關係

**承接 PRD 和 research**：
- PRD 提供高層次需求和技術方向，本階段將其展開成具體任務
- PRD 的高階驗收標準會被轉化成詳細的 Gherkin 場景
- **關鍵責任**：將 research 文件和 PRD 中的技術細節（程式碼範例、架構決策、技術分析）萃取並保留在「實作參考資訊」章節
- 這個階段是技術細節的「承接點」，確保前期的技術討論不會遺失

**為下游階段準備**：
- implementation.md 會被 `/process-task-list` 讀取，用來執行任務
- 開發者會在執行任務時參考「實作參考資訊」章節
- Acceptance.feature 會在驗收測試階段被執行

## 輸出

### 主要任務清單

- **格式：** Markdown (`.md`)
- **位置：** `/docs/specs/[prd-slug-name]`
- **檔案名稱：** `implementation.md`

### 驗收條件檔案

- **格式：** Gherkin (`.feature`)
- **位置：** `/docs/specs/[prd-slug-name]`
- **檔案名稱：** `acceptance.feature`

## 流程

1. **接收來源文件：** 用戶指向 PRD 或 Research 文件（或兩者都有）
   - **有 PRD 時**：以 PRD 為主要需求來源
   - **只有 Research 時**：從 Research 的結論和建議中提取實作需求
   - **兩者都有時**：PRD 提供需求框架，Research 提供技術細節

2. **分析來源文件和萃取實作資訊：** AI 讀取並分析指定文件的需求、技術分析和建議方案。

   **實作資訊萃取策略：**
   - 重點識別實作相關的技術內容，排除純理論討論
   - 保持程式碼範例和實作模式的概念正確性
   - 確保技術決策包含足夠的背景脈絡
   - 維持資訊的簡潔性，避免與任務清單重複

   **特別提取以下技術資訊：**
   - 程式碼範例和實作示範
   - 技術選型的詳細分析和理由
   - 架構決策和設計模式
   - 具體的 API 設計或檔案結構
   - 已驗證的解決方案和最佳實踐
   - 技術限制和考量事項

3. **評估現狀：** 檢視現有程式碼庫，了解現有的基礎設施、架構模式和慣例。同時，識別任何已存在且可能與需求相關的元件或功能。然後，識別可以利用或需要修改的現有相關檔案、元件和工具。

4. **生成任務與任務說明：** 基於來源文件分析和現狀評估，創建檔案並生成實作功能所需的主要任務。根據判斷決定使用多少個任務，通常約為 5-7 個。為每個任務生成詳細的任務說明（以條列式呈現），用於與開發者溝通開發範圍和實作細節，確保涵蓋所有實作要點。同時為每個任務生成「完成檢查」，提供 1-5 條簡要的檢查要點，說明如何驗證該任務已完成（使用純條列 `-`，不使用 checkbox `- [ ]`；詳見[完成檢查生成指引](references/completion-check-guide.md)）。

   **測試整合原則：**
   - **不建立獨立的測試任務**：測試應該整合在實作任務中，作為實作的一部分
   - **完成檢查包含驗證**：每個任務的「完成檢查」應包含適當的驗證方式（如單元測試執行、MCP 工具檢查、指令執行、手動驗證等）
   - **及早驗證、及早修正**：實作完成後立即執行完成檢查，在進入下一個任務前發現並修正問題
   - **驗收測試獨立**：功能層級的完整驗收測試仍保持為獨立的「執行驗收測試」任務

5. **生成驗收條件：** 基於 PRD 中的 Acceptance Criteria 部分，創建 Gherkin 格式的驗收測試場景。每個驗收條件應轉換為具體的 Feature、Scenario 和 Given/When/Then 步驟。這些步驟將由 AI 通過指令或 MCP 瀏覽器操作直接執行，而非傳統的 Cucumber glue code。詳細撰寫指引請參考[驗收測試撰寫指引](references/acceptance-test-guide.md)。

6. **生成最終輸出：** 將任務、任務說明、相關檔案和備註結合到最終的 Markdown 結構中。在任務清單末尾添加驗收測試任務和更新專案文件任務。接著將提取的實作參考資訊組織成三個子章節，放置在文件最後：
   - 來自研究文件的技術洞察（如無 research 文件則留空或省略）
   - 來自 PRD 的實作細節
   - 關鍵技術決策總結

7. **儲存檔案：**
   - 將任務清單儲存為 `implementation.md`（位置：`/docs/specs/[prd-slug-name]/`）
   - 將 Gherkin 驗收條件儲存為 `acceptance.feature`（位置：`/docs/specs/[prd-slug-name]/`）

## 輸出格式

詳細的輸出格式範例和模板，請參考[輸出格式參考](references/output-format.md)。

### 關鍵結構要求

**任務清單 (implementation.md)** 必須包含：
- 來源文件參考章節（PRD 或 Research 路徑，至少一個）
- 任務概要（checkbox 列表）
- 任務細節（每個任務包含實作要點、相關檔案、完成檢查、實作備註）
- 實作參考資訊章節

**驗收條件 (acceptance.feature)** 必須遵循：
- Gherkin 格式，使用繁體中文語言標籤
- Feature、Background、Scenario 結構
- 可由 AI 執行的 Given/When/Then 步驟

### 必要任務

每個 implementation.md 必須包含以下兩個任務：

1. **執行驗收測試**：在所有功能任務完成後執行
2. **更新專案文件**：在驗收測試後更新 README.md、CLAUDE.md 等專案層級文件（不包含 docs/research 和 docs/specs 歷史文件）

## 目標受眾

假設任務清單的主要讀者是**初級開發人員**，他們將在了解現有程式碼庫背景的情況下實作功能。
