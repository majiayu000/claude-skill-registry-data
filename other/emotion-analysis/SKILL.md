---
name: "emotion-analysis"
description: "Professional discernment of subtle cues! It performs detailed analysis and recognition of facial micro-expressions, outputs precise emotional state reports, and unveils true inner emotional activities. | 微观情绪（微表情）识别分析工具，专业察言观色！针对人物面部微表情进行细致分析识别，输出精准的情绪状态分析报告，揭示真实内心情绪活动"
version: "1.0.23"
---

# 😊 Micro-Expression Recognition & Analysis Tool | 微观情绪识别分析工具
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **微观情绪识别分析工具** |
| 🎯 核心目标 | 微观情绪（微表情）识别分析工具，专业察言观色！针对人物面部微表情进行细致分析识别，输出精准的情绪状态分析报告，揭示真实内心情绪活动 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `EMOTION_ANALYSIS` |

This tool is a professional emotion analysis system based on cutting-edge computer vision and psychological
micro-expression theory. It captures facial features with millimeter-level precision and deeply analyzes fleeting,
subtle muscle changes. By accurately identifying basic emotions—such as surprise, fear, anger, and joy—as well as
complex psychological states, the system generates a detailed emotional state analysis report. Designed to penetrate
linguistic and superficial disguises, it objectively reveals an individual's true inner emotional fluctuations,
providing scientific and quantifiable data support for psychological assessment, human-computer interaction, and
behavioral analysis.

本工具是一款基于前沿计算机视觉与心理学微表情理论的专业情绪分析系统，能够对人物面部进行毫米级特征捕捉，深度解析转瞬即逝的细微肌肉变化。通过对惊讶、恐惧、愤怒、愉悦等基础情绪及复杂心理状态的精准识别，系统将生成一份详尽的情绪状态分析报告，旨在穿透语言与表层的伪装，客观揭示个体最真实的内心情感波动，为心理评估、人机交互及行为分析提供科学、量化的数据支撑。

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals

### 1. 🧩 技能用途

