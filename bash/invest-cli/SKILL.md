---
name: invest-cli
description: |
  投资分析 CLI — 数据获取 + 分析框架一体化，dual-mode 运行。

  触发：「/cli」「/投资cli」「invest cli」「终端分析」「命令行分析」
  或：「用cli分析」「终端查一下」「命令行看看」

  命令入口：`invest-cli stock 600519`（PATH 无 invest-cli 时兜底：`"$HOME/.local/bin/invest-cli" stock 600519`——wrapper 优先用 skill 自带 venv，含 yfinance）
---

## 完整触发条件（原始 description）

投资分析 CLI — 数据获取 + 分析框架一体化，dual-mode 运行。 触发：「/cli」「/投资cli」「invest cli」「终端分析」「命令行分析」 或：「用cli分析」「终端查一下」「命令行看看」 命令入口：invest-cli（兜底脚本见下）


# invest-cli — 投资分析 CLI

## 定位

现有 invest 系列 skill 只定义"怎么想"（分析框架），数据靠 web search。
invest-cli 补充"怎么取"（数据获取），把 CLI 脚本和分析框架串起来。

**dual-mode**：
- Skill 触发 → 调用 CLI 脚本（`--json`）→ 用 invest 系列框架解读 → 输出完整分析报告
- 终端直接运行 → 输出表格快照

**入口约定**：优先 `invest-cli` 命令（PATH，wrapper 在 `~/.local/bin/`）；PATH 无该命令时用 `"$HOME/.local/bin/invest-cli"` 兜底。不要绕过 wrapper 直接 `python3` 裸跑系统解释器——那样会丢掉 venv 里的 yfinance，美股路径从全量快照依次降级为腾讯行情 → Tiingo EOD → Bitget rToken。

## 路由逻辑

1. 识别标的类型（股票/基金/美股/选股）
2. 调用对应子命令，`--json` 获取结构化数据
3. 将 JSON 数据传给 invest 系列分析框架
4. 输出完整分析报告

## 子命令

### stock — A股/港股分析

```bash
invest-cli stock <代码/名称> [--json]
```

- 数据源：同花顺金融数据服务优先（A 股官方 REST）；失败或港股回退东方财富
- 获取：实时行情 + PE/PB/PS/PCF + 近 5 年年报 + ROE/毛利率/现金流（港股仍走东财）
- 分析框架：对标 invest-stock 三关审查（懂不懂 / 好不好 / 贵不贵）
- 内置名称映射：茅台→600519、五粮液→000858、宁德时代→300750 等

### fund — 基金分析

```bash
invest-cli fund <代码/名称> [--json]
```

- 数据源：同花顺金融数据服务优先；失败回退东方财富（intent deep fund 仍先盈米）
- 获取：净值/业绩/回撤/费率/经理/十大重仓
- 分析框架：对标 invest-fund 三关审查
- 内置名称映射：易方达蓝筹（精选）→005827、中欧医疗→003096 等。注意 110011 现为「易方达优质精选(QDII)」，旧文档把「易方达蓝筹」映射到 110011 是错的（源码注释里专门记过这次纠偏）

### us — 美股分析

```bash
invest-cli us <代码> [--json]
invest-cli us <代码> --history [--years N]   # Tiingo EOD 历史专项（复权K线+分红/拆股/回撤摘要）
```

- 数据源：yfinance（估值/财务/评级，装了才在）；缺失或失败时回退**腾讯行情**（实时美股行情，含 PE/PB/市值/52周/股息率/ROE，实测 ~189ms 全字段），再退 **Tiingo**（官方交易所收盘价 + 市值/PE/PB/52周/股息率/最大回撤，`quote_basis=eod` 诚实标注收盘口径），最后 Bitget rToken 报价（USDT，非官方价，只有成交价与 24h 区间）
- 获取：全量快照（yfinance）或行情口径快照（tencent）或 EOD 口径快照（tiingo）或行情-only（bitget，`quote_type=rtoken`）
- 妙想（mxds）已于 2026-10-11 移出美股快照链：它是「自然语言→表格」服务（单次 1.2s+，快照查询只回收盘价简表，对比 tencent 全字段 189ms），不适合确定性快照；美股的自然语言查询走 `intent mxds "AAPL 股价"`（裸 ticker 已适配包装，结果缓存 300s）
- `--history` 走 Tiingo 独占能力：可靠复权历史（adjClose + divCash + splitFactor），快照链其余源都不提供；免费档无三表，财报问题走 `invest-cli sec`
- 分析框架：对标 invest-stock 美股四维度（ROE持续性/负债安全/FCF质量/经济护城河）；Bitget 回退仅有报价，无财务

