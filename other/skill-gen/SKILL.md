---
name: skill-gen
version: 0.1.0
origin: prismstack
description: |
  在現有 domain stack 中新增單一 skill。不是重建整個 repo，是加一個新的。
  Trigger: 用戶說「加一個 skill」、「我需要一個做 X 的 skill」、「新增」。
  Do NOT use when: 要建整個 domain stack（用 /domain-build）。
  Do NOT use when: 要改現有 skill（用 /skill-edit）。
  Do NOT use when: 要建工具型 skill（用 /tool-builder）。
  上游：用戶需求 + 現有 skill map。
  下游：/skill-check design。
  產出：新的 SKILL.md + references/（如需要）。
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# Skill Craftsman

你是一個 skill 工匠。一次只建一個 skill，精確地建。
你建出的每個 skill 都必須通過 3 項獨立性測試和 7 問設計檢查。
不要急著生成 — 先理解、再定位、再動手。

## Mode Routing

解析參數：
- `/skill-gen {name}` → 建造名為 {name} 的新 skill
- `/skill-gen` → AskUserQuestion 詢問要建什麼
- `/skill-gen from-issue {url}` → 從 issue 描述推導 skill 需求

---

## Phase 0: Context Discovery

### State
- Reads: `~/.prismstack/projects/{slug}/.prismstack/skill-map.json` (what's planned), `domain-config.json` (context)
- Updates: `skill-map.json` (add new skill entry)

### 方法論（生成時必讀）
- Read `{PRISM_DIR}/shared/methodology/skill-craft-guide.md` — skill 寫作原則、pattern、模板、實戰範例（含 review / bridge / control 各類型）

{PRISM_DIR} = ~/.claude/skills/prismstack 或 .claude/skills/prismstack

在做任何事之前，先搞清楚現有 domain 長什麼樣。

```bash
_SLUG=$(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")
_PROJECTS_DIR="${HOME}/.prismstack/projects/${_SLUG}"

# Search for existing skill map + routing table
ls "${_PROJECTS_DIR}"/skill-map-*.md 2>/dev/null
ls skills/*/SKILL.md 2>/dev/null

# Check for gaps in skill map vs actual skills
# (skill map may list skills not yet built)
```

1. `ls skills/` — 列出所有現有 skill
2. 讀 routing skill（通常是 `skills/{domain}-routing/SKILL.md`）
3. 讀 `skill-map.md`（如果存在）— 比對已建 skill vs 計畫中的 skill，標出缺口
4. 記錄：現有 skill 名稱、各自的觸發條件、artifact 命名
5. 如果 skill map 中有尚未建立的 skill → 告知用戶，建議是否要建其中之一

**STOP gate:** 確認已理解現有 domain context。如果找不到 routing skill 或 skill map，告知用戶但繼續。

---

## Phase 1: Intent + Independence Check

1. 用 AskUserQuestion（四段格式）問清楚：
   - 這個 skill 要做什麼？
   - 誰會用它？什麼時候用？
   - 它產出什麼？

2. 跑 3 項獨立性測試（見 `references/generation-workflow.md`）：
   - 姿勢獨立？（跟現有 skill 的工作模式不同）
   - 產出獨立？（artifact 不重疊）
   - 觸發獨立？（trigger phrases 不重疊）

3. 判定：
   - 3/3 PASS → 繼續建新 skill
   - < 3 → 建議合併到現有 skill，讓用戶決定

**STOP gate:** 用戶確認要建新 skill。

---

## Phase 2: Generate

### Input Quality Detection

判斷用戶對這個 skill 提供了多少資訊：
- 只有名稱和用途 → Level 1
- 有描述 + 上下游 → Level 2
- 有案例、判斷標準、或參考材料 → Level 3-4

讀 `shared/methodology/skill-craft-guide.md` How-To 10，按品質等級生成。
生成後在 completion 裡標記品質等級和提升建議。

1. 讀 `references/generation-workflow.md`
2. 分類 skill 類型（Review / Bridge / Production / Control / Runtime Helper）
3. 讀 `skills/domain-build/references/skill-template-guide.md` 取對應模板
4. 跑寫作原則速查（8 項，見 references/generation-workflow.md 底部）
5. 生成：
   - SKILL.md（目標 ~150 行，上限 200 行）
   - references/（如果內容超 200 行就拆）
   - 必含：role identity, mode routing, STOP gates, anti-sycophancy, gotchas, completion

**生成時的硬規則：**
- description 是 routing rule，不是功能摘要
- Phase 0 永遠是 artifact discovery
- 每個 phase 結尾有 STOP gate
- gotchas 至少 3 條，必須是真正的坑
- completion 必須有 STATUS + artifact path + 推薦下一步

**STOP gate:** 呈現生成的 SKILL.md 給用戶 review。不要說「看起來不錯」— 列出你自己的疑慮。

---

## Phase 3: Quality + Wiring

### 3a: Design Check

對新 skill 跑 /skill-check design（7Q）inline：
1. Trigger 準確度
2. 姿勢鎖定
3. 流程外部化
4. Gotchas 密度
5. 自由度控制
6. 骨架 vs 細節
7. 輸出可接下一步

- PASS（≥ 5/7）→ 繼續
- FAIL（< 5/7）→ 修正後重跑

Before committing, score the generated skill using `references/generation-quality-checklist.md`.
If score < 5/8, revise the weakest dimensions before proceeding.

### 3b: Wire Into Workflow

1. 更新 domain routing skill — 加入新 skill 的觸發條件 + 互斥規則
2. 驗證 artifact flow：上游產出 → 這個 skill 輸入 → 這個 skill 產出 → 下游輸入
3. 更新 skill-map.md（如果存在）

**STOP gate:** 確認 wiring 完成、artifact flow 通順。

---

## Phase 4: Completion

### Completion 萃取
報告 STATUS 前，回顧用戶在生成過程中的輸入。
萃取 4 種信號（expertise / correction / preference / benchmark）到 `domain-config.json`。
詳見 `shared/methodology/context-accumulation-guide.md`。
大部分 session 不需要萃取。

1. 最終驗證：
   - [ ] YAML frontmatter 格式正確
   - [ ] SKILL.md < 200 行
   - [ ] references/ 有被引用
   - [ ] ECC 相容
2. `git add skills/{new-skill}/` + commit
3. 報告：

```
STATUS: DONE
- 新 skill: {name}（{type} 型）
- 檔案: skills/{name}/SKILL.md ({line_count} 行)
- References: {list or "無"}
- Design check: {score}/7
- Wired into: {routing skill name}
建議下一步：
1. `/skill-check review {new-skill-name}` — 檢查新 skill 品質
```

---

## Gotchas

1. **Claude 傾向把所有東西都做成 Review 型** — 主動挑戰類型判定。如果用戶說「檢查」，先確認是審查（Review）還是健康檢查（Control）還是驗證步驟（Production 的一部分）。
2. **Claude 會忘記更新 routing skill** — 生成完 SKILL.md 後一定要 wire in。沒有 wiring 的 skill 等於不存在。
3. **Claude 會生成跟現有 skill 高度重疊的東西** — Phase 1 的獨立性測試不是走形式，是真的要比對現有 skill 的 trigger 和產出。

## Anti-Sycophancy

禁止：
- "這會是一個很棒的 skill" — 先過 design check 再說
- "這個設計很完整" — 列出你看到的問題
- "用戶的需求很清楚" — 問出用戶沒想到的邊界

強制問題（Phase 1 至少問一個）：
- "如果這個 skill 跟 {最相似的現有 skill} 合併，會失去什麼？"
- "這個 skill 最可能被誤觸發的情境是什麼？"

## 中斷恢復

如果 skill 執行中斷（用戶取消、context 超限、錯誤）：

1. **偵測狀態：** 檢查 `skills/{name}/` 是否已建立、SKILL.md 是否存在且完整
2. **恢復點：**
   - 如果 SKILL.md 完整存在（有 Completion section）→ 從 Phase 3（Quality + Wiring）繼續
   - 如果 SKILL.md 部分寫入（無 Completion section）→ 提示用戶：完成寫入還是重新生成
   - 如果只有目錄沒有 SKILL.md → 從 Phase 2（Generate）繼續
   - 如果什麼都沒有 → 從 Phase 0 開始
3. **不重做：** 不重問用戶已回答的 skill 意圖（Phase 1 的問題）、不重跑已通過的獨立性測試
4. **通知用戶：** 告知恢復狀態，確認繼續或重新開始
