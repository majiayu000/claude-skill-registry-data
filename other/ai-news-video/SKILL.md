---
name: ai-news-video
description: 抓取本週 AI 新聞並產出 4-7 分鐘 YouTube 影片配音腳本 + 投影片 + mp4（繁體中文台灣用詞）。從 15+ 來源廣掃 30+ 候選，**按議題群整合（5-8 個 cluster）而非選 3 則單一新聞**，預設 ElevenLabs Tiffy_TW 1.7× 配音 + 黑底橘色 accent 投影片。觸發詞：「AI 週報」「跑週報」「本週 AI 新聞」「產 YouTube 腳本」「整理本週新聞」。使用者經營不露臉 AI 新聞頻道時務必使用此 skill。
---

# AI Weekly News → YouTube Script + Video

產出一支 **4-7 分鐘** 不露臉 YouTube 影片的完整素材（腳本 + 配音 + slides + mp4），主題是本週 AI 圈所有值得看的事。

**核心心法（W22 後校準）**：
- **整合不是篩選**：本週候選通常 30-50 則，同主題多家媒體會報導同一件事，要 **cluster 成 5-8 個議題群**再講，不是硬挑「最重要 3 則」
- **深度 > 數量**：每個議題群要有「發生什麼 / 為什麼這事重要 / 對台灣的意義」三層，避免「掃過去」
- **影片時長 4-7 分鐘**：太短像 shorts、太長觀眾跳出。1.7× 語速、~2000-2500 字稿、約 4-5 分鐘是甜蜜點
- **完整 pipeline 已封裝**：所有步驟對應一個 Python script，不要重發明輪子

---

## 執行流程

### Step 0：DB init check（每次必跑）

確認 SQLite DB 已就緒：

```python
import sqlite3
from pathlib import Path
DB = Path.cwd() / ".handover" / "handover.db"
if not DB.exists() or not sqlite3.connect(DB).execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='ainews_sources'"
).fetchone():
    raise SystemExit("DB 未建好，先在專案根目錄跑 `python init_db.py`")
```

DB schema 詳見 `schema.md`（7 個 `ainews_*` 表 + 1 個 ainews_clusters 議題群表）。**所有 fetch / 候選 / cluster / 腳本一律寫進 DB**，markdown 檔僅作為人類可讀鏡像。

### Step 1：本週時間範圍

- 今天日期 → 計算本週週一(含)到今天的範圍 → `WEEK_RANGE`
- 計算本週是該年度第幾週：`f"{y}-W{w:02d}"`（例 `2026-W22`）
- 若週中跑（週三以前），照樣跑「本週至今」，不要硬等到週日

### Step 2：廣掃 15+ 來源，目標候選池 30+

**從 DB 撈所有 enabled=1 來源**：

```sql
SELECT id, name, url, fetch_strategy
FROM ainews_sources
WHERE enabled = 1
ORDER BY tier, id;
```

目前 enabled 的來源涵蓋（**v3.1 後新增「release notes」類**）：

- **官方 blog**：Anthropic / OpenAI / Google DeepMind / Meta AI / xAI / Microsoft AI / Mistral
- **官方 release notes（追新功能用）**：Anthropic Claude Apps / Anthropic API / Anthropic Claude Code / OpenAI ChatGPT / OpenAI Models / Gemini API Changelog
- **模型追蹤**：LLM Stats AI News / LLM Stats Model Updates / Artificial Analysis（benchmark 排行）/ Hugging Face Blog / Hugging Face Papers
- **聚合器**：Hacker News / AI News by Smol(Swyx)
- **科技媒體**：TechCrunch AI / The Verge AI / Maginative
- **社群**：Reddit r/LocalLLaMA / r/singularity

**特別說明**：Step 4.5 的「Claude / GPT 新功能 slot」優先讀**官方 release notes 類**（docs.anthropic.com / help.openai.com / ai.google.dev），這些是一手且有版本號 / 日期，比依賴 TechCrunch 二手解讀準確得多。

