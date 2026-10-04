---
name: glowup-review-pipeline
description: "驅動 Glow Up 美妝評論網站的完整資料管線——從 Threads/Google/小紅書抓評論，到用 Claude Code 本身當 LLM 做語言理解標記、Python 做加權計算，產出可重現的評分 CSV。務必在使用者提到「更新評分」「抓新資料」「跑評分」「幫我評分」「新增了XX小紅書/Threads/Google資料」「這個品項評分」或提到 route_reviews.py／score_reviews.py／parse_xhs.py 等本專案腳本名稱時觸發，引導 Claude Code 正確走完抓取→圖上心得補救→清洗→路由→評分六個步驟，而不是憑印象或單一步驟猜測。"
---

# Glow Up 評論管線

這是一個多步驟、有明確順序的資料管線技能。**不要跳步驟**——每一步都是因為踩過真實的坑
才加進來的（詳見「已知地雷」），跳過會導致資料錯置或分數被誤覆蓋。

## 先讀這兩份專案文件，它們是權威來源，本檔不重複內容

- **[`../../../CLAUDE.md`](../../../CLAUDE.md)**——專案現況、資料夾結構、API Key 清單、
  「已知問題/待辦」。開始任何工作前先讀，尤其是文件開頭的「目前資料狀態」區塊（了解現在
  有多少品項已評分）。
- **[`../../../SKILL_商品評比.md`](../../../SKILL_商品評比.md)**——完整評分方法論：LLM
  怎麼標記每則評論（商品身份比對、業配偵測三層篩查、情緒強度七級、可信度三級）、Python
  怎麼把標記轉成分數（加權平均、共識度修正、雙軌加權、兩極化偵測）。**評分相關的所有規則
  細節都在這份文件，不要自己發明新的判斷邏輯。**

> ⚠️ 這份方法論文件描述的是「理想設計」，`score_reviews.py` 目前的實作**大部分**已對齊
> （共識度修正、雙軌高頻加權、負評可信度保護規則都已補齊），但情緒換算分與可信度權重的
> 「數值」是刻意重新校準過的（程式碼裡有註解說明），跟文件裡 Step 3.4／4.1 表格寫的原始
> 數字不同——這是有意的調整，不是 bug，兩邊數值不必強求一致。真的要確認實際數值以
> `score_reviews.py` 檔案開頭的 `SENTIMENT_SCORE` / `CREDIBILITY_WEIGHT` 常數為準。

## 六步驟總覽

```
Step 1  在 csv/Items.csv 把要更新的品項 "Update This Time" 欄填 "yes"
Step 2  跑爬蟲：Threads + Google 自動化；小紅書半手工（存 HTML → parse_xhs.py 匯入）
Step 2.5 圖上心得補救：檢查有沒有「心得寫在圖片裡」的貼文（見下方章節，每次有新資料都要查）
Step 3  clean_data.py 清洗廣告
Step 4  多品項拆分與歸位路由：route_reviews.py（LLM兩段式）或 route_xhs_programmatic.py（小紅書單品牌資料夾捷徑）
Step 5  審核 csv/候選新品.csv，決定要不要收編新品項
Step 6  評分：score_reviews.py（LLM兩段式，Claude Code 自己扮演標記者）
```

以下逐步展開；每一步該跑哪個指令、輸出去哪裡，`CLAUDE.md` 的「工作流程」章節有完整指令
區塊可以直接照抄，這裡只講「為什麼」跟容易出錯的地方。

### Step 1-2：標記待更新品項、抓資料

`scrape_threads.py`／`test_google.py` 是全自動的，`.env` 裡的 key 沒過期就能直接跑。
小紅書是半手工：使用者存 HTML 到 `小紅書美妝貼文/{子分類}/{品牌資料夾}/`，然後跑
`parse_xhs.py {子分類...}`（或 `--all`）匯入。**這一步是冪等的**（依 URL 去重），重跑不會
重複匯入，所以可以放心多跑幾次確認有沒有新檔案進來。

注意檢查：新增的小紅書資料夾有沒有不小心巢狀放錯位置（例如把「眼霜」子分類的資料夾整個
搬進「面膜」資料夾底下）——如果真的看到某個資料夾底下有跟資料夾名稱完全對不上的品牌
子資料夾，先確認過再匯入，不要讓錯置的資料污染到不相關的子分類。

### Step 2.5：圖上心得補救（每次有新資料都要檢查一次，不是一次性）

**背景**：有些貼文的心得是寫在圖片裡而不是貼文本文（小紅書長圖文、Threads 截圖轉發都
發生過），爬蟲/parse_xhs.py 抓不到圖片裡的文字，該則評論看起來內容很短甚至空白，但圖片
裡才是真正的心得，直接漏掉等於少了一部分真實聲音。**這是每次有新資料就該檢查的標準動作，
不是只在遇到特定子分類時才做一次的例外處理。**

**小紅書**（前提：貼文是用瀏覽器「完整網頁」存檔，該篇旁邊會多一個 `{檔名}_files/`
資料夾）：
1. `python3 extract_xhs_images.py 子分類A 子分類B`（或 `--all`）→ 掃有 `_files/` 的貼文，
   濾掉頭像/icon，把內容大圖轉成 png，產出 `llm_io/xhs_image_manifest.json`
