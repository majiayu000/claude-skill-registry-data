---
name: invest
description: |
  invest系列主入口。识别标的类型，路由到专业分析工具。
  触发：「分析一下」「看看这个」「值得买吗」「这只怎么样」「资产配置」「大师怎么看」「债券」「流动性」「市场环境」「比特币抄底」
triggers:
  - 分析一下
  - 看看这个
  - 值得买吗
  - 这只怎么样
  - 基金
  - ETF
  - 基金经理
  - 股票
  - 护城河
  - 资产配置
  - 大师怎么看
  - 圆桌
  - 会诊
  - 债券
  - 可转债
  - 黄金
  - 流动性
  - 市场环境
  - 比特币
  - 投委会
  - IC报告
  - 研报
  - 行业深度
  - 市场日报
  - 再平衡
  - 组合
  - 港股
  - 美股
  - 大宗商品
  - REITs
  - 分派率
  - 债市
  - 美联储
  - 缩表
  - 企业分析
  - 企业信用
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
| 「基金池」「选基」「基金组合」「关注池」「基金池构建」「基金池更新」 | invest-pool |
| 「风险管理」「风险认知」「本金安全」「杠杆」「仓位管理」「风险系统」「投资纪律」「现金管理」「安全垫」 | invest-risk |
| 「大师怎么看」「圆桌」「巴菲特和芒格」「会诊」「多几个角度」「上会」「投委会」「重仓前再看看」 | invest-discuss |
| 「债券」「国债」「利率债」「信用债」「城投」「债市」「利差」「久期」 | invest-asset（债券细则） |
| 「流动性」「美联储」「缩表」「SOFR」「MOVE」「市场环境」「美股情绪」「NAAIM」「市场过热」「比特币抄底」「MVRV」「钱紧不紧」 | invest-macro |
| 「出一份IC报告」「电话会」「业绩会」「纪要」「一致预期」「主题策略」「行业深度」「产业链」「市场日报」「晨报」「事件驱动」「投资论点」 | invest-analyst（机构级内容产出） |
| 「企业分析」「企业深度」「企业信用」「企业一页纸」「这家企业怎么样」 | invest-enterprise |

**混合表述**：如「分析一下易方达蓝筹这只基金」→ 含「基金」→ invest-fund。边界：「用机构视角看XX」「IC怎么样」= 判断买不买 → invest-stock；「出 IC 报告/写研报」= 产出文档 → invest-analyst。

**通用开场白**：「分析一下」「看看这个」「值得买吗」「这只怎么样」这四句在上表里没有对应行——它们只说明「要分析」，不说明「分析什么」。此时**先从标的本身判定类型**（6 位数字 / 5 位港股 / 基金代码段 / 字母代码），再回上表选技能；不要因为没有关键词就反问用户「想分析什么」——标的通常就在同一句话里（「分析一下茅台」）。只有当句子里确实找不到任何标的线索时，才追问。

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
| 「分析一下XX企业的信用风险」 | 进入invest-enterprise。 |

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

## 架构说明

invest 系列采用三层架构：

| 层 | 职责 | 组件 |
|---|---|---|
| **方法论层** | 分析框架、决策逻辑、路由规则 | invest-*（本系列） |
| **数据层** | 取数、清洗、结构化 | `mx-data`（统一数据源） |
| **呈现层** | 报告模板、格式、交付 | `mx-templates`（报告模板库） |

- invest-* 调用 mx-data 获取数据
- invest-* 拿到数据后按方法论分析
- invest-* 调用 mx-templates 渲染报告
- mx-data 不知道"分析"是什么，mx-templates 不知道"数据"从哪来

---

## invest系列完整图谱

### 单一品种分析
| 技能 | 分析对象 | 核心问题 |
|------|---------|---------|
| invest-stock | 个股（A股/港股/美股+机构深度） | 懂生意吗？有护城河吗？价格合适吗？ |
| invest-fund | 基金/ETF/基金经理 | 懂策略吗？能跑赢吗？成本合理吗？ |
| invest-asset | 可转债 / 黄金白银原油 / REITs / 债券（利率/信用） | 债券：偿付+利差+位置；可转债：条款+债底+溢价；商品：逻辑+位置+波动；REITs：底层+运营+估值 |
| invest-enterprise | 单一企业主体 | 股东治理+行业+经营+财务+信用+司法 |

