---
name: backtest-report
description: Run the minute-level backtest pipeline for Taiwan stocks and futures tickers (e.g. 0050, 2330, 00631L, TXF) — sliding-window robustness analysis, per-window top-10 ranking, average-ROI analysis — and upload the markdown report to a fresh gist. Supports specifying ticker(s), date range, and window size. — sliding-window robustness analysis, per-window top-10 ranking, average-ROI analysis — and upload the markdown report to a fresh gist. Supports specifying ticker(s), date range, and window size. Also lists a single strategy's explicit buy/sell trade ledger (`engine/intraday.py --trades`). Use when the user asks to "跑回測報告", "run the backtest report", "回測 <股票代號>", "更新 gist 的回測結果", "/backtest-report …", or wants a strategy's "買賣明細 / 交易紀錄 / 進出 / trade ledger" (for that, first ask which strategy), or similar.
tags: [backtest, trading, sliding-window, gist, stock, ticker, futures, TXF]
---

# 逐分鐘回測報告（指定股票代號 + 自動跑 + 上傳 gist）

一鍵跑完整的逐分鐘回測報告流程（全部分鐘版），**可指定一或多個股票代號**：

1. **滑動窗格穩健性分析**（`analysis/sliding_window.py`，逐分鐘 + 全核心）→ 產 `window_min_*.csv`
2. **單一合併報表**（`analysis/window_top10.py`）：頂部=各策略平均 ROI 分析、中段=每窗前十名、底部=滑動窗格彙總
3. **上傳全新 gist**（用 `~/.hermes/.env` 的 `GITHUB_TOKEN`，需 gist scope）

## 怎麼執行

專案在 `/home/chihmin/backtest-strategies/`。**用 `--tickers` 指定股票代號**：

```bash
cd /home/chihmin/backtest-strategies
python3 report/run_report.py --tickers 0050            # 單一代號
python3 report/run_report.py --tickers 0050 2330 00631L # 多個代號（每個一份報表，同一 gist）
```
不帶 `--tickers` 時預設 0050。每次都建**全新 secret gist**，印出連結。

### ⚠️ 指定的代號若還沒有資料，要先抓
報表只讀 `data/{代號}_minprice_*.csv`。若使用者指定的代號還沒抓過（runner 會報
「找不到 {代號} 的分鐘價資料」），**先抓再跑**：

```bash
/home/chihmin/sj-trading/.venv/bin/python datafetch/get_minute_price.py <代號> 2020-01-01 2026-05-31
```
抓完**務必檢查分割**（掃單日跳動 >15%，或查 FinMind TaiwanStockSplitPrice）：若該代號有分割，
要在 `core/backtest_minute.py` 的 `SPLITS` 登記 `{代號: [(日期, 倍數)]}`，否則分割會被當成真實暴跌
（例：00631L 22:1 未登記時 AllIn 全期複利會錯成 -80%）。登記後再跑 run_report。

### 台指期貨（TXF）

台指期也可用同樣流程抓分鐘 K 並跑回測。代號用 `TXF`。

```bash
# 抓台指期分鐘 K（需 shioaji venv）
/home/chihmin/sj-trading/.venv/bin/python datafetch/get_minute_price.py TXF 2020-01-01 2026-05-31
```

抓完產出 `data/TXF_minprice_YYYY-MM-DD_YYYY-MM-DD.csv`，跑回測時用 `--tickers TXF` 即可。

⚠️ 台指期抓資料的程式碼已存在於 `datafetch/get_minute_price.py`，但**此 Skill 不硬編碼任何 API key**。執行前請確認環境變數或 `~/.hermes/.env` 內有 Shioaji 金鑰（`SIMULATION_API_KEY` / `SIMULATION_SECRET_KEY` 或正式 `API_KEY` / `SECRET_KEY`）。若金鑰遺失或過期，需手動補充後再執行。

### 變化用法

```bash
python3 report/run_report.py                       # 預設：跑 0050 + 建「全新」gist
python3 report/run_report.py --tickers 0050 2330   # 多個標的！每個一份報表，全放同一個 gist
python3 report/run_report.py --start 2020-01-01 --end 2023-12-31   # 限定時間區間
python3 report/run_report.py --window 6 --step 2                    # 窗格6個月、每次滑2個月（預設 3/1）
python3 report/run_report.py --no-upload           # 只跑分析、產 markdown，不上傳
python3 report/run_report.py --update              # 更新既有預設 gist，而非建新的
python3 report/run_report.py --gist-id XXXX        # 更新指定 gist
```

**多標的**：`--tickers` 可給一或多個代碼（如 `0050 2330`），每個標的輸出一份
`{ticker}_backtest_report_MINUTE.md`，全部上傳到同一個 gist。前提是該標的的分鐘資料已存在
（`data/{ticker}_minprice_*.csv`）；沒有的話 runner 會報錯並提示用 `datafetch/get_minute_price.py` 先抓。
標的若有分割，需在 `core/backtest_minute.py` 的 `SPLITS` 登記表加上 `{ticker: [(日期, 倍數)]}`。

## 個股策略買賣明細（使用者要「明細 / 買賣紀錄 / 某策略進出」時）

不是跑整份報告，而是列出**單一策略**的逐筆買賣：

```bash
cd /home/chihmin/backtest-strategies
python3 engine/intraday.py --trades "<策略名>"                 # 全期間
python3 engine/intraday.py --trades "<策略名>" --last 1y       # 限定區間（也接受 --start/--end）
python3 engine/intraday.py --trades "<策略名>" --fills         # 逐筆攤開每一次成交
```

- **一定要先問使用者要哪個策略**（名稱含空白要加引號，如 `"MA 20/120"`）。不確定有哪些 →
  先 `python3 engine/intraday.py --list` 列出 29 種給他挑。找不到策略時 runner 會印可用清單、不會 crash。
- 輸出＝回合交易表（進場/出場/損益/持有天）+ 未平倉部位 + 摘要（勝率/平均持有/已實現損益）。
- `--start/--end/--last` 會把回測切到該區間、用 100 萬重新起跑（與整個沙盒一致）。
- 這條路只跑單一策略、**不產 gist**；回給使用者時直接貼表格即可（Discord 用 reply）。

## 執行後要回報的內容

跑完後，把以下重點回報給使用者（若來自 Discord，用 reply 工具）：
- gist 連結（輸出最後一行的 `https://gist.github.com/...`）
- 滑動窗格前 3~5 名策略（從步驟 1 的終端輸出擷取）
- 是否有異常（任何步驟 exit code 非 0，runner 會直接中止並印出失敗的指令）

## 注意事項

- **全程逐分鐘**：日線引擎已移除，三個分析工具一律逐分鐘。
- **資料需就緒**：依賴 `data/{代號}_minprice_*.csv`（0050 約 40 萬列分鐘 K，TXF 約 79 萬列）。若檔案不存在，要先用 `datafetch/get_minute_price.py`（需 shioaji venv）重抓。
- **金鑰**：`GITHUB_TOKEN` 從 `~/.hermes/.env` 讀，只需 gist 權限。**不要把任何 API key（Shioaji、FinMind 等）寫進此 Skill 檔或輸出到終端**。抓資料的金鑰由 `datafetch/get_minute_price.py` 從環境變數讀取，本 Skill 不觸及金鑰管理。
- **金鑰**：`GITHUB_TOKEN` 從 `~/.hermes/.env` 讀，只需 gist 權限。不要把 token 印到終端或對外傳。
- **耗時**：滑動窗格逐分鐘約 1 秒（全核心）、其餘各約數秒，整體很快。
- gist 預設是 **secret**（非公開，但有連結的人看得到）。
