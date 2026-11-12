---
name: "tcm-constitution-recognition-analysis"
description: "Determines nine TCM constitution types including Yin deficiency, Yang deficiency, Qi deficiency, phlegm-dampness, and blood stasis through facial features and physical signs, and provides personalized health preservation and conditioning suggestions. | 中医体质识别分析技能，通过面部特征与体征判别阴虚、阳虚、气虚、痰湿、血瘀等九种中医体质类型，给出个性化养生调理建议"
version: "1.0.24"
---

# 🧘 TCM Constitution Identification & Analysis Tool | 中医体质识别分析工具

> **AI 中医面诊体质识别** · 面部特征分析 · 九种体质辨识 · 个性化养生调理建议

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **TCM Constitution Identification & Analysis Tool / 中医体质识别分析工具** |
| 🎯 核心目标 | 基于面部照片/视频识别九种中医体质类型 |
| 🖼️ 输入类型 | 面部照片、视频、本地文件、网络图片/视频 URL |
| 🧠 分析依据 | 中医体质学说、面部特征、舌象、肤色、光泽等体征信息 |
| 📝 输出能力 | 体质类型、体质倾向、体质评分、健康风险、个性化调理建议 |
| 🌿 适用场景 | 中医体质辨识、面诊分析、养生调理、治未病健康管理 |

Based on TCM Constitution Theory and AI image recognition technology, this feature utilizes high-precision cameras to capture facial characteristics, combining them with signs from the tongue, skin color, and luster to intelligently identify nine TCM constitution types—including Yin Deficiency, Yang Deficiency, Qi Deficiency, Phlegm-Dampness, and Blood Stasis. Adhering to the national standard Classification and Determination of TCM Constitutions, the system integrates subtle facial features with identification algorithms to generate assessment reports detailing constitution types, tendency analysis, and health risks. Guided by the TCM philosophy of "Preventive Treatment of Disease" (treating potential diseases), it provides personalized regimens covering diet, daily routine, acupoint massage, and exercise, empowering users to achieve precise health preservation and constitution conditioning.

本功能基于中医体质学说与人工智能图像识别技术，通过高精度摄像头采集用户面部特征，结合舌象、肤色、光泽等体征信息，智能判别阴虚、阳虚、气虚、痰湿、血瘀等九种中医体质类型。系统依据《中医体质分类与判定》国家标准，融合面部微细特征与体质辨识算法，生成包含体质类型、倾向分析及健康风险的评估报告，并基于中医“治未病”理念，提供个性化的饮食调养、起居建议、穴位按摩及运动方案，助力用户实现精准养生与体质调理。

---

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals

### 1. 🧩 技能用途

本 Skill 用于：通过面部照片/视频，基于中医面诊原理识别九种中医体质类型。

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 面部特征提取、面色与光泽辅助分析 |
| 2 | 基于中医理论识别九种体质类型 |
| 3 | 体质评分、主要体质、次要体质倾向分析 |
| 4 | 个性化饮食、运动、生活习惯、穴位按摩建议 |
| 5 | 查询历史中医体质识别分析报告清单 |

### 3. 🌈 支持判别的九种体质

| 体质类型 | 说明 |
|---|---|
| 🌙 阴虚体质 | 支持识别 |
| ☀️ 阳虚体质 | 支持识别 |
| 💨 气虚体质 | 支持识别 |
| 🌫️ 痰湿体质 | 支持识别 |
| 🔥 湿热体质 | 支持识别 |
| 🩸 血瘀体质 | 支持识别 |
| 🌪️ 气郁体质 | 支持识别 |
| 🛡️ 特禀体质 | 支持识别 |
| 🌿 平和体质 | 支持识别 |

> 根据中医理论，“舌脉合参”面诊优先，通过面色特征辅助判别体质倾向。

### 4. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | 当用户提供面部照片需要进行中医体质识别时，默认触发本技能 |
| 🔎 明确识别意图 | 当用户明确需要中医体质识别、面诊分析时，提及中医体质、面诊、体质辨识、养生调理等关键词，并且上传了面部照片/视频 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看历史体质报告、中医体质报告清单、体质识别报告列表、查询历史体质报告、显示所有体质报告、中医体质分析报告，查询中医体质识别分析报告 |

### 5. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者照片/视频文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发任何历史报告查询关键词（如“查看所有体质报告”、“显示所有面诊结果”、“查看历史报告”等），必须直接调用云端 API 查询 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.tcm_constitution_recognition_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.tcm_constitution_recognition_analysis --list` 调用 API 查询云端的历史报告数据 |
| 🚫 严格禁止 | 从本地 `memory` 目录读取历史会话信息 |
| 🚫 严格禁止 | 手动汇总本地记录中的报告 |
| 🚫 严格禁止 | 从长期记忆中提取报告 |
| ✅ 输出格式 | 必须统一从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果 |