### quote — 免鉴权多标的实时行情（跨市场）

```bash
invest-cli quote <代码[,...]> [--json]
```

- 用途：**只要行情**的问题（「现在多少钱」「涨跌多少」「这几只对比一下」）
- 数据源：腾讯行情（零鉴权），一次 HTTP 请求可带任意多个标的，跨 A股/港股/美股/ETF/可转债
- 实测：单标的 ~130ms，6 标的混合 ~132ms；缓存 10s（比快照链的 60s 更严，行情语境下可忽略）
- 与 `stock`/`fund`/`us` 的分工：那三条是**深度快照**（含基本面，冷取数 0.5s 起，美股 4s 量级），
  `quote` 是**纯行情**。问基本面却用 quote 会缺 ROE/净利润；问行情却用 stock 会多付几倍等待

### sec — SEC EDGAR 美股数据（免费官方源，五个动作）

```bash
invest-cli sec <代码> [--forms 10-K,10-Q,8-K] [--filings 5] [--years 5] [--quarterly] [--json]
invest-cli sec <代码> --search "关键词" [--forms 10-K] [--from 2025-01] [--to 2025-12] [--limit 10]
invest-cli sec <代码> --insiders [--days 180] [--limit 20]
invest-cli sec <代码> --events [--days 365] [--limit 20]
invest-cli sec <投资人> --holdings [--limit 40]     # 机构名 / CIK / 上市代码（如 BRK）
```

- 数据源：SEC EDGAR 官方 API（companyfacts + submissions + full-text search + Archives），免费无 key
- 身份声明：SEC 要求 UA 含邮箱（www.sec.gov 强制，否则 403）；默认用占位邮箱通过校验，建议设置 `SEC_EDGAR_USER_AGENT="你的名字 你的邮箱"` 声明真实联系方式
- 快照（默认动作）：24 项年报指标（营收/毛利/营业利润/净利/EPS/研发/销售管理费/所得税/经营现金流/资本开支/自由现金流/回购/分红/资产/负债/权益/现金/长期债务/存货/应收/流通股数；FCF 为派生并标注）+ 近 5 年年度序列（三关趋势表直接可用）+ 最近申报清单；`--quarterly` 附近 8 季（Q4 为推导值，标 derived）
- 全文检索：EDGAR full-text search（2001 年起），命中到申报 + 原文段落（前 5 条拉原文抽取，抽不到留空、不编造）；多词自动按短语检索
- 内部人交易：Form 4 逐笔（谁/职位/交易代码/股数/价格/金额/交易后持股），含期权行权与代扣税行
- 事件：8-K 逐事项（业绩发布/高管变动/协议/减值/退市通知…按 SEC item 编码映射）+ 13D/13G 权益变动
- 13F 持仓：机构最新一期（按发行人聚合，带占比）；金额单位随申报期标注（2023 年起为美元）
- 口径：标签漂移按优先级回退（如 Apple 的 Revenues 停在 2018，自动改用 RevenueFromContractWithCustomerExcludingAssessedTax）；时长型事实限 300~400 天，季度值不进年度结果；**一次只做一件事**（四个动作旗标互斥，同时给会报错）
- 定位：与 Wind / yfinance 的结构化数字交叉验证的「原文级」依据；原始 JSON 磁盘缓存（companyfacts 24h / 申报原文 7 天）
- 不做：外国私人发行人（20-F）、投资公司（N-CSR）不在覆盖内，会明确报错；13F 只含美国多头与期权（不含空头）

