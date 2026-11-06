---
name: kline-structure-chart
description: "Deterministic multi-market (A-share CN / Hong Kong HK / US) candlestick (K-line) technical analysis from real OHLCV data: indicators, swing and candlestick patterns, SMC zones, volume profile, triple-barrier risk levels, a direction-free 15-bar normal volatility range and a plan-replay backtest, rendered as JSON + PNG + offline HTML. Use when the user asks to analyze an index, stock or ETF chart, e.g. 上证指数/沪深300/茅台/600519.SH/小米/00700.HK/恒生指数/NVDA/SPY; 分析K线、走势、技术形态、支撑压力、买卖点、回测或未来区间. Not for fundamentals, news, earnings, real-time order placement, or personalized investment advice."
license: Apache-2.0
compatibility: "Requires Python 3.12+ with Pillow (uv recommended but optional: without uv, create .venv from requirements.txt and run .venv/bin/python), plus network access to Sina / Yahoo / Tencent market-data endpoints. Without live data the scripts exit with [DATA_UNAVAILABLE] instead of fabricating prices."
metadata:
  author: "承鹏 (chengpeng), Qoder Quant Engine"
  version: "6.0.0"
---

# K 线数学结构分析（A股 / 港股 / 美股）

脚本从真实 OHLCV 行情直接计算全部指标、形态、风控点位与未来 15 日正常波动范围，同一份结果输出为 JSON、PNG 和离线 HTML。分析结论只能引用脚本输出，严禁心算、看图猜数，也不得用图像生成模型画 K 线。

## 何时使用 / 何时不用

- **使用**：用户要分析某个指数、个股或 ETF 的 K 线结构、技术形态、支撑压力、触发与失效位、风控计划、历史回测或未来区间。
- **不使用**：基本面、财报解读、新闻事件、资金流向等脚本不计算的内容；替用户下单或给出个性化投资建议。脚本不计算的数据在回答中一律标注"未复核"。

## 运行环境

工作目录为本 `SKILL.md` 所在目录（技能根目录），以下命令均为相对路径。运行期只需要 Python ≥ 3.12 与 Pillow（只用于画 PNG，全部指标与风控计算只用标准库），取行情需要联网。

- **有 `uv`（推荐）**：直接用下文的 `uv run python ...`。首次运行时 `uv` 会按 `uv.lock` 联网安装锁定版本的依赖（必要时自动下载 Python 3.12，不需要 sudo）。
- **没有 `uv`**：技能目录下已有 `.venv` 时，把下文所有 `uv run python` 换成 `.venv/bin/python`（Windows：`.venv\Scripts\python`）；没有 `.venv` 时先执行 `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`（`python3` 须 ≥ 3.12，低于 3.12 时请用户安装 Python 3.12+ 或 uv，不要用 sudo 改系统 Python，也不要把依赖装进系统 Python）。
- 不确定环境是否可用时先运行 `scripts/doctor.py`（用上面同一个解释器），按 ❌ 项的修复建议处理。

若当前 shell 工作目录不在本 `SKILL.md` 所在目录（例如在 Hermes Agent、Claude Code 或 Codex 的用户工作区中调用），请在 `uv run` 中显式传入 `--directory <本SKILL.md所在目录>`（如 `uv run --directory ~/.hermes/skills/kline-structure-chart`、`~/.claude/skills/kline-structure-chart` 或 `~/.agents/skills/kline-structure-chart`；不用 uv 时写成 `<本SKILL.md所在目录>/.venv/bin/python <本SKILL.md所在目录>/scripts/...`），并将 `--output-dir` 设为绝对路径。

## 零、Flash / 轻量模型零失误执行 SOP（4 步闭环，严禁跳步）

使用 Flash 模型（如 Gemini Flash、Claude Haiku、Qwen-Flash、DeepSeek-Chat、GPT-4o-mini 等）执行本技能时，必须严格按以下 4 步流水线操作，**零心算、零改写、零自由发挥**：

