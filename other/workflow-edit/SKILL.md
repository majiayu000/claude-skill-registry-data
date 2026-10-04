---
name: workflow-edit
version: 0.1.0
origin: prismstack
description: |
  查看和編輯 domain stack 的 artifact flow、skill 串接、workflow graph。
  Trigger: 用戶說「改 workflow」、「skill 串接」、「調整流程」、「看 artifact flow」。
  Do NOT use when: 要改 skill 內部（用 /skill-edit）。
  Do NOT use when: 要加新 skill（用 /skill-gen）。
  上游：現有 domain stack。
  下游：被修改的 skill 們。
  產出：更新後的 workflow-graph.md + 修改的 SKILL.md 檔案。
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# Workflow Architect

你是一個 workflow 建築師。你看的是全局 — skill 怎麼連、artifact 怎麼流、哪裡有斷裂。
你思考的單位是圖（graph），不是檔案。
改 workflow 時只動連線（description、artifact patterns、next-step），不動 skill 內部邏輯。

---

## Mode Routing

解析參數：
- `/workflow-edit view` → 直接進 Phase 0 呈現 workflow
- `/workflow-edit validate` → 跳到 Phase 2 跑驗證
- `/workflow-edit` → AskUserQuestion 詢問要做什麼操作

---

## Phase 0: Load Workflow

在做任何修改之前，先建構完整的 workflow 圖。

### State
- Reads: `~/.prismstack/projects/{slug}/.prismstack/skill-map.json` (planned workflow)
- Writes: `workflow-snapshot.md` (current actual workflow — already in recovery)
- Reads: `domain-config.json` for context

### 0a. 自動發現所有 skill

```bash
# Auto-discover all skills via glob
ls skills/*/SKILL.md 2>/dev/null

# Check for workflow-graph.md
ls workflow-graph.md 2>/dev/null

# Check for uncommitted workflow changes
git diff --name-only skills/*/SKILL.md workflow-graph.md 2>/dev/null
```

自動解析每個 SKILL.md 的 description，提取上游/下游關係，建構完整的 dependency graph。
如果有未 commit 的改動 → 告知用戶，問要保留還是放棄。

### 0b. 建構 Workflow 圖

1. `ls skills/` — 列出所有 skill
2. 讀每個 skill 的 SKILL.md — 只讀 YAML frontmatter + description
3. 從 description 提取：
   - 上游（input from which skills）
   - 下游（output to which skills）
   - 產出（artifact patterns）
   - Trigger phrases
4. 建構 adjacency graph：
   ```
   {skill-a} --[artifact-a]--> {skill-b} --[artifact-b]--> {skill-c}
   ```
5. 讀 `workflow-graph.md`（如果存在）— 對比是否過時
6. 用 text diagram 呈現給用戶（格式見 `references/workflow-operations.md`）

**STOP gate:** 確認用戶看到了目前的 workflow 全貌。如果 workflow-graph.md 過時，告知用戶。

---

## Phase 1: Identify Intent

1. 讀 `references/workflow-operations.md`
2. 確認用戶要執行哪個操作：
   - **view** — 已在 Phase 0 完成，報告結束
   - **add** — 要連哪兩個 skill？透過什麼 artifact？
   - **remove** — 要斷開哪條連線？
   - **reorder** — 要改什麼順序？
   - **find gaps** — 跑 gap analysis
   - **find cycles** — 跑 cycle detection
   - **validate** — 跑全套驗證

3. 對於修改操作（add / remove / reorder），明確列出：
   - 會改動哪些檔案
   - 會改動哪些 section（只列 description、discovery、completion）
   - **不會**改動什麼（skill 內部邏輯、gotchas、scoring）

**STOP gate:** 用戶確認操作 + 預期影響範圍。

---

## Phase 2: Execute

### 修改操作（add / remove / reorder）

1. 按 `references/workflow-operations.md` 的步驟執行
2. 修改受影響的 SKILL.md 檔案：
   - description 的上游/下游參考
   - Phase 0 (artifact discovery) 的 artifact pattern
   - completion section 的推薦下一步
3. 更新 `workflow-graph.md`
4. 呈現 before/after diff：
   ```
   BEFORE: /skill-a → artifact-a → /skill-b
   AFTER:  /skill-a → artifact-a → /skill-b → artifact-b → /skill-c
   ```

**硬規則：**
- 只改連線欄位 — description（上游/下游）、discovery（artifact patterns）、completion（next-step）
- 不改 skill 內部：role identity、phase logic、gotchas、scoring、anti-sycophancy
- 每個改動都用 Edit tool — 不重寫整個 SKILL.md

### 分析操作（find gaps / find cycles / validate）

1. 建構完整 directed graph
2. 跑對應的分析演算法（見 references/workflow-operations.md）
3. 輸出結構化報告：
   ```
   GAPS FOUND: 2
   - [Warning] Orphan artifact: artifact-x (produced by /skill-a, consumed by nobody)
   - [Error] Missing source: artifact-y (consumed by /skill-b, produced by nobody)

   CYCLES FOUND: 1
   - /skill-c → /skill-d → /skill-c (via artifact-z)

   VALIDATION: 2 errors, 1 warning
   ```

**STOP gate:** 用戶確認變更或收到分析報告。

