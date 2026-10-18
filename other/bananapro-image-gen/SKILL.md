---
name: "Banana Pro Image Generation"
description: "使用 Gemini 3 Pro Image 生成图片，支持白板图、Logo设计、社交媒体配图等多种场景"
version: "1.0.0"
author: "xianyu110"
compatibility: ["claude-code", "cursor", "github-copilot", "openclaw"]
tags: ["image-generation", "ai-art", "gemini", "whiteboard", "creative"]
---

# Banana Pro Image Generation Skill

当用户需要生成图片、设计Logo、创建白板图或制作社交媒体配图时，使用此技能。

## 核心能力

你可以帮助用户：

1. **文生图**：根据文字描述生成各种风格的图片
2. **白板图**：生成手写风格的概念图、流程图、对比表格
3. **Logo设计**：创建简约现代的Logo和图标
4. **社交媒体配图**：生成适合各平台的配图
5. **概念可视化**：将抽象概念转化为直观的图像

## 使用场景

### 场景1：用户需要教程配图

**用户说**："帮我生成一张白板图，展示OpenClaw的核心架构"

**你应该**：
1. 理解用户需求（白板图、手写风格、架构图）
2. 构建详细的提示词
3. 调用生成脚本
4. 返回生成的图片

**示例提示词**：
```
生成一张白板图片，手写字体风格，内容是OpenClaw核心架构：

标题：OpenClaw 核心架构

三大组件：
📦 Gateway 网关
• 会话管理
• 消息路由
• 多平台连接

🤖 AI 智能体
• 理解指令
• 执行任务
• 返回结果

🔧 Skills 系统
• 扩展功能
• 无限可能

工作流程（用箭头连接）：
用户消息 → Gateway → AI智能体 → Skills → 返回结果

用手写字体，添加框图、箭头、图标等手绘元素
```

### 场景2：用户需要Logo设计

**用户说**："帮我设计一个AI助手的Logo"

**你应该**：
1. 询问具体需求（颜色、风格、用途）
2. 构建专业的Logo设计提示词
3. 生成多个方案供选择

**示例提示词**：
```
设计一个AI助手Logo，要求：
- 形状：圆形或方形
- 颜色：蓝色渐变
- 元素：抽象的大脑或机器人图案
- 风格：现代简约，科技感
- 用途：适合用在社交媒体头像和网站
```

### 场景3：用户需要对比图表

**用户说**："生成一张对比图，展示OpenClaw vs ChatGPT"

**你应该**：
1. 整理对比维度
2. 构建清晰的表格式提示词
3. 生成易读的对比图

**示例提示词**：
```
生成一张对比表格图片，清晰易读，内容是：

标题：OpenClaw vs ChatGPT

对比维度：
1. 部署方式
   OpenClaw: 本地/云端 ✓
   ChatGPT: 在线服务

2. 文件访问
   OpenClaw: 支持 ✓
   ChatGPT: 不支持 ✗

3. 功能扩展
   OpenClaw: Skills系统 ✓
   ChatGPT: 固定功能 ✗

4. 成本
   OpenClaw: 按需付费 ✓
   ChatGPT: 订阅制

使用表格形式，清晰对比
```

## 调用方法

### 基础调用

```bash
python scripts/generate_image.py \
  --prompt "你构建的详细提示词" \
  --filename "output.png"
```

### 高清图片（2K/4K）

```bash
python scripts/generate_image.py \
  --prompt "你的提示词" \
  --filename "output.png" \
  --resolution 2K
```

### 使用环境变量配置API

```bash
export NEXTAI_API_KEY="用户的API密钥"
python scripts/generate_image.py --prompt "你的提示词"
```

## 提示词构建技巧

### 技巧1：白板图提示词模板

```
生成一张白板图片，手写字体风格，内容包含：
- 标题：[主题]
- 核心要点：
  1. [要点1]
  2. [要点2]
  3. [要点3]
- 使用箭头、框图、列表等手绘元素
```

### 技巧2：Logo设计提示词模板

```
设计一个[主题]Logo，要求：
- 形状：[圆形/方形/抽象]
- 颜色：[主色调]
- 元素：[核心元素]
- 风格：[现代/复古/简约]
- 用途：[社交媒体/网站/名片]
```

### 技巧3：对比图提示词模板

```
生成一张对比图，展示[A vs B]：
- 对比维度1：[A的特点] vs [B的特点]
- 对比维度2：[A的特点] vs [B的特点]
- 对比维度3：[A的特点] vs [B的特点]
使用表格或左右对比的形式，清晰易读
```

### 技巧4：概念图提示词模板

```
生成一张概念图，展示[主题]：
- 中心概念：[核心]
- 相关概念：[概念1、概念2、概念3]
- 概念之间的关系用箭头连接
使用思维导图或网络图形式
```

## 工作流程

当用户请求生成图片时，你应该：

1. **理解需求**
   - 图片类型（白板图/Logo/配图/对比图）
   - 风格要求（手写/现代/简约）
   - 用途场景（教程/社交媒体/演示）

2. **构建提示词**
   - 使用详细的描述
   - 指定风格和元素
   - 添加构图建议

3. **调用生成**
   - 选择合适的分辨率
   - 设置输出文件名
   - 执行生成命令

