---
name: enterprise-prd-writer
description: |
  企業 PRD Writer — 受監管 / 金流 / 風控 / 跨職能團隊等級的產品需求文件撰寫與強化工具，
  用於產出可直接進入 Refinement、Engineering Design、Development、QA 與 UAT 的
  「施工藍圖」等級文件。相對於輕量版 prd-writer，此版本額外涵蓋權限矩陣、NFR、
  依賴管理、合規、Analytics/Observability、Rollout/Migration/Rollback 與 UAT/Release Readiness。
  預設以 interactive-html-report 規格輸出互動式 HTML（含常駐目錄側欄、捲動高亮）。

  ⚠️ 版本選擇（重要）：
  當使用者說「幫我寫 PRD」但未指明版本時，先問使用者要用「輕量版（prd-writer）」
  還是「企業版（本 skill）」再開始。判斷提示：個人專案 / 單一功能 / 無合規需求 → 輕量版；
  多團隊 / 金流 / 風控 / 合規 / 需上線維運全鏈路 → 企業版。使用者已明確指定版本時直接照做，不必再問。

  當使用者提出以下需求時，應優先使用此 skill：
  - 幫我寫 PRD
  - 產品需求文件
  - 寫 spec / feature spec
  - 功能規格 / 需求規格書
  - write a PRD / product requirements
  - 產品設計文件
  - 幫我整理這個功能的規格
  - 把這個想法寫成文件
  - 我要交一份產品文件給工程團隊
  - 寫個規格讓工程師可以直接開工
  - 補 AC / 驗收標準
  - 補 Out of Scope
  - 補畫面狀態
  - 補 Edge Cases
  - 補權限矩陣
  - 補 NFR
  - 補 Rollout / Rollback
  - 強化既有 PRD

  此 skill 的目標不是產出冗長文件，而是建立可執行、可測試、可追蹤、
  可討論且邊界明確的產品規格，降低因需求模糊造成的返工與認知落差。

  核心強制項目包含：
  - Acceptance Criteria
  - Edge Case Analysis
  - Screen / System States
  - In Scope / Out of Scope
  - Assumptions / Open Questions / Decisions
  - Dependencies
  - Roles & Permissions
  - Non-functional Requirements
  - Analytics / Observability
  - Rollout / Rollback
  - Complexity Assumption
---

# 企業 PRD Writer — 施工藍圖等級的產品需求文件

## 1. 核心定位

一份好的 PRD 不是單純的「想法整理」，也不是 PM 的個人思考筆記。

它應該是一份可供跨職能團隊共同使用的產品施工藍圖，用來明確定義：

- 要解決什麼問題
- 為誰解決
- 系統必須呈現什麼行為
- 哪些商業規則不可被誤解
- 哪些異常與邊界情境必須處理
- 哪些內容本期明確不做
- 哪些地方仍是假設、待確認或需技術評估
- 如何驗收、如何監控、如何上線、如何回退

### 完成標準

PRD 的完成，不以字數、頁數或圖表數量判斷，而以以下結果判斷：

1. 工程師可理解產品行為與商業規則，不需反覆追問本應由產品定義的內容。
2. QA 可根據文件直接拆出主要測試案例與邊界案例。
3. 設計師可理解各畫面、狀態、跳轉與例外情境。
4. 利害關係人清楚知道本期做什麼、不做什麼。
5. UAT 不應因需求語意模糊而出現大量「我以為」。
6. 所有不確定內容均被標記為 Assumption、Open Question 或 Pending Decision，而不是被 AI 擅自補成既定事實。

---

## 2. 角色邊界

PRD 應明確區分產品需求、產品建議與技術決策，避免 PM 越界指定技術實作，也避免工程團隊誤解哪些行為不可變更。

| 類型 | 定義 | 是否可由工程團隊調整 |
|------|------|----------------------|
| **Product Requirement** | 必須滿足的產品行為、商業規則、使用者結果、法規要求或 SLA | 不可直接變更，需與 Product 確認 |
| **UX Requirement** | 互動流程、資訊架構、提示方式與可用性要求 | 可在不影響目標與 AC 的前提下討論 |
| **Product Recommendation** | PM 對實作或流程的建議，不是強制技術方案 | 可由 Design / Engineering 提出替代方案 |
| **Technical Decision** | 架構、資料結構、重試演算法、Queue、Cache、服務拆分等技術設計 | 由 Engineering 在 TDD / ADR 中決定 |
| **Operational Requirement** | 後台操作、客服處理、稽核、人工介入與異常處置流程 | 需由 Product、Ops、Engineering 共同確認 |