2. 由你（Claude Code）逐張 Read manifest 內的 png，把圖上文字抄出來，寫成
   `llm_io/xhs_image_texts.json`（格式：`{url: 圖片內文}`）
3. `python3 merge_xhs_image_text.py` → 把圖片內文接回三份 reviews json 的 `content`
   欄位（冪等、可重跑，標記 `image_review: true`）
4. 之後 Step 6 評分時，這些補回的內文才會真正被讀到。

**Threads**：目前沒有對應的自動抽取工具（Threads 沒有「完整網頁存檔含原圖資料夾」這個
管道）。若發現某則 Threads 評論內容異常短/空白但明顯附了截圖，手動打開原始連結把圖片裡
的文字抄進該筆記錄的 `content` 欄位，格式比照 `merge_xhs_image_text.py` 的
`【圖片內文】` marker 寫法。這是已知的工具缺口——如果之後這類 Threads 貼文量大到需要
自動化，可以參考小紅書那套三段式流程另外做一版。

### Step 3：清洗

`python3 clean_data.py`——過濾業配/廣告，輸出 `cleaned_reviews.json`。沒有需要注意的坑。

### Step 4：多品項拆分與歸位路由

一篇貼文常常同時講多款商品，需要先拆分再歸位到正確的品項，評分才不會把 A 商品的評論
混進 B 商品。兩條路徑，依情況選：

- **`route_reviews.py`（LLM 兩段式，處理多品項/不確定的情況）**：
  `--prepare --subcat 子分類A,子分類B` 產出 `llm_io/route_requests.json` → 由你讀取、
  逐則拆分並比對商品目錄、寫出 `llm_io/route_responses.json` → `--compute` 產出
  `routed_reviews.json` + `csv/候選新品.csv`。**目錄裡有對應的品項才會被歸位，目錄外的
  新品只會被暫存到候選新品清單，不會自動收編、不會被評分**——這是刻意設計，避免亂長品項。
  - ⚠️ `route_reviews.py` 只處理小紅書貼文（設計如此，Threads/Google 一律原樣通過不拆分）。
    如果加了新的子分類，記得檢查 `route_reviews.py` 裡的 `FOLDER_TO_SUBCAT` 對照表有沒有
    登記這個子分類的小紅書資料夾名稱——沒登記會直接找不到任何待拆分貼文（0則），這個坑
    已經真的踩過一次（面膜/面霜當時漏登記）。
- **`route_xhs_programmatic.py`（程式化捷徑，免 LLM，只適用單一品牌資料夾）**：小紅書
  貼文如果已經放在「單一品牌」的子資料夾（不是「多品項XXX評比」這種混合資料夾），品牌
  名稱明確，不需要 LLM 拆分，直接依資料夾開頭品牌名比對 `Items.csv` 補上 `item_id` 更快。
  用法：`python3 route_xhs_programmatic.py 子分類A 子分類B`。跟 `route_reviews.py` 是
  互補關係，不是取代——多品項/評比類資料夾這支腳本會自動跳過，交給 `route_reviews.py` 處理。

`score_reviews.py` 找不到 `routed_reviews.json` 時會自動退回舊的 `cleaned_reviews.json`
+ keyword 比對，向後相容，但比對會比較粗（見「已知地雷」的雜訊問題）。

### Step 5：審核候選新品

打開 `csv/候選新品.csv`，人工確認哪些是真的要收錄的新品項，手動補進 `Items.csv`，再重跑
Step 4 讓新加入的品項也能被歸位。這一步沒有自動化，是刻意要有人把關。

### Step 6：評分

`--prepare --subcat 子分類A,子分類B` 產出 `llm_io/score_requests.json` → 由你（Claude Code）
逐則標記（見下方「標記時的角色」）、寫出 `llm_io/score_responses.json` → `--compute` 算分。

**標記時的角色**：你就是 `SKILL_商品評比.md` 裡說的「LLM」，負責純語言理解——商品身份
比對（是不是同一個商品/系列/規格）、業配偵測、子款識別（`sub_variant`）、情緒強度標記、
可信度判斷。**不要自己心算分數**——加權平均、共識度修正、兩極化偵測全部是 Python
（`score_reviews.py`）做的計算，你只需要老老實實輸出結構化標記，讓分數可重現。

## 已知地雷（每一條都真實發生過，不是理論風險）

1. **`score_reviews.py --compute` 沒有 `--subcat` 參數，永遠重算全部 430 個品項。**
   若 `score_responses.json` 只包含本輪新標記的子分類，其餘沒被標記到的品項的
   `product_key` 不在檔案裡，程式碼會直接跳過（保留 CSV 裡的舊分數），**理論上**不會被清空
   ——但這個保護是後來加的修正，**每次跑完 `--compute` 還是要親自比對新舊 `csv/AI_Scores.csv`
   的 `Subcategories` 欄位去重清單有沒有無故消失**，發現不對馬上停手排查，不要接著跑
   `build_scores_data.py`（會把錯誤傳播到前台）。這是實際發生過一次的資料遺失事故
   （2026-07-21，靠 Time Machine 復原），養成每次跑完就 diff 一下子分類清單的習慣。
   建議先 `cp csv/AI_Scores.csv csv/AI_Scores.csv.bak_<說明>` 再跑 `--compute`。

