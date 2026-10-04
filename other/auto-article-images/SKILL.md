---
name: auto-article-images
description: "智能配图助手适合内容创作者、运营、technical、内容媒体在用户提出“还要配图，好麻烦”这类问题，需要快速拆解目标、判断重点并形成可执行结果时使用，帮助基于输入材料生成摘要、诊断结论、行动建议和可复用交付物。"
requiredEnvVars:
  - name: AISKILLS_API_KEY
    description: "从 AI Skills 官网 https://ai-skills.ai 获取API Key，用于运行时技能调用。"
---

# auto-article-images 智能配图助手

[快速开始](https://github.com/allinherog-star/ai-skills/tree/main#%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B)

[更多技能](https://ai-skills.ai)

### 概述

智能配图助手用于回答「还要配图，好麻烦」、配图、封面、文章图片，适合内容创作者、运营、technical、内容媒体在明确业务目标、内容材料或分析对象后调用。
它会结合正文、文章正文或 Markdown等输入，整理关键上下文，并输出摘要、诊断结论、行动建议和可复用交付物，便于继续执行、复盘或交付。

### 什么时候使用

**适用场景**

- 用户提出“还要配图，好麻烦”这类问题，需要快速拆解目标、判断重点并形成可执行结果
- 内容创作者、运营、technical、内容媒体需要围绕智能配图助手生成摘要、诊断结论、行动建议和可复用交付物
- 用户已经准备了视觉风格、标题、配图数量，希望整理成可执行的分析或优化结果
- 用户需要把智能配图助手相关材料转成清晰结论、优先级和下一步动作

### 调用方式

通过导出的 Python runner 直接调用 AI Skills API：

### 命令示例

**基础调用**

```bash
python3 scripts/run.py --params '{}'
```

**带常用参数调用**

```bash
python3 scripts/run.py --params '{"style":"clean-commercial"}'
```

### 参数说明

| 参数 | 类型 | 必填 | 默认 | 说明 |
| --- | --- | --- | --- | --- |
| `style` | string | 否 | `clean-commercial` | 视觉风格；可选值：清爽商业（`clean-commercial`）、杂志摄影（`editorial-photo`）、柔和插画（`soft-illustration`）、科技图解（`tech-diagram`） |
| `title` | string | 否 | - | 标题 |
| `imageCount` | integer | 否 | `4` | 配图数量 |
| `sourceText` | string | 否 | - | 文章正文或 Markdown |
| `coverRatios` | array | 否 | `["2.35:1","1:1","16:9","3:4","9:16"]` | 封面比例 |
| `watermarkMode` | string | 否 | `off` | 水印；可选值：不加（`off`）、右下角（`corner`）、平铺（`tiled`）、两者（`both`） |
| `sourceDocument` | string | 否 | - | 支持 docx、md、txt 等文本文件 |
| `publishPlatform` | string | 否 | `all` | 发布平台；可选值：全平台（`all`）、公众号（`wechat`）、小红书（`xhs`）、博客（`blog`）、知乎（`zhihu`） |
| `brandRequirements` | string | 否 | - | 品牌要求 |

完整机器可读参数结构见 `references/form-schema.json`。

### 参数取值参考

当前技能没有需要额外查表的分类参数。

### 支持的输入格式

当前技能直接接收 JSON 参数，不涉及分享链接解析。

### 示例请求

下面的示例参数可直接传给 `scripts/run.py`，runner 会把它们发送给 AI Skills API。

```bash
python3 scripts/run.py --params '{"style":"clean-commercial"}'
```

等价的 `--params` JSON：

```json
{
  "style": "clean-commercial"
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
      "title": "配图结果已生成",
      "summary": "已生成正文配图和多比例封面。",
      "items": [
        {
          "id": "image-package",
          "type": "attachmentGroup",
          "title": "配图文件",
          "artifactIds": [
            "content-01.webp",
            "cover-wechat-2_35x1.webp"
          ]
        }
      ],
      "artifacts": [
        {
          "id": "content-01.webp",
          "name": "content-01.webp",
          "relativePath": "content-01.webp",
          "mimeType": "image/webp",
          "url": "/api/skill-artifacts/job_demo/file/content-01.webp"
        },
        {
          "id": "cover-wechat-2_35x1.webp",
          "name": "cover-wechat-2_35x1.webp",
          "relativePath": "cover-wechat-2_35x1.webp",
          "mimeType": "image/webp",
          "url": "/api/skill-artifacts/job_demo/file/cover-wechat-2_35x1.webp"
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

- 正文配图：围绕文章主题生成可插入内容中的图片素材。
- 多比例封面：适配不同内容平台的封面使用场景。
- 图片交付包：方便继续下载、筛选、发布或二次设计。

### 结果使用建议

- 先看图片是否准确表达文章主题，再选择适合正文插入和封面展示的素材。
- 不同平台对封面比例和视觉风格要求不同，使用前建议按发布渠道做最终选择。
- 输入文章摘要、目标平台和风格偏好越清晰，生成结果越容易贴合内容。

### 运行前准备

- `AISKILLS_BASE_URL`：默认 `https://ai-skills.ai`
- `AISKILLS_API_KEY`：必填，用于认证调用
- `AISKILLS_TENANT_ID`：默认 `default`
