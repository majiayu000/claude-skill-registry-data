---
name: design-system
description: "建立或修改三层设计 Token、主题 CSS 变量及组件状态规范，生成并校验 Token 配置。用于 Token 架构、暗色主题和组件设计交付；不负责演示文稿或整站生成。"
license: MIT
metadata:
  source: "dingdong905/design-skills"
  scope: "tokens-only"
  language: "zh-CN"
---

# 设计 Token 与组件规范

以项目现有品牌、组件库和 CSS 变量命名为起点。已有系统优先做窄修改；没有系统时再采用 primitive → semantic → component 三层结构。不要为了套模板改变技术栈或覆盖已有 Token。

## 任务与资料

- 架构与命名：[token-architecture.md](references/token-architecture.md)。原始值、语义和组件分别查 [primitive-tokens.md](references/primitive-tokens.md)、[semantic-tokens.md](references/semantic-tokens.md)、[component-tokens.md](references/component-tokens.md)。
- 组件交付与状态：[component-specs.md](references/component-specs.md)、[states-and-variants.md](references/states-and-variants.md)。只定义目标组件实际存在的状态，并保留键盘焦点、错误、禁用、加载等交互语义。
- Tailwind 项目查 [tailwind-integration.md](references/tailwind-integration.md)，先确认版本：v4 使用 CSS `@theme`，v3 才使用 `tailwind.config`。不要套用混合版本示例。
- JSON 格式、生成器边界和主题引用见 [token-tooling.md](references/token-tooling.md)。新项目可以复制 `templates/design-tokens-starter.json`，明确其色值只是示例。

## 生成与检查

Node.js 内置模块即可运行。将 `<skill-dir>` 换为本技能真实目录；配置和输出指向用户项目。

```powershell
node "<skill-dir>/scripts/generate-tokens.cjs" --config "<project-root>/assets/design-tokens.json"
node "<skill-dir>/scripts/generate-tokens.cjs" --config "<project-root>/assets/design-tokens.json" -o "<project-root>/assets/design-tokens.css"
node "<skill-dir>/scripts/validate-tokens.cjs" --dir "<project-root>/src"
```

先在标准输出检查生成结果，再写入用户要求的目标。生成器检查缺失引用、引用循环和 CSS 变量命名碰撞；保留引用为 `var(...)`，使组件能跟随 `.dark` 的语义变量切换。复杂 DTCG 对象需明确转换，不支持的类型会报错。

`validate-tokens` 是启发式扫描：返回 1 表示有需要审查的硬编码候选，不代表产品不合格；`--fix` 只显示建议，不自动修改。它会跳过 Token/全局定义文件，对 Tailwind 任意值等也不能完整识别。按项目已有规范判断是否需要替换，不能为了清零把所有尺寸都机械转换为变量。

交付 JSON 源、生成 CSS、必要的组件状态说明及实际验证结果。JSON 是源，CSS 是派生物；确认主题、语义状态与文字/控件对比，不以脚本通过代替界面验证。品牌源需要调整时调用 `brand`，视觉选型需要检索时用 `ui-ux-pro-max`。PPTX 与 HTML 演示不由本技能路由。
