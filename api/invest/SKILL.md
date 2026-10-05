---
name: invest
description: |
  invest系列主入口。识别标的类型，路由到专业分析工具。

  触发：「分析一下」「看看这个」「值得买吗」「这只怎么样」「资产配置」「大师怎么看」「债券」「流动性」「市场环境」「比特币抄底」
---

# invest：入口

> 只做路由，不做分析。

## 哲学锚点

- **巴菲特「价值投资」**：买股票就是买企业的一部分。不懂不做，没有护城河不做，价格不合适不做。
- **芒格「格栅思维」**：单一视角必然盲视。用多个维度交叉验证，避免陷入思维定式。
- **德鲁克「有效性」**：投资的终极标准不是「能不能赚」，而是「对谁有价值」「不做会怎样」。

---

## 路由逻辑

收到请求后，识别关键词，直接路由：

| 关键词 | 路由 |
|--------|------|
| 「基金」「ETF」「基金经理」「基金管理人」 | invest-fund |
| 「股票」「公司」「护城河」「PE」「ROE」「美股」「Apple」「TSLA」「NVDA」「港股」「南下」「北上」「深度分析」「DCF」「机构视角」「IC」 | invest-stock（A股/港股/美股+机构深度） |
| 「转债」「可转债」「转股」「溢价率」「债底」「下修」 | invest-asset（可转债细则） |
| 「黄金」「白银」「原油」「商品」「大宗商品」 | invest-asset（商品细则，黄金叠加十维度） |
| 「REIT」「REITs」「公募REIT」「分派率」 | invest-asset（REITs 细则） |
| 「资产配置」「组合」「股债比例」「再平衡」 | invest-allocation |
| 「大师怎么看」「圆桌」「巴菲特和芒格」「会诊」「多几个角度」「上会」「投委会」「重仓前再看看」 | invest-discuss |
| 「债券」「国债」「利率债」「信用债」「城投」「债市」「利差」「久期」 | invest-asset（债券细则） |
| 「流动性」「美联储」「缩表」「SOFR」「MOVE」「市场环境」「美股情绪」「NAAIM」「市场过热」「比特币抄底」「MVRV」「钱紧不紧」 | invest-macro |
| 「出一份IC报告」「电话会」「业绩会」「纪要」「一致预期」「主题策略」「行业深度」「产业链」「市场日报」「晨报」「事件驱动」「投资论点」 | invest-analyst（机构级内容产出） |

**混合表述**：如「分析一下易方达蓝筹这只基金」→ 含「基金」→ invest-fund。边界：「用机构视角看XX」「IC怎么样」= 判断买不买 → invest-stock；「出 IC 报告/写研报」= 产出文档 → invest-analyst。

---

## 工作流程

**第一步：识别**
读用户问题，匹配上表关键词。

**第二步：确认**
说一句：

> 分析[标的名称]，进入[技能名]。

**第三步：路由**
立即执行对应技能，不中断、不重复询问。

---

## 示例

| 用户说 | 动作 |
|--------|------|
| 「分析一下茅台」 | 分析茅台，进入invest-stock。 |
| 「张坤的基金怎么样」 | 分析张坤的基金，进入invest-fund。 |
| 「这只转债值得买吗」 | 分析这只转债，进入invest-asset（可转债细则）。 |
| 「黄金能配置吗」 | 分析黄金，进入invest-asset（商品细则）。 |
| 「REITs怎么看」 | 分析REITs，进入invest-asset（REITs细则）。 |
| 「我的资产配置合理吗」 | 进入invest-allocation。 |
| 「让巴菲特和芒格看看这只股」 | 进入invest-discuss（大师会诊）。 |
| 「解读腾讯最新季报」 | 解读腾讯最新季报，进入invest-stock。 |
| 「深度分析茅台，写个投资备忘录」 | 深度分析茅台，进入invest-stock（深度研报模式）。 |
| 「出一份茅台的IC报告」 | 出一份茅台的IC报告，进入invest-analyst。 |

## 结论信号 → 下一步

分析结束后按结论信号衔接下一步，不把用户留在断头路：

| 结论信号 | 下一步 |
|----------|--------|
| 「便宜且好，可以买」 | invest-allocation 定仓位 → invest-discuss 多视角压力测试 |
| 「好公司但不便宜」 | invest-stock 等击球区；需要持续跟踪 → invest-analyst 出跟踪报告 |
| 「看不懂 / 超出能力圈」 | invest-discuss 换视角；仍看不懂 → 不做 |
| 「基本面 / 持有人变了」 | 回到 invest-stock / invest-fund 重走三关 |
| 「组合偏离目标」 | invest-allocation 再平衡 |
| 「市场过热 / 流动性收紧」 | invest-macro 看温度 → invest-allocation 降风险敞口 |

---

## invest系列完整图谱

