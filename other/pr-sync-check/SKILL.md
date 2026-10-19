---
name: pr-sync-check
description: This skill should be used after a change is complete — at the wrap-up of /maigo:quick, /maigo:go, /maigo:team, or /maigo:address-comments — when the current branch may already have an open GitHub PR, to check whether the PR's title/description still accurately reflects the actual diff and draft an update if it has drifted. It never runs `gh pr edit` on the user's behalf.
---

<!-- mkdocs-include-start -->

# PR Sync Check

**Owner Agent**: — (orchestrator 直跑)
**Consumers**: [`/maigo:quick`](https://github.com/Lee-W/maigo/blob/main/commands/quick.md) 收尾、[`skills/teammate-flow`](https://github.com/Lee-W/maigo/blob/main/skills/teammate-flow/SKILL.md)（`/maigo:go` / `/maigo:team` 的「Commit message draft」段）、[`/maigo:address-comments`](https://github.com/Lee-W/maigo/blob/main/commands/address-comments.md) 步驟 6 Finale。

## Why this skill exists

改動收尾時，現有流程落地 commit（訊息依 [`skills/commit-message`](https://github.com/Lee-W/maigo/blob/main/skills/commit-message/SKILL.md)），完全沒有回頭核對「這個 branch 如果已經開著一個 PR，它的 title/description 是否還符合現在的實際改動」。PR 的 title/description 常在多輪 review、追加 commit 之後跟原始描述脫鉤——reviewer 讀到的第一印象已經過期，但沒有任何收尾步驟會發現這件事。這個 skill 補上那個核對步驟，需要時草擬更新，但**絕不代跑 `gh pr edit`**——編輯既有 PR description 是使用者自己的動作，不是「開 PR」那個授權範圍的延伸（見下方「絕不自動編輯」）。

## 何時套用

改動完成、收尾階段，且當前 branch **可能**已經對應一個開啟中的 PR 時。三個既有收尾點套用：

- `/maigo:quick` 步驟 4（顯式驗證 passed、commit message 草擬前後皆可）
- `/maigo:go` / `/maigo:team`（經 [`skills/teammate-flow`](https://github.com/Lee-W/maigo/blob/main/skills/teammate-flow/SKILL.md)「Commit message draft」段，Taki 全綠後）
- `/maigo:address-comments` 步驟 6 Finale（這裡已知 PR 存在——步驟 1 的 pre-flight gate 已經核過，可以省略步驟 1）

沒有對應 PR 就直接跳過整個 skill，**不算失敗**——大部分 quick-fix / go / team 任務跑在還沒開 PR 的 branch 上，這是常態不是例外。

## 步驟

### 1. 判斷當前 branch 是否有對應的開啟中 PR

沿用 [`/maigo:address-comments`](https://github.com/Lee-W/maigo/blob/main/commands/address-comments.md) pre-flight gate 的既有慣例：

```bash
gh pr view --json number,title,body,url,state,headRefName,baseRefName,isDraft
```

`gh pr view` 不帶位置參數時會自動解析當前 branch 的 PR；exit 非 0 或回「no pull requests found」→ 視為沒有對應 PR，**跳過整個 skill，不印錯誤、不算失敗**。

`state` 是 `MERGED` / `CLOSED` → 同樣跳過（PR 已經結案，不需要核對描述）。

### 2. 對照現有 title/body 與目前的實際改動

抓目前 branch 相對 PR base 的實際改動（`baseRefName` 用步驟 1 抓到的值，不要假設是 `main`）：

```bash
git log <baseRefName>..HEAD --pretty=format:'%h %s%n%b' --no-merges
git diff <baseRefName>...HEAD --stat
git diff <baseRefName>...HEAD
```

把步驟 1 的 `title` / `body` 拿來跟這份實際改動對照，判斷是否仍準確反映現狀。常見的脫鉤形狀：

- description 講「還沒做完 / draft」，但實際 diff 已經是完整實作
- description 提到的檔案 / 範圍已經被拆掉、改名，或整段 revert
- title 只反映最早一版的改動，後續 review 追加的行為完全沒提到
- description 的 Breaking changes / Test Plan 段落跟目前 diff 對不上

**兩類漂移，逐句判斷是哪一類**：(1) 沒涵蓋新改動＝漏寫，讀者少知道一件事；(2) 描述的行為已不
存在＝**敘述錯誤**，讀者被主動誤導。第 2 類是多輪 review 的 PR 特有的——review 常常就是在改
行為，而 body 寫的是第一版行為。只問「新改動有沒有寫進去」只抓得到第 1 類。

做法：每輪把行為改掉之後，拿反面描述詞（`ignored` / `inert` / `no-op` / `never enforces` /
`silently` / `defaults to`）回掃 body，逐句判斷「這句現在還成立嗎」。案例：某 PR body 留著
「a group's own `timeout` is inert too」，而行為已改成 `__init__` 直接丟 `ValueError`
（apache/airflow #72786）——這句在多輪之前是對的，多輪之後變成敘述錯誤。

### 3. 不符 → 套 `github-title-description` 邏輯草擬新版，交給使用者

依 [`skills/github-title-description`](https://github.com/Lee-W/maigo/blob/main/skills/github-title-description/SKILL.md) 的 Title 規則與 Description 結構，用步驟 2 抓到的 commits/diff 重新草擬 title + description。呈現方式依
[`skills/copyable-deliverable`](https://github.com/Lee-W/maigo/blob/main/skills/copyable-deliverable/SKILL.md)：完整的新 title + description 放進**單一** fenced code block（四個 backtick 外層，避免內部三-backtick code block 把它截斷），讓使用者可以直接複製貼到 GitHub 的 PR edit 頁面。

**絕不自動編輯**：不執行 `gh pr edit`，不論之前的動作有沒有被授權過開 PR。「開 PR」跟「編輯既有 PR 的 description」不是同一個授權——依
`skills/git-workflow/references/outward-ops-authority.md`「Creating a PR and editing an existing one's description are not the same authorization」那條規則，這裡只交出草稿，由使用者自己貼上。

### 4. 相符 → 一句話帶過

現有 title/body 仍準確反映現狀時，不用特別聲張——簡短一句「PR #`<number>` title/description 仍符合現狀」即可，不需要展開對照細節。

**但「相符」這個結論的證據門檻不能低**：下結論前必須已讀完 body **全文**，並逐句對照步驟 2 抓到的整條
branch 改動（`git diff <baseRefName>...HEAD`，不是只看本輪新增的 commit）。對 body 或 diff 跑關鍵字
grep、「沒搜到某個詞」都不構成相符的證據——它只證明已知的脫鉤形狀不存在，抓不到漏寫的新行為，也抓不到
沒被想到的敘述錯誤；步驟 2 的反面描述詞回掃只是輔助找出敘述錯誤，不能代替逐句對照。
（實例：某 address-comments 收尾只 grep 了幾個關鍵字就回報「描述不需要更新」，使用者追問後才完整讀全文
對照 branch diff；結論剛好相同，但第一次下結論時證據並不成立。）

## What this skill does NOT cover

- 開 PR 本身（`gh pr create`）——那是 [`skills/github-title-description`](https://github.com/Lee-W/maigo/blob/main/skills/github-title-description/SKILL.md) 的 Inputs 前提，不是本 skill 的事。
- 回覆 PR review comment——見 [`skills/github-reply-draft`](https://github.com/Lee-W/maigo/blob/main/skills/github-reply-draft/SKILL.md)。
- 真的執行 `gh pr edit`——本 skill 只產草稿，交給使用者自己貼。
