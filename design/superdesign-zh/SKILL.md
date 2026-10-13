---
name: frontend-design-zh
description: 专精前端设计指南，用于创建美观、现代的用户界面。适用于构建落地页、仪表盘或任何用户界面。
metadata: {"clawdbot":{"emoji":"🎨"}}
---

# 前端设计技能

在创建 UI 组件、落地页、仪表盘或任何前端设计工作时使用此技能。

## 设计工作流程

遵循以下结构化方法进行 UI 设计：

1. **布局设计** — 思考组件结构，创建 ASCII 线框图
2. **主题设计** — 定义颜色、字体、间距、阴影
3. **动画设计** — 规划微交互和过渡效果
4. **实现落地** — 生成实际代码

### 1. 布局设计

在编码之前，先用 ASCII 格式绘制布局草图：

```
┌─────────────────────────────────────┐
│         页眉 / 导航栏               │
├─────────────────────────────────────┤
│                                     │
│            主视觉区域               │
│         (标题 + 行动号召)           │
│                                     │
├─────────────────────────────────────┤
│   功能卡片  │  功能卡片  │  功能卡片  │
├─────────────────────────────────────┤
│              页脚                   │
└─────────────────────────────────────┘
```

### 2. 主题指南

**颜色规则：**
- 永远不要使用通用的 Bootstrap 风格蓝色 (#007bff) —— 看起来很过时
- 优先使用 oklch() 定义现代颜色
- 使用语义化颜色变量 (--primary, --secondary, --muted 等)
- 从一开始就考虑亮色和暗色模式

**字体选择 (Google Fonts)：**
```
Sans-serif: Inter, Roboto, Poppins, Montserrat, Outfit, Plus Jakarta Sans, DM Sans, Space Grotesk
Monospace: JetBrains Mono, Fira Code, Source Code Pro, IBM Plex Mono, Space Mono, Geist Mono
Serif: Merriweather, Playfair Display, Lora, Source Serif Pro, Libre Baskerville
Display: Architects Daughter, Oxanium
```

**间距与阴影：**
- 使用一致的间距比例 (0.25rem 为基准单位)
- 阴影应该微妙 —— 避免厚重的投影
- 考虑也使用 oklch() 定义阴影颜色

### 3. 主题模式

**现代暗色模式 (Vercel/Linear 风格)：**
```css
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.970 0 0);
  --muted: oklch(0.970 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --border: oklch(0.922 0 0);
  --radius: 0.625rem;
  --font-sans: Inter, system-ui, sans-serif;
}
```

**新野兽派风格 (90 年代网页复兴)：**
```css
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0 0 0);
  --primary: oklch(0.649 0.237 26.97);
  --secondary: oklch(0.968 0.211 109.77);
  --accent: oklch(0.564 0.241 260.82);
  --border: oklch(0 0 0);
  --radius: 0px;
  --shadow: 4px 4px 0px 0px hsl(0 0% 0%);
  --font-sans: DM Sans, sans-serif;
  --font-mono: Space Mono, monospace;
}
```

**玻璃拟态：**
```css
.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1rem;
}
```

### 4. 动画指南

**微语法规划：**
```
button: 150ms [S1→0.95→1] press
hover: 200ms [Y0→-2, shadow↗]
fadeIn: 400ms ease-out [Y+20→0, α0→1]
slideIn: 350ms ease-out [X-100→0, α0→1]
bounce: 600ms [S0.95→1.05→1]
```

**常见模式：**
- 入场动画：300-500ms，ease-out
- 悬停状态：150-200ms
- 按钮点击：100-150ms
- 页面过渡：300-400ms

### 5. 实现规则

**Tailwind CSS：**
```html
<!-- 通过 CDN 导入用于原型开发 -->
<script src="https://cdn.tailwindcss.com"></script>
```

**Flowbite (组件库)：**
```html
<link href="https://cdn.jsdelivr.net/npm/flowbite@2.0.0/dist/flowbite.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/flowbite@2.0.0/dist/flowbite.min.js"></script>
```

**图标 (Lucide)：**
```html
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
<script>lucide.createIcons();</script>
```

**图片：**
- 使用真实的占位图服务：Unsplash、placehold.co
- 不要编造图片 URL
- 示例：`https://images.unsplash.com/photo-xxx?w=800&h=600`

### 6. 响应式设计

始终采用移动优先和响应式设计：

```css
/* 移动优先 */
.container { padding: 1rem; }

/* 平板设备 */
@media (min-width: 768px) {
  .container { padding: 2rem; }
}

/* 桌面设备 */
@media (min-width: 1024px) {
  .container { max-width: 1200px; margin: 0 auto; }
}
```

### 7. 无障碍访问

- 使用语义化 HTML (header, main, nav, section, article)
- 包含正确的标题层级 (h1 → h2 → h3)
- 为交互元素添加 aria-labels
- 确保足够的颜色对比度 (至少 4.5:1)
- 支持键盘导航

### 8. 组件设计技巧

**卡片：**
- 微妙的阴影，不要厚重的投影
- 一致的内边距 (p-4 到 p-6)
- 悬停状态：轻微上浮 + 阴影增强

**按钮：**
- 清晰的视觉层级 (主要、次要、幽灵按钮)
- 足够的点击区域 (最小 44x44px)
- 加载和禁用状态

**表单：**
- 输入框上方清晰的标签
- 可见的焦点状态
- 内联验证反馈
- 字段之间足够的间距

**导航：**
- 长页面使用粘性页眉
- 清晰的激活状态指示
- 移动端友好的汉堡菜单

---

## 快速参考

| 元素 | 推荐值 |
|------|--------|
| 主要字体 | Inter, Outfit, DM Sans |
| 代码字体 | JetBrains Mono, Fira Code |
| 圆角 | 0.5rem - 1rem (现代风格), 0 (野兽派) |
| 阴影 | 微妙，最多 1-2 层 |
| 间距 | 4px 基准单位 (0.25rem) |
| 动画 | 150-400ms, ease-out |
| 颜色 | oklch() 现代风格，避免通用蓝色 |

---

*基于 SuperDesign 模式 — https://superdesign.dev*