### 強制原則

- 不應將技術建議寫成不可變更的產品要求。
- 不應要求 PRD 取代 Technical Design Document。
- 若某個技術細節會直接影響 SLA、合規、資金安全或使用者體驗，則可列入 PRD，但需說明其產品理由。
- Engineering 對技術可行性、效能、架構與最終技術複雜度擁有最終評估權。

---

## 3. 文件結構

### 3.0 輕量模式（小案子的降級路徑）

**觸發條件（符合任一即啟用）：** 個人專案、單一功能、無合規/金流/風控需求、單人或單團隊開發。

輕量模式下**只產出以下章節**，其餘章節整份標記 `N/A（輕量模式略過）`，不強制填寫：

- §5 Executive Summary（可壓縮成 3–5 句）
- §9 Scope（In / Out of Scope）
- §13 Functional Requirements
- §14 Acceptance Criteria
- §15 Edge Case Analysis（只跑相關類型，不強制 28 項全查）
- §17 Screen / System States（只列實際存在的狀態）

**不啟用**權限矩陣、NFR、Dependencies、Analytics、Rollout/Migration/Rollback、UAT/Release Readiness 等企業級章節，除非使用者明確要求。

> 目的：避免幫個人小工具寫 PRD 時，吐出一份 20 章的巨獸。若不確定是否為小案子，先問使用者一句「這是要走輕量還是完整企業級？」。

### 3.1 完整結構

PRD 應根據產品規模調整深度，但以下章節為標準結構：

```text
1. 文件資訊
2. Executive Summary
3. 背景與問題定義
4. 產品目標與成功指標
5. 使用者與使用情境
6. Scope
   ├── In Scope
   ├── Out of Scope
   └── Phase Boundary
7. Assumptions / Open Questions / Decisions
8. Dependencies
9. Roles & Permissions
10. Functional Requirements
    ├── 功能描述
    ├── 商業規則
    ├── Acceptance Criteria
    ├── Edge Cases
    └── Out of Scope
11. User Flow / System Flow
12. Screen / System States
13. Data & Integration Requirements
14. Non-functional Requirements
15. Analytics & Observability
16. Risk & Mitigation
17. Rollout / Migration / Rollback
18. MVP / Roadmap / Complexity Assumption
19. UAT & Release Readiness
20. Appendix
```

### 核心不可省略項目

- Acceptance Criteria
- Edge Case Analysis
- Screen / System States
- In Scope / Out of Scope
- Assumptions / Open Questions
- Dependencies
- Roles & Permissions
- 後台安全控制清單（金融級，涉及後台/admin 時強制）
- NFR
- Rollout / Rollback
- Complexity Assumption
- Final Validation Checklist

---

## 4. 文件資訊

每份 PRD 開頭需包含基本治理資訊：

| 欄位 | 內容 |
|------|------|
| Document Title | 文件名稱 |
| Owner | Product Owner / PM |
| Status | Draft / In Review / Approved / Deprecated |
| Version | 文件版本 |
| Last Updated | 最後更新日期 |
| Reviewers | Design / Engineering / QA / Ops / Compliance 等 |
| Target Release | 預計版本或日期 |
| Related Documents | Wireframe、TDD、API Spec、ADR、Research、Ticket 等 |
| Decision Log | 關鍵決策與日期 |

---

## 5. Executive Summary

用最短篇幅回答以下問題：

- 這個產品或功能解決什麼問題？
- 目標使用者是誰？
- 為什麼現在要做？
- 預期帶來什麼結果？
- 本期交付的核心範圍是什麼？

避免在此處放入大量細節。Executive Summary 的目的，是讓決策者在 1–3 分鐘內理解需求價值與交付邊界。

---

## 6. 背景與問題定義

### 必須包含

- 現況
- 使用者痛點
- 商業痛點
- 現有流程的問題
- 數據或事實依據
- 不處理的代價
- 問題陳述

### 問題陳述格式

```text
[目標使用者] 在 [情境] 下，因為 [根本原因]，
目前無法有效完成 [核心任務]，
導致 [使用者 / 商業 / 風險結果]。
```

