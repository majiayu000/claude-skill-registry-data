---
name: plain-language
description: 把繞口、術語堆疊、一句話塞三個概念的 AI 回覆或技術文字，改寫成人類一眼看懂的白話 —— 中文走中文的規則，英文走英文的規則，且都不改變原意。Rewrites convoluted AI output and technical writing into plain language a human gets on the first read; Chinese and English each have their own rule set. 當用戶說「白話」「翻成人話」「太繞口」「看不懂」，或說 "plain English"、"simplify this"、"too wordy"，或當你自己正要輸出一段密度過高的解釋時，載入這個 skill。
---

# plain-language：把 AI 話翻成人話 / Plain-language rewriting

> 目標讀者是**忙、聰明、但沒空解碼**的人。他要的是「看一遍就懂」，不是「讀三遍才懂」。
> The reader is busy, smart, and has no time to decode. They want to get it on the first read.

## 先選語言軌 / Pick the language track first

中文和英文的病灶不一樣，改法也不一樣。**不要把一種語言的規則套到另一種上。**
Chinese and English fail in different ways and need different fixes. **Do not port one language's rules onto the other.**

| 輸出語言 Output | 讀這份 Read |
| --- | --- |
| 繁體中文 Traditional Chinese | `references/zh-TW.md` |
| English | `references/en.md` |

舉例：中文的頭號病灶是「一句話塞三個概念、沒有斷點」；英文的頭號病灶是「被動語態藏掉主事者」和「名詞疊名詞」。兩者的解法沒有交集。
Example: Chinese's worst habit is cramming three ideas into one unbroken sentence; English's is agentless passive voice and noun stacking. The fixes don't overlap.

如果 `references/_private-examples.md` 存在，一併讀取 —— 那是本機專屬的真實案例，不會進版控。
If `references/_private-examples.md` exists, read it too — local-only real cases, never committed.

**本檔案是兩軌共用的部分** —— 紅線、長文結構、自檢、什麼時候不要用。語言層的診斷、改寫規則、範例都在 `references/` 裡。
**This file holds what both tracks share** — the red line, long-form structure, the checklist, and when not to apply this. Language-level diagnosis, rewrite rules, and examples live in `references/`.

## 0. 唯一紅線：可以變好懂，不可以變不對 / The one red line

白話化 **不等於** 簡化。以下一律原封保留，寧可句子長一點：
Plain language is **not** simplification. Preserve these verbatim, even at the cost of a longer sentence:

- 數字、單位、比較基準 / numbers, units, baselines（`+5.3%` 不能變「表現不錯」／not "solid results"）
- 限制與前提 / constraints and preconditions（「只在大型訂單成立」／"only holds for large orders"）
- 風險與不確定性 / risk and stated uncertainty（「待驗」不能變「可行」／"unverified" is not "works"）
- 專有識別碼 / identifiers（API 端點、檔名、函式名、欄位名、行號）

**如果為了好懂必須犧牲準確 → 選準確，然後把難的部分拆成兩句話講。**
**If clarity would cost accuracy, keep the accuracy and spend two sentences on it.**

## 1. 長文結構（超過 6 個 bullet 或 150 字就必須做）/ Long-form structure

長回覆真正的問題不是長，是**讀者不知道自己讀到哪、這段要幹嘛**。
The problem with a long answer isn't length — it's that the reader can't tell where they are or what a section is for.

### 骨架 / Skeleton

```
【重點】/ 【Bottom line】
＜結論一句＋所以要做什麼一句。讀者只讀這塊就要能做決定＞
＜One sentence of conclusion, one of what to do. A reader who stops here still decides correctly＞

1. ＜起：現在是什麼狀況 / what the situation is＞
2. ＜承：為什麼會這樣、影響多大 / why, and how far it reaches＞
3. ＜轉：有哪些選擇、卡在哪 / the options and the conflict＞
4. ＜合：建議什麼＋理由一句 / the recommendation and one reason＞

附：原始細節 / Appendix: raw detail
附：不確定的地方 / Appendix: what's unconfirmed
```

### 規則 / Rules

- **開頭那塊先給最精華的結論，不是給主題。** 讀者的第一秒要拿到答案，不是拿到預告。
  **Lead with the conclusion, not the topic.** The first second must deliver the answer, not a table of contents.
- **開頭塊不放理由、不放過程、不放細節。** 理由留給第 4 段，細節留給附錄。
  **No reasoning, process, or detail in the lead block.** Reasons go in section 4; detail goes to the appendix.
- **開頭塊要能單獨存活。** 假設讀者看完它就關掉視窗 —— 他做的決定還是對的嗎？不是就重寫。
  **The lead must survive alone.** If the reader closes the window right after it, is their decision still right?
- **下面的編號小節是「逐一確認」，不是「重新推導」。**
  **The numbered sections are for verification, not re-derivation.**
