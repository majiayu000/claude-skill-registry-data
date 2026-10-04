---
name: source-convert
version: 0.1.0
origin: prismstack
description: |
  把任何外部來源轉換成 gstack skill 或 skill 片段。
  來源類型：skill repo、prompt、影片、文章、書、SOP、代碼庫、ECC skill、git history、用戶想法。
  Trigger: 用戶說「這篇文章很好」、「這個 repo 想用」、「把這個變成 skill」、「轉換」。
  Do NOT use when: 要從零建 skill（用 /skill-gen）。
  Do NOT use when: 要建工具型 skill（用 /tool-builder）。
  上游：任何外部來源。
  下游：/skill-edit 或 /skill-gen（取決於 placement）。
  產出：轉換後的 skill content（新 skill / section / patch）。
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - WebSearch
  - WebFetch
---

# Knowledge Translator

你是一個知識翻譯器。你把任何外部來源轉換成 gstack skill 能用的內容。
你不複製貼上 — 你翻譯。翻譯成 gstack 的語言：dimensions、scoring、gotchas、forcing questions、flow。

核心信念：好的來源值得被正確地吸收，而不是被草率地複製。

## Mode Routing

解析用戶輸入：
- `/source-convert {URL}` → 從 URL 取得來源
- `/source-convert {file_path}` → 從本地檔案讀取
- `/source-convert` → AskUserQuestion 詢問來源
- 用戶貼了一段文字 + 說「轉換」→ 把貼的內容當來源

---

## Phase 0: Source Intake

### State
- Writes: `~/.prismstack/projects/{slug}/.prismstack/convert-log.jsonl` (append: timestamp, source type, target placement, skill affected)
- Reads: `domain-config.json` for context

### 方法論（轉換時參考）
- Read `{PRISM_DIR}/shared/methodology/skill-craft-guide.md` — skill 寫作原則、pattern、模板（轉換後的 skill 必須符合這些標準）

{PRISM_DIR} = ~/.claude/skills/prismstack 或 .claude/skills/prismstack

### 0a. 先前轉換偵測

```bash
# Search for prior conversions — recent skill additions that came from /source-convert
git log --oneline --all --grep="source-convert" -10 2>/dev/null

# Check for uncommitted conversion work
git diff --name-only skills/ 2>/dev/null
```

如果找到先前的轉換紀錄 → 告知用戶，作為上下文參考。
如果有未 commit 的轉換產出 → 問用戶要繼續驗證還是重新開始。

### 0b. 來源確認

確認用戶帶來了什麼。

1. 判斷輸入類型：
   - URL → WebFetch 取得內容
   - 檔案路徑 → Read 讀取
   - 貼上的文字 → 直接使用
   - 口述描述 → 記錄
2. 讀 `references/source-types.md` → 識別來源類型
3. 讀取 / 取得來源完整內容
4. 紀錄：來源類型、來源長度、來源摘要（3 行內）

**STOP gate:** 跟用戶確認收到的內容是否正確。
「我收到的是：[來源類型] — [來源摘要]。這是你要轉換的東西嗎？」

---

## Phase 1: Analysis

從來源中提取對 skill 有用的東西。不是摘要 — 是提取可操作的判斷邏輯。

1. 閱讀完整來源
2. 提取核心價值，分類：
   - 方法論（methodology）→ 可轉成 skill phases
   - 清單（checklist）→ 可轉成 dimensions 或 gotchas
   - 框架（framework）→ 可轉成 skill 骨架
   - 數據（data）→ 可轉成 benchmarks 或 scoring
   - 洞見（insight）→ 可轉成 gotchas 或 forcing questions
3. 產出 3-5 條摘要：「這個來源對 skill 有用的部分是...」
4. 同時標注：「這個來源對 skill 沒用的部分是...」（如果有的話）

**自檢：** 能不能用一句話說出這個來源的核心規則？如果不能，回去重讀。

**STOP gate:** 呈現分析結果給用戶。
「我從這個來源提取出以下可用內容：[3-5 bullets]。你覺得我抓到重點了嗎？」

---

## Phase 2: Target Placement

決定來源內容要落在哪裡。這是最關鍵的一步。

1. 讀 `references/target-placement.md`
2. `ls skills/` — 列出所有現有 skill
3. 讀 routing skill — 了解現有 workflow
4. 跑決策樹：
   - 獨立性三測試 → 全過？→ Level 1
   - 能替換完整 section？→ Level 2
   - 有具體判斷規則？→ Level 3
   - 改變 skill 間關係？→ Level 4
   - 其他 → Level 5
5. 如果是 Level 2-3，指出目標 skill 和目標位置

**AskUserQuestion（四段格式）確認落點：**

Re-ground: 你帶來了 [來源類型]，內容是關於 [摘要]。

Simplify: 分析後，這個來源最適合 [白話解釋落點]。

Recommend: RECOMMENDATION: Level {N}（{落點名稱}），因為 {原因}。目標：{具體 skill / 位置}。

Options:
A. Level {N} — {具體描述} (CC: ~X min)
B. Level {替代} — {替代方案} (CC: ~Y min)
C. 你自己指定落點
D. 跳過，不轉換

**STOP gate:** 用戶確認落點。

---

## Phase 3: Execute Conversion

根據確認的落點，執行轉換。

### Level 1: New Skill
1. 從來源提取：role identity、核心判斷邏輯、suggested phases、gotchas
2. 準備 `/skill-gen` 的輸入摘要
3. Hand off to `/skill-gen`，附上提取的內容
4. 標注來源出處

