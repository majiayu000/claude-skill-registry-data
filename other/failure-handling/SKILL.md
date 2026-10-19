---
name: failure-handling
description: This skill should be used when handling failures in go-class command flows — Soyo blocking with NEEDS_CHANGES / BLOCKED, Taki test failures, subagent infrastructure overload / unavailability (e.g. 529), mid-task usage/session-limit interruption of a running subagent, and infinite-loop protection for repeated same must-fix or same test ID. Applies to /maigo:go, /maigo:quick, /maigo:team, and /maigo:address-comments step 5.
---

<!-- mkdocs-include-start -->

# Failure Handling

**Consumers**: [`/maigo:go`](https://github.com/Lee-W/maigo/blob/main/commands/go.md) 失敗處理段、[`/maigo:quick`](https://github.com/Lee-W/maigo/blob/main/commands/quick.md) 同段、[`/maigo:team`](https://github.com/Lee-W/maigo/blob/main/commands/team.md) 同段、[`/maigo:address-comments`](https://github.com/Lee-W/maigo/blob/main/commands/address-comments.md) step 5 都引用本 skill。

### 爽世擋下（NEEDS_CHANGES / BLOCKED）

1. **完整把爽世 (Soyo) 的輸出傳給愛音 (Anon)**——must-fix 清單 + evidence 待補 + 具體改法
2. 愛音修完後，**必須附上每條 must-fix 的對應 diff 與 evidence**（不接受「都改好了」這種模糊回報）
3. 重新請爽世 review。爽世會逐條對照——任何一條沒清就維持 BLOCKED

### 修正輪閉環

套用任何 review 修正後，一律**送回同一位 reviewer** 複驗——同一個 context 才抓得到這輪
修正本身引入的新矛盾；換一個沒看過前情的 reviewer，等於失去對照歷史的能力。

1. **修到 PASS 為止**——每一輪修正都可能引入新缺陷，改完就收工等於沒驗；verdict 未達
   對應 command 的通過門檻前，流程不算完成。
2. **reviewer 無法續用**（原 agent session 已結束、必須開新 agent）時，**視同重新審查**：
   附上完整前情——原始 diff、前幾輪 must-fix 清單、目前已套用的修正——不能只給「這是修正
   後的版本」讓新 reviewer 從零判斷。

### 立希驗證紅

1. 把 failure 完整貼給愛音 (Anon)（command + exit code + output）
2. 🎀 愛音修完後，若程式碼、測試或其他受審內容有變，先送回 🟡 爽世複審，再讓 🟣 立希重跑；team 可依原本規則並行兩者。**不接受口頭說「修好了」，也不沿用修改前的 APPROVED。**
3. 只有修復環境且受審內容完全沒變，才能沿用 review、只重跑驗證。
4. 🟡 爽世 APPROVED 與 🟣 立希 PASS 必須對應同一份變更快照才算過。交辦與回報保留 HEAD、tracked diff 與 untracked 檔內容的識別／雜湊；僅 HEAD 相同不足以證明內容未變。修復改了內容，舊 review 與驗證結果都失效。

### 環境造成的假紅

測試紅燈被診斷為**環境造成的假紅**（Node/OS/工具版本行為差異，不是程式碼缺陷）時，
判準：乾淨環境會綠、紅的成因指向 Node/OS/工具版本而非被測程式碼本身。

優先順序：

1. **改環境設定讓它真的綠**（例如 `.claude/settings.local.json` 的 `env`、正確的 flag、
   對版本的工具）
2. 治本的 repo 改動（測試 setup 層的隔離），範圍合理時另開 PR
3. **最後才是遮蔽**（本 repo 的 known-test-failures 機制）

**Why**：遮蔽名單是全檔粒度，遮掉噪音的同時把該檔案未來的**真回歸**一起遮掉；環境修法
沒有這個代價，還會讓別的 session 也直接受益。

**不要把「加進 known-test-failures」當預設收尾動作**——寫之前先問使用者，並在選項裡說明
代價；修完環境要回報「修掉幾個 / 還剩幾個」，剩下的說清楚為什麼修不掉。

### Subagent 過載 / 不可用（如 529 Overloaded）

某個 agent 的 Task 因基礎設施問題（伺服器 529 Overloaded、逾時、暫時不可用）反覆啟動失敗，與該 agent 的工作品質無關時：

1. **有限次重試**——重試 **2-3 次**。每次重試成本不低（subagent 啟動到報錯可能耗數分鐘），不要無聲地一直重撞。
2. 仍失敗 → **把選項攤給使用者**，不自行決定：
   - 等久一點再試（短間隔重試只是重複燒時間；建議擱 20-30 分鐘讓尖峰過）
   - **orchestrator 主線代打**該 stage——繞過過載點立即解卡
   - 暫停，等基礎設施恢復後再接續
3. 使用者授權主線代打時：
   - **明示這違反該 command 的分工守則**（orchestrator 本不該自己 review / 實作），且**獨立性較弱**（等於審 / 改自己流程的產出）
   - **嚴格度不打折**——照對應 skill（如 `strict-review` 9 項）硬走，以 `git diff` / 實測為憑，不因「我自己跑」放水
   - review 類代打要實際構造場景驗證（不只讀 code 說 OK）；驗證類代打要貼真實 exit code
4. **infra 恢復後，讓真人 agent 補跑一次複核**——代打有真實盲點（代打者對該 repo 的慣例未必熟，且審/驗自己的產出獨立性弱）。基礎設施恢復可 spawn 時，對代打過的 stage 補跑真正的 agent 一輪；真人 agent 揪出代打漏掉的問題是常態，不是例外。

**不能做**：因 subagent 撞 529 就**跳過**該 stage（跳過 review / 跳過驗證）。過載是基礎設施問題，不是放行理由——要嘛代打、要嘛等，不能省。

### Subagent 中途被切斷（`stalled`／睡眠／連線中斷）

與 529 不同：529 是啟動失敗，這是**跑到一半沒了**，而且回傳往往只有一句 harness 訊息，看不出真因。

**`Agent stalled: no progress for 600s` 不等於基礎設施過載。** 同樣的訊息也會由
**本機電腦進入睡眠**產生（訊息可能到下一次才變成 `Your computer went to sleep
mid-response`）。差別很重要：過載該退避重試，睡眠退避無效——所以**不要**因為連續幾次
`stalled` 就把 prompt 拆得越來越小，那治不到真因，只是把同一份工作重跑好幾遍。
判準：`ListAgents` 顯示其他 agent 同時段也一起停、或多次中斷落在同一段掛機時間 → 懷疑睡眠。

**唯一可靠的緩解是把「落檔」寫進回報合約**，而不是縮小任務：

> 報告檔路徑：`<scratchpad>/<agent>-<task>.md`
> **每答完一條就立刻追加寫入，不要累積到最後才寫。** 若你中途被切斷，落檔的部分就是有效交付。

被切斷後的復原順序：

1. **先看落檔**（`ls` scratchpad、讀那個報告檔）——已答完的部分可能已經在裡面
2. **不要開新 agent 從頭重做**——用 `SendMessage` 續跑同一個 agent，transcript context 還在
3. 續跑指令要求**先盤點再續作**：讀既有報告檔 ＋ `git status` ＋ 檢視目標檔，逐項判斷做到哪，**只補缺的**
4. 明確告知「哪幾項已確認完成、不用重做」——orchestrator 自己先盤點過，能省掉一整輪

**第二個成因：單一前景指令長時間無輸出。** 睡眠之外，`stalled` 也常停在一個逼近 Bash
10 分鐘上限、期間不吐任何輸出的前景指令上（整包 pytest、`pnpm install`、mkdocs build）。
這是相關性觀察加合理機制（watchdog 只看得到「600 秒沒進度」），不是已證明的因果；但緩解
成本低，所以**交辦文一律附防停滯條款**——這也不是「拆小 prompt」，任務範圍不變：

> 任何可能超過 2 分鐘的指令一律背景執行、輸出導檔，用 `tail` 短指令輪詢；每條指令加
> `timeout`；每完成一步就把結論追加進 progress 檔。

續跑的上限與接手：

- 同一個 agent 經 `SendMessage` 續跑後**再次** `stalled` → 不要第三次續跑同一個
  transcript。改開新 agent，輸入＝progress 檔＋既有 scratchpad 產物＋完整失敗軌跡
  （原交辦文、兩次停在哪個指令）；要不要換模型依
  [`model-dispatch`](https://github.com/Lee-W/maigo/blob/main/skills/model-dispatch/SKILL.md)
  「模型選擇與重試」（只換已授權的替代模型，換了也計入兩輪重試預算）。這不違反上面
  第 2 點：新 agent 是接手續作，不是從頭重做。
- 被切斷的 agent 若正在做**變異驗證**，worktree 可能殘留被改壞的檔案——續跑或接手的
  第一件事是 `git status --short` 加 sha 對帳並還原，再做別的。

> 案例（2026-10）：兩個 sonnet review agent 各 `stalled` 兩次，每次都停在整包 pytest 的變異驗證或
> `pnpm install` 上，其中一個 worktree 殘留了 M5 變異，靠接手者先對帳才發現；之後約 14 個
> 交辦加上防停滯條款，含 35 分鐘、165 次工具呼叫的審查，零次 `stalled`。

### Subagent 中途撞 usage / session limit

與 529 不同：529 是啟動失敗，這是**跑到一半被切斷**——subagent 可能已完成部分工作（working tree 留有半成品），回傳卻只有一句 limit 訊息（含重置時間）。

1. **不要開新 agent 從頭重做**——半成品會跟新一輪工作糾纏，已完成的部分也白費。
2. Limit 重置後，**用 SendMessage 續跑同一個 agent**——transcript context 還在，任務背景不用重講。
3. 續跑指令必須要求**先盤點再續作**：`git status` + 檢視目標檔案，逐項判斷任務做到哪，只補缺的。盤點常發現工作其實已全部完成（切斷發生在回報前）——此時直接進驗證，避免重工。
4. 盤點與續作完成後照常走原流程——review / 驗證不因中斷打折。

### task-notification 標記 `status: failed`，不代表工作沒做完

跟 529（啟動失敗）、usage/session limit（有明確 limit 訊息）都不同：這是第三種訊號——subagent
在收尾寫最終報告時遭遇 API 連線中斷，task-notification 的 `status` 欄位字面上顯示
`failed`，`summary`/`result` 只留下被截斷的半句話（例："Exit 0, passed. Let's verify final
git state is clean..."）。**這個 `failed` 字面上看起來像整個任務失敗，但實際常常是：實質工作
（含 commit）早就做完，中斷只發生在自我確認 / 收尾報告階段。**

1. **先查實際狀態，不要照 `status: failed` 字面重派**——去該 agent 實際操作的目錄/repo 跑
   `git log --oneline` + `git status --porcelain` + `git diff --stat <base>...HEAD`，對照原始
   交辦的驗收條件逐項核對，而不是看到 `failed` 就假設一切從零開始。
2. 若 git 狀態顯示工作（含 commit）已完整——**不要重派 agent 從頭做**，直接把這個結果送進
   下一階段（review / 驗證），比照「Subagent 中途撞 usage / session limit」第 3-4 點的做法；
   被截斷的只是它自己的收尾敘述，不是它的產出。
3. 若 git 狀態顯示工作明顯未完成或矛盾——才視同「跑到一半被切斷」，比照上面 usage/session
   limit 小節處理（SendMessage 續跑同一 agent，要求先盤點再續作）。

### Handback 送達但內容遺失

`<task-notification>` 正常到達且 `status: completed`，`<result>` 寫著報告已用訊息送達，
但那則訊息從未出現——這是內容遺失，不是任務失敗。**不要**重派新 agent 重做同一輪工作、
不要自己代跑它該做的檢查、不要假設遺失的結論是 PASS。三步處置（先自己看現場 →
`SendMessage` 同一 agent 要求只重貼不重跑 → 採用重貼內容）與案例，見
[`references/handback-content-missing.md`](https://github.com/Lee-W/maigo/blob/main/skills/failure-handling/references/handback-content-missing.md)。

**附帶**：這也代表**不能用「收到 handback」當 agent 已停止的訊號**——handback 只是那一輪
的輸出，agent 可能仍在跑、仍在改共用 worktree；生命週期一律用 `ListAgents` 查。

### 等待自己開的背景 agent

用 Agent tool 開的背景 agent 完成時會自動發 task-notification 把 orchestrator 叫回來，**不需要
排 ScheduleWakeup 去輪詢**。ScheduleWakeup 是 `/loop` dynamic mode 專用工具，不是等待自己 spawn
的背景任務的機制——同一條教訓在不同 `/maigo:address-comments` 場次重複違反過，根因是
orchestrator 自己跑 `/maigo:*` 流程前沒有主動查一次 memory（見
[`skills/memory-loading`](https://github.com/Lee-W/maigo/blob/main/skills/memory-loading/SKILL.md)
consumer 清單已補上 orchestrator）。

背景 subagent 若寫了一個等待「從未被建立過的哨兵檔案」的假迴圈（例如輪詢一個不存在的 flag
檔案直到自己的 Bash timeout 打斷它），**不要重新 spawn 這個 agent**——用 SendMessage 直接告訴它
(1) 那個假旗標檔案不會被任何東西建立，停掉那個迴圈；(2) 明確給出它自己啟動的背景任務的真實
output 檔案路徑或 task id，叫它直接讀那個檔案或用 TaskOutput 查真實狀態。

同理，也**不要為了「等待」而 spawn 一隻 placeholder / fork agent**——harness 會在背景 agent
結束時自動發 task-notification，不需要任何 tool call 觸發。想等待時直接結束當前 turn（回一句
短訊息告訴使用者正在等什麼）即可。實例：一次為了等 review 完成而 spawn 的「placeholder to
force wait」agent 燒掉約 28 萬 subagent token 卻什麼都沒做。

### Subagent 拒絕 relay 而卡死

Orchestrator 用 `SendMessage` 把 Soyo 的 must-fix 轉給一個正在跑的 Anon 時，Anon 可能把這個
relay 當成「沒有使用者直接授權的 coordinator 訊息」而拒絕執行，即使 orchestrator 事後確認授權
也持續卡住。

**How to apply**：對於一個一行、完整指定的簡單修正（import 移動、rename、單行邏輯），
orchestrator 直接 inline 套用，不要再 relay 一次。真的需要委派時，開一個**全新**的 Agent()
（乾淨 context、無 relay 框架），不要對已卡死的 agent 再 SendMessage——同類任務由全新 agent
執行通常不會被拒絕。

### 先定位層級再修，不要直接 patch 工具原始碼

當某個 maigo / hook / 共用工具在**特定 repo** 表現異常時，先追高層再考慮改工具本身：

1. 這個 repo 是否已有對應的 `repo-aware` skill（如 `airflow-aware`、`commitizen-aware`）在處理這類摩擦？有 → 修法大概率在該 skill 或它引用的 seed。
2. maigo 的 `SessionStart` `repo_detect` hook 是否已經替這個 repo seed 了對應的 `.claude/<config>`？檢查 `hooks/repo_detect.py` 的 `REPO_RULES` → `claude_config_seeds`；若有，可能只是這個 worktree 建立在該功能之前，手動補寫一次 seed 檔即可。
3. 這個工具是否已支援 opt-in / opt-out 設定檔（如 `skip-test-verification`、`test-command`、`known-test-failures`）？有就用它。

三層都確認缺席後才考慮動工具原始碼——patch 共用工具的 blast radius 是跨 repo 的，一個為
某 repo 環境限制調校的「修法」會改變所有沒有那個限制的其他 repo 的行為。

### Stop hook 假陽性迴圈

當 Stop-hook 的 test verifier 因為**環境 / collection 層**問題（不是變更本身壞掉）逐輪重新觸發：

1. **先確認一次成因**——是 host 環境結構性壞掉（bootstrap / install-time 失敗），還是單純
   monorepo scope 抓錯 test 指令。前者才適用「寫 skip 檔」；後者且變更有真正新行為要覆蓋時，
   應該修對應的 `.claude/test-command` 成正確 scoped 指令、寫一個真的 test 去測，不要圖方便
   直接跳過驗證。
2. 環境結構性壞掉、且已經用該 repo 的真實 runner 確認過一次是綠的 → 立刻寫
   `.claude/skip-test-verification`（帶非空、非註解的原因說明）disarm 該 worktree 的 verifier，
   不要每輪重新解釋同一個假陽性——任何一次回覆都會重新觸發 Stop hook，逐輪重複解釋等於空轉。
3. 使用者明確說「忽略這個 hook」時，**輸出零字元**——連 `.`、`[ignored]`、空白都不行。任何輸出
   都會結束該輪、讓 harness 重跑 Stop hook、hook 再次擋下，形成迴圈。等使用者修 hook 設定 /
   中斷 session / 送新任務，不要逐次確認每次觸發。
4. **受限權限模式下，第 1、2 點的寫檔動作本身可能被擋。** `.claude/` 是 harness 的設定目錄，
   權限 classifier 會把寫入判成 self-modification / safety bypass（實例 2026-09-17，Claude Code
   auto mode：Bash heredoc 回 `[Self-Modification]`、Write 工具回 `[Safety Bypass Flag]`，同一個
   檔案兩條路都不通，hook 連擋五輪）。這道防護的用意是對的——不該讓模型自己關掉測試驗證——
   所以**不要繞**，也**不要換工具重試**（換工具做同一個動作，仍是同一個動作）。第一次被擋就
   停手交給使用者，並給**可直接執行的一行**，而不是「請你去寫個檔案」：

   ```text
   ! printf '%s\n' "<scoped test command>" > .claude/test-command
   ```

   `!` 前綴讓使用者在自己的 session 裡跑，輸出直接進對話。使用者授權後再由模型寫入亦可。

### 無限迴圈防護

計數只屬於同一個邏輯任務／執行批次，不帶入其他 work item 或舊 session 的歷史總數。
`verify_task.py` 首次回傳 run/task ID，重試須沿用；SubagentStop 只能辨識同一 agent 的續跑，
Stop 沒有可靠的 task ID。換 agent、沒有 hook 或缺識別碼時，由 orchestrator 保存本任務預算，
不能因 runtime 無法聚合就無限重試。doctor 的歷史次數不是這個連續計數。

- 爽世連續擋 **2 次**同一條 must-fix → 停下，請使用者介入（可能是計畫本身有問題）
- 立希連續紅 **2 次**同一個 test → 停下，請使用者介入（可能 test 本身需要更新）

「同一條 must-fix」判準：Soyo 輸出的 must-fix 條目**指向同一個檔案 + 同一個函式 / 區段 + 同一類問題描述**（不要求 wording 完全相同，但語意相同算同條）。Anon 改 wording、換實作方式但問題本質沒解掉 → 仍算同條。

「同一個 test」判準：test runner 報出的**同一個 test ID**（pytest 的 `path::TestClass::test_method[param]`、其他 framework 的等價 identifier）。**錯誤訊息字串變化不算「不同 test」**——ID 相同就是同一條。一次 run 裡多個 test ID 同時紅 → 各自獨立計次，不互相抵消。
