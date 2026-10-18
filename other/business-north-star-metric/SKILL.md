---
name: business-north-star-metric
description: "Define a North Star Metric and 3-5 supporting input metrics that form a metrics constellation. Classify the business game (Attention, Transaction, Productivity) and validate against 7 criteria for an effective North Star. Use when choosing a North Star Metric, setting up a metrics framework, learning about the North Star Framework, or deciding what to measure."
---

## App 执行约定

先读取本技能正文及任务所需的本地参考资源。使用中文；工作目录由任务提供，仅读取用户提供、当前任务授权的资料。正文中的 `$ARGUMENTS` 及斜杠命令表示用户任务输入，不调用 Claude 专用命令。`AskUserQuestion`/提问通过 App `ask_user`；本地文件通过 `read_file`，成果使用 `write_file` 后 `register_artifact`，或 `write_artifact`。相对资源路径以本 SKILL.md 所在目录为起点。若技能读取结果含目录，按该目录构建资源绝对路径。

正文中 Search/WebFetch、Figma、CRM、广告平台及其它连接名称仅为可选来源；只使用 App 实际提供且已授权的工具。没有连接时从上传材料完成流程，把缺少的外部验证列出，不安装运行时插件或扫描用户全局配置。默认输出 Markdown/CSV 草稿；Office、图表、HTML、PNG 或图像生成只在对应工具和运行库可用时执行。不得擅自发送邮件、发表内容、签约、创建发票、修改线上商品或花费广告预算。

# North Star Metric

Identify a North Star Metric and 3-5 Input Metrics that form a metrics constellation. Classifies the business game being played and validates against criteria for an effective North Star. Use when defining key metrics, setting up a metrics framework, or choosing what to measure.

## Domain Context

NSM is **NOT**: multiple metrics, a revenue/LTV metric (must be customer-centric), an OKR (that's a goal-setting technique), or a strategy (but choosing the right NSM is a strategic choice).

NSM **IS**: a single, customer-centric KPI that reflects the value customers get from the product and serves as a leading indicator of long-term business success. You can use Key Results (OKRs) to express expected change in NSM.

Free resource: [The North Star Framework 101 (PDF)](https://learn.productcompass.pm/nsm101)

## When to Use

- Defining your company's key metric framework
- Setting up a metrics tracking system
- Choosing what to measure and optimize for
- Evaluating potential North Star candidates
- Triggers: North Star metric, north star, key metric, what to measure, metrics framework, OMTM

## The Three Business Games

Before identifying your North Star, classify your business into one of these three games:

- **Attention Game**: How much time do customers spend using your product? (Examples: Facebook, Spotify, YouTube, TikTok)
- **Transaction Game**: How many transactions occur between customers and your platform? (Examples: Amazon, Uber, Airbnb, PayPal)
- **Productivity Game**: How efficiently can someone complete their work or achieve their goals? (Examples: Canva, Dropbox, Loom, Notion)

## Prompt

You are a metrics strategist specializing in North Star metrics and growth measurement frameworks.

Given the following business context: $ARGUMENTS

**Step 1: Classify the Business Game**
Determine which game this company plays: Attention, Transaction, or Productivity.

**Step 2: Identify the North Star Metric**
Suggest a single metric that meets all seven criteria for an effective North Star:

1. **Easy to Understand**: Clear definition that everyone in the organization comprehends
2. **Customer-Centric**: Reflects value delivered to customers, not just revenue or activity
3. **Sustainable Value**: Indicates habits and long-term customer engagement
4. **Vision Alignment**: Represents meaningful progress toward the company's vision and mission
5. **Quantitative**: Measurable with clear, numeric tracking
6. **Actionable**: Teams can directly influence it through product, marketing, and operational changes
7. **Leading Indicator**: Predicts future business success and revenue growth

**Step 3: Identify Input Metrics**
Define 3-5 Input Metrics (also called leading indicators) that most directly influence and drive the North Star Metric. Each input metric should:
- Be easier to move in the short term
- Directly contribute to the North Star outcome
- Help identify where optimization efforts should focus

## Tips for Best Results

- Provide details about your business model and revenue model
- Share your company's vision, mission, or long-term goals
- Include current metrics you're tracking
- Mention key customer segments and use cases
- Describe the primary value you deliver to customers

---

### Further Reading

- [The North Star Framework 101](https://www.productcompass.pm/p/the-north-star-framework-101)
- [AARRR (Pirate) Metrics: The 5-Stage Framework for Growth](https://www.productcompass.pm/p/aarrr-pirate-metrics)
- [The Google HEART Framework: Your Guide to Measuring User-Centric Success](https://www.productcompass.pm/p/the-google-heart-framework)
- [The Ultimate List of Product Metrics](https://www.productcompass.pm/p/the-ultimate-list-of-product-metrics)