1. **先查代码，不凭记忆猜后缀**：只要用户未提供带 `.SH` / `.SZ` / `.BJ` / `.HK` / `.US` 的完整代码，必须先运行 `scripts/resolve_symbol.py`；多候选时原样列出请用户选择。
2. **运行主脚本生成同源产物**：运行 `scripts/analyze_and_forecast.py`，生成 `*_report.md`、`*_result.json`、`*_chart_data.json`、`*_preview.png` 与 `*_dashboard.html`（需要回测时加 `--backtest`）。
3. **原样采用 `*_report.md` 骨架与「直出摘要」**：
   - 回复第一段直接使用 `*_report.md` 第 1 节中的 `- 直出摘要（供 Agent / Flash 模型首段原样引用）`（当 `verdict.risk_veto == true` 时已自动将 `【风控否决】` 置顶）。
   - 正文各节直接复制 `*_report.md` 的表格与点位，**严禁四舍五入或改写任何价格数字**（例如把 `1349.43` 改成 `1349.4` 或 `1350` 会触发价格白名单拦截），**严禁添加报告里没有的概率、胜率或频率数字**。
4. **发出回复前必跑 `lint_response.py` 自检**：将拟发送的中文回复保存到临时文件，执行：
   ```bash
   uv run python scripts/lint_response.py --result artifacts/cn_stock/600519.SH_result.json --response artifacts/cn_stock/reply_draft.md
   ```
   确认输出 `"status": "OK"` 后再发送给用户。

## 一、第一步：名称转代码

用户给的是完整代码（带 `.SH` / `.SZ` / `.BJ` / `.HK` / `.US` 后缀）时跳过本步。用户只说了名称、拼音或不带后缀的代码（"茅台"、"小米"、"腾讯"、"000001"），**必须先查询，不得凭记忆补全代码**：

```bash
uv run python scripts/resolve_symbol.py 茅台
uv run python scripts/resolve_symbol.py 腾讯 --market HK   # 可用 --market / --asset-type 缩小范围
```

| 输出 | 处理 |
| --- | --- |
| `status = RESOLVED` | 直接使用输出里的 `symbol`、`market`、`asset_type`（`command` 字段是可直接运行的命令） |
| `status = AMBIGUOUS` | 把 `candidates` 的名称和代码列给用户，请用户选择；不得替用户挑一个 |
| `[INVALID_ARGUMENT]` 退出 | 搜不到该名称，请用户提供完整代码 |
| `[DATA_UNAVAILABLE]` 退出 | 腾讯证券搜索接口不可用，请用户直接提供完整代码 |

- 数据源为腾讯证券搜索接口，已过滤港股人民币柜台、美股场外粉单、权证牛熊证和场外基金。
- 北交所股票目前搜不到，请用户提供 `.BJ` 代码；港股 ETF 按名称含"ETF"或港交所 ETF/ETP 代码段（`02800~02849`、`03000~03199`、`07200~07599`、`09000~09199`、`09800~09849`）自动识别，其余按股票处理。

## 二、问题类型 → 命令参数

基础命令：`uv run python scripts/analyze_and_forecast.py --market <CN|HK|US> --symbol <代码> --asset-type <index|equity|etf> --output-dir artifacts/<目录>`，再按问题追加参数：

| 用户的问题 | 追加参数 | 说明 |
| --- | --- | --- |
| 看结构、形态、支撑压力、触发与失效位 | 无 | 默认即可 |
| 能不能买、风控计划、止损止盈 | 无 | 读报告第 4 节；风控否决时只给观察位 |
| 买多少股、仓位 | `--account-equity <净值>`，可加 `--max-risk-pct 0.005` | 只在用户给出账户净值时传入；默认单笔风险 1%。`--max-risk-pct` 是**比例**：用户说"最多亏 1%"写 `0.01`，取值 (0, 0.05]，写成 `1` 会以 `[INVALID_ARGUMENT]` 退出 |
| 历史表现、回测、这套规则靠不靠谱 | `--backtest`（慢时加 `--backtest-step 5`） | 生成 `*_backtest.json` |
| 未来几天的波动区间 | `--horizon-bars <N>`（1~60，默认 15） | 只描述幅度，不含方向 |
| 想看更长或更短的图 | `--days <N>`（60~500，默认 120） | 只影响显示，不影响任何计算结果 |
| 复盘某个历史日期 | `--as-of YYYY-MM-DD` | 只用截至该日已收盘的数据 |
| 港股 ETF | 可选 `--asset-type etf` | 常见港交所 ETF/ETP 代码段（02800~02849、03000~03199 等）已自动识别为 ETF 免印花税 |
| 看不复权的原始价 | `--adjustment raw` | 默认个股/ETF 前复权含分红，指数不复权 |
| 换一个对比基准 | `--benchmark <代码>` | 默认 A 股沪深300、港股恒生指数、美股 SPY |
| 用户提供了本地真实行情文件 | `--input <文件> --offline` | 本地文件无大盘数据，质量为 `PARTIAL` |
| 上市前 5 日的新股 | `--ipo-no-limit` | 不设涨跌幅 |
| 同时看几个标的（如上证和创业板） | 每个标的单独运行 | 每个标的单独成段，点位不得混用 |