**同一個 message 內** 把所有 `webfetch` 來源平行打。`search_first` 來源（OpenAI、Google DeepMind 等 SPA 站）改走 WebSearch 找入口。

**Fallback**：任一來源 403 / SPA 空頁 / 區域擋（xAI、Reddit、部分 US-only）→ 直接 WebSearch 補位：
- `<source> announcement <WEEK_RANGE>`
- 額外補抓「戲劇性」題材的 search：`AI lawsuit OR layoff OR scandal <WEEK_RANGE>`、`AI startup funding <WEEK_RANGE>`、`open source LLM release <WEEK_RANGE>`、`AI demo viral <WEEK_RANGE>`

**每次抓完寫 fetch_log + 更新 source 健康度**：

```sql
INSERT INTO ainews_fetch_log (source_id, strategy, http_status, items_extracted, duration_ms, error_msg) VALUES (?, ?, ?, ?, ?, ?);
UPDATE ainews_sources
   SET total_attempts = total_attempts + 1,
       total_hits     = total_hits + :hit,
       success_rate   = CAST(total_hits + :hit AS REAL) / (total_attempts + 1),
       last_fetched_at = datetime('now')
 WHERE id = :source_id;
```

success_rate 長期偏低（< 0.3）的來源，提示使用者考慮關閉。

### Step 3：寫候選進 DB（每則三軸評分）

每則新聞 INSERT 進 `ainews_items`，**用三個維度評分**而非單一重要性：

```sql
INSERT OR IGNORE INTO ainews_items
    (week, source_id, title, url, published_date, summary,
     importance_score, drama_score, visual_score, category, status)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'candidate');
```

**三軸評分（1-5）**：

| 維度 | 看什麼 |
|------|--------|
| **importance**（重要性） | 對開發者 / 企業的長期影響、產業結構性變化 |
| **drama**（戲劇性） | 衝突、爭議、人事鬥爭、訴訟、Twitter 口水戰、模型翻車——好看的料 |
| **visual**（視覺潛力） | 有沒有 demo 截圖 / benchmark 圖表 / 產品 UI 能放進影片 |

**category** 從 [model_release / acquisition / policy / tooling / research / business] 擇一（schema 限制，drama 性質的 fallback 到 business 或 policy）。

**自動排除**：純預印本論文（除非已被三大廠採用）、純財務新聞（無策略意涵）、與 AI 無直接關聯的科技新聞。

**目標**：本週 INSERT **至少 30 則** 進 candidates。15 來源平行掃，正常一週都能達標。少於 20 則 → 表示掃得不夠，補搜尋。

### Step 4：Cluster 成 5-8 個議題群（核心步驟）

**這一步是 W22 後的關鍵改動，取代舊版「選 3 則」。**

從 candidate 中**找同主題的歸成一群**：

- Anthropic 估值 + Karpathy 跳槽 + Q2 營收 → 同一個議題群「Anthropic 全面爆發」
- Google Eyewear + Google Search 改版 + Gemini Omni → 同一個議題群「Google I/O 後續三連發」
- Intuit 裁員 + ClickUp 裁員 + AI 創造力研究 → 「就業衝擊」
- DDG +30% + Uber 質疑 ROI + YouTube 標 AI → 「反 AI 浪潮」

**目標 5-8 個議題群**。每個議題群：
- 一個簡短的核心命題（如「Anthropic 全面爆發」）
- 含 3-8 則 candidate items
- 一個主標 + 一個次標
- 涵蓋的子事件清單

**寫進 DB（ainews_clusters 議題群表）**：

```sql
INSERT INTO ainews_clusters (script_id, position, title, subtitle, narrative)
VALUES (?, ?, ?, ?, ?);
```

未選入任何 cluster 的 candidate 仍可在「未選入但達標」清單中提及，做為 Shorts 延伸題目。

**選議題群的優先順序**：
1. **戲劇性 + 重要性都高**的議題（會吸引觀眾停留）
2. **同週多家媒體報導**的（自然形成 cluster，新聞密度高）
3. **能用具體數字 / 對比表達**的（slide 好做）
4. 避免議題群之間主軸重複