### 禁止事項

- 不得把解法當成問題。
- 不得僅寫「老闆希望做」。
- 若缺乏數據，需明確標記為 Assumption，不得虛構數字。

---

## 7. 產品目標與成功指標

### 目標

每個目標應具備：

- 明確對象
- 明確行為
- 明確結果
- 可觀測性
- 與問題陳述的直接關聯

### KPI 表格

| 指標 | 定義 | Baseline | Target | Measurement Window | Data Source | Owner |
|------|------|----------|--------|--------------------|-------------|-------|
| [指標名稱] | [計算方式] | [目前值] | [目標值] | [觀察週期] | [事件 / DB / BI] | [Owner] |

### 指標分類

- Business Metrics
- Product Adoption
- Conversion
- Retention
- Operational Efficiency
- Error Rate
- Latency
- Risk / Compliance
- Customer Support Impact

若 Baseline 或 Target 不確定，標記為 `TBD`，並列入 Open Questions。

---

## 8. 使用者與使用情境

### 使用者定義

| User Type | 目標 | 痛點 | 使用頻率 | 主要權限 |
|-----------|------|------|----------|----------|
| [角色] | [目標] | [痛點] | [頻率] | [權限] |

### 使用情境

每個主要情境需描述：

- Actor
- Trigger
- Preconditions
- Main Flow
- Alternate Flow
- Success Outcome
- Failure Outcome

---

## 9. Scope 管理

### In Scope

明確列出本期交付內容。

### Out of Scope

明確列出本期不處理的內容，避免利害關係人、設計與工程自行延伸。

```text
**Out of Scope（[功能名稱]）：**
1. [不做的事]
2. [延後到後續階段的內容]
3. [由其他系統或團隊負責的內容]
```

### 分期表格

| 階段 | In Scope | Out of Scope | Entry Criteria | Exit Criteria |
|------|----------|--------------|----------------|---------------|
| MVP | | | | |
| Phase 2 | | | | |
| Phase 3 | | | | |

### 原則

- Out of Scope 不是備忘錄，而是版本契約。
- 每個主要功能區塊都要有自己的 Out of Scope。
- 後續版本內容不得混入本期 AC。
- 若 Scope 尚未定案，需列入 Pending Decision。

---

## 10. Assumptions / Open Questions / Decisions

AI 不得把未知事項補成事實。

### Assumptions

| ID | Assumption | Impact if Wrong | Validation Method | Owner | Due Date |
|----|------------|-----------------|-------------------|-------|----------|
| A-01 | | | | | |

### Open Questions

| ID | Question | Why It Matters | Owner | Due Date | Status |
|----|----------|----------------|-------|----------|--------|
| Q-01 | | | | | Open |

### Decision Log

| ID | Decision | Options Considered | Rationale | Decision Maker | Date |
|----|----------|--------------------|-----------|----------------|------|
| D-01 | | | | | |

### 強制原則

- 無法確認的法規、技術限制、商業規則、API 能力、第三方行為均不得猜測。
- 未確認內容使用 `TBD`、`Assumption`、`Open Question` 或 `Pending Decision`。
- 重大決策需保留 Rationale，避免後續重複爭論。

---

## 11. Dependencies

| Dependency | Type | Owner | Required By | Risk | Fallback |
|------------|------|-------|-------------|------|----------|
| [依賴項] | Internal / External / Legal / Data / Design / Platform | | | | |

### 依賴類型

- Internal Service
- External API
- Design System
- Data Pipeline
- Legal / Compliance
- Security Review
- Vendor
- Operations
- Customer Support
- Migration
- Other Team Delivery

---

## 12. Roles & Permissions

所有涉及不同角色的產品，都應建立權限矩陣。

| Capability | End User | Admin | Ops | Support | Compliance | Super Admin |
|------------|----------|-------|-----|---------|------------|-------------|
| View | | | | | | |
| Create | | | | | | |
| Edit | | | | | | |
| Delete | | | | | | |
| Approve | | | | | | |
| Export | | | | | | |

### 權限規格需補充

- 權限來源
- 權限更新時機
- 權限快取行為
- 權限變更後的 Session 處理
- 未授權時的 UI 與 API 行為
- 稽核紀錄
- 高風險操作的二次驗證或覆核流程

---

