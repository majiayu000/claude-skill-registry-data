---
name: 06_maintenance
description: 維護與監控階段，負責線上運行日誌收集與分析、錯誤原因萃取、系統硬體與效能監控、程式執行軌跡追蹤、熱修補（Hotfix）程式編寫及回歸測試。
---

# 維護與監控階段技能 (06_maintenance)

> 📌 本階段的完整 PDCA 規範定義於框架 `.agents/skills/06_maintenance/SKILL.md`。本檔案為專案層級整合定義，Skill 導入後自動合併。

## 已導入 Skill

> 尚無 Skill 導入。請使用 `@06` 查詢可用 Skill 並以 `@06/XX` 導入。

## 安全防護整合（條件式）

> 🔒 **已啟用**：普級防護基準 (general)，`phase_gates.json` → `security_baseline.enabled = true`

*   **適用安全構面**：構面 2（事件日誌與可歸責性）、構面 3（營運持續計畫）、構面 7（系統與資訊完整性）
*   **對應參考文件**：`../external-resources/Security-Principles/references/02_audit_logging.md`、`../external-resources/Security-Principles/references/03_bcp.md`、`../external-resources/Security-Principles/references/07_integrity.md`
*   **對應等級檢核表**：`../external-resources/Security-Principles/assets/checklist_general.md`（構面 2/3/7 控制措施）
*   **Planner 安全職責**：規劃日誌審查排程、NTP 校時驗證、日誌完整性雜湊檢查、漏洞修補排程（Critical 7天/High 30天）、定期備份還原測試、備援切換演練。
*   **Generator 安全產出**：`outputs/security_trend.md`、`outputs/vulnerability_advisory.md`
*   **參照框架層**：`.agents/skills/06_maintenance/SKILL.md` 安全整合段落
