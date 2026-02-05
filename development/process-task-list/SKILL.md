---
name: process-task-list
description: |
  Task list management and execution for spec-driven development.
  Use when: executing implementation tasks, managing task progress, processing task list with git commits.
  Keywords: task execution, process-task, implementation, commit, task management, 任務執行, 實作, 任務清單.
---

# 任務清單管理

用於在 Claude Code 中管理任務清單的指導原則，以追蹤完成 PRD 的進度

## 工作流程脈絡

### 整體開發流程

本指令是 claude-code-config 三步驟開發流程中的**第三步：任務執行**。完整流程如下：

1. **【選用】需求研究 (`/research`)**：深入調查技術問題、探索解決方案、產出研究文件
2. **需求澄清 (`/create-prd`)**：透過問答釐清需求、產出 PRD 文件
3. **實作規劃 (`/create-impl-plan`)**：分析 PRD 和程式碼庫、產出任務清單和驗收測試
4. **【當前】任務執行 (`/process-task-list`)**：逐一實作任務、執行驗收測試

### 當前階段的輸入與輸出

**輸入來源**（至少需要 PRD 或 Research 其中之一）：
- **implementation.md**：任務清單和實作要點（必需）
- **acceptance.feature**：驗收測試場景（必需）
- **PRD 文件**：功能背景和商業需求（產品導向任務）
- **Research 文件**：技術分析和解決方案（技術導向任務）

**三種常見流程**：
1. **Research + PRD**：完整流程，implementation.md 來自完整規劃
2. **只有 PRD**：技術明確，implementation.md 直接從產品需求產出
3. **只有 Research**：技術導向任務，implementation.md 從研究結論產出

**輸出目標**：
- 實際的程式碼變更
- Git commits（每個任務完成後）
- 驗收測試結果

### 各參考文件的角色

**implementation.md**：
- 提供任務清單和優先級
- 提供實作要點和技術指導
- 提供「實作參考資訊」（來自 research 和 PRD 的技術細節）

**acceptance.feature**：
- 提供驗收測試的具體場景
- 幫助理解功能的預期行為

**prd.md**（產品導向任務）：
- 提供功能的商業背景和使用者價值
- 幫助理解「為什麼」要這樣實作
- 提供高層次的技術方向

**research 文件**（技術導向任務）：
- 提供問題分析和技術選型的背景
- 提供已驗證的解決方案和最佳實踐
- 補充深入的技術脈絡

### 當前階段的職責範圍

**應該做的事**：
- 按順序執行任務清單中的任務
- 參考實作要點完成實作
- 在需要理解背景時參考 PRD 和 research
- 完成任務後進行 git commit
- 執行驗收測試

**不應該做的事**：
- 擅自修改任務清單的順序或範圍（除非發現明確的問題）
- 忽略實作參考資訊中的技術決策
- 在不理解商業背景的情況下實作

## Claude Code 任務清單同步

Claude Code 提供內建的 TodoWrite 工具來管理任務，這與 Cursor 等其他編輯器的工作方式不同。為了充分利用 Claude Code 的功能同時保持任務記錄的持久性，我們需要同步機制。

### 同步機制
- **初始載入：** 從 `implementation.md` 的「任務概要」區塊讀取任務清單，使用 TodoWrite 工具將其轉換為 Claude Code 內部任務清單
- **雙向同步：** 當 Claude Code 內部任務清單狀態改變時（pending、in_progress、completed），必須同步更新 `implementation.md` 中「任務概要」區塊對應的任務項目
- **格式對應：**
  - Claude Code `pending` → Markdown `[ ]`
  - Claude Code `in_progress` → Markdown `[ ]` (可在旁邊加註 _進行中_)
  - Claude Code `completed` → Markdown `[x]`
- **任務識別：** 使用任務標題（而非編號）作為唯一識別方式，確保概要和細節區塊的標題完全一致

### 為什麼需要同步

1. **持久化：** TodoWrite 的任務只存在於當前對話，implementation.md 提供永久記錄
2. **可見性：** 用戶可以直接在檔案中查看任務進度
3. **協作：** 其他開發者可以透過 implementation.md 了解專案狀態
4. **版本控制：** implementation.md 可以透過 Git 追蹤歷史變更

## 任務實作

