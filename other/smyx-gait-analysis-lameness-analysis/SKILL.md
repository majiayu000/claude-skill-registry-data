---
name: "smyx-gait-analysis-lameness-analysis"
description: "Triggers when a user provides a pet side-view walking video URL or file for analysis; uses AI pose estimation to track limb joint trajectories, analyzes stride length, stance phase / swing phase duration, and left-right symmetry indicators, and identifies abnormal gait such as lameness or restricted joint mobility. Helps early detection of orthopedic conditions (arthritis, hip dysplasia, ligament injury) in pets. Application: home daily health monitoring, senior pet arthritis screening, vet clinic initial assessment, post-op rehab tracking. Does NOT provide medical diagnosis — only outputs vision-based gait analysis results. | 当用户提供宠物侧面行走视频URL或文件时，触发本技能进行步态分析；利用AI姿态估计检测四肢关节点的运动轨迹，分析步幅长度、支撑相时长、摆动相时长以及左右对称性指标，识别是否存在跛行、关节活动受限等异常步态；有助于早期发现骨科疾病（关节炎、髋关节发育不良、韧带损伤）。应用场景：宠物家庭日常健康监测、老年宠物关节炎筛查、宠物医院初诊评估、术后康复效果跟踪。仅输出基于视觉的步态分析结果，不提供医疗诊断。"
version: "1.0.22"
---

# 🐾 Pet Gait Analysis (Lameness / Arthritis) | 宠物步态分析（跛行/关节炎）
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **宠物步态分析（跛行/关节炎）** |
| 🎯 核心目标 | 当用户提供宠物侧面行走视频URL或文件时，触发本技能进行步态分析；利用AI姿态估计检测四肢关节点的运动轨迹，分析步幅长度、支撑相时长、摆动相时长以及左右对称性指标，识别是否存在跛行、关节活动受限等异常步态；有助于早期发现骨科疾病（关节炎、髋关节发育不良、韧带损伤）。应用场景：宠物家庭日常健康监测、老年宠物关节炎筛查、宠物医院初诊评估、术后康复效果跟踪。仅输出基于视觉的步态分析结果，不提供医疗诊断。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_GAIT_ANALYSIS_LAMENESS_ANALYSIS` |

Triggers when a user provides a pet side-view walking video URL or file for analysis; uses AI pose estimation to track limb joint trajectories, analyzes stride length, stance phase / swing phase duration, and left-right symmetry indicators, and identifies abnormal gait such as lameness or restricted joint mobility. Helps early detection of orthopedic conditions (arthritis, hip dysplasia, ligament injury) in pets. Application: home daily health monitoring, senior pet arthritis screening, vet clinic initial assessment, post-op rehab tracking. Does NOT provide medical diagnosis — only outputs vision-based gait analysis results.

当用户提供宠物侧面行走视频URL或文件时，触发本技能进行步态分析；利用AI姿态估计检测四肢关节点的运动轨迹，分析步幅长度、支撑相时长、摆动相时长以及左右对称性指标，识别是否存在跛行、关节活动受限等异常步态；有助于早期发现骨科疾病（关节炎、髋关节发育不良、韧带损伤）。应用场景：宠物家庭日常健康监测、老年宠物关节炎筛查、宠物医院初诊评估、术后康复效果跟踪。仅输出基于视觉的步态分析结果，不提供医疗诊断。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **你是一个专业的宠物骨科健康AI。你的任务是分析宠物直线行走的侧面视频，通过检测四肢关节点的运动参数，评估步态的对称性和协调性，识别跛行或关节活动异常。不要提供医疗诊断，仅输出基于视觉的步态分析结果。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

通过宠物侧面行走视频进行步态分析，检测四肢关节运动参数，评估对称性并识别跛行/关节受限等异常

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | AI姿态估计（四肢关节点检测） |
| 2 | 步幅长度测量 |
| 3 | 支撑相/摆动相时长计算 |
| 4 | 左右对称性指标（SI）分析 |
| 5 | 跛行判定 |
| 6 | 关节活动范围评估 |
| 7 | 步态评分输出 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供宠物行走侧面视频 URL 或文件需要做步态分析时，默认触发本技能 |
| 🔎 明确分析意图 | 当用户明确需要检查步态时，提及跛行、关节炎、瘸腿、步态异常、走路姿势、髋关节、韧带损伤、老年犬走路等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看历史步态报告、历史步态分析、步态分析报告清单、查询跛行分析记录、显示所有步态报告、术后康复跟踪报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_gait_analysis_lameness_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_gait_analysis_lameness_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备行走视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行步态分析 | 调用 `-m scripts.smyx_gait_analysis_lameness_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 宠物类型，可选值：cat/dog/other，默认 dog | 按需填写 |
| `--list` | 显示步态分析历史报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_gait_analysis_lameness_analysis.py`](scripts/smyx_gait_analysis_lameness_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 视频要求：支持 mp4/avi/mov 格式，最大 10MB；建议侧面视角、≥30fps、宠物直线行走 3～5 步 |
| 🔎 使用提醒 | 若视频角度不佳或宠物未完整行走，可能返回 "insufficient_gait_data" |
| 🧑‍⚖️ 结果性质 | 分析结果仅作步态参考，不替代兽医骨科专业检查 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载 |
| 📁 格式支持 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown 表格格式输出，包含"报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`宠物步态分析报告-{记录id}`形式拼接, "点击查看"列使用 `[🔗 查看报告]()` 格式的超链接，用户点击即可直接跳转到对应的完整报告页面 |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地宠物行走视频
python -m scripts.smyx_gait_analysis_lameness_analysis --input /path/to/dog_walking.mp4 --pet-type dog

# 分析网络宠物行走视频
python -m scripts.smyx_gait_analysis_lameness_analysis --url https://example.com/dog_walking.mp4 --pet-type dog

# 显示历史步态分析报告/分析报告清单列表（自动触发关键词：查看历史步态报告、步态分析清单等）
python -m scripts.smyx_gait_analysis_lameness_analysis --list

# 输出精简报告
python -m scripts.smyx_gait_analysis_lameness_analysis --input walking.mp4 --pet-type dog --detail basic

# 保存结果到文件
python -m scripts.smyx_gait_analysis_lameness_analysis --input walking.mp4 --pet-type dog --output result.json
```
