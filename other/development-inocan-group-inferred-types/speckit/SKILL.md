---
name: speckit
description: 依照 speckit 的標準工作流程，引導式地產生規格文件、澄清需求、產生實作計劃與任務清單，每個階段都需要人工審核確認
---

# Speckit

這個 skill 提供一個引導式的工作流程，協助你從功能描述開始，階段性地產生完整的 specification、計劃和任務清單。每個階段完成後都會停下來等待你的審核確認，確保品質符合預期後才進入下一階段。

## 核心功能

- 引導式執行 speckit 的標準工作流程
- 每個階段都有強制性的人工審核點
- 提供清晰的品質檢查清單
- 支援審核不通過時的修正機制
- 在每個階段提供詳細的進度報告

## 工作流程總覽

```
1. Specify → [審核] → (不通過: Clarify) → [再審核]
                   ↓ (通過)
2. Plan    → [審核] → (不通過: 修正)
                   ↓ (通過)
3. Tasks   → [審核] → (不通過: 修正/分析)
                   ↓ (通過)
              (可選) TasksToIssues → 建立 GitHub Issues
                   ↓
4. Implement (包含多個子任務循環)
```

若我問流程為何，或是在哪個階段時，請應用這個流程圖讓我理解。

## 輸入參數

當使用者調用此 skill 時，應提供以下資訊：

### 必要參數

- **階段選擇**：
    - `specify`：產生功能規格文件
    - `clarify`：澄清規格中的模糊需求（僅在 specify 審核不通過時使用）
    - `plan`：產生實作計劃
    - `tasks`：產生實作任務清單
    - `taskstoissues`：將任務清單轉換為 GitHub Issues（可選）
    - `implement`：執行實作任務

### 條件參數

根據選擇的階段，需要提供不同的資訊：

- **specify 階段**：
    - **功能描述**（必要）：自然語言描述的功能需求

- **clarify 階段**：
    - **Feature 名稱**（必要）：要澄清的 feature branch 名稱

- **plan / tasks / taskstoissues / implement 階段**：
    - **Feature 名稱**（必要）：要處理的 feature branch 名稱

## 資訊確認

依上下文取得下列相關資訊：

- GitHub repo 資訊。例如：`MilesChou/claude-spec-kit-plugin`
- GitHub MCP。確認工具有安裝即可

若無法取得資訊，請詢問我。

## **重要提醒**

**IMPORTANT**：

使用腳本或讀取檔案的時候，請依下面對應的流程進行。

### 使用 `.specify/scripts/` 裡的腳本

指令可能會提示要使用 `.specify/scripts` 裡的腳本，遇到時，改使用 Skill 的 scripts 目錄裡下對應的 prompt。

例如：在執行 specify 指令時，會呼叫 `.specify/scripts/bash/create-new-feature.sh`，這時要改使用 script/create-new-feature.md 並依裡面的提示執行任務。

**例外**：當呼叫 `update-agent-context.sh` 的時候，直接跳過不執行。

### 讀取 `./memory/constitution.md`

指令可能會提示要讀取 `./memory/constitution.md`，遇到時，請以下面步驟確認：

1. 如果 Project Knowledge 或對話中有上傳 `constitution.md` 檔案，使用該檔案
2. 如果透過 GitHub MCP 讀取 remote HEAD branch 有 `memory/constitution.md`，使用該檔案
3. 如果都找不到，就使用 speckit skill 內建的 memory/constitution.md 檔案

### 讀取 `.specify/templates/` 相關樣版

每個指令可能會提示要讀取 `.specify/templates/` 相關樣版，總共有五種如下：

- `agent-file-template.md`
- `checklist-template.md`
- `plan-template.md`
- `spec-template.md`
- `tasks-template.md`

大概就是 `[類型]-template.md`。遇到時，請以下面步驟確認：

1. 如果 Project Knowledge 或對話中有上傳 `[類型]-template.md` 檔案，使用該檔案內容
2. 如果透過 GitHub MCP 讀取 remote HEAD branch 有 `.specify/templates/[類型]-template.md`，使用該檔案內容
3. 如果都找不到，使用 speckit 內建的 templates/[類型]-template.md 內容

