---
name: agent-ide
description: |
  TS/JS 程式碼智能重構工具。執行以下操作時自動選用：
  - 重命名符號 → /rename（取代逐一 Edit）
  - 移動/重組檔案 → /move（取代 Write+Delete）
  - 理解專案架構 → /snapshot（取代逐檔 Read）
  - 清理未使用程式碼 → /deadcode
  - 修改函式參數 → /change-signature
  - 檢測循環依賴 → /cycles
  - 分析變更影響 → /impact
  - 查找符號引用 → /find-references
  - 追蹤呼叫層次 → /call-hierarchy
  優勢：自動更新所有引用、一次完成、零遺漏
---

# Agent IDE

TS/JS 程式碼智能重構工具，透過 slash commands 操作。

## 可用命令

| 命令 | 用途 |
|------|------|
| `/snapshot` | 專案/模組 API 快照 |
| `/cycles` | 循環依賴檢測 |
| `/impact` | 變更影響分析 |
| `/find-references` | 符號引用查找 |
| `/call-hierarchy` | 呼叫層次追蹤 |
| `/rename` | 重命名符號 + 自動更新引用 |
| `/move` | 移動檔案/成員 + 自動更新 import |
| `/change-signature` | 修改函式參數 + 更新呼叫點 |
| `/deadcode` | 檢測/清理未使用程式碼 |

## 最佳實踐

### 重構標準流程

```text
1. /deadcode     → 清理未使用程式碼（清場）
2. /snapshot     → 了解專案架構（偵察）
3. /cycles       → 檢測循環依賴（診斷）
4. /move         → 重組檔案/成員（重構）
5. /rename       → 修正命名風格（收尾）
```

### 場景選用指南

| 場景 | 命令 | 說明 |
|------|------|------|
| 接手新專案 | `/deadcode` → `/snapshot` | 先清垃圾，再看全貌 |
| 重構前診斷 | `/cycles` → `/impact` | 找問題點，評估影響範圍 |
| 檔案重組 | `/move src/a.ts src/b/` | 自動更新所有 import |
| 抽取函式 | `/move src/a.ts:25 src/b.ts` | 移動成員到新位置 |
| 統一命名 | `/rename --from userId --to uid` | 全專案一致性 |
| 修改 API | `/change-signature` | 參數順序/名稱變更 |
| 追蹤呼叫 | `/call-hierarchy` → `/find-references` | 理解函式使用情況 |

### 安全操作原則

1. **先 `--dry-run` 再執行**：變更類命令務必預覽
2. **清理優先於重構**：`/deadcode` 減少不必要的移動/重命名
3. **小步快跑**：一次只做一種類型的變更，便於回滾
4. **重構後驗證**：`/cycles` 確保沒引入循環依賴
