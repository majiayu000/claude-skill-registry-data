---
name: ui-ux-pro-max
description: Professional UI/UX design resource library with searchable design patterns, color palettes, font pairings, chart types, and UX guidelines. Use when creating beautiful, professional-grade user interfaces, selecting color schemes, choosing typography, designing data visualizations, or following modern UX best practices. Includes 50+ UI styles, 100+ color palettes, curated font pairings, chart selection guide, and comprehensive UX patterns.
---

# UI UX Pro Max - 专业设计资源库

完整的 UI/UX 设计资源库，让 AI 生成的界面像专业设计师作品一样精美。

## 何时使用此 Skill

- 设计任何用户界面时需要专业参考
- 选择配色方案（品牌色、功能色、中性色）
- 挑选字体组合（标题+正文）
- 设计数据可视化图表
- 需要 UX 最佳实践指导
- 寻找特定行业/风格的设计灵感

## 资源导航

| 资源类型 | 文件 | 内容 |
|---------|------|------|
| 🎨 **UI 风格库** | [references/ui-styles.md](references/ui-styles.md) | 50+ 种界面设计风格 |
| 🌈 **配色方案** | [references/color-palettes.md](references/color-palettes.md) | 100+ 专业调色板 |
| 🔤 **字体配对** | [references/typography.md](references/typography.md) | 精选字体组合 |
| 📊 **图表类型** | [references/charts.md](references/charts.md) | 数据可视化指南 |
| 📘 **UX 模式** | [references/ux-patterns.md](references/ux-patterns.md) | 用户体验最佳实践 |
| 🎯 **组件库** | [references/components.md](references/components.md) | 常用组件设计规范 |

## 快速开始

### 1. 确定设计风格
先读取 `references/ui-styles.md`，选择适合项目的设计风格：
- SaaS/企业应用 → Minimalist / Corporate
- 电商 → Modern E-commerce / Luxury
- 创意作品 → Brutalist / Glassmorphism
- 社交应用 → Neumorphism / Soft UI

### 2. 选择配色
读取 `references/color-palettes.md`，根据品牌调性选择：
- 科技/专业 → Blue/Cyan 系列
- 自然/健康 → Green/Earth 系列
- 时尚/美妆 → Purple/Pink 系列
- 金融/法律 → Navy/Gray 系列

### 3. 搭配字体
读取 `references/typography.md`：
- 现代科技感 → Inter + JetBrains Mono
- 优雅精致 → Playfair Display + Inter
- 友好亲和 → Nunito + Open Sans

### 4. 应用 UX 模式
读取 `references/ux-patterns.md` 获取具体场景的交互模式。

## 设计决策框架

### 选择 UI 风格的 3 个问题

1. **目标用户是谁？**
   - 企业用户 → 简洁、专业、高效
   - 年轻消费者 → 活泼、大胆、有趣
   - 高端客户 → 精致、留白、质感

2. **产品类型是什么？**
   - 工具类 → 功能优先，清晰直观
   - 内容类 → 阅读体验，排版优雅
   - 社交类 → 情感连接，互动感强

3. **品牌调性如何？**
   - 创新先锋 → 尝试新风格（Glassmorphism）
   - 稳定可靠 → 经典风格（Material Design）
   - 独特个性 → 大胆风格（Brutalist）

### 配色选择矩阵

| 场景 | 主色 | 辅助色 | 强调色 |
|-----|------|-------|-------|
| 科技产品 | Blue-600 | Slate-500 | Cyan-400 |
| 健康医疗 | Teal-600 | Gray-500 | Emerald-400 |
| 金融科技 | Indigo-700 | Gray-600 | Amber-500 |
| 电商零售 | Rose-600 | Gray-500 | Violet-500 |
| 教育培训 | Violet-600 | Slate-500 | Yellow-400 |
| 娱乐社交 | Fuchsia-600 | Gray-500 | Pink-500 |

## 实用技巧

### Tailwind CSS 快速应用

```css
/* 配色示例 */
.bg-brand { @apply bg-blue-600; }
.text-muted { @apply text-gray-500; }
.border-accent { @apply border-cyan-400; }

/* 字体示例 */
.font-heading { @apply font-display text-3xl font-bold; }
.font-body { @apply font-sans text-base leading-relaxed; }
```

### 响应式断点建议

```
Mobile First:
- 默认: 320px+
- sm: 640px+
- md: 768px+
- lg: 1024px+
- xl: 1280px+
```

### 间距系统

```css
/* 8px 基础倍数 */
space-1: 4px
space-2: 8px
space-3: 12px
space-4: 16px
space-6: 24px
space-8: 32px
space-12: 48px
space-16: 64px
```

## 专业提示

1. **不要混合太多风格** - 选择1种主风格，2-3个设计元素点缀
2. **颜色不超过5种** - 主色、辅助色、中性色、成功色、错误色
3. **字体最多2种** - 1种标题字体 + 1种正文字体
4. **留白是设计** - 不要害怕空白，它是呼吸空间
5. **一致性 > 创新** - 保持设计系统的一致性比追求独特更重要

## 参考资源

- [UI Styles →](references/ui-styles.md) 选择界面风格
- [Color Palettes →](references/color-palettes.md) 选择配色方案
- [Typography →](references/typography.md) 选择字体配对
- [Charts →](references/charts.md) 选择图表类型
- [UX Patterns →](references/ux-patterns.md) 学习交互模式
- [Components →](references/components.md) 查看组件规范

---

**记住：** 好的设计不是堆砌特效，而是解决问题。先确保可用性，再追求美观。
