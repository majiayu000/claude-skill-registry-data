---
name: "visual-qa-analysis"
description: "Conducts open-ended Q&A on image content based on computer vision and large language models, supporting any questions to receive natural language responses. | 大模型视觉问答（VQA）技能，基于计算机视觉和大语言模型对图片内容进行开放式问答，支持任意提问得到自然语言回答"
version: "1.0.23"
---

# ❓ Large Model Visual Question Answering Skill | 大模型视觉问答技能
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **大模型视觉问答技能** |
| 🎯 核心目标 | 大模型视觉问答（VQA）技能，基于计算机视觉和大语言模型对图片内容进行开放式问答，支持任意提问得到自然语言回答 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `VISUAL_QA` |

Deeply integrating Computer Vision (CV) and Large Language Model (LLM) technologies, this feature constructs a
next-generation open-ended image question-answering system. Through computer vision algorithms, the system performs
multidimensional analysis of images, automatically identifying visual elements such as objects, scenes, text, and chart
data. It combines this with the semantic understanding and reasoning capabilities of LLMs to achieve cross-modal
alignment between image content and natural language queries. Users can pose open-ended questions to any image (e.g., "
What is the core trend of this chart?" or "Which period does the architectural style in the picture belong to?").
Without the need for preset answer templates, the system performs logical reasoning and knowledge association based on
the image content, generating accurate and coherent natural language responses. Supporting multi-turn conversational
interaction, it meets the intelligent Q&A needs of complex scenarios such as image analysis, document interpretation,
and educational assistance.

本功能深度融合计算机视觉（CV）与大语言模型（LLM）技术，构建了新一代开放式图片问答系统。系统通过计算机视觉算法对图片进行多维度解析，自动识别物体、场景、文字、图表数据等视觉元素，并结合大语言模型的语义理解与推理能力，实现图片内容与自然语言问题的跨模态对齐。用户可对任意图片提出开放式问题（如“这张图表的核心趋势是什么？”“图片中的建筑风格属于哪个时期？”），系统无需预设答案模板，即可基于图片内容进行逻辑推理与知识关联，生成准确、连贯的自然语言回答，支持多轮对话交互，满足图像分析、文档解读、教育辅助等复杂场景下的智能问答需求

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals

### 1. 🧩 技能用途

通过图片结合用户问题进行大模型视觉问答，获得自然语言回答

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 图片内容理解 |
| 2 | 开放式问答 |
| 3 | 场景描述 |
| 4 | 细节识别 |
| 5 | 知识推理 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供图片 URL 或文件，并提出问题需要对图片进行问答时，默认触发本技能 |
| 🔎 明确分析意图 | 当用户明确需要进行视觉问答，提及 VQA、看图问答、图片问答、视觉问答等关键词，并且上传了图片 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史问答记录查询功能** ：查看历史问答记录、视觉问答历史、问答记录清单、查询历史问答，显示所有问答记录 |
| 触发规则 4 | 用户提供图片后附带问题，如"这张图片里有什么？"，直接触发视觉问答 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.visual_qa_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.visual_qa_analysis --list` 调用 API 查询云端的历史报告数据 |
| 🚫 严格禁止 | 从本地 `memory` 目录读取历史会话信息 |
| 🚫 严格禁止 | 手动汇总本地记录中的报告 |
| 🚫 严格禁止 | 从长期记忆中提取报告 |
| ✅ 输出格式 | 必须统一从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果 |

## 📦 前置准备 | Requirements
- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

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
| 1 | 📥 准备图片输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行视觉问答 | 调用 `-m scripts.visual_qa_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看回答结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地图片文件路径 | 适用于本地文件分析 |
| `--url` | 网络图片 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--question` | 用户提出的问题（必填） | 按需填写 |
| `--list` | 显示历史视觉问答列表清单 | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/visual_qa_analysis.py`](scripts/visual_qa_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 支持格式：图片支持 jpg/png/jpeg/webp 格式，最大 20MB |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 🧑‍⚖️ 结果性质 | 本技能依赖大模型生成，回答仅供参考，重要信息请核实后再使用 |
| 📁 格式支持 | 当显示历史问答清单的时候，从数据 json 中提取字段  作为超链接地址，使用 Markdown 表格格式输出，包含" |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 本地图片问答
python -m scripts.visual_qa_analysis --input /path/to/image.jpg --question "这张图片里有什么内容？请描述一下" 网络图片问答
python -m scripts.visual_qa_analysis --url https://example.com/image.jpg --question "图片中有几个人，他们在做什么？" 显示历史问答记录（自动触发关键词：查看历史问答、历史记录、问答清单等）
python -m scripts.visual_qa_analysis --list

# 输出精简回答
python -m scripts.visual_qa_analysis --input image.jpg --question "描述一下这张图片" --detail basic

# 保存结果到文件
python -m scripts.visual_qa_analysis --input image.jpg --question "请识别图片中的文字内容" --output result.json
```
