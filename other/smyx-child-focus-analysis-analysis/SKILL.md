---
name: "smyx-child-focus-analysis-analysis"
description: "Using the camera built into a smart desk lamp or a tabletop camera, the system analyzes video of the child's study area in real time, detecting behavioral indicators such as face orientation (whether it deviates from the book/screen), eye gaze direction, and fidgeting hand actions (playing with a pen, touching the face, fiddling with objects), and computes a per-minute focus score (0-100) while recording distraction periods. The skill helps parents and teachers understand the child's learning state and optimize study habits. Application scenarios: smart study lamps, home study rooms, classrooms. The system monitors in real time, generates focus reports, and pushes alerts when focus stays persistently low. Skill features: improve learning efficiency. | 通过智能台灯内置摄像头或桌面摄像头，实时分析儿童学习区域的视频，检测面部朝向（是否偏离书本/屏幕）、眼部注视方向、手部小动作（玩笔、摸脸、摆弄物品）等行为指标，计算每分钟专注得分（0-100分），并记录走神时段。该技能可帮助家长和教师了解儿童学习状态，优化学习习惯。应用场景：智能学习台灯、家庭书房、教室。系统实时监测，生成专注度报告，当专注度持续偏低时推送提醒。技能特点：提升学习效率。"
version: "1.0.24"
---

# 🎯 Child Focus / Distraction Period Analysis | 儿童专注度与走神时段分析
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **儿童专注度与走神时段分析** |
| 🎯 核心目标 | 通过智能台灯内置摄像头或桌面摄像头，实时分析儿童学习区域的视频，检测面部朝向（是否偏离书本/屏幕）、眼部注视方向、手部小动作（玩笔、摸脸、摆弄物品）等行为指标，计算每分钟专注得分（0-100分），并记录走神时段。该技能可帮助家长和教师了解儿童学习状态，优化学习习惯。应用场景：智能学习台灯、家庭书房、教室。系统实时监测，生成专注度报告，当专注度持续偏低时推送提醒。技能特点：提升学习效率。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_CHILD_FOCUS_ANALYSIS_ANALYSIS` |

Using the camera built into a smart desk lamp or a tabletop camera, the system analyzes video of the child's study area in real time, detecting behavioral indicators such as face orientation (whether it deviates from the book/screen), eye gaze direction, and fidgeting hand actions (playing with a pen, touching the face, fiddling with objects), and computes a per-minute focus score (0-100) while recording distraction periods. The skill helps parents and teachers understand the child's learning state and optimize study habits. Application scenarios: smart study lamps, home study rooms, classrooms. The system monitors in real time, generates focus reports, and pushes alerts when focus stays persistently low. Skill features: improve learning efficiency.

通过智能台灯内置摄像头或桌面摄像头，实时分析儿童学习区域的视频，检测面部朝向（是否偏离书本/屏幕）、眼部注视方向、手部小动作（玩笔、摸脸、摆弄物品）等行为指标，计算每分钟专注得分（0-100分），并记录走神时段。该技能可帮助家长和教师了解儿童学习状态，优化学习习惯。应用场景：智能学习台灯、家庭书房、教室。系统实时监测，生成专注度报告，当专注度持续偏低时推送提醒。技能特点：提升学习效率。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的儿童学习行为分析 AI。你的任务是分析桌面学习区域固定摄像头的实时视频，检测儿童的面部朝向、视线方向以及手部小动作，计算每分钟的专注得分。不要提供教学建议或学习方案，仅输出基于视觉的专注度指标与走神事件统计。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于智能台灯/桌面摄像头视频，量化儿童每分钟专注得分并标注走神时段，输出整体专注度等级

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 儿童面部检测 |
| 2 | 面部朝向估计（是否对准书本/屏幕） |
| 3 | 视线方向估计 |
| 4 | 手部小动作识别（玩笔 / 摸脸 / 摆弄物品 / 玩手机） |
| 5 | 离座事件检测 |
| 6 | 每分钟专注得分（0-100） |
| 7 | 走神事件类型分类（gaze_away / head_lift / hand_fidget / off_seat / phone_use） |
| 8 | 累计走神时长统计 |
| 9 | 整体等级判定（excellent / good / fair / poor） |
| 10 | 专注度持续偏低提醒 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供儿童学习区域监控视频 URL 或文件需要分析时，默认触发本技能进行专注度与走神时段分析 |
| 🔎 明确分析意图 | 当用户明确提及儿童专注度、走神、分心、注意力、学习状态、写作业、玩笔、摸脸、智能台灯监督等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看儿童专注度历史报告、专注度报告清单、走神时段报告清单、查询历史专注度记录、显示所有儿童专注度报告、显示学习状态诊断报告，查询走神事件清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_child_focus_analysis_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_child_focus_analysis_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备儿童学习区域监控视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行儿童专注度与走神时段分析 | 调用 `-m scripts.smyx_child_focus_analysis_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地儿童学习区域监控视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络儿童学习区域监控视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，儿童学习行为分析场景默认 `other` | 按需填写 |
| `--list` | 显示儿童专注度历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_child_focus_analysis_analysis.py`](scripts/smyx_child_focus_analysis_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov 视频，最大 10MB；建议正对面部 + 学习区域 |
| 🧑‍⚖️ 结果性质 | 专注度评分仅作为学习行为辅助参考，本工具不替代家长/教师的实际观察与教育判断 |
| 🔏 隐私合规 | 隐私合规：儿童学习场景视频涉及未成年人隐私，使用前需取得监护人知情同意，并妥善保管/加密相关录像 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地儿童学习区域视频
python -m scripts.smyx_child_focus_analysis_analysis --input /path/to/study.mp4

# 分析网络儿童学习区域视频
python -m scripts.smyx_child_focus_analysis_analysis --url https://example.com/study.mp4

# 显示历史专注度分析报告（自动触发关键词：查看儿童专注度历史报告、专注度报告清单等）
python -m scripts.smyx_child_focus_analysis_analysis --list

# 输出精简报告
python -m scripts.smyx_child_focus_analysis_analysis --input study.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_child_focus_analysis_analysis --input study.mp4 --output result.json
```
