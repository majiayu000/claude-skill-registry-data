---
name: doc-structure
description: |
  專案文檔結構管理工具，用於建立、維護和驗證專案的層級聚攏文檔結構。
  使用時機：
  - 當需要建立新的 README.md 文件
  - 當需要為程式檔案添加標準化開頭註解
  - 當重構或更新專案文檔結構
  - 當需要驗證 README 連結有效性
  - 當需要檢查文檔結構完整性
  關鍵字：README、文檔結構、層級聚攏、檔案註解、連結驗證、結構檢查
---

# 文檔結構管理 Skill

## 設計意義

標準化專案文檔結構，確保所有 README 和檔案註解格式一致，避免資訊重複和認知負擔。

## 核心理念：層級聚攏結構

```
CLAUDE.md（根）─ 專案規範 + 頂層目錄索引
    │
    ├── {dir}/README.md（上層）─ 設計意義 + 索引 + 參考
    │       │
    │       └── {subdir}/README.md（下層）─ 設計意義 + 索引 + 參考
    │               │
    │               └── {file}.js ─ 檔案頂部註解（Position + Input + Output + 職責）
```

**三個原則**：
1. **上層索引下層**：每個 README 只負責索引直接下層內容
2. **設計意義穩定**：說明「為什麼」，不隨程式修改而變
3. **重構才重寫**：只有架構變動時才更新設計意義

## 使用流程

### 建立新 README

1. 確定目錄層級（頂層 or 子目錄）
2. 讀取對應模板：
   - 頂層：[templates/readme-top.md](templates/readme-top.md)
   - 子目錄：[templates/readme-sub.md](templates/readme-sub.md)
3. 填入三個必要欄位：設計意義、索引、參考
4. 確認不包含禁止內容

### 添加檔案註解

1. 確定檔案類型，選擇對應模板：

   | 語言 | 模板 |
   |------|------|
   | JavaScript/TypeScript | [header-js.txt](templates/header-js.txt) |
   | Python | [header-py.txt](templates/header-py.txt) |
   | Dart | [header-dart.txt](templates/header-dart.txt) |
   | Go | [header-go.txt](templates/header-go.txt) |
   | HTML | [header-html.txt](templates/header-html.txt) |
   | PHP | [header-php.txt](templates/header-php.txt) |
   | Java | [header-java.txt](templates/header-java.txt) |
   | C# (.NET) | [header-csharp.txt](templates/header-csharp.txt) |
   | YAML | [header-yaml.txt](templates/header-yaml.txt) |
   | Shell/Bash | [header-shell.txt](templates/header-shell.txt) |

   **不支援註解的格式**：JSON、Markdown、純資料檔案 → 由 README 說明

   **自動排除**：名稱包含 `log` 的資料夾和檔案（不區分大小寫）

2. 填入四個必要欄位：
   - **Position**：功能定位（在系統架構中的位置和角色）
   - **Input**：外部依賴（依賴哪些模組或服務）
   - **Output**：對外提供（導出的介面、類別或函數）
   - **職責**：做什麼（1-3 項主要職責）

## 驗證工具

### 連結驗證

驗證所有 README.md 的內部連結是否有效：

```bash
# 使用當前目錄
uv run validate-readme-links.py

# 指定專案路徑
uv run validate-readme-links.py /path/to/project
```

### 結構檢查

檢查預期的 README.md 是否存在：

```bash
# 使用當前目錄
uv run check-doc-structure.py

# 指定專案路徑
uv run check-doc-structure.py /path/to/project
```

## 參考文檔

- [README 格式標準](references/readme-format.md)
- [檔案註解標準](references/file-header-format.md)