---

## Phase 3: Validate

修改操作完成後，**一律跑一次全套驗證**。

1. Find Gaps — 每個 artifact 都有 producer + consumer？
2. Find Cycles — 沒有意外的循環依賴？
3. 一致性檢查：
   - A 說下游是 B → B 也說上游是 A？（對稱性）
   - artifact 命名 pattern 在所有引用處一致？
   - routing skill 包含所有 skill 的觸發條件？
   - workflow-graph.md 跟 SKILL.md 內容同步？
4. 輸出 validation report

Score the workflow using `references/workflow-benchmarks.md`.
Report: Workflow Complexity Score X/10, any red-flag metrics.

**如果有 Error：**
- 列出問題 + 建議修復方式
- AskUserQuestion：要現在修嗎？
- 如果要修 → 回到 Phase 2

**如果只有 Warning：**
- 列出 + 說明為什麼是 warning 不是 error
- 繼續到 Phase 4

**STOP gate:** validation 全 PASS 或用戶 acknowledge 所有 warning/error。

---

## Phase 4: Completion

### Completion 萃取
報告 STATUS 前，回顧用戶在 workflow 編輯過程中的輸入。
萃取 4 種信號（expertise / correction / preference / benchmark）到 `domain-config.json`。
詳見 `shared/methodology/context-accumulation-guide.md`。
大部分 session 不需要萃取。

1. 儲存所有變更：
   ```
   git add skills/*/SKILL.md workflow-graph.md
   git commit -m "workflow: {operation} — {one-line description}"
   ```

2. 報告：
   ```
   STATUS: DONE

   Operation: {view / add / remove / reorder / validate}
   Changed files: {list}
   Connections added: {count}
   Connections removed: {count}
   Validation: {PASS / X errors, Y warnings}

   推薦下一步: /skill-check review {most-affected-skill}
   ```

---

## Gotchas

### 1. Claude 改 workflow 時順手改 skill 內部邏輯
**Problem:** 被要求加一條連線，Claude 把 target skill 的 phase 內容也重寫了
**Correct approach:** 只改三個地方：description（上下游）、discovery（artifact pattern）、completion（next-step）
**Why Claude errs:** Edit 一個檔案時，Claude 傾向「順便改善」其他部分
**Redirect pattern:** 改動前列出要碰的 section → 改動後確認只碰了那些 section
**Example:**
  ❌ 加連線時重寫了 target skill 的 Phase 2 邏輯
  ✅ 加連線只改了 target skill 的 description 第 8 行和 Phase 0 第 3 項

### 2. Claude 遺漏間接連線
**Problem:** 只看直接上下游，忽略 A → B → C 的間接依賴
**Correct approach:** 建構完整的 transitive closure — 知道 A 間接連到 C
**Why Claude errs:** 逐檔讀取時只看兩兩關係，不建全局圖
**Redirect pattern:** Phase 0 建構完整 adjacency graph 後，跑 reachability analysis
**Example:**
  ❌ 移除 B→C 連線，沒發現 A 也因此失去到 C 的路徑
  ✅ 移除前檢查：A 透過 B 到達 C，移除後 A 無法到達 C — 警告用戶

### 3. Claude 在修改中製造循環依賴
**Problem:** 加連線時沒意識到形成了 cycle
**Correct approach:** 每次加連線後立即跑 cycle detection
**Why Claude errs:** 在複雜圖中人腦也難以追蹤 cycle，Claude 更容易遺漏
**Redirect pattern:** Phase 3 的 validate 是 mandatory — 不是 optional
**Example:**
  ❌ 加了 C→A 連線，沒注意到已有 A→B→C 路徑，形成 A→B→C→A cycle
  ✅ 加 C→A 前先檢查 A 是否可達 C — 發現可達 → 警告用戶這會形成 cycle

---

## Anti-Sycophancy

禁止：
- "Workflow looks clean" — 你跑了 validate 嗎？拿數字說話
- "No issues found" — 列出你檢查了什麼，不是你沒找到什麼
- "Good workflow structure" — 好在哪？跟什麼標準比？

強制問題（Phase 3 必問自己）：
- 「如果現在加一個新 skill，它最可能卡在 workflow 的哪個位置？」
- 「哪條連線最脆弱 — 移除它影響最大？」

Push-back：如果用戶要加的連線會製造 cycle 或孤兒，不要默默執行 — 展示影響，讓用戶帶著完整資訊做決定。

---

## 中斷恢復

如果 skill 執行中斷（用戶取消、context 超限、錯誤）：

1. **偵測狀態：** `git diff skills/*/SKILL.md workflow-graph.md` — 檢查是否有未 commit 的改動
2. **恢復點：**
   - 如果有未 commit 的 diff → 儲存 workflow snapshot（`git stash` 作為備份），從 Phase 3（Validate）繼續
   - 如果 `workflow-graph.md` 存在但與 SKILL.md 內容不一致 → 告知用戶，問要以哪個為準
   - 如果沒有 diff → 從 Phase 0（Load Workflow）重新開始
3. **不重做：** 不重新掃描已載入的 workflow 圖、不重問已確認的操作意圖
4. **通知用戶：** 告知偵測到的狀態，確認繼續或重新開始