若該週新聞密度低（<20 candidates），改成 4-5 議題群即可，每群更深。

### Step 4.5：固定保留位 ── Claude / GPT 新功能 ＆ 新概念（v3.1 校準）

**使用者明示在意這塊**：每週 8 個議題群中，**至少 1 個 slot 留給「Claude / GPT / Gemini 三大模型本週的新功能、新功能、新概念」**，即使該週其他新聞更勁爆。

理由：使用者是 Claude 重度用戶 + 標案 SA，對「我現在能拿來用的新工具」最有感。純商業 / 地緣 / 倫理新聞他能看，但**功能更新是他工作日常會用到的料**。

**判斷標準**：
- ✅ 必選：Claude / ChatGPT / Gemini 新模型發布、新功能上線、新 API、新介面、新概念框架（例如 Anthropic MCP、OpenAI Operators、Google Spark agent）
- ✅ 必選：三大廠官方部落格本週的 product release / feature announcement
- ⚪ 可選：對手家功能跟風（例如 Anthropic 跟 OpenAI 出類似功能）→ 比較性更好
- ❌ 不算：純財報、組織重整、人事流動（這些歸「商業」議題群）

**slot 命名**：「**Claude / GPT 本週新功能**」或「**三大模型本週重點**」（依當週密度命名）。

**內容深度**：跟其他議題一樣的「事實 ＋ 我認為」雙層結構。「我認為」段重點放：
- 這功能我會怎麼用？對台灣標案 / 開發工作有什麼具體幫助？
- 這個新概念是創新還是 catch-up？

**例外**：若該週三大廠都沒新功能（罕見），這個 slot 可改成「**本週開源 / 第三方工具值得試的**」（HuggingFace 熱榜、Cursor / Cline / Aider 更新等）。

### Step 4.6：固定保留位 ── AI 資安攻防雙線（v3.2 校準）

**使用者明示在意這塊**：每週至少 1 個 slot 留給「**AI 資安攻防雙線**」，整合本週「防（defense）」跟「攻 / 風險（offense / risk）」兩面新聞。

**理由**：使用者是 SA + ISMS 稽核 + 政府標案實戰人員，AI 對資安帶來的衝擊（攻防雙向）是他工作必修課，純技術 / 商業新聞蓋不到這塊。

**判斷標準**：

| 維度 | 內容類型 |
|------|----------|
| **防（DEFENSE）** | Claude Security / GPT Guardian 類安全產品上線、資安平台整合（CrowdStrike / PaloAlto / Okta / Wiz / Fortinet 串接）、AI 紅隊 / 漏洞掃描、AI 模型自報安全強化 |
| **攻 / 風險（OFFENSE / RISK）** | AI 助長詐騙 / 釣魚、prompt injection 漏洞、AI 幻覺造成法律/醫療誤判、員工不當使用 AI 洩密、deepfake 攻擊、AI 模型被 jailbreak 翻車 |

**slot 命名**：「**AI 資安攻防雙線**」或「**本週 AI security**」。

**slide 視覺結構**（沿用 W22 v4 模板）：
- **左欄綠色「防 DEFENSE」**（color `#4ade80`）：列 3-5 個正面進展
- **右欄紅色「攻 / 風險」**（color `#ef4444`）：列 3-5 個風險/翻車事件
- 下方橘色「我認為」框

**「我認為」段重點放**：
- 對台灣 ISMS 稽核要新增什麼題目？（SBOM、模型來源、員工 audit log 等）
- 標案資安附冊要怎麼補 AI 條款？
- 跟使用者熟悉的 fortigate / web-sqa skill 怎麼對接？

**例外**：若該週資安新聞密度極低（罕見），slot 可降為「**本週合規 / 法律動態**」，仍歸納在同一 slide。

### Step 5：寫腳本（議題群結構，非 3-pick 結構）

