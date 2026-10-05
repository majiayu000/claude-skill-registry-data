---
name: od-video-gen
description: 按描述生成视频文件（mp4）并保存到项目中，适合宣传片段、概念演示和动态视觉稿。
---

# 视频生成（PilotDeck 内置）

当用户明确说「生成视频」「出一段 MP4」时，调用 `generate_video`。

## 输入建议
- `prompt`: 描述场景、镜头语言、风格、运动趋势。
- `duration_seconds`: 常见 5-15 秒。
- `aspect_ratio`: 常见 `16:9`、`9:16`。
- `output_path`: 建议落到 `artifacts/media/` 下。

## 示例
- 生成一段 8 秒科技感开场动画，蓝紫渐变背景，粒子向中心汇聚后出现 LOGO。
- 生成一段 10 秒竖屏产品展示视频，镜头从细节拉远到全貌。