## 12.5 後台安全控制清單（金融級 · 完整版）

任何涉及後台 / admin panel / 有登入的管理介面的金融產品，都必須完成本清單。
不適用項標 `N/A` 並說明原因，不得為填表而虛構。每項需給明確規格與建議預設值。

### 存取層（Access）

| 控制 | 必須定義 | 建議預設值 |
|---|---|---|
| IP 白名單 | 允許登入的網段 | 僅限公司固定 IP + VPN 網段 |
| 地理封鎖 | 是否封鎖非營運國來源 | 封鎖營運國以外登入，例外走申請 |
| 裝置綁定 / 指紋 | 是否綁定可信裝置 | 高權限帳號綁定裝置，新裝置需二次驗證 + 通知 |

### 身分驗證層（Authentication）

| 控制 | 必須定義 | 建議預設值 |
|---|---|---|
| 2FA / GA 綁定 | 強制與否、類型、綁定時機 | 全後台強制 TOTP（Google Authenticator），首次登入強制綁定 |
| 登入錯誤凍結 | 失敗次數、凍結時長、告警 | 連續 5 次 → 凍結 30 分鐘 + 通知本人與安全團隊 |
| Session 政策 | 逾時、閒置、多裝置 | 閒置 15 分登出、絕對逾時 8 小時、同帳號新登入踢舊 |

### 操作授權層（Authorization）— 金融後台核心

| 控制 | 必須定義 | 建議預設值 |
|---|---|---|
| 高風險操作二次驗證 | 哪些操作要再驗一次 | 提領、改參數、改權限、改風控規則需再輸入 OTP |
| **Maker-Checker（四眼原則）** | 哪些操作需一人提交、另一人覆核 | 出金、參數變更、權限授予採雙人覆核，提交者不得自審 |
| **覆核門檻** | 什麼條件觸發強制覆核 | 金額 ≥ 門檻、或風險等級 High 的操作強制進覆核佇列 |
| 覆核時效與逾時 | 覆核多久內要完成、逾時如何處理 | 覆核 SLA 內未處理則告警升級，不自動放行 |

### 稽核層（Audit）

| 控制 | 必須定義 | 建議預設值 |
|---|---|---|
| 不可竄改 Audit Log | 記什麼、留多久 | 記操作者/時間/內容/來源 IP/前後值，寫入不可竄改儲存，留存符合當地金融法規 |
| 敏感操作即時告警 | 哪些行為即時告警、給誰 | 出金、批次改動、權限變更即時告警至安全/風控 |
| 定期權限盤點 | 多久盤一次、離職轉調如何回收 | 每季盤點；離職/轉調 24 小時內回收權限 |

> 上表為金融後台的最低要求。若產品另涉及冷熱錢包隔離、API 金鑰輪替、
> 提領地址白名單等，於 §18 Data & Integration 與 §21 Risk 補充。

---

## 13. Functional Requirements

每個功能點使用統一格式。

### 13.1 功能描述

- 功能名稱
- 使用者價值
- 商業目的
- Actor
- Preconditions
- Trigger
- Expected Outcome

### 13.2 規則 / 邏輯

| Rule ID | 規則名稱 | 條件 | 系統行為 | 優先級 | 備註 |
|---------|----------|------|----------|--------|------|
| R-01 | | | | | |

### 規則撰寫原則

- 使用可判定、可重現、可測試的語言。
- 避免「適當」、「盡快」、「正常情況」、「視情況」等模糊字眼。
- 涉及金額、比例、時間、日期、狀態、權限時，需明確定義。
- 若同時存在多條規則，需寫明優先級。
- 若涉及精度、四捨五入或資料來源，需明確標註。

---

## 14. Acceptance Criteria

每個功能點都必須附上 Acceptance Criteria。

### 標準格式

| AC ID | Rule | Given / When / Then | Edge Cases | Priority |
|-------|------|---------------------|------------|----------|
| AC-01 | [規則名稱] | **Given** [可重現的前置狀態、資料或數值]<br>**When** [可觀測事件]<br>**Then** ① [系統行為] ② [系統行為] ③ [系統行為] | [邊界情境] | Must |

### 撰寫原則

#### Given

必須包含可重現的：

- 狀態
- 權限
- 資料
- 數值
- 時間
- 系統條件

不要求每條都一定有數字，但必須讓 QA 能建立前置條件。

