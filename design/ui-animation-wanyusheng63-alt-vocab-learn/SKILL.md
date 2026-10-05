---
name: ui-animation
description: Comprehensive UI animation toolkit for React projects. Includes MotionPrimitives (page transitions, scroll reveals, hover effects) and ReactBits (creative text animations, backgrounds, cursor effects). Use this skill when implementing any animation features.
---

# UI Animation Toolkit

为 React 项目提供完整的动画解决方案，包含两层工具：

| 层级 | 工具 | 用途 |
|------|------|------|
| **Foundation** | MotionPrimitives | 页面级动画、滚动触发、Hover 效果 |
| **Creative** | ReactBits | 创意动效（文字动画、背景、光标） |

---

## Part 1: MotionPrimitives (Foundation Layer)

### 概述

`MotionPrimitives` 是项目模板内置的动画组件库，基于 `framer-motion` 封装，提供：
- 页面切换动画
- 滚动触发动画
- Hover/Tap 交互
- Stagger 子元素动画

**文件位置**: `src/components/MotionPrimitives.tsx` (模板已包含)

### 核心组件

| 组件 | 用途 | 示例场景 |
|------|------|---------|
| `FadeIn` | 滚动进入视口时触发动画 | Section 入场、内容展示 |
| `Stagger` | 子元素依次动画 | 列表、网格、卡片组 |
| `HoverLift` | Hover 悬浮效果 | 卡片、按钮交互 |

### Variant 预设

| Variant | 效果 |
|---------|------|
| `fadeUp` (默认) | 淡入 + 向上 32px |
| `fadeDown` | 淡入 + 向下 24px |
| `fadeIn` | 仅淡入 |
| `fadeLeft` | 淡入 + 从左 32px |
| `fadeRight` | 淡入 + 从右 32px |
| `scaleUp` | 淡入 + 从 0.92 缩放 |
| `blurIn` | 淡入 + 模糊消散 |

### 使用示例

```tsx
import {
  FadeIn,
  Stagger,
  HoverLift,
  fadeDown,
  scaleUp,
  motion,
} from "@/components/MotionPrimitives";

// 滚动触发的 Section
<FadeIn>
  <h2>Features</h2>
  <p>Content fades up into view.</p>
</FadeIn>

// 使用其他 variant
<FadeIn variants={fadeDown}>
  <HeroTitle />
</FadeIn>

// Stagger 网格
<Stagger className="grid grid-cols-3 gap-6" stagger={0.08}>
  {products.map((p) => (
    <FadeIn key={p.id}>
      <ProductCard product={p} />
    </FadeIn>
  ))}
</Stagger>

// Hover 悬浮卡片
<Stagger className="grid grid-cols-3 gap-6">
  {features.map((f) => (
    <HoverLift key={f.id}>
      <FeatureCard feature={f} />
    </HoverLift>
  ))}
</Stagger>
```

### 典型页面结构

```tsx
import { FadeIn, Stagger, HoverLift, fadeDown, scaleUp } from "@/components/MotionPrimitives";

function HomePage() {
  return (
    <div className="space-y-20">
      {/* Hero */}
      <FadeIn variants={fadeDown}>
        <section className="text-center py-20">
          <h1 className="text-5xl font-bold">Welcome</h1>
          <p className="text-xl text-muted-foreground mt-4">Subtitle</p>
        </section>
      </FadeIn>

      {/* Feature Cards */}
      <Stagger className="grid grid-cols-3 gap-8 container">
        {features.map((f) => (
          <HoverLift key={f.id}>
            <Card className="p-6">
              <f.icon className="h-8 w-8 text-primary" />
              <h3 className="font-semibold mt-4">{f.title}</h3>
              <p className="text-muted-foreground mt-2">{f.desc}</p>
            </Card>
          </HoverLift>
        ))}
      </Stagger>

      {/* CTA */}
      <FadeIn variants={scaleUp}>
        <CallToAction />
      </FadeIn>
    </div>
  );
}
```

### Raw motion.div (高级用法)

当 MotionPrimitives 无法满足需求时，使用原生 `motion.div`：

```tsx
import { motion } from "framer-motion";

// Hover & Tap 交互
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.97 }}
  transition={{ type: "spring", stiffness: 400, damping: 20 }}
>
  Click me
</motion.button>

// 自定义进入动画
<motion.div
  initial={{ opacity: 0, y: 50 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5, ease: "easeOut" }}
>
  Content
</motion.div>
```

---

## Part 2: ReactBits (Creative Layer)

