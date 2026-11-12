---
name: "smyx-child-bedtime-soothing-analysis"
description: "Through a fixed camera (with infrared night vision) and microphone in the child's bedroom, the system analyzes pre-sleep and night-time video and audio to detect pre-sleep crying (continuous crying, calling 'Mama'), fear-of-the-dark expressions (curling up, looking around), and nightmare awakenings (sudden sitting up, trembling, screaming). | 通过儿童卧室的固定摄像头（红外夜视）及麦克风，分析儿童睡前及夜间视频，检测睡前哭闹（持续性哭声、呼喊'妈妈'）、怕黑表现（身体蜷缩、四处张望）、噩梦惊醒（突然坐起、颤抖、尖叫）等行为。当检测到上述情绪不安时，自动触发安抚动作：开启小夜灯（柔光）、播放预先录制的妈妈讲故事音频或轻柔摇篮曲。"
version: "1.0.22"
---

# 🌙 Child Bedtime Soothing (Fear of Dark / Post-Nightmare) | 儿童睡前情绪安抚（怕黑/噩梦后）
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **儿童睡前情绪安抚（怕黑/噩梦后）** |
| 🎯 核心目标 | 通过儿童卧室的固定摄像头（红外夜视）及麦克风，分析儿童睡前及夜间视频，检测睡前哭闹（持续性哭声、呼喊'妈妈'）、怕黑表现（身体蜷缩、四处张望）、噩梦惊醒（突然坐起、颤抖、尖叫）等行为。当检测到上述情绪不安时，自动触发安抚动作：开启小夜灯（柔光）、播放预先录制的妈妈讲故事音频或轻柔摇篮曲。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_CHILD_BEDTIME_SOOTHING_ANALYSIS` |

Through a fixed camera (with infrared night vision) and microphone in the child's bedroom, the system analyzes pre-sleep and night-time video and audio to detect pre-sleep crying (continuous crying, calling 'Mama'), fear-of-the-dark expressions (curling up, looking around), and nightmare awakenings (sudden sitting up, trembling, screaming). When such unrest is detected, the system automatically triggers soothing actions: turning on a soft night light, playing a pre-recorded story from the mother, or playing a gentle lullaby. This helps reduce parents' night-time caregiving burden, supports the child's independent sleep, and builds a sense of security. Application scenarios: children's bedrooms, nurseries. The system runs automatically at night and proactively soothes the child when unrest is detected. Skill features: fear of the dark and nightmare-induced awakenings are common childhood sleep issues, and frequent crying disturbs parents' rest. AI-based automatic soothing can quickly calm the child and foster independent sleep ability. Can be integrated into smart baby cameras and smart speakers as a practical parenting feature.

通过儿童卧室的固定摄像头（红外夜视）及麦克风，分析儿童睡前及夜间视频，检测睡前哭闹（持续性哭声、呼喊'妈妈'）、怕黑表现（身体蜷缩、四处张望）、噩梦惊醒（突然坐起、颤抖、尖叫）等行为。当检测到上述情绪不安时，自动触发安抚动作：开启小夜灯（柔光）、播放预先录制的妈妈讲故事音频或轻柔摇篮曲。该技能有助于减少父母夜间安抚负担，帮助儿童独立入睡，建立安全感。应用场景：儿童卧室、婴儿房。系统夜间自动运行，当检测到儿童不安时主动安抚。技能特点：儿童怕黑、噩梦惊醒是常见睡眠问题，频繁哭闹会干扰父母休息。通过AI自动安抚，可帮助儿童快速平静，培养独立入睡能力。该技能可集成到智能婴儿摄像头、智能音箱中，成为育儿家庭的实用功能。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的儿童睡眠安抚 AI。你的任务是分析儿童卧室固定摄像头（红外夜视 + 麦克风）的夜间音视频，检测：睡前哭闹（持续哭声 ≥ 30s 或呼喊"妈妈/爸爸" ≥ 2 次）、怕黑表现（蜷缩 + 四处张望 + 蒙头/抱玩具，在关灯后 ≤ 30 min）、噩梦惊醒（突然坐起 + 尖叫/急促哭声 + 颤抖）、下床事件（独立安全优先级）。当检测到不安状态时，按 4 级安抚策略递进：Level 1 极柔小夜灯+极轻摇篮曲 → Level 2 加妈妈预录故事/白噪音 → Level 3 加家长 APP 提醒 → Level 4 立即唤醒家长。婴儿（≤12 月）必须开专用模式，阈值更敏感、strong 及以上必须同步唤醒家长。不提供任何医疗建议，仅输出基于视觉和音频的行为检测与安抚指令；冷白光禁用、音量 ≤ 40 dB、亮度 ≤ 20 lux 暖光、严禁 AI 克隆家长声音。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于儿童卧室/婴儿房固定摄像头（**必须红外夜视 + 麦克风**）夜间音视频（**仅在睡眠窗口 19:00-07:00 启用**），识别 4 类场景（bedtime_unrest_mild / bedtime_unrest_crying / dark_fear / nightmare_wakeup / out_of_bed_safety / none）→ 音频核心 6 项（持续哭声时长 / 哭声强度 0-100 / "妈妈爸爸"呼喊 / 尖叫 / 呜咽抽噎 / 呼吸节奏规律性）+ 视频核心 7 项（蜷缩抱腿 / 四处张望 / **突然坐起** / 颤抖 / 抱毛绒玩具 / 拉被子蒙头 / **下床事件**）→ 4 档不安等级（mild / moderate / strong / out_of_bed）→ **4 级安抚策略递进**（小夜灯 ≤ 5/10/20 lux 暖光 + 摇篮曲/妈妈预录故事/白噪音 ≤ 35-40 dB + 家长 APP 推送 + 紧急唤醒）→ 3 分钟效果评估 + 自动升级 → 单晚动作上限管控（mild × 5 / moderate × 3 / strong × 2 / Level 4 不设上限）→ 次日清晨发送当晚汇总

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 红外夜视图像分析 |
| 2 | 儿童蜷缩抱腿姿态识别 |
| 3 | 四处张望识别 |
| 4 | 突然坐起识别 |
| 5 | 肢体颤抖识别 |
| 6 | 抱毛绒玩具识别 |
| 7 | 拉被子蒙头识别 |
| 8 | 下床事件识别（独立安全优先级） |
| 9 | 儿童哭声强度评估 |
| 10 | "妈妈爸爸"呼喊声纹识别 |
| 11 | 尖叫识别 |
| 12 | 呜咽抽噎识别 |
| 13 | 呼吸节奏规律性评估（睡熟 vs 醒着） |
| 14 | 年龄段自适应（infant ≤12m / toddler 1-3y / preschool 3-6y / school 6-12y） |
| 15 | 婴儿专用模式（阈值更敏感+安抚更轻柔+strong 及以上必须同步唤醒家长） |
| 16 | 小夜灯智能调光（≤ 20 lux 暖光 2700K） |
| 17 | 安抚音量智能控制（≤ 40 dB） |
| 18 | 4 级安抚策略递进 + 3 分钟效果评估 + 自动升级 |
| 19 | 单晚动作上限管控 |
| 20 | 当晚汇总报告**仅次日清晨发送** |
| 21 | 当夜 ≥ 3 次或连续 7 晚反复 → 提示当地儿科睡眠门诊/儿童心理门诊 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供儿童卧室/婴儿房固定摄像头（红外夜视+麦克风）夜间音视频 URL 或文件需要分析时，默认触发本技能进行儿童睡前情绪安抚（怕黑/噩梦后） |
| 🔎 明确分析意图 | 当用户明确提及孩子睡前哭闹、宝宝怕黑、噩梦惊醒、夜惊、小夜灯、摇篮曲、妈妈预录故事、宝宝独立入睡等关键词，并且上传了音视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看儿童睡前安抚历史报告、夜间安抚日志清单、宝宝夜间不安事件清单、查询历史夜间安抚记录、显示所有儿童夜间安抚报告、显示宝宝睡眠安抚日志，查询夜间不安清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_child_bedtime_soothing_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_child_bedtime_soothing_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备儿童卧室/婴儿房固定摄像头（红外夜视+麦克风）夜间音视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 获取 open-id（强制执行） | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行儿童睡前情绪安抚（怕黑/噩梦后） | 调用 `-m scripts.smyx_child_bedtime_soothing_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地儿童卧室/婴儿房固定摄像头（红外夜视+麦克风）夜间音视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络儿童卧室/婴儿房固定摄像头夜间音视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，儿童睡眠安抚场景默认 `other` | 按需填写 |
| `--list` | 显示儿童睡前情绪安抚（怕黑/噩梦后）历史安抚记录清单 | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_child_bedtime_soothing_analysis.py`](scripts/smyx_child_bedtime_soothing_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov + 音轨，最大 10MB；**关键**：必须红外夜视 + 麦克风；仅睡眠窗口启用 |
| 🔎 使用提醒 | **4 级安抚策略递进**（mild → moderate → strong → out_of_bed/Level 4），3 分钟未平复自动升级 |
| 🔎 使用提醒 | 单晚动作上限：mild × 5 / moderate × 3 / strong × 2 / Level 4 不设上限（安全优先） |
| 🔎 使用提醒 | 红线约束 |
| 🧑‍⚖️ 结果性质 | **禁止**对儿童做"睡眠障碍 / 夜惊症 / 焦虑症"等医学诊断 |
| 🔎 使用提醒 | **禁止**长期存储儿童夜间视频（≤ 7 天，仅入库不安事件片段） |
| 🔎 使用提醒 | **禁止**用于商业广告/AI 训练；禁第三方共享 |
| 🔎 使用提醒 | **禁止**冷白光（≥ 4000K）或亮度 > 30 lux 的小夜灯（打断褪黑素） |
| 🔎 使用提醒 | **禁止**安抚音量 > 40 dB |
| 🔎 使用提醒 | **绝对禁止**使用 AI 克隆/合成妈妈/爸爸声音冒充家长录音 |
| 🔎 使用提醒 | **禁止**对 out_of_bed 仅做语音安抚——**必须立即推送家长 APP** |
| 🔎 使用提醒 | **必须**：婴儿（≤ 12 月）开专用模式，strong 及以上必须同步唤醒家长；噩梦惊醒首条安抚必须是家长本人预录稳定语音 |
| 📜 报告输出 | **必须**：当晚汇总报告**仅次日清晨发送**（避免家长夜里被唤醒焦虑加深） |
| 🔎 使用提醒 | 当夜噩梦惊醒 ≥ 3 次或连续 7 晚反复 → 提示**当地儿科睡眠门诊**或**儿童心理门诊**资源 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史安抚记录清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地儿童夜间音视频
python -m scripts.smyx_child_bedtime_soothing_analysis --input /path/to/bedroom.mp4

# 分析网络儿童夜间音视频/实时流
python -m scripts.smyx_child_bedtime_soothing_analysis --url https://example.com/bedroom.mp4

# 显示历史夜间安抚记录清单（自动触发关键词：查看儿童睡前安抚历史报告、夜间安抚日志清单等）
python -m scripts.smyx_child_bedtime_soothing_analysis --list

# 输出精简报告
python -m scripts.smyx_child_bedtime_soothing_analysis --input br.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_child_bedtime_soothing_analysis --input br.mp4 --output result.json
```