### fund-class — 基金三层分类器（评价友好分类）

```bash
invest-cli fund-class <6位代码> [--json]
```

- 定位：只输出**稳定的分类事实**——L1 大类资产 / L2 产品形态 / L3 投资策略 + 辅助标签（运作方式/固收+/指数型/QDII/FOF/养老/REITs/申赎状态/风险等级/目标ETF），含依据与口径原文；**不做评价结论**——筛选/三关审查/同类对比/watchlist 各自消费，分类器与消费方解耦
- 数据底座：ttskill TTFUND_BASE_INFOS expansion（**单请求**：FTYPE + SHORTNAME + traits 布尔组 + 申赎状态）；其余源没有类型字段（实测快照只有场内外标记），SHORTNAME 的类型后缀当交叉复核列，冲突并列不裁决、只对境内大类生效
- 规则真源：`fund-classification.yaml`（FTYPE 全文映射 + 前缀兜底 + 资产段优先 + L3 关键词 + 固收+ 判定）——改规则不改代码，golden 用例锁行为
- 未定语义：字段缺失/未登记 → None + unresolved 原因，**绝不静默猜**；L1 按「主要投什么资产」判（资产优先：QDII-商品 → 另类(商品) 而非跨境）
- 与基金链分工：`invest-cli fund` 给净值/费率/重仓快照；本命令给分类事实

### fmp — Financial Modeling Prep 美股深取（免费档，不进快照链）

```bash
invest-cli fmp <代码> [--json]                       # 深取快照：行情 + TTM 比率 + 结构化评级 + 公司概况
invest-cli fmp <代码> --estimates [--json]           # 年度分析师预测（EPS/营收 低/均/高）
invest-cli fmp <代码> --statements [--period annual] [--limit 2]
invest-cli fmp <代码> --dividends [--json]
```

- 数据源：FMP `/stable` API；免费档 250 次/天 + 30 天 500MB 带宽，**深取专项，不进快照链**（兜底位已由 Tiingo 承担，别拿本源做日常快照）
- 与 `sec` 分工：sec = 10-K XBRL **原文级**（官方免费、申报清单/内部人/事件/13F）；fmp = **加工好**的 TTM 比率（毛利率/利润率/负债/股息）、结构化评级（字母 + DCF/ROE/ROA/负债/PE/PB 六维分项分）、年度分析师预测
- 免费档边界（2026-09-30 实测）：三表 annual 通、quarterly 付费；`ratios-ttm` 的 **ROE/ROA=null**（要 ROE 走三表自算或 yfinance）；estimates 仅 annual；ETF 持仓明确付费墙；**查无此票与付费墙同码 402**（按文案分流）
- 分析框架：评级分项与 TTM 比率喂给 invest-stock 的「好不好/贵不贵」，数字与 sec_edgar/yfinance 交叉验证

### cn — A股/港股市场结构（公告/一致预期/股东/披露日历/研报）

```bash
invest-cli cn notice <代码[,代码...]> [--type N] [--limit N] [--offset N]
invest-cli cn notice --search "关键词" [--limit N]      # 巨潮 cninfo 关键词检索（走 argo）
invest-cli cn consensus <代码[,代码...]>                # 一致预期（目标价 + 年度预测）
invest-cli cn holders <代码[,代码...]>                  # 股东研究（十大股东 + 变动）
invest-cli cn disclosure <代码[,代码...]>               # 财报披露日历（预约披露日）
invest-cli cn report <代码[,代码...]> [--limit N] [--offset N]   # 研报列表
```

- 数据源：westock（腾讯微证券）五个高频子命令的收敛入口；`--search` 走 argo 的 cninfo 引擎
- `--json` 把 markdown 表格解析成结构化行（`tables[].rows` 按字段取值），原文始终保留在 `raw`
- 公告列表在 westock 通道故障时自动降级到 argo/cninfo 检索（标明来源与局限）
- 代码归一：`600519,000858` → `sh600519,sz000858`，中文名也可直接用
- 与 `westock` 透传的关系：透传仍是长尾出口（chip/lhb/events/industry-chain 等 40+ 子命令）；`invest-cli capabilities westock` 看已收敛清单

