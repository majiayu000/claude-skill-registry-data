---
name: "package-detection-analysis"
description: "Detects the presence of delivery packages within the target surveillance area; suitable for inventory checks and unattended alerts at community stations, residential entrances, and office building lobbies. | 包裹检测技能，检测目标监控区域内是否出现快递包裹，适用于社区驿站、小区门口、写字楼前台快递盘点和无人值守提醒"
version: "1.0.23"
---

# 📦 Package Detection Skill | 包裹检测技能
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **包裹检测技能** |
| 🎯 核心目标 | 包裹检测技能，检测目标监控区域内是否出现快递包裹，适用于社区驿站、小区门口、写字楼前台快递盘点和无人值守提醒 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `PACKAGE_DETECTION` |

Equipped with advanced video analysis algorithms, this feature conducts non-contact intelligent monitoring of daily
activities for patients with chronic diseases such as Parkinson's disease. By capturing and analyzing typical motor
features like limb tremors, convulsions, muscle rigidity, and gait abnormalities, the system automatically identifies
disease fluctuations or potential risks. This technology extends professional clinical observation into the home
setting, helping doctors remotely grasp symptom changes and providing objective evidence for adjusting treatment plans,
thereby achieving a shift from passive medical treatment to active health management.

本功能基于先进的计算机视觉技术，能够对社区驿站、小区门口及写字楼前台等指定监控区域进行全天候智能扫描。系统可精准识别区域内出现的快递包裹，自动判断包裹的有无及滞留状态。该功能完美适配快递盘点与无人值守提醒场景，一旦检测到新包裹到达或异常滞留，即刻触发通知，有效解决了传统人工巡查效率低、易漏件的问题，显著提升了物流末端的管理效率与安全性

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals

### 1. 🧩 技能用途

检测图片/视频监控场景中的快递包裹，统计包裹数量，长时间未取件触发提醒

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 包裹检测 |
| 2 | 数量统计 |
| 3 | 位置标定 |
| 4 | 超时未取提醒 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供监控图片/视频需要检测快递包裹时，默认触发本技能 |
| 🔎 明确分析意图 | 当用户明确需要包裹检测、快递盘点时，提及包裹检测、快递识别、驿站盘点、未取包裹等关键词，并且上传了图片/视频 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史检测报告、包裹检测报告清单、检测报告列表、查询历史检测报告、显示所有检测报告、包裹分析报告，查询包裹检测分析报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.package_detection_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.package_detection_analysis --list` 调用 API 查询云端的历史报告数据 |
| 🚫 严格禁止 | 从本地 `memory` 目录读取历史会话信息 |
| 🚫 严格禁止 | 手动汇总本地记录中的报告 |
| 🚫 严格禁止 | 从长期记忆中提取报告 |
| ✅ 输出格式 | 必须统一从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果 |

## 📦 前置准备 | Requirements
- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 📸 检测要求 | Detection Requirements
| 要求项 | 说明 |
|---|---|
| 监控摄像头固定位置 | ，覆盖驿站/门口/前台指定摆放区域 |
| 光线充足清晰 | ，包裹完整可见，避免被桌椅和杂物大面积遮挡 |
| 定期盘点场景建议固定时段拍摄，便于统计对比 | 定期盘点场景建议固定时段拍摄，便于统计对比 |

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
| 1 | 📥 准备监控图片/视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行包裹检测分析 | 调用 `-m scripts.package_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地图片/视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络图片/视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--list` | 显示历史包裹检测分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/package_detection_analysis.py`](scripts/package_detection_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 支持格式：jpg/jpeg/png/mp4/avi/mov，最大 10MB |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 检测本地驿站监控图片
python -m scripts.package_detection_analysis --input /path/to/station.jpg 检测本地监控视频
python -m scripts.package_detection_analysis --input /path/to/entrance.mp4 检测网络图片
python -m scripts.package_detection_analysis --url https://example.com/front_desk.jpg 显示历史检测报告/显示检测报告清单列表/显示历史包裹检测（自动触发关键词：查看历史检测报告、历史报告、检测报告清单等）
python -m scripts.package_detection_analysis --list

# 输出精简报告
python -m scripts.package_detection_analysis --input station.jpg --detail basic

# 保存结果到文件
python -m scripts.package_detection_analysis --input station.jpg --output result.json
```
