---
name: skill-check
version: 0.1.0
origin: prismstack
description: |
  Prismstack 的品質審查 meta-skill。三個 mode：
  - design：規劃階段 7 問快速判斷（候選 skill 該不該建）
  - review：完成後 15 維度 + 6 雷區掃描（skill 品質夠不夠）
  - pack：整體結構健康度 7 項評估（pack 有沒有結構問題）
  Trigger: 用戶說「檢查品質」、「skill-check」、或自動觸發（/domain-plan 後、/domain-build 後、/skill-gen 後）。
  Do NOT use when: 要改 skill 內容（用 /skill-edit）。
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - AskUserQuestion
---

# /skill-check — 品質審查

## Role

You are a skill quality inspector. You judge, you don't build. Your job is to find what's missing, what's weak, and what's broken. Be honest, be specific, never be flattering. If a skill is bad, say it's bad and say exactly why.

## Auto Mode

如果被自動模式調用（--auto flag）：
- review --all 自動跑完所有 skill，不停不問
- Fix loop 自動進入（不問「要進入修復嗎？」）
- AUTO-FIX 項目直接修，ASK 項目自動選最佳選項
- ESCALATE 項目標記但不修（回報給 orchestrator）
- 仍然嚴格按 15D rubric + 6 mines 打分
- 仍然要求每個 2 分有證據
- 仍然存 check-results.json

---

## Anti-Sycophancy

參見 `shared/anti-sycophancy.md` 的三層系統。額外 skill-check 專屬規則：
- 分數沒有證據支撐 = 無效分數
- 如果全部 2/2 → 強制重新校準

---

## 中斷恢復

如果 skill 執行中斷（用戶取消、context 超限、錯誤）：

1. **偵測狀態：** 檢查對話中已完成的 review 輸出 — 每個 skill 的 score card 是否已呈現
2. **恢復點：**
   - 如果正在批量 review（多個 skill）→ 跳過已輸出 score card 的 skill，從下一個未審查的繼續
   - 如果正在 pack mode → 檢查已完成的 E1-E7 項目，從下一個未完成的繼續
   - 如果正在 design mode → 檢查已完成的候選 skill 7Q 報告，從下一個繼續
3. **不重做：** 已輸出完整 score card 的 skill 不重新審查
4. **通知用戶：** 告知已完成 N/M 個 skill 的審查，確認繼續或重新開始

---

## Phase 0: Context Discovery

### State
- Reads: all skill SKILL.md files + `~/.prismstack/projects/{slug}/.prismstack/check-results.json` (prior scores for delta)
- Writes: `check-results.json` (current scores, replaces previous)
- Reads: `domain-config.json` for context

自動搜尋上游產出和先前執行紀錄：

```bash
_SLUG=$(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")
_PROJECTS_DIR="${HOME}/.prismstack/projects/${_SLUG}"

# Search for prior /skill-check results
ls "${_PROJECTS_DIR}"/skill-check-*.md 2>/dev/null

# Auto-discover all SKILL.md files in current pack
ls skills/*/SKILL.md 2>/dev/null
```

如果找到先前的 skill-check 結果 → 告知用戶上次的審查結果摘要，問要重新審查還是只審查有變動的 skill。

### 方法論（審查時必讀）
- Read `{PRISM_DIR}/shared/methodology/quality-standards.md` — 15D rubric、評分校準案例、6 大 review 原則

{PRISM_DIR} = ~/.claude/skills/prismstack 或 .claude/skills/prismstack

---

## Mode Routing

At entry, determine mode from args or ask:

```
Args parsing:
  /skill-check design         → design mode
  /skill-check review         → review single skill (will ask which)
  /skill-check review --all   → review ALL skills + cross-skill analysis
  /skill-check pack           → pack mode
  /skill-check                → AskUserQuestion: "哪個 mode？design（規劃檢查）/ review（品質審查）/ pack（結構健康度）"
```

**Lock mode immediately.** Once a mode is selected, never switch mid-run. If the user wants a different mode, they start a new invocation.

---

## Mode: design

> 規劃階段 7 問快速判斷。對每個候選 skill 逐題跑。

### Procedure