**腳本目標 1800-2500 字** （TTS 1.7× 後 4-5 分鐘）。**直接寫純配音用的 voice.txt**，不要 markdown header（TTS 不會念）。

結構：

```
[開場 100-150 字]
本週 AI 圈炸了 N 件事，全部串成同一個故事：[一句總結軸線]。
這集會把這 N 件事一次串給你，告訴你哪幾條線真正會影響台灣的開發者跟企業。

[每個議題群 200-250 字]
第 X 件，[議題標題]。
（發生什麼，50-60 字）
（為什麼這事重要 / 產業脈絡，80-100 字）
（對台灣 / 對開發者 / 對企業的意義，60-80 字）

[結尾 100 字]
本週的 takeaway 一句話，[整週軸線總結]。
下週看點 [2-3 個]：[具體可追蹤的線索]。
```

**寫完同步寫進 DB**：

```sql
INSERT INTO ainews_scripts
    (week, title_candidates, thumbnail_candidates,
     word_count, duration_sec, file_path, status)
VALUES (?, ?, ?, ?, ?, ?, 'draft');
```

- `title_candidates` / `thumbnail_candidates`：JSON array `json.dumps(arr, ensure_ascii=False)`
- 標題候選 3 個（衝突型、抽象型、單一爆點型各一）
- 縮圖文案候選 3 個（8 字內）
- `duration_sec`：估 `word_count / 5.0`（中文 ElevenLabs Tiffy 1.0× 約 5 字/秒，1.7× 約 8.5 字/秒）

### Step 5.5：腳本結構強制要求（v3 校準）

**每個議題群必須有「事實 + 我認為」雙層結構。** 不只念新聞，要給觀點，否則跟其他頻道無區別。

每個議題群的格式：

```
第 N 件，[議題標題]。

【事實段】120-180 字：
誰、做了什麼、產業脈絡。客觀陳述，不夾帶個人立場。

【我認為】60-100 字：
- 多數人怎麼看（檯面解讀）：例「市場把這當好消息，覺得是 X 的訊號」
- 我認為真正的訊號（檯面下、反差、被忽略的點）：例「但我看到的是 Y，這才是真正會發酵的線」
- 對台灣讀者的具體啟示：例「對台灣的標案 PM 來說，這代表下半年提案要把 Z 寫進去」
```

**slide 視覺區隔**：事實段用一般白字 slide，「我認為」段在 slide 上用 **橘色框 highlight**（`border-left: 8px solid #ff6b35; padding-left: 24px`），跟事實段視覺區隔，觀眾一眼分辨「這是個人觀點不是新聞」。

### Step 5.6：本週快訊牆 segment（v3 必加）

腳本最後（結尾之前）必有「本週其他值得知道」一段。

**目的**：cluster 後感覺只剩 8 個議題，但觀眾要的是「我看完知道本週 AI 圈全貌」的感受。快訊牆補足這個 coverage。

**格式**：150-250 字 ticker style，列 10-15 件本週其他重要新聞，每件一句話帶過（公司名 + 動作 + 數字 / 關鍵字）：

```
本週還有這些值得知道：
OpenAI 發 X、Mistral 開源 Y、AWS 砍 Bedrock 價、NVIDIA 出 Z 晶片、
Cursor 估值翻倍到 $90 億、Perplexity 拿 Apple 投資、
歐盟 AI Act 細則公布、Anthropic Claude 4.7 偷偷上線、
Figma AI 設計師補位、Cohere 裁員 20%、
Vercel v0 推 SaaS 訂閱、HuggingFace 釋出新 leaderboard，
還有 [社群熱議 1-2 件]。
```

**對應 slide**：條列 grid（3 欄 × 4 列 或 4 欄 × 3 列），每格一行小字，30 秒掃過。slide 上方標題「本週其他 12 件 AI 大事」。

### Step 6：跑 pipeline 產 mp4（v3：per-topic TTS 對位）

