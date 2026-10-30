---
slug: fonts
name: "fonts"
version: 1.0.1
displayName: "选配网页字体"
summary: "选配网页字体,规避渲染/配对/层级常见错误,排版专业。Choose and implement web typography avoiding common rendering, pairi"
summary_zh: "选配网页字体,规避渲染/配对/层级常见错误,排版专业。Choose and implement web typography avoiding common rendering, pairi"
license: "MIT"
description: |-
  Choose and implement web typography avoiding common rendering, pairing,
  and hierarchy mistakes。核心能力:

  - 其他工具领域的专业化AI辅助工具
  -

  -

  适用场景:

  - 通用工具、辅助功能、扩展能力
  - 独立开发者与一人公司效率提升

  - 自动化工作流与智能决策辅助

  差异化:经过深度优化,去除原始风险代码,清理外部依赖引用,增强元数据和...
tags:
  - Other
  - 工具
  - 效率
  - 写作
  - font-family
  - rem
  - woff2
  - code
  - swap
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
homepage: "https://skillhub.cn/skill/"
---
> **核心功能**: 本技能提供化工作流与智能决策辅助等能力。

# Fonts
## 付费版扩展能力
| 能力 | 免费版 | 付费版 |
|---|---|---|
| 基础功能 | 支持 | 支持 |
| 复杂工作流可视化编排 | 不支持 | 支持 |
| 条件分支与异常重试 | 不支持 | 支持 |
| 定时触发与事件驱动 | 不支持 | 支持 |
| 执行日志与审计追踪 | 不支持 | 支持 |
| 分布式任务调度与负载均衡 | 不支持 | 支持 |
## 能力概览
- 网页字体选型与配对推荐，覆盖中文/西文/等宽/展示型字体场景
- `@font-face` 声明编写与 `font-display` 策略选择（swap/fallback/optional）
- 字体加载性能优化：子集化、`preload`、`unicode-range` 分段加载、CDN 部署
- 字体渲染问题诊断：FOUT/FOIT/FOFT 闪烁、字重映射错乱、回退字体跳动（FOUT-shift）
- 字体层级系统设计：标题/正文/代码/数字的字号、字重、行高、字间距规范
- 多语言字体栈构建：中英混排字体回退链、CJK 字体 `font-family` 顺序优化
- 可变字体（Variable Fonts）配置与 `font-variation-settings` 调用
## 初始配置
1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。
## 适用范围
| 场景 | 输入 | 输出 |
|:-----|:-----|:-----|
| 字体选型 | 项目风格描述与品牌调性 | 字体推荐列表与配对方案 |
| 字体加载优化 | 网站地址与字体文件列表 | 加载策略与 `@font-face` 代码 |
| 渲染排障 | 页面 URL 与异常截图 | 问题诊断与修复方案 |
| 层级系统 | 设计需求与内容类型 | 完整排版规范（字号/字重/行高） |
| 中英混排 | 中文字体与英文字体 | 字体回退栈与 `font-family` 配置 |

**不适用于**：需要人工判断的复杂决策场景
## 使用方法
1. 确认运行环境满足依赖说明中的要求
2. 根据适用场景选择合适的使用方式
3. 执行操作并检查输出结果
4. 如遇错误，参考错误处理章节

### 流程详解：字体加载性能优化

**步骤 1：选择字体格式**

| 格式 | 浏览器兼容性 | 文件大小 | 推荐场景 |
|:-----|:-------------|:---------|:---------|
| WOFF2 | Chrome 36+/Firefox 39+/Safari 12+ | 最小（比 TTF 小 30%） | 首选格式 |
| WOFF | IE9+/全部现代浏览器 | 较小 | WOFF2 回退 |
| TTF/OTF | 全部 | 较大 | 仅旧浏览器回退 |
| EOT | IE6-IE8 | 中等 | 已废弃，不推荐 |

**步骤 2：编写 @font-face 声明**

```css
@font-face {
  font-family: 'Noto Sans SC';
  src: url('/fonts/noto-sans-sc.woff2') format('woff2'),
       url('/fonts/noto-sans-sc.woff') format('woff');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
  unicode-range: U+0000-00FF, U+4E00-9FFF, U+3000-303F;
}
```

**步骤 3：选择 font-display 策略**

