---
name: external-resource-workflow
description: "外部第三方資源管理：引入、移除、查詢，確保 external-resources/ 目錄結構完整一致。"
version: 1.1.0
---

# External Resource Workflow — 外部第三方資源管理

> 適用階段：00_cross_phase（跨階段全域共用）

本文件定義 `@external-resource` 指令體系的完整操作規範，確保第三方 Skill 的引入、移除與查詢流程一致且可追溯。

---

## 指令總覽

| 指令 | 功能 | 口語觸發 |
|:-----|:-----|:---------|
| `@external-resource add <URL>` | 引入第三方 Skill | 「引入外部 Skill」「新增第三方資源」 |
| `@external-resource remove <名稱>` | 移除第三方 Skill | 「移除外部 Skill」「刪除第三方資源」 |
| `@external-resource list` | 列出所有外部資源 | 「查看外部資源」「列出第三方 Skill」 |

---

## 一、`@external-resource add <URL>` — 引入

### 1.1 前置條件

AI 代理執行前必須確認：
- 已讀取本文件（`external-resources/SKILL.md`）
- 已讀取 `external-resources/README.md` 的目前資源清單
- 已讀取根目錄 `.gitignore` 的尾段排除規則

### 1.2 執行步驟

#### Step 1 — 分析來源

1. 確認 URL 為有效的 GitHub repo 連結
2. Clone 或下載至暫存目錄
3. 閱讀來源 README，確認以下四項：

| 確認項目 | 說明 |
|:---------|:-----|
| 授權類型 | MIT / Apache 2.0 / 其他，不得與框架現有授權衝突 |
| 核心功能 | 精準描述用途（限 15 字以內） |
| 外部依賴 | 是否需要 API Key 或其他服務 |
| 功能重疊 | 與 `external-resources/` 現有目錄交叉比對，若高度重疊則詢問使用者 |

#### Step 2 — 下載與放置

1. 將來源複製到 `external-resources/<skill-name>/`
   - `<skill-name>` 取 repo 名稱，去除版本後綴（如 `ui-ux-pro-max-skill-2.6.2` → `ui-ux-pro-max-skill`）
   - 移除 `.git/` 與 `.github/` 目錄
2. 建立 `url.txt` 索引：

```
https://github.com/<owner>/<repo>
Version: <版本號，若已知>
License: <授權類型>
```

#### Step 3 — 更新 `README.md` 資源清單

在「📦 資源清單」表格中新增一列（按目錄名字母排序）：

```
| `<目錄名>/` | [repo 名稱](GitHub URL) | <授權類型> | <功能簡述> |
```

#### Step 4 — 更新 `.gitignore`

在根目錄 `.gitignore` 的「外部第三方 Skill 原始碼」區塊追加：

```gitignore
external-resources/<skill-name>/*
!external-resources/<skill-name>/url.txt
```

> 若規則已存在，不得重複新增。

#### Step 5 — 更新引用警語模板

同步更新 `external-resources/README.md` 中「📋 引用警語模板」區塊：
- **專案根目錄 README.md 追加區塊**：在聲明表格中新增該資源的列
- **.gitignore 追加規則**：在規則區塊中追加該目錄的排除行

#### Step 6 — 驗證並報告

| 檢查項目 | 驗證方式 | 通過標準 |
|:---------|:---------|:---------|
| 目錄存在 | `external-resources/<skill-name>/` 存在 | ✅ |
| url.txt 完整 | 含 GitHub URL | ✅ |
| README 表格同步 | 資源清單表格含新增列 | ✅ |
| .gitignore 正確 | `git check-ignore` 原始碼被排除、`url.txt` 不被排除 | ✅ |
| 授權合規 | 不與框架現有授權衝突 | ✅ |
| 功能無重疊 | 與現有 Skill 無高度重複 | ✅（有重疊需告知使用者） |

---

## 二、`@external-resource remove <名稱>` — 移除

### 2.1 執行步驟

| 步驟 | 操作 |
|:-----|:-----|
| 1 | 確認要移除的目錄名稱（顯示該目錄的來源與說明，讓使用者二次確認） |
| 2 | 刪除 `external-resources/<skill-name>/` 目錄 |
| 3 | 從 `external-resources/README.md` 資源清單表格中移除該列 |
| 4 | 從 `external-resources/README.md` 引用警語模板中移除該列 |
| 5 | 從根目錄 `.gitignore` 中移除該目錄的排除 + negation 規則（2 行） |
| 6 | 向使用者報告清理結果（已刪除項目 + 殘留確認） |

---

## 三、`@external-resource list` — 查詢

### 3.1 執行步驟

1. 掃描 `external-resources/` 目錄下所有子目錄
2. 讀取每個子目錄的 `url.txt` 索引（若有）
3. 以表格輸出：

| 目錄 | 來源 | 授權 | 說明 |
|:-----|:-----|:-----|:-----|
| `<name>/` | GitHub URL | 授權類型 | 功能簡述 |

---

## 四、目錄結構規範

完成引入後，`external-resources/` 的結構應為：

```
external-resources/
├── README.md                    # 資源清單 + 引用警語 + 指令操作說明
├── SKILL.md                     # 本工作流程文件
├── <skill-name>/
│   ├── url.txt                  # 來源索引（唯一入庫的子目錄檔案）
│   ├── LICENSE                  # 授權檔（若有）
│   ├── README.md                # 來源原始 README
│   ├── SKILL.md                 # Skill 定義（若有）
│   └── ...                      # 其他來源檔案
└── ...
```

**Git 追蹤規則**：

| 類別 | 追蹤 | 說明 |
|:-----|:-----|:-----|
| `README.md`、`SKILL.md` | ✅ 入庫 | 框架管理文件 |
| 各子目錄 `url.txt` | ✅ 入庫 | 來源索引 |
| 第三方原始碼、腳本 | ❌ 不入庫 | 由 `.gitignore` 排除 |
| `.env`、`runtime.conf` | ❌ 不入庫 | 含敏感資訊或本機設定 |
| `.git/`、`.github/` | ❌ 不入庫 | 引入時主動移除 |

---

## 五、範例

### 引入

```
使用者：幫我引入這個外部 Skill https://github.com/nextlevelbuilder/ui-ux-pro-max-skill

AI 執行流程：
1. Clone → 確認 Apache 2.0 授權 → 無衝突
2. 放置到 external-resources/ui-ux-pro-max-skill/
3. 建立 url.txt
4. 更新 README.md 資源清單表格
5. 更新 .gitignore 排除規則
6. 更新引用警語模板
7. 驗證：目錄 ✅ / url.txt ✅ / README ✅ / gitignore ✅
```

### 移除

```
使用者：幫我移除 ui-ux-pro-max-skill

AI 執行流程：
1. 確認目標：external-resources/ui-ux-pro-max-skill/（MIT v2.6.2、UI/UX 設計智慧技能組）
2. 刪除目錄
3. 從 README.md 移除資源清單列與引用警語列
4. 從 .gitignore 移除排除規則
5. 報告：已刪除 1 個目錄、2 行 gitignore 規則、2 行 README 列
```

### 查詢

```
使用者：列出外部資源

AI 執行流程：
1. 掃描 external-resources/ 下所有子目錄
2. 讀取各 url.txt
3. 輸出資源清單表格
```