### 组合与决策
| 技能 | 功能 | 用途 |
|------|------|------|
| invest-allocation | 资产配置 | 股债商比例、再平衡、组合检视、投稳/投变、现金管理 |
| invest-pool | 基金池管理 | 风格分类矩阵、选基七维度、行业轮动评估、更新机制 |
| invest-discuss | 大师会诊 | 4视角×3深度，多视角验证、发现盲区 |
| invest-macro | 宏观与市场环境 | 全球流动性、美股情绪、加密底部信号、市场温度 |
| invest-analyst | 机构级工作台 | IC研报/主题策略/事件驱动/一致预期/行业深度/市场日报 |

### 风险与纪律
| 技能 | 功能 | 用途 |
|------|------|------|
| invest-risk | 风险认知与管理系统 | 风险四层递进诊断、风险管理四层框架、不依赖意志力的系统设计、现金管理与安全垫 |

### 支撑层
| 组件 | 职责 |
|------|------|
| mx-data | 多数据源聚合取数（同花顺/东财/天天/Wind/腾讯/argo 等，智能路由+组合） |
| mx-templates | 报告模板库（公司一页纸/基金深度/债券一页纸/利差/业绩点评/IC/企业15板块/行业） |

---

## 数据源门闩（场景 → invest-cli 取数映射）

取数统一走 invest-cli，不在分析 skill 里猜源。主路 = hithink（同花顺）。ttskill 只是可选深取，登录就绪才参与。可用性以 `invest-cli datasources` 运行时探测为准。

| 场景 | 命令 | 数据源 |
|------|------|--------|
| A股快照 | `invest-cli stock <代码>` | hithink（同花顺） > eastmoney（东方财富） |
| 港股快照 | `invest-cli stock <代码>` | eastmoney（东方财富） |
| 美股快照 | `invest-cli us <代码>` | yfinance > tencent（腾讯行情） > tiingo > bitget |
| 美股历史 | `invest-cli us <代码> --history` | tiingo |
| 基金快照 | `invest-cli fund <代码>` | hithink（同花顺） > ttskill（天天基金，可选深取） > eastmoney（东方财富） |
| 基金诊断/组合/配置 | `invest-cli intent deep/screen/portfolio/plan` | yingmi（盈米） |
| 债券 | `invest-cli intent deep bond <代码>` | mxds（妙想） |
| 资讯/舆情/宏观 | `invest-cli info` / `invest-cli intent macro` | argo / fred（FRED） |
| 美股原文级 | `invest-cli sec <代码>` | sec_edgar（SEC EDGAR） |
| 美股深取 | `invest-cli fmp <代码>` | fmp |
| 指数/行业估值/宏观深取 | 透传 | wind / index_hub / etfirst / westock |

运行时解析约定（PATH 优先、缓存口径）见 `invest/references/cli-runtime.md`；其中两张派生表已作废，取数以本页映射表为准。

## 已归档路由

| 旧名 | 归入（已归档） | 查看方式 |
|------|---------------|---------|
| invest-bond | invest-asset（已归档） | `invest-cli intent deep bond` |
| invest-commodity | invest-asset（已归档） | `invest-cli intent deep commodity` |
| invest-reit | invest-asset（已归档） | invest-asset |
| invest-us | invest-stock（已归档） | `invest-cli us` |
| invest-report | invest-analyst（已归档） | `invest-cli cn report` |
| fund-investment-guide | invest-fund（已归档） | `invest-cli fund` |

## 推理档位

分析前先读当前档位（`references/mode.yaml` → `references/mode.local.yaml`，后者覆盖前者）：

| 档位 | 取数次数 | 输出 | 适用场景 |
|------|---------|------|---------|
| **低** | ≤ 2 次 | 终端简洁结论（1-5 行核心指标 + 判断） | 简单查询、推荐、筛选 |
| **中** | ≤ 4 次 | 要点列表 + 简要分析 | 对比、初步分析 |
| **高** | 不限 | 完整报告（mx-templates 渲染） | 深度分析、IC 报告、投委会 |

**默认低档**。用户说「详细」「全面」「深入」→ 中档；说「报告」「IC」「深度分析」「完整报告」「研报」→ 高档。

## 核心原则

- **不问**：不让用户选择分析类型
- **不重复**：路由后不再重复询问
- **不分析**：本技能不做任何分析，只做路由
- **不默认出报告**：低/中档只给结论，高档才走 mx-templates

---

*invest v3.0 | 三层架构（方法论/数据/呈现）· 新增 invest-enterprise · 统一走 mx-data + mx-templates*