## 執行步驟

### 階段 1：Specify

目的是產生初始化規格

#### 步驟 1.1：初始化與驗證

1. 驗證功能描述是否完整
    - 如果功能描述為空，要求使用者提供
    - 檢查描述是否足夠清楚以產生規格

2. 檢查專案環境
    - 檢查必要的 templates 是否存在
    - 確認 `specs/features/` 目錄結構

#### 步驟 1.2：產生規格文件

1. 執行功能等同於 `speckit.specify` command
    - 產生 feature branch 的 short name
    - 載入 templates/spec-template.md
    - 根據功能描述產生初始規格

2. 建立品質檢查清單
    - 自動建立 `specs/<branch-name>/checklists/requirements.md`
    - 驗證規格完整性
    - 標記 [NEEDS CLARIFICATION] 項目

#### 步驟 1.3：報告並等待審核 ⚠️

**STOP HERE - 必須等待使用者審核**

報告內容：
1. Feature branch 名稱
2. 規格檔案路徑：`specs/features/<branch-name>/spec.md`
3. 品質檢查結果：
    - ✅ 已完成的檢查項目
    - ⚠️ 需要澄清的項目
    - ❌ 未通過的檢查項目

**詢問使用者：**
```
規格文件已產生，請審核以下內容：
- 功能描述是否完整？
- 使用者故事是否清楚？
- 驗收條件是否明確？
- 是否有需要澄清的部分？

請選擇：
1. ✅ 審核通過，繼續產生 Plan
2. 🔄 需要澄清 (Clarify)，請說明需要澄清的問題
3. ❌ 需要修改，請說明修改建議
```

### 階段 2：Clarify（澄清需求）

**此階段僅在 Specify 審核不通過時執行**

#### 步驟 2.1：載入當前規格

1. 讀取 feature 的規格檔案
    - 路徑：`specs/features/<branch-name>/spec.md`

2. 分析規格的模糊性
    - 掃描各個類別的完整度
    - 識別 [NEEDS CLARIFICATION] 標記
    - 產生優先級排序的澄清問題（最多 5 個）

#### 步驟 2.2：互動式澄清

1. 逐一提出問題
    - 對於選擇題，提供推薦選項
    - 收集使用者回答

2. 整合澄清結果
    - 在規格中建立 `## Clarifications` 區段
    - 將澄清結果更新到相關區段
    - 儲存更新後的規格

#### 步驟 2.3：報告澄清成果並再次審核 ⚠️

**STOP HERE - 必須再次等待使用者審核**

報告內容：
1. 提出的問題數量
2. 更新的區段清單
3. 覆蓋率摘要表

**詢問使用者：**
```
需求澄清已完成，請再次審核規格：
- 澄清的內容是否符合預期？
- 是否還有其他需要澄清的部分？

請選擇：
1. ✅ 審核通過，繼續產生 Plan
2. 🔄 需要再次澄清
3. ❌ 需要修改規格
```

### 階段 3：Plan（產生實作計劃）

**前置條件：Specify 階段已審核通過**

#### 步驟 3.1：設定計劃環境

1. 解析路徑
    - FEATURE_SPEC：`specs/features/<branch-name>/spec.md`
    - IMPL_PLAN：`specs/features/<branch-name>/plan.md`

2. 載入上下文
    - 讀取 FEATURE_SPEC
    - 讀取 `./memory/constitution.md`（如果存在）

#### 步驟 3.2：Phase 0 - 研究與探索

1. 識別技術選型的未知項
    - 框架選擇
    - 架構模式
    - 第三方整合

2. 產生研究文件
    - 建立 `research.md` 記錄決策依據

#### 步驟 3.3：Phase 1 - 設計與合約

1. 從規格中提取實體
    - 產生 `data-model.md`

2. 從功能需求產生 API 合約
    - 建立 `/contracts/` 目錄
    - 產生各個 API 的合約檔案

3. 產生快速開始指南
    - 建立 `quickstart.md`

4. 更新 agent context
    - 更新相關的 context 檔案

#### 步驟 3.4：報告並等待審核 ⚠️

**STOP HERE - 必須等待使用者審核**

