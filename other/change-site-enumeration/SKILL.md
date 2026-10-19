---
name: change-site-enumeration
description: This skill should be used when about to declare "N sites need changing", "the scope is closed", or "this is already fully shared" — before writing a plan that lists change sites, before implementing against a plan's site list, before reviewing a diff for lingering per-section branches, or before an orchestrator reports a scope/size number to the user.
---

<!-- mkdocs-include-start -->

# Change-Site Enumeration

**Owner agents**: Tomori (planning) / Anon (implementation) / Soyo (review)
**Consumers**: orchestrator — before declaring a scope/size number to the user

## 核心判準

適用時機：你準備說出「有 N 處要改」、「範圍是封閉的」、「已經共用化了」這類宣告。

**核心命題**：「有幾處要改」的宣告必須由**解析權威來源**得出——不能由清單轉述（plan 列的清單、
上一輪 review 點名的位置）得出，也不能由 grep 符號名（而非常數名/入口名）得出。三種常見的改動
形狀各自有不同的權威來源，查下表決定用哪一種枚舉方法。

## 依形狀查表選枚舉方法

| 改動形狀 | 枚舉方法 | 為什麼眼睛盤點會漏 |
|---|---|---|
| 使用者可見行為（搜尋／篩選／排序／顯示） | 從**使用者入口**反推：這個功能在站上/app 有幾個進入點？每個進入點綁到哪個 handler？資料來源各是什麼（DOM／索引／API）？入口數 > 1 就逐一確認。**不要**只 grep 相關符號名——那是從實作往外找，使用者的 bug 是從入口往內走。危險地帶：build 步驟（`postbuild`、索引產生腳本）、`_data` 之外的資料管線、第三方搜尋／索引套件——它們常常不讀頁面 HTML，改 template 對它們完全無效。 | 同一個使用者可見功能常有多套獨立實作，符號名不同、彼此不 import；grep 只找到走過的那一套，另一套安靜地不生效，不會有任何錯誤訊息。 |
| 平行程式碼收共用表 | **逐行 diff** 列出候選平行程式碼的**所有**差異 literal（欄位名、type id、yaml key、category 覆寫），列成清單後逐一問「這個能進表嗎？」——能進的全進，不能進的在註解寫明為什麼。判準寫成語意版：「這段邏輯還需要幾個 per-section 分支？」目標 0；不要寫成「reviewer 提的那個欄位收了沒」。**同源提醒**：收完別忘了同步那段解釋「為什麼需要各自的迴圈」的舊註解——理由消失後，留著的舊註解會誤導下一個讀者。 | 只收本輪 review 點名的那一個欄位，等於把同型 drift 留在原地——剩下的差異仍逼著程式碼保留 per-section 分支，下一個 reviewer 或下一個新 section 會再撞一次。 |
| 共用常數改 tuple arity／欄位數 | 用**常數名**（不是型別名、不是欄位名）`grep -rn` 全 repo（含 tests、含子專案之外），逐一標記「這裡是不是在解包」；改完再 grep 一次複查，確認沒有第 N+1 個站點。 | 解包站點不一定長得像解包：中繼變數（先存起來、下一行才拆）、comprehension 裡的 `for t, _ in ...`、參數化 fixture 的清單，都不會出現在「我以為會有的樣子」裡；tuple arity 錯誤是 runtime 才炸，路徑沒被測到時靜態檢查也不一定攔得下來。 |
| 同批下游的守衛／欄位對稱性 | 找出這批下游**全部**成員（同一個 base class 的子類、同一組 dispatch table 的 entry），逐一確認守衛/欄位是否存在；補一個就要補同批的全部。 | 不對稱本身即缺陷——只補被點名的那個，其餘成員在下一次同型輸入時仍會炸，且拋出的錯誤型別可能對不上（該是 `ValueError` 的地方變成 `TypeError`）。 |
| 拆／搬被別處引用的資料檔 | 拆檔前後各 `grep -rn` 一次舊檔名（含內容目錄、模板、測試），把引用清單列出來逐一改完，再 grep 確認零殘留；驗收看**產物**（該出現的區塊數量），不看 build exit code。 | 靜態產生器對「引用目標不存在」常靜默降級（渲染成一則註解、exit 0），build 綠也不代表引用沒壞；只改手邊正在編輯的那幾筆，舊內容的引用會安靜地失效。 |

## 各 consumer 怎麼套

**Tomori（規劃期）**：寫 plan 前先依上表枚舉落點，把用了哪種枚舉方法、枚舉出的清單寫進對應 step，
不要只寫「改 N 處」的數字結論——結論要附「怎麼查出來的」。

**Anon（實作期）**：**不要沿用 plan 列的清單**——plan 的枚舉可能是錯的（見 worked example 4：計畫
列 3 處解包站點，實作時重新 grep 才發現實際 5 處）。動手前自己依上表重新枚舉一次；若跟 plan 的
清單不一致，回報差異，不要靜默照 plan 做、也不要靜默照自己查的做而不說。

**Soyo（review 期）**：當作判準——問「這段邏輯還剩幾個 per-section 分支？」目標 0；問「這個常數／
入口的所有站點都改了嗎？」不接受「reviewer 上輪點名的那處改了」當作已窮盡的 evidence；diff 裡若
出現「已經共用化」「範圍封閉」這類宣告，要求作者展示枚舉方法，不是照單全收。