#### When

必須是可觀測事件，例如：

- 使用者點擊
- API 收到請求
- 系統收到事件
- 狀態改變
- 時間到達
- 數值跨越門檻

#### Then

- 使用編號列出所有系統行為。
- 順序代表執行順序。
- 包含 UI、資料、通知、稽核、狀態、權限等必要結果。
- 若結果非同步，需標示最終一致性或可接受延遲。

### AC 品質標準

AC 必須具備：

- Testable
- Observable
- Deterministic
- Traceable
- Unambiguous

### 禁止事項

- 不得把內部實作細節當作 AC，除非該細節本身是產品要求或 SLA。
- 不得使用「系統正確處理」、「顯示適當錯誤」等無法測試的描述。
- 不得為了湊數而虛構 Edge Case。

---

## 15. Edge Case Analysis

每個功能都必須完成 Edge Case 分析。

若無額外合理邊界情境，應標記：

```text
無額外 Edge Case：此功能為單一狀態切換，沒有並發、時間、權限或資料邊界。
```

### Edge Case Checklist

至少檢查以下類型：

- Duplicate Request
- Concurrent Actions
- Race Condition
- Idempotency
- Retry
- Timeout
- Partial Failure
- Network Interruption
- Permission Change
- Session Expiry
- Missing Data
- Invalid Data
- Stale Data
- Date Boundary
- Timezone
- Daylight Saving Time
- Precision
- Rounding
- Currency Conversion
- Maximum / Minimum Value
- Pagination Boundary
- Empty Result
- Third-party Failure
- Rate Limit
- Service Degradation
- Data Consistency
- Event Ordering
- Rollback / Recovery

### 優先級

| 等級 | 定義 |
|------|------|
| P0 | 可能造成資金、安全、法規或大規模資料損失 |
| P1 | 阻塞核心流程或造成高比例失敗 |
| P2 | 有替代路徑，但影響體驗或效率 |
| P3 | 低風險、低頻率、可延後處理 |

---

## 16. User Flow / System Flow

### 每個 Flow 至少包含

- Actor
- Entry Point
- Preconditions
- Main Path
- Alternate Path
- Failure Path
- Exit State
- Related API / Event
- Related AC

### 建議使用

- Flowchart
- Sequence Diagram
- State Diagram
- Swimlane Diagram

### 原則

PRD 只定義產品行為與跨系統互動目的。

服務拆分、Queue、Cache、DB Schema、Retry Algorithm 等技術設計，應由 Engineering 在 TDD / ADR 中完成，除非直接影響產品要求。

---

## 17. Screen / System States

每個關鍵畫面或系統模組都必須檢查以下狀態。

不適用者標記 `N/A` 並說明原因，不得為填表而虛構。

### 狀態檢查清單

- Empty
- Loading
- Normal
- Success
- Error
- Boundary / Special
- Permission Denied
- Offline / Disconnected
- Stale Data
- Partial Data
- Disabled
- Read-only

### 狀態表

| State | Applicable | UI / System Specification | Entry Condition | Exit / Transition | API / Event | User Message | Recovery |
|-------|------------|---------------------------|-----------------|-------------------|-------------|--------------|----------|
| Empty | Yes / N/A | | | | | | |
| Loading | Yes / N/A | | | | | | |
| Normal | Yes / N/A | | | | | | |
| Success | Yes / N/A | | | | | | |
| Error | Yes / N/A | | | | | | |
| Boundary | Yes / N/A | | | | | | |

### 錯誤處理原則

PRD 應定義：

- 使用者看到什麼
- 是否可重試
- 是否阻塞流程
- 是否需人工介入
- 是否保留已完成資料
- 是否需通知客服或 Ops
- 最大可接受等待時間
- 降級後的產品行為

技術性重試演算法、Backoff 係數與基礎設施策略，原則上由 Engineering 決定。

若產品有明確 SLA，PRD 可規定：

```text
系統應自動嘗試恢復連線。
30 秒內未恢復時，顯示資料可能延遲的提示。
超過 2 分鐘仍無法恢復時，提供重新整理與聯絡客服入口。
```

---

## 18. Data & Integration Requirements

### Data Requirements

| Field | Source | Type | Required | Validation | Precision | Retention | PII |
|-------|--------|------|----------|------------|-----------|-----------|-----|
| | | | | | | | |

