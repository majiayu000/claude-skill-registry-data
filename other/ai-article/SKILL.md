---
name: ai-article
description: "自动图文助手适合内容创作者、运营、technical、内容媒体在用户提出“自动公众号和种草”这类问题，需要快速拆解目标、判断重点并形成可执行结果时使用，帮助基于输入材料生成摘要、诊断结论、行动建议和可复用交付物。"
requiredEnvVars:
  - name: AISKILLS_API_KEY
    description: "从 AI Skills 官网 https://ai-skills.ai 获取API Key，用于运行时技能调用。"
---

# ai-article 小红书种草笔记（自动配图）

[快速开始](https://github.com/allinherog-star/ai-skills/tree/main#%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B)

[更多技能](https://ai-skills.ai)

### 概述

自动图文助手用于回答「自动公众号和种草」、图文、写作、配图，适合内容创作者、运营、technical、内容媒体在明确业务目标、内容材料或分析对象后调用。
它会结合主题、文章主题、关键词或一句话需求等输入，整理关键上下文，并输出摘要、诊断结论、行动建议和可复用交付物，便于继续执行、复盘或交付。

### 什么时候使用

**适用场景**

- 用户提出“自动公众号和种草”这类问题，需要快速拆解目标、判断重点并形成可执行结果
- 内容创作者、运营、technical、内容媒体需要围绕自动图文助手生成摘要、诊断结论、行动建议和可复用交付物
- 用户已经准备了语气、主题（文章主题、关键词或一句话需求）、目标读者，希望整理成可执行的分析或优化结果
- 用户需要把自动图文助手相关材料转成清晰结论、优先级和下一步动作

### 调用方式

通过导出的 Python runner 直接调用 AI Skills API：

### 命令示例

**按必填参数调用**

```bash
python3 scripts/run.py --params '{"topic":"主题"}'
```

### 参数说明

| 参数 | 类型 | 必填 | 默认 | 说明 |
| --- | --- | --- | --- | --- |
| `tone` | string | 否 | `practical` | 语气；可选值：实用清晰（`practical`）、故事化（`story`）、专家型（`expert`）、轻松活泼（`lively`） |
| `topic` | string | 是 | - | 文章主题、关键词或一句话需求 |
| `audience` | string | 否 | - | 目标读者 |
| `keywords` | string | 否 | - | 关键词 |
| `platform` | string | 否 | `all` | 发布平台；可选值：全平台（`all`）、公众号（`wechat`）、小红书（`xhs`）、博客（`blog`）、知乎（`zhihu`） |
| `wordCount` | integer | 否 | `1600` | 字数 |
| `imageCount` | integer | 否 | `3` | 正文配图数量 |
| `watermarkMode` | string | 否 | `off` | 水印；可选值：不加（`off`）、品牌轻水印（`brand`）、右下角（`corner`）、平铺（`tiled`）、两者（`both`） |
| `watermarkText` | string | 否 | `ai-skills.ai` | 选择加水印后显示，默认使用 ai-skills.ai，可替换为品牌名、站点或账号 |
| `brandRequirements` | string | 否 | - | 品牌要求 |

完整机器可读参数结构见 `references/form-schema.json`。

### 参数取值参考

当前技能没有需要额外查表的分类参数。

### 支持的输入格式

当前技能直接接收 JSON 参数，不涉及分享链接解析。

### 示例请求

下面的示例参数可直接传给 `scripts/run.py`，runner 会把它们发送给 AI Skills API。

```bash
python3 scripts/run.py --params '{"topic":"主题"}'
```

等价的 `--params` JSON：

```json
{
  "topic": "主题"
}
```

### 返回结果示例

```json
{
  "success": true,
  "data": {
    "mode": "async",
    "status": "completed",
    "resultEnvelope": {
      "status": "completed",
      "title": "自动图文已生成",
      "summary": "已生成文章正文、正文配图和多比例封面。",
      "items": [
        {
          "id": "article",
          "type": "markdown",
          "title": "文章正文",
          "artifactIds": [
            "ai-skills-auto-image-article.md"
          ]
        }
      ],
      "artifacts": [
        {
          "id": "ai-skills-auto-image-article.md",
          "name": "ai-skills-auto-image-article.md",
          "relativePath": "ai-skills-auto-image-article.md",
          "mimeType": "text/markdown",
          "url": "/api/skill-artifacts/job_demo/file/ai-skills-auto-image-article.md"
        },
        {
          "id": "content-01.webp",
          "name": "content-01.webp",
          "relativePath": "content-01.webp",
          "mimeType": "image/webp",
          "url": "/api/skill-artifacts/job_demo/file/content-01.webp"
        }
      ],
      "presentation": {
        "mode": "single"
      }
    },
    "zipUrl": "/api/skill-artifacts/job_demo/archive"
  },
  "meta": {
    "executionTime": 842,
    "cached": false
  }
}
```

### 交付内容

- 完整中文图文文章：包含标题、正文结构、段落内容和适合发布的 Markdown 文稿。
- 文章配图与封面素材：用于公众号、博客或内容平台的视觉配套。
- 可下载交付包：便于把正文和图片继续交给编辑、发布或归档流程。

### 结果使用建议

- 先检查标题、开头和分段结构是否贴合目标读者，再判断正文是否适合直接发布。
- 配图和封面用于提升可读性与传播感，发布前仍建议结合品牌风格做最后筛选。
- 如果用户已有关键词、受众或平台要求，尽量在输入里明确说明。

### 运行前准备

- `AISKILLS_BASE_URL`：默认 `https://ai-skills.ai`
- `AISKILLS_API_KEY`：必填，用于认证调用
- `AISKILLS_TENANT_ID`：默认 `default`
