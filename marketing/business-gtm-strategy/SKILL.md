---
name: business-gtm-strategy
description: "Create a go-to-market strategy covering marketing channels, messaging, success metrics, and launch timeline. Use when planning a product launch, creating a GTM plan from scratch, or defining a launch strategy for a new market."
---

## App 执行约定

先读取本技能正文及任务所需的本地参考资源。使用中文；工作目录由任务提供，仅读取用户提供、当前任务授权的资料。正文中的 `$ARGUMENTS` 及斜杠命令表示用户任务输入，不调用 Claude 专用命令。`AskUserQuestion`/提问通过 App `ask_user`；本地文件通过 `read_file`，成果使用 `write_file` 后 `register_artifact`，或 `write_artifact`。相对资源路径以本 SKILL.md 所在目录为起点。若技能读取结果含目录，按该目录构建资源绝对路径。

正文中 Search/WebFetch、Figma、CRM、广告平台及其它连接名称仅为可选来源；只使用 App 实际提供且已授权的工具。没有连接时从上传材料完成流程，把缺少的外部验证列出，不安装运行时插件或扫描用户全局配置。默认输出 Markdown/CSV 草稿；Office、图表、HTML、PNG 或图像生成只在对应工具和运行库可用时执行。不得擅自发送邮件、发表内容、签约、创建发票、修改线上商品或花费广告预算。

# GTM Strategy

## Overview
Create a comprehensive go-to-market strategy for a product launch. This skill covers marketing channels, messaging development, success metrics definition, and launch planning.

## When to Use
- Planning a product launch
- Creating a GTM plan from scratch
- Defining a launch strategy for a new market
- Developing product-to-market fit strategy
- Preparing a product go-live roadmap

## How It Works

### Step 1: Gather Research Data
The system will help you load and analyze early research about your product and target market. Provide:
- Product description and key features
- Target market segment details
- Market research or validation data
- Competitive landscape information
- Any available customer interviews or survey data

### Step 2: Define Marketing Channels
Evaluate which channels best reach your target audience:
- Digital marketing channels (paid search, social media, display)
- Content and inbound channels (blog, SEO, thought leadership)
- Sales and outbound channels (direct outreach, partnerships)
- Community and grassroots channels
- Product-led and viral channels

### Step 3: Develop Messaging
Create audience-specific messaging that resonates:
- Core value proposition for target segment
- Key differentiators and competitive advantages
- Pain point validation and solution mapping
- Proof points and social proof strategies
- Channel-specific messaging variations

### Step 4: Define Success Metrics
Establish measurable KPIs to track launch success:
- Awareness metrics (impressions, reach, brand recall)
- Engagement metrics (CTR, cost per engagement, time on site)
- Conversion metrics (signups, demos requested, trials started)
- Revenue metrics (MRR, customer acquisition cost, lifetime value)
- Market metrics (market share, segment penetration)

### Step 5: Create Launch Plan
Build a phased launch timeline:
- Pre-launch preparation (messaging, channels, timeline)
- Launch day activities and announcements
- Post-launch momentum (content, partnerships, communities)
- Measurement and optimization cadence
- Success criteria and go/no-go decision points

## Input Format
Use $ARGUMENTS to pass:
- Product name and description
- Target market segment
- Research data or file path
- Launch timeline and constraints
- Budget or resource limitations

## Output
A structured GTM strategy document including:
- Recommended marketing channels with justification
- Channel-specific messaging and positioning
- Launch timeline with key milestones
- KPI targets and measurement framework
- Risk mitigation strategies
- 90-day execution roadmap

## Framework
This skill applies Product Compass GTM strategy methodology, focusing on market selection, channel fit, and message-market fit for sustainable product growth.

## Tips
- Start with your most confident customer segment
- Validate assumptions through customer interviews before full launch
- Focus on a few channels excellently rather than many channels poorly
- Establish baseline metrics before launch to measure impact
- Plan for feedback loops and optimization

---

### Further Reading

- [5 GTM Principles You Should Know as a PM](https://www.productcompass.pm/p/5-gtm-principles-with-frameworks-templates)
- [OpenAI’s Product Leader Shares 3-Layer Distribution Framework To Win Mind & Market Share in the AI World](https://www.productcompass.pm/p/distribution-framework-ai-products)
- [Product-Led Growth 101, Part 1/2](https://www.productcompass.pm/p/product-led-growth-101-12)
- [How to Design a Value Proposition Customers Can't Resist?](https://www.productcompass.pm/p/how-to-design-value-proposition-template)
- [How to Achieve Product-Market Fit? Part I: Market and Value Proposition](https://www.productcompass.pm/p/how-to-achieve-the-product-market)
