---
name: load-plan
description: 顯示當前 workspace 的載入計畫：已自動載入的規則（大小/行數）、所有可用 skill（依領域分組）、觸發關鍵詞。適合在 session 開始、接手新任務、或評估 workspace 配置時使用。
disable-model-invocation: true
context: fork
---

# Load Plan — Workspace 載入計畫

## 觸發條件

- Session 開始想知道有哪些工具可用
- 接手新任務想快速找到對應 skill
- 向新使用者介紹 workspace 能力
- 確認 workspace 配置是否正常

## 執行方式

```bash
bash "$CLAUDE_PROJECT_DIR/scripts/load-plan.sh"
```

或直接呼叫：
```bash
bash /home/user/claude-code-workspace/scripts/load-plan.sh
```

## 輸出說明

Script 會產出三個區塊：

1. **自動載入（常駐 context）** — 每次 session 自動載入的規則，顯示行數與大小
2. **按需 Skill（說觸發詞即載入）** — 所有可用 skill，依領域分組，顯示觸發關鍵詞
3. **快速參考** — 最常用的命令入口

## Gotcha

- 若看不到某個 skill，確認 `.claude/skills/{name}/SKILL.md` 存在
- 自動載入規則來自 CLAUDE.md 的 `@` 行，新增規則後需更新 CLAUDE.md 才會顯示
- Script 動態讀取檔案，不需手動維護
