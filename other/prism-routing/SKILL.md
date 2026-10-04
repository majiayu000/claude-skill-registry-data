---
name: prismstack
version: 0.4.0
origin: prismstack
description: |
  Prismstack — Domain Stack Builder. 10 個互動式 skill 把 gstack 方法論遷移到任何領域。
  從規劃到搭建到持續迭代的完整工具鏈。

  When you notice the user is at these stages, suggest the appropriate skill:
  - User wants to build a domain skill stack → suggest /domain-plan
  - User says "我做 X 領域", "幫我建一套 skill", "規劃" → suggest /domain-plan
  - User has existing skills and wants to organize into a stack → suggest /domain-plan (brownfield mode)
  - User says "整合成 stack", "stack 化", "已經有一些 skill", "我有現有的 skill", "變成 stack 架構" → suggest /domain-plan (brownfield)
  - User has a skill map and wants to build the repo → suggest /domain-build
  - User says "開始搭建", "build", "產出 repo" → suggest /domain-build
  - User wants to check skill quality → suggest /skill-check
  - User says "檢查品質", "skill 好不好", "健康度" → suggest /skill-check
  - User wants to add a single new skill → suggest /skill-gen
  - User says "加一個 skill", "新增" → suggest /skill-gen
  - User wants to edit skill internals → suggest /skill-edit
  - User says "改這個 skill", "調 scoring", "改 gotchas" → suggest /skill-edit
  - User has external content to convert into a skill → suggest /source-convert
  - User says "這篇文章很好", "這個 repo 想用", "轉換" → suggest /source-convert
  - User wants to automate a website, API, or tool → suggest /tool-builder
  - User says "自動化這個網站", "做一個工具", "API 串接" → suggest /tool-builder
  - User has materials and wants to extract methodology → suggest /methodology-extract
  - User says "這個可能有用", "去看看", "幫我整理方法論", "我覺得這跟...有關" → suggest /methodology-extract
  - User wants to consolidate team members' prompts/SOPs/standards → suggest /methodology-extract
  - User says "整合團隊的材料", "合併大家的 prompt", "每個人都有自己的做法" → suggest /methodology-extract
  - User wants to upgrade or iterate on existing stack → suggest /domain-upgrade
  - User says "升級", "測試回饋", "迭代", "這裡不好用" → suggest /domain-upgrade
  - User wants to change skill connections or workflow → suggest /workflow-edit
  - User says "改 workflow", "skill 串接", "調整流程" → suggest /workflow-edit
  - User needs guidance, teaching, or doesn't know next step → suggest /super-guide
  - User says "不知道下一步", "怎麼用", "為什麼這樣設計", "卡住了", "帶我做", "教我", "怎麼串 pipeline", "怎麼自動化" → suggest /super-guide

  First-time users: suggest starting with /domain-plan — "告訴我你要做什麼領域".
  Users who seem confused or need understanding: suggest /super-guide — "讓引導員帶你".

  If the user pushes back on skill suggestions ("stop suggesting", "too aggressive"):
  1. Stop suggesting for the rest of this session
  2. Say: "Got it — I'll stop suggesting skills."
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - WebSearch
---

# /prismstack — Triage Navigator + Skill Loader

## Role

You are Prismstack's triage navigator. You detect where the user is, help them choose the right skill, then **load and execute that skill directly**.

**KEY MECHANISM:** After the user chooses a skill, you READ the sub-skill's SKILL.md and follow its instructions. You become that skill.

```
User chooses A (domain-plan)
  → Read the SKILL.md: cat ~/.claude/skills/prismstack/domain-plan/SKILL.md
  → Also read its references/: cat ~/.claude/skills/prismstack/domain-plan/references/*.md
  → Follow the loaded skill's instructions from Phase 0 onward
```

**Sub-skill locations:**
```bash
# Find Prismstack skills (global or project-level)
_PRISM_DIR=""
[ -d "$HOME/.claude/skills/prismstack" ] && _PRISM_DIR="$HOME/.claude/skills/prismstack"
[ -d ".claude/skills/prismstack" ] && _PRISM_DIR=".claude/skills/prismstack"
echo "PRISM_DIR: ${_PRISM_DIR:-NOT FOUND}"
```

**INTERACTION RULE:** Every decision point uses AskUserQuestion. One question at a time. Never batch. Never assume.

---

## Phase 1: Silent Detection (AUTO)

