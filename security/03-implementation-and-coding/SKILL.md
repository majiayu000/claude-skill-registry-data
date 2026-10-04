---
name: 03_implementation_and_coding
description: 開發與編碼階段，負責將設計規格拆解為微小任務，進行 AI 輔助程式碼實作、代碼規範檢查、自動格式化、單元測試撰寫以及跨模組依賴整合管理。
---
> 匯入日期：2026-06-29 | 匯入指令：`@03/03,13`
> 匯入 Skill：code-simplifier(03), prettier(13)

---

## code-simplifier 規範

- **名稱**：code-simplifier
- **用途**：代碼簡化與重構 — 在不改變功能的前提下，提升代碼清晰度、一致性與可維護性。專注於最近修改的代碼，保持可讀性優先於極簡寫法。
- **來源**：Anthropic Skills

### 核心原則
- 保留所有既有功能，不改變行為
- 優先使用專案既有的最佳實踐與慣例
- 明確、可讀的代碼優於過度緊湊的寫法
- 僅簡化最近修改過的代碼（除非另有指示）

---

## prettier 規範

- **名稱**：prettier
- **用途**：代碼風格美化與自動格式化，避免團隊排版衝突。適用於 HTML、CSS、JavaScript 檔案。
- **歸屬階段**：03_implementation_and_coding
- **來源**：本機外部資源

### 使用時機
- 在提交代碼前自動格式化
- 確保團隊代碼風格一致
- 本專案用於 `ui_prototype.html` 中的 HTML/CSS/JS 格式化

---

---

> 尚無 Skill 導入。請使用 `@03` 查詢可用 Skill 並以 `@03/XX` 導入。

## 安全防護整合（條件式）

> 🔒 **已啟用**：普級防護基準 (general)，`phase_gates.json` → `security_baseline.enabled = true`

*   **適用安全構面**：構面 1（存取控制）、構面 2（事件日誌）、構面 4（識別與鑑別）、構面 5（系統與服務獲得）、構面 6（系統與通訊保護）
*   **對應參考文件**：`../external-resources/Security-Principles/references/01_access_control.md`、`../external-resources/Security-Principles/references/02_audit_logging.md`、`../external-resources/Security-Principles/references/04_auth.md`、`../external-resources/Security-Principles/references/05_acquisition.md`、`../external-resources/Security-Principles/references/06_comm_protection.md`
*   **對應等級檢核表**：`../external-resources/Security-Principles/assets/checklist_general.md`（構面 1/2/4/5/6 控制措施）
*   **Planner 安全職責**：選定安全編碼規範（OWASP Top 10 防範、輸入驗證、帳號鎖定、日誌框架、HTTPS 強制），納入任務清單 `task_list.json` 的安全需求欄位。
*   **Generator 安全產出**：`outputs/security_check_report.md`、`outputs/security_scan_report.json`
*   **參照框架層**：`.agents/skills/03_implementation_and_coding/SKILL.md` 安全整合段落