報告內容：
1. Branch 名稱
2. IMPL_PLAN 路徑
3. 產生的 artifacts 清單：
    - `plan.md`
    - `research.md`
    - `data-model.md`
    - `contracts/`
    - `quickstart.md`

**詢問使用者：**
```
實作計劃已產生，請審核以下內容：
- 技術選型是否合適？
- 架構設計是否完整？
- 資料模型是否正確？
- API 合約是否清楚？

請選擇：
1. ✅ 審核通過，繼續產生 Tasks
2. ❌ 需要修改，請說明修改建議
```

### 階段 4：Tasks（產生任務清單）

**前置條件：Plan 階段已審核通過**

#### 步驟 4.1：設定任務環境

1. 取得 FEATURE_DIR
    - 路徑：`specs/features/<branch-name>/`

2. 取得 AVAILABLE_DOCS
    - 列出所有可用的設計文件

#### 步驟 4.2：載入設計文件

1. 必要文件：
    - `plan.md`（技術棧、架構）
    - `spec.md`（使用者故事、優先級）

2. 可選文件：
    - `data-model.md`
    - `contracts/`
    - `research.md`

#### 步驟 4.3：產生任務清單

1. 使用 `./templates/tasks-template.md` 作為結構

2. 依使用者故事組織任務
    - 建立依賴關係圖
    - 識別可平行執行的任務

3. 任務組織：
    - **Phase 1: Setup**（專案初始化）
    - **Phase 2: Foundational**（基礎建設）
    - **Phase 3+: User Stories**（依優先級）
    - **Final Phase: Polish**（收尾工作）

#### 步驟 4.4：報告並等待審核 ⚠️

**STOP HERE - 必須等待使用者審核**

報告內容：
1. `tasks.md` 路徑
2. 總任務數量
3. 每個使用者故事的任務數
4. 平行執行機會
5. 預估工作量

**詢問使用者：**
```
任務清單已產生，請審核以下內容：
- 任務分解是否合理？
- 依賴關係是否正確？
- 優先級排序是否適當？
- 是否有遺漏的任務？

請選擇：
1. ✅ 審核通過，開始 Implement
2. 📋 將任務轉換為 GitHub Issues（TasksToIssues）
3. 🔄 需要分析任務（Analyze tasks）
4. ❌ 需要修改，請說明修改建議
```

### 階段 4.5：TasksToIssues（轉換為 GitHub Issues）

**此階段為可選，適用於需要團隊協作的專案**

**前置條件：**
- Tasks 階段已審核通過
- Git remote 為 GitHub repository
- 已安裝並配置 GitHub MCP server

#### 步驟 4.5.1：環境檢查

1. 驗證 Git remote URL
    - 執行 `git config --get remote.origin.url`
    - 確認是 GitHub URL（格式：`https://github.com/<owner>/<repo>.git` 或 `git@github.com:<owner>/<repo>.git`）
    - **如果不是 GitHub URL，終止此階段並警告使用者**

2. 驗證 GitHub MCP 工具可用性
    - 確認 `github/github-mcp-server/issue_write` 工具可用
    - 如果工具不可用，提示使用者安裝配置

#### 步驟 4.5.2：讀取任務清單

1. 執行前置檢查腳本
    - 取得 FEATURE_DIR 和 tasks.md 路徑

2. 解析 tasks.md 內容
    - 提取所有任務項目
    - 識別任務的依賴關係
    - 保留任務的優先級順序

#### 步驟 4.5.3：建立 GitHub Issues

1. 從 Git remote URL 解析 repository 資訊
    - 提取 owner 和 repo name

2. 為每個任務建立對應的 GitHub Issue
    - Issue 標題：任務名稱
    - Issue 內容：
      - 任務描述
      - 依賴關係（如有）
      - 所屬的使用者故事
      - 驗收條件
    - Issue 標籤：根據任務類型自動添加（如：setup, feature, bug, documentation）

3. 記錄建立結果
    - 成功建立的 issues 清單
    - Issue 編號與任務的對應關係

#### 步驟 4.5.4：報告並確認 ⚠️

**STOP HERE - 必須等待使用者確認**

