---
name: work-board
description: This skill should be used when reading, writing, or migrating `.maigo/board.md` — the single cross-session Work Board that tracks issues to triage, your own PRs, and PRs you're reviewing, ranked into a single priority ladder (🎯 下一件 / ⏳ 等別人 / ✅ 最近結案). Covers the line grammar, possession-判定 tables per item type, the upsert contract each writing command follows, the review-board.md migration path, and the checkbox → `--learn` memory gate.
---

<!-- mkdocs-include-start -->

# Work Board

**Owner Agent**: orchestrator（直跑，不 delegate 五人）
**Consumers**: [`/maigo:board`](https://github.com/Lee-W/maigo/blob/main/commands/board.md)（讀寫全套）、
[`/maigo:review`](https://github.com/Lee-W/maigo/blob/main/commands/review.md)、
[`/maigo:triage-issue`](https://github.com/Lee-W/maigo/blob/main/commands/triage-issue.md)、
[`/maigo:take-issue`](https://github.com/Lee-W/maigo/blob/main/commands/take-issue.md)、
[`/maigo:address-comments`](https://github.com/Lee-W/maigo/blob/main/commands/address-comments.md)、
[`/maigo:describe-pr`](https://github.com/Lee-W/maigo/blob/main/commands/describe-pr.md)（各自的收尾回寫段）

`.maigo/` 全貌型錄（board 在其中的定位、其餘產物種類）見
[`docs/reference/artifacts.md`](https://github.com/Lee-W/maigo/blob/main/docs/reference/artifacts.md)。

**`~/.config/maigo/board-index.md` 是什麼**：跨 repo 唯讀索引，由
`scripts/board_index.py`（`/maigo:board --cross-repo` 觸發）產生——回答「這台
機器裝了 maigo 的所有 repo，現在該我動哪些」這句話，**不是另一份 `board.md`
正典**。每次重新產生、沒有手寫區、沒有 upsert 語意；只逐字複製各 repo
`board.md` 的 `## 🎯 下一件` 整段，不重新解析或合併排序。跟本節下面講的
`board.md` 單一 repo 內的行文法、upsert 合約是完全不同的東西。

## Why this skill exists

`/maigo:review` 的 `.maigo/review-board.md` 只涵蓋「reviewer 視角」。實際工作面是三種混在一起的球：
**要 triage / 接的 issue**、**自己開的 PR**、**在審別人的 PR**。Work Board 把它們併成一份，
核心機制沿用 review board 最有價值的部分：board 的存在意義不是收藏分類，
而是回答「**現在該我動哪些**」。

## 1. `.maigo/board.md` 格式規格

### Sections（固定順序，三個 section 即 treesitter fold 邊界）

```markdown
# Work Board — Lee-W/maigo
> 最後刷新：2026-08-18 14:30 ｜ 🎯 3 ｜ ⏳ 2 ｜ ✅ 1 ｜ 🧠 待學習盤點 1

## 🎯 下一件（3）

1. [ ] 🔀 CHANGES_REQUESTED @Lee-W i/9201.md — Redesign Work Board reading view
2. [x] 👀 ↩︎ 回你的球 @contributor i/9301.md — Avoid duplicate GitHub requests
3. [ ] 🐛 待 triage @reporter 💤 i/9101.md — CLI 在空設定檔時會 crash

## ⏳ 等別人（2）

- [ ] 🔀 等 review @Lee-W i/9202.md — Document plugin installation flow
- [ ] 🐛 NEEDS_INFO（已請補作業系統與完整 log） @reporter i/9103.md — Hook occasionally exits without output

## ✅ 最近結案（1）

- [x] 👀 APPROVE（merged 07-12） @contributor 🧠 i/9303.md — Add structured review verdicts
```

`i/9201.md` 對應的細節檔（相對 `.maigo/`）：

```markdown
# 🔀 CHANGES_REQUESTED — Redesign Work Board reading view

- 連結：https://github.com/Lee-W/maigo/pull/9201
- 規模：Δ+286/-74
- 下一步：`/maigo:address-comments`

## 判斷

補測試還是反駁 reviewer

## 筆記

<!-- 手寫區 -->
```

細節檔格式規格見 §1a；欄位省略規則（`作者`／`規模`／`下一步` 何時整行不寫）與 upsert
生命週期（建立/更新/回收/孤兒偵測）也在該節。

- **🎯 下一件**：Rank P0–P7，**編號清單**（`1. [ ]`），第 1 行就是下一件事。
- **⏳ 等別人**：Rank P8，checkbox 清單、無編號——球不在你手上，這區是查閱，不是待辦。
- **✅ 最近結案**：Rank P9，checkbox 清單、無編號，7 天後自動清（待盤點未完成的行——(`[x]` 或 `🔖`) 且沒有 `🧠`——不清）。
- 舊版另外兩個獨立 section（收 `gh` 抓不到的項目、收軟刪項目的那兩區）**已取消**：
  `gh` 抓不到的項目改判 `抓不到`（P0），併進 🎯 最上面；`--drop` 改成把該行移進 ✅ 最近結案、狀態詞
  `已放棄`，跟其他結案行共用同一條 7 天老化規則，同時寫入排除紀錄（§3a），之後刷新不再補回。

### 行文法

**設計原則：索引直接回答「哪顆 PR、誰貢獻、現在要做什麼」。**
狀態詞後保留 `@貢獻者`，裸細節檔路徑供 `gf`，完整 title 放最後、不截斷。
不再為 60 欄限制隱藏貢獻者；URL、規模、完整下一步與判斷句仍放細節檔。
`board_state.py` 回傳 `index_entry` 是可重用的行內容；orchestrator 加原 checkbox、badges
與編號，既有缺作者的行在刷新取得 GitHub author 後補上，不臆造作者。
完整刷新的行與整檔由 `scripts/board_refresh.py` 的 `render_line` / `render_board` 渲染——這兩個函式是
本節文法的程式鏡像，由 `tests/test_board_refresh.py` 的 round-trip 測試守著；改文法時兩邊一起改。

```text
🎯 區：<n>. [ ] <型別emoji> <狀態詞>[（旁註）][ @<contributor>][ <badges>] <細節檔路徑> — <title>
⏳/✅ 區：- [ ] <型別emoji> <狀態詞>[（旁註）][ @<contributor>][ <badges>] <細節檔路徑> — <title>
```

- **一行一項、絕不換行**：`/` 搜尋與 `dd` 刪除都以行為單位；換行會讓兩者都失準。
- **型別 emoji**：🐛 issue ｜ 🔀 你的 PR ｜ 👀 在審的 PR
- **編號 ＋ checkbox 混排（僅 🎯 區）**：`1. [ ]`。使用者選定編號清單，checkbox 是學習閘門
  的唯一訊號（§5），兩者都要留；⏳/✅ 區是查閱不是待辦，維持無編號的 `- [ ]`。
- **旁註**（沿用 review board 慣例，optional）：branch 名、closed 理由、linked PR、DRAFT、
  他人 review decision 這類「per-item 事實」寫在狀態詞後面的括弧裡
  （例：`IN_PROGRESS（分支 fix/xxx）`）——旁註記事實，判斷句記決定，兩者不是同一件事；
  判斷句本身已搬進細節檔（§1a）。`（gh 失敗：…）` 開頭的旁註是 `refresh` 專用的抓料錯誤標記，恢復時
  會被清掉；手寫旁註請勿用這個開頭。
- **貢獻者**：從 GitHub `author.login` 取得，包含自己的 PR；放狀態詞／旁註後、badges 前。
  舊行沒有作者仍可讀；下次刷新補回。
- **badges**（`🧠`/`💤`/`🔖`，optional）：緊接在貢獻者（缺值時為旁註）之後、細節檔路徑之前，用一個空格分隔；
  §2 vocabulary 表下方有各自的觸發規則。
- **細節檔路徑（必填、裸相對路徑、不加反引號）**：相對 `.maigo/`，由
  [`detail_path()`](https://github.com/Lee-W/maigo/blob/main/scripts/board_state.py)
  算出——同 repo 是 `i/<n>.md`，跨 repo 是 `i/<repo>-<n>.md`。**不加反引號**：反引號會擋住
  nvim `gf`；游標停在路徑上 `gf` 直接開對應細節檔（格式見 §1a、操作見 §6）。
- **`— <title>` 的 `—` 分隔符是強制的，parser 不會用啟發式猜**：title 前面那個 `—`
  一定要打；title **不再加引號**（title 已是行尾最後一欄，引號在舊文法是為了跟後續欄位
  切開，現在只是純雜訊）。漏打分隔符一律回報格式壞掉，寫回命令**大聲失敗**，不靜默留空
  ——比照未知狀態詞。
- **checkbox**：👀 行的 `[x]` ＝「我看完目前這份報告了」——使用者在 nvim 勾上，下次刷新會 ack 該
  report；有新 commit／作者留言（回你的球）或待 review 時**自動取消勾**。🐛/🔀 行的 `[x]` ＝「這項我
  **親自**處理過了」，純學習閘門訊號（見 §5），不 ack、不自動取消勾；與所在 section 正交。
- **🧠 標記**：學習盤點已完成，不重複學。
- **🔖 標記**：待學習盤點——👀 行被勾（含 `--reviewed`）時加上，跨刷新保留，所以後來自動取消勾也
  不會吃掉學習訊號；`--learn` 完成後換成 `🧠`。
- **💤 標記**：`updatedAt` 逾期未更新（stale badge，見 §2 vocabulary 表下方說明），跟
  `🧠` 一樣是正交於狀態詞的 badge，不影響 rank / section。
- **跨 repo**：board 綁 cwd repo（header 記 `gh repo view --json nameWithOwner` 結果）；
  丟進來的 URL 若屬其他 repo，細節檔路徑改用 `i/<repo>-<n>.md` 形式（見上），真 URL
  完整記在該項的細節檔 `連結` 欄裡，不在索引行出現。
- **空白容錯**：旁註 `（…）` 與緊接著的 badges／細節檔路徑之間有沒有留空格，parser 都吃得下
  （nvim 手改最容易漏這格空白）。

### 1a. 細節檔格式 `.maigo/i/<slug>.md`

索引行以外的細節（URL、規模 Δ+A/-D、完整作者資訊、下一步、審查時間、判斷句、舊 `📄 <產物路徑>`）全部
收進這份細節檔：

```markdown
# <型別emoji> <狀態詞> — <title>

- 連結：<URL>
- 規模：Δ+A/-D ｜ 作者：<author>
- 下一步：`<next_action>`
- 最後 review：<ISO 8601 時間，含時區>
- 已看完：<ISO 8601 時間，含時區；尚未確認時省略>

## 判斷

<判斷句——你現在要決定什麼，不寫發生了什麼>

## 筆記

<!-- 手寫區 -->
```

**硬規則：refresh 或任何寫回只重寫 `## 判斷` 之前的事實區（標題行 ＋ metadata），
`## 判斷` 與 `## 筆記` 兩段一律原樣保留，絕不覆蓋。** 細節檔不存在時才整份新建
（判斷句寫進 `## 判斷`、`## 筆記` 留空）。這條硬規則適用於**所有**寫回路徑——`/maigo:board`
的 refresh 以及五個 delegate 命令（review / triage-issue / take-issue / describe-pr /
address-comments）各自的 upsert，沒有例外可以整份覆蓋掉細節檔清掉使用者手寫的 `## 筆記`。

**撞號限制與後果**：`detail_path()` 的 `<repo>` 只取 repo 名、不含 owner（見
[`scripts/board_state.py`](https://github.com/Lee-W/maigo/blob/main/scripts/board_state.py)
docstring），所以不同 owner 的同名 repo（例如 `Lee-W/maigo` 與另一個 owner 的
`maigo`）在跨 repo 情境會共用同一個 `i/<repo>-<n>.md`——兩項的事實區與 `## 判斷` /
`## 筆記` 會互相覆蓋。這是刻意的取捨（路徑短優先），目前**不自動處理**；真的撞號時
手動把其中一份細節檔改名（並同步索引行的細節檔路徑）即可繞開。

欄位省略規則：

- **作者**：索引行一律顯示取得的 `@login`；細節檔可重複完整 login，不寫含糊的「你」。
- **最後 review / 已看完**：使用 report 的 `reviewed_at` / `acknowledged_at`，不能用
  board 刷新時間取代。沒有 report 時寫「尚未 review」；舊檔 mtime fallback 註明「舊檔時間推估」。
- **規模**：issue 省略整行（沒有 additions/deletions 可言）。
- **下一步**：`next_action` 為 `null` 時省略整行——狀態沒有對應下一步，見
  [`scripts/board_state.py`](https://github.com/Lee-W/maigo/blob/main/scripts/board_state.py)
  的 `_STATUS_META`（`WIP` / `IN_PROGRESS` / P8 / P9 / P0 這類狀態）。
- **舊 `📄 <產物路徑>`**（`review/<n>/review.md` / triage 筆記等本地產物）：改寫進 `## 筆記`
  區裡的一行裸相對路徑連結（相對 `.maigo/`，例：`review/9301/review.md`），不佔事實區欄位。
- **資料缺失時的降級**（與上面三條「刻意省略」不同）：某欄位該有值但當下拿不到
  （例：遷移進來的 👀 項目沒有 `Δ+A/-D`，因為舊格式本來就沒記），就**只寫拿得到的部分**
  ——`- 規模：` 整行只剩作者時退化成 `- 作者：<author>`，不要填 `?` 或 `N/A` 佔位。
  下次寫回拿到真值就補回完整形狀，省略規則不會擋住它被填回去。

`## 判斷`：只寫「你現在要決定什麼」，**不寫「發生了什麼」**。

- 狀態詞本身已經講清楚下一步、或根本沒有判斷要下（例：`可合併`、`等 review`、
  `IN_PROGRESS`）→ 該段留空
- 真有岔路要選（改還是不改、修還是換路、能不能重現）→ 一句話點出岔路，愈短愈好

### 狀態詞 vocabulary（依型別，含 rank）

rank 決定排序與所在 section，10 級由緊急到不急：P0 最急，P9 只留痕。
**正典在 [`scripts/board_state.py`](https://github.com/Lee-W/maigo/blob/main/scripts/board_state.py) 的 `BoardStatus` enum ＋ `Rank` ＋ `_STATUS_META`**，
本表只是人類可讀鏡像，兩者須一致（由 `tests/test_board_state.py` 守）。

| 型別 | 狀態詞 | rank |
|---|---|---|
| 跨型別 | `抓不到`（orchestrator 指派，`classify()` 不產出） | P0 |
| 🐛 issue | `待 triage` | P6 |
| 🐛 issue | `READY` | P7 |
| 🐛 issue | `IN_PROGRESS` | P5 |
| 🐛 issue | `有新回覆` | P2 |
| 🐛 issue | `NEEDS_INFO` | P8 |
| 🐛 issue | `DUP` / `CLOSE` | P9 |
| 🔀 你的 PR | `WIP` | P5 |
| 🔀 你的 PR | `有衝突` | P1 |
| 🔀 你的 PR | `CI 紅` | P1 |
| 🔀 你的 PR | `CHANGES_REQUESTED` | P1 |
| 🔀 你的 PR | `有新 comment` | P2 |
| 🔀 你的 PR | `可合併` | P3 |
| 🔀 你的 PR | `CI 等待` | P8 |
| 🔀 你的 PR | `等 review` | P8 |
| 👀 在審的 PR | `他人草稿` | P8 |
| 👀 在審的 PR | `待 review` | P4 |
| 👀 在審的 PR | `↩︎ 回你的球` | P2 |
| 👀 在審的 PR | `待送出`（本地報告待你看／決定是否送出） | P3 |
| 👀 在審的 PR | `已看完`（本地確認，或已送出但無本地 verdict） | P8 |
| 👀 在審的 PR | `BLOCKED` / `NEEDS_CHANGES` / `APPROVE_WITH_NITS` / `APPROVE` | P8 |
| 跨型別終端 | `closed` / `merged` | P9 |
| 跨型別 | `已放棄`（`--drop` 軟刪，進 ✅ 最近結案；寫入排除紀錄、刷新不重新分類） | P9 |

triage verdict 沿用 [`strict-triage`](https://github.com/Lee-W/maigo/blob/main/skills/strict-triage/SKILL.md)、
review verdict 沿用 [`strict-review`](https://github.com/Lee-W/maigo/blob/main/skills/strict-review/SKILL.md)，不另造詞。

**badge（正交於狀態詞，不佔 rank）**：`🧠` 已完成學習盤點；`🔖` 待學習盤點；`💤` stale——`updatedAt`
逾 14 天（`scripts/board_state.py --stale-days` 可調），提示這顆球可能被遺忘，不改變 rank / section。
都寫在旁註之後、細節檔路徑之前，例：`🎯 1. [ ] 🔀 WIP 🧠💤 i/12.md — <title>`。

**不在 enum 內的狀態詞**（手改壞、或舊工具寫入的殘留字）——寫回命令刷新該行時大聲失敗，
不靜默正規化成任何看似合理的狀態，比照 `— <title>` 分隔符解析失敗的處理方式。

**向下相容**：新 vocab 是舊 vocab 的超集，沒有任何舊狀態詞被移除或改名（包含 `抓不到`／`待送出`／`已看完`）。第一次 `/maigo:board` 刷新時，`board_state.py` 的 `classify()`
會用 `prior_status` 重算每一行，未知或已停用的狀態詞視為 `None`（等同剛加入），自動
正規化成新表的對應狀態——不需要手動遷移步驟，沿用既有「刷新即正規化」的遷移慣例。
讀到舊版任何 section 標題（球權三分區時代的四個舊標題）時同樣吃得進來：取 checkbox /
`🧠` / 狀態詞後，整檔以新骨架（三個 section）重寫，不做逐行 in-place 遷移。

**但整檔重寫與 §3(a) 的「禁止整份 `Write`」會直接對撞——併發安全優先。** 舊格式遷移必然是
整檔重寫，而 board 是跨 session 共用、不帶任務識別碼、且 `.maigo/` 被 gitignore（輾掉沒有
版本可救）。所以誰能做整檔寫入是分工，不是隨手做的事：

- **整檔重寫只有 `board_sync.py refresh --apply` 會做**，由 CAS（讀檔雜湊、寫前重讀比對、不一致就
  中止，見 §3(b)）取代 `ListAgents` 確認：別人動過檔案，這次寫入就以 exit 2 中止、不寫任何檔。
  refresh 遇到舊格式（舊 section 標題）或 `review-board.md` 會直接拒絕（exit 1），不遷移。
- **舊格式正規化**仍由 Claude 的 `/maigo:board` 完整刷新做——它本來就要重算每一行，是唯一有理由
  持有整檔的 Claude 寫入者；因為 script 看不到 `🔍 本批佇列` 的重判，也看不到其他 session。
- **五個 delegate 命令的收尾 upsert**（review / triage-issue / take-issue / describe-pr /
  address-comments）遇到舊格式時，**只 `Edit` 自己那一行，並沿用該檔當下的舊行文法**，把正規化
  留給下一次 `/maigo:board`。**不要把一行新格式混進舊格式檔**——那會讓檔案同時有兩種文法，比
  整檔仍是舊格式更難解析。寫完在回覆裡告訴使用者「board 仍是舊格式，正規化留給
  `/maigo:board`」，不要靜默略過。
- Claude 做舊格式整檔重寫前先確認沒有其他 session 正在寫（`ListAgents`；同一台機器多個 worktree
  各跑一個 session 時，它們共用這一份 board）。不確定就當作有。`refresh --apply` 不需要這一步，
  CAS 會在衝突時自己中止。

實例（2026-09-19）：一次 `address-comments` 收尾對舊格式 board 只 `Edit` 了自己那一行；同一份
board 在那之後又被別的 session 加了一項、改了另一項、計數從 🎯 7 變 8——若當時照「整檔重寫」
辦，那兩筆會被安靜輾掉。

### 排序

- 🎯 區：**rank 升序 → 同 rank 內 `updatedAt` 升序**——排名先分先後，同一級內最久沒動的
  排前面（沿用舊「責任感排序」的精神，但改成明確的 `updatedAt`）。編號 `1. 2. 3.` 就是
  這個排序結果，排名本身不顯示在行內。
- ⏳ / ✅ 區：`updatedAt` 降序（這兩區是查閱，不是待辦）。
- ✅ 區超過 7 天的行在刷新時自動清掉，清掉時同時寫入排除紀錄（`reason: aged`，§3a）
  （唯一例外：待盤點未完成的行〔(`[x]` 或 `🔖`) 且沒有 `🧠`〕不清，學完才走）。
  老化基準時間（`refresh` 實作）依序取 `mergedAt` → `closedAt` →（排除項目）排除紀錄的 `last_drop_at`
  → `updatedAt`。
  `/maigo:board --drop` 的落點也是這裡（狀態詞改 `已放棄`），跟其他結案行共用同一條
  老化規則，不再有獨立的 tombstone 區。

## 2. 型別偵測與球權判定

### 型別偵測（加 item 時跑一次）

1. URL → 直接解析 owner/repo + 型別 + 編號
2. 裸編號 → `gh api repos/<owner>/<repo>/issues/<n>`，有 `pull_request` key ＝ PR
3. PR 再看 `author.login` 是否等於 `gh api user --jq .login` → 🔀 vs 👀
4. `gh` 抓不到 → 狀態詞 `抓不到`（P0，orchestrator 指派），併進 🎯 最上面，附錯誤末行

### 刷新時抓的欄位

```bash
# issue
gh issue view <n> --repo <r> --json title,state,stateReason,assignees,author,comments,createdAt,updatedAt,labels,closedByPullRequestsReferences
# PR（自己的與在審的同一組）
gh pr view <n> --repo <r> --json title,state,isDraft,mergedAt,mergeable,reviewDecision,createdAt,updatedAt,headRefOid,commits,reviews,comments,author,statusCheckRollup,additions,deletions
```

「你」＝ `gh api user --jq .login`（沿用 review board 既有做法）。
「你最後活動 vs 他人最後活動」的比對邏輯：把 comments + reviews 的 author + 時間戳整理成
`gh_meta`，交給 [`scripts/board_state.py`](https://github.com/Lee-W/maigo/blob/main/scripts/board_state.py)
的 `classify()` 純函式比較——這是這次重構後的**判定邏輯正典**，本節三張表只是它的人類可讀
鏡像，兩者不一致以程式為準（`tests/test_board_state.py` 逐條守）。

呼叫方式（薄 CLI，stdin 餵 JSON 陣列 `[{type, gh_meta, prior_status}]`）：

```bash
echo '[{"type": "🐛", "gh_meta": {"state": "OPEN"}, "prior_status": null}]' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/scripts/board_state.py" --you <login>
```

`mergeable` 欄位可能回 `CONFLICTING` / `MERGEABLE` / `UNKNOWN`（GitHub 尚在計算）；
`classify()` 只在明確 `CONFLICTING` 時判定衝突，`UNKNOWN` fallthrough 到其他規則，不誤判。

### 球權判定表（merged / closed 一律優先 → ✅；由上往下第一個命中）

**🐛 issue**：

| 條件 | 狀態 | section | rank |
|---|---|---|---|
| `state == CLOSED` | `closed`（stateReason / linked PR 併入旁註） | ✅ | P9 |
| prior 為 `DUP` / `CLOSE` | 保留該 verdict | ✅ | P9 |
| board 無 verdict（剛加入、從未 triage） | `待 triage` → `/maigo:triage-issue <n>` | 🎯 | P6 |
| prior `READY` 且無 assignee（或 assignee 是你） | `READY` → `/maigo:take-issue <n>` | 🎯 | P7 |
| 已 take（prior `IN_PROGRESS`） | `IN_PROGRESS`（旁註 branch 名） | 🎯 | P5 |
| 你最後活動後有別人新 comment | `有新回覆` → `/maigo:triage-issue <n>`（重判） | 🎯 | P2 |
| prior `NEEDS_INFO` 或你留言後無新活動 | `NEEDS_INFO` | ⏳ | P8 |

**🔀 你的 PR**（每次刷新純由 gh metadata 重算，不看 prior_status）：

| 條件 | 狀態 | section | rank |
|---|---|---|---|
| merged / closed | `merged` / `closed` | ✅ | P9 |
| `isDraft == true` | `WIP`（自己 draft＝還在寫） | 🎯 | P5 |
| `mergeable == CONFLICTING` | `有衝突` → `/maigo:address-comments` | 🎯 | P1 |
| `statusCheckRollup` 有 FAILURE | `CI 紅` → `gh pr checks <n>` | 🎯 | P1 |
| `reviewDecision == CHANGES_REQUESTED` | `CHANGES_REQUESTED` → `/maigo:address-comments` | 🎯 | P1 |
| 你最後 push/comment 後有別人 review/comment | `有新 comment` → `/maigo:address-comments` | 🎯 | P2 |
| `reviewDecision == APPROVED` 且 CI 綠 | `可合併` → `gh pr merge <n>` | 🎯 | P3 |
| `statusCheckRollup` 有 PENDING（其餘正常） | `CI 等待` | ⏳ | P8 |
| 其他（最後活動是你） | `等 review` | ⏳ | P8 |

**👀 在審的 PR**：

| 條件 | 狀態 | section | rank |
|---|---|---|---|
| merged / closed | `merged` / `closed` | ✅ | P9 |
| `isDraft == true` | `他人草稿` | ⏳ | P8 |
| report 的 head 與目前 head 不同，或最後 review／已看完／送出後有新 commit、作者留言 | `↩︎ 回你的球` → `/maigo:review <n>` | 🎯 | P2 |
| 使用者明確 `--reviewed` 本版 report，之後無新活動 | `已看完`；本地確認，不代表送出 GitHub | ⏳ | P8 |
| 有本地 report / verdict，尚未確認且沒有這輪送出的 GitHub review | `待送出`；先看 report，再決定送出或 `--reviewed` | 🎯 | P3 |
| GitHub 已送出這輪 review，且無新活動 | 本地 verdict（若有）；否則 `已看完` | ⏳ | P8 |
| 沒有本地 report 或已送出 review | `待 review` → `/maigo:review <n>` | 🎯 | P4 |

`board_state.py --maigo-root <repo-root>` 讀 report 的明確時間與 head；舊報告才退回 mtime。
`待送出` 的下一步：`.maigo/review/<id>/draft.md` 存在才給 `gh pr review --body-file` 指令，不存在時
改為「尚無草稿：先起草 …（§4.5 裁決 gate）」——否則使用者照 board 跑指令會因檔案不存在而失敗
（2026-10 batch 有 5 顆 `待送出` 指向沒起草的 draft.md）。沒給 `--maigo-root` 時無從判斷，維持給指令。
`PENDING` / `DISMISSED` 的 GitHub review 不算已送出。`--reviews` 檢視只列 `needs_review`
為 true 的項目：待 review、回你的球、待送出，依 rank 排序；**這個過濾結果不得拿去重寫
完整 board**。索引顯示標題與貢獻者；最後 review／已看完時間在細節與對話待看清單中顯示。

review verdict 詞彙沿用 [`strict-review`](https://github.com/Lee-W/maigo/blob/main/skills/strict-review/SKILL.md)；
per-PR queue 排序 / 前置處理（merged / closed / draft 自動 skip 或問使用者）另見
[`review-batch-queue.md`](https://github.com/Lee-W/maigo/blob/main/skills/strict-review/references/review-batch-queue.md)，
那份文件管的是 **per-run 排隊**，跟本表管的**跨 session 落點**是兩件事。

## 3. 各命令回寫合約

**upsert 規則**：以 `#<n>`（含 repo 全稱時用全稱）為 key；行存在→整行替換
（**保留原 checkbox 與 🧠 狀態**），不存在→append 到對應 section；board 檔不存在就先建骨架。
**整行替換時，對應細節檔（`.maigo/i/<slug>.md`）必須跟著整份重寫，不可只改索引行漏改
細節檔**——索引行與細節檔是同一次寫回的兩個產物，不允許其中一個落後。
**例外：board 還是舊格式時這條無從執行**——舊行文法把 URL / 規模 / 產物路徑都內嵌在索引行裡，
`.maigo/i/` 整個目錄不存在。此時只更新索引行，不要為單一項目憑空生一份細節檔（那會讓同一份
board 一半有細節檔一半沒有）；細節檔由 `/maigo:board` 在整檔正規化時一次建齊，見 §2 向下相容段。

**併發寫回（board 是跨 session 共用的單一檔，不帶任務識別碼，所以要靠寫法自保）**。
共同目的：別人動過就吵，不安靜覆蓋。寫入者有兩種：

**(a) Claude（五個 delegate 命令的收尾 upsert，以及 `/maigo:board` 的 fallback 手動流程）**：

1. **既有 board 一律用 `Edit`，禁止整份 `Write`。** `Edit` 的 `old_string` 就是天然的樂觀鎖：
   別的 session 動過那一行時 `Edit` 會失敗——**會吵**；`Write` 則會安靜輾過對方的寫入。
   `Write` 只保留給「board 檔不存在、要建骨架」那一次。
2. **寫入前立即重讀。** 不可拿幾輪之前讀到的內容當現況——中間可能已經有別的 session 寫過。
3. **`Edit` 失敗 → 重讀、重算那一行、再試；不要改用 `Write` 硬寫。** 失敗是訊號不是障礙。

**(b) `board_sync.py refresh --apply`（script，整檔寫回）**：以 compare-and-swap 取代 `Edit` 的樂觀鎖——
讀 board.md 時記下內容雜湊，寫入前（ack 之前與實際寫檔之前各一次）重讀比對，不一致就以 **exit 2** 中止
（每個要改／刪的細節檔同樣比對，要新建的細節檔必須仍不存在）。第一次比對在 ack 之前、什麼都沒寫；
第二次比對在 ack 之後，所以 exit 2 時**除了 review.md 的 ack 標記外**不會寫任何檔。通過後先備份到
`.maigo/_internal/board/backup/<UTC ts>/`（§3a），再用同目錄 tmp＋rename 原子寫入；寫 board／細節檔失敗
從備份還原並 exit 3；board 已寫成功後 ledger／snapshot 才失敗也是 exit 3，但此時**不還原**、board 已是
新版（重跑安全，漏寫的事件會列在輸出裡）。

已知限制：某列抓料失敗時狀態詞會變 `抓不到`，恢復時 `refresh` 從該列細節檔的 H1 取回舊狀態詞；
若同一輪你手改了索引行的狀態詞、又剛好抓料失敗，恢復後會回到細節檔 H1 的舊狀態，手改的狀態詞不會保留。exit 2 的處理方式是**直接重跑**，不要改用 `Write`。

`.maigo/i/<slug>.md` 的「整份重寫事實區、保留手寫 `## 判斷` / `## 筆記`」同樣要求
**重寫前立即重讀**（script 則是上面的 CAS），理由相同。

### 細節檔生命週期

- **建立**：項目首次進 board → 建細節檔（§1a）。
- **更新**：refresh 或任何寫回 → 重寫事實區，`## 判斷` / `## 筆記` 原樣保留（§1a 硬規則）。
- **回收**：項目離開 board（✅ 區 7 天老化清除、`--drop` 後也走同一條老化規則）→
  產物**封存而非刪除**，不留孤兒檔：orchestrator 在 `drop --reason closed|aged` 之後，對同一批
  URL 跑 `board_sync.py archive <url...>`，把 `.maigo/review/<id>/`（整個目錄）搬到
  `.maigo/_archive/review/<id>/`、`.maigo/i/<id>.md` 搬到 `.maigo/_archive/i/<id>.md`。它不查
  GitHub、不判斷 PR 狀態（哪些已結案由 orchestrator 決定，同 `drop`），目的地已存在就跳過不覆蓋，
  逐 URL 回報 moved／skipped／missing；`_internal/` 不碰。**順序不能顛倒**：只對已經 `drop` 掉、
  board 上已無索引行的項目跑 `archive`；索引行還在就先搬走 `i/<id>.md`，下次 `plan` 會讀不到細節檔，
  `review/<id>/review.md` 一消失，artifact 對帳也可能把項目當新項目補回——`archive` 本身沒有這層防呆。
  `refresh --apply` 目前仍直接刪老化的細節檔
  （刪前備份到 `_internal/board/backup/`），對它輸出的 `aged` URL 再跑 `archive`，`review/<id>/`
  照樣封存、`i/` 回 missing 屬正常。
  **為什麼**：已結案的 review 留在 `review/` 會混進「目前在審」的產物清單；直接刪又丟掉日後要翻的
  審查紀錄。封存後 `review/` 與 `i/` 只剩進行中的項目，`plan` 的孤兒偵測與 artifact 對帳也不再看到它們。
  案例：一次 40 顆 PR 的 batch 結束後手動封存了 25 個 review 目錄、10 個細節檔——使用者早已在自己的
  repo 用同一個 `_archive/` 佈局手動執行，規格卻從未寫過。
- **孤兒偵測（dd 語意）**：`/maigo:board` 刷新時比對 `.maigo/i/*.md` 與 board 索引行；沒有任何
  索引行引用的細節檔，代表使用者用 `dd` 刪了那一行——`board_sync.py plan` 把它判成 dd 並寫進排除
  紀錄（§3a）。剛寫好的細節檔有 10 分鐘寬限（delegate 命令先寫細節檔、後 `Edit` 加行，plan 若
  落在兩者之間會誤判），期間列為 `pending_orphans`、本輪不判。排除項目殘留的細節檔
  （`excluded_detail_files`）列出來給使用者確認後才刪，不自動刪。

| 命令 | 回寫時機 | 行為 |
|---|---|---|
| `/maigo:review` | 每顆 PR publish 後 | 依 report metadata + GitHub 重新 classify；待看／待送出 → 🎯，已看完／已送且無新活動 → ⏳；同步 title、貢獻者與審查時間 |
| `/maigo:triage-issue` | 每個 verdict 出爐 | `READY`→🎯（next: take）；`NEEDS_INFO`→⏳；`DUP`/`CLOSE`→✅，duplicate / close 理由放狀態旁註。board 是本地檔，不違反 triage「不主動寫 GitHub」原則 |
| `/maigo:take-issue` | 開工時＋收尾 | 開工：issue 行標 `IN_PROGRESS` ＋ branch 名；收尾若開了 PR：新增 🔀 行、issue 行旁註 linked PR |
| `/maigo:describe-pr` | PR 開出後（若使用者說已開） | 新增/更新對應 🔀 行 → ⏳ `等 review` |
| `/maigo:address-comments` | 步驟 8（全部 work item 走完） | commit 未 push（**預設**——該命令不 push、不替使用者回覆）→ 🎯 留著，細節檔 `## 判斷` 區寫「push 了嗎——還沒就先 push」；使用者已自行 push 且回覆已送出 → ⏳ `等 review`（`## 判斷` 區留空） |

maigo 命令自己處理的項目**不勾 checkbox**——checkbox 專屬「使用者親自處理」的訊號（見 §5）。
`--reviewed` 是使用者的明確操作，可以勾（等同使用者在 nvim 手勾）。

**Work Board 每個專案只有一份**，但它的位置**不是固定的**——它住在「當初建立它的那個
worktree」，不一定是主 worktree；那個 worktree 一旦被 `git worktree remove`，board 就得
搬到別的存活 worktree，記下來的舊路徑會過期（2026-09-09 實例：一份記憶條目原記 `<repo>-main`，
但 board 實際已經在一個 topic worktree 裡）。跑 board 回寫類命令（`/maigo:board`、
`address-comments` 步驟 8 等）時，**先 `find <workspace 根> -maxdepth 3 -name board.md`
找到現存的那一份再 upsert**，不要假設它在主 worktree、也不要照抄任何舊記錄的路徑；
找不到任何 `board.md` → 問使用者要建在哪，不要自己挑一個 worktree 建。

**Upsert 紀律**（單項 upsert 的日期更新、容易被漏掉的獨立檢查、verdict 未必已送出 GitHub）
三條實務守則見
[`references/upsert-discipline.md`](https://github.com/Lee-W/maigo/blob/main/skills/work-board/references/upsert-discipline.md)。

## 3a. 對帳、discovery 與排除紀錄

正典是 [`scripts/board_sync.py`](https://github.com/Lee-W/maigo/blob/main/scripts/board_sync.py)
（stdlib-only CLI：`plan` / `ack` / `drop` / `revive` / `snapshot` / `refresh`）。`plan` / `ack` / `drop` /
`revive` / `snapshot` 不寫 `board.md` 與 `i/*.md`，只輸出 JSON 變更清單，由 orchestrator 用 `Edit` 寫回
（§3(a) 規則不變）；`refresh --apply` 會整檔寫 `board.md` 與 `i/*.md`，規則見 §3(b)（CAS ＋ 備份 ＋ 原子寫入）。
`refresh` 不帶 `--apply` 是預覽：只印 unified diff，不寫任何檔、不 ack。從 shell 跑它即是零 token 刷新，
用法見 [`commands/board.md`](https://github.com/Lee-W/maigo/blob/main/commands/board.md)。

**機器狀態檔**——只有 script 寫，都在 `.maigo/_internal/board/`（script 自行建立目錄；
`plan --dry-run` 與 `refresh` 預覽不建目錄、不寫檔；型錄與 doctor 永遠不列 `_internal/`）：

| 檔案 | 格式 | 寫法 | 用途 |
|---|---|---|---|
| `dropped.jsonl` | 每行 `{"url","event":"drop"\|"revive","reason","at"}` | 單次 append 一行，只增不改 | 持久排除紀錄；以 canonical URL（`(owner, repo, number)` 小寫，`pull`/`issues` 同一項）為 key，依事件順序 fold，最後一筆決定狀態 |
| `snapshot.json` | `{"version":1,"written_at","items":{<url>:{"checked","detail"}}}` | tempfile ＋ replace 原子寫入 | 上次刷新結束時 board 上有哪些項目與勾選狀態，用來偵測 `dd` 與勾選變化 |
| `backup/<UTC ts>/` | 與 board.md 相同的目錄結構（`board.md`、`i/*.md`） | `refresh --apply` 寫回前複製要改／刪的檔，只留最新 10 份 | 寫入失敗時還原；也是誤刪細節檔後的救援來源 |

**`dd` → 排除**：`removed = (snapshot 的 URL ∪ 孤兒 i/ 檔的 URL) − board 現有行 − 已排除`，成立就
append `{"event":"drop","reason":"dd"}`。第一次跑（沒有 snapshot）時既有的孤兒 i/ 檔一律視為 `dd`，
並在輸出列出清單。排除項目：discovery 與 artifact 對帳都跳過；仍留在 board 上的排除項目（`已放棄`
的行）標 `excluded: true`，orchestrator 不重新分類。`--drop` / 老化 / 已結案的 artifact 補行也寫入
排除紀錄（`reason` 分別是 `drop` / `aged` / `closed`）。

**重新指名 → 復活**：要同時滿足 (1) URL 出現在本輪 `user-review-requested:@me` 結果；(2) timeline 有
`review_requested` 事件、`requested_reviewer.login` 是你，且 `created_at` 晚於最後一次 drop 的時間。
抓取 timeline 失敗時 fail-closed：維持排除並列進 `errors`。使用者明確把被排除的項目重新加進 board
（`/maigo:board <targets>`）時，先跑 `board_sync.py revive --reason manual <url...>`，只對目前被排除的
key 寫 `revive` 事件。`dd` 事件的時間記為 snapshot 的 `written_at`（沒有 snapshot 才用現在），所以
「刪行後、刷新前」被重新指名的 PR 仍會復活。

**fail-closed**：board.md 壞掉的行（含 `i/*.md` 路徑但解析失敗）不當成 `dd`，列進 `errors`；
snapshot 有項目但 board.md 不存在或沒有任何項目行時略過整個 `dd` 判定。

**已知限制**：ack 的 `acknowledged_at` 是刷新當下，不是勾選當下；第一次跑（沒有 snapshot）時，
已勾的 👀 行會以推斷模式補 ack。

**對帳 `.maigo/` 產物**（建在 `maigo_dir_catalog.scan()` 之上）：`review/<id>/review.md` 的 metadata
`source`（GitHub PR URL，可跨 repo）、舊扁平 `review-<id>.md` 的 `**PR:**` 行、以及純數字 id 的
`review/<n>/*` / `issue/<n>/*`（推導成 board repo 的 URL）是可靠對應，會補進 board；
`plan-*`、舊固定檔名、`unregistered` 的 `.md`、metadata `source` 不是 URL 的本地 review、
`<repo>-<n>` 形式的 id 沒有可靠對應，只列入 `unattributed`。孤兒 i/ 檔是 `dd` 訊號，不是補行來源。

**Discovery**：在 board repo 跑兩次 `gh search prs --state open`（`user-review-requested:@me`、
`--reviewed-by @me` 加 `-author:@me`），依 key 合併；bot PR 照常收；作者是你本人的項目給 `🔀` 提示。
**筆數**：`--max-new`（預設 50）限制單次新增的項目數，排序「被指名 → 審過 → artifact」，同類內
`updatedAt` 由舊到新；超過的放進 `overflow`，在對話列出、下次刷新接著補。結果數等於 `gh search` 的
`--limit 200` 時在 `errors` 註明「可能截斷」。

**`[x]` 與 ack**：snapshot 的 `checked` 與現檔比對，`[ ]→[x]` 記 `checked`、`[x]→[ ]` 記 `unchecked`；
沒有 snapshot 或該 URL 不在 snapshot 裡時退回推斷（已勾即記 `checked`，`inferred: true`，不產生
`unchecked`）。`checked` 且 report 存在、head 相符 → ack；`inferred` 而且同一 head 已被你 ack →
不重打（避免把 seen_at 推過作者的新留言）；明確的 `[ ]→[x]` 一律重打；沒有 report → `no_report`；
head 已變 → `head_changed`；`unchecked` → `acknowledge --undo`。最終 👀 checkbox ＝
`(acked_current or checked_now) and not needs_review`（`board_state.checkbox_after_refresh`）。
👀 勾了卻沒有 report 或 head 已變：取消勾、加 `🔖`，並警告先 `/maigo:review <n>`。

**學習訊號 `🔖`**：👀 行的 `checkbox_change == checked` 且行上沒有 `🧠` 時加 `🔖`（`learn_pending`），
跨刷新保留；`--learn` 處理「(`[x]` 或 `🔖`) 且沒有 `🧠`」的行，完成後加 `🧠`、拿掉 `🔖`。

## 4. 併入遷移（review-board.md 退役）

首次跑 `/maigo:board`（或某回寫命令要寫 board 時）偵測到 `.maigo/review-board.md`
存在且 `board.md` 不存在：

1. 讀舊檔，按分區映射搬行：`Active` + `↩︎ 回你的球` → 🎯；`Off-board` → ⏳；
   `Merged/closed` → ✅；`🔍 本批佇列` → 依 §2 重判
2. 解析舊行的 author / URL / 規模（`- #<PR> (<author>) …` 這個舊尾註形狀）→ 用
   [`detail_path()`](https://github.com/Lee-W/maigo/blob/main/scripts/board_state.py)
   算出細節檔路徑並依 §1a 格式建檔（事實區填入解析出的 author/URL/規模，`## 判斷` /
   `## 筆記` 留空）→ 索引行改寫成新文法，只留
   `- [ ] 👀 <狀態詞> @<author> <細節檔路徑> — <title>`；author 已知就保留於索引，URL 移至細節檔
3. 舊檔改名 `review-board.md.migrated`（留底不刪），之後一切只寫 `board.md`
4. [`review-batch-queue.md`](https://github.com/Lee-W/maigo/blob/main/skills/strict-review/references/review-batch-queue.md)
   的「持久 review board」段落改為指向本 skill，只保留 review 特有的 verdict 語彙說明

## 4a. 看完 review 的標記

在 board 把 👀 行勾成 `[x]`，或跑 `/maigo:board --reviewed <n...>`（等同勾上），都表示使用者
已看完目前報告、不需再留在待看清單；`--unreviewed`（或把 `[x]` 改回 `[ ]`）取消。下次刷新由
[`scripts/board_sync.py ack`](https://github.com/Lee-W/maigo/blob/main/scripts/board_sync.py)
呼叫
[`review_report.acknowledge`](https://github.com/Lee-W/maigo/blob/main/scripts/review_report.py)
把時間、使用者 login 寫進該 report metadata，須與目前 PR head 相同（規則見 §3a），再依 classify
結果更新 board。它不送 GitHub review。`--reviewed` 同時加 `🔖`，後續照 §5 學習。完整流程見
[`commands/board.md`](https://github.com/Lee-W/maigo/blob/main/commands/board.md)。

新報告會清除上一版的確認；新 commit／作者留言也會重新排入待看（👀 行自動取消勾）。單純碰檔案
mtime 或刷新 board 不會改最後 review 時間。cleanup 刪掉同 source 舊報告後，細節檔的舊 report
連結要用 Edit 換成 canonical `review/<id>/review.md`；只改路徑，保留其餘手寫內容。

## 5. 學習閘門（checkbox → `--learn` → 記憶層）

使用者需求原文脈絡：打勾＝「我看過/我親自處理了」，maigo 去看**你實際怎麼處理的**，判斷要不要把這項知識學下來。

1. **勾**：使用者在任何編輯器把 `- [ ]` 改 `- [x]`（nvim 一鍵）。勾與分區正交。🐛/🔀 的勾跨刷新保留；
   👀 的勾代表「看完報告」（§4a），回你的球時會自動取消勾，但 `🔖` 會把學習訊號留下來。
   也可用 `/maigo:board --check <n...>`；要取消就用 `--uncheck`。這兩個命令只改
   checkbox（不寫 snapshot、不 ack，效果等同手勾，下次刷新才判斷），保留分區、整行內容與
   `🧠` / `🔖`，並且 idempotent。
2. **偵測**：`/maigo:board` 刷新時列出「(`[x]` 或 `🔖`) 且沒有 🧠」的項目，提示跑 `--learn`。刷新本身**不**
   自動進學習——學習有 AskUserQuestion 確認，不該混進快速刷新。
3. **抓料**（`--learn`，委派 sonnet，一項一隻或小批）：抓該 item 上**你的**實際輸出——
   review：你的 review comments / verdict；issue：你的 triage 回覆；你的 PR：你怎麼回 reviewer。
   對照 maigo 記憶層現有條目，蒸餾 0–3 條候選知識（「使用者在 X 類 PR 特別看 Y」「使用者回
   NEEDS_INFO 的口吻慣例是 Z」）。沒有可學的就回「無候選」，不硬湊。
4. **確認**：orchestrator 走既有
   [`memory-propose-confirm`](https://github.com/Lee-W/maigo/blob/main/skills/memory-propose-confirm/SKILL.md) skill，
   逐條 AskUserQuestion，確認的寫進 `~/.config/maigo/memory/`（type: feedback / project 按內容判）。
5. **標記**：處理完（含「無候選」）該行加 `🧠`、拿掉 `🔖`；之後刷新不再提示。反覆出現的知識日後由
   [`/maigo:crystallize`](https://github.com/Lee-W/maigo/blob/main/commands/crystallize.md) 畢業成 skill——學習閘門只負責進料，不重造管線。

## 6. 在 nvim 裡怎麼用

真相層永遠是純 markdown 的 `.maigo/board.md`——agent 跟人都直接改它，不為排版
混入 HTML wrapper。**maigo 不提供任何呈現層，也不會建議你裝 nvim plugin**：
`.maigo/board.md` 就是最終產物，`:e` 開檔即讀即改。

1. **三個 fold**：三個 `## ` section 標題就是 treesitter markdown fold 的邊界，`zM`
   收合後只剩三行標題 ＋ 計數，`za`/`zo` 逐一展開想看的區。
2. **`/狀態詞` 搜尋**：狀態詞是純文字（`待 triage`、`CHANGES_REQUESTED`……），
   `/待送出` 之類直接命中；細節檔路徑內含編號（`i/9201.md`），`/9201` 一樣命中對應行。
3. **只找現在要看的 PR**：`/maigo:board --reviews`，看完報告後直接在 board 勾 `[x]`
   （或 `/maigo:board --reviewed <n>`），下次刷新就從待看清單移除；`--check` 只翻 checkbox，
   效果等同手勾。🐛/🔀 行的 `[x]` 仍只作學習訊號。
4. **細節檔路徑用 `gf` 跳過去**：裸相對路徑（不加反引號）就是 nvim `gf` 吃得下的形式，
   游標停在 `i/<slug>.md` 上 `gf`（Neovim 核心內建，不需 plugin）直接開那份細節檔
   （格式見 §1a）；看完 `<C-o>` 跳回 board.md 原本的位置。
5. **細節檔內 `gx` 開 GitHub**：真 URL 搬進了細節檔的「連結」那一行，游標移到該行 `gx`
   直接開瀏覽器到該 issue/PR；「筆記」段落裡的裸相對路徑（例：`review/9301/review.md`）同樣
   `gf` 可跳。
6. **勾 `[x]` 觸發 ack 與 `--learn`**：把 `- [ ]` 或 `1. [ ]` 改成 `[x]` 存檔即完成（見 §4a、§5），
   不需要額外命令；下次 `/maigo:board` 刷新會 ack 該 report，並列出「(`[x]` 或 `🔖`) 且沒有 `🧠`」的項目。
7. **一行一項**：`/` 搜尋與 `dd` 刪除都以行為單位，board.md 的每一行對應一個 item，
   nvim 原生操作即可管理，不需要任何格式轉換或外部工具。**`dd` 刪掉的行不會再冒回來**：下次刷新
   把它寫進排除紀錄（§3a），除非你又被重新指名審那顆 PR。

## 7. 跨 session 接續：`ListAgents` 查不到對應 session 時

使用者說「有個 session 在做 X」，但 `ListAgents` 查不到可觸及的對應 session——session 本身
消失了不代表工作內容跟著消失。**先查 `.maigo/board.md` 有沒有這個 issue/PR 的 `IN_PROGRESS`
行**（`/maigo:take-issue` 開工時會旁註 branch 名，見 `commands/take-issue.md` 步驟 4），有的話
直接用旁註的 branch 名定位 worktree；board 沒記到，才退而找對應 worktree 本身（該任務的
`.maigo/plan-<id>.md`——或遷移前留下的舊 `.maigo/plan.md`——是否存在、`git log`/`git status`
做到哪一步）——兩者都能讓 orchestrator 從既有進度接著跑，不必
等原 session 復活，也不必整個重新走一次 Raana 探索 + Tomori 規劃。

**不確定該任務在哪個 repo時**：這台機器裝了 maigo 的 repo 不只一個，先查
`~/.config/maigo/board-index.md`（沒有就先跑一次 `/maigo:board --cross-repo`
產生）縮小範圍，再進到命中的那個 repo 查 `board.md` / `plan-<id>.md`，比逐一
`cd` 進每個 repo 問一輪快。

## What this skill does NOT cover

- `/maigo:board` 的命令面（無參數刷新 / `<targets...>` / `--all` / `--learn` /
  `--check` / `--uncheck` / `--reviewed` / `--unreviewed` / `--reviews` / `--drop`）——
  見 [`commands/board.md`](https://github.com/Lee-W/maigo/blob/main/commands/board.md)
- Review verdict 本身的判斷標準——那是
  [`strict-review`](https://github.com/Lee-W/maigo/blob/main/skills/strict-review/SKILL.md) /
  [`strict-triage`](https://github.com/Lee-W/maigo/blob/main/skills/strict-triage/SKILL.md) 的事，本 skill 只管球權落點與行文法
