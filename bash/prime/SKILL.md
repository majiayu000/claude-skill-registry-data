---
name: prime
description: 冷啟新 session：掃描 codebase 結構並讀取 README，快速建立專案 context。適合在陌生 repo 或新 session 開始時使用。
disable-model-invocation: true
context: fork
---

# Prime — 冷啟 Context Loading

## 觸發條件

- 新 session 開始，需要快速了解一個不熟悉的 codebase
- 接手他人專案或剛 clone 的 repo
- 從 `/clear` 或 `/compact` 後重新建立 context

## 執行步驟

1. **掃描 git 追蹤的檔案結構**
   ```bash
   git ls-files | head -80
   ```

2. **取得目錄樹概覽**
   ```bash
   find . -type f -not -path './.git/*' -not -path './node_modules/*' | head -60 | sort
   ```

3. **讀取專案文件**（按優先順序）
   - `@README.md`（若存在）
   - `@CLAUDE.md`（若存在）
   - `@.claude/REFERENCES.md`（若存在）

4. **產出 Context 摘要**，包含：
   - 專案目的（1-2 句）
   - 技術棧
   - 主要模組/目錄說明
   - 下一步建議（適合開始什麼工作）

## 針對本 workspace 的額外步驟

若在 `claude-code-workspace` 中執行，額外讀取：
- `.claude/rules/` 目錄列表（了解現有規則）
- `.claude/skills/` 目錄列表（了解現有 skills）
- `.claude/agents/` 目錄列表（了解現有 agents）
- `scripts/healthcheck.sh` 提示可執行健康檢查

## Gotcha

- **不要** 讀取超過 3 個文件全文，優先讀入 README + CLAUDE.md 即可
- 若 README 超過 200 行，只讀前 80 行摘要
- context 摘要長度控制在 ≤300 字，避免佔用過多 context budget
