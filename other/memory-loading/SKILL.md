---
name: memory-loading
description: "This skill should be used by all maigo agents at startup, before beginning work, to load relevant cross-project memory entries with relevance-based ordering and a 10-entry cap. Consumers: Raana, Tomori, Soyo, the orchestrator itself, and any future agent that reads ~/.config/maigo/memory/."
---

<!-- mkdocs-include-start -->

# Memory Loading

**Owner**: all agents
**Consumers**: [`agents/Raana.md`](https://github.com/Lee-W/maigo/blob/main/agents/Raana.md)、[`agents/Tomori.md`](https://github.com/Lee-W/maigo/blob/main/agents/Tomori.md)、[`agents/Soyo.md`](https://github.com/Lee-W/maigo/blob/main/agents/Soyo.md)、orchestrator 本身

## 為什麼這個 skill 存在

三個 agent 在啟動時都要做相同的「讀記憶 → schema 自檢 → fallback」流程，但過去各自在 agent prompt 裡重複寫。這個 skill 是三者共通行為的 single source of truth。

**orchestrator 自己也是 consumer**：orchestrator 開始跑任何 `/maigo:*` 流程前，也要主動查一次
memory，不能只靠 delegate 給 Raana/Tomori/Soyo 時才觸發這個 skill——曾經因為只有 delegate 對象
會查記憶，orchestrator 自己重複違反同一條「背景 agent 不用 ScheduleWakeup 輪詢」的教訓，兩次都
沒查過記憶就重犯（見 [`skills/failure-handling`](https://github.com/Lee-W/maigo/blob/main/skills/failure-handling/SKILL.md)「等待自己開的背景 agent」段）。

## 標準 5 步流程

啟動後、正式開始工作之前，先載入記憶（兩層）：

1. **依序讀兩個 index**：
   - **Cross-project**：`cat ~/.config/maigo/memory/MEMORY.md`
   - **Per-project**：`cat ~/.claude/projects/<current-project>/memory/MEMORY.md`（若存在）

   `<current-project>` 是當前專案路徑 slug 化的結果（與 `validate_memory.py` 相同的枚舉方式——即 `~/.claude/projects/` 下對應的目錄名，例如 `-Users-weilee-Programming-personal-maigo`）。

2. **讀 index 每行** `- [Title](file.md) — description`（兩層 index 合併），判斷哪些 description 跟當前 task 的 keyword / 主題有 overlap
3. **相關性排序**：把**兩層合併後**的候選 entry 依匹配度排序
4. **限量載入**：若相關條目過多，僅 Read 最相關的前 10 筆 entry 全文——**10 筆是兩層合計上限，不是每層各 10**；當作這次工作的 context
5. **在輸出開頭印 `## Loaded memory entries` 段**，列出用了哪些 entry

## Schema 自檢（lazy）

對每個讀進來的 entry frontmatter 做最小檢查：

- 缺 `name` / `description` / `type` 任一欄位
- `type` 值不在 `{user, feedback, project, reference}`

遇到問題**不 abort**，繼續使用該 entry（lenient），但在 `## Loaded memory entries` 段該行末尾加 `[schema warn: <缺什麼或 type 不合法>]`。

完整檢查可手動跑 [`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_memory.py"`](https://github.com/Lee-W/maigo/blob/main/scripts/validate_memory.py)。

## Fallback 規則（不報錯、不抱怨、繼續做事）

兩層各自獨立 fallback，任一層不影響另一層：

- 某一層目錄不存在 → 該層當「沒記憶」，另一層照常讀
- 某一層 `MEMORY.md` 不存在或是空的 → 該層當「沒記憶」，另一層照常讀
- 某一層 index 裡完全沒有跟當前 task 相關的 entry → 該層當「沒記憶」，另一層照常讀
- **兩層皆無相關記憶**才整體當「沒記憶」處理

不要求使用者建立 memory 目錄或 index。

## 輸出格式範例

```
## Loaded memory entries
- [Integration test 偏好](integration-test-preference.md) — 已載入
- [Some entry](some-entry.md) — 已載入 [schema warn: 缺 type]
（若無相關 entry：「（無相關 entry）」）
```

## 開口問環境問題前先掃記憶

Orchestrator 要開口問使用者環境／工具類問題（「你有沒有 X 工具/流程/基礎設施？」
「你用什麼管 X？」）前，先照上面的標準流程掃過兩層記憶庫，特別留意 `type: reference`
的條目——這類條目常常正好是答案，卻不會被使用者自己想起來提。

**Why**：記憶庫存在的意義就是代替使用者記得。曾有一次在設計跨機器同步方案時，直接
開口問使用者「有沒有現成的 dotfiles 流程」，使用者當下答案不完整——但一份
`type: reference` 記憶其實早就記著答案，直到後續才被翻出來，回頭推翻了已經定稿的
方案建議。

**How to apply**：問題只要涉及「使用者有什麼」（工具、帳號、repo、流程、硬體）→ 先
掃過兩層記憶庫的 index 再決定要不要問；掃到相關條目就直接引用並向使用者確認是否
仍有效，而不是當作未知重新問一次。

## 客製延伸點

各 agent 在引用本 skill 後，可在自己的 prompt 內補充客製差異：

- **🩵 Tomori（Planner）**：若有相關 `project` 或 `user` entry，在 plan 開頭新增 `## Honoured memory` 段，把使用者偏好 / 慣例如何影響步驟安排寫出來——讓 fresh-context 的 🎀 Anon 透過讀 plan 就能間接拿到記憶，不必自己讀 MEMORY。詳見 `agents/Tomori.md`。
- **🟡 Soyo（Reviewer）**：對 `type: project` 的 entry 額外蒐集 `triggers` 欄位，把觸發的 skill 加進 review checklist。詳見 `agents/Soyo.md`。
- 其他 agent 若有額外需求，可在自己的 prompt 內說明，不修改本 skill。
