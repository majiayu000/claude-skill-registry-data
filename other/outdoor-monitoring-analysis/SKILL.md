---
name: "outdoor-monitoring-analysis"
description: "Detects targets such as people, vehicles, non-motorized vehicles, and pets within target areas; supports batch image analysis, suitable for outdoor surveillance scenarios like courtyards, orchards, and farms. | 户外看护智能监测分析技能，检测目标区域内的人、车、非机动车、宠物等目标，支持批量图片分析，适用于庭院、果园、养殖场等户外区域看护场景"
version: "1.0.22"
---

# 🏞️ Intelligent Outdoor Care Monitoring & Analysis Tool | 户外看护智能监测分析工具
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **户外看护智能监测分析工具** |
| 🎯 核心目标 | 户外看护智能监测分析技能，检测目标区域内的人、车、非机动车、宠物等目标，支持批量图片分析，适用于庭院、果园、养殖场等户外区域看护场景 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `OUTDOOR_MONITORING` |

Equipped with advanced AI recognition algorithms, this feature conducts 24/7 automated monitoring of expansive outdoor
areas such as courtyards, orchards, and breeding farms. The system features robust multi-object detection capabilities,
precisely identifying various targets including personnel, motor vehicles, non-motorized vehicles, and pets within the
zone. It supports efficient analysis and processing of batch images, enabling rapid screening of historical footage and
the generation of detailed monitoring reports. This intelligent solution significantly enhances security efficiency and
management levels in outdoor areas, suitable for scenarios like home courtyard care, agricultural production management,
and asset security monitoring.

本功能搭载先进的AI智能识别算法，能够对庭院、果园、养殖场等户外广阔区域进行全天候自动化监测。系统具备强大的多目标检测能力，可精准识别区域内的人员、机动车辆、非机动车辆以及宠物等多种目标对象。支持批量图片的高效分析与处理，能够快速筛查历史影像数据，生成详细的监测报告。这一智能化解决方案极大地提升了户外区域的安防效率与管理水平，适用于家庭庭院看护、农业生产管理及资产安全监控等多种场景

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals

### 1. 🧩 技能用途

通过户外监控图片/视频进行目标检测，识别区域内出现的人、车、非机动车、宠物等闯入目标

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 多目标检测 |
| 2 | 目标分类 |
| 3 | 数量统计 |
| 4 | 入侵判定 |
| 5 | 风险等级评估 |
| 6 | 异常闯入预警 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供户外监控图片/视频需要检测闯入目标时，默认触发本技能进行户外看护分析 |
| 🔎 明确分析意图 | 当用户明确需要进行户外看护、入侵检测时，提及庭院看护、果园监控、目标检测、户外安防等关键词，并且上传了图片或视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史监测报告、户外看护报告清单、监测报告列表、查询历史监测报告、显示所有监测报告、户外监测分析报告，查询户外看护智能监测分析报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.outdoor_monitoring --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.outdoor_monitoring --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备图片/视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行户外看护智能监测分析 | 调用 `-m scripts.outdoor_monitoring` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地图片/视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络图片/视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--list` | 显示历史户外看护监测分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/outdoor_monitoring.py`](scripts/outdoor_monitoring.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 支持格式：jpg/jpeg/png/mp4/avi/mov，最大 10MB，支持批量图片分析 |
| 🧑‍⚖️ 结果性质 | 分析结果仅供安防参考，不能替代专业安保措施，发现可疑闯入请及时报警 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析单张监控图片
python -m scripts.outdoor_monitoring --input /path/to/yard.jpg 分析网络监控视频
python -m scripts.outdoor_monitoring --url https://example.com/garden.mp4 显示历史分析报告/显示分析报告清单列表/显示历史监测报告（自动触发关键词：查看历史监测报告、历史报告、监测报告清单等）
python -m scripts.outdoor_monitoring --list

# 输出精简报告
python -m scripts.outdoor_monitoring --input capture.jpg --detail basic

# 保存结果到文件
python -m scripts.outdoor_monitoring --input capture.jpg --output result.json
```