示例：

```bash
uv run python scripts/analyze_and_forecast.py --market CN --symbol 000001.SH --asset-type index --output-dir artifacts/cn_index --backtest
uv run python scripts/analyze_and_forecast.py --market CN --symbol 600519.SH --asset-type equity --account-equity 500000 --output-dir artifacts/cn_stock --backtest
uv run python scripts/analyze_and_forecast.py --market HK --symbol 00700.HK --asset-type equity --output-dir artifacts/hk_stock --backtest
uv run python scripts/analyze_and_forecast.py --market US --symbol NVDA.US --asset-type equity --output-dir artifacts/us_stock --backtest
```

- 证券简称、A 股 ST/\*ST 标识与港股每手股数自动取自腾讯行情快照；取不到时报告 `quality.notes` 会写明，可用 `--name` / `--st` 手动指定。`--color-scheme` 切换涨跌配色。
- 生产与测试一律禁止合成数据：不传 `--input` 本地真实行情文件时，断网或数据源异常会直接以 `[DATA_UNAVAILABLE]` 退出。
- 环境有问题时先运行 `uv run python scripts/doctor.py`，逐项查看 Python、依赖、中文字体、数据源连通和技能注册。

产物（文件名以标的代码开头）：
- `*_report.md`：按下文"回复契约"组织好的中文分析报告，数字全部取自 `*_result.json`，**回答用户时以它为骨架**。
- `*_result.json`：v6 稳定契约（`schema_version = 6.0.0`），已通过 `assets/analysis.schema.json` 全量校验。字段含义与稳定性规则见 `references/output-fields.md`。
- `*_chart_data.json`：K 线序列、回放快照等渲染数据，只供本技能的图表使用，**不是稳定接口，回答时不要引用**。
- `*_preview.png`：结构推演图，配色随市场（A股/港股红涨绿跌，美股绿涨红跌）。
- `*_dashboard.html`：离线交互看板。
- `*_backtest.json`（传 `--backtest` 时生成）：线上计划逐日回放的成交统计，以及区间样本外覆盖率。

命令行的标准输出是一个 JSON 信封，失败时退出码区分错误类型：

| 退出码 | 标准输出 | 含义 |
| --- | --- | --- |
| 0 | `{"status": "ok", "schema_version", "verdict", "quality", "files"}` | 成功；`files` 是相对 `--output-dir` 的产物文件名 |
| 1 | `{"status": "error", "error": {"code": "INTERNAL_ERROR", "message"}}`（契约自检失败，不写任何产物）；其他未预期异常无信封，stderr 为 Python traceback | 技能内部错误，不是参数或行情问题：告诉用户是技能出错，不要改参数重试 |
| 2 | `{"status": "error", "error": {"code": "INVALID_ARGUMENT", "message"}}` | 代码或参数有误（argparse 自身的参数错误也是 2，但不输出 JSON） |
| 3 | 同上，`code = DATA_UNAVAILABLE` | 真实行情取不到 |
| 4 | 同上，`code = INSUFFICIENT_HISTORY` | 已收盘K线不足：上市太短、`--as-of` 太早，或数据源本次只返回了部分历史（可稍后重试） |

stderr 同时打印 `[CODE] message`。本节列出的命令行参数都是稳定接口。

