---
name: domain-build
version: 0.1.0
origin: prismstack
description: |
  根據 /domain-plan 產出的 skill map，自動搭建完整的 domain gstack repo。
  Trigger: /domain-plan 完成後、用戶說「開始搭建」、「build」。
  Do NOT use when: 還沒規劃 skill map（先用 /domain-plan）。
  Do NOT use when: 要加單一 skill（用 /skill-gen）。
  上游：/domain-plan（讀取 skill-map-*.md）。
  下游：/skill-check pack（Wave 2）。Wave 1 內建輕量 pack health 替代。
  產出：完整的 domain gstack repo。
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# Domain Stack Builder

你是領域 stack 搭建引擎。快速搭建、完整搭建。品質目標：「可用，不求完美」。

## Auto Mode

如果被自動模式調用（--auto flag）：
- 跳過所有 STOP gates — 不每 5 個 skill 停一次
- 跳過 AskUserQuestion — 「repo 建在哪」用預設（temp 目錄或 orchestrator 指定）
- 仍然遵循 skill-craft-guide + system-wiring-guide
- 仍然跑 validate-repo.sh（失敗自動修）
- 仍然做 Input Quality Detection（按用戶輸入品質對等生成）
- 仍然存 build-progress.md

---

## Recovery（中斷恢復）

如果被中斷：
1. 檢查目標目錄是否已存在
2. 讀取 `build-progress.md`（如果有）
3. 從最後一個未完成的 Phase 續跑
4. **不要重新生成已存在的 skill**

---

## Phase 0: Artifact Discovery + 進度追蹤

### State
- Reads: `~/.prismstack/projects/{slug}/.prismstack/skill-map.json`, `domain-config.json`
- Writes: `build-progress.md` (already implemented)
- Updates: `domain-config.json` → `last_build` timestamp

1. 搜尋 `~/.prismstack/projects/*/skill-map-*.md`，找到最新的 skill map
2. 若找不到 → **STATUS: BLOCKED** — 建議先用 `/domain-plan`
3. 搜尋目標目錄是否已有部分建置（`build-progress.md`、`skills/` 目錄）：
   - 如果有 `build-progress.md` → 讀取，從最後一個 `pending` 狀態的 skill 繼續
   - 如果有 `skills/` 但沒有 progress file → 列出已存在的 skill，問用戶要接續還是重建
4. 搜尋 `~/.prismstack/projects/` 其他 domain 的已建 stack，列出可能相關的（用戶可能想參考）
5. 讀取 skill map，用 AskUserQuestion 確認：
   - 確認 skill 清單正確
   - 詢問 repo 建立位置（預設：當前目錄）
   - 詢問 domain slug（用於 artifact 路徑）
4. 建立 `build-progress.md` — 狀態追蹤表：

```
| Skill | Type | Status | Notes |
|-------|------|--------|-------|
| routing | Control | pending | |
| {skill-1} | {type} | pending | |
| ... | ... | ... | ... |
```

### 方法論
- Read `{PRISM_DIR}/shared/methodology/skill-craft-guide.md` — skill 寫作原則、pattern、模板、實戰範例
- Read `{PRISM_DIR}/shared/methodology/system-wiring-guide.md` — 搭建流程、系統 pattern、artifact flow 接線

{PRISM_DIR} = 找到的 Prismstack 安裝路徑（~/.claude/skills/prismstack 或 .claude/skills/prismstack）

**STOP: 確認 skill map + 建置位置後才繼續。**

---

## Phase 1: Repo Scaffold

讀取 `references/repo-scaffold-spec.md`。

1. 建立完整目錄結構
2. 生成根目錄檔案：README.md, CLAUDE.md, VERSION, CHANGELOG.md, LICENSE, .gitignore
3. 生成 bin/install.sh（chmod +x）+ bin/{domain}-slug.sh
4. `git init` + 第一次 commit
5. 更新 `build-progress.md`

**STOP: 呈現已建立的目錄樹，確認後繼續。**

---

## Phase 2: Shared Resources

讀取 `references/preamble-template.md`。

1. 根據領域知識生成 `skills/shared/preamble.md`（LLM 產生領域詞彙）
2. 生成 `skills/shared/completion-protocol.md`
3. 生成 `skills/shared/ask-format.md`
4. 生成 `skills/shared/artifact-conventions.md`
5. 更新 `build-progress.md`

---

## Phase 3: 依序生成 Skills

讀取 `references/skill-template-guide.md` + `references/quality-standards.md` + `references/ecc-compat-guide.md`。

### Source-Aware Build（Brownfield 支援）

如果 skill map 來自 brownfield 規劃（skill 帶有 `source` 標記），Phase 3 根據 source 決定每個 skill 的處理方式：

| Source | 處理方式 |
|--------|---------|
| **🆕 新增** | 正常生成（下方標準流程） |
| **🔧 改造** | **Adapt Mode**（見下方） |
| **✅ 直接用** | **Wire-Only Mode**（見下方） |
| **🔨 包裝** | 先讀非 skill 資產，再用 skill 模板包裝 |

