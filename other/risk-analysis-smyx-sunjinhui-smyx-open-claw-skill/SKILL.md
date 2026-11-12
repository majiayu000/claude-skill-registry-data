---
name: "risk-analysis"
description: "Supports identifying high-risk behaviors and health risks through video/images, including elderly falls, precursors to heart attacks and strokes, and abnormal behaviors, issuing timely warning alerts. | 高风险行为识别分析工具，支持通过视频/图片识别高危行为和健康风险，包括老人跌倒、心梗脑梗前兆、异常行为等，及时发出预警提示"
version: "1.0.24"
---

# ⚠️ High-Risk Behavior Identification & Analysis Tool | 高风险行为识别分析工具
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **高风险行为识别分析工具** |
| 🎯 核心目标 | 高风险行为识别分析工具，支持通过视频/图片识别高危行为和健康风险，包括老人跌倒、心梗脑梗前兆、异常行为等，及时发出预警提示 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `OPEN_PERSON_RISK_ANALYSIS` |

Deeply integrating Computer Vision, Pose Estimation, and Multimodal Health Risk Recognition algorithms, this feature
constructs an intelligent early warning system designed for high-risk behaviors and sudden health events. The system
analyzes individual behavior patterns and physiological manifestations in real-time from video or images. It precisely
captures high-risk behaviors such as sudden posture changes during falls or prolonged stillness indicating abnormal
retention. Simultaneously, by analyzing visual cues like facial microcirculation changes, abnormal skin color, and
decreased limb coordination, it assists in identifying precursors to sudden diseases such as heart attacks and
strokes.  
Leveraging temporal behavior modeling and risk assessment models, the system effectively distinguishes between daily
activities and potential dangers. Once an anomaly is detected, it immediately triggers a multi-level warning mechanism,
notifying family members and caregivers via APP push, SMS, and voice broadcasts. It synchronously transmits anomaly
footage, risk type, and location information. This provides 24/7, unobtrusive, and precise safety protection for
high-risk groups like the elderly living alone and chronic disease patients, realizing a closed-loop health management
system that shifts from passive response to active prevention.

本功能深度融合计算机视觉、姿态估计与多模态健康风险识别算法，构建了一套面向高危行为与突发健康事件的智能预警系统。系统可实时解析视频或图片中的个体行为模式与生理表征，精准捕捉老人跌倒时的姿态骤变、异常滞留时的长时间静止等高危行为，同时通过面部微循环变化、肤色异常、肢体协调性下降等视觉线索，辅助识别心梗、脑梗等突发疾病的前兆特征。借助时序行为建模与风险等级评估模型，系统能够有效区分日常活动与潜在危险，一旦检测到异常，立即触发分级预警机制，通过APP推送、短信、语音播报等多渠道通知家属及护理人员，并同步发送异常画面、风险类型与位置信息，为独居老人、慢性病患者等高风险群体提供7×24小时无感化、精准化的安全守护，实现从被动应对到主动预防的健康管理闭环

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals

### 1. 🧩 技能用途

通过视频或图片分析识别高风险行为和健康风险，及时发出预警

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 跌倒识别 |
| 2 | 异常行为检测 |
| 3 | 心梗脑梗前兆识别 |
| 4 | 健康风险评估 |
| 5 | 实时预警 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **仅当用户明确提及"风险分析"、"跌倒"、"跌倒检测"、"行为识别"、"安全监测"、"老人看护"、"风险识别"、"高危风险识别" |
| 🖼️ 支持输入 | 本地视频/图片文件、网络视频/图片URL、实时流地址 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.risk_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.risk_analysis --list` 调用 API 查询云端的历史报告数据 |
| 🚫 严格禁止 | 从本地 `memory` 目录读取历史会话信息 |
| 🚫 严格禁止 | 手动汇总本地记录中的报告 |
| 🚫 严格禁止 | 从长期记忆中提取报告 |
| ✅ 输出格式 | 必须统一从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果 |

## 📦 前置准备 | Requirements
- 依赖说明：scripts脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  opencv-python>=4.5.5
  numpy>=1.21.0
  pillow>=9.0.0
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
| 1 | 📥 准备输入源 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行风险分析 | 调用 `-m scripts.risk_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 获取分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地文件路径（与--url二选一） | 适用于本地文件分析 |
| `--url` | 网络URL或实时流地址（与--input二选一） | API 服务自动下载网络资源 |
| `--list` | 列出该 open-id 的历史风险分析报告（与--input/--url互斥） | 用于云端历史报告查询 |
| `--page-num` | 分页页码，配合--list使用（默认 1） | 按需填写 |
| `--page-size` | 分页大小，配合--list使用（默认 30） | 按需填写 |
| `--api-url` | API服务地址（可选，使用默认值） | 按需填写 |
| `--mode` | 分析模式（all/fall/health/behavior，默认all） | 按需填写 |
| `--threshold` | 预警阈值（0.1-1.0，默认0.8） | 按需填写 |
| `--output` | 结果输出文件路径（可选） | 可选 |
| `--alert` | 是否开启自动预警（true/false，默认false） | 按需填写 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/risk_analysis.py`](scripts/risk_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/risk_categories.md`](references/risk_categories.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 支持格式：mp4/avi/mov/jpg/png/rtsp/http/https |
| 📁 格式支持 | 最大支持视频大小：200MB |
| 🧑‍⚖️ 结果性质 | 分析结果仅供参考，不能替代专业安防和医疗诊断 |
| 🔎 使用提醒 | 高风险事件会自动记录到日志目录 |
| 📁 格式支持 | 实时流分析支持持续监测，检测到风险立即触发预警 |
| 🚫 脚本限制 | **禁止临时生成脚本**：执行检测或历史报告查询时，只能使用本技能自带脚本，不得临时生成替代脚本 |

## 🧰 使用示例 | Examples
```bash
# 分析本地视频文件
python -m scripts.risk_analysis --input /path/to/video.mp4

# 分析网络视频URL
python -m scripts.risk_analysis --url https://example.com/video.mp4

# 跌倒识别模式（只检测跌倒事件）
python -m scripts.risk_analysis --input video.mp4 --mode fall

# 实时流监测（RTSP摄像头）
python -m scripts.risk_analysis --url rtsp://camera_ip:554/stream --alert true

# 自定义预警阈值
python -m scripts.risk_analysis --input video.mp4 --threshold 0.7

# 保存结果到文件
python -m scripts.risk_analysis --input video.mp4 --output result.json

# 📋 列出指定用户的历史风险分析报告
python -m scripts.risk_analysis --list

# 列出指定用户的历史报告，自定义分页
python -m scripts.risk_analysis --list --page-num 2 --page-size 20
```

## ⚠️ 风险类型说明 | Risk Type Description
| 维度/类型 | 说明 |
|---|---|
| 跌倒风险（fall） | 识别人员跌倒事件，置信度>0.8触发高等级预警 |
| 健康风险（health） | 识别心梗/脑梗前兆、突发疾病症状等 |
| 异常行为（behavior） | 识别剧烈运动、长时间静止、闯入等异常行为 |
| 综合模式（all） | 同时检测所有类型风险 |

## 🚦 预警等级 | Alert Levels
| 等级/类型 | 说明 |
|---|---|
| **高风险（红色）** | 置信度>0.9，立即触发报警 |
| **中风险（黄色）** | 置信度0.7-0.9，记录并关注 |
| **低风险（蓝色）** | 置信度0.5-0.7，仅记录日志 |
