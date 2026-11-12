---
name: "smyx-plant-vitality-index-analysis"
description: "Using a plant-monitoring platform that periodically (e.g., daily) collects plant images, environmental data, and growth metrics (new bud count, leaf-area change, leaf color), an AI evaluation model fuses leaf color (chlorophyll index), morphology (spread, leaf size), and growth dynamics (new buds, leaf-area growth rate) to output an overall vitality score from 0-100 along with a trend (rising / stable / declining). | 通过植物监测平台定期（如每天）采集的植物图像、环境数据以及生长指标（如新芽数、叶片面积变化、叶色），利用AI综合评估模型融合叶片颜色（叶绿素指数）、形态（舒展度、叶片大小）、生长动态（新芽萌发数、叶面积增长率），输出0-100的整体活力评分，并给出活力趋势（上升/稳定/下降）。"
version: "1.0.22"
---

# 🌿 Plant Vitality Index | 植物整体活力指数（综合评分）
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **植物整体活力指数（综合评分）** |
| 🎯 核心目标 | 通过植物监测平台定期（如每天）采集的植物图像、环境数据以及生长指标（如新芽数、叶片面积变化、叶色），利用AI综合评估模型融合叶片颜色（叶绿素指数）、形态（舒展度、叶片大小）、生长动态（新芽萌发数、叶面积增长率），输出0-100的整体活力评分，并给出活力趋势（上升/稳定/下降）。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_PLANT_VITALITY_INDEX_ANALYSIS` |

Using a plant-monitoring platform that periodically (e.g., daily) collects plant images, environmental data, and growth metrics (new bud count, leaf-area change, leaf color), an AI evaluation model fuses leaf color (chlorophyll index), morphology (spread, leaf size), and growth dynamics (new buds, leaf-area growth rate) to output an overall vitality score from 0-100 along with a trend (rising / stable / declining). It helps users intuitively grasp plant health and guides care decisions. Application scenarios: smart planters, plant factories, home gardening, plant-monitoring platforms. The system generates a daily vitality report and pushes alerts when scores keep dropping (e.g., 'vitality index dropped 15% in the past week, please check light or roots'). Skill features: an intuitive way to understand plant health.

通过植物监测平台定期（如每天）采集的植物图像、环境数据以及生长指标（如新芽数、叶片面积变化、叶色），利用AI综合评估模型融合叶片颜色（叶绿素指数）、形态（舒展度、叶片大小）、生长动态（新芽萌发数、叶面积增长率），输出0-100的整体活力评分，并给出活力趋势（上升/稳定/下降）。该技能帮助用户直观了解植物健康状况，指导养护决策。应用场景：智能花盆、植物工厂、家庭园艺、植物监测平台。系统每日生成活力指数报告，当评分持续下降时推送提醒（如'活力指数近一周下降15%，请检查光照或根系'）。技能特点：直观了解植物健康。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的植物健康评估 AI。你的任务是综合植物的多项视觉和环境指标（叶片颜色、新芽数量、叶片面积变化、生长速度等），计算整体活力指数（0-100 分），并分析近期变化趋势。不要提供具体养护操作（如施肥配方、修剪方案），仅输出评分及趋势。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于植物图像（单图或连续日间序列）+ 可选环境数据/生长指标，输出 0-100 整体活力评分与变化趋势

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 叶片颜色（叶绿素指数）评估 |
| 2 | 叶片形态（舒展度 |
| 3 | 叶片大小）评估 |
| 4 | 新芽萌发数计数 |
| 5 | 叶面积增长率估算（基于序列） |
| 6 | 整体株型紧凑度 |
| 7 | 活力总分（0-100） |
| 8 | 活力等级（excellent / good / fair / poor） |
| 9 | 近期趋势（rising / stable / declining） |
| 10 | 变化百分比 |
| 11 | 活力下降阈值告警 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供植物图像/连续日间图像序列/视频 URL 或文件需要分析时，默认触发本技能进行活力指数综合评分 |
| 🔎 明确分析意图 | 当用户明确提及活力指数、植物活力、综合评分、健康打分、生长状态打分、植物体检、活力趋势、叶绿素指数等关键词，并且上传了图像/视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看植物活力历史报告、活力指数报告清单、活力评分报告清单、查询历史活力指数、显示所有植物活力报告、显示植物体检诊断报告，查询活力趋势清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_plant_vitality_index_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_plant_vitality_index_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备植物图像输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行植物活力指数综合评分 | 调用 `-m scripts.smyx_plant_vitality_index_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地植物图像/连续日间图像序列/视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络植物图像/连续日间图像序列/视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，植物活力评估场景默认 `other` | 按需填写 |
| `--list` | 显示植物活力指数历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_plant_vitality_index_analysis.py`](scripts/smyx_plant_vitality_index_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 jpg/png 图像或 mp4/avi/mov 视频，最大 10MB；建议连续日间序列以获得稳定趋势 |
| 🧑‍⚖️ 结果性质 | 评分结果仅供养护参考，单次评分受拍摄角度/光照影响较大，建议结合趋势查看 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地植物图像/序列
python -m scripts.smyx_plant_vitality_index_analysis --input /path/to/plant.jpg

# 分析网络植物图像/视频
python -m scripts.smyx_plant_vitality_index_analysis --url https://example.com/plant.jpg

# 显示历史活力指数报告/活力指数报告清单（自动触发关键词：查看植物活力历史报告、活力指数报告清单等）
python -m scripts.smyx_plant_vitality_index_analysis --list

# 输出精简报告
python -m scripts.smyx_plant_vitality_index_analysis --input plant.jpg --detail basic

# 保存结果到文件
python -m scripts.smyx_plant_vitality_index_analysis --input plant.jpg --output result.json
```
