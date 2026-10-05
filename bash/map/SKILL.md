---
name: map
description: 產出 codebase 語意符號地圖（classes、functions、interfaces、types 的精確 file:line 位置）。適合在大型重構前或接手陌生 codebase 時使用。
disable-model-invocation: true
context: fork
---

# Map — Codebase Symbol Map

## 觸發條件

- 開始大規模重構前，需要精確的符號位置
- 接手陌生 codebase，需要快速建立心智地圖
- 避免 Grep 在註解/字串中找到誤報
- 與 `prime` skill 搭配：prime 讀 README，map 產出符號索引

## 執行方式

```bash
# 在專案根目錄執行（輸出存於 ~/.claude/codebase-maps/）
python3 ~/.claude/skills/map/scripts/symbol_map.py

# 或指定目標目錄
python3 ~/.claude/skills/map/scripts/symbol_map.py /path/to/project
```

腳本會：
1. 自動偵測語言（TypeScript / JavaScript / Python / Rust / Go）
2. 提取所有 exported 符號與精確 `file:line`
3. 輸出 markdown 地圖至 `~/.claude/codebase-maps/<project>_symbols.md`

## 輸出格式範例

```markdown
# Codebase Symbol Map

**Project**: `my-project`
**Languages**: typescript
**Files**: 42 | **Symbols**: 183

## Classes
| Symbol | Location |
|--------|----------|
| `AuthProvider` | `src/auth/provider.ts:15` |

## Functions
| Symbol | Location |
|--------|----------|
| `formatDate` | `src/utils/date.ts:42` |
```

## 產出後的使用方式

地圖生成後，直接引用精確位置：
- 「讀 `src/auth/provider.ts:15` 確認 AuthProvider 的介面」
- 「`src/utils/date.ts:42` 的 `formatDate` 需要修改」

不再需要猜測或用 Grep 反覆搜尋。

## 支援語言

| 語言 | 提取符號類型 |
|------|------------|
| TypeScript | function, class, interface, type, const, enum |
| JavaScript | function, class, const, module.exports |
| Python | class, def, TypeVar |
| Rust | pub fn, pub struct, pub enum, pub trait |
| Go | exported func, struct, interface (大寫開頭) |

## Gotcha

- **腳本路徑**：確認 `~/.claude/skills/map/scripts/symbol_map.py` 存在（在 workspace 的 `.claude/skills/map/scripts/` 目錄中）
- **輸出目錄**：地圖存於 `~/.claude/codebase-maps/`，非 workspace 目錄，不會被 git 追蹤
- **大型 codebase**：超過 1000 個檔案時產出可能較大；用 `head -100` 先看摘要
- **動態語言**：Python 只提取頂層 class/def，不含動態建立的符號
- **更新時機**：每次大規模重構後重跑更新地圖
