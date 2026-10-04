---
name: competitive-analysis
description: >
  竞品决策分析 / Competitive Decision Brief：当用户要调研竞品、替代方案、新产品、SaaS/AI 产品或市场信号，
  并希望把官网、定价、评论、文档、更新日志、登录态走查、截图或浏览器取证转成产品定位、路线图、定价、
  功能优先级、差异化、Go/No-Go 或 PRD 输入时使用。核心行为是先锚定产品决策，再选择证据渠道，
  最后输出可行动的 Product Decision Brief；不要把它降级成泛泛功能清单、纯 UX 走查或“点完所有按钮”报告。
---

# 竞品决策分析 Skill（competitive-analysis）

## 中文速查

- 中文名：竞品决策分析 / 竞品决策简报
- 英文稳定名：`competitive-analysis`
- 分类：决策调研 / 产品研究
- 你可以这样叫我：`帮我做竞品分析`、`研究下这个新产品对我们有什么启发`、`打开这个产品看看对产品决策有什么用`、`分析 Krowork 这类产品`、`把竞品信息转成 PRD 输入`
- 适合：围绕一个产品决策，把竞品、替代方案、市场信号和可选产品走查转成路线图、定位、定价、功能优先级、差异化或 Go/No-Go 输入。
- 不适合：问题还没定义清楚（先用 `ai-collaboration-calibration`）；只想建立长期主题认知或候选池（用 `research-topic-compiler`）；已经只有 A/B/C 最终选择（用 `decision-research`）；只要 UI 高保真参考（用 `ui-mockup-desktop-workbench`）。

## 核心原则

**竞品分析服务产品决策，不服务信息完整性。**

不要把“打开网站、登录、点完功能”当作目标。产品走查只是证据渠道之一。真正要回答的是：

- 我们该学什么？
- 我们该避开什么？
- 我们需要验证什么？
- 这会改变我们的产品路线、定位、定价或优先级吗？

如果用户只给了一个竞品 URL，先把它改写成决策问题，再决定是否需要浏览器、截图、登录态或外部评论渠道。

## 启动协议

先判断用户的请求处在哪一层：

| 层级 | 用户表述 | 处理方式 |
| --- | --- | --- |
| 取证层 | “打开这个网址点一下所有功能” | 追问或推断它服务什么产品决策；走查只是可选证据渠道。 |
| 产品层 | “这个产品对我们有什么启发” | 进入本 Skill，输出 Product Decision Brief。 |
| 决策层 | “我们要不要做这个方向 / 学它的定价 / 改路线图” | 进入本 Skill；若只剩最终选择，交给 `decision-research`。 |
| 研究层 | “系统研究这个赛道，先沉淀一批竞品” | 交给 `research-topic-compiler` 的 Product Candidate Research。 |

最多问 3 个启动问题；能从用户上下文、URL、仓库文档或已有 PRD 推断的，不要打断：

1. 这次竞品分析要影响哪个产品决策？
2. 我方产品、目标用户、当前阶段是什么？
3. 是否允许使用登录态、截图、浏览器自动化或用户账号？如果没有明确授权，只用公开信息。

## 工作流

1. **决策锚定**
   - 把请求转成一句 `decision_question`。
   - 写清 `current_product_context`、`decision_owner`、`time_budget` 和 `decision_deadline`，未知就标为假设。
   - 如果没有决策问题，先用 `ai-collaboration-calibration` 校准，不直接开始搜索。

2. **竞品边界定义**
   - 区分 direct competitor、workflow alternative、status quo、adjacent inspiration。
   - 如果用户只给一个产品，补充“它代表哪类替代方案”的推断。
   - 如果目标是候选池，转 `research-topic-compiler`；本 Skill 可消费候选池做决策简报。

3. **证据渠道选择**
   - 读取 `references/evidence-channel-guide.md`。
   - 不要默认所有渠道全开；按决策问题选择 3-6 个高价值渠道。
   - 将产品走查、浏览器截图、OAuth 登录和 Computer Use 视为 `Product Walkthrough Evidence`，按 `references/browser-walkthrough-boundaries.md` 执行。

4. **证据收集与分级**
   - 官方页面、定价页、文档、changelog、案例、招聘、评论、社区、用户访谈和走查证据分开记录。
   - 每条证据标注：source、date/accessed_at、evidence_level、supports、contradicts、decision_implication。
   - 对动态信息、价格、当前功能、登录流程和评论，必须实时验证并给来源链接或截图路径。

