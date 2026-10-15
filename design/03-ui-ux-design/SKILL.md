---
name: win-03-ui-ux-design
description: Windows App Workflow 阶段 3 —— UI/UX 设计与设计系统。适用场景：架构已定，需要设计令牌（颜色/字体/间距）、组件清单、亮暗主题、信息架构与无障碍基线，产出开发可直接实现的规范。提炼自 UX Architect、UI Designer、Brand Guardian、Accessibility Auditor。
---

# 阶段 3：UI/UX 设计与设计系统

> 目标：把视觉与交互决定沉淀为**代码可用的 tokens 与组件规范**，而不是口头描述。先定系统，再画页面。

## 1. 品牌基础（轻量版，1 页即可）

- 产品气质一句话（例：冷静、可靠、工具感 / 活泼、创作者向）
- 主色 + 语义色（成功/警告/错误/信息）
- 字体：优先系统字体栈（Windows 上即 Segoe UI 家族），避免为小工具引入大字体文件
- 图标风格统一（线性或面性，二选一，别混用）

## 2. 设计令牌（Design Tokens）

先定义变量，再写组件。命名用语义名，不用裸值：

```css
/* tokens 示例 —— 开发直接照抄为 CSS 变量 / Tauri/Electron 主题配置 */
--color-bg-base:        #FFFFFF;   /* dark: #1E1E1E */
--color-bg-subtle:      #F5F5F5;   /* dark: #2A2A2A */
--color-text-primary:   #1A1A1A;   /* dark: #F0F0F0 */
--color-accent:         #2563EB;
--color-danger:         #DC2626;
--space-1: 4px;  --space-2: 8px;  --space-3: 12px;  --space-4: 16px;  --space-6: 24px;
--radius-sm: 4px; --radius-md: 8px;
--font-body: "Segoe UI Variable", "Segoe UI", system-ui, sans-serif;
--font-size-sm: 13px; --font-size-md: 14px; --font-size-lg: 16px;
```

规则：
- 间距只用 4px 网格的倍数
- 对比度满足 WCAG 2.1 AA（正文 ≥ 4.5:1，大字 ≥ 3:1）
- 亮色/暗色/跟随系统 三种主题，变量成对定义

## 3. 组件清单（MVP 级最小集合）

每个组件要定义：状态（默认/悬停/按下/禁用/聚焦）、尺寸、可访问语义。

- 基础：Button、Input、Select、Checkbox、Radio、Switch、Label
- 反馈：Toast/Notification、Dialog/Modal、Progress、Empty State、Error State
- 布局：标题栏区、侧边导航、列表/表格、工具栏、状态栏
- 桌面特有：托盘菜单项、系统通知样式、快捷键提示（用 `Ctrl` 不是 `Cmd`）、文件拖放区

## 4. 信息架构与页面流

- 画出页面/视图流转图（哪些是常驻视图、哪些是弹窗）
- 每个视图回答：用户进来第一眼做什么？主操作放在哪？出错去哪？
- **空状态、加载态、错误态**与正常态同等设计——桌面应用没网没数据时的样子决定第一印象

## 5. Windows 平台约定（尊重平台，来自 Desktop App Engineer 规则 #7）

| 项目 | Windows 约定 |
|---|---|
| 窗口控制 | 最小化/最大化/关闭在右上；自绘标题栏必须保留系统行为（吸附、拖动、双击最大化） |
| 快捷键 | Ctrl+S/C/V/Z、F2 重命名、F5 刷新、Del 删除；提供"快捷键列表"视图 |
| 对话框 | 文件操作用系统原生对话框（打开/保存），不自绘 |
| 托盘 | 右键菜单 + 左键恢复窗口；图标提供亮暗两套 |
| 安装预期 | 开始菜单快捷方式、桌面快捷方式（可选）、卸载入口在"设置→应用"里可见 |
| 通知 | 用 Windows Toast 通知，不自绘假通知 |

## 6. 无障碍基线（WCAG 2.1 AA）

- 键盘可达：所有操作可纯键盘完成，焦点顺序合理、焦点可见
- 屏幕阅读器：控件有 accessible name；用语义角色而不是裸 div（Web 技术栈下 `getByRole` 能命中 = 语义合格）
- 不只靠颜色传达状态（错误要有图标/文字，不能只变红）
- 支持系统缩放（125%/150% DPI 下布局不崩）

## 7. 交付物清单

1. `design/tokens.css`（或框架等价物）——亮暗两套
2. `design/components.md`——组件清单 + 状态定义
3. `design/flows.md`——页面流转图 + 空/载/错状态
4. 主界面高保真稿 1–2 张（其余视图按系统推导）

## 8. 质量门

| # | 判据 | 通过？ |
|---|------|--------|
| 1 | tokens 完整（颜色/间距/字体/圆角），亮暗成对 | ☐ |
| 2 | 组件清单覆盖 MVP 全部页面所需 | ☐ |
| 3 | 空/加载/错误状态都有设计 | ☐ |
| 4 | Windows 平台约定逐项对照过 | ☐ |
| 5 | 对比度与键盘可达性写进验收标准 | ☐ |

通过后 → 阶段 4（工程地基）。
