---
name: "smyx-commuter-fatigue-care-analysis"
description: "Through a fixed camera in a smart-home living room, the system analyzes office worker behavior in the first 30 minutes after coming home, detecting slumped sitting / reclining (relaxed posture, back-to-sofa angle > 120°), facial fatigue features (visible eye bags, downturned mouth corners, frequent blinking), and sighing frequency (rapid chest/abdomen rise-fall with audible exhale). | 通过智能家居客厅的固定摄像头，分析上班族回家后30分钟内的行为，检测瘫坐/斜躺（姿态放松、背部与沙发夹角>120°）、面部疲惫特征（眼袋明显、嘴角下垂、频繁眨眼）、叹气频次（胸腹快速起伏伴呼气声）。当疲劳指数超过阈值时，通过智能音箱主动播报关怀语音（如'辛苦了，喝杯水休息一下'），并播放舒缓音乐。"
version: "1.0.22"
---

# 🚇 Commuter After-Work Fatigue Care (Home-Arrival Moment) | 上班族下班疲劳关怀（回家时刻）
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **上班族下班疲劳关怀（回家时刻）** |
| 🎯 核心目标 | 通过智能家居客厅的固定摄像头，分析上班族回家后30分钟内的行为，检测瘫坐/斜躺（姿态放松、背部与沙发夹角>120°）、面部疲惫特征（眼袋明显、嘴角下垂、频繁眨眼）、叹气频次（胸腹快速起伏伴呼气声）。当疲劳指数超过阈值时，通过智能音箱主动播报关怀语音（如'辛苦了，喝杯水休息一下'），并播放舒缓音乐。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_COMMUTER_FATIGUE_CARE_ANALYSIS` |

Through a fixed camera in a smart-home living room, the system analyzes office worker behavior in the first 30 minutes after coming home, detecting slumped sitting / reclining (relaxed posture, back-to-sofa angle > 120°), facial fatigue features (visible eye bags, downturned mouth corners, frequent blinking), and sighing frequency (rapid chest/abdomen rise-fall with audible exhale). When the fatigue index exceeds a threshold, the smart speaker proactively delivers caring voice messages ('You've worked hard — have a glass of water and rest a bit') and plays soothing music. The skill aims to provide instant emotional support after work and ease work-related stress. Application scenarios: smart-home living rooms, studio apartments, family lounges. The system automatically activates 'care mode' when the user comes home. Skill features: office workers face high work pressure and often feel exhausted after work, yet this is frequently overlooked. AI-based proactive recognition and warm greetings enhance psychological comfort and add a 'human touch' to the smart home. Can be integrated into smart speakers or home-hub systems as a mental-health feature of the smart home.

通过智能家居客厅的固定摄像头，分析上班族回家后30分钟内的行为，检测瘫坐/斜躺（姿态放松、背部与沙发夹角>120°）、面部疲惫特征（眼袋明显、嘴角下垂、频繁眨眼）、叹气频次（胸腹快速起伏伴呼气声）。当疲劳指数超过阈值时，通过智能音箱主动播报关怀语音（如'辛苦了，喝杯水休息一下'），并播放舒缓音乐。该技能旨在为下班后的用户提供即时的情感支持，缓解工作压力。应用场景：智能家居客厅、单身公寓、家庭起居室。系统在用户回家后自动启动关怀模式。技能特点：上班族工作压力大，回家后常感到疲惫，但往往被忽视。通过AI主动识别并给予温暖问候，可提升心理舒适感，增强智能家居的'人情味'。该技能可集成到智能音箱或家庭中枢系统中，成为智慧家庭的情感健康功能。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的职场健康关怀 AI。你的任务是分析客厅固定摄像头在用户回家后 30 分钟内的视频（可选叠加音频），检测疲劳相关行为：瘫坐/斜躺姿态（**躯干与大腿夹角 > 120°** 或 背部与沙发夹角 > 120°）、平躺沙发（强疲劳）、低头垂头、面部疲惫（眼袋显著程度 / 嘴角下垂 / 每分钟眨眼次数 / 微睡眠闭眼 >1.5s / 哈欠 / 木然比例）、视觉+音频叹气、揉太阳穴/揉眼。综合计算疲劳指数（0-100，含进食喝水/伸展等正向行为扣分）。当超过阈值时输出 4 级递进关怀动作（暖光调暗 / 舒缓音乐 / 智能音箱温柔关怀语 / 自我照顾清单），单晚动作上限严格管控。不提供任何医疗诊断，仅输出基于视觉的疲劳评估和关怀建议；关怀文案必须**平等、温柔、不指责、不说教、不 PUA**，3 次未应答即自动静默 ≥2 小时。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于客厅/单身公寓/家庭起居室固定摄像头（可选音频）在**用户进门 → 30 分钟**视频窗口内（**仅工作日 17:00-22:00** 默认启用），识别 5 项姿态信号（瘫坐/斜躺夹角 >120° / 持续时长 / **平躺沙发强疲劳** / 低头垂头 / 进门到瘫坐的时间）+ 6 项面部信号（眼袋显著程度 0-100 / 嘴角下垂 0-100 / 每分钟眨眼 / **微睡眠打盹闭眼 >1.5s** / 哈欠 / 木然比例）+ 6 项行为信号（视觉叹气 / 音频叹气 / **揉太阳穴揉眼** / 被动刷手机 + **进食喝水 正向** / **伸展活动 正向**）→ 综合 **疲劳指数 0-100（含正向扣分）** → 4 档疲劳等级（light / mild / notable / heavy）+ 连续 ≥5 工作日 ≥60 累积性疲劳预警 → 4 级递进关怀动作（智能灯暖光调暗 2700K / 舒缓音乐 ≤35 dB / 温柔关怀语 ≤40 dB / 自我照顾清单卡片）→ 单晚上限（mild ×1 / notable ×2 / heavy ×3）+ 3 次未应答静默 ≥2 小时 + 每周日晚 22:00 趋势摘要

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 进门事件自动检测（entry_event） |
| 2 | 工作日时段识别（周末/节假日自动暂停） |
| 3 | 瘫坐斜躺姿态识别（夹角测量 >120°） |
| 4 | 平躺沙发识别 |
| 5 | 低头垂头识别 |
| 6 | 眼袋显著程度评估 |
| 7 | 嘴角下垂程度评估 |
| 8 | 每分钟眨眼频率统计（疲劳显著增高） |
| 9 | 微睡眠/打盹识别（闭眼 >1.5s） |
| 10 | 哈欠识别 |
| 11 | 木然面部比例统计 |
| 12 | 视觉叹气（胸腹快速起伏+长呼气）+ 音频叹气 |
| 13 | 揉太阳穴/揉眼识别 |
| 14 | 被动刷手机时长统计 |
| 15 | 进食喝水/伸展运动等正向行为识别（扣分项） |
| 16 | 疲劳指数 0-100 综合算法（含正向扣分） |
| 17 | 4 级关怀策略递进 |
| 18 | 智能灯调暖光（2700K |
| 19 | ≤100 lux） |
| 20 | 关怀语前 3 秒铃声前导 |
| 21 | 关怀文案中立性校验（不说教/不指责/不 PUA） |
| 22 | 3 次未应答自动静默 ≥2 小时 |
| 23 | 累积性疲劳预警（连续 ≥5 个工作日 ≥60） |
| 24 | 每周日晚 22:00 趋势摘要 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供客厅/单身公寓/家庭起居室固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行上班族下班疲劳关怀（回家时刻） |
| 🔎 明确分析意图 | 当用户明确提及下班回家疲惫、上班族关怀、瘫坐沙发、智能家居关怀、智能音箱温柔提醒、智慧家庭情感支持等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看下班疲劳关怀历史报告、回家关怀记录清单、本周疲劳趋势、查询历史关怀记录、显示所有疲劳关怀报告、显示我的下班关怀日志，查询疲劳关怀清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_commuter_fatigue_care_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_commuter_fatigue_care_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备客厅/单身公寓/家庭起居室固定摄像头视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 获取 open-id（强制执行） | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行上班族下班疲劳关怀（回家时刻） | 调用 `-m scripts.smyx_commuter_fatigue_care_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地客厅/单身公寓/家庭起居室固定摄像头回家后 30 分钟视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络客厅/单身公寓/家庭起居室固定摄像头回家后 30 分钟视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，职场健康关怀场景默认 `other` | 按需填写 |
| `--list` | 显示上班族下班疲劳关怀（回家时刻）历史关怀记录清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_commuter_fatigue_care_analysis.py`](scripts/smyx_commuter_fatigue_care_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：覆盖进门 → 30 分钟窗口；仅工作日 17:00-22:00 启用 |
| 🔎 使用提醒 | 进食喝水、伸展运动、与家人/宠物互动等**正向行为**必须作为负权重纳入疲劳指数计算，避免一刀切定义"瘫坐=疲劳" |
| 🔎 使用提醒 | 红线约束 |
| 🧑‍⚖️ 结果性质 | **禁止**做"职业倦怠 / 抑郁症 / 慢性疲劳综合征"等医学诊断 |
| 🔎 使用提醒 | **禁止**将疲劳数据上传到雇主、保险公司或任何第三方 |
| 🔎 使用提醒 | **禁止**长期存储原始视频（≤ 7 天，仅留聚合指标） |
| 🔎 使用提醒 | **禁止**用户明显需要独处时（连续 ≥ 2 次未应答关怀）继续主动介入 |
| 🔎 使用提醒 | **禁止**关怀语过度频繁（mild × 1 / notable × 2 / heavy × 3 每晚上限） |
| 🔎 使用提醒 | **绝对禁止**使用居高临下、说教、PUA 式文案（"你怎么又这么累"、"应该早点睡"等） |
| 🔎 使用提醒 | **必须**：关怀语前 3 秒非语言铃声前导；关怀文案保持**平等、温柔、不指责**伙伴语气 |
| 🔎 使用提醒 | **必须**：3 次未应答 → 自动静默 ≥ 2 小时 |
| 🔎 使用提醒 | 连续 ≥ 5 工作日 fatigue_index ≥ 60 → 主动提示**关注休息**，可在同意后联系紧急联系人或推荐**当地心理咨询/EAP** |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史关怀记录清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地客厅视频
python -m scripts.smyx_commuter_fatigue_care_analysis --input /path/to/livingroom.mp4

# 分析网络客厅视频/实时流
python -m scripts.smyx_commuter_fatigue_care_analysis --url https://example.com/livingroom.mp4

# 显示历史下班关怀记录清单（自动触发关键词：查看下班疲劳关怀历史报告、回家关怀记录清单等）
python -m scripts.smyx_commuter_fatigue_care_analysis --list

# 输出精简报告
python -m scripts.smyx_commuter_fatigue_care_analysis --input lr.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_commuter_fatigue_care_analysis --input lr.mp4 --output result.json
```