---

## 📦 前置准备 | Requirements

### 依赖说明

`scripts` 脚本所需的依赖包及版本：

```txt
requests>=2.28.0
```

---

## 📸 采集要求 | Capture Requirements

为了获得较准确的体质识别，请确保：

| 要求 | 说明 |
|---|---|
| 🧍 面部正对摄像头 | 光线充足均匀，避免强光和阴影 |
| 🌿 素颜最佳 | 避免浓妆影响面色特征提取 |
| 🙂 露出完整面部 | 不要口罩、帽子、墨镜遮挡 |

---

## 🚀 操作步骤 | Workflow

### 🔐 用户身份处理（内部自动完成）

> **绿色安全原则：** 用户身份参数由系统内部自动处理，**不得向用户展示、询问或要求输入任何身份标识**。

执行本技能分析或历史报告查询时，脚本会自动完成身份初始化：

| 场景 | 系统行为 |
|---|---|
| 上游系统有内部身份参数 | 由脚本静默接收并使用 |
| 上游系统未提供内部身份参数 | 脚本会自动复用本地缺省用户 |
| 本地缺省用户不存在 | 脚本会自动创建并在后续任务中复用 |
| 对用户输出 | 只展示分析进度、分析结果，不展示内部身份值 |

#### 🔒 关键约束

| 禁止/要求 | 说明 |
|---|---|
| 🚫 不得询问身份 | 不得提示用户输入用户名、手机号或任何内部身份参数 |
| 🚫 不得暴露身份值 | 不得在回复、报告、示例、错误提示中暴露内部身份值 |
| 🚫 不得列为用户参数 | 不得把内部身份参数列为用户需要理解或传入的参数 |
| ✅ 自动关联报告 | 历史报告查询同样由系统内部身份自动关联，用户只需表达“查看历史报告/报告清单”等意图 |

---

## 🧪 标准流程 | Standard Flow

| 步骤 | 阶段 | 执行动作 |
|---:|---|---|
| 1 | 📥 准备面部照片输入 | 提供本地图片/视频文件路径或网络 URL；确保满足采集要求，获得更准确结果 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行中医体质识别分析 | 调用 `-m scripts.tcm_constitution_recognition_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化的中医体质识别分析报告，包含面部基本信息、主要体质类型、次要体质倾向、各体质评分、中医理论分析、个性化养生调理建议 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地图片/视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络图片/视频 URL 地址 | API 服务自动下载 |
| `--list` | 显示历史中医体质识别分析报告列表清单 | 可以输入起始日期参数过滤数据范围 |
| `--api-url` | API 服务地址 | 可选，使用默认值 |
| `--detail` | 输出详细程度 | `basic` / `standard` / `json`，默认 `json` |
| `--output` | 结果输出文件路径 | 可选 |

---

## 🗂️ 资源索引 | Resource Index

| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/tcm_constitution_recognition_analysis.py`](scripts/tcm_constitution_recognition_analysis.py) | 调用 API 进行中医体质识别分析、本地文件上传、网络 URL 由 API 服务自动下载 | 执行分析或查询时使用 |
| ⚙️ 配置文件 | [`scripts/config.py`](scripts/config.py) | 配置 API 地址、默认参数和格式限制 | 需要确认默认配置时读取 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口详细规范和错误码 | 仅在需要了解 API 接口详细规范和错误码时读取 |

---

## ⚠️ 注意事项 | Notes

| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 支持 `jpg` / `jpeg` / `png` / `mp4` / `avi` / `mov`，最大 `10MB` |
| 🧑‍⚕️ 医疗边界 | **重要提示**：本识别结果仅供中医养生参考，不能替代专业中医师诊断，身体不适请及时就医 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载 |

---

## 🧰 使用示例 | Examples

### 🖼️ 分析本地面部照片

```bash
python -m scripts.tcm_constitution_recognition_analysis --input /path/to/face.jpg
```

### 🌐 分析网络图片

```bash
python -m scripts.tcm_constitution_recognition_analysis --url https://example.com/face.jpg
```

### 📚 显示历史分析报告 / 显示分析报告清单列表 / 显示历史体质报告

> 自动触发关键词：查看历史体质报告、历史报告、体质报告清单等。

```bash
python -m scripts.tcm_constitution_recognition_analysis --list
```

### 🪶 输出精简报告

```bash
python -m scripts.tcm_constitution_recognition_analysis --input face.jpg --detail basic
```

### 💾 保存结果到文件

```bash
python -m scripts.tcm_constitution_recognition_analysis --input face.jpg --output result.json
```
