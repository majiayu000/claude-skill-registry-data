---
name: 02_system_design
description: 系統設計階段，負責承接正規化需求並產出七項標準設計交付物：DB Schema、ER 圖、API 規格、UI 雛型、使用案例圖、活動圖、時序圖。
---
> 匯入日期：2026-06-29 | 匯入指令：`@02/04,05,08,10,11,12,13,17`
> 匯入 Skill：brand-guidelines(04), canvas-design(05), frontend-design(08), mermaid(10), openapi_generator(11), plantuml(12), prisma(13), theme-factory(17)

---

## brand-guidelines 規範

- **名稱**：brand-guidelines
- **用途**：品牌色彩與字型規範套用（Anthropic 官方風格）。適用於需要品牌一致性、視覺格式化或公司設計標準的場景。
- **來源**：Anthropic Skills

---

## canvas-design 規範

- **名稱**：canvas-design
- **用途**：建立靜態視覺藝術（.png / .pdf），使用設計哲學進行創作。適用於海報、藝術品、設計稿等靜態作品。禁止複製既有藝術家作品。
- **來源**：Anthropic Skills

---

## frontend-design 規範

- **名稱**：frontend-design
- **用途**：前端視覺設計指引 — 在建立新 UI 或重塑既有 UI 時，提供獨特、有意識的視覺方向。涵蓋排版、字型、配色、動畫與版面決策，避免模板化的預設外觀。
- **來源**：Anthropic Skills

### 設計原則
1. **扎根於主題**：從產品/主題本身的世界尋找獨特設計線索。
2. **字型承載個性**：慎選 Display 與 Body 字型配對，讓字型處理本身成為難忘的設計元素。
3. **結構即資訊**：編號、分隔線、標籤應編碼內容的真實意義，而非裝飾。
4. **善用動態**：考慮動畫服務主題的時機（頁面載入序列、滾動觸發、hover 微互動）。
5. **複雜度匹配願景**：極繁方向需精緻執行；極簡方向需間距/字型/細節的精準。

### 流程：腦力激盪 → 探索 → 規劃 → 批判 → 建構 → 再次批判
- 兩階段工作：先產出設計計畫（色彩 4-6 色、字型 2+ 角色、版面概念、簽名元素），再審查後實作。
- 把大膽用在一處，其餘保持克制。
- 響應式至手機、可見鍵盤焦點、尊重 reduced motion。

---

## mermaid 規範

- **名稱**：mermaid
- **用途**：以文字繪製專案流程圖、系統架構圖、ER 圖與狀態圖。
- **歸屬階段**：02_system_design
- **GitHub**：https://github.com/mermaid-js/mermaid
- **來源**：本機外部資源
- **替代功能**：可替代 sa-design 的系統架構圖與流程圖產出功能
- **支援圖表**：flowchart（流程圖）、erDiagram（ER 圖）、sequenceDiagram（時序圖）、stateDiagram（狀態圖）

---

## openapi_generator 規範

- **名稱**：openapi_generator
- **用途**：自動產生符合 OpenAPI 規格的 API 文件與介面程式碼。
- **歸屬階段**：02_system_design
- **GitHub**：https://github.com/OpenAPITools/openapi-generator
- **來源**：本機外部資源
- **替代功能**：可替代 sa-design 的 API spec 產出功能
- **支援格式**：OpenAPI 3.0/3.1 YAML/JSON、多語言 SDK 產生

---

## plantuml 規範

- **名稱**：plantuml
- **用途**：UML 圖表工具：用例圖、活動圖、時序圖、部署圖等。
- **歸屬階段**：02_system_design
- **來源**：本機外部資源
- **替代功能**：可替代 sa-design 的 UML 圖表產出功能
- **支援圖表**：Use Case（用例圖）、Activity（活動圖）、Sequence（時序圖）、Deployment（部署圖）

---

## prisma 規範

- **名稱**：prisma
- **用途**：資料庫實體關係圖 (ER Model)、Schema 定義與 SQL DDL 產生工具。
- **歸屬階段**：02_system_design
- **GitHub**：https://github.com/prisma/prisma
- **來源**：本機外部資源
- **替代功能**：可替代 sa-design 的 ER 圖與資料字典產出功能

---

## theme-factory 規範

- **名稱**：theme-factory
- **用途**：主題工廠 — 提供 10 組預設專業色彩/字型主題，或即時生成新主題，可套用至任何成品（簡報、文件、報表、HTML 頁面等）。
- **來源**：Anthropic Skills

---

> 以上 8 個 Skill 已於 2026-06-29 透過 `@02/04,05,08,10,11,12,13,17` 聯合導入至 `myPrj/02_system_design/`。
> 各 Skill 完整原始檔位於對應同名子目錄中。
> **2026-07-10 更新**：移除 sa-design（Benson 敏感來源清理），由 prisma + mermaid + plantuml + openapi_generator 組合替代其功能。

# 系統設計階段技能 (02_system_design)

> 📌 本階段的完整 PDCA 規範定義於框架 `.agents/skills/02_system_design/SKILL.md`。本檔案為專案層級整合定義，Skill 導入後自動合併。

## 已導入 Skill

| 快捷編號 | Skill 名稱 | 用途 | 替代功能 |
|:---:|:---|:---|:---|
| 04 | brand-guidelines | 品牌色彩與字型規範套用 | — |
| 05 | canvas-design | 建立靜態視覺藝術（.png/.pdf） | — |
| 08 | frontend-design | 前端視覺設計指引 | — |
| 10 | mermaid | 以文字繪製流程圖、架構圖、ER 圖 | 替代 sa-design 系統架構圖 |
| 11 | openapi_generator | 自動產生 OpenAPI 規格文件 | 替代 sa-design API spec |
| 12 | plantuml | UML 圖表工具 | 替代 sa-design UML 圖表 |
| 13 | prisma | 資料庫 ER 圖與 SQL DDL 產生 | 替代 sa-design ER 圖與資料字典 |
| 17 | theme-factory | 主題工廠 | — |

## 安全防護整合（條件式）

> 🔒 **已啟用**：普級防護基準 (general)，`phase_gates.json` → `security_baseline.enabled = true`

*   **適用安全構面**：構面 1（存取控制）、構面 4（識別與鑑別）、構面 6（系統與通訊保護）
*   **對應參考文件**：`../external-resources/Security-Principles/references/01_access_control.md`、`../external-resources/Security-Principles/references/04_auth.md`、`../external-resources/Security-Principles/references/06_comm_protection.md`
*   **對應等級檢核表**：`../external-resources/Security-Principles/assets/checklist_general.md`（構面 1/4/6 控制措施）
*   **Planner 安全職責**：讀取構面 1/4/6 控制措施，規劃 RBAC 角色矩陣、認證流程、加密架構（TLS/憑證/資料加密），納入設計簡報。
*   **Generator 安全產出**：`outputs/rbac_matrix.md`（角色權限矩陣）、`outputs/auth_flow.md`（認證流程圖）、`outputs/crypto_architecture.md`（加密架構圖）
*   **參照框架層**：`.agents/skills/02_system_design/SKILL.md` 安全整合段落
