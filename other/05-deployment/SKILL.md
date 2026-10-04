---
name: 05_deployment
description: 部署階段，負責建置成品打包、多服務依賴部署、伺服器組態自動產生、遠端批次部署、數位簽章寫入及部署環境型態完整性（SHA-256）驗證。
---

# 部署階段技能 (05_deployment)

> 📌 本階段的完整 PDCA 規範定義於框架 `.agents/skills/05_deployment/SKILL.md`。本檔案為專案層級整合定義，Skill 導入後自動合併。

## 已導入 Skill

> 尚無 Skill 導入。請使用 `@05` 查詢可用 Skill 並以 `@05/XX` 導入。

## 安全防護整合（條件式）

> 🔒 **已啟用**：普級防護基準 (general)，`phase_gates.json` → `security_baseline.enabled = true`

*   **適用安全構面**：構面 3（營運持續計畫）、構面 6（系統與通訊保護）
*   **對應參考文件**：`../external-resources/Security-Principles/references/03_bcp.md`、`../external-resources/Security-Principles/references/06_comm_protection.md`
*   **對應等級檢核表**：`../external-resources/Security-Principles/assets/checklist_general.md`（構面 3/6 控制措施）
*   **Planner 安全職責**：規劃 HTTPS/TLS 1.2+ 配置、資料庫連線字串加密、備份排程設定、安全組態鎖定（關閉不必要的服務與埠口）。
*   **Generator 安全產出**：`outputs/sbom.json`、`outputs/.env.example`、`outputs/security_deployment_checklist.md`、`outputs/security_deploy_report.md`
*   **參照框架層**：`.agents/skills/05_deployment/SKILL.md` 安全整合段落
