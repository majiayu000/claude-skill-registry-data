---
name: "smyx-eye-anomaly-detection-analysis"
description: "AI-powered pet eye anomaly detection from close-up facial images/video. Detects conjunctival redness, abnormal tearing/tear stains, and pupil/cornea opacity (cataract / corneal edema), then outputs anomaly alerts to help owners catch eye disease risks early. Scenarios: daily home health self-check, boarding center routine inspection, animal hospital triage, senior pet cataract monitoring. | 通过宠物摄像头捕捉宠物面部近景视频，利用AI视觉分析技术检测眼部充血（结膜颜色发红）、异常流泪（泪痕严重或持续性溢泪）、瞳孔区域浑浊（可能为白内障或角膜水肿）等异常征象，输出异常提示，帮助主人及早发现眼部疾病风险。适用于日常健康监测、老年宠物护理及宠物医院预检。应用场景：宠物家庭日常健康自检、宠物寄养中心巡检、宠物医院门诊初筛、老年宠物白内障监测。"
version: "1.0.21"
---

# 👁️ Pet Eye Anomaly Detection (Redness / Tearing / Cataract) | 宠物眼睛异常识别（红肿/流泪/白内障）
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **宠物眼睛异常识别（红肿/流泪/白内障）** |
| 🎯 核心目标 | 通过宠物摄像头捕捉宠物面部近景视频，利用AI视觉分析技术检测眼部充血（结膜颜色发红）、异常流泪（泪痕严重或持续性溢泪）、瞳孔区域浑浊（可能为白内障或角膜水肿）等异常征象，输出异常提示，帮助主人及早发现眼部疾病风险。适用于日常健康监测、老年宠物护理及宠物医院预检。应用场景：宠物家庭日常健康自检、宠物寄养中心巡检、宠物医院门诊初筛、老年宠物白内障监测。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_EYE_ANOMALY_DETECTION_ANALYSIS` |

AI-powered pet eye anomaly detection from close-up facial images/video. Detects conjunctival redness, abnormal tearing/tear stains, and pupil/cornea opacity (cataract / corneal edema), then outputs anomaly alerts to help owners catch eye disease risks early. Scenarios: daily home health self-check, boarding center routine inspection, animal hospital triage, senior pet cataract monitoring.

通过宠物摄像头捕捉宠物面部近景视频，利用AI视觉分析技术检测眼部充血（结膜颜色发红）、异常流泪（泪痕严重或持续性溢泪）、瞳孔区域浑浊（可能为白内障或角膜水肿）等异常征象，输出异常提示，帮助主人及早发现眼部疾病风险。适用于日常健康监测、老年宠物护理及宠物医院预检。应用场景：宠物家庭日常健康自检、宠物寄养中心巡检、宠物医院门诊初筛、老年宠物白内障监测。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的宠物眼科健康AI。你的任务是分析宠物面部近景视频或高清图像，检测双眼的结膜颜色、泪痕程度、瞳孔及角膜透明度，识别是否存在充血、异常流泪、白内障等眼部异常。不要提供医疗诊断，仅输出基于视觉的异常提示。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

通过宠物面部近景图像/视频进行双眼健康视觉评估，识别结膜充血、异常流泪、角膜/瞳孔浑浊等异常征象，输出分级异常提示

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 双眼定位 |
| 2 | 结膜颜色分析 |
| 3 | 泪痕程度评估 |
| 4 | 瞳孔/角膜透明度检测 |
| 5 | 异常征象分级 |
| 6 | 左右眼对比 |
| 7 | 健康建议输出 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供宠物面部近景图像或视频需要分析时，默认触发本技能进行眼部异常识别 |
| 🔎 明确分析意图 | 当用户明确需要眼部健康检查时，提及眼睛、结膜、充血、流泪、泪痕、白内障、角膜、瞳孔等关键词，并且上传了图像或视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史眼部检查报告、历史眼睛异常报告、眼部报告清单、显示所有眼睛报告、查询眼部健康记录 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_eye_anomaly_detection_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_eye_anomaly_detection_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备图像/视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行眼部异常识别 | 调用 `-m scripts.smyx_eye_anomaly_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看识别结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地宠物面部近景图像/视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络宠物面部近景图像/视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 宠物类型，可选值：cat/dog/other，默认 cat | 按需填写 |
| `--list` | 显示眼睛异常识别历史报告列表清单 | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 👁️ 检测项目说明