沒有 source 標記 → 全部視為 🆕（向後相容 greenfield）。

#### Adapt Mode（🔧 改造）

**原則：保留核心邏輯，追加缺少的機制。不重寫。**

1. **讀取現有 SKILL.md 完整內容**
2. **對照 skill map 中列出的「需補機制」清單**
3. **逐項追加**：

| 缺少的機制 | 追加方式 |
|-----------|---------|
| Role lock | 在開頭加 role 定義（保留原有的角色描述風格） |
| Scoring | 從現有 Phase 結構推斷評分維度，加 scoring formula |
| Stop gate | 在現有 Phase 的關鍵判斷點加 `⛔ STOP` |
| Artifact flow | 加 Phase 0 discovery（搜尋上游 artifact）+ 結尾 save（寫到共用路徑） |
| Gotchas | 從 skill 內容和領域知識推斷 AI 盲點 |
| Anti-sycophancy | 加 forbidden phrases + forcing questions |
| YAML frontmatter | 如果缺少或不完整，補齊（name/version/origin/description/allowed-tools） |

4. **不改的東西**：
   - 現有的 Phase 結構和編號
   - 用戶的術語和措辭
   - 核心邏輯和判斷流程
   - 已有的 references/ 檔案

5. **寫入時使用 Edit（追加），不用 Write（覆蓋）**

#### Wire-Only Mode（✅ 直接用）

Skill 本身不改。只追加 artifact flow 接線：
1. 在 SKILL.md 開頭的 context discovery 區塊加上游 artifact 搜尋路徑
2. 在結尾加 artifact save 路徑
3. 確保 YAML frontmatter 有 `上游` 和 `下游` 欄位

#### 🔨 包裝模式

針對非 skill 資產（自動化腳本、API 串接等）：
1. 讀取資產源碼，理解功能
2. 用 skill 模板包裝：trigger、phases、artifact flow
3. 核心邏輯透過 Bash 調用原有腳本，不重新實作

### Input Quality Detection

在生成前，判斷可用輸入的品質等級：

```
Level 1: skill-map 只有 skill 名稱和類型 → Draft 品質
Level 2: skill-map 有描述和上下游 → Draft+ 品質
Level 3: skill-map 有詳細描述 + 用戶在規劃中提供了案例/判斷標準 → Usable 品質
Level 4: 用戶提供了完整 spec（如 marketing-creative-stack-v2.md 級別）→ Production 品質
Level 5（Brownfield）: 現有 skill + skill map 描述 → 改造品質取決於現有 skill 的品質
```

讀 `shared/methodology/skill-craft-guide.md` How-To 10 的品質對等標準。
每個 skill 按偵測到的品質等級生成。

**每個 skill 生成前，檢查 8 大原則（skill-writing-doctrine）：**
1. 先寫 trigger，不是內容
2. Skill = 工作姿態切換，不是知識包
3. 永遠外化 flow（不靠 Claude 記憶）
4. 最高價值內容是 gotchas
5. 脆弱的地方要嚴格
6. 主 skill = 骨架，references = 細節
7. 好 skill 定義 recovery
8. Output 必須是下一步可讀的

**每個 skill 生成後，對照 7 pattern（skill-writing-patterns）：**
1. Single-role identity
2. Progressive disclosure via folder
3. State management via scripts
4. Gotchas are highest-value
5. Argument parsing + mode routing at entry
6. Composability (skills call skills)
7. Anti-sycophancy = forbidden phrases + forcing questions + pushback

### 建置順序

```
Greenfield:
  3a: Routing skill（第一個）
  3b: 通用底盤 skills（fork gstack patterns + 領域詞彙）
  3c: 規劃視角 skills（策略/設計/工程）
  3d: 領域專屬 skills（LLM 根據領域知識生成）
  3e: 入口 skills（import/conversion）
  3f: 工具型 skills（如果有）

Brownfield（順序不同）:
  3a: 改造現有 skill（🔧）— 先補機制，因為現有 skill 是理解 stack 的基礎
  3b: Wire-only（✅）— 接線
  3c: 包裝非 skill 資產（🔨）
  3d: 生成缺口 skill（🆕）— 最後才生成新的，因為需要理解現有 skill 的銜接
  3e: Routing skill — 基於所有 skill（現有 + 新增）生成 triage entry
```

### 每個 skill 的生成流程

**🆕 新增 skill：**
1. 根據類型選擇模板（skill-template-guide.md）
2. 生成 YAML frontmatter（含完整 description）
3. 生成 SKILL.md 主體
4. 若內容 > 200 行 → 拆分到 references/
5. ECC 相容性檢查（ecc-compat-guide.md 自檢清單）
6. 更新 `build-progress.md`

**🔧 改造 skill：**
1. 讀取現有 SKILL.md
2. 對照需補機制清單
3. 逐項追加（使用 Edit，不覆蓋）
4. 如果原有 skill 在不同目錄 → 複製到 stack repo 再改造
5. 更新 `build-progress.md`（標注 source: adapted）

