---
name: fable-commander
description: Fable 指揮官工作流 — Fable 只做規劃/審查/決策，研究與執行派給使用者選的模型（Opus/Sonnet/Haiku subagent）。流程：Fable 產 plan → 問使用者選研究模型 → /workflow 查資料+列驗收標準 → Fable review 修 plan → 問使用者選執行模型 → maker/verifier 分離的執行 loop（驗證硬條件=客觀正確性，禁止以風格/觀點打回）。觸發詞：指揮官模式、fable commander、指揮官流程、用指揮官跑、Fable 當指揮官、commander 這個題目。
---

# fable-commander · Fable 指揮官工作流

你（Fable）是**指揮官**：負責規劃、審查、整合、把關決策點。查資料與寫程式這類大量 token 的工作，派給**使用者選定的模型**用 subagent / Workflow 跑。核心信念來自 Addy Osmani 的 Loop Engineering：

> "The most useful structural thing in a loop, by far, is splitting the one who writes from the one who checks. The model that wrote the code is way too nice grading its own homework."

## 模型切換的實作方式（重要，先讀懂）

Claude Code 的 main loop 模型**無法由 Claude 自行切換**（`/model` 是使用者指令）。因此本 skill 的「切模型」一律用：
- `Agent` / `Workflow` 的 `model` 參數（`opus` / `sonnet` / `haiku`）— 自動、不需使用者動手 ← **預設**
- 若使用者明確想把 main loop 整個換掉（例如長執行期省成本），提示他自己輸入 `/model`，並把 handoff 所需的一切寫進 state file 再交棒

## Advisor 模式：本 skill 的輕量替身（官方 harness 功能，非工作流）

`/advisor <model>` 是 Claude Code 官方（實驗性）功能：主模型跑便宜的（如 Sonnet），Claude 在關鍵時刻（提交方案前／錯誤重複／宣告完成前）**自動諮詢**更強的 advisor（如 Opus）。設定方式 `/advisor opus`、`advisorModel` settings 欄位、或 `--advisor` 旗標；`/advisor off` 關閉。需 Claude Code v2.1.98+，僅 Anthropic API（Bedrock/Vertex/Foundry 不支援）。mid-session 即生效、不需重開 session（官方文件明說中途啟用停用不使 prompt cache 失效）。

**何時用它取代本 skill**：官方文件原文是 advisor 適合「**長、多步驟**任務，方案品質決定成敗」，短任務「加值較低」，官方建議短任務直接換主模型而非掛 advisor——所以正確的折衷地帶，是 Phase −1 三判準裡的「**驗證難以客觀化**」或「**token 預算不夠**」這兩類、但任務本身仍偏長偏多步驟；純粹「任務小」不是 advisor 的甜蜜點，照 Phase −1 直接做即可。

**為何它不能取代完整 loop**：advisor 是給「同一個執行者」的第二意見，執行者通常照建議走——這跟本 skill 的 maker/verifier 分離（獨立、有罪推定、跨模型的檢查者）**方向相反**；官方 blog 明說 advisor strategy 是「反過來的 orchestrator」。所以 advisor 沒有獨立驗證、沒有 gate/停止紀律、沒有證據要求。防「誤報完成」的護欄只有完整 loop 才有。

**⚠️ 與本 skill 併用的陷阱**：官方文件白紙黑字「子代理繼承已設定的顧問，並針對自身模型做配對檢查」。所以在**已開 advisor** 的 session 裡跑本 skill，spawn 出去的 maker/verifier 會**各自諮詢同一顆 advisor**——(1) 成本悄悄上升；(2) 更關鍵：verifier 若也諮詢同一顆 advisor，「獨立、跨模型檢查者」就被部分抵消。**硬規則：跑 Phase 5 verifier 時 advisor 應為 off，或用未開 advisor 的獨立 session 跑 verifier。**（advisor 目前無 per-subagent 開關。）