### screen — 选股（**股票**筛选）

```bash
invest-cli screen <条件> [--json]
```

- 数据源：妙想 mx_stocks_screener（自然语言选股，priority 55）优先，东方财富**选股** API（stock-screen）兜底——按定义只筛股票；两者结果体形状不同，解析层已兼容
- 支持自然语言条件："市盈率低于10的银行股"、"ROE大于20%的消费股"
- 筛**基金**不要用本命令（基金条件会被服务端当成股票的主营业务关键词，结果不是基金）：
  走 `invest-cli intent screen <条件>`，带「基金/ETF/债基」等词时自动路由到盈米基金搜索

### watchlist — 本地自选股

```bash
invest-cli watchlist add <代码> [--name N] [--type fund|stock]
invest-cli watchlist remove <代码>
invest-cli watchlist list [--with-quote]
```

- 本地存储 `<state_root>/watchlist.json`（默认 `~/.config/invest-cli/`，可用 `INVEST_CLI_STATE_DIR` 覆盖；用户数据不放缓存目录），不依赖任何外部账户登录态
- 行情预览走 route.fetch（A 股/基金快照链），按 `--type` 选 stock 或 fund

### tenure — 基金经理任职期复盘（分年度业绩/回撤 + 任职以来 vs 业绩基准指数）

```bash
invest-cli tenure <基金代码|名称> [--manager 姓名] [--since YYYY-MM-DD]
                  [--benchmark auto|指数代码] [--source auto|wind|ttskill]
                  [--years 5] [--excel out.xlsx] [--csv DIR] [--json]
invest-cli tenure --manager 姓名 [--company 公司] [--excel out.xlsx] [--json]
```

- 一次调用产出：档案（成立日/经理/任职日/基准）+ 分年度收益率与最大回撤（近 5 年含 YTD）
  + 任职以来逐日收益（基金 vs 基准）+ 累计/年化/超额 + 官方字段校验行
- 产物三层：终端表（默认）、`--json`（结构化信封，供 agent 消费）、`--excel`（概览/每只基金明细/数据来源；
  无 openpyxl 时自动落 `--csv` 同构文件，不丢数据）
- 数据源：Wind 为主（档案 get_fund_info / 复权净值 get_fund_performance 分段并行 / 基准 get_index_kline /
  官方年度字段），Wind 不可用时回退天天官方 gateway（NAV_INFO/BASE_INFOS/MANAGER_INFO）并在产物里标注
- 口径：任职以来基期 = 任职日前一交易日（与 Wind 区间收益率一致，任职当日收益计入）；
  年度回撤取年内峰值口径；基准指数 = 基金代码 + BI.WI，港股假期沿用前值
- `--manager` 不带基金时扫描该经理全部在管产品，按初始份额（A 类/唯一份额）过滤，一次产出组合级工作簿
- 成本提示：Wind 净值单次硬顶 100 行 → 分段抓取按次计费；结果落 6 小时磁盘缓存，
  同轮重跑命中缓存不再计费（实测 6 只基金全量重取 ≈75s → 命中 <0.1s）

### datasources — 数据源探测（统一门闩）

```bash
invest-cli datasources [--json]
```

- 列出所有已登记数据源（配置真源 `data-sources.yaml`）及运行时可用性
- 同时打印默认快照链（yaml × 真方法 × 可用性）；`--json` 含 `_chains`
- 取数走 `stock/fund/us/intent`，由 `sources/route.py` 选源，禁止在分析 skill 里猜源

### wind — 万得 Wind（机构级，直连 MCP）

```bash
invest-cli wind <server_type> <tool> --input '<json>' [--json]
```

