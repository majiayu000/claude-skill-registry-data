---
name: studio-creation
description: Route a DSH creative request to Qwen images, MiniMax H3 clips or a reviewed multi-shot film. Pass an actual image attachment between tools.
whenToUse: 用户要求解释创作插件用法、先画再拍、从一张图制作视频、选择单镜或长片流程时使用。
---

# 从图像到影片

只请求安装、连服务器或检查权重时，使用 `studio-model-setup`。用户只要提示词或分镜方案时，直接交付文字。开始创作后按以下入口工作。

- **图像**。使用 `qwen-image`。外部图片先用 `qwen_image_import` 得到资源 ID，编辑前用 `qwen_image_resources` 确认当前后端支持所需模式。用 `qwen_generate_image` 提交，需要恢复时按返回的图像任务 ID 调 `qwen_image_status`。
- **一张图接一镜**。从图像生成或状态工具的结果取 `attachment.attachmentId`（完整的 `sha256:…`），传给 `h3_generate_video.reference_images` 数组。在 prompt 用 `<Picture 1>` 指向这张图，交代动作、镜头运动和现场声音。选择 quality480 或 quality768。图像任务 ID、图库资源 ID、文件路径不能当作视频附件 ID。图像是身份或物体参考，首帧构图由 H3 生成。
- **单镜视频**。使用 `h3-video`。无参考时可用 turbo480 做带声音的预览，再按要求做质量档；按原视频 ID 调 `h3_video_status`，完成后原样返回 playback_markdown。
- **多镜头成片**。使用 `h3-long-film`。有固定角色时先存角色卡，再按目标时长创建一个项目，保留项目 ID。用 `h3_film_next` 推进，基于真实素材调用 `h3_film_review`，直到母版可播放。只在实际完成视听终审后登记最终意见。

例：「先画一只蓝瓷杯，再让杯口冒出热气，拍五秒。」先取 Qwen 完成图的附件 ID，然后调用 H3，秒数为 5，参考图为该 ID，提示词指定蒸汽上升与现场声。共用一块 GPU 时先等待上一任务完成。
