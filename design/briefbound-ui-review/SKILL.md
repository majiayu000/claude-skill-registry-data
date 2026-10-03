---
name: briefbound-ui-review
description: Use when an existing page, isolated preview, component, screenshot, UI flow, visual change, or frontend implementation needs a Chinese-first UX, visual hierarchy, interaction-state, responsive, accessibility, design-system, or browser-runtime review; use as support for preview approval and UI-focused PR review, and do not trigger for creating a new design or implementing accepted fixes.
license: MIT
---

# Briefbound UI Review

## 目标

以真实用户任务和运行证据审查界面，找到会妨碍理解、操作、信任或跨视口使用的问题。默认只读、findings 优先；不扩张成重设计，不给无证据审美偏好打分。

## Briefbound task contract

- Context Boundary: 用户目标、待审正式 surface 或隔离预览、主要用户路径、现有设计系统或相邻界面、可用代码/截图/Figma/运行环境，以及本轮允许的审查深度。
- Output Contract: 按影响排序的 UI findings；预览预审时额外给出 `READY_FOR_USER_APPROVAL / REVISE_RECOMMENDED`，并说明未覆盖状态或视口。
- Allowed Action: 读取代码和设计资料、运行应用、操作浏览器并做只读检查；除非 Briefbound Router 另行授权修复，否则不修改产品代码。
- Success Evidence: 可复现的浏览器观察、截图/DOM/无障碍树/console 证据、设计系统偏差或紧邻代码证据；审美判断必须关联用户任务。
- Stop Condition: 目标 surface 或用户任务不明、无法访问关键状态且静态证据不足、缺少必要权限，或审查将越过隐私和授权边界。
- Route Out: 预览无阻塞 finding 时交用户批准；需要调整时回原设计 owner；用户已批准的独立实现转 `briefbound-frontend-engineering`；系统性 token、主题或组件问题转 `briefbound-design-system`；整份 PR 正确性由 `briefbound-pr-review` 主责；阻塞回 `briefbound-router`。

## 统一调用契约

- 只处理 Briefbound task contract 范围；复合 PR 中只提交 UI 专项证据，不重复通用代码审查。没有 finding 时明确通过，并记录真实覆盖缺口。
- 用户可见内容默认中文，保留代码、命令、路径、错误原文、API/协议、skill 名和枚举；Route Out 仅以 Briefbound task contract 为准，末行 `下一步建议: <一个具体动作>`，限于方向、优先级等决策类建议，不交回可自行执行的步骤。

## 审查面

只加载与用户任务有关的视角，没有证据的视角不输出：

- 任务完成：主操作是否清楚，入口、返回、取消、确认和恢复是否可理解。
- 信息层级：首要内容、扫描顺序、对比关系、密度、文案和状态反馈是否支持任务。
- 交互状态：loading、empty、error、disabled、selected、success、权限、长内容和快速重复操作。
- 响应式：目标视口中的重排、换行、溢出、固定元素、触控目标和操作可达性。
- 无障碍：语义结构、标签、键盘路径、可见焦点、对比度、非颜色提示和动态状态播报。
- 一致性：现有组件、token、主题、variants 和相邻页面模式；只把会影响用户或维护的偏差列为 finding。
- 运行质量：console 错误、资源或请求失败、明显布局跳动和关键交互反馈。

不使用“更高级”“不够现代”等无法验证的描述。视觉建议必须说明它改善了什么任务、层级或状态。

## 审查流程

1. 锁定主要用户任务、目标 surface、关键状态和视口；本地可查信息不要反问用户。
2. 读取 owning component、相邻模式和设计 token，建立实际基线。
3. 可运行时使用本轮 Available skills 中的浏览器能力走主路径，按风险补充状态和视口；控制截图和 DOM 输出，只保留能支持 finding 的证据。
4. 将观察分为真实缺陷、设计取舍、证据缺口；不把个人偏好包装成缺陷。
5. 合并同根因的多个症状，按用户阻断、误操作/信任、明显效率损失、一般一致性问题排序。

## 预览预审

审查隔离预览时确认网页 URL 可访问，主要桌面/移动视口、关键状态、代表文案、mock 边界和 console 证据足够评估。只读输出：

- `READY_FOR_USER_APPROVAL`：没有阻止用户判断或明显违反已对齐目标的问题。
- `REVISE_RECOMMENDED`：列出必须先调整的 findings，并回到生成预览的设计 owner。

这两个结果都不是 `APPROVED`。只有用户对具体预览明确批准，Briefbound Router 才能允许正式 UI 写入。

## 输出

每个 finding 使用紧凑结构：`严重度 + 问题 + 证据 + 用户影响 + 最小建议`。可安全依次修复多个项目时给出完整执行顺序，不只推荐一个；只有真实取舍或越权风险才让用户选择。

没有 finding 时说明审查通过，并列出未验证的状态、视口或运行环境。
