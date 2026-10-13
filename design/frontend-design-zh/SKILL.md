---
name: frontend-design-zh
description: 使用 React、Tailwind CSS 和 shadcn/ui 创建独特、生产级的静态网站——无需设计稿。从纯文本需求生成大胆、令人难忘的设计，具备反AI套路美学、移动优先响应式模式和单文件打包功能。适用于构建落地页、营销网站、作品集、仪表盘或任何静态Web界面。支持 Vite（纯静态）和 Next.js（Vercel部署）两种工作流。
homepage: https://github.com/kesslerio/frontend-design-ultimate-clawhub-skill
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      bins: ["node", "npm"]
---

# 前端设计终极版

仅从文本需求创建独特、生产级的静态网站。无需设计稿、无需 Figma —— 只需描述你想要的，即可获得大胆、令人难忘的设计。

**技术栈**: React 18 + TypeScript + Tailwind CSS + shadcn/ui + Framer Motion  
**输出**: Vite（静态HTML）或 Next.js（Vercel就绪）

## 快速开始

```
"为一个AI写作工具构建SaaS落地页。深色主题，
编辑排版风格，微妙纹理背景。页面包括：带动画演示的英雄区、
功能网格、价格表、FAQ手风琴、页脚。"
```

---

## 设计思维（先做这一步）

在编写任何代码之前，确定一个**大胆的美学方向**：

### 1. 理解背景
- **目的**: 这个界面解决什么问题？谁使用它？
- **受众**: 开发者工具？消费者应用？企业？创意代理？
- **约束**: 性能要求、无障碍需求、品牌指南？

### 2. 选择一个极端基调
选择一个并完全投入 —— 犹豫的设计注定失败：

| 基调 | 特点 |
|------|------|
| **极简主义** | 稀疏、单色、巨大排版、原始边缘 |
| **繁复混乱** | 分层、密集、重叠元素、受控的混乱 |
| **复古未来** | 霓虹点缀、几何形状、CRT美学 |
| **有机自然** | 柔和曲线、大地色调、手绘元素 |
| **奢华精致** | 微妙动画、高级排版、克制的调色板 |
| **编辑杂志** | 强网格、戏剧性标题、留白作为特色 |
| **野兽派原始** | 暴露结构、强烈对比、反设计 |
| **装饰艺术几何** | 金色点缀、对称、华丽图案 |
| **柔和粉彩** | 圆角、温柔渐变、友好 |
| **工业实用** | 功能性、等宽字体、数据密集 |

### 3. 定义难忘元素
什么是用户会记住的**一件事**？一个英雄动画？排版处理？颜色组合？不寻常的布局？

---

## 美学指南

### 排版 —— 绝不使用通用字体

**禁止使用**: Inter, Roboto, Arial, 系统字体, Open Sans

**应该使用**: 独特、有个性的选择，提升设计品质。

| 用途 | 方法 |
|----------|------|
| 展示/标题 | 鲜明个性 — Clash, Cabinet Grotesk, Satoshi, Space Grotesk（少量使用）, Playfair Display |
| 正文 | 精致可读 — Instrument Sans, General Sans, Plus Jakarta Sans |
| 等宽/代码 | DM Mono, JetBrains Mono, IBM Plex Mono |
| 搭配策略 | 对比字重（细体展示 + 粗体正文），对比风格（衬线 + 几何无衬线） |

**字号递进**: 使用3倍以上的跳跃，而不是胆小的1.5倍增量。

### 颜色与主题

**禁止使用**: 白色上的紫色渐变、均匀分布的5色调色板

**应该使用**:
- **主色 + 鲜明强调色**: 70-20-10法则（主色-次色-强调色）
- **CSS变量**: `--primary`, `--accent`, `--surface`, `--text`
- **坚定选择深色或浅色**: 不要用灰色中间地带模棱两可
- **高对比CTA**: 按钮应该戏剧性地突出