### 单一品种分析
| 技能 | 分析对象 | 核心问题 |
|------|---------|---------|
| invest-stock | 个股（A股/港股/美股+机构深度） | 懂生意吗？有护城河吗？价格合适吗？ |
| invest-fund | 基金/ETF/基金经理 | 懂策略吗？能跑赢吗？成本合理吗？ |
| invest-asset | 可转债 / 黄金白银原油 / REITs / 债券（利率/信用） | 债券：偿付+利差+位置；可转债：条款+债底+溢价；商品：逻辑+位置+波动；REITs：底层+运营+估值 |

### 组合与决策
| 技能 | 功能 | 用途 |
|------|------|------|
| invest-allocation | 资产配置 | 股债商比例、再平衡、组合检视 |
| invest-discuss | 大师会诊 | 4视角×3深度，多视角验证、发现盲区 |
| invest-macro | 宏观与市场环境 | 全球流动性、美股情绪、加密底部信号、市场温度 |
| invest-analyst | 机构级工作台 | IC研报/主题策略/事件驱动/一致预期/行业深度/市场日报 |

---

## 核心原则

- **不问**：不让用户选择分析类型
- **不重复**：路由后不再重复询问
- **不分析**：本技能不做任何分析，只做路由

---

## 数据层（invest-cli，单一数据入口）

**Agent 只需这一个数据点：** 所有取数走 `invest-cli`（intent / info / datasources），不要为每个数据源单独加载或路由一个 skill。invest-cli 自含，直接调各数据源的 HTTP API / 全局 CLI / 引擎，不 import 任何独立 skill 文件。

各分析 skill 的取数统一交给 `invest-cli`，按数据源门闩路由：

| 数据源 | 覆盖 | 优先级 | 默认快照链 |
| --- | --- | --- | --- |
| Wind（万得） | 个股/基金/指数/债券/宏观/资讯 | 80 | 否（仅 `invest-cli wind` 透传；无 stock()/fund()）。**直连 Wind MCP**，只要 `WIND_API_KEY`，不需要装 node CLI |
| 盈米且慢 | 基金诊断/策略/财富 | 70 | 否（intent deep fund 的「诊断」问题；无 fund() 快照）。**直连盈米 OpenAPI**，只要 apiKey，不需要装 `yingmi-skill-cli` |
| 同花顺金融数据服务 | A 股/公募快照 | 60 | 是（stock A、fund） |
| 东方财富 | 行情/基金/选股 | 50 | 是（港股、回退、自然语言选股）；key 配 `~/.config/invest-cli/eastmoney.env`（技能市场申请） |
| yfinance | 美股 + A股/港股兜底 | 40 | 是（us 主位；stock 链末位兜底，未安装则跳过） |
| 腾讯行情（tencent） | 多市场实时行情（A股/港股/美股/ETF/可转债） | 37 | 是（us 兜底位；A股/港股链末位）。**零鉴权、一次请求可带多标的**，实测单标的 ~130ms；无基本面，故不进主位。行情类问题直接走 `invest-cli quote` |
| SEC EDGAR | 美股财报原文（10-K XBRL 指标 + 申报清单） | 45 | 否（不经快照链；`invest-cli sec <代码>` 直取，免费无 key） |
| 腾讯微证券 CLI（westock） | 筹码/龙虎榜/资金流/一致预期/ESG/机构评级/产业链/板块估值/可转债条款 | 30 | 否（不经快照链；`invest-cli westock <args>` 透传 40+ 子命令，补既有源没有的市场结构类能力） |
| Bitget rToken | 美股代币价 | 35 | 是（us 回退） |
| 天天基金（直连 gateway） | fund 深取（同类分位/机构占比/在管） | 55 | 是（fund，登录就绪时排 hithink 之后）；黄金走 intent deep commodity→TTFUND_GOLD_INFO。**直连官方 gateway**，沿用官方凭据（Keychain）与 ed25519 签名，不需要装 ttskill CLI |
| FRED 宏观时序 | 净流动性三序列（总资产/TGA/ON RRP）+ SOFR | 25 | 否（`intent macro` 优先；无 key 走 fredgraph.csv 免 key 回退，仍失败降级 argo） |
| argo | 资讯/舆情/宏观检索 | —（不经快照链） | 否（`intent macro`、`invest-cli info` 直调） |

组合规则：同一问题整单回退、不混字段。行情、诊断、选股、资讯是四个不同问题，才用不同源。运行时链看 `invest-cli datasources` 的「默认快照链」。

- 取数直接走 `invest-cli stock/fund/us/screen/intent`。`datasources` 只用于诊断「当前机器会打谁」，不要作为每次取数的前置（内部 route.pick 已做准入）。
- 场景级路由与降级规则见 `invest-cli/docs/data-sources.md`。
- 数据来源必须在输出中标注，口径不一致不合并。

### 场景 → invest-cli 取数映射（单一真源）

各分析 skill 取数以此表为准，优先走 invest-cli，不靠 web_search 猜数据。

