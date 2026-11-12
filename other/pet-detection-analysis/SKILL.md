---
name: "pet-detection-analysis"
description: "Detects cats, dogs, and birds appearing in the target area; supports video stream and image detection, suitable for home pet monitoring scenarios. | 宠物检测技能，检测出目标区域内出现的猫、狗、鸟，支持视频流和图片检测，适用于家庭宠物监控场景"
version: "1.0.23"
---

# 🐾 Pet Detection Skill | 宠物检测技能
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **宠物检测技能** |
| 🎯 核心目标 | 宠物检测技能，检测出目标区域内出现的猫、狗、鸟，支持视频流和图片检测，适用于家庭宠物监控场景 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `PET_DETECTION` |

Tailored specifically for home pet monitoring scenarios, this feature is equipped with a high-sensitivity multi-species
recognition algorithm capable of precisely locking onto and distinguishing cats, dogs, and birds within the target area.
The system boasts robust adaptability across all scenarios, perfectly supporting both real-time video stream analysis
and static image detection. Whether monitoring dynamic daily activities or capturing static moments, it delivers
millisecond-level response times and high-precision identification. This technology breaks through the limitations of
single-species recognition, providing a comprehensive and flexible intelligent monitoring solution for multi-pet
households, ensuring that every movement of your pets within the home environment is accurately recorded and perceived.

本功能专为家庭宠物监控场景量身打造，搭载了高灵敏度的多物种识别算法，能够精准锁定并区分目标区域内的猫、狗及鸟类。系统具备强大的全场景适配能力，完美兼容实时视频流分析与静态图片检测，无论是动态的日常活动看护还是静态的画面捕捉，均能实现毫秒级响应与高精度判定。这一技术打破了单一物种识别的局限，为多宠家庭提供了全面、灵活的智能监测方案，确保宠物在家庭环境中的每一次活动都能被精准记录与感知。

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals

### 1. 🧩 技能用途

通过视频/图片对目标区域进行宠物检测，识别猫、狗、鸟等常见宠物，输出结构化的宠物检测报告

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 宠物分类定位 |
| 2 | 宠物数量统计 |
| 3 | 存在性检测 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供监控视频/图片 URL 或文件需要进行宠物检测时，默认触发本技能 |
| 🔎 明确分析意图 | 当用户明确需要进行宠物检测，提及宠物检测、猫咪检测、狗狗检测等关键词，并且上传了视频或图片 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史检测报告、宠物检测报告清单、检测报告列表、查询历史报告、显示所有检测报告、宠物检测历史记录，查询宠物检测分析报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.pet_detection_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.pet_detection_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 3 | ⚙️ 执行宠物检测 | 调用 `-m scripts.pet_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地视频/图片文件路径 | 适用于本地文件分析 |
| `--url` | 网络视频/图片 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--media-type` | 媒体类型，可选值：video/image，默认 video | 按需填写 |
| `--confidence-threshold` | 置信度阈值，低于该分值不输出，默认 0.5 | 按需填写 |
| `--list` | 显示宠物检测历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/pet_detection_analysis.py`](scripts/pet_detection_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 支持格式：视频支持 mp4/avi/mov 格式，图片支持 jpg/png/jpeg 格式，最大 10MB |
| 🧑‍⚖️ 结果性质 | 分析结果仅供家庭宠物监控参考，具体处置请结合实际情况 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📁 格式支持 | 当显示历史检测报告清单的时候，从数据 json 中提取字段  作为超链接地址，使用 Markdown 表格格式输出，包含" |
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
# 检测本地监控视频
python -m scripts.pet_detection_analysis --input /path/to/monitor.mp4 --media-type video

# 检测现场图片，调整置信度阈值
python -m scripts.pet_detection_analysis --input /path/to/room.jpg --media-type image --confidence-threshold 0.6

# 检测网络监控视频
python -m scripts.pet_detection_analysis --url https://example.com/monitor.mp4 --media-type video

# 显示历史检测报告/显示检测报告清单列表/显示历史宠物检测报告（自动触发关键词：查看历史检测报告、历史报告、检测报告清单等）
python -m scripts.pet_detection_analysis --list

# 输出精简报告
python -m scripts.pet_detection_analysis --input video.mp4 --media-type video --detail basic

# 保存结果到文件
python -m scripts.pet_detection_analysis --input video.mp4 --media-type video --output result.json
```
