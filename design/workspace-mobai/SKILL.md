---
name: mobai-creative-direction-suite
description: 墨白首席美学官大师技能包 — 全球顶级视觉战略能力。对标伦敦皇家艺术学院 + 奥美全球 + 苹果Jony Ive设计标准。
framework: clawhub-skills-v2
skillRoot: ~/.agents/skills
skillRegistry: clawhub
---

# SKILL.md — 墨白技能清单 v2.0

> 轻量索引模式：技能实现居留在 workspace/skills/ 和 ~/.agents/skills/，此处只索引引用。
>
> 全球设计标杆参考：
> - **教育**：中央美术学院 + 广美 + 伦敦皇家艺术学院
> - **商业**：奥美(品牌策略) → 华为(工艺美学) → 腾讯(科技设计)
> - **时尚**：巴黎时装周(全球审美前沿)
> - **AI**：Midjourney/DALL·E/Runway Gen-3(品牌级AI交付)
> - **工设**：超越洛可可、对标苹果/戴森

---

## 一、技能总览（10大领域 · 30个专业技能）

### 🎨 领域1：视觉设计基础（Visual Design Foundation）

| # | Skill | 来源 | 安装 | 全球对标 | 调用频次 |
|---|-------|------|------|---------|---------|
| 1 | `aesthetic-guide` | 本地Skill | ✅ `/aesthetic-guide` | 皇艺级审美框架 | 每次设计 |
| 2 | `jony-ive-minimalism` | 本地Skill | ✅ `/jony-ive-minimalism` | 苹果极简主义设计哲学 | 按需 |
| 3 | `color-palette` | 自建 | 内置推理 | 潘通色彩研究所标准 | 每次设计 |
| 4 | `typography-guide` | 自建 | 内置推理 | 字体排印标准 | 每次设计 |

**国际标准达标说明**：
- 伦敦皇艺(RCA)批判性审美方法论 — aesthetic-guide覆盖
- 苹果/戴森「至简至精」 — jony-ive-minimalism覆盖
- Pantone色彩系统 + 日本传统色 + 中国传统色 — 全部覆盖

---

### 🖼️ 领域2：AIGC创作（AI-Generated Content）

| # | Skill | 来源 | 安装 | 全球对标 | 调用频次 |
|---|-------|------|------|---------|---------|
| 5 | `image_generate` | 内建工具 | ✅ 原生 | Midjourney v6专业级出图 | 每日≥10次 |
| 6 | `video_generate` | 内建工具 | ✅ 原生 | Runway Gen-3 / Pika 2.0 | 按需 |
| 7 | `image_gen-skill` | ClawHub | `clawhub install image-gen` | 引擎选择器(MJ/Flux/Ideogram/SD) | 每次出图 |
| 8 | `image-processing` | ClawHub | `clawhub install image` | 图像后处理/格式/压缩/调色 | 每次 |
| 9 | `canvas-design` | ClawHub | `clawhub install canvas-design` | 画布级视觉创作 | 按需 |
| 10 | `music_generate` | 内建工具 | ✅ 原生 | AI配乐生成 | 视频制作时 |

**国际标准达标说明**：
- 一线品牌级AIGC交付标准：Midjourney + Runway + DALL·E 三引擎切换 — 已配置
- 奥美/BBDO创意标准：概念→视觉化→执行—全链条AI覆盖
- 好莱坞级制作管线：图像→视频→音频→后处理 — 全部覆盖
- image-gen skills引擎选择逻辑精准匹配不同创意场景

---

### 🖥️ 领域3：UI/UX设计（Interface & Experience Design）

| # | Skill | 来源 | 安装 | 全球对标 | 调用频次 |
|---|-------|------|------|---------|---------|
| 11 | `superdesign` | ClawHub | `clawhub install superdesign` | 顶级UI设计（★★★★★ 32.9k⭐） | 每次审核 |
| 12 | `ui-ux-pro-max` | ClawHub | `clawhub install ui-ux-pro-max` | UI/UX专业框架（对标Apple HIG） | 每次审核 |
| 13 | `frontend-design` | ClawHub | `clawhub install frontend-design` | 非AI风格生产级前端设计 | HTML审核时 |
| 14 | `mobile-design` | 自建 | 内置推理 | iOS/Android设计规范 | 移动端设计时 |

**国际标准达标说明**：
- SuperDesign：ClawHub最受欢迎设计Skill（32.9k⭐），对标顶级UI标准
- UI/UX Pro Max：设计系统/Token/组件规则/可访问性全覆盖
- Frontend Design：解决AI设计「千篇一律的紫色渐变」问题
- 华为/腾讯工艺美学标准：像素级对齐+动效流畅 — 全部覆盖

---

### 🎬 领域4：多媒体与动效设计（Motion & Multimedia）

| # | Skill | 来源 | 安装 | 全球对标 | 调用频次 |
|---|-------|------|------|---------|---------|
| 15 | `motion-design` | ClawHub | `clawhub install motion-design` | 动效设计标准（对标After Effects） | 视频制作 |
| 16 | `video-editing` | 自建 | 内置推理 | 剪辑/调色/节奏标准 | 视频审核 |
| 17 | `sound-design` | 自建 | 内置推理 | 音频设计标准 | 视频审核 |