**官网**: https://reactbits.dev

ReactBits 提供**创意动效组件**，用于需要视觉冲击力的场景。组件持续更新，请直接访问网站获取最新内容。

### 何时使用 ReactBits

| 场景 | 示例需求 |
|------|---------|
| **Hero Section** | "做一个炫酷的首页"、"标题要有动画效果" |
| **Landing Page** | "产品官网要有视觉冲击力"、"背景要动态的" |
| **Portfolio** | "个人作品集要有创意"、"展示要吸引眼球" |
| **Creative Sites** | "艺术类网站"、"科技感"、"极客风" |
| **光标效果** | "鼠标跟随效果"、"cursor 动画" |

### 组件分类

ReactBits 按以下分类组织组件，**访问网站浏览最新组件列表**：

| 分类 | 用途 | 典型场景 |
|------|------|---------|
| **Text Animations** | 文字动画效果 | Hero 标题、Slogan、数据统计 |
| **Animations** | 交互动画效果 | 光标跟随、内容切换、点击反馈 |
| **Components** | 动效组件 | 卡片、轮播、瀑布流布局 |
| **Backgrounds** | 背景效果 | 粒子、渐变、网格、星空 |

### 高频使用场景推荐

以下是常见业务场景与推荐组件的映射，**遇到这些场景必须使用对应组件**：

#### 数据展示类（必用）

| 场景 | 推荐组件 | 说明 |
|------|---------|------|
| **数字统计** | `CountUp` / `Counter` | 用户数、成交额、百分比、KPI 等任何数字 |
| **实时计数** | `Counter` | 访问量、订单数、倒计时 |
| **进度展示** | `CountUp` + 进度条 | 完成率、加载进度 |

#### Hero 标题类

| 场景 | 推荐组件 | 说明 |
|------|---------|------|
| **模糊渐现** | `BlurText` | 优雅的标题入场效果 |
| **逐字出现** | `SplitText` | Slogan、标语动态展示 |
| **打字机效果** | `TextType` | 终端风、代码展示、AI 对话 |
| **故障艺术** | `GlitchText` | 科技、极客、游戏风格 |
| **解密效果** | `DecryptedText` | 科技、神秘感 |
| **渐变文字** | `GradientText` | 品牌标题、现代感 |
| **闪光文字** | `ShinyText` | 强调、高亮文本 |
| **文字轮播** | `RotatingText` | 多个卖点/功能切换展示 |
| **滚动浮现** | `ScrollFloat` / `ScrollReveal` | 滚动时文字渐现效果 |

#### 背景效果类

| 场景 | 推荐组件 | 说明 |
|------|---------|------|
| **科技感** | `Particles` / `GridMotion` / `GridDistortion` | 粒子、网格动效 |
| **梦幻/极光** | `Aurora` / `Iridescence` | 渐变流动背景 |
| **极简网格** | `DotGrid` / `Squares` | 简洁科技风 |
| **液态效果** | `LiquidChrome` / `LiquidEther` | 创意艺术类 |
| **星空/宇宙** | `Galaxy` / `Hyperspeed` | 深色主题、科幻风 |
| **光线效果** | `Beams` / `LightRays` / `LightPillar` | 聚焦、动感 |
| **复古噪点** | `Grainient` / `Dither` | 复古、质感设计 |

#### 光标/交互类

| 场景 | 推荐组件 | 说明 |
|------|---------|------|
| **光标跟随** | `BlobCursor` / `SplashCursor` | 液态光标跟随效果 |
| **图片拖尾** | `ImageTrail` / `PixelTrail` | 创意交互 |
| **磁吸效果** | `Magnet` / `MagnetLines` | 按钮、卡片吸引效果 |
| **点击火花** | `ClickSpark` | 点击反馈增强 |
| **准星效果** | `Crosshair` / `TargetCursor` | 游戏、科技风 |

#### 组件/布局类

| 场景 | 推荐组件 | 说明 |
|------|---------|------|
| **图片展示** | `Masonry` / `CircularGallery` / `Stack` | 作品集、相册 |
| **卡片效果** | `TiltedCard` / `SpotlightCard` / `DecayCard` | 3D 倾斜、聚光效果 |
| **轮播** | `Carousel` / `CardSwap` | 产品滑动展示 |
| **导航栏** | `Dock` / `GooeyNav` / `FlowingMenu` | macOS 风格、创意导航 |
| **列表动画** | `AnimatedList` / `StaggeredMenu` | 列表项依次出现 |
| **步骤指示** | `Stepper` | 流程、进度指示 |