通过视频分析对人物面部微表情进行精准识别，获取结构化的真实情绪状态分析报告

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 视频分析 |
| 2 | 基础情绪识别 |
| 3 | 复合情绪识别 |
| 4 | 微表情捕捉 |
| 5 | 真实情绪揭示 |
| 6 | 情绪波动分析 |
| 7 | 人际交往情绪建议 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供需要分析的人物面部视频 URL 或文件需要进行微表情情绪分析时，默认触发本技能 |
| 🔎 明确分析意图 | 当用户明确需要进行微表情分析、情绪识别、察言观色、真实情绪探测时，提及情绪分析、微表情、表情识别、察言观色、真实情绪等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史情绪报告、微表情分析报告清单、情绪分析列表、显示所有情绪报告，查询微表情情绪分析报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.emotion_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.emotion_analysis --list` 调用 API 查询云端的历史报告数据 |
| 🚫 严格禁止 | 从本地 `memory` 目录读取历史会话信息 |
| 🚫 严格禁止 | 手动汇总本地记录中的报告 |
| 🚫 严格禁止 | 从长期记忆中提取报告 |
| ✅ 输出格式 | 必须统一从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果 |

## 📦 前置准备 | Requirements
- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 😊 微表情情绪识别分析维度 | Micro-Expression Dimensions
| 维度/类型 | 说明 |
|---|---|
| **开心/愉悦** | 眼角鱼尾纹、嘴角上扬、面颊抬起 |
| 轻微愉悦 | 礼貌性微笑，肌肉轻微收缩 |
| 中度愉悦 | 自然开心笑，双眼弯起 |
| 重度愉悦 | 开怀大笑，面部肌肉充分舒展 |
| **悲伤/难过** | 嘴角下拉、眉头紧皱、眼睑下垂 |
| 轻微悲伤 | 神情黯淡，嘴角微微下沉 |
| 中度悲伤 | 眼眶湿润，眉头紧锁 |
| 重度悲伤 | 哭泣抽搐，面部肌肉颤抖 |
| **愤怒/生气** | 眉毛下压、眼睛瞪大、嘴唇紧闭 |
| 轻微愤怒 | 不满表情，神情严肃 |
| 中度愤怒 | 怒目相对，鼻翼扩张 |
| 重度愤怒 | 面部紧绷，青筋暴起 |
| **惊讶/震惊** | 眉毛上抬、眼睛睁大、嘴巴张开 |
| 轻微惊讶 | 轻度挑眉，嘴唇微张 |
| 中度惊讶 | 明显吃惊，眼睛圆睁 |
| 重度惊讶 | 极度震惊，嘴巴大张 |
| **恐惧/害怕** | 眉毛上抬并聚拢、眼睛睁大、嘴部拉伸 |
| 轻微恐惧 | 紧张不安，神情警惕 |
| 中度恐惧 | 明显害怕，身体后仰 |
| 重度恐惧 | 极度惊恐，面部僵硬 |
| **厌恶/反感** | 眉毛下压、上嘴唇抬起、鼻翼皱起 |
| 轻微厌恶 | 不屑表情，轻微撇嘴 |
| 中度厌恶 | 明显排斥，鼻子皱起 |
| 重度厌恶 | 极度反感，扭头回避 |
| **惊讶/好奇** | 眉毛微抬、目光聚焦、神情关注 |
| 轻微好奇 | 轻度关注，眼神好奇 |
| 中度好奇 | 明显感兴趣，身体前倾 |
| 重度好奇 | 极度关注，全神贯注 |
| **真实情绪伪装识别** | 识别语言与表情不一致，捕捉一闪而过的真实微表情 |
| **情绪波动分析** | 追踪情绪变化过程，识别情绪起伏波动 |
| **压抑情绪识别** | 识别被刻意压抑的真实情绪，从细微肌肉变化中发现线索 |
| **矛盾情绪识别** | 同时存在多种情绪，分析主次情绪关系 |
| **眼部区域** | 瞳孔缩放、眨眼频率、眉毛位置变化、眼睑开合程度 |
| **嘴部区域** | 嘴角微扬/下沉、嘴唇紧绷程度、咬肌紧张度 |
| **鼻部区域** | 鼻翼扩张/收缩、鼻梁皱纹变化 |
| **面颊区域** | 面颊抬起/下垂、肌肉紧张程度 |
| 表情一致性评估 | 言语表达 vs 微表情表现一致性打分 |
| 情绪真实度打分 | 0-100分，分数越低说明情绪掩饰可能性越高 |
| 关键微表情线索 | 列出最能反映真实情绪的微表情关键点 |

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
| 3 | ⚙️ 执行微表情情绪分析 | 调用 `-m scripts.emotion_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--analysis-type` | 分析类型，可选值：comprehensive/basic/micro/trust/other，默认 comprehensive（综合分析） | 按需填写 |
| `--list` | 显示微表情情绪分析历史报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/emotion_analysis.py`](scripts/emotion_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 🧑‍⚖️ 结果性质 | **专业说明**：本分析基于计算机视觉微表情识别技术，仅供参考交流使用。微表情识别不能替代专业心理测谎或心理咨询。 |
| 🧑‍⚖️ 结果性质 | **精度提示**：分析精度受视频质量、面部遮挡、光线条件等因素影响，结果仅供参考 |
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 视频要求：支持 mp4/avi/mov 格式，最大 10MB |
| 🔎 使用提醒 | **面部要求**：建议正面清晰拍摄，面部无遮挡，光线均匀，这样能获得最佳分析效果 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 综合微表情情绪分析
python -m scripts.emotion_analysis --input /path/to/face_video.mp4 --analysis-type comprehensive 基础情绪识别专项
python -m scripts.emotion_analysis --url https://example.com/face_video.mp4 --analysis-type basic 微表情捕捉专项分析
python -m scripts.emotion_analysis --input /path/to/micro_video.mp4 --analysis-type micro 情绪可信度评估
python -m scripts.emotion_analysis --input /path/to/trust_video.mp4 --analysis-type trust 显示历史分析报告/显示分析报告清单列表/显示历史情绪报告（自动触发关键词：查看历史情绪报告、历史报告、情绪报告清单等）
python -m scripts.emotion_analysis --list

# 输出精简报告
python -m scripts.emotion_analysis --input video.mp4 --analysis-type comprehensive --detail basic

# 保存结果到文件
python -m scripts.emotion_analysis --input video.mp4 --analysis-type comprehensive --output result.json
```
