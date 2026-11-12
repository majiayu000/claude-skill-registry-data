---
name: "smyx-sleep-quality-analysis-analysis"
description: "AI-powered pet sleep quality analysis from a fixed bed/rest-area camera. Uses motion detection and pose recognition to distinguish sleeping vs. awake states, accumulates total sleep duration, counts roll-overs / position changes and startle-awakenings, and outputs a 0-100 sleep-quality score. Helps owners spot potential pain, anxiety, or disease early. Scenarios: home nighttime monitoring, senior pet health management, animal hospital wards, pet boarding centers. | 通过宠物窝或休息区固定摄像头，在夜间（或宠物主要睡眠时段）持续分析视频，利用运动检测和姿态识别技术判断宠物处于静止（睡眠）或活动（觉醒）状态，累计睡眠总时长，并统计翻身次数、惊醒频次，输出睡眠质量评分（0-100分），帮助主人了解宠物的睡眠健康，识别潜在的疼痛、焦虑或疾病。应用场景：宠物家庭夜间监护、老年宠物健康管理、宠物医院住院观察、寄养中心。"
version: "1.0.24"
---

# 😴 Pet Sleep Quality Analysis (Duration / Roll Count) | 宠物睡眠质量分析（时长/翻滚次数）
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **宠物睡眠质量分析（时长/翻滚次数）** |
| 🎯 核心目标 | 通过宠物窝或休息区固定摄像头，在夜间（或宠物主要睡眠时段）持续分析视频，利用运动检测和姿态识别技术判断宠物处于静止（睡眠）或活动（觉醒）状态，累计睡眠总时长，并统计翻身次数、惊醒频次，输出睡眠质量评分（0-100分），帮助主人了解宠物的睡眠健康，识别潜在的疼痛、焦虑或疾病。应用场景：宠物家庭夜间监护、老年宠物健康管理、宠物医院住院观察、寄养中心。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_SLEEP_QUALITY_ANALYSIS_ANALYSIS` |

AI-powered pet sleep quality analysis from a fixed bed/rest-area camera. Uses motion detection and pose recognition to distinguish sleeping vs. awake states, accumulates total sleep duration, counts roll-overs / position changes and startle-awakenings, and outputs a 0-100 sleep-quality score. Helps owners spot potential pain, anxiety, or disease early. Scenarios: home nighttime monitoring, senior pet health management, animal hospital wards, pet boarding centers.

通过宠物窝或休息区固定摄像头，在夜间（或宠物主要睡眠时段）持续分析视频，利用运动检测和姿态识别技术判断宠物处于静止（睡眠）或活动（觉醒）状态，累计睡眠总时长，并统计翻身次数、惊醒频次，输出睡眠质量评分（0-100分），帮助主人了解宠物的睡眠健康，识别潜在的疼痛、焦虑或疾病。应用场景：宠物家庭夜间监护、老年宠物健康管理、宠物医院住院观察、寄养中心。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的宠物睡眠健康AI。你的任务是分析宠物窝/休息区固定摄像头的夜间视频，检测宠物的活动状态，统计睡眠总时长、翻身次数、惊醒频次，并输出睡眠质量评分。不要提供医疗诊断，仅输出基于视觉的睡眠指标。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

通过夜间或主要睡眠时段视频进行宠物睡眠质量评估，输出睡眠总时长、翻身次数、惊醒频次和综合评分

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 睡眠/觉醒状态识别 |
| 2 | 睡眠总时长累计 |
| 3 | 翻身/姿势变换次数统计 |
| 4 | 惊醒事件检测 |
| 5 | 深睡/浅睡时段划分 |
| 6 | 睡眠质量综合评分（0-100） |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供宠物窝/休息区夜间视频需要分析时，默认触发本技能进行睡眠质量分析 |
| 🔎 明确分析意图 | 当用户明确需要睡眠监测时，提及睡眠质量、翻身、惊醒、夜间监测、宠物失眠、老年宠物睡眠等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史睡眠报告、历史睡眠质量报告、睡眠报告清单、显示所有睡眠报告、查询睡眠记录 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_sleep_quality_analysis_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_sleep_quality_analysis_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行睡眠质量分析 | 调用 `-m scripts.smyx_sleep_quality_analysis_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地宠物窝夜间视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络宠物窝夜间视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 宠物类型，可选值：cat/dog/other，默认 cat | 按需填写 |
| `--list` | 显示睡眠质量分析历史报告列表清单 | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 😴 睡眠指标参考范围