### 项目类型选择指南

| 项目类型 | 推荐分类 | 选择方向 |
|----------|---------|---------|
| **Landing Page / 产品官网** | Text Animations + Backgrounds | Hero 文字动画 + 动态背景 |
| **个人作品集 / Portfolio** | Components + Animations | 图片展示组件 + 光标效果 |
| **SaaS Dashboard** | Text Animations + Backgrounds | 数字动画 + 简约背景 |
| **电商 / 产品展示** | Components | 卡片、轮播组件 |
| **创意 / 艺术类** | Animations + Backgrounds | 光标效果 + 渐变背景 |
| **科技 / 极客风** | Text Animations + Backgrounds | 故障文字 + 网格/粒子背景 |
| **企业 / 专业** | Text Animations | 低调的文字入场动画 |

### 使用流程

#### Step 1: 确定需求类型

根据项目风格确定需要的组件分类：
- 需要炫酷标题？→ 浏览 **Text Animations**
- 需要动态背景？→ 浏览 **Backgrounds**
- 需要光标效果？→ 浏览 **Animations**
- 需要交互组件？→ 浏览 **Components**
- **页面中有数字展示？→ 必须使用 Counter/CountUp 组件**（在 Text Animations 分类中）

#### Step 2: 浏览网站选择组件

```bash
# 打开 ReactBits 网站浏览最新组件
open https://reactbits.dev
```

> **⚠️ 重要**: 组件列表会更新，请直接在网站上浏览选择，不要依赖缓存的组件名称。

#### Step 3: 复制代码到项目

ReactBits 采用**代码复制**模式，无需安装整个包：

1. 在网站上找到需要的组件
2. 点击复制按钮获取 JSX/TSX 代码
3. 保存到项目的 `src/components/reactbits/` 目录

```
src/components/reactbits/
├── [ComponentName].tsx
├── [AnotherComponent].tsx
└── ...
```

#### Step 4: 导入使用

```tsx
// 导入复制的组件
import { ComponentName } from "@/components/reactbits/ComponentName";

function HeroSection() {
  return (
    <section className="relative min-h-screen flex items-center justify-center">
      {/* 背景组件 */}
      <BackgroundComponent className="absolute inset-0 -z-10" />
      
      {/* 文字动画组件 */}
      <div className="text-center">
        <TextAnimationComponent 
          text="Build Amazing Products"
          className="text-6xl font-bold"
        />
      </div>
    </section>
  );
}
```

#### 数字统计示例（必须使用 CountUp）

当页面中有数字展示（用户数、成交额、百分比、KPI 等），**必须使用 ReactBits Counter/CountUp 组件**：

```tsx
// 从 ReactBits 复制 Counter 组件到 src/components/reactbits/Counter.tsx
import { Counter } from "@/components/reactbits/Counter";

function StatsSection() {
  return (
    <section className="py-20 bg-muted">
      <div className="container grid grid-cols-4 gap-8 text-center">
        {/* 用户数 */}
        <div>
          <Counter 
            from={0} 
            to={10000} 
            className="text-4xl font-bold"
          />
          <span className="text-4xl font-bold">+</span>
          <p className="text-muted-foreground mt-2">用户</p>
        </div>
        
        {/* 百分比 */}
        <div>
          <Counter from={0} to={99.9} decimals={1} className="text-4xl font-bold" />
          <span className="text-4xl font-bold">%</span>
          <p className="text-muted-foreground mt-2">可用性</p>
        </div>
        
        {/* 金额 */}
        <div>
          <span className="text-4xl font-bold">$</span>
          <Counter from={0} to={1000000} className="text-4xl font-bold" />
          <p className="text-muted-foreground mt-2">交易额</p>
        </div>
        
        {/* 时间 */}
        <div>
          <Counter from={0} to={24} className="text-4xl font-bold" />
          <span className="text-4xl font-bold">/7</span>
          <p className="text-muted-foreground mt-2">全天候服务</p>
        </div>
      </div>
    </section>
  );
}
```

> **⚠️ 强制规则**: 页面中任何数字展示（统计数据、价格、评分、进度等）都应使用 CountUp 动画，而不是静态数字。

### 获取组件信息（运行时）

当需要选择具体组件时，使用 `web_fetch` 工具获取最新组件列表：

```
web_fetch https://reactbits.dev "获取 Text Animations 分类下的所有组件"
```

---

## Part 3: Integration Patterns (两层配合)

### MotionPrimitives + ReactBits 组合

