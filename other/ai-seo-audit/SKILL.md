---
name: ai-seo-audit
description: "SEO 审计助手适合technical、产品、市场营销、software在用户提出“网站 SEO 健康吗”这类问题，需要快速拆解目标、判断重点并形成可执行结果时使用，帮助基于输入材料生成SEO 诊断、优先级建议、发布检查清单。"
requiredEnvVars:
  - name: AISKILLS_API_KEY
    description: "从 AI Skills 官网 https://ai-skills.ai 获取API Key，用于运行时技能调用。"
---

# ai-seo-audit SEO 审计助手

[快速开始](https://github.com/allinherog-star/ai-skills/tree/main#%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B)

[更多技能](https://ai-skills.ai)

### 概述

SEO 审计助手用于回答「网站 SEO 健康吗」、性能诊断、网站质量、体验指标，适合technical、产品、市场营销、software在明确业务目标、内容材料或分析对象后调用。
它会结合页面、关键词或内容资料、粘贴页面内容、关键词、站点结构、搜索目标、竞品摘要或优化问题。等输入，整理关键上下文，并输出SEO 诊断、优先级建议、发布检查清单，便于继续执行、复盘或交付。
能力定位补充：热榜营销类高频 skill，可改造成页面和内容 SEO/GEO 审核工具。

### 什么时候使用

**适用场景**

- 用户提出“网站 SEO 健康吗”这类问题，需要快速拆解目标、判断重点并形成可执行结果
- technical、产品、市场营销、software需要围绕SEO 审计助手生成SEO 诊断、优先级建议、发布检查清单
- 用户已经准备了优化目标（说明要提升的关键词、搜索意图、可见性、引用机会或转化目标。）、目标受众（说明搜索用户、目标市场、行业、购买阶段或内容受众。）、页面或站点链接（填写公开可访问的页面、站点、SERP、竞品或参考链接。），希望整理成可执行的分析或优化结果
- 用户需要把SEO 审计助手相关材料转成清晰结论、优先级和下一步动作

### 调用方式

通过导出的 Python runner 直接调用 AI Skills API：

### 命令示例

**基础调用**

```bash
python3 scripts/run.py --params '{}'
```

**带常用参数调用**

```bash
python3 scripts/run.py --params '{"goal":"优化目标"}'
```

### 参数说明

| 参数 | 类型 | 必填 | 默认 | 说明 |
| --- | --- | --- | --- | --- |
| `goal` | string | 否 | - | 说明要提升的关键词、搜索意图、可见性、引用机会或转化目标 |
| `audience` | string | 否 | - | 说明搜索用户、目标市场、行业、购买阶段或内容受众 |
| `materialUrl` | string | 否 | - | 填写公开可访问的页面、站点、SERP、竞品或参考链接；需要传可访问的完整 URL |
| `materialFile` | string | 否 | - | 上传内容稿、关键词表、站点结构、审计报告或 SEO 规划资料 |
| `materialText` | string | 否 | - | 粘贴页面内容、关键词、站点结构、搜索目标、竞品摘要或优化问题 |
| `brandRequirements` | string | 否 | - | 补充目标地区、语言、品牌限制、不可改动事实、合规要求或人工复核重点 |

完整机器可读参数结构见 `references/form-schema.json`。

### 参数取值参考

当前技能没有需要额外查表的分类参数。

### 支持的输入格式

当前技能直接接收 JSON 参数；如果参数里包含链接字段，请传完整、可访问的 URL。

### 示例请求

下面的示例参数可直接传给 `scripts/run.py`，runner 会把它们发送给 AI Skills API。

```bash
python3 scripts/run.py --params '{"goal":"优化目标"}'
```

等价的 `--params` JSON：

```json
{
  "goal": "优化目标"
}
```

### 返回结果示例

```json
{
  "success": true,
  "data": {
    "message": "示例结果请以技能真实返回结构为准。"
  },
  "meta": {
    "executionTime": 842,
    "cached": false
  }
}
```

### 交付内容

- SEO 诊断、优先级建议、发布检查清单：围绕用户目标整理可直接阅读、复盘或交付的核心结果。
- 输入材料解读：结合优化目标（说明要提升的关键词、搜索意图、可见性、引用机会或转化目标。）、目标受众（说明搜索用户、目标市场、行业、购买阶段或内容受众。）、页面或站点链接（填写公开可访问的页面、站点、SERP、竞品或参考链接。）提炼关键上下文和判断依据。
- 下一步动作：给出优先级、执行建议或可继续加工的内容框架。

### 结果使用建议

- 先判断输出是否回答了用户关于「SEO 审计助手」的核心问题。
- 再检查结果是否覆盖SEO 诊断、优先级建议、发布检查清单，以及是否给出明确下一步动作。
- 如果输入材料较少，建议让用户补充目标、受众、限制条件或原始材料后再运行。

### 运行前准备

- `AISKILLS_BASE_URL`：默认 `https://ai-skills.ai`
- `AISKILLS_API_KEY`：必填，用于认证调用
- `AISKILLS_TENANT_ID`：默认 `default`
