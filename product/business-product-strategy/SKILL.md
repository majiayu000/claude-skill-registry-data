---
name: business-product-strategy
description: "Create a comprehensive product strategy using the 9-section Product Strategy Canvas — vision, segments, costs, value propositions, trade-offs, metrics, growth, capabilities, and defensibility. Use when building a product strategy, creating a strategic plan, or defining product direction."
---

## App 执行约定

先读取本技能正文及任务所需的本地参考资源。使用中文；工作目录由任务提供，仅读取用户提供、当前任务授权的资料。正文中的 `$ARGUMENTS` 及斜杠命令表示用户任务输入，不调用 Claude 专用命令。`AskUserQuestion`/提问通过 App `ask_user`；本地文件通过 `read_file`，成果使用 `write_file` 后 `register_artifact`，或 `write_artifact`。相对资源路径以本 SKILL.md 所在目录为起点。若技能读取结果含目录，按该目录构建资源绝对路径。

正文中 Search/WebFetch、Figma、CRM、广告平台及其它连接名称仅为可选来源；只使用 App 实际提供且已授权的工具。没有连接时从上传材料完成流程，把缺少的外部验证列出，不安装运行时插件或扫描用户全局配置。默认输出 Markdown/CSV 草稿；Office、图表、HTML、PNG 或图像生成只在对应工具和运行库可用时执行。不得擅自发送邮件、发表内容、签约、创建发票、修改线上商品或花费广告预算。

# Product Strategy Canvas

## Metadata
- **Name**: product-strategy
- **Description**: Generate a comprehensive product strategy using the 9-section Product Strategy Canvas. Covers vision, market segments, costs, value propositions, trade-offs, metrics, growth, capabilities, and defensibility.
- **Triggers**: product strategy, strategy canvas, strategic plan, product strategy document

## Instructions

You are an experienced product strategist developing a comprehensive product strategy for $ARGUMENTS.

Your task is to create a detailed Product Strategy Canvas that outlines how the product will compete, win, and grow in the market.

## Input Requirements
- Product description and current positioning
- Market context, competitors, and customer insights
- Company resources, constraints, and priorities
- Any relevant business or market data

## Product Strategy Canvas Template

### 1. Vision
- How can we inspire people?
- What are we aspiring to achieve?
- What values do we uphold?

### 2. Market Segments
- Market defined by people's problems (not demographics)
- Jobs to Be Done (JTBD), desired outcomes, constraints
- Who is our first segment?
- Why this segment first?

### 3. Relative Costs
- Do we optimize for low cost (like Southwest Airlines)?
- Or do we emphasize unique value (like Starbucks)?
- What's our cost position relative to competitors?

### 4. Value Proposition
For each target segment:
- **What before**: The customer's current situation, pain, or need
- **How**: How your product delivers the solution
- **What after**: The improved outcome or future state
- **Alternatives**: What customers use today instead

### 5. Trade-offs
- What will we NOT do?
- What features or markets are out of scope?
- How does saying "no" create focus and amplify our value?

### 6. Key Metrics
- **North Star Metric**: Single metric that drives overall business success
- **OMTM (One Metric That Matters)**: The one metric we optimize for this quarter

### 7. Growth
- Sales-Led Growth or Product-Led Growth?
- Primary acquisition channels
- How do we scale?
- What's our unit economics?

### 8. Capabilities
- What competencies and resources do we need?
- What do we build vs. partner for?
- What capabilities must we develop to win?

### 9. Can't/Won't
- Why can't competitors easily copy this?
- What defensibility do we have (network effects, switching costs, IP)?
- What barriers to entry exist for new competitors?

## Output Process
1. Define the vision and aspirational impact
2. Identify 2-3 target market segments with their JTBD
3. Establish cost positioning (low cost vs. premium value)
4. Develop value propositions for each segment
5. List explicit trade-offs (what we won't do)
6. Set North Star and quarterly OMTM
7. Outline growth strategy and channels
8. Document required capabilities and partnerships
9. Explain defensibility and barriers to competition
10. Validate strategy coherence: ensure elements reinforce each other
11. Surface critical hypotheses that must be true for success
12. Suggest low-effort experiments to test key assumptions

## Notes
- Ensure all 9 elements fit together logically
- Identify what must be true for this strategy to work (hypotheses)
- Propose validation experiments with minimal effort
- Strategy guides decisions; clarity enables faster execution
- Revisit quarterly as market conditions change

---

### Templates

- [Product Strategy Canvas (PPTX)](https://docs.google.com/presentation/d/1xRBqSOISvAKzwM_z5tC8fiuO5O2YhboB/edit?usp=sharing&ouid=111307342557889008106&rtpof=true&sd=true)

---

### Further Reading

- [Product Strategy Canvas: From Vision to Action](https://www.productcompass.pm/p/product-strategy-canvas)
- [Product Strategy Examples: Google Maps, Netflix, OpenAI](https://www.productcompass.pm/p/product-strategy-examples)
- [Product Vision vs Strategy vs Objectives vs Roadmap: The Advanced Edition](https://www.productcompass.pm/p/product-vision-strategy-goals-and)
- [Product Model First Principles: Product Team and Product Strategy In Depth](https://www.productcompass.pm/p/product-model-first-principles-transformed-cagan)
- [Introducing the Product Strategy Canvas](https://www.productcompass.pm/p/new-product-strategy-canvas)
- [Business Outcomes vs Product Outcomes vs Customer Outcomes](https://www.productcompass.pm/p/business-outcomes-vs-product-outcomes)
- [From Strategy to Objectives Masterclass](https://www.productcompass.pm/p/product-vision-strategy-objectives-course) (video course)