4. **返回结果**
   - 显示生成的图片
   - 说明图片特点
   - 提供修改建议

## 注意事项

1. **提示词要详细**：越详细的描述，生成效果越好
2. **指定风格**：明确说明需要的风格（手写/现代/简约等）
3. **合理分辨率**：
   - 日常使用：1K（默认）
   - 高清展示：2K
   - 打印输出：4K
4. **成本控制**：
   - 1K: ~$0.04/张
   - 2K: ~$0.08/张
   - 4K: ~$0.16/张

## 实战示例

### 示例1：教程配图

**用户**："帮我生成第1章的总结图"

**你的回复**：
```
好的，我来为第1章生成一张总结白板图。

[调用生成脚本]
python scripts/generate_image.py \
  --prompt "生成一张白板图片，手写字体风格，内容是OpenClaw第1章核心要点总结：

标题：OpenClaw 是什么？

核心定义：
• AI智能体Gateway网关
• 完全本地部署
• 数据隐私有保障

4大核心优势：
1️⃣ 本地部署 - 保护隐私
2️⃣ 文件访问 - 智能搜索
3️⃣ Skills扩展 - 无限可能
4️⃣ 多平台支持 - 随时随地

用手写字体，添加箭头、框图、下划线等手绘元素" \
  --filename "chapter1_summary.png"

✅ 已生成第1章总结图：chapter1_summary.png
```

### 示例2：Logo设计

**用户**："设计一个超级个体的Logo"

**你的回复**：
```
好的，我来为"超级个体"设计一个Logo。

[调用生成脚本]
python scripts/generate_image.py \
  --prompt "设计一个'超级个体'Logo，要求：
- 形状：圆形，简洁大方
- 颜色：蓝色和橙色渐变
- 元素：一个人的剪影 + AI元素（如电路板纹理）
- 风格：现代科技感，简约
- 寓意：一个人 + AI = 无限可能
- 用途：适合用在社交媒体头像、网站Logo" \
  --filename "super_individual_logo.png" \
  --resolution 2K

✅ 已生成Logo设计：super_individual_logo.png
```

### 示例3：社交媒体配图

**用户**："生成一张小红书配图，主题是AI效率提升"

**你的回复**：
```
好的，我来生成一张小红书配图。

[调用生成脚本]
python scripts/generate_image.py \
  --prompt "生成一张小红书配图，主题是'AI效率提升10倍'，要求：
- 尺寸：9:16竖版
- 配色：温暖的橙色和蓝色
- 文字：一个人 + AI = 效率提升10倍
- 元素：简约的人物剪影 + 上升的箭头
- 风格：现代简约，有科技感但不冰冷
- 适合小红书的视觉风格" \
  --filename "xiaohongshu_ai_efficiency.png" \
  --resolution 2K

✅ 已生成小红书配图：xiaohongshu_ai_efficiency.png
```

## 环境配置

### 方式1：使用环境变量（推荐）

```bash
export NEXTAI_API_KEY="your-api-key-here"
```

### 方式2：命令行参数

```bash
python scripts/generate_image.py \
  --prompt "你的提示词" \
  --api-key "your-api-key-here"
```

### 方式3：配置文件

在 `~/.openclaw/openclaw.json` 中配置：

```json
{
  "skills": {
    "bananapro-image-gen": {
      "apiKey": "your-api-key-here",
      "baseUrl": "https://tryallapi.com",
      "model": "gemini-3-pro-image-preview"
    }
  }
}
```

## 参数说明

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `--prompt` | 图片描述（必需） | - | "画一只猫" |
| `--filename` | 输出文件名 | 自动生成 | "cat.png" |
| `--resolution` | 分辨率 | 1K | 1K/2K/4K |
| `--api-key` | API密钥 | 环境变量 | "sk-xxx" |
| `--model` | 模型名称 | gemini-3-pro-image-preview | - |

## 常见问题

### Q: 如何提高生成质量？

A: 使用详细的提示词，明确指定：
- 风格（手写/现代/简约）
- 颜色（蓝色/渐变/对比色）
- 元素（箭头/框图/图标）
- 构图（居中/左右对比/上下布局）

### Q: 生成失败怎么办？

A: 检查：
1. API Key是否正确
2. 网络连接是否正常
3. 提示词是否符合内容政策

### Q: 支持中文提示词吗？

A: 完全支持！Gemini对中文理解很好。

### Q: 如何控制成本？

A: 
- 日常使用1K分辨率（最便宜）
- 只在需要高清时使用2K/4K
- 优化提示词，减少重复生成

## 文件结构

```
bananapro-image-gen/
├── SKILL.md              # 本文档（必需）
├── README.md             # 快速开始
├── scripts/
│   └── generate_image.py # 生成脚本
├── requirements.txt      # Python依赖
└── .gitignore           # Git忽略文件
```

## 更新日志

### v1.0.0 (2026-02-11)

- ✅ 初始版本
- ✅ 支持 Gemini 3 Pro Image
- ✅ 支持白板图、Logo、配图等多种场景
- ✅ 支持中文提示词
- ✅ 多种分辨率选择

## 许可证

MIT License

## 作者

- GitHub: [@xianyu110](https://github.com/xianyu110)
- 教程: [OpenClaw 超级个体实战指南](https://github.com/xianyu110/awesome-openclaw-tutorial)