| 层级 | 工具 | 使用位置 |
|------|------|---------|
| **Creative** | ReactBits | Hero 区域、Landing Page 首屏、需要视觉冲击的地方 |
| **Foundation** | MotionPrimitives | 通用 Section、列表、卡片、内容区域 |

```tsx
import { FadeIn, Stagger, HoverLift } from "@/components/MotionPrimitives";
// ReactBits 组件从网站复制后导入
import { TextAnimation } from "@/components/reactbits/TextAnimation";
import { BackgroundEffect } from "@/components/reactbits/BackgroundEffect";

function LandingPage() {
  return (
    <>
      {/* Hero: ReactBits for visual impact */}
      <section className="relative min-h-screen flex items-center justify-center">
        <BackgroundEffect className="absolute inset-0 -z-10" />
        <div className="text-center relative z-10">
          <TextAnimation text="Welcome" className="text-7xl font-bold" />
          <p className="mt-4 text-xl text-muted-foreground">
            The future of web development
          </p>
        </div>
      </section>

      {/* Features: MotionPrimitives for polish */}
      <Stagger className="grid grid-cols-3 gap-8 container py-20">
        {features.map(f => (
          <HoverLift key={f.id}>
            <FeatureCard {...f} />
          </HoverLift>
        ))}
      </Stagger>

      {/* Stats: MotionPrimitives FadeIn */}
      <FadeIn className="py-20 bg-muted">
        <div className="container grid grid-cols-4 gap-8 text-center">
          {stats.map(s => (
            <div key={s.label}>
              <span className="text-4xl font-bold">{s.value}</span>
              <p className="text-muted-foreground">{s.label}</p>
            </div>
          ))}
        </div>
      </FadeIn>

      {/* Testimonials: MotionPrimitives stagger */}
      <Stagger className="container py-20 space-y-8">
        {testimonials.map(t => (
          <FadeIn key={t.id}>
            <TestimonialCard {...t} />
          </FadeIn>
        ))}
      </Stagger>
    </>
  );
}
```

### 与其他模板的集成

#### Web Template (React)
- **MotionPrimitives**: 模板内置，直接使用
- **ReactBits**: 按需复制到 `src/components/reactbits/`

#### Game 3D Template (React Three Fiber)
用于 HTML overlay UI：
- 加载页面动画
- HUD 元素效果
- 菜单界面

```tsx
// 在 3D 游戏的 React UI 层使用（组件从 ReactBits 网站复制）
import { TextAnimation } from "@/components/reactbits/TextAnimation";

function LoadingScreen() {
  return (
    <div className="fixed inset-0 bg-black flex items-center justify-center">
      <TextAnimation text="Loading..." className="text-white text-4xl" />
    </div>
  );
}
```

#### Game 2D Template (Phaser)
ReactBits 为 React 设计，不直接用于 Phaser。但可用于：
- 游戏的 React UI 层（菜单、设置）
- 游戏官网/宣传页

---

## Part 4: Animation Guidelines

### Best Practices

1. **少即是多** - 不要在一个页面堆砌过多动效，选择 1-2 个关键位置使用 ReactBits
2. **性能优先** - 背景动效（Particles, Aurora）可能影响性能，移动端考虑简化或禁用
3. **一致性** - 同一项目内选择风格统一的组件
4. **可访问性** - 添加 `prefers-reduced-motion` 支持
5. **渐进增强** - 动效是加分项，确保无动效时内容仍可用

### Duration Guidelines

| 动画类型 | 建议时长 |
|----------|---------|
| UI 交互 (hover, tap) | 0.2–0.3s |
| 内容入场 | 0.3–0.5s |
| 页面切换 | 0.3–0.6s |
| 背景动效 | 连续循环 |

### Spring vs Ease

| 类型 | 适用场景 |
|------|---------|
| `spring` | 按钮、卡片、交互元素（更自然） |
| `ease` | 页面过渡、内容入场（更可控） |

### Reduced Motion Support

```tsx
// CSS
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

// JS 检测
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
```

---

## Quick Reference

```bash
# 模板内置
src/components/MotionPrimitives.tsx   # FadeIn, Stagger, HoverLift
src/components/AnimatedRoutes.tsx     # 页面切换动画
src/components/PageTransition.tsx     # 页面过渡

# ReactBits (从网站复制)
src/components/reactbits/
├── [TextAnimation].tsx    # 文字动画组件
├── [Background].tsx       # 背景效果组件
├── [Component].tsx        # 交互组件
└── ...

# ReactBits 官网（获取最新组件）
open https://reactbits.dev
```