**Orchestrator**：對使用者宣告 scope／規模數字（例：「有 N 個檔案要改」「這 15 個都違規」）之前，
先用上表方法覆核一次；不要把 subagent 轉述的數字未經覆核就寫進對使用者的陳述——規模數字常常是
使用者接下來做決策（拆 PR、估工時）的依據，錯了要回頭改。

## Scope 邊界：該不該把某處拉進來,看消費者不是看語意

判斷一個 rename 該不該排除在 scope 外時，判準是**這個名字有沒有已經在外的
消費者**，不是「它描述的東西跟目標欄位是不是同一件事」。

同一個 PR 新增、尚無消費者的符號（欄位、CSS class、常數名），rename 的成本只是
diff 行數；留下一個對不上目標名字的舊符號，才是把成本轉嫁給下一個查它的人——
他會 grep 新名字卻找不到對應的樣式/程式碼。

**How to apply**：擬 plan 或路由計畫時，要把某個 rename 標成 out-of-scope 之前，
先枚舉那個名字的消費者（其他模組、JS、測試、外部 API、已發佈的文件）。枚舉方法
照上表——只 grep 舊名不算枚舉，舊名 0 命中只證明舊名沒了，不證明新名接得上；沒有
型別檢查的配對（例如 CSS/模板）要用腳本比對兩端的名字集合。枚舉成 0 個消費者就
把它拉進 scope，並在 plan 裡寫「無消費者，rename 成本為零」，不要寫理由辯護為何
不做。

案例：apache/airflow PR #70497，plan 把新欄位改名衍生的 CSS class 排除在外，理由
寫「class 描述的是表格 widget 而非 yaml 欄位」；reviewer 指出這些 class 是同一 PR
新增、尚無消費者，rename 現在免費、以後變 dead-name 債，最終照做，8 處 rename、
0 must-fix。

## 歸屬判定：這處是既有缺陷,還是本 PR 引進的

枚舉出 N 處之後還有一步：**每一處分別判歸屬**。同一個檔案裡同型的缺陷常同時橫跨
「main 上就已經錯了」與「本 PR 新增的行」兩種歸屬，而歸屬決定它由哪支 PR 修。

判準：歸屬由 `git diff <base>...HEAD` 的 `+` 行判定，**不能**憑「這看起來是舊問題」或
「這在既有缺陷清單裡」。記憶層或 plan 上的既有缺陷清單不是歸屬證據——那份清單寫於某個
時間點，本 PR 完全可能剛好又加了同型的一處。

兩個方向的誤判成本不對稱：把本 PR 引進的判成既有，會把自己造成的缺陷推給別的 PR，而
作者與審查者都會覺得範圍很乾淨；反向誤判只是 diff 變大。**不確定時往「本 PR 引進」偏。**

**How to apply**：

- 逐處跑 `git diff <base>...HEAD -- <file> | grep '^+.*<pattern>'`，命中的就是本 PR 新增的行
- 特別留意**執行期字串**（log/warning 訊息、例外訊息）與 generated 檔的來源檔：它們容易被
  當成「文件」而跳過歸屬判定，但使用者實際會讀到它們
- 切分 PR 時歸屬同時決定可行性——main 上不存在的行，沒辦法在 main-based 的 PR 裡修

案例：apache/airflow PR #72012，reviewer 指出 docstring 範例與其下的說明自相矛盾。枚舉出
6 處無效的 pydantic-ai model 前綴後，reviewer 與 review agent 都判為既有缺陷、建議留給
別的 PR；實查 `git diff main...HEAD` 的 `+` 行，其中 2 處是本 PR 新增的——包含一則會寫進
使用者 task log 的 warning，而它叫使用者去用一個會拋 `ValueError: Unknown provider` 的
前綴。後續切成兩支 PR 時，這 2 處只能留在原 PR，因為那兩行在 main 上不存在。

## 假訊號

**「有些關鍵字搜得到」不代表修正部分生效**——可能代表你根本沒碰到那條路徑，恰好搜到的詞跟你的
修正無關（例：某筆資料的 description 欄位碰巧含相關字串）。

**`grep`/`rg` 的 `--include`/`--exclude` 值帶 glob 沒加單引號，zsh 會在指令執行前展開**——
當前目錄沒有匹配檔名時直接中止整條指令（`no matches found`），不是回 0 命中。把這種
exit 非 0 讀成「已清空」，就是拿假陰性當範圍封閉的證據。一律寫成 `--include='*.css'`；
宣告「0 命中」之前，先拿一個已知存在的 pattern 反向驗證判準真的抓得到，判準本身沒被
驗證過的話，0 命中不構成證據。

## Worked examples

五個實例（前四個為 apache/airflow PR #70498、#70190）詳見 `references/worked-examples.md`：

1. #70498 — provider 搜尋的兩套獨立機制（inline 過濾框 vs 全站 Pagefind 索引）
2. #70498 — 同一個搜尋缺口的兩個入口共用（DOM 過濾 + build-time 索引產生），reviewer 只點名一個
3. #70190 — 平行 dict-shaped section 的 drift 被抓兩次（先 class-path 欄位，再 integration 欄位）
4. #70190 — 共用常數改 tuple arity，計畫列 3 處解包站點，實作重新枚舉後發現實際 5 處
5. 拆分被引用的資料檔 — 靜態產生器對壞引用靜默降級，build exit 0 但產物少了區塊

## 動手前的五個補充形狀

抽共用邏輯、加子類 override、加 swallow-and-log wrapper、移植機制、蓋新抽象——五種「改一處」形狀各自的
枚舉要點在 `references/enumeration-patterns.md`。