```css
:root {
  --bg-primary: #0a0a0a;
  --bg-secondary: #141414;
  --text-primary: #fafafa;
  --text-secondary: #a1a1a1;
  --accent: #ff6b35;
  --accent-hover: #ff8555;
}
```

### 动效与动画

**优先级**: 一个协调的页面加载 > 分散的微交互

**高影响力时刻**:
- 错开显示的英雄区揭示（`animation-delay`）
- 滚动触发的区块入场
- 令人惊喜的悬停状态（缩放、颜色变化、阴影深度）
- 平滑的页面过渡

**实现**:
- 简单动画只用CSS
- React使用Framer Motion（通过初始化脚本预装）
- 保持时长200-400ms（快速，不拖沓）

### 空间构成

**禁止使用**: 居中、对称、可预测的布局

**应该使用**:
- 有目的的不对称
- 重叠元素
- 对角线流动 / 突破网格
- 慷慨的负空间 或 受控的密度（二选一）
- 偏离网格的英雄区

### 背景与氛围

**禁止使用**: 纯白色/灰色背景

**应该使用**:
- 渐变网格（微妙，不刺眼）
- 噪点/纹理（SVG滤镜或CSS）
- 几何图案（点、线、形状）
- 分层透明度
- 戏剧性的阴影营造深度
- 模糊效果实现玻璃态

```css
/* 微妙噪点覆盖 */
.grain::before {
  content: '';
  position: fixed;
  inset: 0;
  background: url("data:image/svg+xml,...") repeat;
  opacity: 0.03;
  pointer-events: none;
}
```

---

## 移动优先模式

详见 **[references/mobile-patterns.md](references/mobile-patterns.md)** 获取详细CSS。

### 关键规则

| 模式 | 桌面 | 移动端修复 |
|---------|---------|------------|
| 带隐藏视觉的Hero | 2列网格 | 切换为 `display: flex`（不是grid） |
| 大型选择列表 | 水平滚动 | 带分类标题的手风琴 |
| 多列表单 | 并排 | 垂直堆叠 |
| 状态/警告卡片 | 内联 | `align-items: center` + `text-align: center` |
| 功能网格 | 3-4列 | 单列 |

### 断点

```css
/* 平板 - 堆叠侧边栏 */
@media (max-width: 1200px) { }

/* 移动端 - 完全单列 */
@media (max-width: 768px) { }

/* 小屏移动端 - 紧凑间距 */
@media (max-width: 480px) { }
```

### 字体缩放

```css
@media (max-width: 768px) {
  .hero-title { font-size: 32px; }      /* 从 ~48px */
  .section-title { font-size: 24px; }   /* 从 ~32px */
  .section-subtitle { font-size: 14px; } /* 从 ~16px */
}
```

---

## 构建工作流

### 选项A: Vite（纯静态）

```bash
# 1. 初始化
bash scripts/init-vite.sh my-site
cd my-site

# 2. 开发
npm run dev

# 3. 构建静态文件
npm run build
# 输出: dist/

# 4. 打包为单个HTML（可选）
bash scripts/bundle-artifact.sh
# 输出: bundle.html
```

### 选项B: Next.js（Vercel部署）

```bash
# 1. 初始化
bash scripts/init-nextjs.sh my-site
cd my-site

# 2. 开发
npm run dev

# 3. 部署到Vercel
vercel
```

---

## 项目结构

### Vite 静态
```
my-site/
├── src/
│   ├── components/     # React组件
│   ├── lib/           # 工具函数, cn()
│   ├── styles/        # 全局CSS
│   ├── config/
│   │   └── site.ts    # 可编辑内容配置
│   ├── App.tsx
│   └── main.tsx
├── index.html
├── tailwind.config.ts
└── package.json
```

### Next.js
```
my-site/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── privacy/page.tsx
├── components/
├── lib/
├── config/
│   └── site.ts
└── tailwind.config.ts
```

---

## 站点配置模式

将所有可编辑内容放在一个文件中：