| 指标 | 成猫正常范围 | 成犬正常范围 | 异常预警 |
|------|--------------|--------------|----------|
| 总睡眠时长（24h） | 12-16 小时 | 12-14 小时 | <8 或 >20 小时 |
| 夜间睡眠时长（8h） | 5-7 小时 | 6-8 小时 | <4 小时 |
| 翻身次数（夜间） | 3-8 次 | 5-12 次 | >15 次（夜间） |
| 惊醒次数（夜间） | 0-3 次 | 0-3 次 | >5 次 |
| 深睡占比 | 25%-40% | 20%-35% | <15% |

> 数据仅供算法基线参考；幼宠和老年宠物睡眠时长更长（可达 18-20 小时），属正常。

## 📊 睡眠质量评分体系

| 评分区间 | 睡眠质量 | 说明 |
|----------|----------|------|
| 90-100 | 🌟 优秀 | 睡眠充足、深睡占比高、翻身惊醒少 |
| 75-89 | ✅ 良好 | 整体睡眠质量较好，偶有轻度翻身 |
| 60-74 | ⚠️ 一般 | 翻身或惊醒偏多，建议关注环境与健康 |
| 40-59 | 🟠 较差 | 睡眠片段化明显，可能有焦虑或不适 |
| 0-39 | 🔴 极差 | 睡眠严重异常，建议就医检查 |

## 🚨 异常翻身/惊醒可能提示

| 异常表现 | 可能原因 |
|----------|----------|
| 🦴 频繁翻身 + 关节部位活动 | 关节炎、髋关节发育不良、肌肉酸痛 |
| 🐛 频繁翻身 + 抓挠/舔毛 | 皮肤瘙痒、寄生虫、过敏 |
| 😰 频繁惊醒 + 起身张望 | 焦虑、噪音敏感、认知功能障碍 |
| 🌡️ 频繁变换睡姿 | 环境温度不适（过冷/过热） |
| 💤 睡眠时长骤减 | 疼痛、消化不良、应激事件 |
| 😴 睡眠时长骤增 | 嗜睡、代谢性疾病、低血糖 |

## 💡 高风险群体重点关注

| 类别 | 重点关注原因 |
|------|--------------|
| 老年宠物（>7岁） | 关节炎、认知功能障碍（CDS）高发，睡眠常异常 |
| 大型犬 | 髋关节发育不良易致翻身困难 |
| 短鼻品种 | 睡眠呼吸暂停风险，需观察呼吸节律 |
| 既往焦虑史 | 易频繁惊醒 |
| 术后/疾病恢复期 | 睡眠质量是康复重要指标 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_sleep_quality_analysis_analysis.py`](scripts/smyx_sleep_quality_analysis_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 视频要求：支持 mp4/avi/mov 格式，最大 10MB；建议时长 ≥ 1 小时，最佳为整夜 |
| 🔎 使用提醒 | 夜间拍摄需开启**红外/夜视模式**，确保黑暗环境下可见宠物姿态 |
| 🔎 使用提醒 | 摄像头需固定，视角完整覆盖宠物休息区域 |
| 🧑‍⚖️ 结果性质 | **分析结果仅供睡眠健康参考，不提供医疗诊断**；持续异常建议及时就医 |
| 🔎 使用提醒 | 老年宠物和幼宠的正常睡眠时长普遍更长，请结合个体年龄判断 |
| 🔎 使用提醒 | 不建议使用宠物活动期作为分析时段，重点应在主要睡眠时段 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地夜间睡眠视频
python -m scripts.smyx_sleep_quality_analysis_analysis --input /path/to/night_sleep.mp4 --pet-type cat

# 分析网络夜间睡眠视频
python -m scripts.smyx_sleep_quality_analysis_analysis --url https://example.com/night_sleep.mp4 --pet-type dog

# 显示历史分析报告/显示报告清单列表
python -m scripts.smyx_sleep_quality_analysis_analysis --list

# 输出精简报告
python -m scripts.smyx_sleep_quality_analysis_analysis --input video.mp4 --pet-type cat --detail basic

# 保存结果到文件
python -m scripts.smyx_sleep_quality_analysis_analysis --input video.mp4 --pet-type cat --output result.json
```
