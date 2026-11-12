---
name: "smyx-grooming-effectiveness-analysis"
description: "Triggers when a user provides a pet grooming area video or image URL/file for analysis; supports local uploads or network URLs to call server-side APIs for coat condition and shed hair recognition, detecting matting area ratio and shed hair volume to output hairball risk level, helping prevent hairball syndrome. Application scenarios: smart grooming tools, long-haired pet care, pet health management. | 当用户提供梳毛器区域的视频/图像URL或文件时，触发本技能进行毛发表面状态分析；支持通过上传本地视频/图片或网络URL，调用服务端API进行识别，检测打结面积占比、梳下毛发量（堆积面积），输出毛球风险等级，帮助预防毛球症。应用场景：智能梳毛器、长毛宠物护理、宠物健康管理。"
version: "1.0.22"
---

# 🪮 Pet Grooming Effectiveness & Hairball Risk Analysis | 宠物梳毛器梳理效果与毛球风险分析
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **宠物梳毛器梳理效果与毛球风险** |
| 🎯 核心目标 | 当用户提供梳毛器区域的视频/图像URL或文件时，触发本技能进行毛发表面状态分析；支持通过上传本地视频/图片或网络URL，调用服务端API进行识别，检测打结面积占比、梳下毛发量（堆积面积），输出毛球风险等级，帮助预防毛球症。应用场景：智能梳毛器、长毛宠物护理、宠物健康管理。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_GROOMING_EFFECTIVENESS_ANALYSIS` |

Triggers when a user provides a pet grooming area video or image URL/file for analysis; supports local uploads or
network URLs to call server-side APIs for coat condition and shed hair recognition, detecting matting area ratio and
shed hair volume to output hairball risk level, helping prevent hairball syndrome. Application scenarios: smart grooming
tools, long-haired pet care, pet health management.

当用户提供梳毛器区域的视频/图像URL或文件时，触发本技能进行毛发表面状态分析；支持通过上传本地视频/图片或网络URL，调用服务端API进行识别，检测打结面积占比、梳下毛发量（堆积面积），输出毛球风险等级，帮助预防毛球症。应用场景：智能梳毛器、长毛宠物护理、宠物健康管理。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | 假设你是一个专业的宠物护理分析AI。你的任务是基于梳毛器区域的视频/图像（梳毛前后），分析宠物毛发的打结程度和梳下的毛发量，评估毛球症风险等级。不要提供医疗诊断或治疗方案，仅客观描述观察到的毛发状态。 |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals

### 1. 🧩 技能用途

通过梳毛器区域视频/图像进行宠物毛发状态分析，获取标准化的梳理效果评估和毛球风险等级

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 视频/图像分析 |
| 2 | 毛发打结面积检测 |
| 3 | 梳下毛发量估算 |
| 4 | 毛球风险等级评估 |
| 5 | 梳理效果评分 |
| 6 | 历史趋势对比 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供梳毛器区域视频/图像 URL 或文件需要分析时，默认触发本技能进行梳理效果与毛球风险分析 |
| 🔎 明确分析意图 | 当用户明确需要进行毛发/梳毛监测时，提及梳毛、毛发打结、掉毛量、毛球症、毛球风险、梳理效果、长毛护理、换毛期等关键词，并且上传了视频文件或者图片文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史梳毛报告、历史梳理报告、毛球风险报告清单、梳毛分析报告清单、查询历史毛发报告、显示所有梳毛报告、显示毛球风险报告，查询健康风险提示报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_grooming_effectiveness_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_grooming_effectiveness_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备视频/图像输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行梳理效果与毛球风险分析 | 调用 `-m scripts.smyx_grooming_effectiveness_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地视频/图片文件路径 | 适用于本地文件分析 |
| `--url` | 网络视频/图片 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 宠物类型，可选值：cat/dog/bird/other，默认 cat | 按需填写 |
| `--list` | 显示梳毛历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 📊 分析指标说明

| 指标     | 说明                     | 风险参考                                   |
|--------|------------------------|----------------------------------------|
| 打结面积占比 | 毛发表面可见打结/缠结区域占总体表面积的比例 | <5% 低风险；5-15% 中风险；15-30% 高风险；>30% 极高风险 |
| 打结严重程度 | 基于打结密度和深度的综合分级         | 轻度（表面浮毛纠缠）/ 中度（形成毛片）/ 重度（贴皮毛毡化）        |
| 梳下毛发量  | 梳毛后脱落在梳毛器/周围的毛发堆积量     | 少量（正常代谢）/ 中量（换毛期）/ 大量（异常脱毛需关注）         |
| 梳理效果评分 | 梳毛前后毛发平整度改善程度（0-100）   | >80 梳理充分；60-80 基本到位；<60 需补充梳理          |
| 毛球风险等级 | 基于打结程度、掉毛量和宠物品种的综合评估   | 低 / 中 / 高 / 极高                         |
| 历史趋势   | 与近期报告对比的打结和掉毛变化趋势      | 持续加重需关注换毛期或皮肤问题                        |

## 🐱 毛球风险等级定义

| 风险等级  | 判定条件                  | 建议措施              |
|-------|-----------------------|-------------------|
| 🟢 低  | 打结<5%，梳下毛量少，短毛或已充分梳理  | 维持当前梳理频率即可        |
| 🟡 中  | 打结5-15%，梳下毛量中等，轻度缠结   | 适当增加梳理频次，关注换毛期    |
| 🟠 高  | 打结15-30%，梳下毛量较大，有明显毛片 | 增加每日梳理，考虑化毛膏辅助    |
| 🔴 极高 | 打结>30%，梳下毛量很大，贴皮毡化    | 需专业美容处理，高度关注毛球症风险 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_grooming_effectiveness_analysis.py`](scripts/smyx_grooming_effectiveness_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 视频要求：支持 mp4/avi/mov 格式，最大 10MB；图片支持 jpg/png 格式 |
| 🧑‍⚖️ 结果性质 | 分析结果仅供护理参考，不提供医疗诊断或治疗方案 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 🧑‍⚖️ 结果性质 | 梳下毛发量评估基于视觉面积/体积估算，非精确称重，仅供参考 |
| 🔎 使用提醒 | 长毛品种（波斯猫、布偶猫、金毛犬等）建议适当提高梳理频率和关注等级 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地梳毛器视频
python -m scripts.smyx_grooming_effectiveness_analysis --input /path/to/grooming_video.mp4 --pet-type cat

# 分析网络梳毛器视频
python -m scripts.smyx_grooming_effectiveness_analysis --url https://example.com/grooming_video.mp4 --pet-type cat

# 显示历史分析报告/显示分析报告清单列表/显示历史梳毛报告（自动触发关键词：查看历史梳毛报告、历史报告、梳毛报告清单等）
python -m scripts.smyx_grooming_effectiveness_analysis --list

# 输出精简报告
python -m scripts.smyx_grooming_effectiveness_analysis --input video.mp4 --pet-type cat --detail basic

# 保存结果到文件
python -m scripts.smyx_grooming_effectiveness_analysis --input video.mp4 --pet-type cat --output result.json
```