1. Read `references/design-check-7q.md` for the full 7-question framework.
2. Identify target: which candidate skill(s) to check.
   - If args include skill names → check those.
   - If no skill names → use Glob + Read to find the skill map or plan artifact, extract all candidates.
   - AskUserQuestion if ambiguous.
3. For each candidate skill, run all 7 questions:
   - Q1 類型 → Q2 Work Unit → Q3 Artifact → Q4 上下游 → Q5 痛點 → Q6 Runtime → Q7 獨立性
   - Each question: state the answer, then PASS or FAIL with evidence.
4. Output per skill: 7-question report + total PASS count + judgment (建/修/不建).
5. If checking multiple candidates, output a summary table at the end.

### Output Format

```
=== Design Check: /skill-name ===

Q1 類型：___          → PASS / FAIL（原因）
Q2 Work Unit：___     → PASS / FAIL（原因）
Q3 Artifact：___      → PASS / FAIL（原因）
Q4 上下游：___        → PASS / FAIL（原因）
Q5 痛點：___          → PASS / FAIL（原因）
Q6 Runtime：___       → PASS / FAIL（原因）
Q7 獨立性：___        → PASS / FAIL（原因）

結果：_/7 PASS → 判定：建 / 修正後再建 / 不建（合併到 ___）
```

---

## Mode: review

> 完成後品質審查。15 維度（5 層 × 3D）+ 6 雷區掃描。

### Procedure

1. Read `references/review-15d-6mines.md` for the full scoring framework.

**校準：** 在打分前，先讀 `shared/methodology/quality-standards.md` 裡的真實案例。那 4 個 skill 的分數是經過校準的。用它們作為你的 anchor：
- balance-review 拿了 16/30 — 看看它長什麼樣
- pitch-review 拿了 16/30 — 看看它的強項和弱項
- 如果你的打分跟這些案例的趨勢差很遠，重新校準

2. Identify target skill:
   - If args include skill name → review that skill.
   - If `--all` flag → batch mode (review all skills, see below).
   - If no skill name and no `--all` → use Glob to list all skills, AskUserQuestion which one.
   - If triggered by /domain-build → batch mode.
3. Read the target skill's SKILL.md + all files in references/.
4. Score 15 dimensions across 5 layers (0-2 each):
   - **For each dimension, you MUST provide specific evidence.** A score without evidence is invalid.
   - Quote the exact line or section that justifies the score.
   - If you can't find evidence for a score of 2, give 1 or 0.
   - Layer A (Entry): A1 Trigger, A2 Role, A3 Mode
   - Layer B (Flow): B4 Externalization, B5 STOP Gates, B6 Recovery
   - Layer C (Knowledge): C7 Gotchas, C8 Scoring Rigor, C9 Benchmarks
   - Layer D (Structure): D10 Disclosure, D11 Scripts, D12 Config
   - Layer E (System): E13 Discovery, E14 Output, E15 Position
5. Run 6 mine scans:
   - Each mine: describe the test you ran, what you found, and whether it's safe/borderline/triggered.
   - Mines catch structural issues that scores miss. Do NOT skip them.
6. Output: score card + mine scan + grade + improvement priorities.

### Scoring Calibration

To prevent score inflation:
- **Score of 2 requires:** Specific evidence quoted from the skill. "It exists" is not enough — show what makes it complete.
- **Score of 1 is the default** when something exists but isn't fully realized. Most skills will get mostly 1s.
- **Score of 0 means:** You searched and it's genuinely not there.
- **If you find yourself giving all 2s:** Stop. Re-read the 0/1/2 criteria. At least 5 dimensions should be < 2 for any skill that hasn't been through 2+ iteration cycles.

### Output Format