- **直连 Wind MCP**（JSON-RPC over HTTP），不依赖 wind-mcp-skill 的 node CLI
- server_type：stock_data/fund_data/index_data/bond_data/financial_docs/economic_data/analytics_data
- Key 顺序与官方一致：`~/.wind-aifinmarket/config` > skill config.json > 环境变量 `WIND_API_KEY`

### yingmi — 盈米且慢（直连 OpenAPI）

```bash
invest-cli yingmi <tool> --input '<json>' [--json]
```

- **直连盈米 OpenAPI**，不依赖 `yingmi-skill-cli`；操作清单取官方 docs.json（缓存 6h）
- 凭据：`~/.yingmi-skill-cli/config.json` 的 apiKey（`Authorization: Bearer`）
- 已收敛高层入口（优先走，勿重复透传）：GuessFundCode/GetFundDiagnosis/SearchFunds/DiagnoseFundPortfolio/GetAssetAllocationPlan
- 批量/列表类工具（GetPopularFund/Batch*）返回 JSON 数组，适配器已支持

### ttskill — 天天基金业务包（透传，37 包可达，直连 gateway）

```bash
invest-cli ttskill <skill_id> --input '<json>' [--json]
```

- **直连官方 gateway**（POST /openapi/skill/invoke），不依赖 ttskill CLI；
  沿用官方凭据存储（macOS Keychain `com.ttfund.ttskill.base`）与 ed25519 签名（官方同一套认证）
- 常用：`TTFUND_MANAGER_INFO`（经理画像/在管）、`TTFUND_NAV_INFO`（历史净值）、`TTFUND_STOCK_PRICE_QUERY`（实时行情）、`TTFUND_MACRO_DATA`（中美宏观）、`TTFUND_VALUATION_MAP`（指数/行业估值分位）
- 参数以官方包 `examples/*.example.json` 为准；返回为原始结构（各包层级不一，透传不解释）
- fund 深取层内嵌 SEARCH/BASE_INFOS/HOLDING_INFO（走 `fund <code>`，勿手动透传）；黄金走 `intent deep commodity`
- 账户/交易类包（ACCOUNT_*/TRADE_QUERY/CONDITION_ORDER/SIM_TRADE/RATION_PLAN/SUBACCOUNT）为边界外：invest-cli 数据链路不消费，不建高层入口
- 全套 37 包用途与收敛标注：`invest-cli capabilities ttskill`

### capabilities — 能力发现层

```bash
invest-cli capabilities [yingmi|ttskill] [--json]
```

- 取数前先查：官方（盈米 69 工具 / 天天 37 包）有什么、invest-cli 收敛到哪、怎么调——一处可见，根治"不知道有 X 能力"的重复低效
- 空参=数据源总览 + 高层入口速查；`--json` 给 skill 层做路由决策
- 只列清单不取业务数据；拿不准参数先看 `capabilities` 输出里的工具描述

### 天天基金官方（ttskill，fund 源，已封装）

老 ttfund CLI 已退役（2026-09-03）：能力被官方 ttskill 业务包取代。
- fund 默认链为**自带源优先** `hithink > [ttskill 可选深取] > eastmoney`；ttskill 仅在已登录就绪时补充同类分位/机构占比/经理在管等深取字段
- 黄金深取走 `intent deep commodity` → 官方 `TTFUND_GOLD_INFO`
- 分析 skill 不要绕过 invest-cli 直接调官方包：fund 深取走 `fund <code>`，其余包走 `invest-cli ttskill <skill_id>` 透传
- 口径真源 = `invest-fund/references/data-pipeline.md` + `sources/ttskill.py`；差距与收敛进度见 `docs/capability-gap.md`

### intent — 意图层（默认取数入口，收敛接口面）

```bash
invest-cli intent <deep/screen/portfolio/plan/macro/present/mxds> <参数> [--json]
```

- 把盈米 69 个 MCP 工具 + Wind 7 类收敛为 6 个语义入口，内部按场景 + 标的类型路由到权威源
- `intent mxds "<自然语言>"` — 妙想自然语言查询（A股/港股/美股/基金/债券/指数/宏观/新闻/公告自动路由；裸 ticker 自动包装查询模板；结果按查询文本缓存 300s，命中带 `cached: true`）
- 接口面小、能力面全；`--json` 输出统一信封（source/ok/data/error）
- 推荐作为分析 skill 的首选取数方式；wind/yingmi 透传仅作高级/调试