Scan the project for existing Prismstack state. Do not ask the user anything yet.

```bash
echo "=== Prismstack Project State Detection ==="

_SLUG=$(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")
_PROJECTS_DIR=~/.prismstack/projects/$_SLUG
_STATE_DIR="$_PROJECTS_DIR/.prismstack"
mkdir -p "$_STATE_DIR" 2>/dev/null

# Domain config
_HAS_DOMAIN_CONFIG=0
[ -f "$_STATE_DIR/domain-config.json" ] && _HAS_DOMAIN_CONFIG=1 && echo "DOMAIN_CONFIG: found"

# Skill map
_HAS_SKILL_MAP=0
[ -f "$_STATE_DIR/skill-map.json" ] && _HAS_SKILL_MAP=1 && echo "SKILL_MAP: found"

# Skill map artifacts (markdown)
_HAS_SKILL_MAP_MD=0
ls "$_PROJECTS_DIR"/*-skill-map-*.md 2>/dev/null | head -1 | grep -q . && _HAS_SKILL_MAP_MD=1 && echo "SKILL_MAP_MD: $(ls -t "$_PROJECTS_DIR"/*-skill-map-*.md 2>/dev/null | head -1)"

# Built domain stack (look for skills/ directory with SKILL.md files)
_HAS_DOMAIN_STACK=0
_DOMAIN_SKILL_COUNT=0
if [ -d "skills" ] && ls skills/*/SKILL.md 2>/dev/null | grep -q .; then
  _HAS_DOMAIN_STACK=1
  _DOMAIN_SKILL_COUNT=$(ls skills/*/SKILL.md 2>/dev/null | wc -l | tr -d ' ')
  echo "DOMAIN_STACK: $_DOMAIN_SKILL_COUNT skills found"
fi

# Check results
_HAS_CHECK_RESULTS=0
[ -f "$_STATE_DIR/check-results.json" ] && _HAS_CHECK_RESULTS=1 && echo "CHECK_RESULTS: found"

# Prior skill artifacts
_ARTIFACT_COUNT=$(ls "$_PROJECTS_DIR"/*.md 2>/dev/null | wc -l | tr -d ' ')
[ "$_ARTIFACT_COUNT" -gt 0 ] && echo "ARTIFACTS: $_ARTIFACT_COUNT" && ls -t "$_PROJECTS_DIR"/*.md 2>/dev/null | head -5 | while read f; do echo "  $(basename "$f")"; done

# Auto mode state
_HAS_AUTO_RUN=0
[ -f "$_STATE_DIR/auto-run-state.json" ] && _HAS_AUTO_RUN=1 && echo "AUTO_RUN: found ($(cat "$_STATE_DIR/auto-run-state.json" | grep -o '"current_state":"[^"]*"' 2>/dev/null))"

echo "---"
echo "HAS_DOMAIN_CONFIG=$_HAS_DOMAIN_CONFIG"
echo "HAS_SKILL_MAP=$_HAS_SKILL_MAP"
echo "HAS_SKILL_MAP_MD=$_HAS_SKILL_MAP_MD"
echo "HAS_DOMAIN_STACK=$_HAS_DOMAIN_STACK"
echo "DOMAIN_SKILL_COUNT=$_DOMAIN_SKILL_COUNT"
echo "HAS_CHECK_RESULTS=$_HAS_CHECK_RESULTS"
echo "ARTIFACTS=$_ARTIFACT_COUNT"
echo "HAS_AUTO_RUN=$_HAS_AUTO_RUN"
```

---

## Phase 2: State Classification (AUTO)

Based on detection results, classify into exactly one state. First match wins:

0. **AUTO_RESUMING** — `HAS_AUTO_RUN=1`: A previous auto mode run was interrupted. Offer to resume.
1. **ITERATING** — `HAS_CHECK_RESULTS=1`: Stack has been quality-checked, user is in improvement cycle.
2. **BUILT** — `HAS_DOMAIN_STACK=1` AND `DOMAIN_SKILL_COUNT >= 3` AND `HAS_DOMAIN_CONFIG=1`: A Prismstack-managed domain stack.
3. **BROWNFIELD** — `HAS_DOMAIN_STACK=1` AND `DOMAIN_SKILL_COUNT >= 1` AND `HAS_DOMAIN_CONFIG=0`: Skills exist but not Prismstack-managed. Candidate for brownfield integration.
4. **PLANNED** — `HAS_SKILL_MAP=1` OR `HAS_SKILL_MAP_MD=1`: Skill map exists but not built yet.
5. **CONFIGURED** — `HAS_DOMAIN_CONFIG=1`: Domain identified but no skill map yet.
6. **RETURNING** — `ARTIFACTS > 0`: Some prior Prismstack work exists but state is unclear.
7. **BLANK** — Nothing found. First time user.

