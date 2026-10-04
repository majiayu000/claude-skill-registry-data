---
name: ui-styling
description: "实现 React/shadcn/Tailwind 项目的组件样式、主题与响应式，沿用既有版本。"
metadata:
  source: "dingdong905/design-skills"
  scope: "react-shadcn-tailwind"
  language: "zh-CN"
---

# React / shadcn / Tailwind 实现

先读目标文件、package.json、锁文件、components.json、样式入口和相关组件。确认 React/框架、Tailwind 主版本、shadcn 的本地实现及 Radix/Base UI 等实际依赖；项目组件代码是接口来源，不能假定所有 shadcn 组件都用同一底层。

用户选择的技术栈与已有组件库优先。修复局部界面时沿用已有主题、导入别名、组件 API、表单和图标库；不用本技能给非 React 项目迁移技术栈，也不引入海报/Canvas 工作流。

## 实现

- Tailwind 版本和 Token 映射：[版本与主题](references/versions-and-theme.md)。v4 与 v3 的安装和配置分开处理。
- 组件组合、表单与弹层：[组件实现](references/components.md)。先复用本地组件，仅添加任务需要的组件或依赖。
- 键盘、语义、响应式和主题验证：[界面验证](references/verification.md)。不要用样式模拟原生控件语义。

在项目现有样式中落实具体改动，状态变化避免布局跳动。使用显式可被构建器发现的完整类名或项目已有 variant 机制；不能拼接构建时不可见的 Tailwind 类名。

新增项目且用户选择本栈时按当前官方文档与项目包管理器配置。已有项目不运行 `init` 重写配置，不使用 `add --all`，不机械执行 `@latest` 升级。需要新依赖时先落实任务范围、兼容版本和实际命令，再按环境权限执行。

## 验证与交付

运行项目相关构建/类型检查及已有必要测试；打开受影响页面，验证响应式、焦点、表单或弹层状态和主题。已有组件库不会自动保证组合后的可访问性。只有静态检查时明确未运行浏览器。

交付实现改动、理由和实际验证。`ui-ux-pro-max` 提供设计建议，`brand` 提供品牌事实，`design-system` 提供 Token 架构，`hallmark` 用于用户要求的视觉审查或重设计；普通实现不自动加载全部技能。

权威资料可按需查看 [shadcn 文档](https://ui.shadcn.com/docs) 和 [Tailwind 文档](https://tailwindcss.com/docs)，并核对目标版本。UI 自动化使用环境实际可用的浏览器工具文档。