- **一次一個任務：** 完成一個任務後，在請求用戶許可並獲得「yes」或「y」回應之前，**不要**開始下一個任務
- **執行時參考：**
  - 從「任務概要」區塊識別當前要執行的任務
  - 從「任務細節」區塊找到對應的任務章節（標題完全一致）
  - 參考該任務的「實作要點」和「相關檔案」進行實作

- **實作過程記錄**：
  - 在任務執行過程中，遇到以下情況時，**立即**在「實作備註」區塊記錄：

    1. **方向調整**：發現原計畫不可行或需要改用其他方法時
       - 觸發條件：使用者指出錯誤、發現技術限制、原方法行不通
       - 記錄格式：`[方向調整] 原計畫 X 因 Y 原因不可行，改用 Z 方法`
       - 範例：`[方向調整] 原計畫使用 localStorage 但需跨 tab 同步，改用 BroadcastChannel API`

    2. **技術障礙**：遇到預期外的問題需要特別處理時
       - 觸發條件：API 不支援、效能瓶頸、相容性問題、需要繞過的限制
       - 記錄格式：`[技術障礙] 遇到 X 問題，因為 Y，解決方式是 Z`
       - 範例：`[技術障礙] Next.js 動態路由不支援 SSG，需使用 generateStaticParams 預生成路徑`

    3. **關鍵決策**：與使用者討論超過 3 輪才確定的技術方案
       - 觸發條件：有多個可行方案、需要權衡取捨、影響後續任務
       - 記錄格式：`[技術決策] 在 X 和 Y 方案之間選擇 Z，因為 W`
       - 範例：`[技術決策] 在 REST 和 GraphQL 之間選擇 REST，因現有後端已是 REST 且團隊更熟悉`

    4. **後續依賴**：後續任務必須知道的資訊
       - 觸發條件：建立了新的前置條件、修改了共享資源、有執行順序要求
       - 記錄格式：`[後續依賴] 後續任務需注意 X，因為 Y`
       - 範例：`[後續依賴] 後續任務需注意必須先呼叫 initAuth() 才能使用其他 auth 函數`

  - **照預期完成時**：如果整個任務執行過程都按照任務敘述順利完成，沒有觸發上述任何情況，則標註「照預期開發」
  - 詳細的實作備註品質指引，請參考[實作備註指引](references/implementation-notes-guide.md)

- **完成協議：**
  1. 實作任務時，參考「任務細節」中的所有實作要點
  2. 完成任務後，請按照以下順序操作：
  - **檢查並完善實作備註**：
    - 檢視「實作備註」區塊，確認已記錄所有方向調整、技術障礙、關鍵決策、後續依賴
    - 如果執行過程中已經即時記錄，確認記錄完整清晰
    - 如果執行過程中沒有觸發任何需要記錄的情況，標註「照預期開發」
    - **不要**重複記錄任務敘述中已有的實作細節
  - **更新任務狀態**：在 `implementation.md` 的「任務概要」區塊中將完成的任務標記為 `[x]`
  - **暫存變更**：執行 `git add .`（包含 implementation.md 的變更）
  - **清理**：在提交前移除任何臨時檔案和臨時程式碼
  - **提交**：使用描述性的提交訊息，該訊息應：
    - 使用慣例提交格式（`feat:`、`fix:`、`refactor:` 等）
    - 總結任務中完成的內容
    - 列出關鍵變更和新增內容
    - 引用任務標題（而非編號）和 PRD 上下文
  3. 提交後，在 TodoWrite 中將任務狀態更新為 `completed`

- 每個任務完成後停止並等待用戶的許可。

## 任務清單維護

1. **工作時更新任務清單：**
   - 使用 TodoWrite 工具管理內部任務狀態
   - 同步更新 implementation.md「任務概要」區塊中的任務標記（`[ ]` → `[x]`）
   - 當新增任務時，必須同時更新：
     - 「任務概要」區塊：新增 `- [ ] 任務標題`
     - 「任務細節」區塊：新增完整的任務章節（### 任務標題 + 實作要點 + 相關檔案 + 實作備註）
     - TodoWrite 內部清單

2. **維護任務細節區塊：**
   - 每個任務的「相關檔案」列出該任務創建或修改的檔案
   - 為每個檔案提供一行描述其用途的說明
   - 任務執行後填寫「實作備註」，記錄重要的上下文資訊

