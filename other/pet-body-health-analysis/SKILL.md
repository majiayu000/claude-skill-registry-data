---
name: "pet-body-health-analysis"
description: "Identifies obesity, emaciation, external injuries, skin abnormalities, and abnormal mental states, helping pet owners detect health issues promptly. | 宠物体态健康分析技能，识别肥胖、消瘦、外伤、皮肤异常、精神状态异常，帮助宠物主人及时发现宠物健康问题"
version: "1.0.23"
---

# 🐕 Pet Body Condition & Health Analysis Skill | 宠物体态健康分析技能
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **宠物体态健康分析技能** |
| 🎯 核心目标 | 宠物体态健康分析技能，识别肥胖、消瘦、外伤、皮肤异常、精神状态异常，帮助宠物主人及时发现宠物健康问题 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `PET_BODY_HEALTH_ANALYSIS` |

Based on advanced computer vision and behavior analysis technologies, this feature conducts multi-dimensional
intelligent monitoring of pets' body posture, skin condition, and mental state. The system precisely identifies body
changes such as obesity and emaciation, automatically detects skin abnormalities like trauma, swelling, and hair loss,
and analyzes activity levels and behavioral patterns to determine if the mental state is abnormal. This feature helps
pet owners break through the barriers of professional knowledge, promptly identify potential health risks, and provide
reliable data support for scientific pet ownership and early intervention.

本功能基于先进的计算机视觉与行为分析技术，对宠物的体态特征、皮肤状况及精神面貌进行多维度智能监测。系统能够精准识别肥胖与消瘦等体态变化，自动检测外伤、红肿、脱毛等皮肤异常，并通过对活动量与行为模式的分析判断精神状态是否异常。这一功能帮助宠物主人突破专业知识的壁垒，及时发现潜在的健康风险，为科学养宠与早期干预提供可靠的数据支持

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals

### 1. 🧩 技能用途

通过视频/图片对宠物进行体态健康分析，识别常见体态异常和健康问题，输出结构化的宠物体态健康分析报告

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 根据技能场景执行图片/视频分析、结构化结果生成与报告输出 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供宠物视频/图片 URL 或文件需要进行宠物体态健康分析时，默认触发本技能 |
| 🔎 明确分析意图 | 当用户明确需要进行宠物体态分析，提及肥胖、消瘦、皮肤异常、外伤检查、体态健康等关键词，并且上传了视频或图片 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史分析报告、宠物体态分析报告清单、分析报告列表、查询历史报告、显示所有体态分析报告、宠物体态健康分析历史记录 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.pet_body_health_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.pet_body_health_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 3 | ⚙️ 执行宠物体态健康分析 | 调用 `-m scripts.pet_body_health_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地视频/图片文件路径 | 适用于本地文件分析 |
| `--url` | 网络视频/图片 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--media-type` | 媒体类型，可选值：video/image，默认 video | 按需填写 |
| `--list` | 显示宠物体态健康分析历史报告列表清单 | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/pet_body_health_analysis.py`](scripts/pet_body_health_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 支持格式：视频支持 mp4/avi/mov 格式，图片支持 jpg/png/jpeg 格式，最大 10MB |
| 🧑‍⚖️ 结果性质 | 分析结果仅供健康参考，不能替代专业兽医诊断，发现异常请及时就医 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
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
# 分析本地宠物视频
python -m scripts.pet_body_health_analysis --input /path/to/pet_video.mp4 --media-type video

# 分析宠物照片
python -m scripts.pet_body_health_analysis --input /path/to/pet.jpg --media-type image

# 显示历史分析报告/显示分析报告清单列表/显示历史宠物体态报告（自动触发关键词：查看历史分析报告、历史报告、分析报告清单等）
python -m scripts.pet_body_health_analysis --list

# 输出精简报告
python -m scripts.pet_body_health_analysis --input pet_video.mp4 --media-type video --detail basic

# 保存结果到文件
python -m scripts.pet_body_health_analysis --input pet.jpg --media-type image --output result.json
```
