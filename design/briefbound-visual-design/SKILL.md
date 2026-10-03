---
name: briefbound-visual-design
description: Use when a UI task primarily needs a distinctive but context-appropriate visual direction, brand expression, typography, color system, composition, imagery, iconography, or motion language before implementation; do not use for information architecture, routine product UI, design-system governance, implementation of an accepted direction, or review-only findings.
license: MIT
---

# Briefbound Visual Design

## 目标

把产品目的、受众和内容转成有辨识度且可实施的视觉语言，直接给出推荐，不让用户先掌握设计术语；视觉强度服务任务，不以“独特”为理由牺牲可读性、性能或效率。

## Briefbound task contract

- Context Boundary: 产品/品牌、受众、使用场景、内容与资产、目标 surface、现有视觉基线、技术和无障碍约束。
- Output Contract: 一个推荐视觉方向；命中预览闸门时先交付隔离预览 URL、代表截图、覆盖状态和批准状态。
- Allowed Action: 分析现有产品和资产、形成视觉契约；`PREVIEW_REQUIRED` 时只写隔离预览，收到 `APPROVED` 后才调整正式视觉实现；不改无关信息架构、业务行为或全局设计系统。
- Success Evidence: 预览阶段：可访问网页、桌面/移动截图、关键内容与降级边界；正式阶段：关键 surface 真实渲染、目标视口、内容压力、无障碍与性能检查。
- Stop Condition: `WAITING_USER_REVIEW`、用户要求 `REVISE/ABANDON`、品牌资产或产品定位高影响冲突、素材不可获得，或实施越过授权范围。
- Route Out: 信息架构或交互模型成为主要未知量时转 `briefbound-ui-design`；只交付视觉方案或需独立 handoff 时转 `briefbound-frontend-engineering`；系统 token/主题治理转 `briefbound-design-system`；现有结果审查转 `briefbound-ui-review`；验证后残留转 `briefbound-development-cleanup`；阻塞回 `briefbound-router`。

## 统一调用契约

- 只处理 Briefbound task contract 范围；默认输出一个有依据的推荐方向，而不是风格名称堆砌，低影响细节 agent 自行决策。
- 用户可见内容默认中文，只说明会改变实现的视觉决策、证据和取舍；代码、命令、路径、错误原文、API/协议、skill 名和枚举保留原样；Route Out 仅以 Briefbound task contract 为准；有自然闸门（需用户裁决、批准或阻塞）时末行 `下一步建议: <一个具体动作>`，否则声明继续已授权工作。

## 语境判断

- SaaS、CRM、后台、编辑器和运营工具：优先扫描、比较、密度和稳定层级，辨识度来自精确而非装饰。
- 品牌、产品、作品集和展示页面：品牌或对象必须成为首屏信号，用图像、字体、构图和节奏建立记忆点。
- 游戏和创意体验：可以更具表现力，但交互反馈、可读性和性能仍是硬边界。
- 已有产品：先读品牌资产、相邻页面、token 和组件；用户未要求重塑时不引入不兼容的平行视觉语言。

用户只说“更好看、现代一点”时，结合产品类型和现有证据直接推荐；方向会显著改变布局、素材、品牌感知或成本时才给少量备选。

## 单 owner 贯穿

要求视觉设计并实现时，本 owner 贯穿隔离预览、批准后的正式落地和浏览器验收，不再加载 UI Design 或 Frontend Engineering。`WAITING_USER_REVIEW` 是必须暂停的自然闸门。响应式和无障碍约束随实现处理；只有核心信息架构/交互或跨消费者契约需要重定时才切换 owner。

## 预览批准闸门

品牌表达、字体、色彩、构图、图像、图标或动效方向尚未获用户确认时标记 `PREVIEW_REQUIRED`；明确小修、既有语言机械应用或已有批准证据可标记 `PREVIEW_SKIPPED`。

- 优先在项目已有 preview/example surface 或任务级临时目录复用真实组件，不先改正式 route、生产组件、共享 token 或真实写接口。
- 提供可访问本地网页、主要桌面/移动截图、真实文案、关键状态、降级和模拟边界；应用不可运行才降级为独立 HTML/CSS/JS。
- 交付后进入 `WAITING_USER_REVIEW`，只接受用户 `APPROVED / REVISE <反馈> / ABANDON` 状态变化。UI Review 的通过建议不能代替用户批准。
- `REVISE` 只改预览；`APPROVED` 后连续实施已确认方向；`ABANDON` 不写正式 surface。

## 视觉契约

- 参考：动手前锁定风格基准或真实参考对象并写进契约；无基准时由产品类型推导并说明依据。
- 概念：一句可执行原则说明视觉如何支持产品，而非只给风格标签。
- 字体：定义 display/body/mono 的角色、层级、字重、行高和长文本行为；选择兼顾语言覆盖、加载和许可。
- 色彩：定义背景、surface、文本、边框、accent 和状态语义；保证对比度且不只靠颜色传达状态。
- 构图：根据内容优先级选择网格、密度、留白、对齐和节奏；避免默认 hero、均匀卡片阵列和无内容依据的装饰。
- 图像与图标：优先真实产品、对象、地点、人物或状态；图标来自项目已有库，核心图片可检查而非氛围填充。
- 动效：只设计能解释层级、状态变化、空间关系或品牌时刻的运动；明确 reduced-motion 和低性能降级。
- 细节：圆角、阴影、边框和背景效果形成有限体系；按语境判断，不建立脱离产品的永久禁用清单。

## 实施与验证

1. 读取真实内容和最长/最短样本，先验证层级与构图，再精修装饰。
2. 两遍走：先出字号、间距、色板等参数方案，对照 anti-patterns 自检后产出；截图自评一遍，修掉明显生成感特征。
3. 命中 `PREVIEW_REQUIRED` 时先完成隔离网页并等待批准；批准前不进入正式实现。
4. 收到 `APPROVED` 或有依据的 `PREVIEW_SKIPPED` 后复用项目 token 和组件；新视觉语言跨多个消费者时转 `briefbound-design-system`。
5. 核心图像缺失且结果依赖它时，用本轮 Available skills 的图像能力生成或寻找资产，不用临时渐变替代真实主体。
6. 浏览器检查主要视口、长文本、关键状态、资源加载、console、溢出和动效降级；截图必须能看清实际内容。结果对照概念原则与主任务核验；没有运行证据不声称视觉完成。

数字默认值与生成方法按需读 `references/craft-baseline.md`（设排版、间距、色彩、细节参数时）；生成感特征对照按需读 `references/anti-patterns.md`（方案与截图自评时）。
