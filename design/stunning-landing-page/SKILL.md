---
name: stunning-landing-page
description: 制作具有惊艳动画交互的 landing page（落地页/官网首页），也适用于个人作品集、设计师主页、工作室官网和实验型单页。用户只需给出一个主题或产品，本 skill 参考 Apple、Duolingo、Canva、Stripe、Linear、Awwwards 与 OS-HUD 实验作品集等模式，自动设计滚动叙事或单屏交互舞台、视差、微交互等效果，产出令人惊叹的单页网站。凡是用户提到 landing page、落地页、官网、产品首页、宣传页、作品集、设计师主页、酷炫动画网页、滚动动画、"像 Apple 官网那样" 等需求时，务必使用本 skill，即使用户没有明确要求动画效果。
---

# Stunning Landing Page — 惊艳动画落地页

**目标**：给定一个主题，产出一个像 Apple、Duolingo、Canva 官网那样有"哇"效果的 landing page。默认产出为**单个 HTML 文件**（CSS/JS 内联，动画库走 CDN），零构建、双击即看、方便移植到任何框架。

普通网页和惊艳网页的差距不在技术，而在三件事：**叙事**（页面是一个有起承转合的故事，或一个可探索的交互舞台）、**编排**（动画有节奏、有呼应、克制而精准）、**细节**（缓动曲线、噪点质感、悬停反馈这些 1% 的打磨）。本 skill 的流程就是围绕这三件事展开的。

## 参考文档索引

| 文件 | 内容 | 何时读 |
|------|------|--------|
| [references/animation-patterns.md](references/animation-patterns.md) | 顶级网站动画交互模式拆解（按网站和按模式两套索引） | 第 2 步选择签名动画时**必读** |
| [references/tech-toolkit.md](references/tech-toolkit.md) | GSAP/Lenis/SplitType 等库的 CDN 与可直接复用的代码片段、性能陷阱 | 第 4 步编码时**必读** |
| [references/theme-to-style.md](references/theme-to-style.md) | 主题 → 情绪基调 → 配色/字体/动画风格的映射决策表 | 第 1 步定调时**必读** |
| [references/quality-checklist.md](references/quality-checklist.md) | 交付前自检清单（动画质感、性能、响应式、可访问性） | 第 5 步交付前**必读** |

## 工作流程

### 第 1 步：定调 — 从主题推导情绪基调

读 `references/theme-to-style.md`，回答三个问题：

1. **这个产品想让访客产生什么情绪？**（敬畏 / 愉悦 / 信任 / 渴望 / 好奇 / 记忆感）
2. **对应哪种基调原型？** 例如：科技旗舰感（Apple/Linear）、活泼游戏感（Duolingo）、创意工具感（Canva/Figma）、专业信赖感（Stripe）、OS-HUD 实验作品集感
3. **一句话定位**：用 "这是一个 ___ 风格的页面，访客滚动或切换状态时会感受到 ___" 来描述。写不出这句话就不要开始写代码。

如果主题较新颖或用户点名要参考某些网站，可联网补充灵感（非必须）：
- 搜索 `site:awwwards.com` / `godly.website` / `codrops` + 主题关键词，看同类获奖作品用了什么手法
- 搜索 GitHub 上相关效果的开源实现（如 `gsap scroll animation`、`three.js hero`）
- 只取**模式和手法**，不要照抄配色与文案

### 第 2 步：编排 — 设计滚动叙事剧本

惊艳页面默认是**一场滚动驱动的演出**；当主题是个人作品集、设计师主页、实验工作室时，也可以改成**一个单屏交互舞台**。在写任何代码前，先写出剧本（直接写在思考或回复里即可）：

```
Section 1 (Hero)：开场冲击 —— 访客 0.5 秒内被什么抓住？
Section 2-N (叙事)：每屏讲一个卖点，配一个与卖点呼应的动画
Final Section (CTA)：情绪收束，行动召唤
```

如果采用 OS-HUD 单屏舞台，剧本改写成：

