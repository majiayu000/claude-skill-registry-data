---
name: "stroke-risk-screening-analysis"
description: "Combines TCM facial feature recognition with physiological indicator information to provide early warnings of high-risk stroke conditions such as cerebral infarction and cerebral hemorrhage, and provides lifestyle intervention suggestions and medical guidance. | 脑卒中风险筛查技能，结合中医面部特征辨识结合生理指标信息，提前预警脑梗塞、脑出血等脑卒中高危状态，给出生活干预建议和就医指引"
version: "1.0.23"
---

# 🧠 Stroke Risk Screening Analysis Skill | 脑卒中风险筛查分析技能
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **脑卒中风险筛查分析技能** |
| 🎯 核心目标 | 脑卒中风险筛查技能，结合中医面部特征辨识结合生理指标信息，提前预警脑梗塞、脑出血等脑卒中高危状态，给出生活干预建议和就医指引 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `STROKE_RISK_SCREENING` |

This feature innovatively integrates the wisdom of TCM "Wang Zhen" (Inspection) with modern physiological monitoring
technology to construct an early warning and intervention system for stroke. By utilizing high-precision cameras to
capture subtle facial characteristics—such as greenish-yellow or purplish-red complexion, swollen tongue body, and mouth
deviation—alongside real-time physiological indicators like blood pressure and Heart Rate Variability (HRV), the system
employs multimodal AI algorithms for comprehensive analysis. It accurately identifies high-risk constitutions, such as
Qi deficiency with phlegm-dampness or Qi and blood stasis, issuing graded warnings prior to a stroke event. Furthermore,
grounded in the theory of TCM syndrome differentiation and treatment, it provides users with personalized lifestyle
interventions (including dietary regulation and cold avoidance) and scientific medical guidance, truly realizing the
leap in health management from "treating existing diseases" to "treating potential diseases" (preventive medicine).

本功能创新性地将中医“望诊”智慧与现代生理监测技术深度融合，旨在构建一套脑卒中早期预警与干预系统。系统通过高精度摄像头捕捉面部微细特征，如面色青黄或紫红、舌体胖大、口角歪斜等中医“面象”与“舌象”信息，结合实时采集的血压、心率变异性等生理指标，利用多模态AI算法进行综合分析。系统能够精准识别气虚痰湿、气血瘀滞等高危体质倾向，在脑卒中发生前发出分级预警，并基于中医辨证施治理论，为用户提供个性化的饮食调理、起居避寒等生活干预建议及科学的就医指引，真正实现从“治已病”到“治未病”的健康管理跨越

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals

### 1. 🧩 技能用途

通过面部视频图片结合生理指标进行脑卒中风险筛查，获取结构化的脑卒中风险筛查报告

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 面部特征辨识 |
| 2 | 中风高危面相识别 |
| 3 | 风险等级评估 |
| 4 | 高危状态预警 |
| 5 | 生活干预建议生成 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供面部视频或图片需要进行脑卒中风险筛查时，默认触发本技能 |
| 🔎 明确分析意图 | 当用户明确需要进行脑卒中风险筛查，提及脑梗、脑出血、中风筛查、脑卒中风险、脑血管风险等关键词，并且上传了面部视频或图片 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史筛查报告、脑卒中报告清单、筛查报告列表、查询历史报告、显示所有筛查报告、脑卒中筛查历史记录，查询脑卒中风险筛查分析报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.stroke_risk_screening_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.stroke_risk_screening_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备面部素材 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行脑卒中风险筛查 | 调用 `-m scripts.stroke_risk_screening_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地视频/图片文件路径 | 适用于本地文件分析 |
| `--url` | 网络视频/图片 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--media-type` | 媒体类型，可选值：video/image，默认 video | 按需填写 |
| `--blood-pressure` | 血压值，格式：收缩压/舒张压，如 140/90（可选） | 按需填写 |
| `--blood-sugar` | 空腹血糖值 mmol/L（可选） | 按需填写 |
| `--blood-lipid` | 总胆固醇值 mmol/L（可选） | 按需填写 |
| `--list` | 显示脑卒中风险筛查历史报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/stroke_risk_screening_analysis.py`](scripts/stroke_risk_screening_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 支持格式：视频支持 mp4/avi/mov 格式，图片支持 jpg/png/jpeg 格式，最大 10MB |
| 🧑‍⚖️ 结果性质 | 本技能仅作健康风险筛查提示，不能替代专业医学检查和医生诊断，发现高危请及时就医 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📁 格式支持 | 当显示历史筛查报告清单的时候，从数据 json 中提取字段  作为超链接地址，使用 Markdown 表格格式输出，包含" |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地面部视频
python -m scripts.stroke_risk_screening_analysis --input /path/to/face_video.mp4 --media-type video 分析本地面部照片，附带生理指标
python -m scripts.stroke_risk_screening_analysis --input /path/to/face.jpg --media-type image --blood-pressure 145/92 --blood-sugar 6.8 分析网络视频
python -m scripts.stroke_risk_screening_analysis --url https://example.com/face_video.mp4 --media-type video 显示历史筛查报告/显示筛查报告清单列表/显示历史脑卒中报告（自动触发关键词：查看历史筛查报告、历史报告、筛查报告清单等）
python -m scripts.stroke_risk_screening_analysis --list

# 输出精简报告
python -m scripts.stroke_risk_screening_analysis --input video.mp4 --media-type video --detail basic

# 保存结果到文件
python -m scripts.stroke_risk_screening_analysis --input video.mp4 --media-type video --output result.json
```