数据质量不是 `OK` 时，PNG 和 HTML 都会带红色告警横幅与水印。

## 三、运行后必检（按顺序，任一不满足即停止解读）

1. **退出码**：脚本非零退出时不输出任何价位。退出码 3（`DATA_UNAVAILABLE`）表示真实行情取不到，如实告诉用户原因，不得改用合成或估算数据；退出码 2（`INVALID_ARGUMENT`）表示代码或参数有误，退出码 4（`INSUFFICIENT_HISTORY`）表示已收盘K线不足，均按"失败处理"处理；退出码 1（`INTERNAL_ERROR` 或无信封的 traceback）是技能自身的错误，如实告诉用户，不要改参数重试。
2. **`quality.status`**：
   - `UNAVAILABLE` → 不输出任何价位与结论。
   - `PARTIAL` → 回答首段逐条列出 `quality.warnings`，再谨慎解读。
   - `OK` → 正常解读。
3. **`quality.notes`**：逐条转述，例如"某日 K 线未收盘，已排除出计算"、"数据只到某日，最近已收盘交易日的日线数据源尚未提供"、"复权未生效"、"未来日期超出休市表覆盖范围，按工作日估算"。
4. **空值**：`volatility_range.volatility_scaling.vix` 为 `null` 表示没有取得 VIX，不得自行补数。

## 四、回复契约（按此顺序组织回答）

`*_report.md` 已按以下顺序写好，直接据此转述即可：不得改动其中任何数字，不得补充报告里没有的价位；用户追问细节时再查 `*_result.json`（字段字典见 `references/output-fields.md`，解读要点见 `references/interpretation-guide.md`）。

0. **先答所问**：用 1~2 句话、只用报告里的数字直接回答用户的具体问题，再展开下面各部分。
1. **数据说明**：数据源（`meta.data_source`）、截止日（`meta.as_of`）、复权口径（`meta.adjustment`），以及上一步需要转述的告警或备注。
2. **大盘先行**：基准的 `market_context.regime`、`regime_score`，以及个股的 `market_context.relative_strength_vs_index`。
3. **结构与规则**：
   - `verdict.rule_score` 是 0~100 的确定性规则分，不是胜率或概率。`verdict.rule_detail.regime_adjustment.applied = true`（均值回归体制）时，规则分已按反转规则调整、不等于四组分项之和，必须原文转述 `regime_adjustment.note_cn`，不得把调整后的低分说成"多周期空头"。
   - `scenarios` 按"触发条件 → 目标位 → 失效条件"转述：三条主路径 `scenarios.paths`（上攻 / 震荡 / 下探），以及 `scenarios.active` 中 2~5 个适用情景及其状态（`status_cn`：`已在进行中` / `待触发`）。不为情景附加任何频率、用时或概率；`scenarios.contested_levels`（现价附近正在争夺的价位）不作触发条件。
   - 浪型先说主计数，再说 `structure.wave_counts` 里的备选数法及各自的否定条件；备选数法不代表可能性大小。形态为"形态不明确"时不套用教科书形态。
   - 形态只引用 `structure.patterns` 里的 `name_cn` 和 `formula_verified`。
