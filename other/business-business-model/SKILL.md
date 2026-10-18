---
name: business-business-model
description: "Generate a Business Model Canvas with all 9 building blocks. Use when creating a business model, documenting how a business creates value, or analyzing an existing business model."
---

## App 执行约定

先读取本技能正文及任务所需的本地参考资源。使用中文；工作目录由任务提供，仅读取用户提供、当前任务授权的资料。正文中的 `$ARGUMENTS` 及斜杠命令表示用户任务输入，不调用 Claude 专用命令。`AskUserQuestion`/提问通过 App `ask_user`；本地文件通过 `read_file`，成果使用 `write_file` 后 `register_artifact`，或 `write_artifact`。相对资源路径以本 SKILL.md 所在目录为起点。若技能读取结果含目录，按该目录构建资源绝对路径。

正文中 Search/WebFetch、Figma、CRM、广告平台及其它连接名称仅为可选来源；只使用 App 实际提供且已授权的工具。没有连接时从上传材料完成流程，把缺少的外部验证列出，不安装运行时插件或扫描用户全局配置。默认输出 Markdown/CSV 草稿；Office、图表、HTML、PNG 或图像生成只在对应工具和运行库可用时执行。不得擅自发送邮件、发表内容、签约、创建发票、修改线上商品或花费广告预算。

本技能补充约定：LTV/CAC>3 仅是部分订阅业务的经验参照，不构成所有商业模式的可行性门槛。判断还需回收期、毛利和资金约束。

# Business Model Canvas

## Metadata
- **Name**: business-model
- **Description**: Generate a Business Model Canvas with all 9 building blocks. Use when creating a business model, documenting how a business creates value, or analyzing an existing business model.
- **Triggers**: business model canvas, BMC, business model, how we make money

## Instructions

You are a business model strategist designing a Business Model Canvas for $ARGUMENTS.

Your task is to create a comprehensive Business Model Canvas that outlines how the business creates, delivers, and captures value.

## Input Requirements
- Product or service description
- Target customer(s) and market
- Current business operations or assumptions
- Competitive context or industry dynamics

## Business Model Canvas Template

### Left Side: Creating Value

**1. Key Partners**
- Who are the key strategic partners and suppliers?
- What partnerships enable our business model?
- Which activities do partners handle?
- Are there joint ventures or co-creation opportunities?

**2. Key Activities**
- What key activities does the business perform?
- What processes are critical to delivering value?
- Are these activities in-house or outsourced?
- Production, problem-solving, platform/network activities?

**3. Key Resources**
- What resources are necessary to create value?
- Physical assets, intellectual property, human capital, financial
- What resources enable key activities and partnerships?
- What's the minimum viable resource set?

### Center: The Value Proposition

**4. Value Propositions**
- What value do we deliver to customers?
- Which customer problems do we solve?
- What needs are satisfied?
- What products/services address each segment?
- Quantitative (price, speed, quality) vs. qualitative (design, status)

### Right Side: Delivering Value

**5. Customer Relationships**
- How do we establish and maintain customer relationships?
- Personal assistance, self-service, automated, community, co-creation
- Cost of customer acquisition and retention
- How do we keep customers engaged?

**6. Channels**
- How do customers discover and access the value?
- Awareness: How do customers learn about us?
- Purchase: How do they buy?
- Delivery: How is value delivered?
- After-sales: How do we support customers?
- Direct vs. indirect, owned vs. partner channels

**7. Customer Segments**
- Who are the key customer segments?
- Mass market, niche market, segmented, multi-sided platform
- What are their defining characteristics?
- Distinct needs, channels, relationships, or profitability

### Bottom: Financial Viability

**8. Cost Structure**
- What are the most important costs?
- Fixed vs. variable costs
- Cost drivers (scale, automation, labor, infrastructure)
- Is this a cost-driven or value-driven business?

**9. Revenue Streams**
- How does the business make money?
- Per customer, per transaction, subscription, licensing, rents
- Pricing mechanisms (fixed, dynamic, value-based)
- Customer lifetime value and unit economics

## Output Process
1. Identify and profile customer segments
2. Define the core value proposition(s)
3. Map customer relationships and channels
4. List key activities and resources
5. Identify key partners
6. Outline cost structure
7. Define revenue streams
8. Ensure all 9 blocks align and support each other
9. Test economic viability (LTV > 3x CAC)
10. Identify key assumptions and risks

### Domain Context

**Business Model Canvas vs Lean Canvas vs Startup Canvas**:

Business Model Canvas (Strategyzer, Alexander Osterwalder) is the most widely used canvas framework. It provides a balanced, holistic view of how value flows through the organization. However, it has known limitations for product strategy:

- **No vision**: Why should your team wake up every day? BMC doesn't address motivation or aspiration.
- **No Can't/Won't test**: What stops competitors from copying you? BMC lacks a defensibility section that goes beyond listing resources.
- **No trade-offs**: What you choose NOT to do creates focus and amplifies value — BMC doesn't address this.
- **No key metrics**: How do you know the strategy is working? BMC has no metrics section.
- **Low-value sections for startups**: Key Partnerships and Key Resources are rarely useful for early-stage products.

**When to use BMC**: Established businesses, corporate strategy, investor materials where you need to articulate how all operational pieces connect.

**Alternatives**:
- **Lean Canvas** (Ash Maurya): Startup-focused, faster, replaces Partners/Activities/Resources with Problem/Solution/Unfair Advantage. Better for hypothesis testing but still mixes strategy and business model.
- **Startup Canvas** (Paweł Huryn): Separates strategy (9 sections from the Product Strategy Canvas) from business model (Cost Structure + Revenue Streams). Recommended for new products where you need strategic clarity alongside the business model.

## Notes
- The Business Model Canvas provides a holistic view of how value flows through the organization
- Each block should reinforce and support the others
- Strong business models have clear, defensible value propositions
- Financial sustainability requires revenue to exceed costs at scale
- Use this to identify opportunities for innovation and optimization

---

### Further Reading

- [Business Model Canvas Examples: Google Maps, Airbnb, Uber](https://www.productcompass.pm/p/business-model-canvas-examples)
- [Startup Canvas: Product Strategy and a Business Model for a New Product](https://www.productcompass.pm/p/startup-canvas)
