---
name: file-restructurer
description: |
  Restructure project files, reorganize folders, and modularize code.
  LOAD THIS SKILL WHEN: Project structure is messy | User says "整理資料夾", "重構結構", "reorganize", "模組化" | files exceed 500 lines | need DDD folder structure.
  CAPABILITIES: Folder reorganization, module splitting, import path updates, backup/rollback, dry-run preview.
---

# 檔案重構技能

## 描述
重組專案檔案結構，整理資料夾，進行模組化重構。

## 觸發條件
- 「重構檔案結構」
- 「整理資料夾」
- 「模組化」
- Workflow 中的重構步驟

## 重構類型

### 1. 資料夾結構重組
```
Before:
├── app.py
├── utils.py
├── database.py
├── models.py
└── tests.py

After:
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   └── database.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
└── tests/
    ├── __init__.py
    └── test_models.py
```

### 2. 模組拆分
```
Before:
utils.py (500 行)

After:
utils/
├── __init__.py
├── string_utils.py
├── date_utils.py
├── file_utils.py
└── validation.py
```

### 3. Import 路徑更新
自動更新所有受影響檔案的 import 語句

## 執行流程
```
1. 分析當前結構
2. 生成重構計畫
3. 預覽變更（dry-run）
4. 使用者確認
5. 執行重構
6. 更新 imports
7. 驗證功能正常
8. 生成報告
```

## 安全機制

### 備份機制
```bash
# 自動建立備份
.backup/
└── [timestamp]/
    └── [原始結構複製]
```

### 回滾機制
```
如需回滾，執行：
git checkout HEAD -- .
或
從 .backup/[timestamp]/ 還原
```

## 輸出格式
```
🔧 檔案重構報告

═══════════════════════════════════════

📊 重構摘要：
  - 移動檔案：12 個
  - 新建資料夾：5 個
  - 更新 imports：23 處

═══════════════════════════════════════

📁 結構變更：

移動的檔案：
  📄 utils.py → src/utils/helpers.py
  📄 models.py → src/core/models.py
  📄 database.py → src/infrastructure/database.py

新建的資料夾：
  📁 src/
  📁 src/core/
  📁 src/infrastructure/
  📁 src/utils/
  📁 tests/

更新的 imports：
  📄 app.py: 5 處
  📄 test_models.py: 3 處

═══════════════════════════════════════

✅ 重構完成！

⚠️ 建議執行：
1. 運行測試確認功能正常
2. 檢查 IDE 是否正確識別新結構
3. 提交變更到 Git
```

## 使用範例
```
「重構為 DDD 結構」
「整理 utils 資料夾」
「模組化 services.py」
「--dry-run 預覽重構」
```

```
