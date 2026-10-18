---
name: 00_cross_phase
description: 跨階段全域共用技能。適用於所有 SSDLC 開發階段的通用工具，包含版本控制、多 Agent 協作、程式碼差異同步、自主迭代研究與 TDD 流程。
---

# 跨階段全域共用技能規範 (00_cross_phase)

本技能定義了跨階段全域共用層的標準作業程序（SOP）與代理職責。此層級的 Skill 不歸屬於任一特定開發階段，而是為所有階段提供通用基礎能力。

> ⚠️ **最高指導框架原則**：本規範受 [CORE_RULES.md](../../../docs/CORE_RULES.md) 管轄，所有代理行為必須遵循 PDCA 閉環與錯誤分級重試機制。

## 一、 代理人職責規範

### 1. Planner (規劃代理)
*   **任務**：
    1.  根據當前工作階段的上下文，判斷需要哪些跨階段通用工具（版本控制、多 Agent 協作、程式碼差異同步、自主迭代研究等）。
    2.  確認工具的適用性與相容性（如 git 工作區狀態、langgraph Agent 狀態、diffsync 差異範圍）。
    3.  選定工具使用的先後順序與相依關係。
*   **驗收標準**：規劃清單中必須明確定義本次任務所需的跨階段工具清單、使用順序，以及各工具的預期產出格式。

### 2. Generator (執行代理)
*   **核心鐵律**：**只執行、不判斷、不檢查、不修改**。
*   **任務**：
    1.  嚴格依照 Planner 選定的工具清單依序執行。
    2.  執行版本控制操作（git commit、tag、stash、baseline 封存）。
    3.  執行多 Agent 協作工作流（langgraph 狀態管理、Agent 間訊息傳遞）。
    4.  執行程式碼差異對比與同步（diffsync 跨階段比對）。
    5.  執行自主迭代研究循環（autoresearch: 修改→驗證→保留/丟棄）。
    6.  執行 TDD 流程（test-driven-development: 紅→綠→重構）。
    7.  完成後儲存執行快照至根目錄的 `snapshots/` 目錄。

### 3. Evaluator (審查代理)
*   **任務**：驗證跨階段工具執行結果的正確性與完整性。
*   **審查重點**：
    *   **版本控制完整性 (30%)**：確認 git 操作正確執行、commit message 符合規範、tag 正確標記。
    *   **Agent 協作正確性 (25%)**：確認 langgraph 狀態流轉無異常、Agent 間訊息無遺漏。
    *   **差異同步準確性 (25%)**：確認 diffsync 比對結果正確、無遺漏的跨階段差異。
    *   **迭代研究有效性 (20%)**：確認 autoresearch 循環有正確的保留/丟棄決策記錄。
*   **錯誤分類與重試**（依 CORE_RULES.md 規範）：
    *   **A 類錯誤**（工具執行異常、逾時、環境問題）：局部重試最多 3 次，僅退回 Generator。
    *   **B 類錯誤**（工具不相容、Agent 狀態衝突）：立即升級全域迭代，上限 2 輪。

---

## 二、 輸入與輸出規範

*   **輸入路徑 (`inputs/`)**：各階段提出的跨階段工具需求請求。
*   **輸出路徑 (`outputs/`)**：
    *   `cross_phase_report.md`：本次跨階段工具執行摘要報告。
    *   `agent_state_snapshot.json`：langgraph Agent 狀態快照（如有）。
    *   `diff_report.md`：diffsync 跨階段差異比對報告（如有）。


## 三、 SSOT 雙軌規格管理規範

### 1. 一源多用架構

以 specs/executable_spec.yaml 為唯一資料源：

| 規格 | 讀者 | 用途 |
|:---|:---|:---|
| executable_spec.yaml | AI 代理 | 結構化規格（需求/API/資料模型/安全控制） |
| requirements.feature | AI 代理 | 行為化規格（Gherkin Given-When-Then 場景） |
| system_specification.md | 人類 | 交付驗收文件 |

### 2. 產出與讀取規範

Phase 01 Generator 產出 SSOT。Phase 02-06 Planner 執行前必須讀取。
各階段 inputs/ 必須含 spec_ref.md 指向 SSOT。

### 3. 一致性檢查

Evaluator 檢查產出與 SSOT 一致性。不一致即 B 類錯誤。規格先行原則。

## 四、 可用技能