| 检测项 | 关键指标 | 可能提示的疾病方向 |
|--------|----------|--------------------|
| 🔴 结膜充血 | 结膜颜色发红、血管明显 | 结膜炎、角膜炎、过敏 |
| 💧 异常流泪 | 严重泪痕、持续溢泪 | 泪管阻塞、结膜炎、眼睑内翻 |
| 🌫️ 角膜浑浊 | 角膜出现灰白雾状 | 角膜水肿、角膜溃疡 |
| ⚪ 瞳孔浑浊 | 瞳孔区域呈现蓝白色雾状 | 白内障、晶状体硬化 |
| 👀 左右不对称 | 双眼瞳孔大小、颜色明显差异 | 神经系统问题、外伤、青光眼 |

## 🚨 异常分级与建议

| 异常等级 | 表现 | 建议 |
|----------|------|------|
| 🟢 正常 | 双眼明亮、结膜粉色、角膜清澈、无泪痕 | 持续日常监测即可 |
| 🟡 轻度异常 | 轻微泪痕或单侧轻度充血 | 观察 24-48 小时，注意环境清洁与饮食 |
| 🟠 中度异常 | 明显充血、严重泪痕或局部浑浊 | 建议尽快预约兽医检查 |
| 🔴 重度异常 | 明显角膜/瞳孔浑浊、双眼明显不对称、视力疑似受损 | ⚠️ 尽快就医，避免视力进一步损伤 |

## 💡 高风险品种与人群

| 类别 | 重点关注原因 |
|------|--------------|
| 老年宠物（>7岁） | 白内障、晶状体硬化高发 |
| 短鼻犬猫（巴哥、英斗、波斯、加菲等） | 眼球突出，易角膜损伤、泪溢 |
| 长毛品种（比熊、博美、贵宾、波斯） | 毛发刺激易引发流泪、结膜炎 |
| 糖尿病患宠 | 易并发糖尿病性白内障 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_eye_anomaly_detection_analysis.py`](scripts/smyx_eye_anomaly_detection_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 支持 jpg/png/mp4/avi/mov 格式，最大 10MB |
| 🔎 使用提醒 | **拍摄要求**：面部近景、光线充足、双眼清晰；模糊/逆光/眼睛闭合的图像无法得出可靠结果 |
| 🧑‍⚖️ 结果性质 | **识别结果仅供视觉参考，绝不替代专业兽医诊断**；任何疑似异常都建议就医确诊 |
| 🔎 使用提醒 | 部分品种眼部生理特征本身偏红或泪痕较重，需结合个体基线判断 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载 |
| 📜 报告输出 | 当显示历史识别报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地宠物面部近景图像/视频
python -m scripts.smyx_eye_anomaly_detection_analysis --input /path/to/pet_face.jpg --pet-type cat

# 分析网络宠物面部近景图像/视频
python -m scripts.smyx_eye_anomaly_detection_analysis --url https://example.com/pet_face.mp4 --pet-type dog

# 显示历史识别报告/显示报告清单列表（自动触发关键词：查看历史眼部检查报告、眼部报告清单等）
python -m scripts.smyx_eye_anomaly_detection_analysis --list

# 输出精简报告
python -m scripts.smyx_eye_anomaly_detection_analysis --input eye.jpg --pet-type cat --detail basic

# 保存结果到文件
python -m scripts.smyx_eye_anomaly_detection_analysis --input eye.jpg --pet-type cat --output result.json
```
