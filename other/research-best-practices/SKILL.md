---
name: research-best-practices
description: 研究外部 Claude Code best practice 來源（GitHub repos、官方 docs、blog），對比現有 workspace 做 gap analysis，產出可操作建議清單。
disable-model-invocation: true
context: fork
---

# Research Best Practices — Meta 研究 Skill

## 觸發條件（何時使用）

以下情境適合啟動本 Skill：

- **季度審計**：每季定期審查 workspace 設定是否跟上社群最新做法
- **官方 major update**：Anthropic 發布 Claude Code 重大版本或新功能時（如 `/ultraplan`、`/ultrareview`、Voice mode）
- **發現新 community repo**：使用者找到新的高星 best practice repo 想評估是否採納
- **新指令公告**：Thariq 或 Boris 發表新 tip 時，對照 workspace 評估採納優先級

---

## 執行流程（7 步驟，三層模型）

### Step 1 — Fan-out 研究（Haiku）

平行啟動 `researcher` subagent × N，每個負責一個來源：

- 每份研究摘要限制在 **350 字以內**
- **不貼原始檔案內容**，只產出結構化摘要（含：關鍵做法、理由、適用條件）
- 使用 `context: fork` 確保原始內容留在 child context，不污染主對話

### Step 2 — 現狀盤點（Haiku）

枚舉現有 workspace 設定，建立現狀清單：

```
.claude/skills/    → 現有 Skills 列表
.claude/agents/    → 現有 Agents 列表
.claude/hooks/     → 現有 Hooks 列表
.claude/rules/     → 現有 Rules 列表（含 @ auto-load 與 lazy-load 分類）
```

輸出格式：每個項目一行，附簡短功能描述。

### Step 3 — Gap Matrix（Sonnet）

對照 Step 1 研究摘要與 Step 2 現狀清單，產出 gap matrix：

| 現有（Existing） | 缺口（Gap） | 來源（Source） |
|-----------------|------------|--------------|
| 已有類似功能的項目 | 尚未實作或明顯不足之處 | 建議的參考來源 URL |

優先標記：高價值（High）/ 中等（Medium）/ 低價值（Low）。

### Step 4 — Advisor 確認（Opus advisor）

呼叫 `advisor` 工具，提交 gap matrix，詢問：

- 哪些缺口**值得實作**（reason：ROI、複雜度、與現有系統的相容性）
- 哪些缺口**應跳過**（reason：重複、過度工程、不符合本 workspace 使用情境）

**不要在 advisor 確認前動手實作任何東西。**

### Step 5 — 實作（Sonnet implementer）

僅實作 Step 4 中 advisor 核准的項目：

- 新 rules 放入 `.claude/rules/`（lazy-load，不加 `@`）
- 新 skills 放入 `.claude/skills/<name>/SKILL.md`
- 新 agents 放入 `.claude/agents/<name>.md`
- 修改 CLAUDE.md 的 lazy-load 表（如需新增觸發條件）

### Step 6 — 審查（Opus reviewer）

請 Opus 審查實作品質：

- 是否符合 workspace 既有風格
- 是否有多餘或重複的內容
- Frontmatter 格式是否正確
- 是否有任何安全或操作風險

### Step 7 — 提交

```
git add <具體檔案路徑>
git commit -m "feat: apply best practice gap analysis from <date>"
git push -u origin <branch>
```

失敗時重試 4 次，間隔：2s / 4s / 8s / 16s。

---

## 研究來源

預設來源清單見：`references/sources.md`

執行時可附加臨時來源：在呼叫本 Skill 時於 prompt 中列出額外 URL。

---

## Gotcha（注意事項）

1. **不要把原始檔案內容塞進主對話**：researcher subagent 只回傳摘要（≤350 字），原始網頁內容、完整 README 等留在 child context。
2. **新 rules 進 lazy-load 表，不加 `@` auto-load**：避免增加每次 session 啟動的 context 負擔；`@` 只保留給真正「常駐必要」的規則。
3. **既有功能的同類實作要跳過**：若 workspace 已有類似效果的 rule/skill/agent，不要重複建立。避免重複發明（reinventing the wheel）。
4. **advisor 確認後才動手實作**：Step 4 是強制關卡，不可跳過。高確定性的項目也應讓 advisor 快速過目，確保不遺漏邊界案例。
5. **數量不是目標，精簡優於大量**：workspace 設定的可維護性比覆蓋面更重要。10 個高品質的項目勝過 30 個低價值的項目。
6. **⚠️ Researcher subagent 會幻覺（Hallucination Risk）**：研究型 subagent 常捏造 URL、百分比、功能名稱、repo 名稱。Step 4 (Advisor) 的核心職責之一就是攔截這些幻覺。  
   驗證清單：
   - Hook 事件名稱 → 必須對照 `code.claude.com/docs/en/hooks`（官方一次列出所有事件）
   - 社群 repo → 用 `site:github.com <repo-name>` 搜尋確認存在
   - 功能名稱（如 "AutoDream", "Task Memory"）→ 找官方 blog 或 changelog 一手來源
   - 效能數字（"20%→50% activation"）→ 無一手來源即視為捏造，不引用
