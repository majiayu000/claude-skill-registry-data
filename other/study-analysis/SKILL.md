---
name: "study-analysis"
description: "Conducts video analysis of learning behavior for children/students, identifies poor learning habits, provides structured analysis reports and family education improvement suggestions, focusing on learning habit cultivation and behavior correction. | A comprehensive tool designed to analyze video footage of children's and students' learning behaviors. It identifies poor study habits and provides structured analysis reports along with actionable suggestions for family education improvements. The tool is dedicated to fostering positive study habits and facilitating behavioral correction. | 分析孩子学习行为 孩子学习行为分析工具，针对孩子/学生的学习行为进行视频分析，识别不良学习习惯，提供结构化分析报告和家庭教育改善建议，专注学习习惯培养和行为矫正"
version: "1.0.25"
---

# 📚 Child Learning Behavior Analysis Tool | 孩子学习行为分析工具
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **孩子学习行为分析工具** |
| 🎯 核心目标 | A comprehensive tool designed to analyze video footage of children's and students' learning behaviors. It identifies poor study habits and provides structured analysis reports along with actionable suggestions for family education improvements. The tool is dedicated to fostering positive study habits and facilitating behavioral correction. | 分析孩子学习行为 孩子学习行为分析工具，针对孩子/学生的学习行为进行视频分析，识别不良学习习惯，提供结构化分析报告和家庭教育改善建议，专注学习习惯培养和行为矫正 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `STUDY_ANALYSIS` |

Based on advanced computer vision and behavior recognition algorithms, this feature is specifically designed for
analyzing the learning behaviors of children and students. The system utilizes cameras to capture key behaviors during
study sessions, such as posture, concentration levels, and fidgeting, accurately identifying poor learning habits like
slumping, frequent distraction, and incorrect pen-holding. Combined with time-series analysis, the system generates
structured analysis reports containing concentration curves, behavior frequency statistics, and risk levels. Grounded in
educational psychology principles, it provides parents with personalized suggestions for improving home education—such
as environment optimization and time management techniques—helping children cultivate good study habits and achieve
behavioral correction alongside improved learning efficiency.

本功能基于先进的计算机视觉与行为识别算法，专为孩子及学生的学习行为分析设计。系统通过摄像头捕捉学习过程中的坐姿、专注度、小动作等关键行为，精准识别不良学习习惯（如趴桌、频繁分心、握笔姿势错误等）。结合时间序列分析，系统可生成包含专注度曲线、行为频次统计及风险等级的结构化分析报告，并基于教育心理学原理，为家长提供个性化的家庭教育改善建议（如环境优化、时间管理技巧），助力孩子养成良好学习习惯，实现行为矫正与学习效率提升

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals

### 1. 🧩 技能用途

通过视频分析对孩子/学生的学习行为进行评估，识别不良学习习惯，发现潜在学习问题，提供结构化分析报告和家庭教育改善建议

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 视频行为分析 |
| 2 | 专注度评估 |
| 3 | 坐姿姿势评估 |
| 4 | 学习习惯识别 |
| 5 | 不良行为检测 |
| 6 | 家庭教育建议生成 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供需要分析的孩子学习视频 URL 或文件需要进行学习行为分析时，默认触发本技能 |
| 🔎 明确分析意图 | 当用户明确需要进行孩子学习行为分析、学习习惯评估、作业行为检查时，提及学习行为、学习习惯、孩子作业、坐姿矫正、分心走神等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史学习报告、学习分析报告清单、学习行为分析列表、显示所有学习分析报告，查询学习行为分析报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.study_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.study_analysis --list` 调用 API 查询云端的历史报告数据 |
| 🚫 严格禁止 | 从本地 `memory` 目录读取历史会话信息 |
| 🚫 严格禁止 | 手动汇总本地记录中的报告 |
| 🚫 严格禁止 | 从长期记忆中提取报告 |
| ✅ 输出格式 | 必须统一从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果 |

## 📦 前置准备 | Requirements
- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 📚 学习行为分析维度 | Learning Behavior Dimensions
| 维度/类型 | 说明 |
|---|---|
| 高度专注 | 持续关注学习内容，很少分心 |
| 中度分心 | 偶尔走神、看手机、东张西望 |
| 严重分心 | 频繁走神，难以保持注意力在学习上 |
| 坐姿端正 | 腰背挺直，距离书本屏幕合适 |
| 弯腰驼背 | 坐姿不正，弯腰趴在桌上 |
| 歪头斜肩 | 长期歪头写字，可能影响脊柱发育 |
| 距离不当 | 眼睛离书本/屏幕太近 |
| 磨蹭拖延 | 开始作业耗时过长，频繁停顿 |
| 边玩边学 | 同时玩手机/看电视/吃东西 |
| 主动思考 | 主动阅读思考，尝试解题 |
| 依赖帮助 | 一遇到问题就问，不独立思考 |
| 分心走神 | 频繁被外界干扰吸引注意力 |
| 小动作过多 | 转笔、玩橡皮、抖腿等频繁小动作 |
| 抄作业舞弊 | 偷看参考答案、抄袭他人作业 |
| 超时学习 | 连续学习过长时间不休息 |

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
| 1 | 📥 准备视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行学习行为分析 | 调用 `-m scripts.study_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--analysis-type` | 分析类型，可选值：comprehensive/focus/posture/habit/risk，默认 comprehensive（综合分析） | 按需填写 |
| `--list` | 显示学习行为分析历史报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/study_analysis.py`](scripts/study_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 🧑‍⚖️ 结果性质 | **重要声明**：本分析仅供家庭教育参考，不能替代专业老师或心理咨询师诊断。发现严重学习困难建议及时寻求专业帮助 |
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 视频要求：支持 mp4/avi/mov 格式，最大 10MB |
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
# 综合学习行为分析
python -m scripts.study_analysis --input /path/to/homework_video.mp4 --analysis-type comprehensive

# 专注度专项分析
python -m scripts.study_analysis --url https://example.com/study_video.mp4 --analysis-type focus

# 坐姿姿势专项分析
python -m scripts.study_analysis --input /path/to/writing_video.mp4 --analysis-type posture

# 显示历史分析报告/显示分析报告清单列表/显示历史学习报告（自动触发关键词：查看历史学习报告、历史报告、学习报告清单等）
python -m scripts.study_analysis --list

# 输出精简报告
python -m scripts.study_analysis --input video.mp4 --analysis-type comprehensive --detail basic

# 保存结果到文件
python -m scripts.study_analysis --input video.mp4 --analysis-type comprehensive --output result.json
```