| 快捷 | 技能名稱 | 用途 |
|:---|:---|:---|
| 01 | langgraph | 多 Agent 協作工作流狀態管理 |
| 02 | git | 版本控制與 Baseline 封存追溯 |
| 03 | diffsync | 跨階段程式碼差異對比與同步 |
| 04 | autoresearch | 自主迭代研究：修改→驗證→保留/丟棄 |
| 05 | brainstorming | 創意發想引導與需求探索 |
| 06 | firecrawl | 網頁擷取、截圖、搜尋與爬蟲 |
| 07 | test-driven-development | 測試驅動開發 (TDD) 流程 |
| 08 | verification-before-completion | 完成前強制驗證 |
| 09 | writing-plans | 多步驟任務規劃與規格撰寫 |
| 10 | ralph-loop | 自主 AI 開發循環（修改→測試→驗證→保留） |

| 12 | security-principles | 資通系統防護基準檢核（7構面/80項控制措施，支援普/中/高三等級） |
| 11 | using-superpowers | Skill 尋找與使用引導 |

## 五、 資安防護基準整合規範 (Security-Principles)

### 1. 初始化階段引用（@init 指令）

於 @init 指令執行專案初始化時，Planner 必須詢問使用者：
「本專案是否需導入資通系統防護基準（Security-Principles）？」
若使用者同意，則進一步詢問系統防護等級（普/中/高），並執行以下步驟：

1.  呼叫 Security-Principles/scripts/generate_checklist.py <等級> 產生對應檢核表
2.  將檢核表存至當前階段或專案根目錄的 outputs/ 目錄
3.  在專案 phase_gates.json 中記錄已選用之安全等級

### 2. 階段中途呼叫（@security-check 指令）

於任一 SSDLC 階段執行期間，可隨時呼叫本 Skill 進行安全檢核：

- **指令語法**：@security-check [等級]
- **口語觸發**：「執行資安檢核」「以普級防護基準檢查」「資通安全稽核」「弱點掃描檢查清單」
- **AI 代理執行步驟**：
  1.  載入對應等級之檢核表（ssets/checklist_*.md）
  2.  根據當前 SSDLC 階段，篩選適用的控制措施構面（參照 SKILL.md 中 7 構面 vs SSDLC 階段對照表）
  3.  逐項比對當前系統產出是否符合控制措施要求
  4.  產出檢核報告（含符合/不符合/不適用狀態、佐證說明）
  5.  將報告存入當前階段 outputs/security_check_report.md

### 3. 與現有 Skill 之相容性檢查

每次載入或引用 Security-Principles Skill 時，Planner 必須執行以下相容性檢查：

1.  **規則重複檢查**：比對 Security-Principles 各構面控制措施與現有 6 階段 SKILL.md 內容，偵測重複定義之規則
2.  **規則衝突檢查**：偵測 Security-Principles 控制措施與現有 Skill 規則之間是否存在矛盾（例如：安全要求 vs 效能最佳實踐衝突）
3.  **警示機制**：
    - 發現重複規則 → 輸出 [INFO] 提示，說明重複項目及所在檔案
    - 發現衝突規則 → 輸出 [WARN] 警示，列出衝突項目、所在檔案，暫停執行等候使用者確認
    - 無衝突 → 輸出 [OK] 確認，繼續執行


### 5. 階段中途安全導入（@security-load 指令）

於任一 SSDLC 階段執行期間，若 @init 時未導入 Security-Principles，
或僅需針對特定安全面向強化，可呼叫本指令：

- **指令語法**：`@security-load [等級] [構面1,構面2,...]`
- **口語觸發**：「載入資安構面」「導入安全防護」「只加存取控制和日誌」
- **AI 代理執行步驟**：
  1.  無參數時：列出 8 構面清單（含各等級項目數），供使用者選擇
  2.  讀取 `phase_gates.json`，若 `security_baseline` 不存在則自動建立
  3.  載入選定構面的 reference 文件，篩選指定等級控制措施
  4.  執行相容性檢查（比對當前階段已載入 Skill，偵測重複/衝突）
  5.  更新當前階段 `SKILL.md` 中「安全防護整合」段落
   5.5 回溯補寫：若本指令在 Phase 2 之後執行，自動對所有已完成階段補寫安全整合段落與 design_brief.md。

  6.  更新 `phase_gates.json` 記錄選定構面與等級
  7.  產出階段專屬檢核表至 `outputs/`
*   **使用範例**：
    - `@security-load` → 列出構面清單
    - `@security-load medium` → 全構面中級導入
    - `@security-load general 1,4,6` → 僅導入存取控制+識別鑑別+通訊保護

### 4. Skill 實體路徑