### research — 长程研究管线（编排既取数入口，不自建数据路径）

```bash
invest-cli research fund-rank <主题> [--top N] [--order r3y|r1y|ytd] [--limit N] [--dy auto|on|off] [--enrich] [--out DIR] [--json]
```

- 一条命令完成「池构建(TTFUND_SEARCH 分页) → 批量快照(复用 `fund` 同路径同缓存) → 多期业绩排名 → 重仓×股息率交叉(公司名合并, A/H 同司一司) → 双源互证」
- 快照走 `fetch_fund_with_fallback`（与 `invest-cli fund` 完全同源，命中同一份磁盘缓存）；批量并发默认 3，`INVEST_CLI_RESEARCH_CONCURRENCY` 可调（同花顺合同配额未知，调高前先小池试）
- 池规则：主动型（剔指数/货币/理财/债券/QDII）、份额类去重（留 A 类）、「改革红利/混改红利」等复合名剔除、离岸互认基金剔除；红利/股息主题自动并入「股息」别名检索并开启股息率交叉（妙想 ≥4% 参照集），港股通主题默认剔除（重仓在港股，A 股参照集不适用）
- **双源互证**：hithink returns vs ttskill 深取字段逐期对照（容差 0.05pp），不一致显式标注 ✗——「红利」基金名的业绩冠军可能根本不持高股息股，重仓验证比名字重要
- `--out DIR` 落 Markdown 报告与 result.json（provenance 齐全）；`--enrich` 给 Top-N 附 argo 资讯（每只一次检索，默认关）
- 定位：把 2026-10-11 红利交叉分析的十轮手工调用收敛为一条命令；首轮实测 97 只池排名与手工分析完全一致

## Skill 触发后的执行流程

1. **识别标的类型**：根据用户输入关键词判断 stock/fund/us/screen
2. **调用 CLI**：执行对应子命令，`--json` 模式获取数据
3. **解读数据**：
   - stock → 按 invest-stock 三关框架输出分析报告
   - fund → 按 invest-fund 三关框架输出分析报告
   - us → 按 invest-stock 美股四维度框架输出分析报告
   - screen → 直接输出选股结果表格
4. **补充分析**：CLI 数据 + invest 框架 = 完整分析报告

## 示例

### Skill 触发示例

用户：「/cli 分析一下茅台」
→ 识别为 stock → 调用 `invest_cli.py stock 600519 --json`
→ 解析 JSON → 按 invest-stock 三关框架输出分析报告

用户：「/cli 帮我看看 110011 这只基金」
→ 识别为 fund → 调用 `invest_cli.py fund 110011 --json`
→ 解析 JSON → 按 invest-fund 三关框架输出分析报告

用户：「/cli 看看 AAPL」
→ 识别为 us → 调用 `invest_cli.py us AAPL --json`
→ 解析 JSON → 按 invest-stock 美股四维度框架输出分析报告

### 终端直接运行示例

```bash
$ invest-cli stock 600519
============================================================
  贵州茅台（600519）— 行情快照
============================================================

  指标              数值
  ------------------------------
  最新价           1680.00
  涨跌幅             1.23%
  市盈率PE          28.50
  ...

$ invest-cli us AAPL
============================================================
  Apple Inc.（AAPL）— 美股快照
============================================================
  ...
```

## 与现有 invest 系列的关系

| 能力 | invest 系列 | invest-cli |
|------|------------|------------|
| 分析框架 | ✅ 完整 | 复用 invest 系列 |
| 数据获取 | ❌ 靠 web search | ✅ CLI 脚本 |
| 终端直接运行 | ❌ | ✅ |
| 触发方式 | 自然语言 | /cli + 自然语言 |

**invest-cli 不替代 invest 系列，是补充**。当用户想用 CLI 或明确说"/cli"时走 invest-cli，否则走原有 invest 系列。