**✅ 直接用 skill：**
1. 複製到 stack repo（如果不在）
2. 追加 artifact flow wiring
3. 更新 `build-progress.md`（標注 source: existing）

### STOP Gate

**每處理 5 個 skill 後暫停：**
- 呈現進度表（含 source 標記，讓用戶看到哪些是改造、哪些是新增）
- 列出已知問題
- 用 AskUserQuestion 詢問：繼續 / 調整 / 停止

---

## Phase 4: System Integration

1. 檢查每個 skill 的 artifact discovery（讀上游）
2. 檢查每個 skill 的 artifact save（寫到 `~/.prismstack/projects/{slug}/`）
3. 檢查每個 skill 的 workflow position（推薦下一步）
4. 修復斷裂的 artifact flow

---

## Phase 5: Validation

1. 執行 `scripts/validate-repo.sh`（從 prismstack skill 目錄複製到生成的 repo）
2. 自動修復失敗項目
3. 重新執行驗證

### 驗收 Fix Loop

如果 validate-repo.sh 有項目失敗：
1. 記錄 baseline（N/5 pass）
2. Read `{PRISM_DIR}/shared/methodology/fix-loop-guide.md`
3. 每個失敗項自動修復：
   - Routing skill missing → 生成 routing skill
   - Skill count < 3 → 檢查哪些 skill 沒生成，補生成
   - No artifact patterns → 在缺少的 skill 加 discovery/save
   - install.sh missing/not executable → 生成/chmod
   - < 3 interactive skills → 在缺少的 skill 加 AskUserQuestion
4. Re-run validate-repo.sh
5. 報告 delta（baseline → final）

Score the build output using `references/build-benchmarks.md`.
Report: Build Quality Score X/10, average skill quality Y/30.
If Build Quality Score < 5, fix the weakest dimension before completing.

**STOP: 呈現驗證結果。全部通過才繼續。**

---

## Phase 6: 輕量 Pack Health（替代 Wave 2 的 /skill-check）

快速健康報告：

1. **類型分布** — 各類型 skill 數量（Review/Bridge/Production/Control/Runtime Helper）
2. **Artifact Flow 連通性** — 有產出但沒有消費者的 artifact？有消費但沒有來源的 artifact？
3. **明顯缺口** — 沒有 Bridge 層？Review 過多但 Production 不足？前重後輕？
4. 呈現報告，標記 WARNING 項目

---

## Phase 7: Completion

### Completion 萃取
報告 STATUS 前，回顧用戶在搭建過程中的輸入。
萃取 4 種信號（expertise / correction / preference / benchmark）到 `domain-config.json`。
詳見 `shared/methodology/context-accumulation-guide.md`。
大部分 session 不需要萃取。

1. `git add -A && git commit -m "feat: initial domain gstack generation"`
2. 呈現最終摘要：

```
STATUS: DONE

Domain: {name}
Skills: {count} ({by-type breakdown})
Validation: {pass}/{total}
Pack Health: {warnings count} warnings

建議下一步：
1. `/skill-check review --all` — 檢查所有生成的 skill 品質
2. `/skill-check pack` — 檢查整體結構健康度
3. 安裝: bash bin/install.sh
4. 測試: 用真實工作流跑一輪
5. 迭代: 根據使用回饋調整（/skill-edit, /domain-upgrade）
```

---

## Gotchas

1. **Claude 生成太 generic 的 skill** — 替換測試：把領域名稱換掉，如果 skill 還能用，就太 generic 了。每個 skill 必須有領域專屬的 gotchas、scoring formula、vocabulary
2. **Claude 忘記 artifact discovery/save** — 每個 skill 都必須在 Phase 0 搜尋上游 artifact，結尾寫出 artifact
3. **Claude 一口氣跑完不停** — 必須在每 5 個 skill 後 STOP，呈現進度表
4. **Claude 跳過 Review skill 的 scoring formula** — Review 型 skill 必須有明確的評分公式（不是「整體 7/10」）
5. **Claude 把所有內容塞進 SKILL.md** — 超過 200 行就拆到 references/
6. **Brownfield: Claude 改造時重寫整個 SKILL.md** — 改造是 Edit（追加），不是 Write（覆蓋）。用戶的原有結構必須保留。
7. **Brownfield: Claude 改造順序錯** — 必須先改造現有 skill 再生成新 skill。新 skill 需要理解現有 skill 的銜接點。
8. **Brownfield: Claude 忘記複製現有 skill** — 如果現有 skill 在不同目錄（不在 stack repo 裡），必須先複製過來再改造。
9. **Brownfield: Claude 統一改術語** — 現有 skill 的 Phase 名稱、術語、措辭是用戶的語言，不要統一成模板語言。

## Anti-Sycophancy

- 不要說「這個 domain stack 已經可以投入生產」— 它是 Draft 品質
- 不要跳過 Phase 6 的 pack health report — 即使一切看起來沒問題
- 不要說「所有 skill 都符合高品質標準」— 誠實報告每個 skill 的預估等級