**v3 重點改動**：不再「一個整段 voice.txt + 平均切 slide」（會導致 slide 跟配音對不上）。改成 **per-topic TTS**：把腳本切成 N 個 segment（對應 N 張 slide，1:1），每 segment 獨立跑 TTS 拿真實時長，slide 用每 segment 精準秒數對齊。

**所有步驟封裝在 `{cwd}` 的 Python script 裡**，依序跑：

```bash
# 1) 切 segment：手動把 voice.txt 拆成 N 段 seg-NN.txt
# 規則：1 segment = 1 slide。例：開場 1 段、議題 A 事實 1 段、議題 A 我認為 1 段、議題 B 事實 1 段...快訊牆 1 段、結尾 1 段
# 放在 output/2026-W22-segments/seg-01.txt ~ seg-NN.txt
mkdir output/2026-W22-segments
# 手動寫 seg-01.txt, seg-02.txt, ...

# 2) per-topic TTS：每個 seg-NN.txt 獨立跑 TTS
python tts_segments.py 2026-W22 B 1.7
# → output/2026-W22-segments/seg-01.mp3 ~ seg-NN.mp3
# 每段印出真實時長（給後面 slide duration 用）

# 3) 寫投影片 HTML（segment 數 = slide 數，1:1 對應）
# 模板：output/ 內已有 2026-W22-slides.html 可參考；「我認為」段用橘色框 highlight

# 4) 渲染 PNG（playwright，1920x1080）
python render_slides.py 2026-W22 11
# → output/slide-01.png ~ slide-11.png

# 5) 縮圖（HTML 在 output/thumbnail.html）
python render_thumbnail.py
# → output/縮圖.png (1280x720)

# 6) 同步合成 mp4（每張 slide 的時長 = 對應 segment 真實秒數）
python build_synced_video.py 2026-W22 11
# → output/2026-W22-配音.mp3（總配音，segment concat 而成）
# → output/2026-W22-影片.mp4 (1080p, ~7 MB / 4-5 分鐘)

# 舊版整段模式（保留為 fallback）：
# python tts_run.py 2026-W22 B 1.7      # 整段一個 mp3
# python build_video.py 2026-W22 11     # 平均切 slide（不精準）
```

**slide-segment 對位原則**：
- segment 數量 **等於** slide 數量
- segment 順序 **等於** slide 順序
- 每張 slide 顯示時間 **等於** 對應 segment mp3 的 ffprobe 秒數
- 「我認為」段拆成獨立 segment（獨立 slide）以方便用橘色框 highlight

**投影片設計規範**（黑底橘色 accent，沿用 W21/W22 模板）：

- **Slide 1（封面）**：標題 + 本週 N 大議題 grid（給觀眾 5 秒掃完知道整集會講什麼）
- **每個議題群 1-2 張 slide**：title 大字 + bullet points 或數字對比
- **倒數第 2 張**：本週 takeaway 一句話（橘色 accent）
- **最後 1 張**：下週預告 + 訂閱呼籲
- 字級：標題 95-130px / bullet 42-48px / footer 20px
- 顏色：背景 `#000` / 主文 `#fff` / accent `#ff6b35` / 次文 `#999`
- 用 `?slide=N` query string 切換顯示（playwright 渲染每張用）

**TTS 預設配置**：
- 聲音：`Tiffy_TW`（voice key `B`，proposal-narration skill 的 voices.yaml）
- 語速：`1.7`（AI 新聞節奏；若使用者覺得太快可降到 1.5）
- ffmpeg atempo 變速不變調

### Step 7：寫 上傳資訊.md + 跑 finalize

產一份 `output/2026-WNN-上傳資訊.md`，包含：

- 標題候選 3 個
- **影片描述**（含 8 個 章節時間戳 + 來源連結，使用者直接複製貼到 YouTube）
- YouTube 標籤
- 縮圖文案候選
- 延伸 Shorts 題目（從 cluster 外的 candidates 撈，4-8 個）
- 上傳檢核 checklist
- 發布後回填 DB 的 SQL

