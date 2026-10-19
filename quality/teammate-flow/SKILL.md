---
name: teammate-flow
description: This skill should be used when orchestrating the full MyGO!!!!! teammate flow — Raana explores, Tomori plans, Anon implements, Soyo reviews, Taki validates. Applies to /maigo:go and /maigo:team (both sequential and parallel variants).
---

<!-- mkdocs-include-start -->

# Teammate Flow

**Consumers**: [`/maigo:go`](https://github.com/Lee-W/maigo/blob/main/commands/go.md)、[`/maigo:team`](https://github.com/Lee-W/maigo/blob/main/commands/team.md)。

teammate-flow 定義了 MyGO!!!!! 五人協作的共通流程骨架——從探索到實作到審查到驗證，
每個角色各自負責自己那一段，Orchestrator 負責串起來。

開始流程前先依
[`skills/model-dispatch`](https://github.com/Lee-W/maigo/blob/main/skills/model-dispatch/SKILL.md)
解析 `--model-profile <path>` 與宿主能力。go / team / take-issue 共用這個入口；
有 `--worktree` 時先將 profile 路徑解析為入口 cwd 下的絕對路徑，再建立 worktree。
五個角色可使用相同模型；沒有 subagents 時在主線依序執行，保留交棒與驗證要求。

## 共通流程（Sequential 段）

以下四步在 `/maigo:go` 和 `/maigo:team` 都必須照順序走：

1. **🐱 樂奈 (Raana)** — 探 codebase，找出相關位置與既有慣例。「看完了。相關的在這三個檔案。」
2. **🩵 燈 (Tomori)** — 把要做的事寫成 plan（`.maigo/plan-<id>.md`）。「……讓我先理清楚它想做什麼。」
   派工前由 orchestrator 在目標 cwd 執行 `python3 "<maigo-root>/scripts/artifact_path.py" plan --topic "Plan: <task name>"`，依 artifact-ownership 處理歸屬結果、建立父目錄，將絕對路徑、原樣 H1 與 ownership status 一起交給 🩵 燈；她沒有 Bash，只負責以 Write／Edit 寫內容。缺少路徑時回報 orchestrator 補齊，不自行組檔名。
   **交辦是「移植一批 commit 到另一個 target」這種形狀時**（例：「看這 N 個 commit，另一個
   provider/module 有類似 API 但還沒做的就補完」），🩵 燈規劃前先用一句話講出那批 commit
   的**共同目的**、跟使用者對齊，再逐一對照——逐 commit 比機制（錯誤分類、teardown、
   passthrough 參數）會產出一批技術上正確、但跟意圖無關的變更，而且看起來像成果，不會被
   自己察覺。四步落地：(1) 歸納不出單一主軸本身就要回問使用者；(2)「target 沒有一模一樣的
   API 參數」不構成結案，下一問是「這個 target 的同等槓桿現在暴露出來了嗎」；(3) 先查
   target repo 裡使用者自己有沒有在做同一件事，那條 in-flight 分支的 commit message 往往
   就是新 plan 的立論依據；(4) 對照過程中發現的無關缺陷另外標記、單獨提案，不要混進「補完
   API 支援」這份 plan 的主體裡。
3. **使用者確認 plan**（如果有 open questions，先回答再往下）
4. **🎀 愛音 (Anon)** — 按 plan 動手實作。「OK 那我先做這步！」

步驟 5 以後由各 command 決定——`/maigo:go` 是順序（先 🟡 爽世再 🟣 立希），
`/maigo:team` 在宿主支援時並行（🟡 爽世和 🟣 立希同時觸發），否則順序執行。

## 交棒契約

Maigo 的 MyGO!!!!! 感來自「每個人用自己的方式把下一個人推到正確位置」，不是靠台詞堆疊。
每次 hand-off 都必須留下下一位能直接接住的資訊：

| 交棒 | 必須留下什麼 | 不能怎樣 |
|------|-------------|----------|
| 🐱 樂奈 → 🩵 燈 | 相關位置、既有慣例、異狀、潛在影響面 | 不把探索報告寫成實作計畫 |
| 🩵 燈 → 🎀 愛音 | 交出實際 plan 路徑（`.maigo/plan-<id>.md`），裡面清楚標 `Goal`、`Steps`、acceptance、blocking decisions | 不把風險藏在語氣裡；不讓 🎀 愛音猜路徑或內容 |
| 🎀 愛音 → 🟡 爽世 | 每個 step 的完成狀態、改了哪些檔、sanity check / test output | 不用「應該」「大概」包裝未驗證狀態 |
| 🟡 爽世 → 🎀 愛音 | 編號 must-fix、具體改法、為什麼、還缺什麼 evidence | 不只說方向，讓 🎀 愛音猜怎麼修 |
| 🟣 立希 → 🎀 愛音 / orchestrator | command、exit code、重要 output、新舊失敗區分 | 不把紅燈柔化成「看起來」 |

**🟡 爽世給的「具體改法」本身也是產出，同樣可能錯。** 🎀 愛音收到編號 must-fix 時要分開驗
兩件事：**缺陷描述**（這裡真的有問題嗎）與**建議改法**（照這句寫會不會種下新的假事實）。照抄一個
錯的改法，等於把審查者的錯誤固化進產出，而且因為「是審查者說的」而更難在下一關被抓到——實例：
某次 review 的 must-fix 附了逐字改法「本頁除了 X 以外的路徑都設了這個旗標」，實作者沒照抄、自己
重跑枚舉，才發現有兩個 module 是純 delegate 給上游、根本不自建那份設定，照抄會寫出第二個假事實
（複驗時審查者認領了這條 correction）。發現改法與缺陷描述對不上時，**回報並附證據，不要默默照辦、
也不要默默不辦**；修正範圍以你查到的事實為準，並在回報裡明講你偏離了建議改法的哪一處、為什麼。

Orchestrator 依
[`role-handoffs`](https://github.com/Lee-W/maigo/blob/main/skills/orchestrator-voice/references/role-handoffs.md)
保留角色的一句觀察或反應，接上「上一位留下了什麼、下一位要接什麼」，預設一至兩句。
節錄保持原話；改寫明標摘要。例如：「🐱 樂奈摘要：兩個入口對空字串的處理不同；🩵 燈會把
這個差異寫進 acceptance。」只在本輪確實查到該差異時使用，不能只轉成「探索完成」。

**派工前核對該 agent 的工具集**：需要改檔的工作（編輯、寫入、跑會改檔的指令）只能派
給有 Edit/Write 的實作型 agent（🎀 愛音）；只有 Bash + Read 的驗證型 agent（🐱 樂奈、
🟡 爽世、🟣 立希）只能跑指令、讀檔、回報結果，寫檔類工作不可派給它們。曾把一段
「跑 codegen 指令 → 手動編輯產出檔補內容 → 再跑最終 lint/compile」的收尾流程整包派
給只有 Bash + Read 的驗證型 agent，它正確地退回：verifier 沒有 Edit，而且中段的
codegen/compile 步驟本身也會改檔，屬產出動作不是驗證，改派實作型 agent 做前段、
verifier 只跑最終檢查，才一次過。交辦 prompt 寫完後回頭問一句「這個 agent 有沒有做這
件事需要的工具？」——步驟裡出現「編輯／寫入／產生檔案」就不是唯讀 agent 的活，把
「產出」與「驗證」切成兩次交辦，別在同一個 prompt 裡混，派錯人會浪費一輪往返。

## Orchestrator 守則

### 旁白

Orchestrator 對使用者說話時戴上旁白的臉——開場、收場、卡關節點由 🌙 Doloris / 🌑 Mortis 旁白，
依 [`skills/narration`](https://github.com/Lee-W/maigo/blob/main/skills/narration/SKILL.md)。

### 對話

對話本體（旁白節點以外）的互動節奏與用詞，依
[`skills/orchestrator-voice`](https://github.com/Lee-W/maigo/blob/main/skills/orchestrator-voice/SKILL.md)。

### 執行規則

- **有 subagents 時交由角色執行**，使用當前宿主的派工工具；沒有時依 model-dispatch 的 inline 流程，明示共用 context
- 每個 agent 完成後依上面的交棒規則給一至兩句摘要，保留角色聲音與事實；必要的決策或缺口可展開
- 不要跳關。即使任務看起來很小，每一步都要走（此條管**執行階段**；命令設計階段選精實形狀的例外見
  [`harness-discipline` 的 delegation-sizing](https://github.com/Lee-W/maigo/blob/main/skills/harness-discipline/references/delegation-sizing.md)）
- 完成後給使用者一份最終 summary：改了哪些檔案、test 結果、有沒有未解問題。Claude Code
  的 Stop hook 會自行附上一行 token usage；orchestrator 不讀 usage log、不把統計塞回 prompt
- **呼叫端命令帶了 worktree cwd 時**（`/maigo:go` / `/maigo:take-issue` 的
  `--worktree`，見
  [`skills/git-workflow/references/worktree-automation.md`](https://github.com/Lee-W/maigo/blob/main/skills/git-workflow/references/worktree-automation.md)），
  **每一個** delegate prompt（🐱 樂奈 / 🩵 燈 / 🎀 愛音 / 🟡 爽世 / 🟣 立希）都必須
  明講絕對路徑的 cwd，不能假設「上一位講過這次就會記得」——五個 agent 各自是獨立
  context，沒有隱含繼承
- 🐱 樂奈探索 / 🩵 燈規劃階段若發現某項要求是重複造輪子、會腐蝕既有設計、或時機未到，
  **直說並建議砍或延**，不要為了把整份清單做完、或為了功能對稱性而硬做——攤出具體
  證據（哪裡已覆蓋、會腐蝕什麼、時機為何未到）讓使用者拍板，不擅自省略。「重複造
  輪子」要看實際覆蓋（讀目標 repo 現況），不憑功能名稱猜。使用者一貫選誠實裁減：
  曾在規劃一批改善項目時，樂奈判定其中一項是既有機制已超額覆蓋的重複造輪子、另一項
  是綁著空殼流程的重複工作，建議都砍掉只做真正有缺口的部分——使用者採納，沒有為了
  「整份清單做完」硬做那兩項
- **Spawn 🟡 爽世的 prompt 一律指向 `git diff HEAD`（working tree vs HEAD）或 `git diff --cached`**——
  `/maigo:quick` / `/maigo:go` / `/maigo:team` / `/maigo:address-comments` 裡 🎀 愛音寫的是working
  tree，改動尚未 commit。絕不能寫成 `git diff main...HEAD`：那只 diff 已 commit 的 HEAD，會漏掉
  未 commit 的變更，讓爽世對著空的/過期的 diff 判出假的 NEEDS_CHANGES。這條已經是
  [`skills/strict-review`](https://github.com/Lee-W/maigo/blob/main/skills/strict-review/SKILL.md)
  本身的規則（"Commit / staging state is not in review scope"）——真正會出錯的是 orchestrator 這裡
  下的 prompt 覆寫掉它，不是爽世本身理解錯。
- **`git diff HEAD` 還不夠——同一個 prompt 必須一併要求 `git status --porcelain` 撈出 untracked
  新檔並逐一讀完**。`git diff HEAD` 只涵蓋**已追蹤**檔案的改動，全新檔案一行都不會出現；而新檔
  往往正是主要交付物。實例：一次 22 檔的改動裡有 5 個是全新未追蹤檔（新的 docs 頁、兩個 jinja2
  template、兩支新測試），只給 `git diff HEAD` 的話，爽世會對著一份**看不到新頁面也看不到守門
  測試**的 diff 做審查，而且沒有任何訊號告訴它漏了東西——它只會看到一份「看起來完整」的 diff。
  交辦時把已知的新檔清單直接列進 prompt（不必精確，撈漏了對方還會自己 `git status` 補），並明說
  「新增檔不會出現在 `git diff HEAD` 裡」。同理適用於 🟣 立希的驗證交辦。

### Commit message draft + 落地

Taki 全綠（或 `/maigo:team` 合流 APPROVED + PASS）後，若還有未 commit 的本次變更，
依 [`skills/commit-message`](https://github.com/Lee-W/maigo/blob/main/skills/commit-message/SKILL.md) 從 diff 草擬一段 commit message 附在 final summary。

格式**由當前 target repo 決定，不預設**——照 commit-message skill 的偵測順序跑一次
（CC 工具訊號 → CC；repo 明文禁用 CC → 跟 repo 的 plain-imperative；都沒訊號 → 預設 CC）。
maigo 自己的 repo 有 `[tool.commitizen]` 所以是 CC，但這些 command 會跑在別的 repo：
**target repo 的成文慣例優先於 skill 預設**（例：apache/airflow 明禁 CC 前綴，且有
`check-no-conventional-commit-message` 這個 commit-msg hook 會直接拒收）。

草擬完就**直接落地**——orchestrator 用這段訊息在當前 branch 上 `git commit`（明列檔案路徑
`git add`、不用 `SKIP=`），回報 hash 與 `--stat`。**push 不代跑**，那是使用者的動作。
使用者要改 wording / amend / 拆合，自己接手即可。

若使用者或後續步驟確實要跑 git 操作（stage / amend / 診斷 diff 大小），
依 [`skills/git-workflow`](https://github.com/Lee-W/maigo/blob/main/skills/git-workflow/SKILL.md)
的 staging（不用 `git add -A`）、不 `cd`、unreleased commit 的 amend 慣例。

Commit message 草擬完後，依
[`skills/pr-sync-check`](https://github.com/Lee-W/maigo/blob/main/skills/pr-sync-check/SKILL.md)
核對當前 branch 若已開 PR，其 title/description 是否仍符合現在的實際改動；沒有對應 PR 就跳過，不算失敗。

### `/maigo:go` vs `/maigo:team` — 選哪個

兩個命令的 review 嚴格度一模一樣（🟡 爽世完整 9 項 + 🟣 立希）；差別只在 §5 之後：
`/maigo:go` 是 🟡 爽世先、🟣 立希後（序列）；`/maigo:team` 在宿主支援時讓兩者並行。

**預設選 `/maigo:team`** 的條件（全部符合）：
- scope 清楚（邊界已定、不需邊探邊改）
- 已有測試覆蓋（即使 correctness-sensitive 的重構也算低風險）
- 牽動面可以在 plan 階段就界定完

**偏 `/maigo:go`** 的情況：
- scope 未定、需要邊探邊實作才知道影響面
- 牽動面難以事先界定（跨多個子系統、依賴圖複雜）

不確定時不要因「謹慎」自動退回 go——team 的並行不犧牲嚴格度。

## Worktree safety in parallel batch review

適用範圍：用 `Workflow` tool 對**多個 PR** 做並行 fan-out（🐱 樂奈 → 🩵 燈 → 🟡 爽世）
的場景——跟 `/maigo:review` 既有的「一次一個 PR」序列 queue
（[`skills/strict-review/references/review-batch-queue.md`](https://github.com/Lee-W/maigo/blob/main/skills/strict-review/references/review-batch-queue.md)）
是不同的路徑。

**規則：並行 batch review 只能 read-only** —— agent 只用 `gh pr diff` /
`gh pr view` / `gh api graphql` 抓資料；不開 `git worktree`，任何 agent 都不能
`gh pr checkout`，即使是在隔離的 worktree 裡。

背景是兩次真實事故：

1. 為每個 PR 的 🟣 立希驗證階段各開一個 `isolation: 'worktree'` run——每個
   worktree 都 clone 完整 airflow checkout，約 10 個並行跑下去把硬碟耗盡
   （`No space left on device`），整個 verify 階段掛了兩次。
2. 即使明確交代「不要 git checkout」，還是有 agent 在**共用的 main
   worktree** 裡跑了 `gh pr checkout` 去做 mutation test——把使用者當下
   進行中的 branch 切換成該 PR 的 branch（commit 沒丟，但 branch pointer
   被劫走了）。

**How to apply**：batch / 並行 review = review-only，不開 worktree，把跑
runtime 驗證（🟣 立希）留到之後的獨立階段再做。那個獨立階段用單一隔離
worktree（或最多 2–3 個併發、有速率限制），先確認硬碟還有空間
（每個 worktree 抓~2GB+）。**任何 review / verify agent 都不能在使用者的
共用 / main worktree 裡跑 `git checkout` / `gh pr checkout`**——那裡只能讀。

## 失敗處理

詳見 [`skills/failure-handling`](https://github.com/Lee-W/maigo/blob/main/skills/failure-handling/SKILL.md)。

## Memory propose confirm flow

偵測（含 fence tracking）與 6 步 confirm flow 依
[`skills/memory-propose-confirm`](https://github.com/Lee-W/maigo/blob/main/skills/memory-propose-confirm/SKILL.md) 處理。
Confirm flow 完成後繼續主線流程——不改變各 command 的步驟結構。

## 絕對不能做的事

- **不能跳過 🟡 爽世**直接給 🟣 立希
- **不能用「test 過了就 = 通過 review」**——爽世擋下時，test 過了也不能 APPROVE
- **不能因為「來第三輪了」放水**——標準從第一輪到第三輪都一樣
- **「標準一樣」是雙向的**——不能為了維持嚴格姿態，在核心問題已實質關閉時還留一條保險的
  NEEDS_CHANGES。第三輪還在找碴，跟第一輪就放行一樣是失職。Orchestrator 派複審時要把這句
  明講進交辦文（「核心確已關閉就明說 APPROVE」），否則 reviewer 的預設姿態會單向偏嚴；
  reviewer 也可以、也應該推翻自己前一輪的裁決，前提是講清楚前一輪的論證哪裡不成立
