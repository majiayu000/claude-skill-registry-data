---
name: taxue-invest
description: |
  invest系列主入口。识别标的类型，路由到专业分析工具。覆盖个股（A股/港股/美股/机构深度）、基金、单一资产（债券/可转债/大宗商品含黄金十维度/REITs）、宏观与市场环境、机构级内容产出、资产配置、基金池选基、风险管理、企业深度；三层架构：方法论（invest-*）/ 数据（mx-data，invest-cli 的统一封装）/ 呈现（mx-templates 报告模板）。取数统一走 invest-cli（多源数据层：腾讯行情/腾讯微证券/同花顺/东财/yfinance/SEC EDGAR/FRED/Wind/盈米/妙想/天天基金官方 ttskill + argo 财经垂直源）。

  触发：「分析一下」「看看这个」「值得买吗」「这只怎么样」「资产配置」「大师怎么看」「基金分析」「股票分析」「黄金能买吗」「转债」「REITs」「债券」「流动性」「市场环境」「出个研报」「自选股」「选基」「风险管理」「企业分析」「/cli」

  Invest series entry. Route by asset type to a dedicated reviewer. Three layers: methodology (invest-*) / data (mx-data, a thin wrapper over invest-cli) / presentation (mx-templates). Unified data layer via invest-cli (Tencent quotes / Tencent WeStock / Hithink / Eastmoney / yfinance / SEC EDGAR / FRED / Wind / YingMi / Miaoxiang / TTFund official ttskill + argo finance vertical sources).
license: MIT
version: 3.0
---

# Invest 系列：投资分析指南

> 只做路由，不做分析。买基金像请管家，买股票像合伙做生意。

## 系列成员

三层架构：**方法论层**（怎么分析）/ **数据层**（怎么取数）/ **呈现层**（怎么出报告）。

### 方法论层

| 技能 | 分析对象 | 核心问题 |
|:-----|:---------|:---------|
| invest-stock | 个股（A股/港股/美股+机构深度） | 懂生意吗？有护城河吗？价格合适吗？ |
| invest-fund | 基金/ETF/基金经理 | 懂策略吗？能跑赢吗？成本合理吗？ |
| invest-asset | 可转债 / 黄金白银原油 / REITs / 债券 | 债券：偿付+利差+位置；可转债：条款+债底+溢价；商品：逻辑+位置+波动；REITs：底层+运营+估值 |
| invest-allocation | 资产配置 | 股债商比例、再平衡、组合检视 |
| invest-pool | 基金池与选基 | 风格稳不稳？能力圈在哪？行业轮动值不值得配？ |
| invest-risk | 风险与纪律 | 本金安全吗？杠杆安全吗？系统不靠意志力能撑住吗？ |
| invest-enterprise | 企业深度分析 | 股东治理+行业+经营+财务+信用+司法 |
| invest-macro | 宏观与市场环境 | 全球流动性、美股情绪、加密底部信号、市场温度 |
| invest-discuss | 大师会诊 | 4 视角 × 3 深度，多视角验证、发现盲区 |
| invest-analyst | 机构级工作台 | IC 研报 / 主题策略 / 事件驱动 / 一致预期 / 行业深度 / 市场日报 |

### 数据层与呈现层

| 技能 | 职责 |
|:-----|:-----|
| mx-data | 数据层：`invest-cli` 的统一封装（场景→命令映射，零配置） |
| mx-templates | 呈现层：10 个报告模板（`{{变量}}` 占位，不绑定数据源） |
| invest-cli | 底层 CLI：多源路由 + 整单回退 + 来源标注 |

### 推理档位

低（默认，简洁结论）/ 中（要点列表）/ 高（完整报告）。公开默认低档，本机可用 `invest/references/mode.local.yaml` 覆盖。

完整路由表、取数映射与维护约定见 `skills/invest/SKILL.md`。
