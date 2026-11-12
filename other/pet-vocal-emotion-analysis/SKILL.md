---
name: "pet-vocal-emotion-analysis"
description: "Recognizes cat and dog barks through pet voiceprint AI, translates and outputs emotions and behavioral intentions such as happiness, excitement, anger, anxiety, pain, vigilance, and attention-seeking, enabling human-pet smart interaction. | 宠物叫声情绪解析技能，通过宠物声纹AI识别猫狗叫声，翻译输出开心、兴奋、愤怒、焦虑、痛苦、警惕、求关注等情绪与行为意图，实现人宠智能交互"
version: "1.0.25"
---

# 🔊 Pet Vocal Emotion Analysis Skill | 宠物叫声情绪解析技能
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **宠物叫声情绪解析技能** |
| 🎯 核心目标 | 宠物叫声情绪解析技能，通过宠物声纹AI识别猫狗叫声，翻译输出开心、兴奋、愤怒、焦虑、痛苦、警惕、求关注等情绪与行为意图，实现人宠智能交互 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `PET_VOCAL_EMOTION_ANALYSIS` |

Based on advanced deep acoustic models and voiceprint recognition algorithms, this feature precisely captures and
analyzes vocal characteristics of pets like cats and dogs. By extracting frequency-domain features, energy distribution,
and temporal envelopes of vocalizations, and leveraging large models trained on tens of millions of annotated samples,
the system accurately distinguishes multiple sound types such as barking, whining, and growling. Building on this, the
system further infers pets' emotional states (such as happiness, excitement, anger, anxiety, pain, and alertness) and
behavioral intentions (such as seeking attention, hunger, and the need to go out), translating these complex vocal
signals into intuitive human language output. This enables cross-species intelligent interaction, helping owners
understand their pets' needs more scientifically.

本功能基于先进的深度声学模型与声纹识别算法，能够精准捕捉并分析猫狗等宠物的发声特征。系统通过提取叫声的频域特征、能量分布与时间包络，结合千万级标注样本训练的大模型，能够精准区分吠叫、呜咽、咆哮等多种声音类型。在此基础上，系统进一步推断宠物的情绪状态（如开心、兴奋、愤怒、焦虑、痛苦、警惕）及行为意图（如求关注、饥饿、外出需求），并将这些复杂的声音信号转化为直观的人类语言输出，从而实现跨物种的智能交互，帮助主人更科学地理解爱宠需求

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals

### 1. 🧩 技能用途

通过宠物叫声/吠叫/喵呜音频AI分析，识别猫狗不同情绪和行为意图

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 声纹特征提取 |
| 2 | 情绪分类 |
| 3 | 意图翻译 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供宠物叫声音频/视频需要解析情绪时，默认触发本技能 |
| 🔎 明确分析意图 | 当用户明确需要宠物叫声解析、情绪识别时，提及宠物叫声、猫狗情绪、声纹分析、人宠交互等关键词，并且上传了音频/视频 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史解析报告、情绪解析报告清单、解析报告列表、查询历史解析、显示所有解析报告、宠物情绪分析报告，查询宠物叫声情绪解析分析报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.pet_vocal_emotion_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.pet_vocal_emotion_analysis --list` 调用 API 查询云端的历史报告数据 |
| 🚫 严格禁止 | 从本地 `memory` 目录读取历史会话信息 |
| 🚫 严格禁止 | 手动汇总本地记录中的报告 |
| 🚫 严格禁止 | 从长期记忆中提取报告 |
| ✅ 输出格式 | 必须统一从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果 |

## 📦 前置准备 | Requirements
- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 📸 识别要求 | Recognition Requirements
| 要求项 | 说明 |
|---|---|
| 叫声清晰 | ，尽量减少环境噪音和回声 |
| 包含完整叫声片段 | ，持续时间建议 3-30 秒 |
| 如果是视频录制，请确保音频清晰可辨 | 如果是视频录制，请确保音频清晰可辨 |

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
| 1 | 📥 准备宠物叫声音频/视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行宠物叫声情绪解析分析 | 调用 `-m scripts.pet_vocal_emotion_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地音频/视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络音频/视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--list` | 显示历史宠物叫声情绪解析分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/pet_vocal_emotion_analysis.py`](scripts/pet_vocal_emotion_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 支持格式：mp3/wav/mp4/avi/mov，最大 10MB |
| 🧑‍⚖️ 结果性质 | 识别准确率受环境噪音、叫声清晰度等因素影响，结果仅供娱乐互动参考 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 📝 隐私与数据安全声明 | Privacy & Data Security
| 序号 | 说明 |
|---:|---|
| 1 | **数据保密处理** |
| 2 | 系统基于 用户名/手机号 生成的标识仅作为用户关联信息，**不保存任何可直接识别个人身份的明文信息**。 |
| 3 | **安全传输** |
| 4 | 所有数据（包括视频文件及关联标识）均通过 **HTTPS/TLS 加密通道** 发送至云端 API 进行分析，防止数据在传输过程中被窃取或篡改。 |
| 5 | **数据留存策略** |
| 6 | 云端服务器遵循“最小必要原则”，**分析任务完成后即刻删除原始视频数据，不进行持久化存储**，确保用户隐私数据不被留存或滥用。 |
## 🧰 使用示例 | Examples
```bash
# 解析本地猫咪叫声音频
python -m scripts.pet_vocal_emotion_analysis --input /path/to/meow.mp3

# 解析本地视频中的狗叫声
python -m scripts.pet_vocal_emotion_analysis --input /path/to/dog_bark.mp4

# 解析网络音频
python -m scripts.pet_vocal_emotion_analysis --url https://example.com/bark.mp3

# 显示历史解析报告/显示解析报告清单列表/显示历史情绪解析（自动触发关键词：查看历史解析报告、历史报告、解析报告清单等）
python -m scripts.pet_vocal_emotion_analysis --list

# 输出精简报告
python -m scripts.pet_vocal_emotion_analysis --input meow.mp3 --detail basic

# 保存结果到文件
python -m scripts.pet_vocal_emotion_analysis --input meow.mp3 --output result.json
```