2. **Python 版本**：`route_reviews.py`、`score_reviews.py` 必須用 `/usr/bin/python3`（3.9），
   PATH 上預設的 anaconda Python 3.6 不支援 `anthropic` SDK。爬蟲/清洗腳本用哪個都可以。

3. **關鍵字比對（keyword-fallback）雜訊很多**：`score_reviews.py` 對沒有 `item_id` 的評論
   會用品牌+商品名的字串比對來抓可能相關的評論（主要是 Threads/Google 資料，因為只有小紅書
   會被路由），這個比對很寬鬆，容易抓到同品牌但完全不相關的貼文（例如「M.A.C」品牌關鍵字
   比對到「MacBook」的討論串）。這正是 Step 6 標記時 `product_match: mismatch` 存在的原因
   ——標記時要真的讀內容判斷是不是同一個商品，不要因為它出現在候選清單裡就預設相關。

4. **小紅書資料夾容易巢狀放錯**：見 Step 2 的提醒。

5. **前台「真實網友心得」卡片目前 100% 來自小紅書**，不是因為資料真的只有小紅書
   （原始語料 Threads 反而佔多數），而是 `build_scores_data.py` 的 `pick_testimonials()`
   只從有 `item_id` 的評論裡選，而只有小紅書會被路由。如果要讓心得卡片的來源比例更真實，
   需要調整 `pick_testimonials()` 也從已標記 `product_match: match` 的 Threads/Google
   評論裡選，而不是只看有沒有 `item_id`。

6. **`route_reviews.py --compute` 曾經會整批洗掉「其他子分類」先前的路由結果**（已修好，
   但務必知道這個坑）。舊版 `compute()` 每次都只帶著「本輪 `--subcat`」的
   `llm_io/route_responses.json`，本輪沒標記到的 rid 一律直接退回未路由的
   `cleaned_reviews.json` 原始記錄（不含 `item_id`），等於把之前任何一輪（不管是
   `route_reviews.py` 的 LLM 路由，還是 `route_xhs_programmatic.py` 的程式化路由）已經
   標好的 `item_id` 全部蓋掉。**2026-07-28 資料遺失事故**：跑完面膜/面霜的 `--compute`
   後，`routed_reviews.json` 裡粉底液（含植村秀）等所有其他子分類的 `item_id` 全部消失，
   導致前台「真實網友心得」卡片全部顯示「尚無足夠社群心得資料」，連帶讓依賴
   `pick_testimonials()` 的 `build_scores_data.py` 重建 `scores-data.json` 時，把手動補寫的
   `reviewSummary`（網友評價匯總）欄位也一併洗掉（`build_scores_data.py` 本身也有份，見下）。
   **已修正**：`compute()` 現在會先讀舊的 `routed_reviews.json`，本輪沒有標記到的 rid 改成
   沿用舊檔裡「已路由」的版本（保留 `item_id`），只有從未被任何一輪處理過的 rid 才退回原樣
   通過，不會再互相覆蓋。**但事故當下刪除評論路由備份不可逆**：清理專案雜物時如果看到
   `routed_reviews.backup_*.json` 這類檔案，即使看起來像過期產物，也**不要因為「只留最新
   一份」的原則就刪光**——每一份都是不同時間點某輪路由的快照，是這個舊 bug 的唯一救命索。
   建議至少保留最近 2-3 份、或每次 `route_reviews.py --compute` 前也養成
   `cp routed_reviews.json routed_reviews.json.bak_<說明>` 的習慣。

7. **`build_scores_data.py` 每次都是從 `csv/AI_Scores.csv` + `routed_reviews.json` 重新
   算出 `scores-data.json`，不會保留任何「額外手動補寫、不是從 CSV 算出來」的欄位**——
   例如「網友評價匯總」用的 `reviewSummary` 欄位。舊版直接用 `data.setdefault(key, {...})`
   建立全新模板，從來沒讀過舊檔，重建一次就把 `reviewSummary` 洗掉一次（就是上面地雷6
   事故的第二個成因）。**已修正**：現在 `main()` 開頭會先讀舊的 `scores-data.json`，把每個
   品項的 `reviewSummary`（如果有）原樣帶進新模板，之後才用 CSV 算分數覆蓋其餘欄位。
   之後如果還要加其他「非 CSV 算出來」的手動欄位，記得比照這個做法補進保留邏輯，
   不要假設重建腳本會自動保留。

## 完成評分後

`python3 build_scores_data.py` 重新產生前台用的 `scores-data.json`。這一步之前如果懷疑
`AI_Scores.csv` 有問題（見地雷1），先不要跑這步，把錯誤範圍確認清楚再繼續，避免把錯誤
傳播到前台。
