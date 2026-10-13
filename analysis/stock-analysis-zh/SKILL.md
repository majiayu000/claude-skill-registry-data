---
name: stock-analysis-zh
description: "使用金融市场数据进行股票和公司分析。获取公司简介、技术分析、价格走势图、内部人士持股和 SEC 文件，实现全面的股票研究。"
version: 1.0.0
metadata:
  openclaw:
    emoji: "📈"
---

# 股票分析

使用实时市场数据进行全面的股票和公司分析。

## 核心功能

- **公司研究**：获取公司简介、业务信息、高管团队
- **技术分析**：查看价格走势图、技术指标、市场展望
- **基本面分析**：分析估值、分析师评级
- **内部人士活动**：追踪内部人士持股和交易记录
- **监管文件**：访问 SEC 文件历史和文档
- **多股对比**：通过图表数据对比多只股票

## 可用 API

### 公司信息
- `Yahoo/get_stock_profile` - 公司简介（业务、行业、高管、联系方式）
- `Yahoo/get_stock_insights` - 技术指标、估值、评级、研究报告

### 交易与市场数据
- `Yahoo/get_stock_chart` - 历史价格数据，支持自定义时间范围

### 持股与合规
- `Yahoo/get_stock_holders` - 内部人士持股和交易记录
- `Yahoo/get_stock_sec_filing` - SEC 文件历史（10-K、10-Q、8-K 等）

## 常用工作流程

### 1. 公司概览 → 深入分析
```
用户: "介绍一下 AAPL"
→ Yahoo/get_stock_profile（业务摘要、行业、员工数）
→ Yahoo/get_stock_insights（技术展望、估值、评级）
→ Yahoo/get_stock_chart（近期价格表现）
```

### 2. 技术分析 → 基本面验证
```
用户: "TSLA 值得买吗？"
→ Yahoo/get_stock_chart（价格趋势、支撑位/阻力位）
→ Yahoo/get_stock_insights（技术展望、目标价、评级）
→ Yahoo/get_stock_profile（验证业务基本面）
```

### 3. 内部人士活动分析
```
用户: "显示 NVDA 的内部交易情况"
→ Yahoo/get_stock_holders（内部人士交易记录）
→ Yahoo/get_stock_profile（高管背景信息）
→ Yahoo/get_stock_insights（检查是否与展望一致）
```

### 4. 尽职调查报告
```
用户: "MSFT 全面分析"
→ Yahoo/get_stock_profile（公司背景）
→ Yahoo/get_stock_insights（分析师评级、估值）
→ Yahoo/get_stock_chart（历史表现）
→ Yahoo/get_stock_holders（内部人士情绪）
→ Yahoo/get_stock_sec_filing（最新监管文件）
```

### 5. 多股对比
```
用户: "对比 AAPL、MSFT 和 GOOGL"
→ Yahoo/get_stock_chart（使用 comparisons 参数）
→ Yahoo/get_stock_insights（每只股票的分析）
→ 并排比较关键指标
```

### 6. 行业研究
```
用户: "分析科技股：AAPL、NVDA、AMD"
→ Yahoo/get_stock_profile（每家公司的业务重点）
→ Yahoo/get_stock_insights（行业对比评分）
→ Yahoo/get_stock_chart（相对表现）
```

## 关键参数

### 通用参数
- `symbol`：股票代码（如 "AAPL"、"TSLA"）
- `region`：市场区域（US、GB、JP 等）- 默认：US
- `lang`：响应语言（en-US、zh-Hant-HK 等）- 默认：en-US

### 图表专用参数
- `interval`：1m、5m、15m、30m、1h、1d、1wk、1mo
- `range`：1d、5d、1mo、3mo、6mo、1y、2y、5y、10y、ytd、max
- `comparisons`：与其他股票对比（如 "^GSPC,MSFT"）
- `events`：包含股息、拆股、财报（div、split、earn）

## 关键数据点

### 简介数据
- 业务摘要和行业分类
- 员工数量和高管团队
- 联系方式和网站
- 行业和板块指标

### 洞察数据
- **技术展望**：短期/中期/长期信号
- **估值**：相对行业/市场的价值
- **关键技术指标**：支撑位、阻力位、止损位
- **评级**：分析师推荐和目标价
- **公司指标**：创新、招聘、可持续性评分
- **研究报告**：分析师报告和摘要
- **重大事件**：近期发展动态

### 图表数据
- OHLC（开盘、最高、最低、收盘）价格
- 成交量数据
- 调整后收盘价
- 52 周最高/最低价
- 当前交易周期信息

### 持股数据
- 内部人士姓名和职位
- 交易日期和描述
- 持股数量和价值
- 与公司的关系

### 文件数据
- 文件类型（10-K、10-Q、8-K 等）
- 文件日期和标题
- EDGAR 完整文档链接
- 附件和相关文档

## 何时使用此技能

**当用户提到以下内容时，务必调用 API：**
- **股票代码**："AAPL"、"TSLA"、"$MSFT"、"股价"、"股票信息"
- **分析请求**："分析"、"研究"、"调查"、"告诉我关于 [股票]"
- **对比**："对比"、"vs"、"比较"、"哪个更好"
- **价格查询**："价格"、"走势图"、"表现"、"趋势"、"涨还是跌"
- **内部人士活动**："内部人士"、"持股"、"谁拥有"、"买入/卖出"
- **文件**："SEC 文件"、"10-K"、"10-Q"、"财报"、"财务报表"
- **公司信息**："[公司]做什么的"、"谁管理"、"关于 [公司]"

**必须调用的 API 组合：**
- 一般股票问题 → 必须调用 `Yahoo/get_stock_profile` + `Yahoo/get_stock_insights`
- 提及价格/走势图 → 必须包含 `Yahoo/get_stock_chart`
- 投资决策 → 必须调用全部三个：走势图 + 洞察 + 简介
- 多只股票 → 必须在走势图 API 中使用对比参数
- 内部人士问题 → 必须调用 `Yahoo/get_stock_holders` + 简介以获取背景信息

## 最佳实践

1. **先广后深** - 先查看简介，再获取具体数据
2. **注重上下文** - 将简介与技术数据结合以获得更好的洞察
3. **使用对比功能** - 走势图 API 支持多股票对比
4. **区域股票** - 为非美国市场设置 region/lang 参数
5. **时间相关性** - 根据用户的时间范围调整图表范围
6. **内部人士上下文** - 将持股数据与简介结合以获得完整图景

## API 参考

完整的参数规格和响应架构：
- [yahoo-api.md](references/yahoo-api.md)