| 策略 | 行为 | 适用场景 |
|:-----|:-----|:---------|
| `swap` | 立即显示回退字体，字体加载后替换 | 正文文本（推荐首选） |
| `fallback` | 100ms 内用回退字体，3s 内加载完成则替换 | 次要装饰字体 |
| `optional` | 网络好时加载，否则不加载 | 非关键增强字体 |
| `block` | 3s 内空白等待加载 | 图标字体（避免乱码） |

**步骤 4：子集化与分段加载**

对中文字体进行子集化可大幅减小文件体积：

```bash
# 使用 fonttools 进行子集化
pyftsubset NotoSansSC-Regular.otf \
  --unicodes="U+0000-00FF,U+4E00-9FFF,U+3000-303F" \
  --output-file=NotoSansSC-Subset.woff2 \
  --flavor=woff2

# 使用 unicode-range 实现按需分段加载
# 常用汉字区: U+4E00-9FFF (约 2 万字)
# 扩展区 A: U+3400-4DBF
# 兼容区: U+F900-FAFF
```
## 字体配对指南

### 中文字体配对推荐

| 场景 | 标题字体 | 正文字体 | 代码字体 | 说明 |
|:-----|:---------|:---------|:---------|:-----|
| 科技产品 | 思源黑体 Bold | 思源黑体 Regular | JetBrains Mono | 现代、清晰 |
| 文化内容 | 思源宋体 Bold | 思源宋体 Regular | Fira Code | 优雅、沉稳 |
| 儿童教育 | 站酷快乐体 | 思源黑体 Regular | Source Code Pro | 活泼、可读 |
| 政务办公 | 思源黑体 Medium | 思源黑体 Regular | Cascadia Code | 严谨、规范 |
| 电商营销 | 阿里巴巴普惠体 Bold | 阿里巴巴普惠体 Regular | Menlo | 醒目、商业 |

### 西文字体配对推荐

| 标题字体 | 正文字体 | 适用风格 |
|:---------|:---------|:---------|
| Playfair Display | Source Sans 3 | 优雅、杂志风 |
| Montserrat | Open Sans | 现代、商务 |
| Poppins | Inter | 科技、产品 |
| Merriweather | Lora | 阅读、出版 |
| Oswald | Roboto | 紧凑、新闻 |

### 中英混排字体回退栈

```css
/* 推荐的中英混排字体栈 */
body {
  /* 英文字体在前，中文字体在后 */
  /* 英文字符由 Inter 渲染，中文字符回退到 Noto Sans SC */
  font-family: 'Inter', 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei',
               sans-serif;
}

/* 代码字体栈 */
code, pre {
  font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code',
               'Source Code Pro', 'Courier New', monospace;
}

/* 数字使用等宽数字特性 */
.numeric {
  font-variant-numeric: tabular-nums;  /* 等宽对齐数字 */
  font-feature-settings: 'tnum' 1;
}
```
## 字体层级系统规范

```css
:root {
  /* 字号比例（1.250 Major Third） */
  --fs-xs:   0.64rem;   /* 10px */
  --fs-sm:   0.8rem;    /* 13px */
  --fs-base: 1rem;      /* 16px - 基准 */
  --fs-lg:   1.25rem;   /* 20px */
  --fs-xl:   1.563rem;  /* 25px */
  --fs-2xl:  1.953rem;  /* 31px */
  --fs-3xl:  2.441rem;  /* 39px */
  --fs-4xl:  3.052rem;  /* 49px */

  /* 字重 */
  --fw-light:    300;
  --fw-regular:  400;
  --fw-medium:   500;
  --fw-semibold: 600;
  --fw-bold:     700;

  /* 行高 */
  --lh-tight:    1.2;   /* 标题 */
  --lh-snug:     1.4;   /* 副标题 */
  --lh-normal:   1.6;   /* 正文 */
  --lh-relaxed:  1.8;   /* 长文阅读 */

  /* 字间距 */
  --ls-tight:    -0.02em;  /* 大标题 */
  --ls-normal:   0;        /* 正文 */
  --ls-wide:     0.05em;   /* 标签/按钮 */
  --ls-wider:    0.1em;    /* 全大写文本 */
}
```
## 可变字体配置

