---
name: gemini-image
description: Gemini 图片生成与编辑 — 文生图、图编辑、自动放大 2K，支持中英文提示词。写文案/论文/报告需要配图时调用。
---

# Gemini 图片生成

使用 Google Gemini (gemini-3.1-flash-image-preview) 生成和编辑图片，默认输出 2K 分辨率。

## 使用方法

```bash
# 文生图（默认 2K）
python3 skills/gemini-image/generate-image.py "描述" --output workspace/image.png

# 指定尺寸
python3 skills/gemini-image/generate-image.py "描述" --output image.png --size 4k
python3 skills/gemini-image/generate-image.py "描述" --output image.png --size 1080x1920

# 图片编辑
python3 skills/gemini-image/generate-image.py "修改指令" --input 原图.png --output 新图.png
```

## 尺寸选项

| 值 | 说明 |
|----|------|
| `2k` | 长边 2048px（默认） |
| `4k` | 长边 3840px |
| `1080p` | 长边 1920px |
| `1k` | 长边 1024px（原始尺寸，不放大） |
| `1080x1920` | 自定义宽x高 |

## 适用场景

- **文案配图** — 公众号/小红书/博客文章插图
- **论文配图** — 流程图、示意图、概念图
- **PPT 插图** — 演示素材
- **报告封面** — 封面图、题图
- **风格转换** — 照片转插画、水彩等

## 提示词技巧

- 具体描述内容、风格、颜色、构图
- 中英文均可，英文通常效果更好
- 常用风格关键词：
  - `scientific illustration` 科学插画
  - `infographic` 信息图
  - `watercolor` 水彩
  - `minimalist` 极简
  - `flat design` 扁平设计
  - `isometric` 等距视图
  - `tech style` 科技风
  - `hand drawn` 手绘风

## 写作配图工作流

写文案/论文/报告时需要插图：
1. 根据段落内容构思配图描述
2. 用本工具生成图片
3. 图片保存到子任务工作目录
4. 在文档中引用图片路径

## 环境要求

- `GEMINI_API_KEY` 环境变量
- Python 包: `google-genai`, `Pillow`