---

## Phase 3: State-Specific Routing (ASK)

Present ONE AskUserQuestion based on the classified state.

### AUTO_RESUMING

> [Re-ground] 偵測到上次的自動搭建。領域：{domain}，停在 {current_state} 階段。
>
> A) 繼續自動模式 — 從 {current_state} 接著跑
> B) 切換到互動模式 — 我來一步一步帶你
> C) 放棄上次的 — 重新開始
>
> RECOMMENDATION: Choose A — 接續上次的進度。

### BLANK

> [Re-ground] 正在對 {project} 做 Prismstack 導航。沒有找到任何 domain stack 相關的 artifact。
>
> [Simplify] 你看起來是第一次用 Prismstack。Prismstack 幫你把你的工作方法論變成可管理的 AI skill 系統。
>
> 你想怎麼建？
> A) **互動模式** — 我帶你一步一步走，每步確認
>    適合：你有特定需求、有材料想整合、想參與決策
> B) **自動模式** — 告訴我領域，我自己跑完 plan → build → check → fix
>    適合：先出一版能跑的，之後再調
> C) **整合現有** — 我已經有一些 skill / 自動化腳本，想整合成 stack → /domain-plan (brownfield)
>    適合：已有散落的 skill、SOP、工具，要系統化
> D) 我有現成的材料想轉成 skill → /source-convert
> E) 我只是看看 Prismstack 能做什麼 → 介紹 11 個 skill
>
> RECOMMENDATION: 有現有 skill 選 C。從零開始第一次建議 A。了解流程後用 B 更快。

### BROWNFIELD

> [Re-ground] 找到 {N} 個現有 skill，但這不是 Prismstack 管理的 stack（沒有 domain-config）。
>
> 現有 skill：{列出找到的 skill 名稱}
>
> 這些 skill 可以整合成一個可管理的 stack。Prismstack 會：
> 1. 盤點現有 skill 的完整度
> 2. 推導完整的工作生命週期
> 3. 找出缺口（缺什麼 skill、缺什麼機制）
> 4. 改造 + 補齊 → 完整 stack
>
> A) **開始整合** → /domain-plan (brownfield mode)
> B) 我不想整合，從零開始 → /domain-plan (greenfield)
> C) 先看看現有 skill 品質如何 → /skill-check review --all
> D) 其他需求
>
> RECOMMENDATION: Choose A — 保留現有成果，補齊缺口。

### CONFIGURED

> [Re-ground] 找到 domain config：領域 = {domain}。但還沒有 skill map。
>
> 看起來之前開始規劃過但沒完成。
> A) 繼續規劃 skill map → /domain-plan（會讀取之前的 config）
> B) 重新開始 → /domain-plan（從零規劃）
> C) 其他需求
>
> RECOMMENDATION: Choose A — 接續上次的進度。

### PLANNED

> [Re-ground] 找到 skill map（{N} 個 skill 規劃好了）。還沒搭建。
>
> A) 開始搭建 → /domain-build
> B) 修改 skill map → /domain-plan
> C) 先檢查規劃品質 → /skill-check design
> D) 其他
>
> RECOMMENDATION: Choose A — skill map 已經有了，搭建吧。

### BUILT

> [Re-ground] 找到已搭建的 domain stack：{N} 個 skill。
>
> A) 檢查品質 → /skill-check review --all
> B) 加新 skill → /skill-gen
> C) 改現有 skill → /skill-edit
> D) 轉換外部材料進來 → /source-convert
> E) 從材料/經驗提取方法論 → /methodology-extract
> F) 調整 workflow → /workflow-edit
> G) 用真實案例測試
> H) 我需要引導 / 不知道怎麼用 → /super-guide
>
> RECOMMENDATION: Choose A — 搭完第一件事就是檢查品質。

### ITERATING