本 Skill 之完整實體位於：
xternal-resources/Security-Principles/

包含：
- SKILL.md — 主技能定義
- 
eferences/ — 7 構面詳細控制措施
- ssets/ — 普/中/高三等級檢核表
- scripts/generate_checklist.py — 檢核表產生工具
---

## 六、 階段間輸入與輸出檔案管理規範 (Contract Management)

> ⚠️ **選擇性功能（Opt-in）**：本規範為**選擇性套用**，非強制。僅在使用者明確啟用 IO 檔案管理後才生效。若使用者未啟用，Planner / Generator / Evaluator 應跳過本節所有規則，照原流程執行，不得強制要求或自動引導 IO 定義。

### 0. 啟用條件

IO 檔案管理僅在以下任一條件成立時啟用：

1. **使用者主動觸發**：執行 `@io set [phase]` 指令，明確為指定階段定義 IO 檔案。
2. **@init 時使用者同意**：專案初始化時，Planner 詢問「是否啟用階段 IO 檔案管理？」，使用者回答「是」。
3. **快速定義語法觸發**：使用者使用 `@[phase] in: f1, f2?` 或 `@[phase] out: f1, f2` 語法。

若以上條件皆不成立，則 IO 檔案管理**視為未啟用**，以下 1-5 節不適用。

### 1. IO 檔案結構

當 IO 檔案管理啟用後，各階段在 `.agents/skills/0*_*/` 下維護 `io_files.yaml`，明確定義該階段的輸入需求（inputs）與輸出承諾（outputs）。框架提供模板 IO 檔案，使用者可透過 `io_files.override.yaml` 覆蓋預設值。

### 2. Planner 職責（僅在 IO 檔案管理啟用時）

*   **@init 時詢問**：專案初始化時，Planner 應詢問使用者是否啟用 IO 檔案管理（預設答案為「否」）。若使用者同意，則繼續以下步驟；若不同意，則跳過本節。
*   **Skill 選定後引導**（若已啟用）：每次 `@[phase] [skill_codes]` 執行後，若該階段尚無 IO 檔案，Planner 引導 IO 定義對話。
*   **自動建議**：根據該階段的模板 `io_files.yaml` 與選定的 Skill 組合，產生建議的 inputs/outputs 清單（含必填/可選標記）。
*   **確認流程**：以編號清單方式顯示，使用者輸入要保留的編號，確認後寫入。

### 3. Generator 職責（僅在 IO 檔案管理啟用時）

*   讀取 `io_files.yaml`，確認所有 `required: true` 的輸入檔案已存在於 `inputs/`。
*   產出時確保所有 `required: true` 的輸出檔案正確生成於 `outputs/`。
*   產出完成後，將實際產出清單與 IO 檔案比對，缺漏者記錄為 A 類錯誤。
*   **若 IO 檔案管理未啟用**：Generator 照原流程產出，不需檢查 `io_files.yaml`。

### 4. Evaluator 職責（僅在 IO 檔案管理啟用時）

*   **IO 檔案兌現檢查**：比對實際產出與 IO 檔案宣告的 outputs，缺漏者標記。
*   **Mode E 觸發**：Evaluator 通過後自動執行 `python scripts/check_spec_integrity.py --mode E`，進行跨階段 IO 勾稽。
*   **下游影響分析**：若本階段 IO 檔案有變更，自動檢查下游階段是否受影響，產出警告。
*   **若 IO 檔案管理未啟用**：Evaluator 跳過 IO 檔案相關檢查，照原標準審查流程執行。

### 5. 可用指令

| 指令 | 用途 |
|:---|:---|
| `@io show [phase]` | 檢視階段 IO 檔案 |
| `@io set [phase]` | 互動式定義/修改 IO 檔案（觸發啟用） |
| `@io [phase]` | 跨階段 IO 勾稽檢查 |
| `@io diff [A] [B]` | 兩階段 IO 檔案差異比對 |
| `@[phase] in: f1, f2?` | 快速定義輸入（觸發啟用） |
| `@[phase] out: f1, f2` | 快速定義輸出（觸發啟用） |

## REA 選用證據 provider

無原始碼逆向時讀取 [REA Skill](../../../skills/00_cross_phase/rea/SKILL.md)，由既有 reverse_engineering 主控，不新增核准路徑。Planner 確認來源與操作範圍；Generator 蒐證；Evaluator 使用 check_no_source_evidence.py 檢查來源、未知與覆蓋。runtime／MCP 並非隨 Skill 自動安裝。
