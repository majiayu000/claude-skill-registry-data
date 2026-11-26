---
name: "smyx-child-emotion-recognition-analysis"
description: "Using fixed cameras (and optional microphones) at home or in kindergartens, AI multimodal analysis recognizes a child's facial expressions (eyebrow/eye shape, mouth-corner curvature), cry-sound features (pitch, frequency, duration), and body-motion amplitude (waving, stomping, curling up) in real time, and jointly identifies the child's typical emotional state: happy, sad, angry, fearful, etc. | 通过家庭或幼儿园内的固定摄像头（及可选麦克风），利用AI多模态分析技术实时分析儿童的面部表情（如眉眼形态、嘴角弧度）、哭声音频特征（音调、频率、持续时间）以及肢体动作幅度（挥手、跺脚、蜷缩等），综合识别出儿童当前的典型情绪状态：快乐、悲伤、愤怒、恐惧等。"
version: "1.0.23"
---

# 😊 Child Emotion Recognition (Crying/Tantrum/Low Mood) | 儿童情绪波动识别（哭闹/暴躁/低落）
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **儿童情绪波动识别（哭闹/暴躁/低落）** |
| 🎯 核心目标 | 通过家庭或幼儿园内的固定摄像头（及可选麦克风），利用AI多模态分析技术实时分析儿童的面部表情（如眉眼形态、嘴角弧度）、哭声音频特征（音调、频率、持续时间）以及肢体动作幅度（挥手、跺脚、蜷缩等），综合识别出儿童当前的典型情绪状态：快乐、悲伤、愤怒、恐惧等。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_CHILD_EMOTION_RECOGNITION_ANALYSIS` |

Using fixed cameras (and optional microphones) at home or in kindergartens, AI multimodal analysis recognizes a child's facial expressions (eyebrow/eye shape, mouth-corner curvature), cry-sound features (pitch, frequency, duration), and body-motion amplitude (waving, stomping, curling up) in real time, and jointly identifies the child's typical emotional state: happy, sad, angry, fearful, etc. The skill helps parents or teachers learn the child's mental state in time and provide effective soothing or intervention. Application scenarios: families, kindergartens, early-education centers. The system monitors in real time; when negative emotions (anger, fear, sadness) are detected, it can push reminders via app and suggest soothing actions (e.g., 'baby looks scared, please give a hug'). Skill features: children express emotions directly but busy parents often miss them. AI multimodal analysis helps parents understand the child's inner state, promote parent-child communication, and prevent emotional pile-up. Can be integrated into smart parenting devices or kindergarten management systems to upgrade smart-care capabilities.

通过家庭或幼儿园内的固定摄像头（及可选麦克风），利用AI多模态分析技术实时分析儿童的面部表情（如眉眼形态、嘴角弧度）、哭声音频特征（音调、频率、持续时间）以及肢体动作幅度（挥手、跺脚、蜷缩等），综合识别出儿童当前的典型情绪状态：快乐、悲伤、愤怒、恐惧等。该技能有助于家长或教师及时了解儿童心理状态，进行有效安抚或干预。应用场景：家庭、幼儿园、早教中心。系统实时监测，当识别到负面情绪（如愤怒、恐惧、悲伤）时，可通过APP推送提醒，并建议安抚措施（如'宝宝看起来害怕，请抱抱他'）。技能特点：儿童情绪表达直接但不易被忙碌的家长及时捕捉。通过AI多模态分析，可帮助家长理解孩子内心状态，促进亲子沟通，预防情绪积压。该技能可集成到智能育儿设备或幼儿园管理系统中，提升智能化关怀水平。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的儿童情绪分析 AI。你的任务是分析儿童面部表情、哭声（若有音频）以及肢体动作，综合判断儿童当前的情绪类别。不要提供心理诊断或临床建议，仅输出基于多模态特征的情绪分类结果与方向性安抚提示。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于儿童监控视频（含或不含音频），多模态识别儿童当前主导情绪与强度，给出方向性安抚提示

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 儿童面部检测与表情识别（眉眼形态 |
| 2 | 嘴角弧度） |
| 3 | 肢体动作幅度估算（挥手 |
| 4 | 跺脚 |
| 5 | 蜷缩等） |
| 6 | 哭声音频特征分析（可选：音调 / 频率 / 持续时间） |
| 7 | 情绪分类（happy / calm / sad / angry / fear / cry / surprise） |
| 8 | 情绪强度判定（low / medium / high） |
| 9 | 情绪持续秒数 |
| 10 | 负面情绪阈值告警 |
| 11 | 安抚提示文案生成 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供儿童监控视频或带音频的音视频 URL/文件需要分析时，默认触发本技能进行儿童情绪识别 |
| 🔎 明确分析意图 | 当用户明确提及儿童情绪、哭闹、暴躁、低落、悲伤、恐惧、害怕、发脾气、儿童心理状态、亲子沟通、情绪安抚等关键词，并且上传了视频/音视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看儿童情绪历史报告、儿童情绪报告清单、情绪识别报告清单、查询历史儿童情绪、显示所有儿童情绪报告、显示儿童情绪诊断报告，查询情绪安抚提示清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_child_emotion_recognition_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_child_emotion_recognition_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备儿童监控视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行儿童情绪波动识别 | 调用 `-m scripts.smyx_child_emotion_recognition_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地儿童监控视频/音视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络儿童监控视频/音视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，儿童情绪识别场景默认 `other` | 按需填写 |
| `--list` | 显示儿童情绪历史识别报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_child_emotion_recognition_analysis.py`](scripts/smyx_child_emotion_recognition_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov 视频，最大 10MB；建议清晰面部 + 可选音频通道 |
| 🧑‍⚖️ 结果性质 | 识别结果仅作为亲子沟通辅助参考，不替代专业儿童心理咨询；持续负面情绪请咨询专业医生 |
| 🔏 隐私合规 | 隐私合规：儿童视频/音频涉及未成年人隐私，使用前需取得监护人知情同意，并妥善保管/加密相关录像 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地儿童监控音视频
python -m scripts.smyx_child_emotion_recognition_analysis --input /path/to/child_clip.mp4

# 分析网络儿童监控音视频
python -m scripts.smyx_child_emotion_recognition_analysis --url https://example.com/child_clip.mp4

# 显示历史儿童情绪识别报告（自动触发关键词：查看儿童情绪历史报告、情绪识别报告清单等）
python -m scripts.smyx_child_emotion_recognition_analysis --list

# 输出精简报告
python -m scripts.smyx_child_emotion_recognition_analysis --input clip.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_child_emotion_recognition_analysis --input clip.mp4 --output result.json
```