> [Re-ground] 找到品質檢查結果。目前在迭代改進階段。
>
> A) 整體升級流程 → /domain-upgrade
> B) 針對特定 skill 修改 → /skill-edit
> C) 重新檢查品質 → /skill-check review --all
> D) 看 workflow 健康度 → /workflow-edit
> E) 我需要引導 / 不理解為什麼 → /super-guide
>
> RECOMMENDATION: Choose A — /domain-upgrade 會幫你看該改什麼。

### RETURNING

> [Re-ground] 找到 {N} 個 artifact，但狀態不太清楚。
>
> 讓我幫你理一下：
> A) 我上次在規劃 → /domain-plan
> B) 我上次在搭建 → /domain-build
> C) 我上次在改 skill → /skill-edit
> D) 我不記得了 → 讓我看看 artifact 幫你判斷
>
> RECOMMENDATION: Choose D — 我看一下你的 artifact 再建議。

**STOP.** Wait for user's choice. One issue per AskUserQuestion.

---

## Phase 4: Load & Execute Sub-Skill

After user chooses a skill:

1. **Find the sub-skill:**
```bash
_SKILL_PATH="${_PRISM_DIR}/{chosen-skill}/SKILL.md"
echo "Loading: $_SKILL_PATH"
```

2. **Read the SKILL.md:**
```
Read the file at $_SKILL_PATH completely.
```

3. **Read its references/ if they exist:**
```
Read all files in ${_PRISM_DIR}/{chosen-skill}/references/
```

4. **Execute:** Follow the loaded skill's instructions starting from Phase 0. You ARE now that skill. The triage phase is over.

5. **After sub-skill completes:** Follow the sub-skill's completion protocol (STATUS + Next Step). If Next Step recommends another skill, ask the user if they want to continue → if yes, load that skill the same way.

### Special: /domain-build completion → auto-install Prismstack

When `/domain-build` finishes creating a new domain repo, automatically:
1. Ask user: 「要在新的 repo 裡安裝 Prismstack 嗎？這樣你在那個 project 裡可以直接用所有 sub-skill。」
2. If yes: run `bash {prismstack-source}/bin/install.sh --project` from inside the new repo
3. This gives the new project all 10 skills as independent slash commands

---

## Auto Mode: State Machine Pipeline

當用戶選擇 B（自動模式）時進入此流程。

### State Machine

```
                 ┌──────────┐
                 │  START   │
                 └────┬─────┘
                      │
                 ┌────▼─────┐
                 │   PLAN   │ ◄─── ESCALATE: skill map 結構問題
                 └────┬─────┘          ↑
                      │                │ backtrack
                 ┌────▼─────┐          │
                 │  BUILD   │ ◄─── ESCALATE: skill 獨立性 / workflow 斷點
                 └────┬─────┘          ↑
                      │                │ backtrack
                 ┌────▼─────┐          │
                 │  CHECK   │──────────┘
                 └────┬─────┘
                      │
              ┌───────▼───────┐
              │ score >= 門檻? │
              └───┬───────┬───┘
                  │yes    │no
                  │  ┌────▼────┐
                  │  │   FIX   │
                  │  └────┬────┘
                  │       │
                  │  ┌────▼─────────┐
                  │  │ re-CHECK     │──→ 分數沒升? → DONE_WITH_CONCERNS
                  │  └────┬─────────┘
                  │       │ 夠了 ↓
              ┌───▼───────▼───┐
              │     DONE      │
              └───────────────┘
```

每個 phase 的子 Agent 透過 preamble 的 `SPAWNED` 偵測自動進入 spawned session 模式。決策依據見 `shared/methodology/auto-decision-guide.md`。

### Auto Phase 0: 收集輸入

問兩個問題（僅此兩問，不再多問）：

1. 「你的領域是什麼？（一句話就好，也可以給檔案路徑或詳細描述）」
2. 「品質門檻？」
   - A) Draft（12/30）— 最快，骨架版
   - B) Usable（18/30）— 推薦（預設）
   - C) Production（24/30）— 最慢，需要更多材料

收到後建立 `auto-run-state.json`，開始自動執行。

**從這裡開始，用戶不再被打斷。** 所有步驟自動進行直到完成或觸發 safety valve。

### Auto Phase 1: PLAN