**章節時間戳**：每張 slide 約 `duration_sec / slide_count` 秒，第 N 章節從 `(N-1) * per_slide` 秒開始。

**然後跑 finalize.py 整理資料夾**：

```bash
python finalize.py 2026-W22
```

自動把 output/ 下的散檔搬成：

```
output/
├── 2026-WNN-上傳/          ← YouTube 直接上傳這個資料夾
│   ├── 影片.mp4
│   ├── 縮圖.png
│   └── 上傳資訊.md
└── 2026-WNN-工作檔/        ← 工作素材，留著但不混
    ├── 配音稿.txt
    ├── 配音.mp3
    ├── 投影片.html
    ├── 縮圖.html
    └── slides/
        ├── slide-01.png ~ slide-NN.png
        └── concat.txt
```

finalize.py 同時 UPDATE `ainews_scripts.file_path` 指向新位置。

### Step 7.5：v3 影片時長建議

依本週新聞密度調整議題數，搭配快訊牆，自然落在合理區間：

| 議題數 | 預估時長 | 適用情境 |
|--------|----------|----------|
| 3-4 議題 + 快訊牆 | 3-4 分 | 本週相對平靜（candidate < 20） |
| 5-6 議題 + 快訊牆 | 5-6 分 | 本週新聞普通（candidate 20-40） |
| 8 議題 + 快訊牆 | 6-8 分 | 本週新聞密集（candidate > 40） |

不要為了「議題多顯得用功」硬擠 8 個議題；少而深 > 多而淺。快訊牆已經補足 coverage 的感受。

### Step 8：回報

簡短回報：
- 本週掃了 N 個來源 / M 則 candidate / 整合成 K 個議題群
- 腳本字數 + 預估時長
- 上傳資料夾路徑
- **DB 寫入摘要**：「本週寫入 M 則 items / K 個 clusters / 1 份 script；fetch_log N 筆」
- 詢問：「先看影片，再決定要不要調整哪段？」

---

## 語氣規範（輸出腳本時的硬規則）

### 必須遵守
- 繁體中文、台灣用詞
- 軟體 NOT 软件、影片 NOT 视频、頁面 NOT 页面、檔案 NOT 文件、程式 NOT 程序、伺服器 NOT 服务器、使用者 NOT 用户
- 第一人稱用「我」，不要「小編」「筆者」
- 口語但專業，寫給工程師 / SA / PM 聽

### 禁用詞清單（中國感詞彙）
家人們、兄弟們、絕了、卷、賦能、賽道、打法、抓手、心智、顆粒度、對齊、復盤、引流、痛點、用戶、視頻、軟件、屏幕、博客、雲服務、人工智能

### 禁用句型
- 「大家好歡迎來到我的頻道」
- 「廢話不多說我們直接開始」
- 「記得訂閱按讚開啟小鈴鐺」（使用者最後自己加）
- emoji（腳本是配音稿）
- 過度感嘆號

### 鼓勵的表達方式
- 直接給觀點：「我覺得這件事真正的重點不是 X，而是 Y」
- 點出反差：「乍看是好消息，但對 [某類使用者] 反而是壓力」
- 給具體例子優於形容詞：「快了」→「推論成本降 60%，標案每月省 NT$8000」

### TTS 友善寫法
- 阿拉伯數字 + 中文混用時，給 TTS 念得順的版本
  - 「$900B」念不出來 → 寫「九千億美金」
  - 「3.5 Flash」→ 寫「三點五 Flash」
  - 「20-40%」→ 寫「百分之二十到四十」
- 英文專名直接用英文（ElevenLabs Tiffy 念 Anthropic、OpenAI、Karpathy 等都念得出來）

---

## 累積資產 + 偏好學習

**所有 metadata 都進了 SQLite DB**，markdown 是人類可讀鏡像。半年後：

- 26 份結構化 AI 新聞筆記 + 26 週 DB 紀錄
- 26 × ~7 個 cluster = ~180 個議題群追蹤
- 標題候選累積 = YouTube 標題語感訓練資料
- 可分析「哪些題目我預測對 / 預測錯」

