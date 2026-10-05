---
name: fund-investment-guide
description: |
  invest系列主入口。识别标的类型，路由到专业分析工具。覆盖个股（A股/港股/美股/机构深度）、基金、单一资产（债券/可转债/大宗商品含黄金十维度/REITs）、宏观与市场环境、机构级内容产出、资产配置、大师会诊；取数统一走 invest-cli（多源数据层：腾讯行情/腾讯微证券/同花顺/东财/yfinance/SEC EDGAR/FRED/Wind/盈米/天天基金官方 ttskill + argo 财经垂直源，quote/kline/westock/intent/info/datasources 统一入口）。

  触发：「分析一下」「看看这个」「值得买吗」「这只怎么样」「资产配置」「大师怎么看」「基金分析」「股票分析」「黄金能买吗」「转债」「REITs」「债券」「流动性」「市场环境」「出个研报」「自选股」「/cli」

  Invest series entry. Route by asset type to a dedicated reviewer. Unified data layer via invest-cli (Tencent quotes / Tencent WeStock / Hithink / Eastmoney / yfinance / SEC EDGAR / FRED / Wind / YingMi / TTFund official ttskill + argo finance vertical sources) — quote / kline / westock / intent / info / datasources.
license: MIT
version: 2.7
---

# Invest 系列：投资分析指南

> 只做路由，不做分析。买基金像请管家，买股票像合伙做生意。

## 系列成员

| 技能 | 分析对象 | 核心问题 |
|:-----|:---------|:---------|
| invest-stock | 个股（A股/港股/美股+机构深度） | 懂生意吗？有护城河吗？价格合适吗？ |
| invest-fund | 基金/ETF/基金经理 | 懂策略吗？能跑赢吗？成本合理吗？ |
| invest-asset | 可转债 / 黄金白银原油 / REITs / 债券 | 债券：偿付+利差+位置；可转债：条款+债底+溢价；商品：逻辑+位置+波动；REITs：底层+运营+估值 |
| invest-allocation | 资产配置 | 股债商比例、再平衡、组合检视 |
| invest-macro | 宏观与市场环境 | 全球流动性、美股情绪、加密底部信号、市场温度 |
| invest-discuss | 大师会诊 | 4 视角 × 3 深度，多视角验证、发现盲区 |
| invest-analyst | 机构级工作台 | IC 研报 / 主题策略 / 事件驱动 / 一致预期 / 行业深度 / 市场日报 |
| invest-cli | 数据层（单一取数入口） | 怎么取：多源路由 + 整单回退 + 来源标注 |

完整路由表、取数映射与维护约定见 `skills/invest/SKILL.md`。