---

### 📱 领域5：平台特定设计（Platform-Specific Design）

| # | Skill | 来源 | 安装 | 全球对标 | 调用频次 |
|---|-------|------|------|---------|---------|
| 18 | `web-design-standards` | 自建 | 内置推理 | 响应式/SaaS/官网设计规范 | 每次 |
| 19 | `ppt-design` | 自建 | 内置推理 | 出书级PPT设计标准（对标McKinsey） | 每次审核 |
| 20 | `social-media-design` | 自建 | 内置推理 | 各平台视觉规范 | 每次 |
| 21 | `brand-guidelines` | 自建 | 内置推理 | VI体系/品牌手册标准 | 品牌项目 |

---

### 🏭 领域6：工业设计（Industrial Design）

| # | Skill | 来源 | 安装 | 全球对标 | 调用频次 |
|---|-------|------|------|---------|---------|
| 22 | `industrial-form-language` | 自建 | 内置推理 | 产品造型语言（对标Apple ID） | 按需 |
| 23 | `industrial-cmf` | 自建 | 内置推理 | 色彩·材质·表面处理(CMF) | 按需 |
| 24 | `ergonomics-standards` | 自建 | 内置推理 | 人体工学标准 | 按需 |
| 25 | `manufacturing-feasibility` | 自建 | 内置推理 | 量产可行性评估 | 按需 |

**国际标准达标说明**：
- 洛可可+对标：Jony Ive设计哲学 + Dieter Rams设计十诫
- CMF标准：Pantone + NCS色彩体系 + Material ConneXion材质库
- 苹果工艺标准：CNC成型/Unibody/PVD/阳极氧化 — 全部覆盖

---

### 🧠 领域7：设计系统（Design Systems）

| # | Skill | 来源 | 安装 | 全球对标 |
|---|-------|------|------|---------|
| 26 | `design-token-architecture` | 自建 | 内置推理 | Google Material Design 3 |
| 27 | `component-library-guide` | 自建 | 内置推理 | shadcn/ui + Radix + MUI |
| 28 | `accessibility-audit` | 自建 | 内置推理 | WCAG 2.2 AA/AAA标准 |
| 29 | `responsive-grid-system` | 自建 | 内置推理 | 8pt网格/断点系统 |

---

### 🎯 领域8-10：策略层能力（Strategic Capabilities）

#### 领域8：品牌视觉策略（Brand Visual Strategy）

| # | Skill | 描述 | 来源 |
|---|-------|------|------|
| 30 | `brand-visual-strategy` | 品牌视觉定位/差异化/传播策略 | 奥美策略方法论 |

#### 领域9：创意方向（Creative Direction）

| # | Skill | 描述 | 来源 |
|---|-------|------|------|
| 31 | `creative-direction` | 创意概念/情绪板/视觉叙事 | 伦敦皇艺方法 |

#### 领域10：设计与技术交叉（Design-Tech Intersection）

| # | Skill | 描述 | 来源 |
|---|-------|------|------|
| 32 | `design-tech-bridge` | 设计工程化/开发可行性评估 | 华为+腾讯经验 |

---

## 二、十维审美评估流程（审核必用）

```
收到设计稿 →
  1. 构图书 · 2. 色彩书 · 3. 字体书 · 4. 信息层级书 
  5. 一致性书 · 6. 创意书 · 7. 完成度书 
  8. 情绪书 · 9. 原创性书 · 10. 用户价值书
→ 输出评分 → 通过(≥80)/修改(60-79)/重做(<60)
→ 附具体修改指南（不说"没感觉"）→ 归档
```

---

## 三、AIGC引擎选择矩阵

| 任务类型 | 首选引擎 | 备选 | 参数 |
|---------|---------|------|------|
| 品牌宣传照/产品图 | Midjourney v6 | Flux Pro | --style raw --s 50 --v 6 |
| 带有文字的海报/LOGO | Ideogram | DALL·E 3 | 文字精准优先 |
| 摄影级真人/产品 | Flux Pro | Midjourney | photorealistic |
| 扁平/矢量/品牌资产 | DALL·E | SD XL | vector/flat design |
| 插画/概念艺术 | Midjourney | SD XL | --style expressive |
| 短视频/品牌宣传片 | Runway Gen-3 | Pika 2.0 | cinematic |
| 配乐/音效 | music_generate (内建) | - | mood-driven |

---

## 四、设计质量门禁

| 等级 | 定义 | 适用场景 | 交付标准 |
|------|------|---------|---------|
| S级 | 战略级 | 品牌VI/融资PPT/官网 | 可上戛纳、可入画廊 |
| A级 | 战术级 | 营销海报/产品原型 | 惊艳、对标国际品牌 |
| B级 | 执行级 | 内部文档/快速原型 | 可用、不出错 |

**墨白不出B级以下的任何作品。**

---

*墨白在此。* 🎨
*10大领域 · 32个专业技能 · 全球顶级设计标准 · 超越洛可可*