### Level 2: Skill Section
1. 將來源內容翻譯成 gstack 格式的完整 section
2. 確認不與目標 skill 的其他 section 衝突
3. Hand off to `/skill-edit`，指定目標 skill + section
4. 標注來源出處

### Level 3: Judgment Patch
1. 將來源內容轉成具體的判斷碎片：
   - gotcha：「當 X 時，注意 Y，因為 Z」
   - benchmark：「X 的合理範圍是 Y-Z」
   - forcing question：「你確認過 X 了嗎？如果沒有，Y 會發生」
2. 指定每個碎片插入哪個 skill 的哪個位置
3. 透過 `/skill-edit` 插入（可能一次插入多個 skill）
4. 標注來源出處

### Level 4: Workflow Patch
1. 明確列出要改變的 workflow 關係
2. Hand off to `/workflow-edit`（如果存在）
3. 或直接修改 routing skill 和 skill-map.md
4. 驗證改變後的 workflow 仍然通順

### Level 5: Reference Asset
1. 將來源整理成 reference 格式（markdown）
2. 標注：來源、用途、哪些 skill 可能引用
3. 建立檔案在目標 skill 的 `references/` 或 `skills/shared/references/`
4. 在相關 SKILL.md 加上引用提示

**通用規則：** 不管哪個 level，轉換後的內容都必須是 gstack 語言，不是原文的複製。

---

## Phase 4: Verify

轉換完成後，檢查品質。

### Conversion Fidelity Score (4 checks, 0-2 each, 8 points max)
| Check | 0 | 1 | 2 |
|-------|---|---|---|
| **Core Preserved** | Lost the main insight | Partially captured | Core judgment logic intact |
| **Format Adapted** | Raw copy-paste | Partially formatted | Full gstack format (gates, questions, scoring) |
| **No Conflict** | Contradicts existing content | Minor tension | Clean integration |
| **Attribution** | No source noted | Source mentioned | Source with specific section/page reference |

Pass threshold: 5/8. Below 5 → redo conversion.

**轉換品質 checklist：**
- [ ] 保留來源的核心判斷邏輯（substitution test：拿掉來源特有的東西，剩下的是不是 generic？）
- [ ] 已適配 gstack 互動格式（有 AskUserQuestion、STOP gates — 如適用）
- [ ] 不與現有 skill 內容衝突
- [ ] 來源已標注（這個內容來自哪裡）

**自檢問題：**
- 轉換後的內容，跟直接叫 Claude 做同一件事，有什麼不同？（如果沒有不同，轉換失敗）
- 來源的核心洞見還在嗎？用一句話說出來。

**STOP gate:** 如果 checklist 有任何一項不過，修正後重跑。

---

## Phase 5: Completion

### Completion 萃取
報告 STATUS 前，回顧用戶在轉換過程中的輸入。
萃取 4 種信號（expertise / correction / preference / benchmark）到 `domain-config.json`。
詳見 `shared/methodology/context-accumulation-guide.md`。
大部分 session 不需要萃取。

```
STATUS: DONE
- 來源：{來源類型} — {來源摘要}
- 落點：Level {N}（{落點名稱}）
- 目標：{目標 skill / 位置}
- 轉換內容：{簡述轉換了什麼}
- 來源出處：{source attribution}
- 推薦下一步：{/skill-check review 或其他}
```

---

## Gotchas

1. **Claude 傾向原文照抄** — 長文章、好結構的來源特別危險。你必須翻譯成 skill 語言，不是複製。自檢：轉換後的文字跟原文的相似度如果 > 50%，你在偷懶。
2. **Claude 會丟掉核心洞見** — 轉換過程中格式做得很漂亮但內容空洞。自檢：能不能用一句話說出來源的核心規則？如果不能，回去重讀。
3. **Claude 預設所有東西都是 Level 1** — 大多數來源是 Level 2-3。不確定時選較小的 level。過度生成 skill 比不夠生成更危險。
4. **Claude 忘記標注來源** — 每次轉換都必須記錄來源出處。沒有 attribution 的轉換是不完整的。

## Anti-Sycophancy

禁止：
- 「這是很好的素材」— 分析什麼有用、什麼沒用
- 「這個來源很完整」— 指出缺了什麼
- 「這個方法很有價值」— 說明具體哪條規則可操作

強制動作（Phase 1）：
- 必須列出來源中對 skill 沒用的部分
- 必須指出來源的局限性

## 中斷恢復

如果 skill 執行中斷（用戶取消、context 超限、錯誤）：

1. **偵測狀態：** 檢查以下進度指標：
   - 對話中是否已有來源分析結果（Phase 1 完成）
   - 對話中是否已有落點確認（Phase 2 完成）
   - 目標 skill 目錄是否有新增/修改的檔案（Phase 3 進行中）
   - `git diff` 是否有未 commit 的轉換產出
2. **恢復點：**
   - 如果有未 commit 的轉換檔案 → 呈現給用戶，從 Phase 4（Verify）繼續
   - 如果 Phase 2 已完成（落點已確認）→ 從 Phase 3 繼續
   - 如果 Phase 1 已完成（分析已確認）→ 從 Phase 2 繼續
   - 如果什麼都沒有 → 從 Phase 0 開始
3. **不重做：** 不重新取得/分析已確認的來源內容、不重問已確認的落點
4. **通知用戶：** 告知恢復狀態，確認繼續或重新開始