### 偏好回饋一定要寫入 `ainews_preferences`

使用者每次給回饋「以後不要研究類」「第二議題改短」「語氣再口語一點」「不要選純財務」等 → **長期偏好**，UPSERT 進 DB：

```sql
INSERT INTO ainews_preferences (key, value, reason)
VALUES (?, ?, ?)
ON CONFLICT(key) DO UPDATE SET
    value = excluded.value, reason = excluded.reason,
    updated_at = datetime('now'), hit_count = ainews_preferences.hit_count + 1;
```

範例 key：`avoid_category:research`、`prefer_drama_min:4`、`tone:口語化`、`section_length:第二議題=300字`、`avoid_term:賦能`。

**每次跑 Step 4 cluster 之前，先讀 `ainews_preferences`，把偏好套用到議題群排序。**

### 月度回顧 / 預測復盤

每月第一次執行時主動問：「上個月四週的週報要不要彙整成月度回顧？」

```sql
SELECT s.week, s.final_title, s.youtube_url,
       c.position, c.title, c.subtitle
FROM ainews_scripts s
JOIN ainews_clusters c ON c.script_id = s.id
WHERE s.week BETWEEN :start AND :end
ORDER BY s.week, c.position;
```

半年後可主動跑預測復盤：

```sql
SELECT script_id, position, prediction, verified_outcome
FROM ainews_script_picks
WHERE prediction IS NOT NULL AND prediction <> ''
ORDER BY verified_at NULLS LAST, script_id;
```

---

## Pipeline scripts 一覽（{cwd} 根目錄）

| Script | 用途 | 用法 |
|--------|------|------|
| `init_db.py` | 建 7+1 個 ainews_* 表 + seed sources（idempotent） | `python init_db.py` |
| `tts_run.py` | 整段模式：把 voice.txt 轉成單一 mp3（舊版 fallback） | `python tts_run.py 2026-WNN [voice=B] [speed=1.7]` |
| `tts_segments.py` | **v3 主力**：per-topic TTS，每 seg-NN.txt 各跑一個 mp3 | `python tts_segments.py 2026-WNN [voice=B] [speed=1.7]` |
| `render_slides.py` | playwright 把 slides.html 每張轉 PNG | `python render_slides.py 2026-WNN [count=11]` |
| `render_thumbnail.py` | 渲染 1280×720 縮圖 | `python render_thumbnail.py` |
| `build_video.py` | 整段模式：ffmpeg 平均切 slide 合成 mp4（舊版） | `python build_video.py 2026-WNN [slides=11]` |
| `build_synced_video.py` | **v3 主力**：每張 slide 用對應 segment 真實秒數 | `python build_synced_video.py 2026-WNN [slides=11]` |
| `finalize.py` | 整理 output 成上傳 / 工作檔資料夾 | `python finalize.py 2026-WNN` |

新週次直接複製上週的 slides.html 範本當起點改內容，比從零寫快。

---

## 偵錯指引

### WebFetch 全部失敗
網路問題或來源同時改版。改用 WebSearch 為主，通知使用者：「本週直接抓官網失敗，改用 search，內容深度可能略遜。」

### 本週新聞太少（candidate < 20）
不要硬撐。直接問使用者：「本週相對平靜，只有 X 則候選。建議 (1) 收斂到 4 個議題群每個更深 (2) 跳過本週 (3) 加碼一則趨勢分析。」

### 本週新聞太多（candidate > 60）
正常進行，cluster 出 8 個議題群。多出來的在回報中列「另有 X 則達標但未入選，可拍 Shorts 補充」。

### TTS 跑出來破音字
更新 `proposal-narration/references/pronunciation_fixes.yaml`（共用配置），不要在 ai-news-video 本地修。

### ffmpeg PermissionError on Windows
mp3 可能被 Windows 暫時鎖。先 `rm -f output/{week}-配音.mp3*` 再重跑。