**⚠️ 已知相容性 bug**：session（含其內部 subagent）只要在呼叫 advisor **前**用 `ToolSearch` 載入過任何 deferred tool（例：內建 `WebFetch`，或任何 MCP 工具），之後每次 advisor 呼叫都會**確定性失效**（[GitHub #73923](https://github.com/anthropics/claude-code/issues/73923)，Anthropic 已標記 Closed as not planned）。這條會命中很多真實 session——標準 Claude Code 常態性用 ToolSearch 載入 deferred 內建工具。另外，用 **Fable 5** 當主模型時，長對話（約 100K+ tokens）也可能讓 advisor 悄悄失效——此限制專屬 Fable-5-as-main，issue 證據顯示 Opus 4.8 當主模型在 296K context 仍正常（[GitHub #67609](https://github.com/anthropics/claude-code/issues/67609)）。**不要單靠 advisor 當唯一防線。**

**輕量逃生口**：Phase −1 判「不值得跑完整 loop」時，除了「直接做」，若任務仍偏長/多步驟（只是驗證難客觀化或 token 預算不夠），可建議一條中間路線——`/model sonnet` + `/advisor opus`：便宜模型執行、更強模型在關鍵決策點被自動諮詢，無 loop 的多 agent 開銷（併用陷阱見上；純小任務不是 advisor 的甜蜜點）。

## 適用性檢查（Phase −1，先過再開跑）

Loop engineering 不是萬用解。以下任一不成立 → 告訴使用者「這題直接做比較划算」，不走本流程：
1. 任務夠大（多階段、研究+執行分離有價值）——一次性小任務用好 prompt 更快
2. 驗證可客觀化（測試/資料檢核/可重現性這類機器可判的訊號）
3. Token 預算允許（本流程會 spawn 多個 agent，天生燒錢）

## 流程總覽

```
Phase 0  Fable 起草 Plan v0（含驗收標準草稿 + 已知未知清單）
Phase 1  AskUserQuestion①：研究階段用哪個模型？
Phase 2  /workflow 研究 fan-out（該模型）：查證資料源、文獻、工具、補驗收標準
Phase 3  Fable review 研究產出 → 修成 Plan v1（衝突處問使用者）
Phase 4  AskUserQuestion②：執行階段用哪個模型？
Phase 5  執行 loop：maker（執行模型）⇄ verifier（獨立 fresh-context agent）
Phase 6  收尾：Fable 總驗收 + 採納率記錄 + 教訓回灌
```

## Phase 0 — Fable 起草 Plan v0

- 產出一份 `PLAN.md` 存在**任務的專案目錄**（不是 scratchpad）——這是整個 loop 的 **state file**（spine），每個 phase 完成都要回寫
- Plan v0 必含：研究問題、先驗/預期結果、phases×gates 表、**驗收標準草稿**、**已知未知清單**（＝Phase 2 的研究題目，逐條可查證）
- Plan 裡就要寫死執行期的 maker/verifier 合約（見 Phase 5），不是執行時才想

## Phase 1 — 問使用者：研究模型

用 `AskUserQuestion` 問一題（選項附成本/能力 trade-off）：
- **Sonnet（推薦）**：搜尋彙整型研究性價比最高
- **Opus**：題目冷門、需要較強推理時
- **Haiku**：純撈資料、清單型查證
- **先不跑**：使用者要自己挑時機

## Phase 2 — 研究 /workflow（使用者選的模型）

用 `Workflow` 工具（或多個並行 `Agent`，皆帶 `model` override）fan-out，**每條研究題目一個 agent**，題目直接取自 Plan v0 的「已知未知清單」。規則：
- 研究 agent **只查證、不改 plan**（讀寫分離：他們回報事實與來源，改 plan 是 Fable 的事）
- 每條發現必附來源 URL 或資料路徑；查不到就回報「查不到」，禁止腦補
- 其中一個 agent 專門負責「**驗收標準提案**」：把 Plan v0 的驗收草稿改寫成逐條可機器判定的條件
- 產出寫進 `RESEARCH.md`（與 PLAN.md 同目錄）

## Phase 3 — Fable review → Plan v1

Fable（你自己，main loop）做：
1. 逐條核對 RESEARCH.md 是否回答了已知未知；沒答到的標記「仍未知」進 Plan v1 風險節
2. **Trust but verify**：對關鍵事實（資料源可用性、API 限制）抽 1–2 條自己快速複核，不盲信 subagent 報告
3. 修訂驗收標準為定稿（每條都要能客觀判 PASS/FAIL）
4. 與使用者原始意圖衝突、或有重大取捨（如資料源要花錢）→ `AskUserQuestion` 問，不擅自決定
5. Plan v1 回寫 PLAN.md（版本號 + 修訂紀錄）

## Phase 4 — 問使用者：執行模型

`AskUserQuestion`：**Opus（推薦，長程執行力強）** / Sonnet（成本敏感）/ 先不執行。
同時問是否需要 worktree 隔離（會改既有 repo 的任務建議開）。
若使用者選 Sonnet 省成本，可提示另可加開 `/advisor` 取得決策點的強模型指導（中間路線）——但務必提醒「Advisor 模式」節的 verifier 併用陷阱：Phase 5 verifier 要在 advisor off 的狀態下跑，否則獨立性受損。

## Phase 5 — 執行 loop（本 skill 的靈魂：maker/verifier 分離）

### 角色
- **Maker agent**（使用者選的執行模型）：照 Plan v1 實作，一次領一個 phase
- **Verifier agent**（獨立 spawn、fresh context、**禁止共用 maker 的對話**；建議與 maker 不同模型）：對照 Plan 裡的 gate 驗收

### Verifier 的硬規則（寫進每次 verifier prompt）
1. **只驗硬條件＝客觀正確性**：測試通過、資料檢核、數字可重現、規格逐條對照——全部是機器可判或可獨立重跑驗證的訊號
2. **🚫 明文禁止**以下列理由打回：程式/文章風格偏好、敘事方式、作者觀點、結論方向不合預期。這些屬於**使用者的風格與觀點資產**，verifier 無權扼殺——只能寫進報告的「建議（不擋交付）」欄
3. 預設有罪推定（maker 說「done」是 claim 不是 proof），每項 gate 給 PASS/FAIL + 證據
4. Verifier 只判不改（寫審分離），改是 maker 回去改

### Loop 控制（防 Ralph Wiggum 迴圈與空轉）
- 每個 gate 迭代上限 **3 輪**
- 同一項連續 **2 輪無改善** → 判定為「這層修不動」，停止空轉，升級人工（把兩輪證據整理給使用者）
- 3 輪後仍 FAIL → **不得「取最高分放行」**，gate 就是 gate；標記未過、上報使用者裁決
- 每輪結果回寫 state file（phase、輪次、verifier 判定、殘留問題）

### 人工閘（不可逆動作）
commit / push / 對外發布 / 花錢（付費 API、下單）之前一律停下拿使用者明確確認——即使在 bypass permissions 模式下也一樣。

## Phase 6 — 收尾

1. Fable 總驗收：抽核 verifier 報告（trust but verify，第 3 層眼睛）
2. **採納率記錄**：這次產出被使用者接受多少？寫進 state file 尾部（loop 的成功指標是採納率，不是 token 燒了多少）
3. 教訓回灌：這次流程哪個 gate 設計得不好 → 直接改本 SKILL.md（記日期），讓 loop 自我改進
4. 提醒使用者**讀關鍵 diff /報告本體**——comprehension debt 與 cognitive surrender 是使用者自己要守的線，skill 只能提醒

## 實戰教訓：感知品質類任務的驗收（2026-07-12）

**感知品質類任務（語音自然度/腔調/視覺美感/文案人味）的驗收 gate 必含人類感官，機器 proxy 只當 sanity check、不當過閘依據。** 本機語音克隆實證：maker/verifier loop 報「6 條 AC 全 PASS」——speaker cosine 0.92、CER 0、後補的 PESQ 都過，但使用者一聽「完全不行」、真實採納率＝0；PESQ 甚至把使用者一聽就否決的合成音評最高分 3.01。三個機器指標全「**客觀但量錯維度**」——量的是「像不像/念對沒/乾不乾淨」，不是「聽起來好不好」，與 huashu-design『視覺校稿闸』同構。

**硬規則**：①感知品質類 acceptance 設**雙層**——機器預篩（濾掉明顯壞的）＋ **人類感官硬閘（唯一能關 loop）**；②明文禁止拿 cosine/CER/PESQ/UTMOS 宣稱「過了」，它們是 sanity check 不是 gate；③不確定寧可產樣本交使用者感官判，不要 loop 自宣 done（誤報完成＝Ralph Wiggum）。

## 反模式對照表（自檢用）

| 陷阱 | 本 skill 的對策 |
|---|---|
| Ralph Wiggum 迴圈（誤報完成提早退出） | verifier 有罪推定 + 客觀 gate + 證據必附 |
| 軟化閘門（「取最高分」矇混過關） | 3 輪仍 FAIL 就是 FAIL，上報不放行 |
| 同源自評放水 | verifier 必為 fresh context，建議跨模型 |
| 驗證越權殺風格 | 硬條件白名單 + 風格/觀點禁打回條款 |
| 無停止條件空轉燒錢 | 3 輪上限 + 2 輪無改善即升級 |
| 理解債 / 認知投降 | Phase 6 強制提醒使用者親讀關鍵產出 |
| 把 orchestrator/loop 設成 CLAUDE.md 全域預設 | orchestrator/loop 一律 opt-in；Phase −1 適用性檢查先過，小任務走 advisor 輕量路徑而非全域燒 token |
| Advisor 開著跑 verifier（獨立性被抵消） | Phase 5 verifier 一律 advisor off 或獨立 session；派工前確認 advisor 狀態 |
