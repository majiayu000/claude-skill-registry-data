---
name: "smyx-uav-farm-health-index-map-analysis"
description: "Using multispectral or high-resolution RGB cameras mounted on agricultural UAVs to capture orthophotos or mosaics of farmland, AI models compute vegetation indices (e.g., NDVI, NDRE) and generate a farm health-index heatmap, where colors distinguish crop vigor (red = poor, yellow = medium, green = healthy). | 通过农业无人机平台搭载的多光谱或高分辨率RGB相机，采集农田的正射影像或拼接图，利用AI模型计算植被指数（如归一化植被指数NDVI、归一化红边指数NDRE等），生成农田健康指数热力图，用颜色区分作物长势（红色代表健康差、黄色代表中等、绿色代表健康）。该技能可快速识别问题区域（如缺肥、缺水、病虫害、杂草），指导精准变量施肥或植保作业。"
version: "1.0.21"
---

# 🚁 UAV Farm Health Index Map | 无人机农田健康指数图生成
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **无人机农田健康指数图生成** |
| 🎯 核心目标 | 通过农业无人机平台搭载的多光谱或高分辨率RGB相机，采集农田的正射影像或拼接图，利用AI模型计算植被指数（如归一化植被指数NDVI、归一化红边指数NDRE等），生成农田健康指数热力图，用颜色区分作物长势（红色代表健康差、黄色代表中等、绿色代表健康）。该技能可快速识别问题区域（如缺肥、缺水、病虫害、杂草），指导精准变量施肥或植保作业。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_UAV_FARM_HEALTH_INDEX_MAP_ANALYSIS` |

Using multispectral or high-resolution RGB cameras mounted on agricultural UAVs to capture orthophotos or mosaics of farmland, AI models compute vegetation indices (e.g., NDVI, NDRE) and generate a farm health-index heatmap, where colors distinguish crop vigor (red = poor, yellow = medium, green = healthy). This skill quickly identifies problem zones (e.g., nutrient/water deficiency, pests/disease, weeds) and guides precision variable-rate fertilization and crop-protection operations. Application scenarios: large-scale farms, agricultural cooperatives, drone crop-protection services, agricultural research. After the UAV flight uploads imagery, the system automatically produces a health-index map, outputs coordinates and area of problem zones, and pushes suggestions (e.g., 'NDVI is low in the northeast corner, recommend on-site pest inspection'). Skill features: traditional manual field scouting is slow and tends to miss early stress. UAV-based health-index heatmaps drastically improve monitoring efficiency, enable precise variable-rate operations, and save agro-inputs. A core technology of smart agriculture.

通过农业无人机平台搭载的多光谱或高分辨率RGB相机，采集农田的正射影像或拼接图，利用AI模型计算植被指数（如归一化植被指数NDVI、归一化红边指数NDRE等），生成农田健康指数热力图，用颜色区分作物长势（红色代表健康差、黄色代表中等、绿色代表健康）。该技能可快速识别问题区域（如缺肥、缺水、病虫害、杂草），指导精准变量施肥或植保作业。应用场景：规模化农场、农业合作社、植保无人机服务、农业科研。无人机飞行后上传影像，系统自动生成健康指数图，输出问题区域的坐标和面积，并推送建议（如'东北角区域NDVI偏低，建议实地检查虫害'）。技能特点：传统农田巡查依赖人工，效率低且难以发现早期胁迫。通过无人机快速生成健康指数热力图，可大幅提高监测效率，实现精准农业变量作业，节省农药肥料。该技能是智慧农业的核心技术之一。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的精准农业 AI。你的任务是接收无人机航拍的多光谱（或高分辨率 RGB）图像，经过拼接和几何校正后，计算植被指数（如 NDVI、NDRE、OSAVI 等），生成农田健康指数热力图，并识别出健康异常区域（如低植被指数区域），输出其位置和面积。不要提供具体的农事操作建议（如施肥量、农药品种），仅输出基于指数的评估结果。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于无人机航拍正射影像/拼接图，计算植被指数并生成农田健康指数热力图，输出异常区域坐标与面积

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 影像拼接 / 几何校正 |
| 2 | 植被指数计算（NDVI / NDRE / OSAVI / GNDVI / VARI / ExG） |
| 3 | 健康指数热力图渲染（红/黄/绿三段色阶） |
| 4 | 异常区域分割（低指数低健康） |
| 5 | 问题区域坐标多边形与面积估算（ha） |
| 6 | 作物覆盖率统计 |
| 7 | 高/中/低健康占比 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供无人机航拍正射影像/拼接图/视频 URL 或文件需要分析时，默认触发本技能进行农田健康指数图生成 |
| 🔎 明确分析意图 | 当用户明确提及无人机、UAV、多光谱、NDVI、NDRE、植被指数、农田巡查、精准农业、变量施肥、健康指数图、健康热力图、问题区域、长势监测等关键词，并且上传了影像/视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看农田健康指数历史报告、植被指数报告清单、无人机巡田报告清单、查询历史健康指数图、显示所有农田健康指数报告、显示长势监测诊断报告，查询异常区域清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_uav_farm_health_index_map_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_uav_farm_health_index_map_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备无人机航拍影像输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行农田健康指数图生成 | 调用 `-m scripts.smyx_uav_farm_health_index_map_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地无人机正射影像/拼接图/视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络无人机正射影像/拼接图/视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，农田航拍场景默认 `other` | 按需填写 |
| `--list` | 显示农田健康指数图历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_uav_farm_health_index_map_analysis.py`](scripts/smyx_uav_farm_health_index_map_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 jpg/png/tiff 影像或 mp4/avi/mov 视频，最大 10MB；建议提前完成拼接或上传单张高质量正射影像 |
| 🔎 使用提醒 | 多光谱影像需包含 NIR 波段才能计算 NDVI/NDRE 等真植被指数；纯 RGB 影像将回退使用 VARI/ExG |
| 🧑‍⚖️ 结果性质 | 分析结果仅作为田块管理与变量作业的参考，实际作业请结合现场实地踏查 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地无人机正射影像
python -m scripts.smyx_uav_farm_health_index_map_analysis --input /path/to/orthomosaic.tif

# 分析网络无人机航拍影像/视频
python -m scripts.smyx_uav_farm_health_index_map_analysis --url https://example.com/orthomosaic.tif

# 显示历史健康指数图报告/植被指数报告清单（自动触发关键词：查看农田健康指数历史报告、植被指数报告清单等）
python -m scripts.smyx_uav_farm_health_index_map_analysis --list

# 输出精简报告
python -m scripts.smyx_uav_farm_health_index_map_analysis --input ortho.tif --detail basic

# 保存结果到文件
python -m scripts.smyx_uav_farm_health_index_map_analysis --input ortho.tif --output result.json
```
