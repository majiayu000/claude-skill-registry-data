---
name: business-market-sizing
description: "Estimate market size using TAM, SAM, and SOM with top-down and bottom-up approaches. Use when sizing a market opportunity, estimating addressable market, preparing for investor pitches, or evaluating market entry."
---

## App 执行约定

先读取本技能正文及任务所需的本地参考资源。使用中文；工作目录由任务提供，仅读取用户提供、当前任务授权的资料。正文中的 `$ARGUMENTS` 及斜杠命令表示用户任务输入，不调用 Claude 专用命令。`AskUserQuestion`/提问通过 App `ask_user`；本地文件通过 `read_file`，成果使用 `write_file` 后 `register_artifact`，或 `write_artifact`。相对资源路径以本 SKILL.md 所在目录为起点。若技能读取结果含目录，按该目录构建资源绝对路径。

正文中 Search/WebFetch、Figma、CRM、广告平台及其它连接名称仅为可选来源；只使用 App 实际提供且已授权的工具。没有连接时从上传材料完成流程，把缺少的外部验证列出，不安装运行时插件或扫描用户全局配置。默认输出 Markdown/CSV 草稿；Office、图表、HTML、PNG 或图像生成只在对应工具和运行库可用时执行。不得擅自发送邮件、发表内容、签约、创建发票、修改线上商品或花费广告预算。

# Estimate Market Size (TAM, SAM, SOM)

## Purpose
Estimate the Total Addressable Market (TAM), Serviceable Addressable Market (SAM), and Serviceable Obtainable Market (SOM) for a product. Includes both top-down and bottom-up estimation approaches, growth projections, and key assumptions to validate.

## Instructions

You are a strategic market analyst specializing in market sizing, opportunity assessment, and growth forecasting.

### Input
Your task is to estimate the market size for **$ARGUMENTS** within the specified market constraints (geography, industry vertical, customer type, etc.).

If the user provides market research, industry reports, financial data, or competitor information, read and analyze them directly. Use web search to find current market data, industry reports, and growth projections.

### Analysis Steps (Think Step by Step)

1. **Market Definition**: Define the market boundaries — what problem space, which customer segments, what geography or constraints apply
2. **Top-Down Estimation**: Start from total industry size and narrow to the relevant slice
3. **Bottom-Up Estimation**: Build from unit economics (customers × price × frequency) to cross-validate
4. **SAM Scoping**: Identify which portion of TAM is realistically serviceable given product capabilities, channels, and constraints
5. **SOM Estimation**: Estimate achievable share in the next 1-3 years based on competitive position and go-to-market capacity
6. **Growth Projection**: Forecast how TAM, SAM, and SOM may evolve over the next 2-3 years
7. **Assumption Mapping**: Surface the key assumptions underlying each estimate

### Output Structure

**Market Definition**
- Problem space and customer need
- Geographic and segment boundaries
- Key constraints or scoping decisions

**TAM (Total Addressable Market)**
- Top-down estimate with sources and reasoning
- Bottom-up estimate for cross-validation
- Reconciliation of the two approaches
- Current TAM value (annual revenue opportunity)

**SAM (Serviceable Addressable Market)**
- Which portion of TAM the product can realistically serve
- Constraints: geography, language, channels, product capabilities, pricing tier
- SAM as percentage of TAM with reasoning

**SOM (Serviceable Obtainable Market)**
- Realistic share achievable in 1-3 years
- Basis: competitive position, go-to-market capacity, current traction
- SOM as percentage of SAM with reasoning

**Market Summary Table**

| Metric | Current Estimate | 2-3 Year Projection |
|--------|-----------------|---------------------|
| TAM    |                 |                     |
| SAM    |                 |                     |
| SOM    |                 |                     |

**Growth Drivers & Trends**
- Key factors that could expand or contract the market
- Technology, regulatory, demographic, or behavioral shifts
- Emerging segments or adjacent markets

**Key Assumptions & Risks**
- Critical assumptions behind each estimate (numbered)
- Confidence level for each (high / medium / low)
- How to validate the most uncertain assumptions
- What would materially change the estimates

## Best Practices

- Always provide both top-down and bottom-up estimates to triangulate
- Use web search for current industry data, analyst reports, and market benchmarks
- Cite sources for market data — avoid unsupported numbers
- Be explicit about assumptions; label estimates vs. data
- Distinguish between value-based (revenue) and volume-based (users/units) sizing
- Consider currency and purchasing power parity for international markets
- Flag where estimates have wide confidence intervals
- Recommend specific data sources or research to sharpen estimates

---

### Further Reading

- [Market Research: Advanced Techniques](https://www.productcompass.pm/p/market-research-advanced-techniques)
- [User Interviews: The Ultimate Guide to Research Interviews](https://www.productcompass.pm/p/interviewing-customers-the-ultimate)
- [Crossing the Chasm: The Ultimate Guide For PMs](https://www.productcompass.pm/p/crossing-the-chasm)
- [Product Innovation Masterclass](https://www.productcompass.pm/p/product-innovation-masterclass) (video course)
