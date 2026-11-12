---
name: "stranger-recognition-analysis"
description: "Identifies strangers appearing in surveillance areas through facial comparison; supports video stream and image detection, suitable for stranger warnings in residential communities, units, access control, and other scenarios. | 陌生人识别技能，通过人脸比对识别监控区域出现的陌生人员，支持视频流和图片检测，适用于小区、单位、门禁等场景的陌生人预警"
version: "1.0.23"
---

# 🕵️ Stranger Recognition Skill | 陌生人识别技能
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **陌生人识别技能** |
| 🎯 核心目标 | 陌生人识别技能，通过人脸比对识别监控区域出现的陌生人员，支持视频流和图片检测，适用于小区、单位、门禁等场景的陌生人预警 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `STRANGER_RECOGNITION` |

Based on high-precision facial recognition algorithms and feature vector comparison technology, this skill constructs an
intelligent stranger early warning mechanism for surveillance areas. The system supports dual-mode input via real-time
video stream analysis and static image detection, capable of performing millisecond-level feature matching between
captured facial information and a preset whitelist database (such as residents, employees, and regular visitors). Once
an unauthorized陌生 face is detected in scenarios like community entrances, key enterprise areas, or smart access
control points, the system immediately triggers a warning, automatically captures and stores the image, and pushes alert
information to the management terminal. This realizes a security upgrade from passive monitoring to active defense,
effectively safeguarding area security and privacy.

本技能基于高精度人脸识别算法与特征向量比对技术，构建了一套针对监控区域的智能陌生人预警机制。系统支持实时视频流分析与静态图片检测双模态输入，能够将采集到的人脸信息与预设的白名单数据库（如业主、员工、常客）进行毫秒级特征匹配。一旦在小区出入口、企事业单位重点区域或智能门禁场景中检测到未授权的陌生面孔，系统将立即触发预警，自动抓拍留存并推送告警信息至管理端，实现从被动监控到主动防御的安防升级，有效保障区域安全与隐私

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

## 🎯 任务目标 | Goals

### 1. 🧩 技能用途

通过视频流/图片进行陌生人识别，比对底库中已知人脸，识别出陌生人员，输出结构化的陌生人识别报告

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 人脸检测 |
| 2 | 人脸比对 |
| 3 | 陌生人员识别 |
| 4 | 已知人员身份确认 |
| 5 | 陌生人预警 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供监控视频/图片 URL 或文件需要进行陌生人识别时，默认触发本技能 |
| 🔎 明确分析意图 | 当用户明确需要进行陌生人识别、人脸比对、来访人员识别时，提及陌生人识别、人脸比对、陌生人员预警等关键词，并且上传了视频或图片 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史识别报告、陌生人识别报告清单、识别报告列表、查询历史报告、显示所有识别报告、陌生人识别历史记录，查询陌生人识别分析报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.stranger_recognition_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.stranger_recognition_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备媒体输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行陌生人识别 | 调用 `-m scripts.stranger_recognition_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地视频/图片文件路径 | 适用于本地文件分析 |
| `--url` | 网络视频/图片 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--media-type` | 媒体类型，可选值：video/image，默认 video | 按需填写 |
| `--threshold` | 人脸比对相似度阈值，默认 0.6，分值越高要求越严格 | 按需填写 |
| `--enroll` | 是否录入新人员到人脸识别底库，yes/no，默认 no | 按需填写 |
| `--person-name` | 人员姓名，录入底库时必须提供 | 按需填写 |
| `--person-id` | 人员ID，录入底库时可选 | 按需填写 |
| `--list` | 显示陌生人识别历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/stranger_recognition_analysis.py`](scripts/stranger_recognition_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 支持格式：视频支持 mp4/avi/mov 格式，图片支持 jpg/png/jpeg 格式，最大 10MB |
| 🔎 使用提醒 | 底库数据保存在云端，同一 open-id 下的底库数据共享 |
| 🧑‍⚖️ 结果性质 | 分析结果仅供安全管理参考，具体处置请按单位相关规定执行 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📁 格式支持 | 当显示历史识别报告清单的时候，从数据 json 中提取字段  作为超链接地址，使用 Markdown 表格格式输出，包含" |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 识别本地监控视频
python -m scripts.stranger_recognition_analysis --input /path/to/monitor.mp4 --media-type video 识别本地图片，设置 stricter 阈值
python -m scripts.stranger_recognition_analysis --input /path/to/capture.jpg --media-type image --threshold 0.7 录入新人脸到人脸识别底库
python -m scripts.stranger_recognition_analysis --input /path/to/zhangsan.jpg --media-type image --enroll yes --person-name "张三" 显示历史识别报告/显示识别报告清单列表/显示历史陌生人报告（自动触发关键词：查看历史识别报告、历史报告、识别报告清单等）
python -m scripts.stranger_recognition_analysis --list

# 输出精简报告
python -m scripts.stranger_recognition_analysis --input video.mp4 --media-type video --detail basic

# 保存结果到文件
python -m scripts.stranger_recognition_analysis --input video.mp4 --media-type video --output result.json
```