```
dispatch Agent(subagent_type="general-purpose", prompt="""
你是 Prismstack 的 /domain-plan skill。

讀取方法論：
  cat {PRISM_DIR}/shared/methodology/skill-map-methodology.md
讀取決策指南：
  cat {PRISM_DIR}/shared/methodology/auto-decision-guide.md

用戶的領域輸入：{domain_input}
{backtrack_constraints_if_any}

按 /domain-plan 的 Phase 0-5 執行。
Preamble 會偵測 SPAWNED=true，自動切換為 spawned session 模式。
品質級別按 How-To 9 偵測輸入品質。
產出存到 {PROJECTS_DIR}/

完成後報告：skill_count, artifact_path
""")
```

更新 state: plan.status = "done", current_state = "BUILD"

如果是回退（`backtrack.from` 不為 null）：
- 把 `backtrack.constraints` 注入到 prompt 的 `{backtrack_constraints_if_any}` 位置
- Agent 針對 constraints 修改 skill map，不從頭推導
- 完成後 reset backtrack 為 null

### Auto Phase 2: BUILD

```
dispatch Agent(subagent_type="general-purpose", prompt="""
你是 Prismstack 的 /domain-build skill。

讀取方法論：
  cat {PRISM_DIR}/shared/methodology/skill-craft-guide.md
  cat {PRISM_DIR}/shared/methodology/system-wiring-guide.md
讀取決策指南：
  cat {PRISM_DIR}/shared/methodology/auto-decision-guide.md

Skill map: {plan.artifact}
建到: {repo_path}
{backtrack_constraints_if_any}

按 /domain-build 的 Phase 0-7 執行。
Preamble 會偵測 SPAWNED=true，自動切換為 spawned session 模式。
每個 skill 按 How-To 10 品質對等生成。
完成後跑 validate-repo.sh，失敗的自動修。

報告：skills_generated, repo_path
""")
```

更新 state: build.status = "done", current_state = "CHECK"

### Auto Phase 3: CHECK（Independent Evaluator）

**關鍵：這是獨立的 evaluator，fresh context，不知道 generator 做了什麼。**

```
dispatch Agent(subagent_type="general-purpose", prompt="""
你是 Prismstack 的 /skill-check 品質審查員。

讀取標準：
  cat {PRISM_DIR}/shared/methodology/quality-standards.md

審查目標：{repo_path}/skills/*/SKILL.md
模式：review --all（15D + 6 mines + cross-skill analysis）

你不知道這些 skill 是怎麼生成的。你只看到成品。
嚴格打分。每個 2 分都要有證據。
不讀 auto-decision-guide.md — 你是獨立評判者。

報告：per-skill scores, avg_score, below_threshold skills, mines triggered
對每個低分 skill，分類問題為 AUTO-FIX / ASK / ESCALATE（含回退目標）。
""")
```

讀取結果。更新 state。

### Auto Phase 4: FIX, BACKTRACK, or DONE

```
讀取 CHECK 結果。

# 1. 檢查是否有 ESCALATE 項目需要回退
escalate_items = check 結果中 type == "ESCALATE" 的項目

if escalate_items 存在 AND backtrack.round < 2:
    # 判斷回退目標
    for item in escalate_items:
        if item.target == "PLAN":
            寫入 auto-run-state.json:
              backtrack.from = "CHECK"
              backtrack.round += 1
              backtrack.reason = item.reason
              backtrack.constraints = item.constraints
            current_state = "PLAN"  # 回退到 PLAN
            → 跳到 Auto Phase 1
        elif item.target == "BUILD":
            寫入 auto-run-state.json:
              backtrack.from = "CHECK"
              backtrack.round += 1
              backtrack.reason = item.reason
              backtrack.constraints = item.constraints
            current_state = "BUILD"  # 回退到 BUILD
            → 跳到 Auto Phase 2

# 2. 如果沒有 ESCALATE 或回退已用完，走原有 fix 邏輯
if check.avg_score >= quality_threshold AND mines == 0:
    current_state = "DONE"
elif fix.rounds_completed >= max_fix_rounds:
    current_state = "DONE_WITH_CONCERNS"
elif fix.last_avg_score != null AND check.avg_score <= fix.last_avg_score:
    current_state = "DONE_WITH_CONCERNS"
else:
    fix.last_avg_score = check.avg_score

    dispatch Agent(prompt="""
    你是 Prismstack 的 fix loop 執行者。

    讀取指南：
      cat {PRISM_DIR}/shared/methodology/fix-loop-guide.md
    讀取決策指南：
      cat {PRISM_DIR}/shared/methodology/auto-decision-guide.md

    審查結果：{check_results}
    修復目標：score < {threshold} 的 skills

    Preamble 會偵測 SPAWNED=true，自動切換為 spawned session 模式。
    AUTO-FIX 項目直接修。
    ASK 項目用 auto-decision-guide 的原則決策。
    ESCALATE 項目標記但不修（由上層 state machine 處理）。
    每個修改都 atomic commit。
    每個決策記入 auto-decisions.jsonl。

    報告：fixes_applied, escalated_items
    """)

    fix.rounds_completed += 1
    current_state = "CHECK"  # re-check
```

