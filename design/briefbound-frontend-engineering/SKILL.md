---
name: briefbound-frontend-engineering
description: Use when an aligned UI contract or established project pattern needs production frontend implementation across components, layouts, interaction states, responsive behavior, accessibility, or runtime browser verification; do not use when the primary uncertainty is product direction, visual identity, design-system governance, or review-only findings.
license: MIT
---

# Briefbound Frontend Engineering

## 目标

把已对齐的界面契约实现为符合项目约定、状态完整且可在浏览器验证的前端代码。优先复用现有组件、token 和数据契约，不重新发明视觉方向。

## Briefbound task contract

- Context Boundary: 已对齐的用户结果、目标页面或组件、`APPROVED/PREVIEW_SKIPPED` 证据、现有设计系统与相邻实现、技术栈、数据契约和可运行环境。
- Output Contract: 最小生产实现、关键状态覆盖、响应式与无障碍处理，以及与声明相称的运行时证据。
- Allowed Action: 在 Briefbound Router 授权 surface 内修改前端组件、样式和必要测试；不改变无关后端协议、品牌方向或全局设计系统。
- Success Evidence: 目标测试、类型或构建检查，以及真实浏览器中的主路径、关键状态、目标视口和 console 检查。
- Stop Condition: 命中 `PREVIEW_REQUIRED` 但缺少用户 `APPROVED`、界面结果仍有高影响歧义、需要新的产品/视觉方向、数据契约不可用、修改越过授权边界，或运行环境阻止关键验收。
- Route Out: 产品或交互分叉转 `briefbound-ui-design`；跨消费者 token、主题或共享组件治理转 `briefbound-design-system`；复杂外部组件决策转 `briefbound-feature-reuse-research`；验证后的真实残留转 `briefbound-development-cleanup`；阻塞回 `briefbound-router`。

## 统一调用契约

- 只处理 Briefbound task contract 范围；不匹配时回 `briefbound-router` 或最具体 owner。
- 用户可见内容默认中文，只报告关键实现、证据和剩余风险；代码、命令、路径、错误原文、API/协议、skill 名和枚举保留原样；Route Out 仅以 Briefbound task contract 为准；有自然闸门时末行 `下一步建议: <一个具体动作>`，否则声明继续已授权工作。

## 实施边界

- 只在进入时已有用户 `APPROVED`，或有依据的 `PREVIEW_SKIPPED`，或收到包含该证据的独立 handoff 时主责。设计 owner 正在同一上下文执行“设计并实现”时不叠加本 skill。
- `FAST_PATH`：既有模式下的明确小修，记录 `PREVIEW_SKIPPED` 依据后直接实现；`COMPACT_FLOW` 必须消费已批准预览/设计。
- 出现跨页面信息架构、品牌方向或设计系统治理时停止扩张，转对应 owner。

## 预览证据闸门

- 新页面或未确认的布局、交互、视觉、响应式、跨组件结果：`PREVIEW_REQUIRED`，转设计 owner 生成隔离网页。
- 明确小修或既有模式机械改动：记录 `PREVIEW_SKIPPED`；用户已明确批准具体预览或设计稿：记录 `APPROVED` 对象与边界。
- 截图、测试、UI Review 或一般“继续实现”不能替代对具体预览的用户批准；实现偏离时重新预览。

## 条件操作指南

先用依赖、样式入口和组件配置确认技术栈：

- 使用 Tailwind CSS：实施前读取 [references/tailwind.md](references/tailwind.md)。
- 使用 shadcn/ui 或存在 `components.json`：实施前读取 [references/shadcn.md](references/shadcn.md)；两者命中则都读取。
- 指南不新增 owner、依赖、迁移权限或预览豁免。版本、项目定制或 CLI 冲突以项目事实和官方当前文档为准；解决方案若改变依赖、主题、组件 API、兼容性或批准结果，停止受影响写入并与用户讨论。

## 生产实现

1. 读取 owning component、相邻页面、组件库、token、数据流和相关测试，确认项目真实模式。
2. 选择满足契约的最小结构；组件只在形成稳定复用边界或显著降低复杂度时拆分。
3. 覆盖主路径及相关的 loading、empty、error、disabled、success、权限和长内容状态，不凭空增加无关状态。
4. 使用语义元素和原生控件，保证标签、键盘路径、焦点、非颜色提示和必要 ARIA；保留现有无障碍基线。
5. 使用现有响应式策略和 token，稳定固定格式元素的尺寸，检查换行、溢出、窄屏降级和动态内容。
6. 保持服务端/客户端边界、请求缓存、状态所有权和渲染成本符合当前框架约定；性能优化必须针对可观察问题。

避免为了“更工程化”引入新的组件层、状态库、样式体系或依赖。没有现成组件的新界面能力，先转 `briefbound-feature-reuse-research` 做 QUICK。

## 验证

- 浏览器验收由最终写入 owner 执行一次，不重复同一 route、状态和视口检查。
- 先运行与改动最接近的测试、类型检查或构建检查；不机械运行全仓命令。
- 可运行时使用本轮 Available skills 中的浏览器能力验证目标 route。至少检查主路径、受影响状态、相关桌面/移动视口、console 和明显溢出。
- 截图只证明当时的视觉状态；交互、网络和状态同步需要对应运行证据。无法启动应用时明确列出未验证面。
- 实际结果不符合界面契约时先判断是实现、契约、环境还是数据问题，不通过削弱用户行为来换取测试通过。

有自然闸门时正文末行为 `下一步建议: <一个具体动作>`；否则继续已授权工作。
