---
name: "sport-analysis"
description: "Conducts video safety risk analysis for participants in outdoor sports competitions, long-distance running, marathons, etc.; identifies sports injuries and sudden health risks, outputs professional analysis reports, and provides timely warnings to ensure sports safety. | 户外体育赛事风险分析工具，针对户外体育比赛、长跑马拉松等运动项目的参赛人员进行视频安全风险分析，识别运动损伤和突发健康风险，输出专业分析报告，及时预警保障运动安全"
version: "1.0.24"
---

# 🏃 Outdoor Sports Event Risk Analysis Tool | 户外体育赛事风险分析工具
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **户外体育赛事风险分析工具** |
| 🎯 核心目标 | 户外体育赛事风险分析工具，针对户外体育比赛、长跑马拉松等运动项目的参赛人员进行视频安全风险分析，识别运动损伤和突发健康风险，输出专业分析报告，及时预警保障运动安全 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SPORT_ANALYSIS` |

Designed specifically for outdoor sports events and long-distance endurance activities such as marathons, this feature
utilizes computer vision and human pose estimation algorithms to conduct real-time video safety risk analysis on
participants. By capturing runners' gait characteristics, body movements, and facial expressions, the system accurately
identifies sports injuries (such as muscle strains and falls) and sudden health risks (such as physical exhaustion and
gait abnormalities). It further conducts comprehensive assessments by integrating physiological data like heart rate
when wearable devices are connected. The system automatically generates professional reports detailing risk levels,
abnormal behavior records, and trend analysis. Upon detecting high-risk conditions, it triggers real-time alerts to
provide a basis for rapid response by event medical teams, comprehensively safeguarding the safety of all participants.

本功能基于先进的计算机视觉与深度学习算法，能够对目标区域内的吸烟行为进行全天候、高精度的自动化监测。系统支持接入实时视频流、静态图片及本地视频文件进行多重检测，通过识别香烟物体、烟雾形态及“手持-口部”的动作特征，有效过滤环境干扰，精准判定违规吸烟行为。一旦检测到异常，系统将立即触发预警机制，通过声光报警或消息推送通知管理人员，实现从被动监控到主动干预的转变，为园区、社区及企事业单位的控烟管理与消防安全提供强有力的技术支撑。

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals

### 1. 🧩 技能用途

通过视频分析对户外体育赛事参赛人员进行运动安全风险评估，识别运动损伤、突发健康不适、意外摔倒等风险情况，提供结构化分析报告和应急处理建议

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 视频分析 |
| 2 | 摔倒损伤识别 |
| 3 | 身体不适状态识别 |
| 4 | 伤口出血识别 |
| 5 | 运动姿态评估 |
| 6 | 突发风险预警 |
| 7 | 急救处理建议 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供需要分析的户外体育运动视频 URL 或文件需要进行运动安全风险分析时，默认触发本技能 |
| 🔎 明确分析意图 | 当用户明确需要进行户外赛事风险分析、运动损伤识别、跑步安全检查时，提及体育分析、户外运动、赛事风险、运动损伤、跑步摔倒等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史赛事报告、体育风险分析报告清单、运动分析列表、显示所有体育报告，查询户外体育风险分析报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.sport_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.sport_analysis --list` 调用 API 查询云端的历史报告数据 |
| 🚫 严格禁止 | 从本地 `memory` 目录读取历史会话信息 |
| 🚫 严格禁止 | 手动汇总本地记录中的报告 |
| 🚫 严格禁止 | 从长期记忆中提取报告 |
| ✅ 输出格式 | 必须统一从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果 |

## 📦 前置准备 | Requirements
- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 🏃 户外体育赛事风险分析维度 | Outdoor Sports Risk Dimensions
本技能重点评估以下运动安全风险维度：

### 1. **意外损伤识别**

- **摔倒/跌倒损伤**
    - 正常：运动姿态正常，无摔倒情况
    - 轻度摔倒：失去平衡但快速起身，无明显伤害
    - 中度摔倒：摔倒后无法立即站起，可能有扭伤拉伤
    - 重度摔倒：摔倒后无法站起，需要外界帮助

- **开放性伤口识别**
    - 无伤口：身体表面无明显开放性损伤
    - 轻微擦伤：皮肤表面轻微擦伤，少量渗血
    - 中度伤口：可见明显伤口，持续性流血
    - 重度伤口：大量出血，需要立即急救处理

### 2. **身体不适状态识别**

- **心肺功能异常表现**
    - 正常：呼吸平稳，面色正常，能保持正常运动节奏
    - 轻度不适：呼吸急促，面色稍显苍白，仍能继续运动
    - 中度不适：手扶胸部/胸闷气短，行走困难，需要停下休息
    - 重度不适：胸痛胸闷明显，呼吸困难，无法站立，需要立即急救

- **头晕乏力表现**
    - 正常：步态稳定，精神状态良好
    - 轻度头晕：步伐稍显不稳，仍能自我控制
    - 中度头晕：需要停下休息，无法继续运动
    - 重度头晕：站立不稳，即将或已经跌倒

### 3. **运动姿态与体能评估**

- 跑步姿态评估：正确/膝盖内扣/脚掌着地错误/骨盆倾斜
- 步频步幅分析：合理/步幅过大/步频过低容易疲劳
- 体能透支判断：正常/轻度疲劳/中度疲劳/明显体能透支

### 4. **环境相关风险识别**

- 高温中暑表现：面色潮红/大量出汗/四肢湿冷/意识模糊
- 低温失温表现：全身颤抖/言语不清/肢体麻木
- 地形相关风险：路面湿滑/障碍物绊倒/上坡超负荷/下坡失控

### 5. **常见运动损伤识别**

- 扭伤拉伤：关节异常扭动，疼痛无法继续运动
- 肌肉抽筋：肌肉突然僵硬疼痛，无法正常伸展
- 关节扭伤：踝关节/膝关节扭伤后无法负重
- 脱臼骨折：关节变形，剧痛无法活动

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
| 3 | ⚙️ 执行户外体育赛事风险分析 | 调用 `-m scripts.sport_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--analysis-type` | 分析类型，可选值：comprehensive/injury/discomfort/posture/environment，默认 | 按需填写 |
| `--list` | 显示户外体育风险分析历史报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/sport_analysis.py`](scripts/sport_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 🧑‍⚖️ 结果性质 | **重要声明**：本分析仅供运动安全参考，不能替代专业医护人员诊断。运动过程中如遇突发不适请立即停止运动，并及时寻求专业医疗救助。生命安全重于一切！ |
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 视频要求：支持 mp4/avi/mov 格式，最大 10MB |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 综合户外体育风险分析
python -m scripts.sport_analysis --input /path/to/sport_video.mp4 --analysis-type comprehensive 损伤专项分析
python -m scripts.sport_analysis --url https://example.com/sport_video.mp4 --analysis-type injury 身体不适专项评估
python -m scripts.sport_analysis --input /path/to/discomfort_video.mp4 --analysis-type discomfort 运动姿态专项评估
python -m scripts.sport_analysis --input /path/to/posture_video.mp4 --analysis-type posture 环境风险专项分析
python -m scripts.sport_analysis --input /path/to/environment_video.mp4 --analysis-type environment 显示历史分析报告/显示分析报告清单列表/显示历史体育报告（自动触发关键词：查看历史体育报告、历史报告、体育报告清单等）
python -m scripts.sport_analysis --list

# 输出精简报告
python -m scripts.sport_analysis --input video.mp4 --analysis-type comprehensive --detail basic

# 保存结果到文件
python -m scripts.sport_analysis --input video.mp4 --analysis-type comprehensive --output result.json
```