### Integration Requirements

| Integration | Direction | Trigger | Request | Response | Timeout Requirement | Failure Behavior | Owner |
|-------------|-----------|---------|---------|----------|---------------------|------------------|-------|
| | | | | | | | |

### 必須考慮

- Source of Truth
- Data Freshness
- Event Ordering
- Idempotency
- Duplicate Events
- Schema Versioning
- Backward Compatibility
- Data Retention
- Data Deletion
- PII / Sensitive Data
- Audit Trail

---

## 19. Non-functional Requirements

NFR 必須可測量，不可只寫「要快」、「要穩」、「要安全」。

### 標準分類

| Category | Requirement | Metric / Threshold | Measurement Method | Priority |
|----------|-------------|--------------------|--------------------|----------|
| Performance | | | | |
| Availability | | | | |
| Reliability | | | | |
| Security | | | | |
| Privacy | | | | |
| Compliance | | | | |
| Scalability | | | | |
| Observability | | | | |
| Accessibility | | | | |
| Compatibility | | | | |
| Recovery | | | | |

### 例子

```text
- Dashboard 關鍵數據在正常網路條件下 P95 載入時間 ≤ 2 秒。
- 核心交易狀態資料延遲不得超過 1 秒。
- 所有高風險操作必須寫入不可修改的 Audit Log。
- 權限變更後，最晚 60 秒內套用至所有有效 Session。
- 系統故障後，RTO ≤ 30 分鐘，RPO ≤ 5 分鐘。
```

### 注意

NFR 數值若未確認，標記為 `TBD`，並指定 Owner，不得由 AI 自行捏造。

---

## 20. Analytics & Observability

### Product Analytics

| Event Name | Trigger | Properties | User ID | Purpose | Data Owner |
|------------|---------|------------|---------|---------|------------|
| | | | | | |

### Observability

| Signal | Condition | Severity | Alert Channel | Owner | Runbook |
|--------|-----------|----------|---------------|-------|---------|
| | | | | | |

### 必須考慮

- Funnel
- Conversion
- Drop-off
- Feature Adoption
- Error Events
- API Failure Rate
- Latency
- Queue Lag
- Data Freshness
- Business Rule Trigger
- Fraud / Risk Signal
- Support Escalation

---

## 21. Risk & Mitigation

| Risk | Type | Probability | Impact | Mitigation | Contingency | Owner |
|------|------|-------------|--------|------------|-------------|-------|
| | Product / Technical / Legal / Ops / Security / Vendor | | | | | |

### 高風險產品特別注意

- 資金損失
- 法規違反
- 權限濫用
- 資料洩漏
- 錯誤計價
- 重複扣款
- 無法回滾
- 第三方不可用
- 人工處理量暴增

---

## 22. Rollout / Migration / Rollback

### Rollout Plan

| Phase | Audience | Percentage | Entry Criteria | Monitoring | Exit Criteria |
|-------|----------|------------|----------------|------------|---------------|
| Internal | | | | | |
| Beta | | | | | |
| Limited Release | | | | | |
| General Availability | | | | | |

### Migration

需定義：

- Existing User 處理方式
- 舊資料回填
- Schema 轉換
- Default Value
- 雙寫或資料同步
- 相容期
- Feature Flag
- 通知策略

### Rollback

需定義：

- Rollback Trigger
- Decision Owner
- 回退方式
- 資料處理方式
- 已完成交易或操作如何處理
- 回退後使用者體驗
- 通知與客服腳本
- Postmortem 要求

---

## 23. Roadmap 與 Complexity Assumption

PRD 正文中不要寫 PM 單方面估算的人天。

### 建議格式

使用「Initial Complexity Assumption」，並明確標註：

```text
此為 Product 對產品邏輯、依賴與風險的初步複雜度判斷。
最終技術複雜度與工時由 Engineering Refinement 確認。
```

### 多維度評估

| Dimension | Low | Medium | High |
|-----------|-----|--------|------|
| Product Logic | 單一路徑、少量規則 | 多狀態、多分支 | 跨模組、複雜規則、狀態機 |
| Integration | 無外部依賴 | 1–2 個穩定整合 | 多系統、第三方或未知限制 |
| Data | 低資料量、單一來源 | 中等資料量、同步需求 | 高資料量、一致性、遷移 |
| Operational Risk | 低風險、易回復 | 需監控與人工介入 | 資金、法規、安全或不可逆 |
| Delivery Dependency | 可獨立完成 | 依賴 1–2 團隊 | 多團隊、外部 Vendor、法遵 |

