---
name: 01_planning_and_analysis
description: 規劃與需求分析階段，負責原始需求釐清、口語需求正規化、需求追溯矩陣建置、Skill 複選與階段交付物定義。
---

# 規劃與需求分析階段技能 (01_planning_and_analysis)

> 📌 本階段的完整 PDCA 規範定義於框架 `.agents/skills/01_planning_and_analysis/SKILL.md`。本檔案為專案層級整合定義，Skill 導入後自動合併。

## 已導入 Skill

| 快捷編號 | 導入日期 | Skill 名稱 | 用途 |
|:---:|:---|:---|:---|
| 03 | 2026-06-29 | docling | 各式複雜文件（PDF, Word等）轉換為標準 Markdown 格式 |
| 06 | 2026-06-29 | file-organizer | 專案文件分類與整理工具，依標準架構歸類/命名 |
| 10 | 2026-06-29 | langchain | 需求場景拆解、語意整理與鏈式呼叫工具 |
| 12 | 2026-06-29 | meeting-record | 會議逐字稿 → EKB note + 投影片 + 配音影片，一條龍 |

## 安全防護整合（條件式）

> 🔒 **已啟用**：普級防護基準 (general)，`phase_gates.json` → `security_baseline.enabled = true`

*   **適用安全構面**：構面 5（系統與服務獲得—需求階段）
*   **對應參考文件**：`../external-resources/Security-Principles/references/05_acquisition.md`
*   **對應等級檢核表**：`../external-resources/Security-Principles/assets/checklist_general.md`（構面 5 控制措施）
*   **Planner 安全職責**：讀取構面 5 需求階段控制措施，將安全需求（CIA 等級定義、威脅建模要求、OWASP 防範需求）納入需求分析範圍。
*   **Generator 安全產出**：`outputs/security_requirements.md`（安全需求規格）
*   **參照框架層**：`.agents/skills/01_planning_and_analysis/SKILL.md` 安全整合段落

---

## docling 規範

> 📥 導入日期：2026-06-29 | 快捷編號：03 | 來源：`skills/01_planning_and_analysis/docling/`

### 適用開發階段
* 歸屬階段：01_planning_and_analysis

### 主要用途
* 各式複雜文件（PDF, Word等）轉換為標準 Markdown 格式工具。

### GitHub 原始倉庫
* [GitHub 連結](https://github.com/DS4SD/docling)

---

## file-organizer 規範

> 📥 導入日期：2026-06-29 | 快捷編號：06 | 來源：`skills/01_planning_and_analysis/file-organizer/`

### 專案文件分類與整理 (File Organizer)

核心任務：將使用者提供的檔案，依照標準分類架構進行精準歸類、標準化命名、產生完整資料夾路徑。

### 工作流程

#### Step 1：情報收集
在做任何分類之前，先搞清楚背景。不要光看檔名就猜。

1. **讀取專案清單**：先讀 `references/projects.md` 取得使用者的所有專案名稱
2. **盤點檔案**：掃描使用者指定的目錄，列出所有檔案
3. **辨識專案**：從檔名、資料夾結構，對照專案清單進行初步匹配
4. **向使用者確認**：用 AskUserQuestion 一次問清楚

#### Step 2：讀取檔案內容輔助判斷
對於檔名模糊的檔案，嘗試讀取內容來判斷（.docx/.md/.txt 讀前幾行、.xlsx 檢查 sheet 名稱、.zip 列出內部檔案清單）。

#### Step 3：依規範分類
讀取 `references/taxonomy.md` 取得完整的分類架構定義，然後逐一分類每個檔案。根據使用者提供的路徑，判斷使用「專案結構整理模式」或「扁平結構整理模式」。

---

## langchain 規範

> 📥 導入日期：2026-06-29 | 快捷編號：10 | 來源：`skills/01_planning_and_analysis/langchain/`

### 適用開發階段
* 歸屬階段：01_planning_and_analysis

### 主要用途
* 需求場景拆解、語意整理與鏈式呼叫工具。

### GitHub 原始倉庫
* [GitHub 連結](https://github.com/langchain-ai/langchain)

---

## meeting-record 規範

> 📥 導入日期：2026-06-29 | 快捷編號：12 | 來源：`skills/01_planning_and_analysis/meeting-record/`

### 核心用途
把會議逐字稿變成「EKB 知識資產 + 投影片 + 介紹影片」的一條龍 pipeline。

### 觸發條件
**啟用**：使用者丟出 `.md` / `.txt` 逐字稿、或說「會議紀錄」「整理會議」「彙整這份會議」「開會記錄」「跨進度會議」「會議影片」。

### 四階段 Pipeline
1. **Phase 1**：逐字稿 → 結構化紀錄 → EKB note（必跑）
2. **Phase 2**：結構化紀錄 → HTML/CSS 投影片（預設跑）
3. **Phase 3**：投影片 + 旁白稿 → 1.5x 配音影片（預設跑，可 skip）
4. **Phase 4**：全部上 EKB + 軟刪舊版（必跑）

### Phase 1 關鍵步驟
1. 完整讀逐字稿（不能只讀「會議記錄」段）
2. 問使用者三件事：會議正式名稱、與會名單+角色對照、EIP 專案 id
3. 校正語音錯字（參考 `references/pronunciation-corrections.yaml`）
4. 結構化 EKB note 內容