```typescript
// config/site.ts
export const siteConfig = {
  name: "Acme AI",
  tagline: "写得更好、更快",
  description: "AI驱动的写作助手",
  
  hero: {
    badge: "现在测试中",
    title: "你的文字，\n如虎添翼",
    subtitle: "用理解你风格的AI，10倍速写作",
    cta: { text: "开始使用", href: "/signup" },
    secondaryCta: { text: "观看演示", href: "#demo" },
  },
  
  features: [
    { icon: "Zap", title: "闪电般快速", description: "..." },
    // ...
  ],
  
  pricing: [
    { name: "免费", price: 0, features: [...] },
    { name: "专业", price: 19, features: [...], popular: true },
  ],
  
  faq: [
    { q: "如何运作？", a: "..." },
  ],
  
  footer: {
    links: [...],
    social: [...],
  }
}
```

---

## 实施前检查清单

在最终确定任何设计之前运行此检查：

### 设计质量
- [ ] 排版独特（无Inter/Roboto/Arial）
- [ ] 调色板有清晰的主色 + 强调色（非均匀分布）
- [ ] 背景有氛围（非纯白色/灰色）
- [ ] 至少有一个令人难忘/难忘的元素
- [ ] 动画经过协调（非分散）

### 移动端响应
- [ ] Hero在移动端居中（无空网格空间）
- [ ] 所有网格折叠为单列
- [ ] 表单垂直堆叠
- [ ] 大型列表使用手风琴（非水平滚动）
- [ ] 字体大小适当缩小

### 表单一致性
- [ ] Input、select、textarea样式一致
- [ ] Radio/checkbox可见（检查透明边框样式）
- [ ] 下拉选项有可读背景
- [ ] 标签使用CSS变量（非硬编码颜色）

### 无障碍
- [ ] 颜色对比符合WCAG AA（文字4.5:1，UI 3:1）
- [ ] 焦点状态可见
- [ ] 语义化HTML（nav, main, section, article）
- [ ] 图片有alt文本
- [ ] 键盘导航可用

---

## shadcn/ui 组件

预装10个常用组件（button, badge, card, accordion, dialog, navigation-menu, tabs, sheet, separator, avatar, alert）。使用 `npx shadcn@latest add [name]` 添加更多，或用 `npx shadcn@latest add --all` 安装全部。

详见 **[references/shadcn-components.md](references/shadcn-components.md)** 获取完整组件参考。

落地页最常用：
- `Button`, `Badge` — CTA和标签
- `Card` — 功能卡片、价格层级
- `Accordion` — FAQ部分
- `Dialog` — 模态框、视频播放器
- `NavigationMenu` — 头部导航
- `Tabs` — 功能展示
- `Carousel` — 推荐/评价

---

## 参考资料

- **[references/design-philosophy.md](references/design-philosophy.md)** — 扩展的反AI套路指南
- **[references/mobile-patterns.md](references/mobile-patterns.md)** — 详细响应式CSS
- **[references/shadcn-components.md](references/shadcn-components.md)** — 组件快速参考
- **[templates/site-config.ts](templates/site-config.ts)** — 完整siteConfig示例

---

## 示例

### 提示词 → 输出

**输入**:
> "摄影师的作品集网站。极简、编辑感。
> 网格画廊带灯箱、关于部分、联系表单。"

**设计决策**:
- 基调: 编辑/杂志
- 排版: Cormorant Garamond（展示）+ Plus Jakarta Sans（正文）
- 颜色: 近黑背景（#0c0c0c），暖白文字（#f5f5f0），铜色强调（#b87333）
- 难忘元素: 全出血英雄图片，文字覆盖在滚动时显示
- 动效: 画廊图片在滚动时交错淡入

**输出**: 完整的Next.js项目，包含响应式画廊、灯箱组件和带验证的联系表单。

---

*基于Anthropic的frontend-design、web-artifacts-builder和社区frontend-design-v2技能。*
