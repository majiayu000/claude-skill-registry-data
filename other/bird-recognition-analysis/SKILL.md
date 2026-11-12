---
name: "bird-recognition-analysis"
description: "Identifies bird species in images/videos of target areas. Supports recognition of no less than 500 common bird species, supports customized model training, suitable for ecological observation, garden bird watching and other scenarios. | 鸟类识别工具，识别目标区域图片/视频中的鸟类种类，支持不低于500种常见鸟类识别，支持定制化模型训练，适用于生态观测、庭院观鸟等场景"
version: "1.0.23"
---

# 🐦 Bird Recognition Tool | 鸟类识别工具

> **智能健康/识别分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **鸟类识别工具** |
| 🎯 核心目标 | 鸟类识别工具，识别目标区域图片/视频中的鸟类种类，支持不低于500种常见鸟类识别，支持定制化模型训练，适用于生态观测、庭院观鸟等场景 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、风险/识别结果、建议与报告链接 |
| 🧩 场景码 | `BIRD_RECOGNITION` |

This capability supports automatic bird identification in images or video streams, covering over 500 common species and
capable of distinguishing between similar species and subspecies. Powered by deep learning visual models, the system can
be deployed in ecological observation stations, nature reserves, or home backyards to enable real-time monitoring and
recording of bird species. It also supports customized model training to optimize recognition performance based on
specific regional or species requirements, providing intelligent assistance for bird diversity surveys, birdwatching
hobbies, and ecological conservation.

本技能支持对图片或视频流中的鸟类进行自动识别，覆盖不低于500种常见鸟类，可区分相似种与亚种。系统基于深度学习视觉模型，可部署于生态观测站、自然保护区或家庭庭院等场景，实现鸟种实时监测与记录。同时支持定制化模型训练，根据特定区域或物种需求优化识别效果，为鸟类多样性调查、观鸟爱好及生态保护提供智能辅助。

## 🎬 技能演示 | Skill Demo
[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

## 🎯 任务目标 | Goals

### 1. 🧩 技能用途

识别图片/视频中出现的鸟类，准确判定鸟类品种

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 鸟类检测 |
| 2 | 品种分类 |
| 3 | 置信度评定 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供图片/视频需要识别鸟类品种时，默认触发本技能 |
| 🔎 明确分析意图 | 当用户明确需要鸟类识别、鸟种类鉴定时，提及观鸟、鸟类识别、鸟种类识别等关键词，并且上传了图片/视频 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史识别报告、鸟类识别报告清单、识别报告列表、查询历史识别报告、显示所有识别报告、鸟类分析报告，查询鸟类识别分析报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.bird_recognition_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.bird_recognition_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 要求 | 如果是视频，建议截取鸟类清晰停留的片段上传 |

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
| 1 | 📥 准备鸟类图片/视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行鸟类识别分析 | 调用 `-m scripts.bird_recognition_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地图片/视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络图片/视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--list` | 显示历史鸟类识别分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/bird_recognition_analysis.py`](scripts/bird_recognition_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 支持格式：jpg/jpeg/png/mp4/avi/mov，最大 10MB |
| 🧑‍⚖️ 结果性质 | 识别结果仅供自然观察参考，物种保护请遵循当地法律法规 |
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
# 识别本地鸟类图片
python -m scripts.bird_recognition_analysis --input /path/to/bird.jpg

# 识别本地视频
python -m scripts.bird_recognition_analysis --input /path/to/forest.mp4

# 识别网络图片
python -m scripts.bird_recognition_analysis --url https://example.com/bird.jpg

# 显示历史识别报告/显示识别报告清单列表/显示历史鸟类识别（自动触发关键词：查看历史识别报告、历史报告、识别报告清单等）
python -m scripts.bird_recognition_analysis --list

# 输出精简报告
python -m scripts.bird_recognition_analysis --input bird.jpg --detail basic

# 保存结果到文件
python -m scripts.bird_recognition_analysis --input bird.jpg --output result.json
```