```
Default State：首页舞台 —— 3D/图像签名物 + 一句话身份声明
Work State：作品档案 —— 通过导航或滚动进入错位作品索引
Contact State：收束场景 —— 视觉元素聚拢，联系人和社媒成为主角
System Layer：固定 HUD —— 时间、坐标、主题、状态开关持续反馈
```

然后读 `references/animation-patterns.md`，为整页挑选 **1 个签名动画 + 3~5 个支撑模式**：

- **签名动画**（signature moment）：全页最贵的一个效果，放在 Hero 或核心卖点处，访客会因为它截图发朋友圈。如 Apple 式滚动序列帧、WebGL 渐变流体、巨字逐字浮现。
- **支撑模式**：scroll reveal、视差、磁性按钮、数字滚动等"氛围组"，让全页处处有呼吸感但不抢戏。

**克制是高级感的来源**：每屏最多一个主角动画；所有动画共用一套缓动曲线和时长体系（如统一 `cubic-bezier(0.22, 1, 0.36, 1)`、0.6~1.2s）；宁可少一个效果，不要让两个效果打架。

### 第 3 步：视觉系统 — 三分钟定好再动手

不需要完整设计稿，但必须先定死以下变量（写成 CSS 自定义属性）：

- **配色**：1 个主色 + 1 个强调色 + 背景/文字色阶（深色底易出高级感，亮色底易出愉悦感，查 theme-to-style.md 的映射表）
- **字体**：标题用有性格的展示字体，正文用高可读性字体；中文场景标题可用思源黑体加粗/抖音美好体等，英文标题可用 CDN 的 Google Fonts（如 Inter、Space Grotesk、Fraunces）
- **排版尺度**：Hero 标题要敢大（`clamp(3rem, 8vw, 7rem)` 起步），留白要敢空
- **质感层**：噪点 overlay、辉光、玻璃拟态——挑一种贯穿全页

### 第 4 步：实现 — 单文件，库走 CDN

读 `references/tech-toolkit.md` 后开始编码。硬性约定：

- 产出 `index.html` 单文件；如用户在已有项目里提需求，则遵循该项目结构
- 动画首选 **GSAP + ScrollTrigger**（CDN），平滑滚动用 **Lenis**，文字拆字用 **SplitType**；简单效果优先纯 CSS，不要为一个 fade-in 引库
- 只动画 `transform` 和 `opacity`，避免 layout 抖动
- 图片用 CSS 渐变、SVG 插画或 `picsum.photos` 占位，**不要引用不存在的本地图片路径**
- **禁止用 emoji 充当图标或装饰图形**：图标一律使用在线图标库（Remix Icon / Iconify CDN，见 tech-toolkit.md）或内联 SVG。emoji 在不同系统渲染不一致，且会瞬间拉低页面质感
- 必须实现 `prefers-reduced-motion` 降级和移动端适配
- 代码注释用中文，文件头部含 `@Date / @Author: xisy / @Discription`

### 第 5 步：自检与交付

读 `references/quality-checklist.md` 逐项过一遍。有浏览器工具时，打开页面截图检查首屏与滚动后的实际效果；发现"动画存在但不惊艳"时，回到清单里的"质感修复表"对症下药（通常是缓动太线性、节奏太均匀、或缺少质感层）。

交付时向用户说明：页面的叙事结构、签名动画是什么、如何替换占位文案和图片。

## 示例

**输入**：「给我的手冲咖啡品牌做个官网」

**定调**：温暖渴望系（理由：咖啡卖的是感官与仪式感）→ 奶油底色 + 深咖啡文字 + 琥珀强调色，衬线展示字体，缓动舒缓。

**剧本**：Hero 巨字 "晨光，注入" 逐字浮起 + 一缕 SVG 蒸汽路径动画（签名动画）→ 滚动进入"豆子的旅程"横向滚动章节 → 冲煮参数区数字滚动 + 卡片 stagger 浮现 → 用户证言 marquee → 暗色收束 CTA "预订你的第一袋"。

**实现**：GSAP ScrollTrigger 驱动横向滚动与逐字动画，Lenis 平滑滚动，全页统一 `power3.out` 缓动，噪点 overlay 营造纸张质感。
