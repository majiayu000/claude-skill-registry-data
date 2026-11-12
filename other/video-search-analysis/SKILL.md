---
name: "video-search-analysis"
description: "Conducts intelligent video search based on target and semantic descriptions; supports conventional target retrieval, natural language description retrieval, and vectorized model matching. | 视频搜索/视频检索智能分析技能，基于目标、语义描述进行智能视频搜索，支持常规目标检索、自然语言描述检索、向量化模型匹配"
version: "1.0.22"
---

# 🔎 Intelligent Video Search & Retrieval Analysis Skill | 视频搜索检索智能分析技能
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **视频搜索检索智能分析技能** |
| 🎯 核心目标 | 视频搜索/视频检索智能分析技能，基于目标、语义描述进行智能视频搜索，支持常规目标检索、自然语言描述检索、向量化模型匹配 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `VIDEO_SEARCH` |

Based on multimodal large models and deep learning algorithms, this feature constructs a next-generation intelligent
video retrieval system, supporting three core modes: conventional object retrieval, natural language description
retrieval, and vectorized model matching. Through computer vision technology, the system automatically identifies and
indexes conventional targets such as people, vehicles, and objects. Simultaneously, it leverages image-text multimodal
large models to achieve cross-modal alignment between semantics and video content, enabling open-ended retrieval via
natural language descriptions like "person wearing red clothes" or "talking on the phone." Furthermore, employing a
full-modal vectorization model, the system transforms video content into high-dimensional vectors, realizing fused
retrieval across mixed modalities of text, image, and video. Supporting multi-condition combination and fuzzy semantic
matching, it rapidly locates target footage, meeting the precise retrieval demands of complex scenarios such as security
surveillance and video asset management.

本功能基于多模态大模型与深度学习算法，构建了新一代智能视频检索系统，支持常规目标检索、自然语言描述检索及向量化模型匹配三种核心模式。系统通过计算机视觉技术自动识别并索引人、车、物等常规目标，同时利用图文多模态大模型实现语义与视频内容的跨模态对齐，支持用户通过“穿红色衣服的人”、“打电话”等自然语言描述进行开放式检索。此外，系统采用全模态向量化模型，将视频内容转化为高维向量，实现文本、图像、视频混合模态的融合检索，支持多条件组合与模糊语义匹配，快速定位目标画面，满足安防监控、视频资产管理等复杂场景下的精准检索需求

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals

### 1. 🧩 技能用途

在长视频中根据用户提供的目标描述或关键词智能搜索，定位包含特定目标的片段

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | **常规目标检索**（检测特定物体/人物出现） |
| 2 | **自然语言智述检索**（用自然语言描述要找的内容） |
| 3 | **向量化模型匹配** |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户需要在视频中搜索特定内容/目标时，默认触发本技能进行视频检索分析 |
| 🔎 明确分析意图 | 当用户明确需要视频搜索、视频检索时，提及视频搜索、视频检索、找片段、定位目标、智能搜视频等关键词，并且提供了视频文件和搜索描述 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史搜索报告、视频搜索报告清单、搜索报告列表、查询历史搜索报告、显示所有搜索报告、视频检索分析报告，查询视频搜索分析报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.video_search_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.video_search_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行视频搜索智能分析 | 调用 `-m scripts.video_search_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--text` | 搜索目标/自然语言描述（说明要找什么内容） | 按需填写 |
| `--list` | 显示历史视频搜索分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/video_search_analysis.py`](scripts/video_search_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 支持格式：mp4/avi/mov，最大 1GB |
| 🧑‍⚖️ 结果性质 | 搜索结果仅供参考，请以实际视频内容为准 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 在本地视频中搜索特定目标
python -m scripts.video_search_analysis --input /path/to/life.mp4 --text "狗狗出现的片段" 在网络视频中用自然语言搜索
python -m scripts.video_search_analysis --url https://example.com/event.mp4 --text "有人发言的片段" 显示历史搜索报告/显示搜索报告清单列表/显示历史视频搜索（自动触发关键词：查看历史搜索报告、历史报告、搜索报告清单等）
python -m scripts.video_search_analysis --list

# 输出精简报告
python -m scripts.video_search_analysis --input video.mp4 --text "汽车" --detail basic

# 保存结果到文件
python -m scripts.video_search_analysis --input video.mp4 --text "人物出现" --output result.json
```
