---
name: business-metrics-dashboard
description: "Define and design a product metrics dashboard with key metrics, data sources, visualization types, and alert thresholds. Use when creating a metrics dashboard, defining KPIs, setting up product analytics, or building a data monitoring plan."
---

## App 执行约定

先读取本技能正文及任务所需的本地参考资源。使用中文；工作目录由任务提供，仅读取用户提供、当前任务授权的资料。正文中的 `$ARGUMENTS` 及斜杠命令表示用户任务输入，不调用 Claude 专用命令。`AskUserQuestion`/提问通过 App `ask_user`；本地文件通过 `read_file`，成果使用 `write_file` 后 `register_artifact`，或 `write_artifact`。相对资源路径以本 SKILL.md 所在目录为起点。若技能读取结果含目录，按该目录构建资源绝对路径。

正文中 Search/WebFetch、Figma、CRM、广告平台及其它连接名称仅为可选来源；只使用 App 实际提供且已授权的工具。没有连接时从上传材料完成流程，把缺少的外部验证列出，不安装运行时插件或扫描用户全局配置。默认输出 Markdown/CSV 草稿；Office、图表、HTML、PNG 或图像生成只在对应工具和运行库可用时执行。不得擅自发送邮件、发表内容、签约、创建发票、修改线上商品或花费广告预算。

## Product Metrics Dashboard

Design a comprehensive product metrics dashboard with the right metrics, visualizations, and alert thresholds.

### Context

You are designing a metrics dashboard for **$ARGUMENTS**.

If the user provides files (existing dashboards, analytics data, OKRs, or strategy docs), read them first.

### Domain Context

**Metrics vs KPIs vs NSM**: Metrics = all measurable things. KPIs = a few key quantitative metrics tracked over a longer period. North Star Metric = a single customer-centric KPI that is a leading indicator of business success.

**4 criteria for a good metric** (Ben Yoskovitz, *Lean Analytics*): (1) Understandable — creates a common language. (2) Comparative — over time, not a snapshot. (3) Ratio or Rate — more revealing than whole numbers. (4) Behavior-changing — the Golden Rule: "If a metric won't change how you behave, it's a bad metric."

**8 metric types**: Vanity vs Actionable (only actionable metrics change behavior), Qualitative vs Quantitative (WHAT vs WHY — you need both; never stop talking to customers), Exploratory vs Reporting (explore data to uncover unexpected insights), Lagging vs Leading (leading indicators enable faster learning cycles, e.g. customer complaints predict churn).

**5 action steps**: (1) Audit metrics against the 4 good-metric criteria. (2) Update dashboards — ensure all key metrics are good ones. (3) Identify vanity metrics — be careful how you use them. (4) Classify leading vs lagging indicators. (5) Pick one problem and dig deep into the data.

For case studies and more detail: [Are You Tracking the Right Metrics?](https://www.productcompass.pm/p/are-you-tracking-the-right-metrics) by Ben Yoskovitz

### Instructions

1. **Identify the metrics framework** — organize metrics into layers:

   **North Star Metric**: The single metric that best captures core value delivery

   **Input Metrics** (3-5): The levers that drive the North Star

   **Health Metrics**: Guardrails that ensure overall product health

   **Business Metrics**: Revenue, cost, and unit economics

2. **For each metric, define**:

   | Metric | Definition | Data Source | Visualization | Target | Alert Threshold |
   |---|---|---|---|---|---|
   | [Name] | [Exact calculation: numerator/denominator, time window] | [Where the data comes from] | [Line chart / Bar / Number / Funnel] | [Goal value] | [When to trigger an alert] |

3. **Design the dashboard layout**:

   ```
   ┌─────────────────────────────────────────────┐
   │  NORTH STAR: [Metric] — [Current Value]     │
   │  Trend: [↑/↓ X% vs last period]             │
   ├──────────────────┬──────────────────────────┤
   │  Input Metric 1  │  Input Metric 2          │
   │  [Sparkline]     │  [Sparkline]             │
   ├──────────────────┼──────────────────────────┤
   │  Input Metric 3  │  Input Metric 4          │
   │  [Sparkline]     │  [Sparkline]             │
   ├──────────────────┴──────────────────────────┤
   │  HEALTH: [Latency] [Error Rate] [NPS]       │
   ├─────────────────────────────────────────────┤
   │  BUSINESS: [MRR] [CAC] [LTV] [Churn]        │
   └─────────────────────────────────────────────┘
   ```

4. **Set review cadence**:
   - **Daily**: Operational health (errors, latency, critical flows)
   - **Weekly**: Input metrics and engagement trends
   - **Monthly**: North Star, business metrics, OKR progress
   - **Quarterly**: Strategic review and metric recalibration

5. **Define alerts**:
   - What thresholds trigger investigation?
   - Who gets alerted and through what channel?
   - What's the expected response time?

6. **Recommend tools** based on the user's context:
   - Amplitude, Mixpanel, PostHog for product analytics
   - Looker, Metabase, Mode for SQL-based dashboards
   - Datadog, Grafana for operational health

Think step by step. Save the dashboard specification as a markdown document.

---

### Further Reading

- [The Ultimate List of Product Metrics](https://www.productcompass.pm/p/the-ultimate-list-of-product-metrics)
- [The North Star Framework 101](https://www.productcompass.pm/p/the-north-star-framework-101)
- [The Product Analytics Playbook: AARRR, HEART, Cohorts & Funnels for PMs](https://www.productcompass.pm/p/the-product-analytics-playbook-aarrr)
- [AARRR (Pirate) Metrics: The 5-Stage Framework for Growth](https://www.productcompass.pm/p/aarrr-pirate-metrics)
- [The Google HEART Framework: Your Guide to Measuring User-Centric Success](https://www.productcompass.pm/p/the-google-heart-framework)
- [Funnel Analysis 101: How to Track and Optimize Your User Journey](https://www.productcompass.pm/p/funnel-analysis)
- [Are You Tracking the Right Metrics?](https://www.productcompass.pm/p/are-you-tracking-the-right-metrics)
- [Continuous Product Discovery Masterclass (CPDM)](https://www.productcompass.pm/p/cpdm) (video course)