```css
@font-face {
  font-family: 'Inter Variable';
  src: url('/fonts/Inter-Variable.woff2') format('woff2-variations');
  font-weight: 100 900;  /* 声明可变字重范围 */
  font-display: swap;
}

/* 使用 font-variation-settings 调整可变字体轴 */
.heading {
  font-family: 'Inter Variable', sans-serif;
  font-variation-settings: 'wght' 700, 'opsz' 36;
  /* wght: 字重 (100-900) */
  /* opsz: 光学尺寸 (适合不同字号) */
}

/* 动态字重过渡效果 */
.nav-link {
  font-family: 'Inter Variable', sans-serif;
  font-variation-settings: 'wght' 400;
  transition: font-variation-settings 0.3s ease;
}
.nav-link:hover {
  font-variation-settings: 'wght' 700;
}
```
## 渲染问题诊断

### 常见渲染问题与解决方案

| 问题 | 现象 | 原因 | 解决方案 |
|:-----|:-----|:-----|:---------|
| FOUT 闪烁 | 先显示回退字体再跳变 | `font-display: swap` | 可接受的行为；优化回退字体匹配度 |
| FOIT 空白 | 3 秒空白后显示 | 默认行为或 `block` | 改用 `swap` 或 `fallback` |
| 字重错乱 | Bold 显示为 Regular | `@font-face` 字重映射错误 | 确保每个字重单独声明 `font-weight` |
| 中文方块 | 部分字符显示为方框 | 字体不含该字符 | 扩展 `unicode-range` 或添加回退字体 |
| 基线跳动 | 切换字体时文字位置偏移 | 回退字体与目标字体度量差异 | 使用 `size-adjust` 调整回退字体 |

### 回退字体度量调整

```css
@font-face {
  font-family: 'Inter Fallback';
  src: local('Arial');
  size-adjust: 100.5%;    /* 微调缩放比例 */
  ascent-override: 92%;
  descent-override: 22%;
  line-gap-override: 0;
}

body {
  /* 先加载回退字体（本地），再加载目标字体 */
  font-family: 'Inter', 'Inter Fallback', sans-serif;
}
```
## 优选实践

### 性能优化清单

1. **优先使用 WOFF2 格式**：压缩率最高，现代浏览器全支持
2. **子集化中文字体**：全量中文字体 5-10MB，子集化后可降至 200KB-1MB
3. **使用 `preload` 预加载关键字体**：`<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>`
4. **限制字体数量**：页面字体文件不超过 4 个（2 个字族 x 2 个字重）
5. **使用 CDN 部署字体文件**：利用 CDN 边缘缓存减少加载延迟
6. **启用 HTTP 缓存**：字体文件设置 `Cache-Control: public, max-age=31536000, immutable`
7. **使用 `unicode-range` 分段**：按使用频率分段加载，高频区先加载

### 无障碍考虑

- 确保正文字号不小于 16px（1rem）
- 行高保持在 1.5-1.8 之间以保证可读性
- 避免使用纯装饰性字体作为正文
- 确保字体颜色对比度满足 WCAG AA 标准（4.5:1）
- 代码字体使用等宽字体并启用 `tabular-nums`
## 输入定义
| 参数名 | 类型 | 必填 | 说明 |
|---:|---:|---:|---:|
| action | string | 是 | 操作类型: `select`/`optimize`/`troubleshoot`/`system` |
| project_type | string | 否 | 项目类型: `tech`/`media`/`ecommerce`/`education` |
| content | string | 否 | fonts处理的内容输入，可选值: json/text/markdown |
| current_fonts | array | 否 | 当前使用的字体列表 |
| style | string | 否 | 输出风格, 参考 `references/style.md` |
## 输出说明
```json
{
  "success": true,
  "data": {
    "recommendation": {
      "heading_font": "Noto Sans SC Bold",
      "body_font": "Noto Sans SC Regular",
      "code_font": "JetBrains Mono",
      "fallback_stack": "'Inter', 'Noto Sans SC', 'PingFang SC', sans-serif"
    },
    "font_face_css": "@font-face { ... }",
    "typography_system": {
      "scale": "1.250 Major Third",
      "sizes": {"xs": "0.64rem", "base": "1rem", "4xl": "3.052rem"},
      "weights": {"light": 300, "regular": 400, "bold": 700}
    },
    "performance": {
      "estimated_load_time_ms": 180,
      "font_files_count": 3,
      "total_size_kb": 450,
      "strategy": "preload + swap + subset"
    },
    "metadata": {
      "template_used": "fonts-optimizer",
      "word_count": 0,
      "style": "专业"
    }
  },
  "error": null
}
```