**按问题选命令（同一问题不混源；不同问题才组合）：**

| 问题 | 命令 | 运行时链 |
| --- | --- | --- |
| 个股三关快照（A股） | `invest-cli stock <代码>` 或 `intent deep stock` | hithink > eastmoney |
| 个股三关快照（港股） | 同上 | eastmoney |
| 美股快照 | `invest-cli us` 或 `intent deep us` | yfinance > tencent > bitget |
| 只要行情（现在多少钱/涨跌，可多标的） | `invest-cli quote <代码...>`（逗号分隔，跨市场） | tencent（零鉴权，一次请求）|
| 市场结构类（筹码/资金流/龙虎榜/一致预期/板块估值/产业链） | `invest-cli westock <子命令>` | 腾讯微证券 CLI（透传，自带代码归一化）|
| 美股财报原文（10-K 指标 + 申报链接） | `invest-cli sec <代码>` | SEC EDGAR 官方（免费无 key；与 Wind/yfinance 数字交叉验证） |
| 基金三关快照（净值/费率/重仓/收益） | `invest-cli fund <代码>` | hithink > eastmoney（ttskill 就绪时深取补充） |
| 基金诊断雷达 | `intent deep fund <代码>` | 盈米 GetFundDiagnosis；失败再走基金快照链 |
| 债券 | `intent deep bond <代码或名称>` | wind bond_data（get_bond_market_data） |
| 黄金/商品 | `intent deep commodity` | 官方 TTFUND_GOLD_INFO |
| 宏观/市场 | `intent macro` | FRED 净流动性（WALCL/TGA/ON RRP + SOFR；无 key 走免 key CSV 回退）；失败降级 argo（nbs_stats 等，免配额） |
| HTML 报告阅读 | `intent present <html文件>` | 本地提取正文（终端摘要；PDF 导出用浏览器打印） |
| 组合诊断/配置 | `intent portfolio <持仓json或自然语言>` | 盈米 |
| 家庭财务规划 | `intent plan <自然语言>`，**必须含「投资三性」至少一项**（预期年化收益率 / 投资期限 / 最大回撤，如 `intent plan 能承受20%回撤 5年 预期年化8%`）；只给「30岁 年收入30万」会被盈米以 9400 拒绝 | 盈米 |
| 自然语言选股 | `intent screen` / `invest-cli screen` | eastmoney |
| 资讯 / 舆情 / 宏观背景 | `invest-cli info <查询词>` | argo |

高级/调试：直接透传数据源 `invest-cli wind/yingmi ...`（默认不鼓励；天天官方已封装进 fund/intent，不直接透传 37 个业务包）。

---

## 已归档路由（2026-06-07 合并）

| 原独立 Skill | 现归入 | 查看方式 |
|-------------|--------|---------|
| hk-a-share-deep-analysis | invest-stock | invest stock |
| stock-analysis-guide / stock-analysis-cn | invest-stock | invest stock |
| fund-investment-guide / fund-manager-selector / invest-fund-read | invest-fund | invest fund |
| macro-liquidity / market-analysis-radar | invest-macro | invest macro |
| bond-market / gold-analyzer | invest-asset（bond 细则 / 黄金十维度） | invest bond / invest commodity |
| eastmoney-financial-data/search/select-stock | eastmoney 子命令 | eastmoney query/search-news/screen |
| smart-investor-final | invest 入口 | invest |
| investment-data-adapter | invest-cli | invest cli |

## 维护

- **版本与变更**：见 `CHANGELOG.md`；改路由表/图谱后必须同步更新
- **共享方法论真源**：`_shared/references/`（成员 skill 用**软链**引用，不复制副本；`test_skill_integrity.py` 有守卫防止有人手滑改成实体副本）
- **数据层运行时约定**：`references/cli-runtime.md`（PATH 优先/skill 树兜底、外部依赖只允许「登录态源」与「搜索技能」两类）。**取数分工的唯一真源是本文件的映射表**，cli-runtime 里那张同名旧表已作废
- **归档记录**：invest-report、invest-fund-manager、invest-us、hk-a-share-deep-analysis 等已并入上表成员，原文在 `~/.claude/skills-archive/`；2026-09-03 冗余 skill（smart-investor 四件套、stock-analysis、investment-agent、eastmoney、eastmoney-financial-data、financial-report-analyst）已 git 备份后从注册表删除，原文见 `~/.agents` 仓 commit 0479653；2026-09-03 invest-bond/convertible/commodity/reit 四技能合并为 invest-asset（同一三关模板×四种资产参数），原文见 `~/.claude/skills-archive/2026-09-03_merged-invest-asset/`

---

*invest v2.7 | 纯路由 + 统一数据层（天天/盈米/Wind 直连 API，无外部 CLI 依赖；腾讯行情/微证券并入）| 股基+四资产合一(债/转债/商品/REIT)+宏观+配置+圆桌+机构深度+分析师工作台*
