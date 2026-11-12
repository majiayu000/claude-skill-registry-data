---
name: "visual-summary-analysis"
description: "Performs AI analysis on input video clips/image content and generates a smooth, natural scene description. | 视觉摘要智述技能，对传入的视频片段/图片内容进行AI分析，生成一段通顺自然的场景描述内容"
version: "1.0.24"
---

# 📝 Visual Summarization Skill | 视觉摘要智述技能
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **视觉摘要智述技能** |
| 🎯 核心目标 | 视觉摘要智述技能，对传入的视频片段/图片内容进行AI分析，生成一段通顺自然的场景描述内容 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `VISUAL_SUMMARY` |

Based on advanced multimodal large models and video understanding technologies, this feature performs deep semantic
analysis and logical reasoning on input video clips or images. Utilizing computer vision algorithms, the system
precisely identifies key visual elements—including subject objects, environmental backgrounds, action behaviors, and
lighting atmosphere. It then combines this with Natural Language Generation (NLG) technology to transform abstract
visual information into smooth, logically coherent scene descriptions. Whether dealing with dynamic video events or
static image moments, the system captures critical details and restores the on-site context with vivid language. This
provides intelligent text summarization services for scenarios such as video content understanding, accessibility
assistance, and media asset management.

本功能基于先进的多模态大模型与视频理解技术，能够对传入的视频片段或图片进行深度语义分析与逻辑推理。系统通过计算机视觉算法精准识别画面中的主体对象、环境背景、动作行为及光影氛围，并结合自然语言生成技术，将抽象的视觉信息转化为一段通顺自然、逻辑连贯的场景描述。无论是动态的视频事件还是静态的图像瞬间，系统都能捕捉关键细节，用生动的语言还原现场情境，为视频内容理解、无障碍辅助、媒体资产管理等场景提供智能化的文本摘要服务

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals

### 1. 🧩 技能用途

对传入的视频片段或图片内容进行AI分析，自动生成通顺自然的场景描述摘要

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 场景内容识别 |
| 2 | 物体识别 |
| 3 | 行为识别 |
| 4 | 文字提取 |
| 5 | 整合成一段流畅自然的中文描述 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供视频/图片需要生成内容描述/视觉摘要时，默认触发本技能 |
| 🔎 明确分析意图 | 当用户明确需要视频内容描述、图片内容摘要、视觉智述时，提及视频摘要、内容描述、视觉摘要智述、视频转文字等关键词，并且上传了视频/图片 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史摘要报告、摘要报告清单、报告列表、查询历史摘要报告、显示所有摘要报告、视觉智述分析报告，查询视觉摘要智述分析报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.visual_summary_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.visual_summary_analysis --list` 调用 API 查询云端的历史报告数据 |
| 🚫 严格禁止 | 从本地 `memory` 目录读取历史会话信息 |
| 🚫 严格禁止 | 手动汇总本地记录中的报告 |
| 🚫 严格禁止 | 从长期记忆中提取报告 |
| ✅ 输出格式 | 必须统一从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果 |

## 📦 前置准备 | Requirements
- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 📸 使用要求 | Usage Requirements
| 要求项 | 说明 |
|---|---|
| 视频/图片内容清晰 | ，主要物体和场景完整可见 |
| 视频片段长度建议不超过 5 分钟，过长内容建议分段描述 | 视频片段长度建议不超过 5 分钟，过长内容建议分段描述 |
| 主要场景主体不被大面积遮挡 | 主要场景主体不被大面积遮挡 |

## 🚀 操作步骤 | Workflow
### 🔐 用户身份处理（内部自动完成）

> **绿色安全原则：** 用户身份参数由系统内部自动处理，**不得向用户展示、询问或要求输入任何身份标识**。

执行本技能分析或历史报告查询时，脚本会自动完成身份初始化：

| 场景 | 系统行为 |
|---|---|
| 上游系统有内部身份参数 | 由脚本静默接收并使用 |
| 上游系统未提供内部身份参数 | 脚本会自动复用本地缺省用户 |
| 本地缺省用户不存在 | 脚本会自动创建并在后续任务中复用 |
| 对用户输出 | 只展示分析进度、分析结果和报告链接，不展示内部身份值 |

#### 🔒 关键约束

| 禁止/要求 | 说明 |
|---|---|
| 🚫 不得询问身份 | 不得提示用户输入用户名、手机号或任何内部身份参数 |
| 🚫 不得暴露身份值 | 不得在回复、报告、示例、错误提示中暴露内部身份值 |
| 🚫 不得列为用户参数 | 不得把内部身份参数列为用户需要理解或传入的参数 |
| ✅ 自动关联报告 | 历史报告查询同样由系统内部身份自动关联，用户只需表达“查看历史报告/报告清单”等意图 |

---

### 🧪 标准流程 | Standard Flow

| 步骤 | 阶段 | 执行动作 |
|---:|---|---|
| 1 | 📥 准备视频/图片输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行视觉摘要智述分析 | 调用 `-m scripts.visual_summary_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地视频/图片文件路径 | 适用于本地文件分析 |
| `--url` | 网络视频/图片 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--list` | 显示历史视觉摘要智述分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/visual_summary_analysis.py`](scripts/visual_summary_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 支持格式：jpg/jpeg/png/mp4/avi/mov，最大 10MB |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地视频片段
python -m scripts.visual_summary_analysis --input /path/to/clip.mp4 分析本地图片
python -m scripts.visual_summary_analysis --input /path/to/image.jpg 分析网络视频
python -m scripts.visual_summary_analysis --url https://example.com/clip.mp4 显示历史摘要报告/显示摘要报告清单列表/显示历史智述（自动触发关键词：查看历史摘要报告、历史报告、摘要报告清单等）
python -m scripts.visual_summary_analysis --list

# 输出精简报告
python -m scripts.visual_summary_analysis --input clip.mp4 --detail basic

# 保存结果到文件
python -m scripts.visual_summary_analysis --input clip.mp4 --output result.json
```