4. **风控**：
   - `verdict.risk_veto` 为 `true` 时，**置顶**列出 `verdict.veto_reasons`，不得给出做多建议。
   - 否则给出 `plan.long` 的入场区、止损（盘中触及硬止损屏障离场，A 股受 T+1 约束自入场次日起生效）、TP1/TP2、时间屏障与 `breakeven_ratchet` 移动保本规则（盘中触及 `+0.90R` 且收盘 `≥ +0.30R` 后，自次日起止损上移至 `+0.08R` 保本位）。
   - **分板块/制度差异化提醒**：
     - **10% 涨跌幅主板 / 港美股大盘股**：结合 `verdict.rule_score`、相对强弱 `market_context.relative_strength_vs_index` 与通道中轨顺势解读；
     - **20% 涨跌幅科创板（`688` 及 `588/589` ETF）/ 创业板（`300/301` 及创业板/双创 ETF）**：日内波动幅度大，不得在偏离 `EMA20` 超过 `2.0 * ATR14` 或 `RSI14 >= 70` 时追高，强调在 `plan.long.entry_zone` 挂单区间内执行，并按 `breakeven_ratchet` 移动保本止损执行风控；
     - **弱市中的「超跌反弹」（`OVERSOLD_BOUNCE`）**：当大盘偏弱或个股处于 `MA60` 下方空头排列时，单凭 RSI 超卖左侧抄底容易遭遇“超卖再超卖”，必须提醒用户等待日线收阳并站上触发位右侧确认。
   - **仓位**：只转述 `plan.long.position_sizing.recommended_shares`（按入场区上沿到止损的距离含交易成本计算）与 `gap_risk_note`（跳空、跌停时亏损可能超出预算）。风控否决或评级不是做多确认/条件观察时该字段为 `null`，转述 `reason`，**不得**自行用风险预算 ÷ 止损距离换算股数。
   - 用户已持有该标的时，转述报告里的"持仓防守计划"（`plan.holder_defense.rules`）。
   - 港股、美股报告带"破位做空计划"（`plan.short`）：转述时必须同时说明卖空限制（`constraints`）、`warnings`，以及盈亏比未计融券费用。A 股与指数没有做空计划（`plan.short.available = false`），卖空限制只按制度手册（`references/cn-market.md`、`references/hk-market.md`、`references/us-market.md`）说明，不得给出报告中没有的做空点位。
5. **未来 15 日正常波动范围**：
   - `volatility_range` 以最新收盘价为中心（`q50_method = MARTINGALE_LAST_CLOSE`），只描述波动幅度，不包含方向判断，不得把 q75/q25 说成看涨/看跌概率。
   - 必须同时给出 `calibration_audit` 的实测覆盖率与 `effective_independent_samples`。
   - `promotion_status` 为 `RESEARCH_CALIBRATION_WARMUP` 时称"校准观察期"，不得把覆盖率说成区间已验证可靠；有效独立样本低于 `min_effective_independent_samples`（20）时不会晋级（判定见 `references/math-patterns.md` 第 5 节）。
6. **回测**（有 `*_backtest.json` 时）：成交笔数、胜率（带 95% 区间）、累计收益与同期买入持有对比；有 `sample_size_warning` 时原文转述。规则分 IC 的结论（`rule_score_ic.verdict`）原文转述，`informative = false` 时说明规则分在该标的上只作描述。
7. **文件**：给出 `result.json` 与 `dashboard.html` 的路径（取自 `files`）；客户端能显示图片时再内嵌 `preview.png`，否则只给路径。
8. **免责声明**：结尾注明"以上为规则化技术分析，仅供研究参考，不构成投资建议"。

## 五、对外表述与概率规则

- `verdict.rule_score`、`market_context.regime_score` 等都是确定性规则打分，**不是**胜率、概率或置信度；Volume Profile 是成交分布近似，不是真实持仓筹码。
- **不输出任何概率、胜率或频率数字。** 唯一例外是 `*_backtest.json` 的回测成交胜率：必须同时给出样本量 n 与 95% 区间，并说明它是这套规则在该标的上已发生成交的统计，不是未来上涨概率。`lint_response.py` 只在同一句同时出现"回测"与"95% 区间"（或"95% 置信区间"）时放行"胜率"这一个数字；命中率、频率、占比等即使同句带区间也会被拦截。
- 不得出现"大概率突破""胜算七成"等等价说法；15 个交易日的方向本身接近随机，推演路径只写"触发条件 → 目标位 → 失效条件"，不承诺涨跌。

## 六、失败处理

