---
name: cm-frontend-engineer
description: 前端工程师 Skill，执行前端开发任务，自动适配项目技术栈（React/Vue/Svelte/Next.js 等），支持 Figma/Stitch 设计稿还原
---

# cm-frontend-engineer — 前端工程师

执行前端开发任务。自动识别项目技术栈，遵循项目 `.claude/rules/` 中的规范。

## 触发条件

由 `/cm-ai` 自动调用，当 task 涉及前端开发时触发。

**与 cm-ui-engineer 的分工**：feature 存在设计基准（design-baseline/）时，UI 还原由 `cm-ui-engineer` 前置完成——本 skill **直接消费其组件与 design.md 组件契约，不重写其样式**；无基准时按下方 Step 0 现有行为处理。

## 工作流程

### 0. 设计稿检查

开发前先询问是否先实现设计稿：

- **没有设计稿** → **主动询问用户**是否有设计稿地址（Figma/Stitch 链接），等待用户回复后再继续；用户确认没有设计稿则跳过，直接进入开发
- **有 Figma 链接** → 调用 figma mcp
- **有 Stitch 项目** → 调用 stitch mcp

**设计稿与业务的关系：**

- 设计稿存在且完整 → 按设计稿还原
- 设计稿存在但不是明显的缺失 → 自行补全功能
- 设计稿存在但与业务需求有明显差距或缺失页面 → **主动询问用户**是否需要先还原设计稿再开发功能，等待用户回复后再继续
- 没有设计稿 → 根据 design.md 和业务需求自行实现

### 1. 识别技术栈

读取项目配置自动判断，不做硬编码假设：

- `package.json` → 框架（React/Vue/Svelte/Next/Nuxt/Astro...）、UI 库、状态管理
- `tsconfig.json` / `jsconfig.json` → TS/JS、路径别名
- 样式方案 → Tailwind / CSS Modules / styled-components / UnoCSS 等
- 构建工具 → Vite / Webpack / Turbopack / esbuild

### 2. 读取上下文

- `.claude/rules/frontend.md`、`.claude/rules/coding-style.md`（如存在）
- design.md 中当前任务相关的模块设计
- 扫描 `src/` 了解现有组件结构和命名规律
- **重点扫描项目已有的 UI 组件库**（`components/ui/`、`components/common/` 等），了解哪些组件已封装可复用

### 3. 开发

**组件封装与复用（重要）：**

- 开发前先检查项目已有的 UI 组件库，能复用的绝不重写
- 新建通用 UI 组件时放入项目约定的公共组件目录，确保可被其他页面复用
- 业务组件和 UI 组件分层：UI 组件不含业务逻辑，业务组件组合 UI 组件
- 如果项目使用了第三方组件库（Ant Design/shadcn/Element/Radix 等），优先用库内组件，不自己造轮子

**Tailwind CSS（如项目使用）：**

- 检查 Tailwind 版本（v3 vs v4），全局样式封装方式不同：
  - **v3**：`@layer base/components/utilities` + `@apply` 在 `globals.css` 中
  - **v4**：CSS-first 配置，`@theme` 定义 design token，`@variant` 自定义变体
- 复用样式通过组件封装而非到处复制 class 字符串
- 主题色、间距、字体等通过 Tailwind config / CSS 变量统一管理，不硬编码具体值

**组件开发：**

- 遵循项目已有的组件模式（class/函数、选项式/组合式）
- Props/类型定义跟随项目约定
- 文件命名跟随项目已有规律

**状态管理：**

- 识别项目使用的方案（Redux/Zustand/Pinia/Vuex/Jotai...）
- 简单局部状态用框架原生方案
- 参考 design.md 中的状态流转设计

**API 调用：**

- 基于 design.md 中的接口契约
- 后端未就绪 → 先写 mock，标注 `// TODO: replace mock when API ready`
- 错误处理和 loading 状态

**路由：**

- 按 design.md 页面设计配置，遵循项目路由约定（file-based / config-based）

### 4. 验证

```bash
# 根据项目实际命令执行
npm run lint
npm run typecheck
npm run build
```

如有开发服务器，启动验证页面渲染正常。

**像素级还原验证（如有设计稿）：**

还原度不靠"看着像"，用 BackstopJS 做量化对比：

1. 设计稿导出为参考图（或导出 HTML+CSS 作为基准页面）
2. `npx backstop test` 对比还原页面与基准，生成差异报告
3. 差异集中在特殊效果（渐变边框、复杂阴影）时评估修复成本，其余差异修复后复测
4. 差异报告结果写入任务汇报，供 N6 QA 的可视化回归复用

> 注意：不要让 MCP 直接"照着感觉"还原——先拿到设计稿源文件/导出物作为基准，再开发，再对比。

## 常见坑

| 问题                                    | 处理                                                     |
| --------------------------------------- | -------------------------------------------------------- |
| 路径别名导致 import 报错                | 检查 tsconfig paths 和构建工具配置是否一致               |
| SSR/SSG 组件使用了 browser API          | 加 `typeof window !== 'undefined'` 或动态导入            |
| 样式冲突                                | 优先用项目约定的作用域方案，避免全局样式                 |
| 第三方库类型缺失                        | 检查 `@types/xxx`，必要时声明 `.d.ts`                    |
| Tailwind v3 和 v4 混用                  | 检查版本，v4 不再用 `tailwind.config.js`，改用 CSS-first |
| 组件重复造轮子                          | 开发前先搜索项目已有组件，grep 关键词                    |
| 设计稿颜色/间距与 Tailwind token 不一致 | 扩展 theme 配置而非硬编码 hex 值                         |

## 输出

- 创建/修改的文件列表
- 验证结果（lint + build）
- 设计稿还原情况（如有设计稿）
- 需要其他工种配合的事项