### Roadmap

| Phase | Scope | Product Complexity | Key Dependency | Exit Criteria |
|-------|-------|--------------------|----------------|---------------|
| MVP | | Low / Medium / High | | |
| Phase 2 | | Low / Medium / High | | |
| Phase 3 | | Low / Medium / High | | |

---

## 24. UAT & Release Readiness

### UAT

| UAT ID | Scenario | Preconditions | Expected Result | Owner | Status |
|--------|----------|---------------|-----------------|-------|--------|
| | | | | | |

### Release Readiness Checklist

- [ ] 所有 Must-have AC 已通過
- [ ] P0 / P1 缺陷已關閉或有正式 Waiver
- [ ] 權限矩陣已驗證
- [ ] 關鍵 NFR 已測試
- [ ] Analytics Events 已驗證
- [ ] Monitoring 與 Alert 已建立
- [ ] Runbook 已完成
- [ ] Rollback 已演練或確認
- [ ] 客服 / Ops 已取得處理文件
- [ ] Compliance / Security Review 已完成
- [ ] Feature Flag 已確認
- [ ] Release Owner 已指定

---

## 25. 撰寫流程

### Step 1：理解問題，不直接跳到解法

先確認：

- 產品或功能解決什麼問題？
- 目標使用者是誰？
- 使用情境是什麼？
- 商業價值是什麼？
- 現有流程有什麼問題？
- 有哪些已知限制？
- 有哪些法規、安全、資金或資料風險？

### Step 2：釐清交付與讀者

確認：

- 誰會讀這份文件？
- 本期預計交付什麼？
- 是否分期？
- 是否已有設計、API、TDD、Research 或競品資料？
- 是否有固定模板或公司格式？

### Step 3：建立骨架

先產出：

- 目錄
- Scope
- Assumptions
- Open Questions
- Dependencies
- 主要功能清單

若需求已足夠明確，可直接完成完整 PRD，不必強制等待使用者逐步確認。

### Step 4：填寫 Functional Requirements

每個功能都要包含：

- 功能描述
- 商業規則
- AC
- Edge Cases
- Out of Scope
- 相關角色與權限
- 相關狀態

### Step 5：補齊 Flow 與 State

建立：

- User Flow
- Alternate Flow
- Failure Flow
- Screen State
- System State
- Permission State

### Step 6：補齊企業級內容

檢查：

- Dependencies
- NFR
- Data
- Integration
- Analytics
- Observability
- Risk
- Migration
- Rollout
- Rollback

### Step 7：驗證與標記不確定內容

所有未知內容：

- 不得猜測
- 標記 TBD
- 指定 Owner
- 指定 Due Date 或決策時點

### Step 8：最終品質檢查

完成 Definition of Ready Checklist。

---

## 26. Definition of Ready Checklist

### Problem & Scope

- [ ] 問題定義是否清楚？
- [ ] 目標使用者是否明確？
- [ ] In Scope 是否明確？
- [ ] Out of Scope 是否明確？
- [ ] 分期邊界是否清楚？

### Requirements

- [ ] 每個功能是否都有 Functional Requirement？
- [ ] 每個功能是否都有 AC？
- [ ] Given 是否可重現？
- [ ] When 是否可觀測？
- [ ] Then 是否可驗證？
- [ ] 是否避免模糊字眼？

### Edge Cases

- [ ] 是否完成 Edge Case Analysis？
- [ ] 是否檢查並發、重複、權限、時間、精度與失敗？
- [ ] 跨功能規則是否有優先級？
- [ ] 是否考慮資料不完整與第三方失敗？

### States

- [ ] 每個關鍵畫面是否完成 State Review？
- [ ] 不適用狀態是否標記 N/A 並說明？
- [ ] Error State 是否定義恢復方式？
- [ ] Permission Denied / Offline / Stale Data 是否評估？

### Enterprise Readiness