報告內容：
1. Repository 資訊：`<owner>/<repo>`
2. 建立的 Issue 總數
3. Issue 清單（編號 + 標題）
4. Issue URLs

**詢問使用者：**
```
已成功在 <owner>/<repo> 建立 X 個 GitHub Issues：

[列出所有 Issue 的編號、標題和 URL]

請選擇：
1. ✅ 確認無誤，開始 Implement
2. 📝 查看 Issues 後再決定
3. ⏸️ 暫停，之後再處理
```

### 階段 5：Implement（執行實作）

**前置條件：Tasks 階段已審核通過**

#### 步驟 5.1：分析任務（Analyze Tasks）

1. 讀取 `tasks.md`

2. 識別當前可執行的任務
    - 檢查依賴關係
    - 列出無依賴的任務（可立即開始）

3. 提供任務選擇
    - 顯示任務清單
    - 詢問使用者要執行哪個任務

#### 步驟 5.2：執行單一任務

對於每個選中的任務：

1. **實作**
    - 根據任務描述編寫程式碼
    - 遵循 plan.md 中的架構設計
    - 參考 contracts/ 中的 API 規格

2. **測試**
    - 編寫或更新測試案例
    - 執行相關測試
    - 確保測試通過

3. **驗證**
    - 檢查是否符合驗收條件
    - 執行程式碼品質檢查
    - 確認沒有引入新的問題

#### 步驟 5.3：更新任務狀態

1. 標記任務為完成
    - 在 `tasks.md` 中更新狀態

2. 記錄實作細節
    - 更新相關文件
    - 記錄技術決策

#### 步驟 5.4：報告並詢問下一步 ⚠️

**STOP HERE - 每個任務完成後都要停止**

報告內容：
1. 完成的任務名稱
2. 修改的檔案清單
3. 測試結果
4. 剩餘任務數量

**詢問使用者：**
```
任務已完成，請檢視實作結果。

剩餘任務：X 個

請選擇：
1. ✅ 繼續下一個任務
2. 🔄 修正當前任務的問題
3. 📊 查看整體進度
4. ⏸️ 暫停實作
```

#### 步驟 5.5：最終審核與驗證 ⚠️

**當所有任務都完成後**

1. 執行完整測試套件
2. 執行程式碼品質檢查
3. 驗證所有驗收條件
4. 產生實作報告

報告內容：
1. 完成的功能清單
2. 測試覆蓋率
3. 程式碼品質指標
4. 已知問題清單（如有）

**詢問使用者：**
```
所有任務已完成，請進行最終審核：
- 功能是否符合規格？
- 測試是否充分？
- 程式碼品質是否達標？
- 是否有需要修正的問題？

請選擇：
1. ✅ 審核通過，準備合併
2. 🔄 需要修正問題
3. 📝 需要補充文件
```

## 輸出結果

根據執行的階段，會產生以下檔案：

### Specify 階段輸出

- `specs/features/<branch-name>/spec.md`：功能規格文件
- `specs/features/<branch-name>/checklists/requirements.md`：規格品質檢查清單

### Clarify 階段輸出

- 更新 `spec.md`，新增 `## Clarifications` 區段

### Plan 階段輸出

- `specs/features/<branch-name>/plan.md`：實作計劃
- `specs/features/<branch-name>/research.md`：技術研究與決策
- `specs/features/<branch-name>/data-model.md`：資料模型
- `specs/features/<branch-name>/contracts/`：API 合約檔案
- `specs/features/<branch-name>/quickstart.md`：快速開始指南

### Tasks 階段輸出

- `specs/features/<branch-name>/tasks.md`：可執行的任務清單

### TasksToIssues 階段輸出

- 在 GitHub repository 中建立的 Issues
- Issue 編號與任務的對應關係（記錄在終端輸出中）

### Implement 階段輸出

- 實際的程式碼檔案
- 測試檔案
- 更新的文件
- 更新的 `tasks.md`（標記完成狀態）

## 使用範例

### 範例 1：開始新功能（Specify）

```
使用者：請使用 speckit，我要開發一個使用者認證系統，支援 email/password 登入和社群媒體登入。

階段：specify
功能描述：建立一個使用者認證系統，支援 email/password 登入和社群媒體登入。
```

