---
name: 04_testing
description: 測試驗證階段，負責雙軌測試執行（pytest API 測試 + Playwright UI 測試）、Bug 追蹤與分類、測試覆蓋率報告產出，以及回歸測試策略制定。
---
> 匯入日期：2026-06-29 | 匯入指令：`@04/01,04,05,09,10,11`
> 匯入 Skill：coverage_py(01), playwright(04), pytest(05), sonarqube(09), systematic-debugging(10), webapp-testing(11)

---

## pytest 規範
- **用途**：Python 單元測試與 API 功能驗證
- **本專案**：針對 `app.py` 中的 35+ 路由進行 API 測試（200/201/401/403/422 狀態碼驗證）

## playwright 規範
- **用途**：UI 自動化測試與跨瀏覽器兼容性回歸測試
- **本專案**：驗證登入流程、RBAC 選單顯示、ESS 自助修改、報表載入

## coverage_py 規範
- **用途**：Python 測試覆蓋率分析
- **本專案**：產出 `test_results.md` 中的覆蓋率報告

## sonarqube 規範
- **用途**：代碼安全漏洞、壞味道與品質靜態掃描
- **本專案**：掃描 `app.py`、`models.py` 的安全性問題

## systematic-debugging 規範
- **用途**：系統化 Bug 除錯流程
- **本專案**：Bug 追蹤與分類記錄於 `bug/bug_tracker.md`

## webapp-testing 規範
- **用途**：Playwright Web 應用測試工具包
- **本專案**：輔助 playwright 進行瀏覽器截圖、日誌擷取

# 測試驗證階段技能 (04_testing)

> 📌 本階段的完整 PDCA 規範定義於框架 `.agents/skills/04_testing/SKILL.md`。本檔案為專案層級整合定義，Skill 導入後自動合併。

## 已導入 Skill

> 尚無 Skill 導入。請使用 `@04` 查詢可用 Skill 並以 `@04/XX` 導入。

## 安全防護整合（條件式）

> 🔒 **已啟用**：普級防護基準 (general)，`phase_gates.json` → `security_baseline.enabled = true`

*   **適用安全構面**：構面 5（系統與服務獲得—測試階段）、構面 7（系統與資訊完整性）
*   **對應參考文件**：`../external-resources/Security-Principles/references/05_acquisition.md`、`../external-resources/Security-Principles/references/07_integrity.md`
*   **對應等級檢核表**：`../external-resources/Security-Principles/assets/checklist_general.md`（構面 5/7 控制措施）
*   **Planner 安全職責**：選定 SAST 工具（如 Bandit/SonarQube）、弱點掃描工具、滲透測試範圍，納入測試計畫。
*   **Generator 安全產出**：`outputs/dast_report.md`、`outputs/zap_report.html`、`outputs/security_test_report.md`
*   **參照框架層**：`.agents/skills/04_testing/SKILL.md` 安全整合段落