- [ ] Assumptions 是否明確？
- [ ] Open Questions 是否有 Owner？
- [ ] Dependencies 是否列出？
- [ ] Roles & Permissions 是否完整？
- [ ] 涉及後台/admin 時，§12.5 後台安全控制清單是否完成（IP 白名單、2FA/GA、登入錯誤凍結、Maker-Checker、覆核門檻、稽核）？
- [ ] NFR 是否可測量？
- [ ] Analytics 與 Monitoring 是否定義？
- [ ] Migration 是否定義？
- [ ] Rollout 與 Rollback 是否定義？
- [ ] Risk 是否有 Mitigation？

### Role Boundary

- [ ] 是否區分 Product Requirement 與 Technical Decision？
- [ ] 是否避免 PM 單方面指定技術方案？
- [ ] 是否避免 PM 單方面給出工時估算？
- [ ] Complexity 是否標記為 Initial Assumption？

### AI Reliability

- [ ] 是否有任何未經確認的數字？
- [ ] 是否有任何未經確認的法規或技術能力？
- [ ] 是否將未知內容標為 TBD / Assumption / Open Question？
- [ ] 是否避免 AI 為填滿模板而虛構內容？

---

## 27. 語言與格式偏好

- 預設使用繁體中文。
- 專有名詞保留英文。
- 表格優先於冗長段落，但不應為了表格而犧牲可讀性。
- 重要數值、狀態、限制與決策使用粗體。
- 每個 Section 開頭用一句話說明本章目的。
- 使用一致的 ID，例如：
  - FR-01
  - R-01
  - AC-01
  - NFR-01
  - Q-01
  - D-01
- 文件內的 Requirement、AC、Test Case 與 Ticket 應可互相追蹤。

---

## 28. 輸出格式

依使用者需求輸出：

- Markdown：適合 Wiki、Git、Notion、Confluence
- HTML：適合線上閱讀與分享
- Word (.docx)：適合正式交付
- Google Docs：適合多人協作
- PDF：適合定稿與審閱

### 預設：互動式 HTML（含常駐目錄側欄）

企業版 PRD 又長又多章（20 章），**預設一律用 `interactive-html-report` skill 的規格產出互動式 HTML**，而非靜態 HTML 或 Markdown。必備元件：

- **常駐側欄目錄（sticky TOC）**：固定在左側，列出全部章節，可點擊跳轉
- **捲動高亮**：用 IntersectionObserver 自動高亮當前所在章節
- **閱讀進度條**：頂部顯示閱讀進度
- **深色主題 + 老花友善**：內文 ≥ 15px、行高 ≥ 1.7、充足對比
- **響應式**：手機版目錄收合為浮動按鈕
- **Single-file**：CSS/JS 全內嵌，零外部相依

套用 `interactive-html-report` 的 CSS 變數系統與 sticky TOC 元件（見該 skill）。章節錨點 id 對應目錄連結。

> 輕量版 prd-writer 短，目錄側欄可有可無；企業版因章節多，常駐目錄是剛需。

若使用者指定 Markdown、Word、PDF、Google Docs 或其他格式，應依指定格式輸出，此時不套用互動元件。

---

## 29. 回應策略

### 當資訊不足時

不要自行補齊關鍵商業規則。

應：

1. 先根據現有資訊產出可完成的部分。
2. 將缺失內容整理為 Open Questions。
3. 對可合理推導但未確認的內容標記為 Assumption。
4. 不因資訊不足而只回覆一串問題；優先交付部分成果。

### 當使用者提供既有 PRD 時

應先進行 Gap Analysis：

- 缺少哪些核心章節
- 哪些 AC 不可測試
- 哪些規則互相衝突
- 哪些內容混合了技術決策
- 哪些 Scope 不清楚
- 哪些 Edge Case 尚未處理
- 哪些 NFR、權限、監控、上線與回退缺失

然後再提供修正版。

### 當文件過大時

可以拆分為：

- Master PRD
- Feature Spec
- API Contract
- Permission Matrix
- NFR
- Rollout Plan
- UAT Plan
- Decision Log

避免單一文件失控。

---

## 30. 最終原則

這個 skill 不追求「看起來很完整」。

它追求的是：

- 每條規則都能被實作
- 每項需求都能被驗證
- 每個邊界都能被討論
- 每個未知都被誠實標記
- 每個版本都有清楚邊界
- 每次上線都有可觀測性
- 每個失敗都有恢復策略
- 每個技術決策都有正確 Owner

PRD 的價值，不在於它寫了多少，而在於它消除了多少不必要的猜測。
