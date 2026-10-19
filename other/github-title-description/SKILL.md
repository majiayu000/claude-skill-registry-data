---
name: github-title-description
description: This skill should be used when drafting or rewriting a GitHub PR title and/or description. It produces a user-impact title (not conventional-commits formatted) and a Why / What / Test Plan body with optional Breaking changes / Related issues sections. Use both for fresh drafts from branch commits/diff (e.g., /maigo:describe-pr flow) and for ad-hoc rewrites of an existing PR body without re-fetching git context.
---

<!-- mkdocs-include-start -->

# GitHub Title & Description

**Owner Agent**: Tomori（`/maigo:describe-pr` step 2——orchestrator 前置抓料後交給燈套用）
**Consumers**: [`/maigo:describe-pr`](https://github.com/Lee-W/maigo/blob/main/commands/describe-pr.md)

## Why this skill exists

PR title / description 是 reviewer 對這次變更的第一印象。常見的失敗：
- title 抄最後一個 commit message（內部視角，reviewer 看不出價值）
- description 只寫「改了 X / Y / Z」（檔案清單 reviewer 自己看 diff 就有）
- 沒講為什麼（reviewer 得逆向工程動機）
- 沒講怎麼驗證（reviewer 得自己想 test scope）

這個 skill 把這四件事變成有結構的 process。

## Inputs（caller 必須給 / 自己抓的東西）

1. **Base branch**（通常 `main`；caller 可覆寫）
2. **Branch commits**：`git log <base>..HEAD --pretty=format:'%h %s%n%b' --no-merges`
3. **Branch diff stat**：`git diff <base>...HEAD --stat`
4. **Branch diff**：`git diff <base>...HEAD`（必要時 truncate）——**描述淨交付，不是過程**：
   若 branch 曾經試過一個設計、後來整段 revert（例如先加了某組 flag + UI，後來為了 auto-detect
   拆掉），diff 已經反映拆掉後的淨狀態，草稿只描述這個最終形狀，**不提被拆掉的中途嘗試**——squash
   merge 會把整段歷史壓平，reviewer 只在乎最終長什麼樣。用 `git diff <base>...HEAD`（或明確要求
   working tree 版本 `git diff <base>`，含未 commit 的收尾）取料，不要餵 commit log 的話題給草稿——
   commit log 會帶出被拆掉的中途嘗試痕跡。
5. **Repo commit-style 偵測**（決定要不要參考既有 commit message 風格）：
   偵測規則依 [`skills/commit-message`](https://github.com/Lee-W/maigo/blob/main/skills/commit-message/SKILL.md)
   Inputs 第 3 條（`[tool.commitizen]` / `.cz.*` / commitlint 設定檔 → Conventional Commits；repo
   有明文禁用 CC 的慣例 → 跟 repo 走自由格式；皆無訊號 → 預設 Conventional Commits）。
   **這只影響 commit message 風格參考；PR title 本身永不套 `type:` prefix。**
6. **PR template（若存在）**：caller 在 `.github/PULL_REQUEST_TEMPLATE.md`（含大小寫變體與 `.github/PULL_REQUEST_TEMPLATE/` 目錄）找到的 template 內容。
   - 找到 → 以 template 結構作為描述框架，填入從 commits / diff 萃取的內容；`## Why` / `## What` 標題照樣保留（見「若 repo 有 PR template」）
   - 找不到 → 用本 skill 預設結構

## Title 規則（user-impact 句子）

- **一句話、user 視角**：寫「使用者 / reviewer 看完會知道這 PR 做了什麼」
- **開頭大寫**（英文）；中文無此限
- **不加 conventional-commits prefix**（不要 `feat: `、`fix: `）
- **長度建議 ≤ 72 字**（GitHub UI 一行不截斷）
- **不寫檔名**：「Refactor `auth.py`」← bad；「Reject empty emails before hashing」← good
- **動詞開頭** 比名詞開頭更直接（「Add X」、「Fix Y」、「Allow Z」）

**字級措辭**（em-dash 取代 `, so`、句首 `Also` 不加逗號、避免抽象名詞改用可量化說法）跟
[`skills/github-reply-draft`](https://github.com/Lee-W/maigo/blob/main/skills/github-reply-draft/SKILL.md)
的 Convention 1 共用，見該處的「Word-level conventions」，這裡不重複寫。

### Bad → Good 對照

| Bad | Good |
|-----|------|
| `feat: add email validator` | `Reject empty emails at signup` |
| `update auth.py and tests` | `Block login when MFA token expired` |
| `WIP fix` | `Stop retry storm on 5xx from upstream` |

## Description 結構

**必填三段**（順序固定：Why → What → Test Plan）：

```markdown
## Why
<為什麼要做：bug repro / 痛點 / 觸發場景。可以引用 issue / 對話 / log。1–3 句。>

## What
<2–4 句或 bullets：這個 PR 改了什麼行為。reviewer 讀完就知道要看什麼。>

## Test Plan
- <怎麼驗證：跑了哪些 test / 手動測了什麼 / 看了哪個 metric>
- <command + 預期結果>
```

**每段的長度紀律**：

- `## Why` ≤ 2 句。
- `## What` ≤ 1 段 + 1 個 code example（僅限 core API 改動這種需要秀 signature/呼叫方式的情況）——不要寫成逐檔案條列。
- `## Test Plan` 維持條列、一行一個 bullet，描述測到什麼，**不要**貼 test 檔內容進去。

### Description anti-patterns

| Anti-pattern | 問題 |
|---|---|
| 版本演進敘事（「v1 是這樣做，後來因為 Z 改成 Y」） | 這種討論屬於 PR review thread，不屬於 description |
| `## What` 逐檔案條列（「改了 a.py / 改了 b.py / 改了 c.py」） | reviewer 自己看 diff 就有檔案清單；description 該講行為改變，不是檔案清單 |
| `## Test Plan` 貼整段 test 檔內容 | reviewer 要的是「測了什麼」的摘要，不是原始碼；貼檔案內容讓 test plan 難掃 |

**可選段（有才加，不要為了塞而塞）**：

```markdown
## Breaking changes
<API / config / behaviour 改了什麼會打破既有 caller。沒有就不加這段。>

## Related issues
- Closes #<n>
- Refs #<n>
```

**`Closes:` vs `Refs:` 判斷——colocated TODO 不代表這是誰的改動**：一個緊貼著
某段程式碼異味（code smell）的 `TODO: AIP-XX ... See #N` 註解，**不代表**修那個
異味屬於 AIP-XX 這個 feature 的 scope。要分清楚「誰引入」跟「誰只是標註」——
一個 feature commit 若剛好落在異味旁邊，可能只是**標註**了早就存在的問題，不是
它引入的。判斷方式：`git log -S"<name-or-string>"` 找出真正引入異味的 commit，
`git show <introducing-commit>^:<file>` 確認異味在該 commit 之前就存在；再用
`gh issue view N` 看連結 issue 的 title/labels 是 feature item 還是單純的
`kind:bug`/`kind:meta`。異味早於 feature、issue 也不是 feature item 時，
用 `Refs:`（issue 範圍比這次改動大），不要用 `Closes:`——把長期存在的清理工作
歸給恰好標註它的 feature 會誇大這個 PR 的 scope，也會誤導 reviewer 理解這個 PR
在做什麼。

跟同屬「斷言資料歷史前先查 git」家族的
[`skills/harness-discipline/references/evidence-discipline.md`](https://github.com/Lee-W/maigo/blob/main/skills/harness-discipline/references/evidence-discipline.md)
第 1 節同精神——那條講「別把推測寫成事實」，這條是它在 `closes:`/`related:`
判斷上的具體應用。

**若 repo 有 PR template**（Inputs 第 6 條）：
- 以 template 的 section 結構作為描述框架
- 用 commits / diff 萃取的內容填入對應 section
- template 內原有的 checklist / 說明文字保留在適當位置（template 開頭的 HTML 註解可省）
- 不要增加 template 沒有的 section；不要刪掉 template 要求的 section
- **Why / What 必須保留，且必須帶 `## Why` / `## What` 標題**：即使 template 沒有這兩個 section，也要把它們加在 template 開頭的自由描述區（通常在第一條 `---` 分隔線之前），不能寫成無標題散文。Why/What 是 reviewer 理解改動的最低資訊，不能因 template 不含它們就省略。這是上一條「不要增加 template 沒有的 section」的明確例外；`## Test Plan` 同樣加在那一區（template 已有等價的測試說明 section 時，用 template 的）。

## 怎麼從 commits / diff 萃取這四段

| 段落 | 訊號來源 |
|------|---------|
| Why | commit body 裡的「why」段、PR 描述對話、issue link |
| What | branch commits 的主旨合併 + diff 摘要的 net effect |
| Test Plan | diff 裡新增 / 改動的 test 檔 + 推測的手動驗證 |
| Breaking changes | public API signature 改變、config key 改名、預設值翻轉 |
| Related issues | commit message 裡的 `#<n>` / `Closes #<n>` / `Refs #<n>` |

**找不到 signal 不要編造**——標記 `<待補：...>` 留給使用者填，不要 hallucinate。

## Output format

skill 跑完直接給 caller 兩塊 markdown：

```markdown
## Suggested PR title

<one line, user-impact>

## Suggested PR description

## Why
...

## What
...

## Test Plan
- ...

## Breaking changes  <!-- 若無，整段刪 -->
...

## Related issues  <!-- 若無，整段刪 -->
- Closes #...
```

### Copy-paste 版本（caller 收尾用）

上面兩塊是 skill 回給 caller 的**結構化**輸出。caller（`/maigo:describe-pr` orchestrator）
在印給使用者時，**額外**再附一份「可整段複製」的 description：

- 把 `## Suggested PR description` 底下的 body 原封放進**單一** fenced code block。
- 外層 fence 用**四個 backtick**，避免 Test Plan 等內部三-backtick code block 把它截斷。
- 緊接著用 `**Title:** <one line>` 給 title，方便一起複製。
- 純淨版：不夾旁白、不夾額外提示；`<待補：...>` 佔位符保留讓使用者替換。

**不是每個 `<待補>` 都屬於 fence 裡面**。分兩種：

- **Content placeholder**——使用者填完會留在 body 裡，變成正式內容
  （例：`<待補: closes #NNNNN>`）→ 留在可複製的 fenced block 裡。
- **Advisory placeholder**——caller 在提醒使用者一個要自己判斷的決定，
  使用者不管怎麼決定，那句話本身都不會變成 body 文字
  （例：「這個 PR 要不要加 newsfragment？黃金原則是只有 user-facing 才需要，
  這裡不確定」）→ 移到 fence **外面**，跟 copy-paste block 並列的獨立提醒清單，
  不要放進 fence 裡。

判斷方式：「使用者填完之後，這句話會不會以某種形式留在 body 裡？」
會 → 留在 body。不會（純粹是提醒 / 決策點）→ 移到 fence 外。

案例：某次 airflow `FixedKeyMapper` crash fix 的 describe-pr 草稿，把
`<待補: newsfragment?>` 加上兩行說明直接寫進 PR body——因為 copy-paste block
會被原封複製貼到 GitHub，那兩行說明會變成 PR 描述裡的 literal 雜訊。

（skill 本身只負責產 body / title；組裝 copy-paste block 是 caller 的收尾步驟。）

caller 呈現最終 deliverable 給使用者時，遵守 [`skills/copyable-deliverable`](https://github.com/Lee-W/maigo/blob/main/skills/copyable-deliverable/SKILL.md)——把可複製的內容放進單一 fenced code block。

## Verification discipline (references)

**Verify every PR-state / API-signature / CLI-flag claim against live source before writing** —
reference docs go stale silently; use `gh pr view`, `git show HEAD:<path>`, or
`gh pr diff <n>` to confirm. Details and a per-claim-type recipe in
`references/verification-discipline.md`.

## Tracking issue body: short prose, not a template

When drafting a tracking / follow-up issue body (e.g. for deferred work
surfaced by the current PR), default to a **short prose block** — problem +
proposal + a related PR/comment link — not a 5-section markdown template
(`### Context` / `### Proposal` / `### Out of scope` / `### Acceptance` /
`### Related`). Target ≤3 sentences of prose plus the related link. Add
explicit `### Acceptance` or similar headers only when the user asks for them
or the issue genuinely needs pinned acceptance criteria (e.g. a feature
request being scoped for a milestone).

## No AI attribution

PR body 不加任何 AI / Claude 署名——不寫「🤖 Generated with Claude Code」之類字句，即使 host 工具 / 平台預設會塞。與 [`skills/commit-message`](https://github.com/Lee-W/maigo/blob/main/skills/commit-message/SKILL.md) 的 Trailers 段同精神（commit 不加 `Co-Authored-By`）：產出對外保持中性、不留 AI 痕跡。

## What this skill does NOT cover

- 開 PR（這是 caller / 使用者 的 `gh pr create` 或 GitHub UI）
- 寫 commit message（skill 只看既有 commits）
- 改 commit history（rebase / squash 不是這裡的事）
- 跑 test（test plan 是「描述要跑什麼」，不是跑它）
