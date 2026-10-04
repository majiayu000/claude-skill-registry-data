--- 
name: Security-Principles
description: >
  政府機關資通系統防護基準 Skill，涵蓋數位發展部資通安全署公告之
  7 大安全構面、27 類控制措施類別、80 項控制措施。
  使用時機：(1) SSDLC 各階段需要進行資安檢核時
  (2) @init 初始化專案時選用資安防護等級（general/medium/high）
  (3) 設計資通系統安全架構或撰寫 RFP 資安需求時
  (4) 準備資安稽核文件、弱點掃描、滲透測試時
  (5) 提及「資安檢核」「防護基準」「資通安全」「稽核」「OWASP」「威脅建模」時
---

# Security-Principles

依據數位發展部資通安全署《資通系統防護基準驗證實務 v1.3》（115 年 6 月）
及臺北市政風處《資安稽核與個資防護手冊》建立之資通系統安全檢核 Skill。

> 完整說明文件請參閱 `README.md`。
> 
> **本 Skill 目錄結構**：共 19 個檔案，包含 8 份構面參考文件、3 份等級檢核表、4 份原始 PDF、2 份核心說明檔、1 份 UI 中繼資料、1 支腳本。


## 適用對象

- SSDLC 六階段之 Planner / Generator / Evaluator

## 使用方式

### 1. 專案初始化（@init）

於 `@init` 執行時，詢問使用者是否導入本 Skill。若同意，依選定等級（general / medium / high）
執行 `scripts/generate_checklist.py <等級>`，將檢核表寫入 `outputs/` 目錄。

### 2. 階段中途檢核（@security-check）

```
@security-check general    # 普級檢核（58 項）
@security-check medium     # 中級檢核（70 項）
@security-check high       # 高級檢核（80 項）
```

口語觸發：「執行資安檢核」「以普級防護基準檢查」「資通安全稽核」

**執行步驟**：
1. 載入對應等級檢核表（`assets/checklist_*.md`）
2. 根據當前 SSDLC 階段，篩選適用構面（參照下方對照表）
3. 逐項比對系統產出是否符合控制措施要求（**比對範圍參照 
references/check_scope_per_domain.md**，每個構面的比對對象、比對方式與判定基準均有明確定義）
4. 產出檢核報告至 outputs/security_check_report.md（**報告格式參照 assets/security_check_report_template.md**，含檢核摘要、逐項結果、階段性限制說明、重點風險、改善建議）
5. **⚠️ 階段性限制免責聲明（必須執行）**：若檢核結果存在部分符合或不符合項目，且其原因非屬軟體設計或開發實作缺陷（如：需正式 TLS 憑證但處於本機開發階段、涉及硬體/機房實體安全、需組織管理程序），則報告必須包含「階段性限制說明」章節，逐項標註不符合原因與是否為階段性限制，避免閱讀者誤判為設計或實作缺陷。

6. **⚠️ 構面 8 處理規則**：構面 8（組織、實體與供應鏈安全）為「非軟體因子」，在軟體開發專案中預設標記為 ➖ 不適用。僅當專案明確涉及外部服務商整合時，才對「供應鏈管理」子類別進行存在性檢查。檢核報告中構面 8 獨立成章，並在階段性限制說明中統一註明。
7. 存入當前階段 `outputs/security_check_report.md`

### 2.5 階段中途彈性導入（@security-load）

```
@security-load               # 列出 8 構面清單供選擇
@security-load general       # 全構面普級導入
@security-load medium 1,4,6  # 僅導入存取控制+識別鑑別+通訊保護，中級
@security-load high 2,3      # 僅導入日誌+備援，高級
```

口語觸發：「導入安全防護」「載入資安構面」「只加存取控制和日誌」

**執行步驟**：
1. 讀取 `README.md` 構面對照表，列出 8 構面清單供使用者選擇
2. 依選定等級與構面，載入對應 `references/0X_*.md`
3. 執行相容性檢查後寫入當前階段 `SKILL.md`
4. 更新 `phase_gates.json` 中 `security_baseline.domains`
5. 呼叫 `scripts/generate_checklist.py` 產生階段專屬檢核表

### 3. 相容性檢查


每次載入本 Skill 時，自動比對現有 6 階段 Skill 內容：
- 重複規則 → `[INFO]` 提示
- 衝突規則 → `[WARN]` 警示，暫停等候確認
- 無衝突 → `[OK]` 繼續

## 7 構面 vs SSDLC 階段對照

| 構面 | 控制措施類別 | 主要適用階段 |
|------|------------|------------|
| 1. 存取控制 | 帳號管理、最小權限、遠端存取 | Phase 2 + Phase 3 |
| 2. 事件日誌與可歸責性 | 記錄、格式、校時、保護 | Phase 3 + Phase 6 |
| 3. 營運持續計畫 | 備份、備援 | Phase 5 + Phase 6 |
| 4. 識別與鑑別 | 驗證、密碼、多因子 | Phase 2 + Phase 3 |
| 5. 系統與服務獲得 | SSDLC 全階段、威脅建模、OWASP | Phase 1~5 |
| 6. 系統與通訊保護 | TLS、憑證、加密 | Phase 2 + Phase 3 |
| 7. 系統與資訊完整性 | 漏洞修復、監控、輸入驗證 | Phase 4 + Phase 6 |

## 等級對照

| 等級 | 檢核表 | 控制措施數 |
|------|--------|:--:|
| 普 (General) | `assets/checklist_general.md` | 58 |
| 中 (Medium)  | `assets/checklist_medium.md`  | 70 |
| 高 (High)    | `assets/checklist_high.md`    | 80 |

各等級均含臺北市政府 15 類資訊使用管理稽核項目。

## 腳本

```bash
python scripts/generate_checklist.py general
python scripts/generate_checklist.py medium
python scripts/generate_checklist.py high
```

## 參考文件

- `references/01_access_control.md` — 存取控制
- `references/02_audit_logging.md` — 事件日誌與可歸責性
- `references/03_bcp.md` — 營運持續計畫
- `references/04_auth.md` — 識別與鑑別
- `references/05_acquisition.md` — 系統與服務獲得
- `references/06_comm_protection.md` — 系統與通訊保護
- `references/07_integrity.md` — 系統與資訊完整性
- `references/08_organizational.md` — 組織、實體與供應鏈安全（非軟體開發因子）
- `references/source/` — 原始 PDF 文件
- `references/08_organizational.md` — 組織/實體/供應鏈補充篇