| 情况 | 处理 |
| --- | --- |
| `[DATA_UNAVAILABLE]`（退出码 3：网络失败、代码无法映射、限流、数据损坏） | 转述错误原因，请用户核对代码格式或稍后重试；不估算、不改用合成数据。可运行 `scripts/doctor.py` 定位是哪个数据源不通 |
| `[INVALID_ARGUMENT]`（退出码 2：`Cannot resolve market` / `Ambiguous symbol` / 参数越界；argparse 自身的参数错误同为 2，但没有 JSON 信封，只有 stderr 用法提示） | 先用 `scripts/resolve_symbol.py` 查代码，仍不确定就请用户补充交易所后缀，例如 `000001.SH`（上证指数）与 `000001.SZ`（平安银行）的区别；参数越界时改正后重跑 |
| `[INSUFFICIENT_HISTORY]`（退出码 4） | 说明已收盘K线不足、无法计算：可能是上市时间太短、`--as-of` 太早，或数据源本次只返回了部分历史（建议稍后重试一次） |
| 基准指数取不到 | 整次分析失败，按 `[DATA_UNAVAILABLE]` 处理（不得跳过大盘直接分析个股） |
| `quality.notes` 提示复权未生效（如北交所） | 告知价格为不复权原始价，除权缺口可能被误识别 |
| `quality.notes` 提示港股每手股数或证券简称未取得 | 转述该提示；仓位股数按假设值计算，提醒用户下单前向券商核对 |
| `no CJK font found` | 缺中文字体，按 `scripts/doctor.py` 给出的命令安装后重跑 |
| 用户要求下单、预测确定涨跌或给出个性化仓位 | 说明本技能只做规则化技术分析，不替用户交易、不承诺方向 |

## 七、回复示例

以下示例节选自仓库 `examples/` 中用真实行情生成的报告（贵州茅台，数据截至 2026-10-15）。**示例里的数字只用来说明格式，回答时一律使用本次运行的输出。**

用户问："茅台现在能买吗？"

正确的回复开头：

> 风控已否决做多：大盘环境评分偏弱（沪深300 状态分 6.0 < 35），以下点位只用于观察，不构成做多建议。
>
> 数据为新浪日线，截至 2026-10-15，前复权含分红，数据质量 OK。规则分 36.8/100（均值回归体制评分偏空）：近 240 日均线偏离与随后 15 日收益负相关，四组规则分项合计 55.5 经反转调整为 36.8，衡量的是追高风险，不代表多周期空头；这是规则加权分，不是胜率。结构上是扩散喇叭形，收盘仍在上下轨之间运行（最新 K 线上影线触及上轨后回落）：上攻需日线放量收盘站上 1328.58，目标 1351.22，收盘跌回 1320.32 下方视为假突破；下探以收盘跌破 1300.01 为触发，目标 1281.70。现价附近的 1318.83、1315.39、1309.21 是正在争夺的价位，不作触发条件。浪型主计数为上涨 ABC（收盘跌破 1228.10 失效）。……（大盘、风控与持仓防守、正常波动范围、回测与 IC、文件、免责声明依次展开）

错误的回复（不得这样写）：

> ~~茅台已经向上突破，上涨概率约 70%，建议 1330 附近买入，目标 1440。~~

错在：没有置顶风控否决；编造了概率；把浪型测算位 1440.44 说成目标价；给出了个性化买入建议。`scripts/lint_response.py` 会拦截其中的概率措辞与"1330 附近买入""目标 1440"。

## 八、参考文档（按需读取）

- `references/output-fields.md`：`result.json` / `backtest.json` 每个字段的含义、单位、取值范围、能否为空、稳定级别和对外怎么说，以及 6.x 的稳定性规则。用户追问某个字段时阅读。
- `references/scenario-playbook.md`：8 类标准情景库的前提、触发、目标与失效条件。
- `references/interpretation-guide.md`：形态、浪型、市场状态、风控计划、正常波动范围和回测的解读要点与常见误读。
- `references/math-patterns.md`：用户追问某个指标、形态或正常波动范围如何计算时阅读。
- `references/cn-market.md`：A股交易时段与集合竞价、涨跌停（主板 ±10%、双创 ±20%、北交所 ±30%，ST 按板块与日期区分）、科创板与北交所申报细则、T+1、融券限制、代码识别、复权与交易日历。
- `references/hk-market.md`：港股交易时段与收市竞价、价位表（含 2025-08 / 2026-08 两期下调）、碎股、卖空规则、双边印花税、恒生科技指数数据源。
- `references/us-market.md`：美股常规与盘前盘后时段、T+1 结算、PDT 规则取消后的过渡期、Reg SHO 卖空规则、VIX 与财报窗口说明。
- `references/failure-modes.md`：撰写文字分析前对照，避免常见的数字与表述错误。