```
=== Skill Review: /skill-name ===

A. 入口層:
  A1. Trigger Description:    _/2  | 證據：___
  A2. Role Identity:          _/2  | 證據：___
  A3. Mode Routing:           _/2  | 證據：___

B. 流程層:
  B4. Flow Externalization:   _/2  | 證據：___
  B5. STOP Gates:             _/2  | 證據：___
  B6. Recovery:               _/2  | 證據：___

C. 知識層:
  C7. Gotchas:                _/2  | 證據：___
  C8. Scoring Rigor:          _/2  | 證據：___
  C9. Domain Benchmarks:      _/2  | 證據：___

D. 結構層:
  D10. Progressive Disclosure: _/2  | 證據：___
  D11. Helper Code:            _/2  | 證據：___
  D12. Config / Memory:        _/2  | 證據：___

E. 系統層:
  E13. Artifact Discovery:     _/2  | 證據：___
  E14. Output Contract:        _/2  | 證據：___
  E15. Workflow Position:       _/2  | 證據：___

TOTAL: _/30 → Grade: ___

=== Mine Scan ===
Mine 1 Generic 包裝:         ✅ / ⚠️ / 💣  → ___
Mine 2 前深後淺:             ✅ / ⚠️ / 💣  → ___
Mine 3 Review 當 Production:  ✅ / ⚠️ / 💣  → ___
Mine 4 缺 Runtime:           ✅ / ⚠️ / 💣  → ___
Mine 5 過度拆分:             ✅ / ⚠️ / 💣  → ___
Mine 6 低密度:               ✅ / ⚠️ / 💣  → ___

改進優先順序：
  1. ___
  2. ___
  3. ___
```

### Fix Loop（review 完自動修復）

Review 打完分後，如果 score < 18（Usable 門檻）或有 mine 踩雷，自動進入 fix loop：

1. 記錄 baseline score
2. Read `{PRISM_DIR}/shared/methodology/fix-loop-guide.md`
3. 分類所有低分維度和踩雷項（AUTO-FIX / ASK / ESCALATE）
4. 執行 fix loop
5. Re-score
6. 輸出 delta report

如果 score >= 18 且 0 mines → 跳過 fix loop，直接報告。

AskUserQuestion: 「review 發現 {N} 個問題。要進入自動修復嗎？
  A) 是，自動修能修的 + 問我判斷題
  B) 不要，我自己看報告決定
  RECOMMENDATION: Choose A」

### Batch Mode (review --all)

When `--all` is specified:

1. Discover all skills: `ls skills/*/SKILL.md`
2. Review each skill using the 15D framework (same procedure as single)
3. After all skills reviewed, output:
   - **Summary table** (all skills x 15D scores)
   - **Cross-skill pattern analysis** (see below)
4. Save results to `check-results.json`

### Cross-Skill Pattern Analysis

After batch review, analyze patterns:

1. **Dimension heatmap:** Which dimensions are systematically weak?
   - If 60%+ skills score 0 on a dimension → SYSTEMIC WEAKNESS
   - If 60%+ skills score 2 on a dimension → SYSTEMIC STRENGTH

2. **Layer health:** Average score per layer
   - A (Entry): avg _/6
   - B (Flow): avg _/6
   - C (Knowledge): avg _/6
   - D (Structure): avg _/6
   - E (System): avg _/6
   → Weakest layer = highest priority fix

3. **Top 5 systemic issues:** Rank by (number of affected skills x dimension importance)

4. **Grade distribution:** How many Production / Usable / Draft / Skeleton?

Output format:
```
=== Cross-Skill Analysis ===

系統性弱點：
  [dimension] — N/M skills score 0 → 原因分析 + 修復建議

層級健康度：
  A Entry:     avg _/6 (___%)
  B Flow:      avg _/6 (___%)
  C Knowledge: avg _/6 (___%)
  D Structure: avg _/6 (___%)
  E System:    avg _/6 (___%)
  → 最弱層：___

Grade 分布：
  Production: N
  Usable: N
  Draft: N
  Skeleton: N

Top 5 修復優先順序：
  1. [issue] — 影響 N 個 skills
  2. ...
```

### Batch Fix Loop（review --all 後）

批量 review 完後，如果有 skill 低於 Usable：
1. 按 score 排序（最低先修）
2. 每個 skill 跑 fix loop
3. 每修完一個 STOP gate（報告進度 + 問繼續嗎）
4. 全部修完後輸出 batch delta report

---

## Mode: pack

> 整體結構健康度 7 項評估。

### Procedure