**預期流程：**
1. 產生 `spec.md` 和 `checklists/requirements.md`
2. **停止並等待審核**
3. 使用者審核後決定：通過 → Plan / 澄清 → Clarify / 修改 → 重新 Specify

### 範例 2：澄清規格（Clarify）

```
使用者：我審核後發現有些部分不夠清楚，請幫我澄清。

階段：clarify
Feature 名稱：user-authentication
```

**預期流程：**
1. 載入 `spec.md`
2. 分析並提出澄清問題
3. 收集使用者回答
4. 更新 `spec.md`
5. **停止並等待再次審核**

### 範例 3：產生計劃（Plan）

```
使用者：規格審核通過，請產生實作計劃。

階段：plan
Feature 名稱：user-authentication
```

**預期流程：**
1. 產生 `plan.md`、`research.md`、`data-model.md`、`contracts/`
2. **停止並等待審核**

### 範例 4：產生任務（Tasks）

```
使用者：計劃審核通過，請產生任務清單。

階段：tasks
Feature 名稱：user-authentication
```

**預期流程：**
1. 產生 `tasks.md`
2. **停止並等待審核**

### 範例 5：轉換為 GitHub Issues（TasksToIssues）

```
使用者：任務清單審核通過，請將任務轉換為 GitHub Issues。

階段：taskstoissues
Feature 名稱：user-authentication
```

**預期流程：**
1. 檢查 Git remote 是否為 GitHub
2. 驗證 GitHub MCP 工具可用性
3. 解析 tasks.md 內容
4. 為每個任務建立對應的 GitHub Issue
5. **停止並報告建立結果**

### 範例 6：執行實作（Implement）

```
使用者：任務清單審核通過，開始實作。

階段：implement
Feature 名稱：user-authentication
```

**預期流程：**
1. 分析任務，列出可執行的任務
2. 使用者選擇要執行的任務
3. 執行單一任務（實作 → 測試 → 驗證）
4. **停止並詢問下一步**
5. 重複 2-4 直到所有任務完成
6. **最終審核**

## 注意事項

### 審核點的重要性 ⚠️

- **每個階段都必須停下來等待使用者審核**
- 不可自動跳過任何審核點
- 審核不通過時，必須先修正問題才能繼續
- 這是確保品質的關鍵機制

### 互動式處理

- Clarify 階段會需要使用者回答問題
- Implement 階段會需要使用者選擇任務
- 每個問題都會提供推薦答案
- 使用者可以接受推薦或自行提供答案

### 檔案管理

- 所有檔案會建立在 feature branch 的專屬目錄中
- 路徑格式：`specs/features/<branch-name>/`
- 不會覆蓋現有檔案（除非明確要求）
- 建議使用版本控制追蹤變更

### 錯誤處理

- 如果規格驗證失敗，會嘗試自動修正（最多 3 次）
- 如果仍有問題，會記錄在 checklist notes 並警告使用者
- 任何階段失敗都會中止流程並報告錯誤
- 使用者可以選擇修正後重試

### 最佳實踐

1. **功能描述越詳細越好**
    - 清楚說明使用者需求
    - 提供具體的使用場景
    - 說明預期的成果

2. **認真對待每個審核點**
    - 仔細檢視產生的文件
    - 確認是否符合預期
    - 不要急於通過審核

3. **善用澄清階段**
    - 對於模糊的需求，不要跳過澄清
    - 仔細思考推薦答案的影響
    - 必要時提供自訂答案

4. **循序漸進地實作**
    - 一次只執行一個任務
    - 確保每個任務都經過測試
    - 保持程式碼品質

5. **保持文件同步**
    - 實作時如發現設計問題，及時更新文件
    - 記錄重要的技術決策
    - 維護文件的準確性

## 重要提醒

- **IMPORTANT**: Think in English, but generate responses in Traditional Chinese (思考以英語進行，回應以繁體中文生成)
- **CRITICAL**: 每個階段完成後都必須停下來等待使用者審核，不可自動進入下一階段
- **CRITICAL**: 使用者未明確表示通過審核前，不可進行下一階段