- **小節標題一律加編號（1. 2. 3. …）。** 讀者要能一眼看到「總共幾段、現在第幾段」。
  **Always number the sections.** The reader needs to see how many there are and where they are.
- **小節標題要是「一句帶內容的話」，不是抽象標籤。** 把所有標題連起來讀，就該懂全文八成。
  **Headings must carry content, not be labels.** Reading only the headings should give ~80% of the answer.
  - ❌ 1. 現況分析／2. 資料層／3. 結論 · 1. Analysis / 2. Data layer / 3. Conclusion
  - ✅ 1. 欄位被拆一半就停手／2. 前端還在讀，所以折扣永遠是 0／3. 建議另開一張卡
- **編號只給主體那 4 段。** 附錄不編號，讀者才不會以為後面還有重點沒讀。
  **Number the body only.** Leaving appendices unnumbered signals there's no buried lede left.
- **標題說出「出了什麼事」，不是「這段在講什麼」。**
  **A heading says what went wrong, not what the section covers.**
- **一節最多 3-5 個 bullet。** 超過就是兩件事黏在一起，拆成兩節。
  **3-5 bullets per section, max.** More than that means two topics stuck together.
- **「要處理」不是結論，是空話。** 每個行動項都要有：**誰**做、動**哪個檔案／分頁／欄位／行號**、改成**什麼**。
  **"Needs handling" is not a conclusion.** Every action item needs an actor, a location (file / sheet / column / line), and a target state.
  - ❌ 常數欄：要處理 · Constant column: needs handling
  - ✅ `config/limits.yaml` 的 `retry_count`（永遠是 3）：從設定檔移掉，或改程式不要讀它 —— 由你決定
- **原文缺主詞或缺位置時，不要幫它圓過去。** 寫「原文沒說」並列成一節。白話化只能把話講清楚，不能生出原文沒有的事實。
  **Never paper over a missing actor or location.** Label it `原文沒說` / "the source doesn't say" and list it. Plain language may clarify; it may not invent facts.
- **表格一律拆成 bullet。** ASCII 框線表格（`┌─┬─┐`）在手機、Telegram、Discord 上會爛成一團。
  **Break tables into bullets.** Box-drawing tables collapse into noise on phones and chat clients.
- **分類清單先講「哪幾類要動」，再列全部。** 讀者要的是待辦，不是分類學。
  **Say which categories need action before listing all of them.** The reader wants a to-do list, not a taxonomy.
- 短內容不要硬分節。分節是為了導航，不是儀式。
  Don't section short content. Structure is navigation, not ceremony.

## 2. 交付前自檢 / Pre-flight checklist

- [ ] 第一句話單獨拿出來看，有回答問題嗎？/ Does the first sentence, alone, answer the question?
- [ ] 有哪句話要讀兩次才懂？→ 拆掉 / Any sentence that needs a second read? Split it.
- [ ] 每個抽象名詞，讀者能指出它是什麼嗎？/ Can the reader point at what each abstract noun refers to?
- [ ] 數字、限制、風險、不確定性，一個都沒漏掉嗎？/ Every number, constraint, risk, and hedge still there?
- [ ] 每個「要處理／要修」都指到具體檔案、分頁、欄位或行號了嗎？沒有就標「原文沒說」
      Does every "fix this" point at a file, sheet, column, or line? If not, label it as missing.
- [ ] 意思有跑掉嗎？（拿原文逐點對一遍）/ Did the meaning drift? Check point by point against the source.
- [ ] 有沒有為了好懂而變成廢話？（「表現不錯」「值得關注」＝廢話）
      Did clarity turn into vacancy? ("solid results", "worth watching" = vacancy)
- [ ] 長文：開頭那塊單獨看，讀者能不能直接做決定？/ Long form: can the reader decide from the lead block alone?
- [ ] 長文：小節有編號嗎？標題連起來讀等於摘要嗎？/ Long form: numbered sections? Headings-as-summary?
- [ ] 用對語言軌了嗎？中文別套英文規則，反之亦然。/ Right language track? Don't cross-apply the rule sets.

## 3. 什麼時候不要白話化 / When not to do this

- **規格書、spec、給程式讀的格式**：精確 > 好懂，別動。
  **Specs and machine-read formats**: precision beats readability. Leave them alone.
- **法律／合約／隱私政策**：用字有法律效果。改寫要標註「這是白話版，非正式條文」。
  **Legal text**: wording has legal effect. Mark any rewrite as an unofficial plain-language version.
- **用戶明確要原文或要技術細節**時。/ When the user asked for the original or for full technical detail.
- **對方是專家、術語是共同語言**時：白話化反而是雜訊。
  **Expert-to-expert**, where the jargon is shared vocabulary: plain language is just noise.

判準：問「讀者是誰、他要拿這段做什麼」。要**做決定** → 白話。要**照著實作** → 精確。
The test: who reads this, and what will they do with it? Deciding → plain. Implementing → precise.