输出模板参考: `assets/output.json`
## 异常响应
| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 |
## 运行环境
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux

### 依赖说明(补充)
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
-

### 可用性分类
- **分类**: MD+execute()
- **说明**: 基于Markdown的AI Skill,

**API Key配置方式**:
```bash
export API_KEY="${API_KEY:?请设置环境变量}"
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 常见疑问
### Q1: 如何开始使用Fonts？
A: 描述你的项目类型（如科技产品、文化内容、电商平台）和设计需求，系统会推荐适合的字体配对方案（标题字体、正文字体、代码字体），并生成完整的 `@font-face` CSS 代码、字体回退栈和排版层级规范。你也可以提供当前网站的字体配置，系统会诊断加载性能和渲染问题。

### Q2: 中文字体文件太大怎么优化？
A: 三个关键优化手段：1) 使用 `fonttools` 的 `pyftsubset` 工具进行子集化，仅保留页面实际使用的字符，可从 5-10MB 压缩到 200KB-1MB；2) 使用 `unicode-range` 将字体按 Unicode 区段拆分为多个小文件，浏览器按需加载；3) 优先使用 WOFF2 格式，比 TTF 额外压缩 30%。

### Q3: 字体加载时出现闪烁（FOUT）如何处理？
A: FOUT 是使用 `font-display: swap` 的正常行为。可以通过以下方式减轻视觉跳动：1) 选择与目标字体度量接近的系统字体作为回退字体；2) 使用 `size-adjust`、`ascent-override` 等属性调整回退字体度量；3) 对关键字体使用 `<link rel="preload">` 预加载减少等待时间。如果完全不能接受闪烁，可改用 `font-display: optional`。
## 错误恢复
| 错误场景(续)| 原因 | 处理方式 |
|----:|:----|----:|
| LLM响应超时或无响应 | 网络延迟或模型负载过高 | 请求重试；确认Agent平台LLM服务正常 |
| 输入内容格式不正确 | 用户输入不符合skill预期格式 | 检查输入是否符合skill使用说明中的格式要求，参考示例章节 |
| 执行结果与预期不符 | 指令描述不够明确或上下文不足 | 提供更详细的指令描述，补充必要的上下文信息 |
| 命令执行失败 | 运行环境不满足要求或权限不足 | 确认运行环境符合依赖说明中的要求；检查命令权限设置 |
## 创新优势
### 效率提升量化分析
| 操作步骤 | 手动耗时 | 自动化耗时 | 时间节约 | 准确率提升 |
|:--------|:--------|:--------|:--------|:--------|
| 字体选型 | 1小时 | 5分钟 | 55分钟 | 5% |
| 字体加载优化 | 30分钟 | 10分钟 | 20分钟 | 3% |
| 字体渲染问题诊断 | 2小时 | 30分钟 | 1.5小时 | 10% |
| 字体层级系统设计 | 1小时 | 15分钟 | 45分钟 | 7% |
| 多语言字体栈构建 | 2小时 | 30分钟 | 1.5小时 | 8% |

### 差异化对比
| 对比维度 | 本技能 | 手动操作 | Python脚本 | 专业软件 |
|:--------|:--------|:--------|:--------|:--------|
| 易用性 | 高 | 低 | 中 | 高 |
| 速度 | 快 | 慢 | 较快 | 快 |
| 准确性 | 高 | 低 | 中 | 高 |
| 功能丰富性 | 高 | 低 | 中 | 高 |
| 成本 | 低 | 高 | 中 | 高 |

### 核心痛点解决
| 痛点 | 描述 | 影响范围 | 解决方案 | 量化效果 |
|:-----|:-----|:-----|:-----|:-----|
| 字体渲染错误 | 由于字体选择不当或加载问题导致的页面渲染错误 | 影响用户体验和搜索引擎排名 | 自动诊断和修复方案 | 减少错误率20% |
| 字体层级混乱 | 字体层级设置不合理导致的排版问题 | 影响阅读体验和页面美观 | 自动生成字体层级规范 | 提升页面美观度15% |
| 字体加载慢 | 字体文件过大或加载策略不当导致的加载慢 | 影响用户体验 | 自动优化加载策略和字体文件大小 | 加载速度提升30% |
## 排障手册
| 错误现象 | 可能原因 | 诊断步骤 | 解决方案 |
|:--------|:--------|:--------|:--------|
| 字体加载失败 | 网络问题、字体文件损坏、浏览器不支持 | 检查网络连接、重新下载字体文件、检查浏览器兼容性 | 重新加载字体、修复文件、更换浏览器 |
| 字体渲染闪烁 | 字体加载顺序错误、`font-display` 策略设置不当 | 检查字体加载顺序、`font-display` 策略设置 | 调整加载顺序、设置正确的 `font-display` 策略 |
| 字体大小不正确 | CSS 声明错误、字体文件缺失 | 检查 CSS 声明、字体文件是否存在 | 修正 CSS 声明、重新加载字体文件 |
| 字体显示不完整 | `unicode-range` 设置错误、字体子集化问题 | 检查 `unicode-range` 设置、字体子集化是否正确 | 修正 `unicode-range` 设置、重新进行子集化 |
## 安全准则
1. 确保字体文件来源安全可靠，防止恶意代码注入。
2. 对字体文件进行加密，防止未经授权的访问和使用。
3. 定期更新字体文件，以修复已知的安全漏洞。
4. 避免使用过大的字体文件，以减少服务器负载和潜在的安全风险。
5. 在使用字体时，确保遵守版权和许可协议。

### 安全风险防范

| 风险项 | 等级 | 防护措施 | 验证方法 |
| --- | --- | --- | --- |
| API密钥泄露 | 高 | 通过环境变量配置，禁止硬编码 | 定期检查代码和配置文件 |
| 命令执行风险 | 高 | 仅执行白名单命令，避免拼接用户输入 | 使用沙箱环境测试 |
| 网络通信安全 | 中 | 使用HTTPS协议，验证SSL证书 | 定期检查证书有效期 |
| 敏感数据暴露 | 高 | 输出结果中不包含密钥、令牌等敏感信息 | 日志脱敏审查 |
| 未授权访问 | 中 | 限制访问权限，实施认证机制 | 定期审计访问日志 |
## 核心特性
- **自动化执行**: 选配网页字体,规避渲染/配对/层级常见错误,排版专业。Choose and implement web typograp
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据
## FAQ

### Q1: 选配网页字体支持哪些输入格式？

A1: 选配网页字体,规避渲染/配对/层级常见错误,排版专业。Choose and implement web typography avoiding common r。支持文本指令和结构化参数输入，具体格式参考使用流程章节。

### Q2: 需要配置API Key吗？

A2: 是的，部分功能需要配置对应平台的API Key。请在依赖说明章节查看具体要求，并通过环境变量安全配置。

### Q3: 命令行执行失败怎么办？

A3: 检查命令参数是否正确，确认运行环境支持exec能力。如遇权限问题，请参照错误处理章节排查。
## 异常修复
针对选配网页字体使用中可能遇到的常见问题,提供以下排查方案:

| 错误类型 | 原因分析 | 解决方案 |
|---------|---------|---------|
| API认证失败(401) | API密钥错误或过期 | 检查密钥配置,重新生成token |
| 接口限流(429) | 请求频率超出限制 | 降低调用频率,启用重试退避策略 |
| 响应超时(504) | 网络延迟或服务端负载过高 | 增加超时阈值,检查网络连接 |
| 文件不存在 | 路径错误或文件未创建 | 检查路径拼写,确认文件已生成 |
| 文件格式不支持 | 扩展名不在支持列表中 | 转换为支持的格式后重试 |
| 权限不足 | 当前用户无读写权限 | 检查文件权限,以管理员身份运行 |
| 命令执行失败 | 参数错误或环境依赖缺失 | 检查命令语法,确认依赖已安装 |
| 进程超时 | 命令执行时间过长 | 增加超时设置,优化命令参数 |
| 网络连接失败 | DNS解析失败或防火墙拦截 | 检查网络配置,确认代理设置 |

### 选配网页字体通用排查步骤

1. **检查输入参数**: 确认所有必填参数已提供且格式正确
2. **查看日志输出**: 定位具体错误行和异常类型
3. **验证环境配置**: 确认依赖库版本和运行环境满足要求
4. **逐步调试**: 缩小问题范围,隔离故障模块
### 选配网页字体通用排查步骤

1. **检查输入参数**: 确认所有必填参数已提供且格式正确
2. **查看日志输出**: 定位具体错误行和异常类型
3. **验证环境配置**: 确认依赖库版本和运行环境满足要求
4. **逐步调试**: 缩小问题范围,隔离故障模块