5. **从外部观察转成内部判断**
   - 不输出“竞品有这些功能”就结束。
   - 把观察翻译成我方 taxonomy：用户任务、激活路径、付费触发、协作模型、信息架构、AI 能力边界、信任机制、增长入口、运营负担。
   - 对每个可借鉴点写清：照抄会错在哪里、需要适配的我方上下文、最小验证动作。

6. **生成 Product Decision Brief**
   - 使用 `references/decision-brief-template.md`。
   - 输出必须包含：结论、决策影响、证据强度、建议动作、反证、未知项、下一步验证。
   - 若证据不足，不要用专业包装制造确定性；明确哪些结论只是弱信号。

## 输出合同

默认输出 `Product Decision Brief`，而不是普通竞品报告。简版结构：

```markdown
**Product Decision Brief**
- Decision question:
- Recommendation:
- Confidence:
- What changes for us:
- Evidence base:
- What to copy / adapt / avoid:
- Product implications:
- Open risks:
- Next validation:
```

需要完整结构时，读取 `references/decision-brief-template.md`。

## 安全与权限边界

- 没有用户明确授权，不要登录账号、使用 OAuth、绕过付费墙、抓取私有内容或自动提交表单。
- 可以阅读公开页面、公开文档、公开评论、公开 changelog 和公开定价。
- 使用用户登录态时，只做最小必要浏览；不要修改数据、邀请用户、创建真实项目、发送消息、购买、删除或导出敏感信息。
- 涉及浏览器自动化、截图、录屏、控制台日志或 Computer Use 时，先读取 `references/browser-walkthrough-boundaries.md`。
- 高风险行业、法律、医疗、金融和合规结论必须标注为产品信号，不给专业法律/医疗/金融意见。

## 与相邻 Skill 的边界

| 用户真正目标 | 用哪个 Skill |
| --- | --- |
| “我还不知道为什么要研究这个竞品” | `ai-collaboration-calibration` |
| “帮我系统研究一个赛道，先沉淀竞品池 / 候选池” | `research-topic-compiler` |
| “围绕这个产品决策，研究竞品并给可行动简报” | `competitive-analysis` |
| “基于这些候选项，最终选 A/B/C” | `decision-research` |
| “把竞品 UI 参考转成项目高保真 mockup/handoff” | `ui-mockup-desktop-workbench` |
| “已有方案，拷问它会不会失败” | `grill-me` |

## Resource Guide

- `references/decision-brief-template.md`：当要输出完整竞品决策简报、证据表和行动清单时读取。
- `references/evidence-channel-guide.md`：当需要选择官网、评论、定价、文档、changelog、招聘、浏览器走查等证据渠道时读取。
- `references/browser-walkthrough-boundaries.md`：当用户要求打开网站、登录、点功能、截图、录屏、使用 Google/OAuth 或 Computer Use 时必须读取。
- `scripts/check_decision_brief.py`：检查 Product Decision Brief 是否包含决策问题、建议、置信度、证据、借鉴 / 避免和下一步验证。

## Definition of Done

一次合格的竞品决策分析必须满足：

- 决策问题明确，不只是产品介绍。
- 证据来源覆盖至少 3 类渠道；如果少于 3 类，说明原因。
- 关键结论有证据等级、反证或置信边界。
- 竞品观察被转译成我方产品动作、验证问题或明确不做项。
- 登录态或浏览器取证的权限、边界和副作用被说明。
- 输出能直接进入 PRD、路线图评审、定价讨论、Go/No-Go 或后续 `decision-research`。

## Evaluation Prompts

- `$competitive-analysis 打开 https://krowork.com 看看这个产品对我们 AI PM 工作台有什么产品决策启发。`
- `$competitive-analysis 研究 Linear、Height、Motion 的 AI 项目管理能力，判断我们要不要做类似路线。`
- `$competitive-analysis 帮我分析这个竞品的定价和 onboarding，输出我们下个版本应该学什么、避开什么。`
- Non-trigger：`系统研究整个 AI 项目管理赛道，先沉淀 20 个候选产品。` 应转 `research-topic-compiler`。
- Non-trigger：`基于这三个方案给我最终选一个。` 应转 `decision-research`。