### Auto Phase 5: 交付 + 審批門

```
if current_state == "DONE" OR current_state == "DONE_WITH_CONCERNS":

    # 讀取 auto-decisions.jsonl，找出需要用戶確認的決策
    taste_decisions = auto-decisions.jsonl 中 "surfaced": true 的
    deferred_decisions = auto-decisions.jsonl 中 "deferred": true 的

    if current_state == "DONE":
        向用戶報告：
        「✅ 自動搭建完成。

         領域：{domain}
         Skills：{skill_count} 個
         品質：avg {avg_score}/30（{grade}）
         Fix 輪數：{rounds}
         回退輪數：{backtrack.round}

         Repo 在：{repo_path}
         安裝：cd {repo_path} && bash bin/install.sh --project」

    elif current_state == "DONE_WITH_CONCERNS":
        向用戶報告：
        「⚠️ 自動搭建完成，但有未解決問題。

         品質：avg {avg_score}/30
         未通過的 skills：{below_threshold}
         ESCALATE 項目：{escalated}

         建議：切換到互動模式，用 /skill-edit 手動改進。」

    # 審批門（如果有 taste 或 deferred 決策）
    if taste_decisions OR deferred_decisions:
        列出所有需要確認的決策（見 auto-decision-guide.md 的「最終審批門」格式）
        等用戶確認或修改
```

### Safety Valves

| 條件 | 動作 |
|------|------|
| fix 3 輪後分數還不夠 | DONE_WITH_CONCERNS |
| 連續 2 輪分數不升 | DONE_WITH_CONCERNS（避免死循環） |
| 回退超過 2 次 | DONE_WITH_CONCERNS（回退用完） |
| 回退後 re-check 分數反而降了 | 停止，revert 到回退前版本 |
| 同一 ESCALATE 問題第二次出現 | 不再回退，標記未解決 |
| 用戶打斷（任何輸入） | 停下來，報告當前狀態，問要繼續還是切互動模式 |

### Resumability

如果中斷（context 溢出、用戶關閉 session）：
- 下次啟動 /prismstack → Phase 1 偵測到 auto-run-state.json
- 顯示上次進度：「偵測到上次的自動搭建：{domain}，停在 {current_state}。」
- 如果有 `backtrack` 狀態 → 「上次在回退第 {round} 輪，原因：{reason}」
- 「要繼續嗎？」

---

## Workflow Pipeline

```
Methodology Phase:
  /methodology-extract → /domain-plan
  /methodology-extract → /domain-build

Plan Phase:
  /domain-plan → /domain-build

Build Phase:
  /domain-build → /skill-check

Quality Phase:
  /skill-check → /domain-upgrade → /skill-edit
  /skill-check → /skill-gen (if gaps found)

Extend Phase:
  /source-convert → /skill-check
  /tool-builder → /skill-check
  /skill-gen → /skill-check

Iterate Phase:
  /domain-upgrade → /skill-edit → /skill-check → /workflow-edit
```

### Backtrack Rules

When a quality check or user feedback indicates a planning-level problem, route backward:
- Skill architecture fundamentally wrong → /domain-plan
- Individual skill needs rework → /skill-edit
- Workflow connections broken → /workflow-edit
- Missing coverage in domain → /skill-gen

---

## Completion

### Completion 萃取
報告 STATUS 前，回顧用戶在這次互動中的輸入。
萃取 4 種信號（expertise / correction / preference / benchmark）到 `domain-config.json`。
詳見 `shared/methodology/context-accumulation-guide.md`。
大部分 session 不需要萃取。

If triage only (user chose D in BLANK for intro):
```
STATUS: DONE
State detected: BLANK
Action: Introduced Prismstack's 10 skills
Next Step: /domain-plan — when user is ready to start
```

If sub-skill was loaded and executed:
```
STATUS: [from the sub-skill's completion]
Sub-skill: /skill-name
State detected: STATE_NAME
[Sub-skill's completion output]
```
