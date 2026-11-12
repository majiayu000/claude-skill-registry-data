---
name: "smyx-fish-egg-incubation-stage-analysis"
description: "Through breeding-tank fixed cameras (macro lens), the system periodically captures high-definition images of fish eggs and uses AI vision analysis to detect egg color changes (transparent → white / black) and embryonic eye-spots (small black dots), identifying incubation stages (unfertilized / early / mid / late-eyespot / hatching). | 通过繁殖缸固定摄像头（微距镜头），定期拍摄鱼卵的高清图像，利用 AI 视觉分析技术检测鱼卵颜色变化（透明 → 发白/发黑）以及胚胎眼睛点（黑色小点）的出现，识别鱼卵的孵化阶段（未受精/早期/中期/晚期/破壳）。系统定时（如每 6 小时）自动分析，输出孵化阶段及建议（如'已出现眼睛点，预计 24 小时内孵化，准备丰年虾'）。"
version: "1.0.20"
---

# 🥚 Fish Egg Incubation Stage Identification | 鱼卵孵化状态识别
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **鱼卵孵化状态识别** |
| 🎯 核心目标 | 通过繁殖缸固定摄像头（微距镜头），定期拍摄鱼卵的高清图像，利用 AI 视觉分析技术检测鱼卵颜色变化（透明 → 发白/发黑）以及胚胎眼睛点（黑色小点）的出现，识别鱼卵的孵化阶段（未受精/早期/中期/晚期/破壳）。系统定时（如每 6 小时）自动分析，输出孵化阶段及建议（如'已出现眼睛点，预计 24 小时内孵化，准备丰年虾'）。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_FISH_EGG_INCUBATION_STAGE_ANALYSIS` |

Through breeding-tank fixed cameras (macro lens), the system periodically captures high-definition images of fish eggs and uses AI vision analysis to detect egg color changes (transparent → white / black) and embryonic eye-spots (small black dots), identifying incubation stages (unfertilized / early / mid / late-eyespot / hatching). This skill helps ornamental fish breeders track incubation progress and timely separate fry or adjust water quality. Application scenarios: ornamental fish breeding tanks, aquaculture hatcheries, laboratories. The system periodically analyzes (e.g. every 6 hours) and outputs incubation stages plus suggestions (such as 'eye-spots have appeared, hatching expected within 24 hours, prepare brine shrimp'). Skill features: incubation period is a critical stage of ornamental fish breeding — separating fry too early causes death, while separating too late risks the parent fish eating the fry. AI-based automatic recognition of eye-spots and color changes helps novice breeders easily grasp the right timing and reduce failure rate. This skill can be integrated into smart breeding tanks or mobile macro lenses, becoming a breeding assistant for ornamental fish enthusiasts.

通过繁殖缸固定摄像头（微距镜头），定期拍摄鱼卵的高清图像，利用 AI 视觉分析技术检测鱼卵颜色变化（透明 → 发白/发黑）以及胚胎眼睛点（黑色小点）的出现，识别鱼卵的孵化阶段（未受精/早期/中期/晚期/破壳）。该技能有助于观赏鱼繁殖者掌握孵化进度，及时分离鱼苗或调整水质。应用场景：观赏鱼繁殖缸、水产育苗场、实验室。系统定时（如每 6 小时）自动分析，输出孵化阶段及建议（如'已出现眼睛点，预计 24 小时内孵化，准备丰年虾'）。技能特点：鱼卵孵化期是观赏鱼繁殖的关键阶段，过早分离鱼苗会导致死亡，过晚则可能被种鱼吞食。通过 AI 自动识别眼睛点和颜色变化，可帮助新手繁殖者轻松掌握时机，降低失败率。该技能可集成到智能繁殖缸或手机微距镜头中，成为观赏鱼爱好者的繁殖助手。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的水产繁育 AI。你的任务是分析鱼卵的微距图像（≥ 3 倍光学微距，分辨率 ≥ 1080p），检测卵的颜色变化（透明 → 发白/灰白 → 发黑）以及胚胎眼睛点（黑色小点，<0.3 mm）的出现，并结合**鱼种 + 水温 + 距产卵时长**联合判定 8 类孵化阶段（incubation_unfertilized / early / mid / late_eyespot / pre_hatch / hatching / mass_failure / signal_unreliable），按 4 级提醒策略递进（Level 1 进度更新 → Level 2 重要提示 + 准备丰年虾/草履虫/分离亲鱼 → Level 3 紧急提示 + 停止充气避免吸入幼苗 + 隔离 → Level 4 大面积失败 + 清理坏卵防霉 + 检查亲鱼/水温/光照）。鱼种特异性必须按基线判定（斑马鱼 48-72h 透明小卵 vs 神仙鱼 60-72h 黄褐色粘性卵 vs 七彩 60-72h 黄色卵 vs 锦鲤 96-120h@20℃ vs 鼠鱼银白色卵），**严禁通用阈值盲判**。必须做白平衡校正避免"背光偏色让透明卵看起来发白"的误判。焦距未对准 / 卵团遮挡 / 浑浊度过高时必须返回 `incubation_signal_unreliable` 并建议重拍/对焦/补光。不提供任何疾病诊断，仅输出基于视觉的孵化阶段分类；**严禁推荐甲基蓝、二氯异氰尿酸钠等防霉化学药物**，**严禁输出具体药物名称和剂量**；严禁伪造夸大颜色比例 / 眼睛点检出率；严禁越权代用户启停加热棒/增氧/换水/灯光（仅建议）。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于繁殖缸固定摄像头 / 微距镜头（≥ 3× 光学微距）/ 智能繁殖缸内置微距**定时拍摄**（默认每 6 小时 ≥ 1 张），识别 8 类孵化阶段（incubation_unfertilized / early / mid / late_eyespot / pre_hatch / hatching / mass_failure / signal_unreliable）→ **三组指标**：卵颜色 5 项（卵总数 / 透明比例 / 发白比例 / 发黑比例 / 黄色卵黄囊比例）+ 胚胎发育 4 项（眼睛点检出数 / 检出比例 / 胚胎抽动 / 破壳事件）+ 上下文与基线 4 项（鱼种 / 鱼种基线孵化时长 / 当前水温 / 距产卵时长）→ 4 档提醒级别（info / important / urgent / warning）→ **4 级提醒策略递进**（仅入库进度更新 → 准备丰年虾分离亲鱼 → 停止充气+隔离 → 大面积失败建议清理坏卵+检查亲鱼水温光照）→ 单日提醒上限（Level 1 不限 / Level 2 × 4 / Level 3 × 6 / Level 4 × 2）→ **每次定时分析的孵化阶段报告**（按 tank_id + spawn_time 输出，含颜色分布 + 眼睛点检出率 + 预计破壳时间窗 + 建议动作 + 免责声明）

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 鱼卵小目标检测（直径 0.5-2 mm） |
| 2 | 卵分类（透明 / 发白 / 发黑 / 含黄色卵黄囊） |
| 3 | **胚胎眼睛点检测**（黑色亚毫米小点） |
| 4 | 胚胎抽动光流检测 |
| 5 | 破壳事件识别（卵壳破裂 + 鱼苗游出） |
| 6 | 鱼种自适应基线（孵化时长 + 卵颜色基线） |
| 7 | **水温修正的孵化龄估算**（Q10 系数粗校正） |
| 8 | 白平衡校正（避免背光偏色误判） |
| 9 | 用户 APP 推送 |
| 10 | 4 级提醒递进 |
| 11 | 单日提醒上限 |
| 12 | 每次定时分析的孵化阶段报告（按 tank_id + spawn_time 输出） |
| 13 | 预计破壳时间窗给出（"24h 内孵化"等开口饵料准备提示） |
| 14 | **侧重育苗助手定位**（非健康告警 |
| 15 | 更偏积极进度提示） |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供繁殖缸固定摄像头/微距镜头鱼卵高清图像或视频 URL/文件需要分析时，默认触发本技能进行鱼卵孵化状态识别 |
| 🔎 明确分析意图 | 当用户明确提及鱼卵孵化、眼睛点、丰年虾准备、未受精卵、坏卵清理、亲鱼分离、破壳等关键词，并且上传了图像/视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看鱼卵孵化历史报告、繁殖缸孵化进度日志清单、孵化阶段事件清单、查询历史鱼卵记录、显示所有繁殖缸孵化报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_fish_egg_incubation_stage_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_fish_egg_incubation_stage_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备繁殖缸固定摄像头/微距镜头鱼卵高清图像输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 获取 open-id（强制执行） | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行鱼卵孵化状态识别 | 调用 `-m scripts.smyx_fish_egg_incubation_stage_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地繁殖缸固定摄像头/微距镜头鱼卵高清图像或视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络繁殖缸固定摄像头/微距镜头鱼卵高清图像或视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，鱼卵孵化状态识别场景默认 `other` | 按需填写 |
| `--list` | 显示鱼卵孵化状态识别历史记录清单 | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_fish_egg_incubation_stage_analysis.py`](scripts/smyx_fish_egg_incubation_stage_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 jpg/png/mp4/avi/mov，最大 10MB；摄像头需 **≥ 3× 光学微距 + 冷白补光 + 透过卵层背光**；分辨率 ≥ 1080p；建议每 6 小时定时 ≥ 1 张 |
| 🔎 使用提醒 | **4 级提醒策略递进**（info → important → urgent → warning），偏育苗助手定位（非健康告警） |
| 🔎 使用提醒 | 单日提醒上限：Level 1 不限 / Level 2 × 4 / Level 3 × 6（破壳事件可能密集）/ Level 4 × 2 |
| 🔎 使用提醒 | 红线约束 |
| 🧑‍⚖️ 结果性质 | **禁止**做"水霉感染 / 真菌污染 / 受精率不足 / 亲鱼不孕"等具体疾病或繁殖学诊断 |
| 🔎 使用提醒 | **🚨 绝对禁止**输出具体药物名称、剂量、给药方案（特别**严禁推荐甲基蓝、二氯异氰尿酸钠等防霉化学剂**） |
| 🔎 使用提醒 | **禁止**长期存储完整鱼缸视频/图像（≤ 14 天，仅入库孵化阶段事件帧；公共育苗场/实验室按管理规定） |
| 🔎 使用提醒 | **禁止**用于商业广告 / AI 训练；禁第三方共享 |
| 🔎 使用提醒 | **禁止**越权代用户启停加热棒 / 增氧 / 换水 / 投药 / 灯光参数；任何水族设备控制变更必须由用户确认（仅可建议） |
| 🔎 使用提醒 | **绝对禁止**伪造或夸大颜色比例、眼睛点检出比例、孵化进度等指标；所有数据必须基于真实图像识别 |
| 🔎 使用提醒 | **必须**按**鱼种 + 水温**联合判定基线（斑马鱼 48-72h 透明小卵 / 神仙鱼 60-72h 黄褐色 / 七彩 60-72h 黄色 / 锦鲤 96-120h@20℃ / 鼠鱼银白色卵）；**禁止使用通用阈值盲判** |
| 🔎 使用提醒 | **必须**做白平衡校正，避免"背光偏色让透明卵看起来发白"导致的未受精误判 |
| 🔎 使用提醒 | **必须**在焦距未对准 / 卵团遮挡 / 浑浊度过高时返回 `incubation_signal_unreliable`，**禁止给出不可靠的失败/未受精判定** |
| 📜 报告输出 | **必须**：每次定时分析的孵化阶段报告**按 tank_id + spawn_time 输出**，含颜色分布 + 眼睛点检出率 + 预计破壳时间窗 + 建议动作 + 免责声明 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史孵化记录清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地鱼卵微距图像（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_fish_egg_incubation_stage_analysis --input /path/to/eggs.jpg

# 分析网络鱼卵微距图像/视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_fish_egg_incubation_stage_analysis --url https://example.com/eggs.jpg

# 显示历史孵化状态记录清单（自动触发关键词：查看鱼卵孵化历史报告、繁殖缸孵化进度日志清单等）
python -m scripts.smyx_fish_egg_incubation_stage_analysis --list

# 输出精简报告
python -m scripts.smyx_fish_egg_incubation_stage_analysis --input eggs.jpg --detail basic

# 保存结果到文件
python -m scripts.smyx_fish_egg_incubation_stage_analysis --input eggs.jpg --output result.json
```
