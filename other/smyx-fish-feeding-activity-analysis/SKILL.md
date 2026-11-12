---
name: "smyx-fish-feeding-activity-analysis"
description: "Through built-in cameras of smart feeders or fixed cameras on aquariums, the system captures fish feeding videos after feeding. Using AI object detection and motion analysis, it identifies the number of fish gathering for food, feeding intensity (fish swimming speed, feeding action frequency), and remaining feed amount, and computes a comprehensive feeding activity score (0-100). | 通过智能喂食器内置摄像头或鱼缸固定摄像头，在投喂后拍摄鱼群摄食视频，利用 AI 目标检测和运动分析技术，识别鱼群聚集抢食的数量、摄食强度（鱼只游动速度、摄食动作频率）以及剩余饲料量，综合计算摄食活跃度评分（0-100 分）。当活跃度评分低于阈值时，输出'食欲下降'提示，可能预示疾病、水质恶化或应激反应。"
version: "1.0.19"
---

# 🍽️ Fish Feeding Behavior Activity Analysis | 鱼类摄食行为活跃度分析
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **鱼类摄食行为活跃度分析** |
| 🎯 核心目标 | 通过智能喂食器内置摄像头或鱼缸固定摄像头，在投喂后拍摄鱼群摄食视频，利用 AI 目标检测和运动分析技术，识别鱼群聚集抢食的数量、摄食强度（鱼只游动速度、摄食动作频率）以及剩余饲料量，综合计算摄食活跃度评分（0-100 分）。当活跃度评分低于阈值时，输出'食欲下降'提示，可能预示疾病、水质恶化或应激反应。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_FISH_FEEDING_ACTIVITY_ANALYSIS` |

Through built-in cameras of smart feeders or fixed cameras on aquariums, the system captures fish feeding videos after feeding. Using AI object detection and motion analysis, it identifies the number of fish gathering for food, feeding intensity (fish swimming speed, feeding action frequency), and remaining feed amount, and computes a comprehensive feeding activity score (0-100). When the score falls below the threshold, the system outputs an 'appetite decline' alert, which may indicate disease, water quality deterioration, or stress reaction. Application scenarios: smart feeders, home aquariums, aquaculture farms, public aquariums. The system automatically analyzes after each feeding, generates a feeding report, and pushes reminders when abnormal. Skill features: appetite decline is an early signal of fish diseases (e.g. enteritis, parasites). AI-based automatic monitoring of feeding activity helps aquarists detect problems early and reduce losses. This skill can be integrated into smart feeders or aquarium cameras to improve product intelligence.

通过智能喂食器内置摄像头或鱼缸固定摄像头，在投喂后拍摄鱼群摄食视频，利用 AI 目标检测和运动分析技术，识别鱼群聚集抢食的数量、摄食强度（鱼只游动速度、摄食动作频率）以及剩余饲料量，综合计算摄食活跃度评分（0-100 分）。当活跃度评分低于阈值时，输出'食欲下降'提示，可能预示疾病、水质恶化或应激反应。应用场景：智能喂食器、家庭鱼缸、水产养殖场、水族馆。系统在每次投喂后自动分析，生成摄食报告，异常时推送提醒。技能特点：食欲减退是鱼类疾病（如肠炎、寄生虫）的早期信号。通过 AI 自动监测摄食活跃度，可帮助养鱼者及早发现问题，减少损失。该技能可集成到智能喂食器或鱼缸摄像头中，提升产品智能化水平。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的水族摄食行为分析 AI。你的任务是分析鱼缸固定摄像头/智能喂食器内置摄像头**投喂后 1 分钟内**的视频（可选续采至 3 分钟用于剩余饲料评估），检测鱼群聚集抢食的数量、摄食强度（游动速度、摄食动作频率、抢食激烈度）以及剩余饲料量，综合计算摄食活跃度评分（0-100）。按 7 类综合场景（feeding_excellent / normal / slightly_low / appetite_decline / severe_appetite_loss / total_refusal / signal_unreliable）作判定，按 4 级告警策略递进（Level 1 入库/轻提醒 → Level 2 重要告警 + 检查水温/溶氧/pH/氨氮 + 近期换鱼/换水/换饲料 → Level 3 紧急告警 + 隔离精神萎靡个体 + 暂停下次投喂 + 联系兽医 → Level 4 完全拒食/连续 ≥ 3 餐异常 + 全面检查（水质+体表+游姿+呼吸）+ 联系专业人员）。鱼种特异性必须按基线判定（水面金鱼/锦鲤 vs 底层鼠鱼/异型 vs 立体抢食神仙鱼 vs 日间不进食的夜行鱼）。必须考虑生理性低食欲的上下文（水温骤变、繁殖期、灯光过渡期、饲料品牌切换），避免误报。视频不在投喂窗口/未检测到投喂动作/水浑浊度过高时，必须返回 `feeding_signal_unreliable` 并建议重拍，**禁止给出不可靠的食欲下降告警**。不提供任何疾病诊断，仅输出基于视觉的活跃度评估；**禁止输出具体药物名称和剂量**；严禁伪造夸大评分，严禁越权代用户启停智能喂食器/换水/投药等设备（仅可建议或在用户明确授权范围内调整下次投喂量）。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于智能喂食器内置摄像头 / 鱼缸固定摄像头 / 养殖池上方摄像头**投喂后 1 分钟内**（关键采样窗口）视频，识别 7 类综合场景（feeding_excellent / normal / slightly_low / appetite_decline / severe_appetite_loss / total_refusal / signal_unreliable）→ **四组指标**：鱼群聚集 4 项（聚集数 / 基线总数 / 聚集比例 / 响应时长）+ 摄食强度 5 项（平均游动速度 / 摄食动作频率 / 抢食激烈度 / 水面摄食事件 / 中底层摄食事件）+ 剩余饲料 3 项（60s 水面残留 / 180s 缸底残留 / 剩余饲料比例）+ 综合评分 1 项（0-100）→ **4 档异常等级**（excellent → slightly_low → appetite_decline → severe/total）→ **4 级告警策略递进**（入库/轻提醒 → 重要告警 + 水质 + 饲料 + 应激排查 → 紧急告警 + 隔离 + 暂停投喂 + 联系兽医 → 最高紧急告警 + 全面检查 + 专业介入）→ 单日告警上限（Level 1 不限 / Level 2 × 4 / Level 3 × 2 / Level 4 不设上限）→ **每餐摄食报告**（按 tank_id + 投喂时间戳输出，含活跃度评分 + 关键子指标 + 下次投喂量建议 + 免责声明）

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 投喂动作自动检测（饲料抛入水面识别）/ 智能喂食器投喂事件联动 |
| 2 | 鱼群目标检测与跟踪（多鱼 ReID） |
| 3 | 聚集数与基线比对 |
| 4 | 游动速度量化（像素/秒 |
| 5 | 可校准为体长/秒） |
| 6 | 摄食动作频率识别（张嘴啄食 / 转身咬颗粒） |
| 7 | 抢食激烈度评分 |
| 8 | 水面/中层/底层摄食事件分层统计 |
| 9 | 剩余饲料颗粒计数（60s 水面 + 180s 缸底） |
| 10 | 综合评分加权融合 |
| 11 | 鱼种自适应基线（水面型 / 底层型 / 立体型 / 夜行型） |
| 12 | 生理性低食欲上下文识别 |
| 13 | 用户 APP 推送 |
| 14 | 4 级告警递进 |
| 15 | 单日告警上限 |
| 16 | 每餐摄食报告（按 tank_id + 投喂时间戳输出） |
| 17 | 下次投喂量建议（基于剩余饲料比例 |
| 18 | 仅建议） |
| 19 | 连续 ≥ 3 餐 Level 2 → 强烈建议联系**当地观赏鱼兽医或养殖场技术员** |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供智能喂食器/鱼缸投喂后 1 分钟内视频 URL 或文件需要分析时，默认触发本技能进行鱼类摄食行为活跃度分析 |
| 🔎 明确分析意图 | 当用户明确提及鱼摄食活跃度、鱼食欲下降、鱼不吃食、鱼抢食、智能喂食器、剩余饲料、鱼摄食评分等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看鱼摄食历史报告、鱼缸摄食活跃度日志清单、食欲下降事件清单、查询历史鱼摄食记录、显示所有鱼缸摄食报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_fish_feeding_activity_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_fish_feeding_activity_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备智能喂食器/鱼缸固定摄像头投喂后 1 分钟内视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 获取 open-id（强制执行） | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行鱼类摄食行为活跃度分析 | 调用 `-m scripts.smyx_fish_feeding_activity_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地智能喂食器/鱼缸固定摄像头投喂后 1 分钟内视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络智能喂食器/鱼缸固定摄像头投喂后 1 分钟内视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，鱼类摄食活跃度分析场景默认 `other` | 按需填写 |
| `--list` | 显示鱼类摄食行为活跃度分析历史记录清单 | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_fish_feeding_activity_analysis.py`](scripts/smyx_fish_feeding_activity_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov，最大 10MB；摄像头需完整覆盖投喂区域；**核心采样窗口：投喂后 1 分钟内**；帧率 ≥ 15 FPS |
| 🔎 使用提醒 | **4 级告警策略递进**（slightly_low → appetite_decline → severe_appetite_loss → total_refusal/Level 4），连续 ≥ 3 餐异常进入 Level 4 |
| 🔎 使用提醒 | 单日告警上限：Level 1 不限 / Level 2 × 4（按投喂次数）/ Level 3 × 2 / Level 4 不设上限（紧急安全优先） |
| 🔎 使用提醒 | 红线约束 |
| 🧑‍⚖️ 结果性质 | **禁止**对鱼做"肠炎 / 寄生虫 / 鳃病 / 细菌感染 / 应激综合征"等具体疾病诊断 |
| 🔎 使用提醒 | **🚨 绝对禁止**输出具体药物名称、剂量、给药方案 |
| 🔎 使用提醒 | **禁止**长期存储完整鱼缸/养殖池视频（≤ 7 天，仅入库异常摄食事件片段；公共养殖场按管理规定） |
| 🔎 使用提醒 | **禁止**用于商业广告 / AI 训练；禁第三方共享 |
| 🔎 使用提醒 | **禁止**越权代用户启停智能喂食器 / 投药 / 换水 / 加热 / 灯光；任何水族设备控制变更必须由用户确认（仅可建议或在用户明确授权范围内调整下次投喂量） |
| 🔎 使用提醒 | **绝对禁止**伪造或夸大评分、聚集比例、剩余饲料量等指标；所有数据必须基于真实视频帧统计 |
| 🔎 使用提醒 | **必须**按**鱼种基线**判定（水面金鱼/锦鲤 vs 底层鼠鱼/异型 vs 立体抢食神仙鱼 vs 日间不进食的夜行鱼）；**禁止使用通用阈值盲判** |
| 📚 文档读取 | **必须**考虑生理性低食欲的上下文（水温骤变、繁殖期、灯光过渡期、饲料品牌切换），避免误报 |
| 🔎 使用提醒 | **必须**在视频不在投喂窗口/未检测到投喂动作/水浑浊度过高时返回 `feeding_signal_unreliable`，**禁止给出不可靠的食欲下降告警** |
| 🔎 使用提醒 | **必须**：连续 ≥ 3 餐 Level 2 → 强烈建议联系**当地观赏鱼兽医或养殖场技术员** |
| 📜 报告输出 | **必须**：每餐摄食报告**按 tank_id + 投喂时间戳输出**，含活跃度评分 + 关键子指标 + 下次投喂量建议 + 免责声明 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史摄食记录清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地投喂后视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_fish_feeding_activity_analysis --input /path/to/feeding.mp4

# 分析网络投喂后视频/实时流（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_fish_feeding_activity_analysis --url https://example.com/feeding.mp4

# 显示历史摄食活跃度记录清单（自动触发关键词：查看鱼摄食历史报告、鱼缸摄食活跃度日志清单等）
python -m scripts.smyx_fish_feeding_activity_analysis --list

# 输出精简报告
python -m scripts.smyx_fish_feeding_activity_analysis --input fe.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_fish_feeding_activity_analysis --input fe.mp4 --output result.json
```
