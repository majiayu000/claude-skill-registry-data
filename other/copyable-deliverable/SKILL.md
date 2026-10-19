---
name: copyable-deliverable
description: This skill should be used whenever a maigo command produces a deliverable destined to be pasted elsewhere (a PR/issue comment, a reply draft, a commit message, a gh command draft). It mandates wrapping that content in a single fenced code block so the user gets raw, one-click-copyable markdown instead of a rendered-only version, and keeps the content itself paste-friendly (no markdown tables, no hard-wrapped prose).
---

<!-- mkdocs-include-start -->

# Copyable Deliverable

**Owner Agent**: orchestrator（呈現 deliverable 給使用者時）

**Consumers**:
[`/maigo:review`](https://github.com/Lee-W/maigo/blob/main/commands/review.md)、
[`/maigo:triage-issue`](https://github.com/Lee-W/maigo/blob/main/commands/triage-issue.md)、
[`/maigo:describe-pr`](https://github.com/Lee-W/maigo/blob/main/commands/describe-pr.md)、
[`/maigo:address-comments`](https://github.com/Lee-W/maigo/blob/main/commands/address-comments.md)、
[`skills/github-title-description`](https://github.com/Lee-W/maigo/blob/main/skills/github-title-description/SKILL.md)、
[`skills/commit-message`](https://github.com/Lee-W/maigo/blob/main/skills/commit-message/SKILL.md)

## When to apply

**Deliverable** = 使用者會拿去貼到別處的內容：PR comment / issue reply 草稿、
commit message 草稿、`gh` 指令草稿、PR title / description。

**不適用**：純對話 / 分析 / 背景說明、review verdict 的 judgement 段落
（checklist / evidence）、純狀態 / queue 表——除非使用者明確要求弄成可複製。

## The rule

**Deliverable 一律放進單一 fenced code block，內含 raw markdown。**

- 外層 fence 用**四個 backtick**（```` ```` ````）——deliverable 內部若有三-backtick
  code block（例：Test Plan 的指令）才不會把外層截斷。
- 整份 deliverable 在同一個 block 裡，不要拆成多塊。
- block 外可以有說明文字（「可整段複製貼到 GitHub：」），但 deliverable 本身要在 block 內。

範例：

`````markdown
可整段複製貼到 GitHub PR comment：

````markdown
幾個問題想確認：

1. `auth.py:42` 的 early return 在 `token == None` 時會跳過 audit log，是預期行為嗎？

整體設計方向 OK，等回覆再 approve。
````
`````

## 一次交付的多筆 deliverable 放同一則回覆

一組 deliverable 若屬於**同一次**交付（例：11 則 PR comment 回覆草稿 ＋ 一份 PR description），
全部放在**同一則回覆**裡，不要跨訊息拆。使用者是逐筆貼出去的——散在多則訊息等於把翻找成本轉嫁給他。
那是一次交付，不是十二次。

後續任何一筆過期（例如又落地一支 commit，讓 PR description 與 diff 脫鉤）→ **整份重發**，
不要只補變動的那一筆。使用者手上沒有「最新的那份在哪」的索引，只補差異會逼他自己拼。

deliverable 數量多時，每筆前面給一行標題與來源連結（哪條 comment / 哪個檔），
讓使用者能對照著逐筆處理；標題與連結放在 fenced block **外面**，block 內只留純內文。

## 多區塊交付物預設寫成檔案，不要印在對話裡

判準是**用途**，不是長度：一份輸出若目的是被複製到別處（GitHub thread、PR body、
email、另一個 repo），且含多個區塊（多則回覆草稿、報告、對照表），**預設寫成一個
檔案**，對話裡只留結論、路徑、以及它包含哪幾節。終端 scrollback 的多段 fenced block
要逐段選取複製，長段落還會被換行破壞；對話一旦被壓縮，只印在對話裡的內容就沒了，
檔案不會。

一次看完就算數的（結論、verdict、一段建議）→ 直接講，不要為了寫檔而寫檔。

落檔位置照 target repo 的成文慣例：

- 一般外部 repo（例如 apache/airflow）：走該 repo 自己的 output convention（例：
  `files/`，已 gitignore）。
- **maigo 流程自己的草稿**（`/maigo:review` 等命令產生、要貼到 GitHub 的 review
  草稿等）：放 `.maigo/`，命名比照同一次任務的產物（例：
  [`commands/review.md`](https://github.com/Lee-W/maigo/blob/main/commands/review.md)
  §4.5 的 `.maigo/review/<id>/draft.md`），不要落到目標 repo 自己的 output
  convention——maigo 的產物本來就集中在 `.maigo/`（review、rubric、board、`i/`
  細節檔），同時把新產物的路徑記到 board 細節檔（`.maigo/i/<n>.md`）的 `## 筆記`。
- 沒有成文慣例的情境用 scratchpad。

對話裡給：檔案路徑、它包含哪幾節、以及**最該先看的那一節是哪一節**。

## Why

平台 render markdown 後，使用者從 UI 框選複製到的是 rendered 結果，不是 raw 語法——
手動框選費工又容易在內部 code block 處截斷。**一個 fenced block = 一鍵複製 = 零選取誤差。**

## Prose 不 hard-wrap

Deliverable 內的 prose 段落**一行連續到底，不手動斷行**——表格列、list item、
fenced code block 內容不受影響（本來就一行一項 / 逐字保留）。

理由同上：hard-wrap 的段落，使用者每次改字都要重排、diff 也雜；一段一行才好
複製、好編輯、diff 乾淨。

## 不用表格，改成條列

Deliverable 內**不要用 markdown 表格**——欄位式的內容改寫成條列，一項一行
（`- **<欄位>**：<值>`），或拆成小節。

理由：deliverable 的宿命是被貼走、被改。表格在純文字編輯器裡欄寬對不齊，補一個
欄位要重排整列，改一個字 diff 就整列全變；條列改一項只動一行。而且貼上的目的地
不一定 render markdown——commit message、終端機、純文字 issue tracker 收到的就是
一堆 `|`。

**唯一例外**：deliverable 要逐字引用的既有內容本來就是表格（例如貼一段原文的比較
表），照原樣保留，不要為了本規則改寫別人的文字。

適用範圍同上面的 When to apply——對話裡的狀態表、review checklist、queue 表不受
影響，那些本來就不是 deliverable。

## What this skill does NOT cover

- 純對話 / 分析 / 狀態表——那是 orchestrator 的敘述，不是 deliverable
- 自動化路徑——`commit-message` 的 output 若直接 pipe 進 `git commit -F -`，不加外層 fence
  （fence 會破壞 pipe）；**呈現給使用者過目**時才適用本 skill。這個 pipe vs 呈現的區分已在
  [`commit-message`](https://github.com/Lee-W/maigo/blob/main/skills/commit-message/SKILL.md) 內部說明。
