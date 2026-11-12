---
name: "smyx-thermal-fever-screening-analysis"
description: "Using a fixed thermal-imaging camera installed in public areas (e.g., living room, dining room), the system automatically analyzes each person's skin-surface temperature (usually forehead or facial region) when multiple people gather, and computes the difference between an individual's temperature and the average temperature of others in the scene. | 通过安装于公共区域（如客厅、餐厅）的固定热成像摄像头，在多人聚集时自动分析每个人的体表温度（通常为额头或面部区域），计算个体温度与场景内其他人平均温度的差值。当某个人温度显著高于周边人群（差值超过预设阈值，如1.5℃）时，输出'体温相对异常'提醒，建议使用额温枪复测。"
version: "1.0.23"
---

# 🌡️ Thermal Relative Fever Screening (Multi-Person Gathering) | 家庭多人聚集时体温相对异常检测
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **家庭多人聚集时体温相对异常检测** |
| 🎯 核心目标 | 通过安装于公共区域（如客厅、餐厅）的固定热成像摄像头，在多人聚集时自动分析每个人的体表温度（通常为额头或面部区域），计算个体温度与场景内其他人平均温度的差值。当某个人温度显著高于周边人群（差值超过预设阈值，如1.5℃）时，输出'体温相对异常'提醒，建议使用额温枪复测。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_THERMAL_FEVER_SCREENING_ANALYSIS` |

Using a fixed thermal-imaging camera installed in public areas (e.g., living room, dining room), the system automatically analyzes each person's skin-surface temperature (usually forehead or facial region) when multiple people gather, and computes the difference between an individual's temperature and the average temperature of others in the scene. When someone's temperature is significantly higher than the surrounding group (delta exceeds a preset threshold, e.g., 1.5 °C), it outputs a 'relative temperature anomaly' alert and recommends rechecking with a calibrated forehead thermometer. The skill is suitable for family gatherings, small meetings, etc., and aids early screening of people with fever. Application scenarios: family living rooms, meeting rooms, kindergarten activity rooms, nursing-home activity areas. The system monitors in real time; when someone's temperature is clearly higher than others, it pushes a mobile-app alert to remind attention to health. Skill features: during flu season or epidemics, if a household member has a fever during gatherings, quick screening enables timely precautions. Relative-temperature detection reduces reliance on absolute-temperature calibration, allowing ordinary families to use a thermal-imaging camera for health monitoring. Can be integrated into smart-home security systems to strengthen family health protection.

通过安装于公共区域（如客厅、餐厅）的固定热成像摄像头，在多人聚集时自动分析每个人的体表温度（通常为额头或面部区域），计算个体温度与场景内其他人平均温度的差值。当某个人温度显著高于周边人群（差值超过预设阈值，如1.5℃）时，输出'体温相对异常'提醒，建议使用额温枪复测。该技能适用于家庭聚会、小型会议等场景，辅助早期筛查发热人员。应用场景：家庭客厅、会议室、幼儿园活动室、养老院活动区。系统实时监测，当检测到某人体温明显高于他人时，通过手机APP推送提醒，提示注意健康状态。技能特点：在流感季节或疫情期间，家庭聚会中若有成员发热，可快速筛查并采取防护措施。通过相对温度检测，可降低对绝对温度校准的要求，使普通家庭也能使用热成像摄像头进行健康监测。该技能可集成到智能家居安防系统中，提升家庭健康防护能力。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的群体体温筛查 AI。你的任务是分析固定热成像摄像头拍摄的多人聚集视频，检测每个个体的体表温度（头部区域），计算个体温度与同期场景内所有个体平均温度的差值。当差值超过预设阈值时，输出相对温度异常提醒。不要提供医疗诊断或具体疾病判定，仅输出基于热成像的相对温度差异与方向性提醒。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于热成像摄像头多人聚集视频，自动检测每个人额头体表温度 → 计算个体相对群体均值的差值 → 输出相对体温异常提醒并建议额温枪复测

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 多人体检测与身份编号 |
| 2 | 头部/额头 ROI 定位 |
| 3 | 热成像像素 → 温度（°C）换算 |
| 4 | 群体均值/标准差统计 |
| 5 | 个体 - 群体差值计算 |
| 6 | 相对异常判定（默认 \| Δ \| > 1.5 °C） |
| 7 | 有效样本数校验 |
| 8 | 持续时间过滤（≥ 3 秒） |
| 9 | APP 推送文本生成 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供热成像摄像头多人聚集视频 URL 或文件需要分析时，默认触发本技能进行体温相对异常筛查 |
| 🔎 明确分析意图 | 当用户明确提及发热筛查、体温相对异常、热成像、群体测温、家庭聚会健康、流感季节、疫情防控、幼儿园/养老院测温等关键词，并且上传了热成像视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看体温筛查历史报告、发热相对异常报告清单、群体测温报告清单、查询历史筛查记录、显示所有体温筛查报告、显示家庭聚会健康报告，查询体温异常预警清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_thermal_fever_screening_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_thermal_fever_screening_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备热成像摄像头多人聚集视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行多人聚集体温相对异常检测 | 调用 `-m scripts.smyx_thermal_fever_screening_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地热成像摄像头多人聚集视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络热成像摄像头多人聚集视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，群体体温筛查场景默认 `other` | 按需填写 |
| `--list` | 显示家庭多人聚集体温相对异常历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_thermal_fever_screening_analysis.py`](scripts/smyx_thermal_fever_screening_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：必须是热成像（红外测温）摄像头视频，普通可见光视频无法识别温度 |
| 🔎 使用提醒 | **本工具仅基于"群体相对差异"判定，不依赖绝对温度校准**；任何相对异常都建议使用经过校准的医用额温枪/电子体温计复测 |
| 🔎 使用提醒 | 戴帽子/口罩、刚运动/喝热饮/晒太阳、紧邻空调或取暖器等情况会显著影响额头体表温度，可能造成误报 |
| 🔏 隐私合规 | 隐私合规：热成像家庭视频涉及个人健康隐私，使用前需取得家庭成员/参与者知情同意，妥善加密保管 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地热成像多人聚集视频
python -m scripts.smyx_thermal_fever_screening_analysis --input /path/to/thermal.mp4

# 分析网络热成像多人聚集视频
python -m scripts.smyx_thermal_fever_screening_analysis --url https://example.com/thermal.mp4

# 显示历史体温相对异常报告（自动触发关键词：查看体温筛查历史报告、发热相对异常报告清单等）
python -m scripts.smyx_thermal_fever_screening_analysis --list

# 输出精简报告
python -m scripts.smyx_thermal_fever_screening_analysis --input thermal.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_thermal_fever_screening_analysis --input thermal.mp4 --output result.json
```