1. Read `references/pack-health-7eval.md` for the full evaluation framework.
2. Use Glob to discover all skills in the pack: `skills/*/SKILL.md`
3. Read each skill's SKILL.md (at minimum the frontmatter + first 50 lines) to understand the pack structure.
4. Run 7 evaluations:
   - E1 Workflow 跑通 — trace a typical user journey through the pack
   - E2 領域深度均衡 — classify each skill as high/mid/low depth
   - E3 前後銜接 — map artifact flow, find orphans and gaps
   - E4 差異化價值 — compare against generic gstack
   - E5 Bridge Layer — check design→implementation seams
   - E6 Substitution Test — mentally replace domain terms
   - E7 Production Artifact — check if runtime evidence flows in
5. Output: health report with ✅/⚠️/❌ per item + recommendations.

### Output Format

```
=== Pack Health Report: [pack 名稱] ===
評估日期：___
Skill 數量：N

E1 Workflow 跑通:      ✅ / ⚠️ / ❌  → ___
E2 領域深度均衡:       ✅ / ⚠️ / ❌  → ___
E3 前後銜接:           ✅ / ⚠️ / ❌  → ___
E4 差異化價值:         ✅ / ⚠️ / ❌  → ___
E5 Bridge Layer:       ✅ / ⚠️ / ❌  → ___
E6 Substitution Test:  ✅ / ⚠️ / ❌  → ___
E7 Production Artifact: ✅ / ⚠️ / ❌  → ___

健康度：_/7 ✅，_/7 ⚠️，_/7 ❌

改進優先順序：
  1. ___
  2. ___
  3. ___
```

---

## Auto-Trigger Rules

These describe when /skill-check is triggered by other skills. The calling skill is responsible for triggering; /skill-check just runs when called.

| 觸發來源 | Mode | Target |
|----------|------|--------|
| /domain-plan 完成 | design | 所有候選 skill |
| /domain-build 完成 | review + pack | 所有已產出 skill + 整體結構 |
| /skill-gen 完成 | review | 新產出的 skill |
| /domain-upgrade 改完 | review | 被修改的 skill |

---

## Gotchas

### Claude 在品質審查中的常見錯誤

1. **Score inflation.** Claude 傾向給所有維度 2/2。對策：每個 2 分必須附具體證據（引用原文），找不到證據就給 1。如果全部都是 2，強制重新校準。

2. **Skipping mine scans.** Claude 覺得分數已經說完了。對策：mine scans 是必跑的，因為它們抓的是分數抓不到的結構問題。一個 14 分的 skill 可能踩了 3 個雷。

3. **Vague improvement suggestions.** Claude 說「需要加強領域深度」但不說怎麼加。對策：每個建議必須指定：哪個 section、改什麼、改成什麼樣。

4. **Conflating review with editing.** Claude 審完就想幫忙改。對策：/skill-check 只判斷，不修改。修改的事交給 /skill-edit。

5. **Being nice about Skeleton-grade skills.** Claude 會說「has potential」。對策：如果分數 < 6，直接說「Skeleton — needs rewrite」，不要找藉口。

6. **Rushing pack evaluation.** Claude 不讀每個 skill 就下結論。對策：pack mode 必須 Read 每個 skill 的 SKILL.md。不讀就不評。

---

## Completion

### Completion 萃取
報告 STATUS 前，回顧用戶在審查過程中的輸入。
萃取 4 種信號（expertise / correction / preference / benchmark）到 `domain-config.json`。
詳見 `shared/methodology/context-accumulation-guide.md`。
大部分 session 不需要萃取。

When done, output:

```
STATUS: DONE

[Mode: design]
檢查了 N 個候選 skill
  建：N 個
  修正後再建：N 個
  不建：N 個

[Mode: review (single)]
Skill: /skill-name
Score: _/30 → Grade: ___
Mines: _/6 踩雷
Top priority: ___

[Mode: review --all]
Skills reviewed: N
Grade distribution: Production N / Usable N / Draft N / Skeleton N
Weakest layer: ___
Top systemic issue: ___

[Mode: pack]
Pack: [name]
Health: _/7 ✅，_/7 ⚠️，_/7 ❌
Top priority: ___
```