## AI 指示（Claude Code）

處理任務清單時，Claude Code 必須：

1. **首次載入任務：**
   - 讀取 `implementation.md` 檔案
   - 從「任務概要」區塊提取任務清單（僅包含任務標題和 checkbox）
   - 讀取 `acceptance.feature` 檔案以了解驗收標準和大局觀點
   - 從 `implementation.md` 的「PRD 參考」章節讀取來源文件：
     - 若有 PRD 文件路徑，讀取 PRD 文件
     - 若有相關研究文件路徑，讀取研究文件
     - 可能兩者都有，或只有其中一個
   - 使用 TodoWrite 工具將任務清單轉換為內部任務格式
   - 使用任務標題作為唯一識別方式（不使用編號）

2. **任務狀態管理：**
   - 使用 TodoWrite 工具管理任務狀態（pending、in_progress、completed）
   - 一次只能有一個任務處於 `in_progress` 狀態
   - 完成任務時立即更新為 `completed`

3. **執行任務時：**
   - **首先，讀取所有已完成任務的「實作備註」**：
     - 檢視 implementation.md 中所有已標記為 `[x]` 的任務的「實作備註」區塊
     - 特別關注：方向調整、技術障礙、關鍵決策、後續依賴等標籤
     - 目的：了解之前實作過程中遇到的問題和做出的調整，避免當前任務與前置脈絡不一致
     - 重點檢查：當前任務是否依賴前置任務、前置任務是否有方向調整影響當前任務
   - 從「任務細節」區塊找到對應的任務章節（標題與「任務概要」完全一致）
   - 參考「實作要點」進行實作
   - 檢查「相關檔案」了解需要修改的範圍
   - **完成實作後，必須執行「完成檢查」**：
     - 參考任務的「完成檢查」章節，執行所有檢查要點
     - 優先使用 MCP 工具進行檢查（如 supabase mcp、playwright mcp 等）
     - 其他檢查手段包括：執行測試指令、執行建置指令、手動驗證檔案內容等
     - 即使任務是撰寫文件，也應檢查文件是否達成預期目標
     - 所有檢查要點都通過後，才能進入下一步驟
   - 完成檢查通過後，填寫「實作備註」

4. **同步更新 implementation.md：**
   - 每當 TodoWrite 中的任務狀態改變時，立即更新 `implementation.md` 的「任務概要」區塊
   - 將完成的任務標記為 `[x]`
   - 使用 Edit 工具更新檔案

5. **新增任務：**
   - 當發現新任務時，同時更新：
     - TodoWrite 內部清單
     - `implementation.md` 的「任務概要」區塊（新增 checkbox 項目）
     - `implementation.md` 的「任務細節」區塊（新增完整任務章節）

6. **填寫實作備註：**
   - 執行任務過程中，遇到方向調整、技術障礙、關鍵決策、後續依賴時，**立即**記錄到「實作備註」區塊
   - 使用結構化標籤：`[方向調整]`、`[技術障礙]`、`[技術決策]`、`[後續依賴]`
   - 任務完成後，檢查實作備註是否完整，照預期完成的任務標註「照預期開發」
   - 參考[實作備註指引](references/implementation-notes-guide.md)確保記錄品質

7. **驗收測試任務處理：**
   - 檢測任務標題或描述中包含以下關鍵詞的任務：
     - 「驗收測試」、「acceptance testing」、「驗收」、「validate implementation」
     - 「執行驗收測試」、「進行驗收」、「驗證實作」等相關詞彙
   - 當遇到驗收測試任務時，使用 Skill tool 調用 `acceptance-test` skill
   - 調用方式：`skill: "acceptance-test"`
   - acceptance-test skill 會自動讀取 implementation.md、acceptance.feature 和背景文件（PRD 或 research）並執行驗收測試
   - 驗收測試由 acceptance-test skill 專門處理，不要在當前 skill 中直接執行測試邏輯

8. **工作流程：**
   - 檢查下一個待處理任務，識別是否為驗收測試任務
   - 將任務標記為 `in_progress`（驗收測試任務調用 acceptance-test skill）
   - 完成後標記為 `completed` 並同步更新 `implementation.md`
   - 等待用戶核准後再進行下一個任務
