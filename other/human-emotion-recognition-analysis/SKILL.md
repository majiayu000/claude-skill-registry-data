---
name: "human-emotion-recognition-analysis"
description: "Uses visual AI on frontal faces to recognize multi-dimensional emotions like happiness, sadness, depression, calmness, anger, surprise, and fear in real-time. Supports emotion intensity quantification and abnormal emotion marking, suitable for human-computer interaction and mental health monitoring. | 人体视觉情绪识别技能，基于正面人脸视觉AI实时识别快乐、悲伤、抑郁、平静、愤怒、惊讶、恐惧等多维度情绪状态，支持情绪强度量化与异常情绪标记，适配人机交互、心理健康监测场景"
version: "1.0.24"
---

# 😊 Visual Emotion Recognition Skill | 人体视觉情绪识别技能
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **人体视觉情绪识别技能** |
| 🎯 核心目标 | 人体视觉情绪识别技能，基于正面人脸视觉AI实时识别快乐、悲伤、抑郁、平静、愤怒、惊讶、恐惧等多维度情绪状态，支持情绪强度量化与异常情绪标记，适配人机交互、心理健康监测场景 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `HUMAN_EMOTION_RECOGNITION` |

Based on frontal face visual AI technology, this capability recognizes multi-dimensional emotional states in real-time,
including happiness, sadness, depression, calmness, anger, surprise, and fear, while supporting emotion intensity
quantification and automatic anomaly marking. By analyzing facial expressions, eye dynamics, and micro-expression
features, the system achieves high-precision affective understanding. It is applicable to scenarios such as emotional
feedback in human-computer interaction and mental health monitoring, assisting in judging changes in user psychological
states and providing data support for intelligent intervention and emotional counseling.

本技能基于正面人脸视觉AI技术，实时识别快乐、悲伤、抑郁、平静、愤怒、惊讶、恐惧等多维度情绪状态，并支持情绪强度量化与异常情绪自动标记。系统通过分析面部表情、眼部动态及微表情特征，实现高精度情感理解。适用于人机交互中的情感反馈、心理健康监测等场景，辅助判断用户心理状态变化，为智能干预与情绪疏导提供数据支撑。

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals

### 1. 🧩 技能用途

通过人脸视频/图片进行多维度情绪识别，获取结构化的情绪识别分析报告

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 多分类情绪识别 |
| 2 | 情绪强度量化 |
| 3 | 异常情绪标记 |
| 4 | 情绪趋势统计 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供人脸视频/图片 URL 或文件需要进行情绪识别时，默认触发本技能 |
| 🔎 明确分析意图 | 当用户明确需要进行情绪识别、心理健康监测，提及情绪识别、情绪分析、心理健康、压力情绪等关键词，并且上传了视频或图片 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史识别报告、情绪识别报告清单、识别报告列表、查询历史报告、显示所有识别报告、情绪识别历史记录，查询人体情绪识别分析报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.human_emotion_recognition_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.human_emotion_recognition_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备素材输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行情绪识别 | 调用 `-m scripts.human_emotion_recognition_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地视频/图片文件路径 | 适用于本地文件分析 |
| `--url` | 网络视频/图片 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--media-type` | 媒体类型，可选值：video/image，默认 video | 按需填写 |
| `--threshold` | 异常情绪强度阈值，高于该分值标记为异常，默认 0.7 | 按需填写 |
| `--list` | 显示人体情绪识别历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/human_emotion_recognition_analysis.py`](scripts/human_emotion_recognition_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 支持格式：视频支持 mp4/avi/mov 格式，图片支持 jpg/png/jpeg 格式，最大 10MB |
| 🧑‍⚖️ 结果性质 | 本技能仅作情绪状态参考，不能替代专业心理咨询和诊断，发现持续异常情绪请及时寻求专业帮助 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📁 格式支持 | 当显示历史识别报告清单的时候，从数据 json 中提取字段  作为超链接地址，使用 Markdown 表格格式输出，包含" |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 识别本地人脸视频
python -m scripts.human_emotion_recognition_analysis --input /path/to/face_video.mp4 --media-type video

# 识别本地人脸照片，设置异常阈值
python -m scripts.human_emotion_recognition_analysis --input /path/to/face.jpg --media-type image --threshold 0.65

# 识别网络视频
python -m scripts.human_emotion_recognition_analysis --url https://example.com/face_video.mp4 --media-type video

# 显示历史识别报告/显示识别报告清单列表/显示历史情绪报告（自动触发关键词：查看历史识别报告、历史报告、识别报告清单等）
python -m scripts.human_emotion_recognition_analysis --list

# 输出精简报告
python -m scripts.human_emotion_recognition_analysis --input video.mp4 --media-type video --detail basic

# 保存结果到文件
python -m scripts.human_emotion_recognition_analysis --input video.mp4 --media-type video --output result.json
```