## 数据源接入（统一门闩）

数据源声明真源为 `data-sources.yaml`，可用性由 `invest-cli datasources` 运行时探测。各源启用条件：

| 数据源 | 启用条件 | 覆盖 |
| --- | --- | --- |
| 同花顺金融数据服务 | `HITHINK_FINANCE_API_KEY` 或用户级 `credentials.env` | stock/fund（A 股与公募，不含港股/美股/自然语言选股） |
| 东方财富 | `EASTMONEY_APIKEY` | stock/fund/screen |
| yfinance | `uv pip install yfinance` | us（行情+财务） |
| SEC EDGAR | 免费无 key（可选 `SEC_EDGAR_USER_AGENT` 声明身份） | us 原文级数据（`invest-cli sec` 直取，不经快照链）：快照/5 年序列、全文检索、Form 4 内部人、8-K+13D/G 事件、13F 持仓 |
| Tiingo（美股 EOD） | `TIINGO_API_KEY` 或 `~/.config/invest-cli/tiingo.env` | us（官方收盘价 + 复权历史 + 估值序列）；EOD 历史专项 `invest-cli us <代码> --history`。免费档无三表（财报走 sec_edgar）、新闻在付费墙内 |
| Financial Modeling Prep（fmp） | `FMP_API_KEY` 或 `~/.config/invest-cli/fmp.env` | 美股深取（三表 annual/TTM 比率/结构化评级/年度预测，`invest-cli fmp` 直取）。免费档 250 次/天：ROE/ROA 比率=null、季度预测与 ETF 持仓付费 |
| Bitget rToken | 始终可用（公开 API） | us（仅行情/USDT） |
| 万得 Wind（直连 MCP） | `WIND_API_KEY`（`~/.wind-aifinmarket/config` 或环境变量） | stock/fund/index/bond/news/macro |
| 盈米且慢（直连 OpenAPI） | `~/.yingmi-skill-cli/config.json` 的 apiKey | fund/strategy/wealth/news |
| 天天基金（直连 gateway） | 官方凭据未过期（Keychain `com.ttfund.ttskill.base`）+ 已装业务包 | fund（同类分位/机构占比/在管列表等深取补充） |
| argo | `argo` skill 目录内含 `scripts/search.py` | news/macro（资讯/舆情/宏观检索；不经快照链，`info`/`intent macro` 直调）。引擎名原样透传给 argo（250+ 个，传错即报错、不静默换源）；清单见 argo `search.py --list-engines` |
| 探测负缓存 | 默认自动 | **http 型**（如 yfinance 的端点可达性）探测失败的源 120s 内不重探（`INVEST_CLI_PROBE_TTL_FAIL` 可覆盖），期间直接跳过不付探测等待；**adapter 型**（同花顺/Wind/盈米/天天等凭据型）失败**不落盘**——补凭据是秒级恢复，落 120s 负缓存会让 `datasources` 给出 2 分钟前的旧结论，故仅进程内 30s；快照命中缓存则完全无感 |

能力矩阵与详细配置见 `docs/data-sources.md`。取数与降级：单一场景优先最高优先级源，整单失败才降级，禁止跨源合并字段。

## 环境要求

- `HITHINK_FINANCE_API_KEY` 或 `~/Library/Application Support/hithink-finance/credentials.env`：同花顺官方源（A 股/公募优先）
- `EASTMONEY_APIKEY`：东方财富 API Key（港股、自然语言选股、以及同花顺失败时的回退）
- `yfinance`：Python 包（us 全量快照推荐；缺省可回退 Bitget）
- `TIINGO_API_KEY` 或 `~/.config/invest-cli/tiingo.env`：Tiingo 美股 EOD（us 链兜底位 + `us --history` 专项；免费注册 https://www.tiingo.com）
- `FMP_API_KEY` 或 `~/.config/invest-cli/fmp.env`：FMP 美股深取（`invest-cli fmp`；免费注册 https://site.financialmodelingprep.com）
- Python 3.10+
