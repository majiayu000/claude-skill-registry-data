---
name: briefbound-design-system
description: Use when a frontend task primarily concerns cross-component design tokens, semantic theming, component APIs, variants and states, shared primitives, Storybook or library governance, Figma-to-code consistency, or a staged design-system migration; do not use for a single page, isolated styling fix, visual direction, or review-only task without a systemic ownership problem.
license: MIT
---

# Briefbound Design System

## 目标

建立或修正跨组件可复用的设计契约，让 token、组件 API、variants、主题和设计工具映射拥有清楚的事实源与渐进迁移路径。只治理已证明是系统级的问题，不借设计系统之名重写全部 UI。

## Briefbound task contract

- Context Boundary: 受影响产品 surface、现有 token/主题/组件库、组件消费者、Storybook 或文档、Figma 资源、构建发布方式和迁移约束。
- Output Contract: 最小系统契约、事实源选择、兼容迁移、受影响组件或 token 实现，以及消费者和视觉验证证据。
- Allowed Action: 在授权范围内修改共享 token、主题、组件、文档/Storybook、映射和必要测试；不顺带重新设计产品页面或改变无关业务行为。
- Success Evidence: token/类型/组件测试、代表性消费者验证、主题和 variants 状态检查、浏览器截图或 Figma/code 映射证据，以及迁移兼容性结果。
- Stop Condition: 品牌或产品方向未定、事实源所有权冲突、破坏性迁移缺少授权、消费者范围不可界定，或设计工具权限/环境阻止关键验证。
- Route Out: 产品交互方向转 `briefbound-ui-design`；品牌与视觉语言转 `briefbound-visual-design`；独立页面实现 handoff 转 `briefbound-frontend-engineering`；系统审查转 `briefbound-ui-review`；真实外部库决策转 `briefbound-feature-reuse-research`；验证后的真实残留转 `briefbound-development-cleanup`；阻塞回 `briefbound-router`。

## 统一调用契约

- 只处理 Briefbound task contract 范围；先证明问题跨越多个消费者或共享契约，单点问题返回当前页面 owner。
- 用户可见内容默认中文，只报告系统决策、迁移影响、证据和剩余风险；代码、命令、路径、错误原文、API/协议、skill 名和枚举保留原样；Route Out 仅以 Briefbound task contract 为准；有自然闸门时末行 `下一步建议: <一个具体动作>`，否则声明继续已授权工作。

## 系统闸门

满足至少一项才进入本 owner：

- 同一语义在多个组件或页面出现漂移、重复或硬编码。
- token、主题、组件 API、variants 或状态契约需要新增或迁移。
- Figma variables/components 与代码 token/components 缺少稳定映射。
- 共享组件的改变需要兼容多个消费者、版本或发布边界。

只有“想统一一下”“代码不够整齐”不足以触发。先在现有系统中寻找已有 primitive、token 和组件 API，避免平行事实源。

系统 owner 负责新契约及为证明迁移有效所需的代表性消费者，不把每个消费者机械转交 Frontend Engineering。只有剩余工作已经变成独立产品页面实现、拥有不同边界或需要跨会话交接时才 Route Out；同一迁移的浏览器证据只运行一次。

## 事实源与契约

- 明确每类事实源：基础值、semantic token、组件 token、组件 API、设计资产和文档分别由哪里拥有。
- token 使用语义名称表达用途，不把具体颜色或尺寸伪装成语义；主题只替换值，不改变业务含义。
- component variants 表达稳定、有限的产品差异；临时页面组合不升级为全局 variant。
- 组件 API 优先语义 props、组合和原生行为，避免布尔参数爆炸、样式逃生口成为默认路径。
- 状态至少考虑 default、hover、focus、active、disabled、loading、error 和选中态，但只实现组件真实支持的集合。
- Figma/code 映射复用现有 Variables、Styles、Components 和 Code Connect 能力；没有 Figma 环境时不伪造同步证据。

## 渐进迁移

1. 盘点事实源、消费者和重复定义，锁定最小迁移单元与兼容要求。
2. 先建立新契约及验证，再迁移代表性消费者；不要一次替换全仓。
3. 兼容层必须有明确消费者、退出条件和删除时机，避免永久双轨。
4. 按依赖顺序迁移其余消费者，机械变更可批量执行，但每类至少验证一个代表实例。
5. 只有消费者清零且发布/回滚边界允许时才删除旧 token、API 或组件。

## 验证

- 对 token 和主题检查类型、构建、引用完整性、semantic mapping 和至少两个代表性消费者。
- 对组件覆盖受影响 variants、状态、键盘/焦点和必要无障碍语义；Storybook 不是运行产品的替代证据。
- 可运行时使用浏览器验证相关主题、桌面/移动视口、长内容和关键状态；必要时做前后截图比较。
- 有 Figma 能力时验证变量、组件、variant 和代码映射；工具未连接时明确保留该证据缺口。
- 迁移完成必须证明旧消费者数量、兼容层状态和回滚路径，不以“新 API 已存在”代替完成。
